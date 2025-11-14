#!/usr/bin/env python3
"""
Meeting Recall Tool
Query and summarize meetings by date range
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class MeetingRecall:
    """Query and summarize meetings"""
    
    def __init__(self, meetings_dir=None):
        """
        Initialize recall tool
        
        Args:
            meetings_dir: Directory with meeting JSON files
        """
        if meetings_dir is None:
            # Default to 8825_files/HCSS/meetings
            meetings_dir = Path(__file__).parent.parent.parent.parent.parent / "8825_files" / "HCSS" / "meetings"
        
        self.meetings_dir = Path(meetings_dir)
        
        if not self.meetings_dir.exists():
            self.meetings_dir.mkdir(parents=True, exist_ok=True)
    
    def find_meetings(self, start_date=None, end_date=None):
        """
        Find meetings in date range
        
        Args:
            start_date: Start date (YYYY-MM-DD) or None for all
            end_date: End date (YYYY-MM-DD) or None for today
            
        Returns:
            List of meeting data dicts
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        meetings = []
        
        for json_file in self.meetings_dir.glob("*.json"):
            try:
                with open(json_file) as f:
                    data = json.load(f)
                
                # Get meeting date
                meeting_date = data.get('processed_data', {}).get('meeting_metadata', {}).get('date')
                
                if not meeting_date:
                    continue
                
                # Check date range
                if start_date and meeting_date < start_date:
                    continue
                if end_date and meeting_date > end_date:
                    continue
                
                meetings.append({
                    'file': json_file,
                    'date': meeting_date,
                    'data': data
                })
            
            except Exception as e:
                print(f"⚠️  Error reading {json_file}: {e}")
        
        # Sort by date
        meetings.sort(key=lambda x: x['date'])
        
        return meetings
    
    def generate_summary(self, meetings, format='markdown'):
        """
        Generate consolidated summary
        
        Args:
            meetings: List of meeting dicts
            format: Output format (markdown, json)
            
        Returns:
            Summary string or dict
        """
        if not meetings:
            return "No meetings found in date range"
        
        if format == 'json':
            return self._generate_json_summary(meetings)
        else:
            return self._generate_markdown_summary(meetings)
    
    def _generate_markdown_summary(self, meetings):
        """Generate markdown summary"""
        start_date = meetings[0]['date']
        end_date = meetings[-1]['date']
        
        md = f"# Meeting Summary: {start_date} to {end_date}\n\n"
        md += f"**Total Meetings:** {len(meetings)}  \n"
        md += f"**Date Range:** {start_date} to {end_date}\n\n"
        md += "---\n\n"
        
        # Aggregate data
        all_decisions = []
        all_actions = []
        all_risks = []
        all_blockers = []
        all_issues = []
        
        # Individual meeting summaries
        md += "## 📋 Individual Meetings\n\n"
        
        for i, meeting in enumerate(meetings, 1):
            processed = meeting['data'].get('processed_data', {})
            metadata = processed.get('meeting_metadata', {})
            
            md += f"### {i}. {metadata.get('title', 'Unknown Meeting')}\n"
            md += f"**Date:** {metadata.get('date', 'Unknown')}  \n"
            md += f"**Type:** {metadata.get('meeting_type', 'Unknown')}  \n"
            
            attendees = metadata.get('attendees', [])
            if attendees:
                md += f"**Attendees:** {', '.join([a.get('name', 'Unknown') for a in attendees])}  \n"
            
            # Key topics
            topics = processed.get('key_topics', [])
            if topics:
                md += "\n**Key Topics:**\n"
                for topic in topics[:3]:  # Top 3
                    md += f"- {topic}\n"
            
            md += "\n"
            
            # Collect for aggregation
            all_decisions.extend(processed.get('decisions', []))
            all_actions.extend(processed.get('actions', []))
            all_risks.extend(processed.get('risks', []))
            all_blockers.extend(processed.get('blockers', []))
            all_issues.extend(processed.get('issues_discussed', []))
        
        md += "---\n\n"
        
        # Consolidated sections
        if all_decisions:
            md += f"## 🎯 All Decisions ({len(all_decisions)})\n\n"
            for dec in all_decisions:
                md += f"- **{dec['text']}** ({dec['category']}, {dec['impact']} impact)\n"
            md += "\n"
        
        if all_actions:
            md += f"## ✅ All Action Items ({len(all_actions)})\n\n"
            
            # Group by owner
            by_owner = defaultdict(list)
            for action in all_actions:
                by_owner[action['who']].append(action)
            
            for owner, actions in sorted(by_owner.items()):
                md += f"### {owner}\n"
                for action in actions:
                    md += f"- {action['what']} (Due: {action['due']}, Priority: {action['priority']})\n"
                md += "\n"
        
        if all_risks:
            md += f"## ⚠️ All Risks ({len(all_risks)})\n\n"
            # Sort by severity
            risks_by_severity = {
                'critical': [],
                'high': [],
                'medium': [],
                'low': []
            }
            for risk in all_risks:
                risks_by_severity[risk['severity']].append(risk)
            
            for severity in ['critical', 'high', 'medium', 'low']:
                risks = risks_by_severity[severity]
                if risks:
                    md += f"### {severity.upper()}\n"
                    for risk in risks:
                        md += f"- {risk['text']}\n"
                        if risk.get('mitigation'):
                            md += f"  - Mitigation: {risk['mitigation']}\n"
                    md += "\n"
        
        if all_blockers:
            md += f"## 🚫 All Blockers ({len(all_blockers)})\n\n"
            for blocker in all_blockers:
                md += f"- **{blocker['text']}**\n"
                md += f"  - Impact: {blocker['impact']}\n"
                md += f"  - Resolution Needed: {blocker.get('resolution_needed_by', 'TBD')}\n"
                md += f"  - Owner: {blocker.get('owner', 'TBD')}\n"
            md += "\n"
        
        if all_issues:
            md += f"## 📌 All Issues Discussed ({len(all_issues)})\n\n"
            # Group by status
            by_status = defaultdict(list)
            for issue in all_issues:
                by_status[issue['status']].append(issue)
            
            for status in ['open', 'in_progress', 'resolved']:
                issues = by_status[status]
                if issues:
                    md += f"### {status.upper()}\n"
                    for issue in issues:
                        md += f"- {issue['topic']}"
                        if issue.get('owner'):
                            md += f" (Owner: {issue['owner']})"
                        md += "\n"
                    md += "\n"
        
        # Summary stats
        md += "---\n\n"
        md += "## 📊 Summary Statistics\n\n"
        md += f"- **Meetings:** {len(meetings)}\n"
        md += f"- **Decisions:** {len(all_decisions)}\n"
        md += f"- **Action Items:** {len(all_actions)}\n"
        md += f"- **Risks:** {len(all_risks)}\n"
        md += f"- **Blockers:** {len(all_blockers)}\n"
        md += f"- **Issues:** {len(all_issues)}\n"
        
        return md
    
    def _generate_json_summary(self, meetings):
        """Generate JSON summary"""
        summary = {
            'date_range': {
                'start': meetings[0]['date'],
                'end': meetings[-1]['date']
            },
            'total_meetings': len(meetings),
            'meetings': [],
            'aggregated': {
                'decisions': [],
                'actions': [],
                'risks': [],
                'blockers': [],
                'issues': []
            }
        }
        
        for meeting in meetings:
            processed = meeting['data'].get('processed_data', {})
            metadata = processed.get('meeting_metadata', {})
            
            summary['meetings'].append({
                'date': metadata.get('date'),
                'title': metadata.get('title'),
                'type': metadata.get('meeting_type'),
                'file': str(meeting['file'])
            })
            
            summary['aggregated']['decisions'].extend(processed.get('decisions', []))
            summary['aggregated']['actions'].extend(processed.get('actions', []))
            summary['aggregated']['risks'].extend(processed.get('risks', []))
            summary['aggregated']['blockers'].extend(processed.get('blockers', []))
            summary['aggregated']['issues'].extend(processed.get('issues_discussed', []))
        
        return summary

