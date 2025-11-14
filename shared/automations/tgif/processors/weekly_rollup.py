"""
Weekly Rollup Generator - Runs Friday at 3pm to generate weekly digest
"""

import os
import json
import schedule
import time
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import components
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from task_tracker.tracker import TaskTracker


class WeeklyRollupGenerator:
    """Generate weekly digest from meetings and emails"""
    
    def __init__(self):
        self.knowledge_base = os.getenv('KNOWLEDGE_BASE_PATH', 'focuses/hcss/knowledge')
        self.task_tracker = TaskTracker()
    
    def run(self):
        """Main processing function - runs Friday at 3pm"""
        logger.info("="*60)
        logger.info(f"Starting weekly rollup generation at {datetime.now()}")
        logger.info("="*60)
        
        try:
            # Get week date range
            week_start, week_end = self.get_week_range()
            logger.info(f"Week: {week_start} to {week_end}")
            
            # Collect all sources
            meetings = self.get_meeting_summaries(week_start, week_end)
            email_batches = self.get_daily_email_batches(week_start, week_end)
            task_state = self.task_tracker.get_state()
            
            logger.info(f"Found {len(meetings)} meetings")
            logger.info(f"Found {len(email_batches)} daily email batches")
            logger.info(f"Task tracker has {task_state['metadata']['total_tasks']} tasks")
            
            # Generate rollup
            rollup = self.generate_rollup(meetings, email_batches, task_state)
            
            # Save rollup
            self.save_rollup(rollup)
            
            # Generate markdown digest
            markdown = self.generate_markdown_digest(rollup)
            self.save_markdown_digest(markdown, week_end)
            
            # TODO: Send email to stakeholders
            
            logger.info("Weekly rollup generated successfully")
            logger.info("="*60)
            
            return rollup
            
        except Exception as e:
            logger.error(f"Error generating weekly rollup: {e}", exc_info=True)
    
    def get_week_range(self):
        """Get Monday-Friday date range for current week"""
        today = datetime.now().date()
        
        # Get Monday of current week
        monday = today - timedelta(days=today.weekday())
        
        # Get Friday of current week
        friday = monday + timedelta(days=4)
        
        return monday, friday
    
    def get_meeting_summaries(self, start_date, end_date):
        """Get all meeting summaries for the week"""
        meetings_dir = os.path.join(self.knowledge_base, 'meetings', 'json')
        
        if not os.path.exists(meetings_dir):
            logger.warning(f"Meetings directory not found: {meetings_dir}")
            return []
        
        meetings = []
        
        for filename in os.listdir(meetings_dir):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(meetings_dir, filename)
            
            try:
                with open(filepath, 'r') as f:
                    meeting = json.load(f)
                    
                    # Check if meeting is in date range
                    meeting_date = datetime.fromisoformat(meeting['date']).date()
                    
                    if start_date <= meeting_date <= end_date:
                        meetings.append(meeting)
            
            except Exception as e:
                logger.error(f"Error loading meeting {filename}: {e}")
        
        # Sort by date
        meetings.sort(key=lambda m: m['date'])
        
        return meetings
    
    def get_daily_email_batches(self, start_date, end_date):
        """Get all daily email batches for the week"""
        batch_dir = os.path.join(self.knowledge_base, 'emails', 'daily_batches')
        
        if not os.path.exists(batch_dir):
            logger.warning(f"Daily batches directory not found: {batch_dir}")
            return []
        
        batches = []
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            filename = f'TGIF_Daily_Batch_{date_str}.json'
            filepath = os.path.join(batch_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        batch = json.load(f)
                        batches.append(batch)
                except Exception as e:
                    logger.error(f"Error loading batch {filename}: {e}")
            
            current_date += timedelta(days=1)
        
        return batches
    
    def generate_rollup(self, meetings, email_batches, task_state):
        """Generate weekly rollup from all sources"""
        week_start, week_end = self.get_week_range()
        
        rollup = {
            'type': 'tgif_weekly_rollup',
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'meetings_count': len(meetings),
                'emails_count': sum(b['emails_count'] for b in email_batches),
                'total_decisions': 0,
                'total_actions': 0,
                'total_risks': 0,
                'total_blockers': 0
            },
            'sources': {
                'meetings': [],
                'emails': []
            },
            'by_category': {},
            'action_items_by_owner': {},
            'red_flags': [],
            'next_week_focus': []
        }
        
        # Process meetings
        for meeting in meetings:
            rollup['sources']['meetings'].append({
                'date': meeting['date'],
                'title': meeting.get('title', 'TGIF Meeting'),
                'summary_link': f"focuses/hcss/knowledge/meetings/summaries/TGIF_Meeting_{meeting['date']}.md"
            })
            
            rollup['summary']['total_decisions'] += len(meeting.get('decisions', []))
            rollup['summary']['total_actions'] += len(meeting.get('actions', []))
            rollup['summary']['total_risks'] += len(meeting.get('risks', []))
            rollup['summary']['total_blockers'] += len(meeting.get('blockers', []))
            
            # Aggregate by category
            self._aggregate_meeting_data(rollup, meeting)
        
        # Process email batches
        for batch in email_batches:
            for extract in batch.get('extracts', []):
                rollup['sources']['emails'].append({
                    'date': extract['date'],
                    'from': extract['from'],
                    'subject': extract['subject'],
                    'key_points': [kp['text'] for kp in extract.get('key_points', [])]
                })
                
                # Aggregate email data
                self._aggregate_email_data(rollup, extract)
        
        # Group action items by owner
        rollup['action_items_by_owner'] = task_state['metadata']['by_owner']
        
        # Identify red flags
        rollup['red_flags'] = self._identify_red_flags(meetings, email_batches, task_state)
        
        # Generate next week focus
        rollup['next_week_focus'] = self._generate_next_week_focus(rollup)
        
        return rollup
    
    def _aggregate_meeting_data(self, rollup, meeting):
        """Aggregate meeting data by category"""
        for decision in meeting.get('decisions', []):
            category = decision.get('category', 'uncategorized')
            
            if category not in rollup['by_category']:
                rollup['by_category'][category] = {
                    'decisions': 0,
                    'actions': 0,
                    'key_updates': []
                }
            
            rollup['by_category'][category]['decisions'] += 1
            rollup['by_category'][category]['key_updates'].append(
                f"{decision['text']} (Meeting {meeting['date']})"
            )
        
        for action in meeting.get('actions', []):
            category = action.get('category', 'uncategorized')
            
            if category not in rollup['by_category']:
                rollup['by_category'][category] = {
                    'decisions': 0,
                    'actions': 0,
                    'key_updates': []
                }
            
            rollup['by_category'][category]['actions'] += 1
    
    def _aggregate_email_data(self, rollup, extract):
        """Aggregate email data"""
        for point in extract.get('key_points', []):
            if point.get('importance') == 'high':
                category = point.get('category', 'uncategorized')
                
                if category not in rollup['by_category']:
                    rollup['by_category'][category] = {
                        'decisions': 0,
                        'actions': 0,
                        'key_updates': []
                    }
                
                rollup['by_category'][category]['key_updates'].append(
                    f"{point['text']} (Email {extract['date']})"
                )
    
    def _identify_red_flags(self, meetings, email_batches, task_state):
        """Identify red flags from all sources"""
        red_flags = []
        
        # Overdue tasks
        overdue_tasks = [t for t in task_state['tasks'] if t.get('overdue', False)]
        for task in overdue_tasks:
            red_flags.append({
                'type': 'overdue_action',
                'item': f"{task['id']}: {task['what']}",
                'owner': task.get('who', 'TBD'),
                'due': task.get('due'),
                'source': task.get('source')
            })
        
        # Blockers from meetings
        for meeting in meetings:
            for blocker in meeting.get('blockers', []):
                red_flags.append({
                    'type': 'blocker',
                    'item': blocker['text'],
                    'impact': blocker.get('impact'),
                    'urgency': 'critical',
                    'source': f"meeting_{meeting['date']}"
                })
        
        # High severity risks
        for meeting in meetings:
            for risk in meeting.get('risks', []):
                if risk.get('severity') in ['high', 'critical']:
                    red_flags.append({
                        'type': 'risk',
                        'item': risk['text'],
                        'severity': risk['severity'],
                        'source': f"meeting_{meeting['date']}"
                    })
        
        return red_flags
    
    def _generate_next_week_focus(self, rollup):
        """Generate next week focus areas"""
        focus = []
        
        # Top red flags
        if rollup['red_flags']:
            focus.append(f"Resolve {len(rollup['red_flags'])} red flags")
        
        # Top categories by activity
        categories = sorted(
            rollup['by_category'].items(),
            key=lambda x: x[1]['decisions'] + x[1]['actions'],
            reverse=True
        )
        
        for category, data in categories[:3]:
            if data['key_updates']:
                focus.append(f"{category.replace('_', ' ').title()}: {data['key_updates'][0]}")
        
        return focus[:5]  # Top 5 focus areas
    
    def save_rollup(self, rollup):
        """Save rollup to JSON"""
        rollups_dir = os.path.join(self.knowledge_base, 'rollups')
        os.makedirs(rollups_dir, exist_ok=True)
        
        filename = f"TGIF_Rollup_{rollup['week_end']}.json"
        filepath = os.path.join(rollups_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(rollup, f, indent=2)
        
        logger.info(f"Saved rollup to {filepath}")
    
    def generate_markdown_digest(self, rollup):
        """Generate markdown digest"""
        md = f"""# TGIF Weekly Digest - Week of {rollup['week_start']} to {rollup['week_end']}

**Generated:** {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p %Z')}

---

## 📊 Executive Summary

- **Meetings:** {rollup['summary']['meetings_count']} this week
- **Emails:** {rollup['summary']['emails_count']} flagged items
- **Decisions:** {rollup['summary']['total_decisions']} total
- **Action Items:** {rollup['summary']['total_actions']} total
- **Red Flags:** {len(rollup['red_flags'])} items

---

## 🎯 Key Updates by Category

"""
        
        for category, data in rollup['by_category'].items():
            md += f"\n### {category.replace('_', ' ').title()}\n\n"
            md += f"- **Decisions:** {data['decisions']}\n"
            md += f"- **Actions:** {data['actions']}\n"
            
            if data['key_updates']:
                md += "\n**Key Updates:**\n"
                for update in data['key_updates'][:3]:
                    md += f"- {update}\n"
        
        md += "\n---\n\n## 📋 Meeting Summaries\n\n"
        
        for meeting in rollup['sources']['meetings']:
            md += f"\n### {meeting['date']} - {meeting['title']}\n"
            md += f"[Full Summary]({meeting['summary_link']})\n"
        
        md += "\n---\n\n## 📧 Email Highlights\n\n"
        
        for email in rollup['sources']['emails'][:10]:  # Top 10
            md += f"\n### {email['date']} - {email['subject']}\n"
            md += f"**From:** {email['from']}\n\n"
            
            if email['key_points']:
                md += "**Key Points:**\n"
                for point in email['key_points']:
                    md += f"- {point}\n"
        
        md += "\n---\n\n## ✅ Action Items by Owner\n\n"
        
        for owner, count in rollup['action_items_by_owner'].items():
            md += f"\n### {owner} ({count} items)\n"
            # TODO: List actual tasks
        
        md += "\n---\n\n## 🚨 Red Flags\n\n"
        
        for flag in rollup['red_flags']:
            md += f"\n### {flag['type'].upper()}\n"
            md += f"- **Item:** {flag['item']}\n"
            
            if 'owner' in flag:
                md += f"- **Owner:** {flag['owner']}\n"
            if 'impact' in flag:
                md += f"- **Impact:** {flag['impact']}\n"
            if 'source' in flag:
                md += f"- **Source:** {flag['source']}\n"
        
        md += "\n---\n\n## 🎯 Next Week Focus\n\n"
        
        for i, focus in enumerate(rollup['next_week_focus'], 1):
            md += f"{i}. {focus}\n"
        
        md += f"\n---\n\n**Next Digest:** Friday, {(datetime.now() + timedelta(days=7)).strftime('%B %d, %Y')} at 3:00 PM\n"
        
        return md
    
    def save_markdown_digest(self, markdown, week_end):
        """Save markdown digest"""
        rollups_dir = os.path.join(self.knowledge_base, 'rollups')
        os.makedirs(rollups_dir, exist_ok=True)
        
        filename = f"TGIF_Digest_{week_end}.md"
        filepath = os.path.join(rollups_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(markdown)
        
        logger.info(f"Saved markdown digest to {filepath}")


def main():
    """Main entry point"""
    generator = WeeklyRollupGenerator()
    
    # Get schedule settings
    schedule_time = os.getenv('WEEKLY_ROLLUP_TIME', '15:00')
    schedule_day = os.getenv('WEEKLY_ROLLUP_DAY', 'friday').lower()
    
    logger.info(f"Scheduling weekly rollup for {schedule_day} at {schedule_time}")
    
    # Schedule weekly run
    if schedule_day == 'monday':
        schedule.every().monday.at(schedule_time).do(generator.run)
    elif schedule_day == 'tuesday':
        schedule.every().tuesday.at(schedule_time).do(generator.run)
    elif schedule_day == 'wednesday':
        schedule.every().wednesday.at(schedule_time).do(generator.run)
    elif schedule_day == 'thursday':
        schedule.every().thursday.at(schedule_time).do(generator.run)
    elif schedule_day == 'friday':
        schedule.every().friday.at(schedule_time).do(generator.run)
    
    # Run immediately on startup (for testing)
    if os.getenv('RUN_ON_STARTUP', 'false').lower() == 'true':
        logger.info("Running immediately on startup")
        generator.run()
    
    # Keep running
    logger.info("Weekly rollup generator started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