def main():
    """CLI for meeting recall"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Query and summarize meetings by date range')
    parser.add_argument('--from', dest='start_date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to', dest='end_date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--last-week', action='store_true', help='Last 7 days')
    parser.add_argument('--last-month', action='store_true', help='Last 30 days')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file (default: print to stdout)')
    
    args = parser.parse_args()
    
    recall = MeetingRecall()
    
    # Determine date range
    start_date = args.start_date
    end_date = args.end_date
    
    if args.last_week:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif args.last_month:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"🔍 Searching for meetings...")
    if start_date:
        print(f"   From: {start_date}")
    if end_date:
        print(f"   To: {end_date}")
    
    meetings = recall.find_meetings(start_date, end_date)
    
    if not meetings:
        print("❌ No meetings found in date range")
        sys.exit(1)
    
    print(f"✅ Found {len(meetings)} meeting(s)\n")
    
    # Generate summary
    summary = recall.generate_summary(meetings, format=args.format)
    
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            if args.format == 'json':
                json.dump(summary, f, indent=2)
            else:
                f.write(summary)
        print(f"💾 Saved summary to: {output_path}")
    else:
        if args.format == 'json':
            print(json.dumps(summary, indent=2))
        else:
            print(summary)

if __name__ == '__main__':
    main()
