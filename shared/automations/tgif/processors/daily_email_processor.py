"""
Daily Email Processor - Runs at 12pm to process flagged TGIF emails
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


class DailyEmailProcessor:
    """Process flagged TGIF emails daily at 12pm"""
    
    def __init__(self):
        self.knowledge_base = os.getenv('KNOWLEDGE_BASE_PATH', 'focuses/hcss/knowledge')
        self.task_tracker = TaskTracker()
        self._init_gmail()
    
    def _init_gmail(self):
        """Initialize Gmail API"""
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
                 'https://www.googleapis.com/auth/gmail.modify']
        
        creds = None
        token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        creds_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.gmail = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail API initialized")
    
    def run(self):
        """Main processing function - runs daily at 12pm"""
        logger.info("="*60)
        logger.info(f"Starting daily email processing at {datetime.now()}")
        logger.info("="*60)
        
        try:
            # Get new emails from last 24 hours
            since = datetime.now() - timedelta(hours=24)
            new_emails = self.get_new_flagged_emails(since)
            
            logger.info(f"Found {len(new_emails)} new flagged emails")
            
            if not new_emails:
                logger.info("No new emails to process")
                return
            
            # Process each email
            email_extracts = []
            for email in new_emails:
                try:
                    extract = self.process_email(email)
                    email_extracts.append(extract)
                    
                    # Update task tracker
                    self.update_task_tracker(extract)
                    
                except Exception as e:
                    logger.error(f"Error processing email {email['id']}: {e}")
            
            # Save daily batch
            self.save_daily_batch(email_extracts)
            
            # Check for overdue tasks
            self.task_tracker.check_overdue()
            
            # Generate summary
            summary = self.generate_daily_summary(email_extracts)
            
            logger.info(f"Processed {len(email_extracts)} emails")
            logger.info(f"New actions: {summary['new_actions']}")
            logger.info(f"Red flags: {len(summary['red_flags'])}")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Error in daily processing: {e}", exc_info=True)
    
    def get_new_flagged_emails(self, since):
        """Get TGIF emails flagged since last run"""
        after_date = since.strftime('%Y/%m/%d')
        
        # Search for forwarded emails
        query_forwarded = f'from:{os.getenv("NOTIFICATION_EMAIL")} subject:TGIF after:{after_date}'
        
        # Search for labeled emails
        query_labeled = f'label:TGIF after:{after_date}'
        
        emails = []
        
        # Get forwarded emails
        try:
            results = self.gmail.users().messages().list(
                userId='me',
                q=query_forwarded,
                maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            for msg in messages:
                message = self.gmail.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                emails.append(self._parse_gmail_message(message))
        except Exception as e:
            logger.error(f"Error getting forwarded emails: {e}")
        
        # Get labeled emails
        try:
            results = self.gmail.users().messages().list(
                userId='me',
                q=query_labeled,
                maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            for msg in messages:
                message = self.gmail.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                emails.append(self._parse_gmail_message(message))
        except Exception as e:
            logger.error(f"Error getting labeled emails: {e}")
        
        # Dedupe
        seen = set()
        unique_emails = []
        for email in emails:
            if email['id'] not in seen:
                seen.add(email['id'])
                unique_emails.append(email)
        
        return unique_emails
    
    def _parse_gmail_message(self, message):
        """Parse Gmail message"""
        headers = message['payload']['headers']
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        from_addr = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        body = self._get_message_body(message['payload'])
        
        return {
            'id': message['id'],
            'subject': subject,
            'from': from_addr,
            'date': date_str,
            'body': body
        }
    
    def _get_message_body(self, payload):
        """Extract message body"""
        if 'body' in payload and 'data' in payload['body']:
            import base64
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        if 'parts' in payload:
            for part in payload['parts']:
                body = self._get_message_body(part)
                if body:
                    return body
        
        return ""
    
    def process_email(self, email):
        """Extract structured data from email"""
        # TODO: Integrate with Chat Mining Agent
        # For now, create basic structure
        
        extract = {
            'type': 'tgif_email_extract',
            'email_id': email['id'],
            'date': email['date'],
            'from': email['from'],
            'subject': email['subject'],
            'key_points': self._extract_key_points(email['body']),
            'actions': self._extract_actions(email['body']),
            'risks': [],
            'decisions': [],
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'source': 'daily_email_processor'
            }
        }
        
        return extract
    
    def _extract_key_points(self, body):
        """Extract key points from email body"""
        # Simple extraction - TODO: Use Chat Mining Agent
        points = []
        
        # Look for bullet points or numbered lists
        lines = body.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '*', '•')) or (len(line) > 0 and line[0].isdigit() and line[1] in '.):'):
                points.append({
                    'text': line.lstrip('-*•0123456789.): '),
                    'importance': 'medium'
                })
        
        return points[:5]  # Limit to top 5
    
    def _extract_actions(self, body):
        """Extract action items from email body"""
        # Simple extraction - TODO: Use Chat Mining Agent
        actions = []
        
        # Look for action keywords
        action_keywords = ['need to', 'should', 'must', 'will', 'please', 'action:', 'todo:']
        
        lines = body.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in action_keywords):
                actions.append({
                    'what': line.strip(),
                    'who': 'TBD',
                    'priority': 'medium'
                })
        
        return actions[:3]  # Limit to top 3
    
    def update_task_tracker(self, extract):
        """Update task tracker with actions from email"""
        for action in extract['actions']:
            self.task_tracker.add_task({
                'what': action['what'],
                'who': action.get('who', 'TBD'),
                'due': action.get('due'),
                'priority': action.get('priority', 'medium'),
                'status': 'todo',
                'source': 'email',
                'source_id': extract['email_id']
            })
    
    def save_daily_batch(self, email_extracts):
        """Save daily email extracts"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Save individual extracts
        emails_dir = os.path.join(self.knowledge_base, 'emails')
        os.makedirs(emails_dir, exist_ok=True)
        
        for extract in email_extracts:
            filename = f"TGIF_Email_{date_str}_{extract['email_id'][:8]}.json"
            filepath = os.path.join(emails_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(extract, f, indent=2)
        
        # Save daily batch summary
        batch_dir = os.path.join(emails_dir, 'daily_batches')
        os.makedirs(batch_dir, exist_ok=True)
        
        batch = {
            'date': date_str,
            'emails_count': len(email_extracts),
            'actions_count': sum(len(e['actions']) for e in email_extracts),
            'extracts': email_extracts
        }
        
        batch_file = os.path.join(batch_dir, f'TGIF_Daily_Batch_{date_str}.json')
        with open(batch_file, 'w') as f:
            json.dump(batch, f, indent=2)
        
        logger.info(f"Saved daily batch to {batch_file}")
    
    def generate_daily_summary(self, email_extracts):
        """Generate daily summary"""
        summary = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'emails_processed': len(email_extracts),
            'new_actions': sum(len(e['actions']) for e in email_extracts),
            'red_flags': [],
            'highlights': []
        }
        
        for extract in email_extracts:
            for point in extract['key_points']:
                if point.get('importance') == 'high':
                    summary['highlights'].append({
                        'from': extract['from'],
                        'subject': extract['subject'],
                        'point': point['text']
                    })
        
        return summary


def main():
    """Main entry point"""
    processor = DailyEmailProcessor()
    
    # Get schedule time from env
    schedule_time = os.getenv('DAILY_EMAIL_TIME', '12:00')
    
    logger.info(f"Scheduling daily email processing at {schedule_time}")
    
    # Schedule daily run
    schedule.every().day.at(schedule_time).do(processor.run)
    
    # Also run immediately on startup (for testing)
    if os.getenv('RUN_ON_STARTUP', 'false').lower() == 'true':
        logger.info("Running immediately on startup")
        processor.run()
    
    # Keep running
    logger.info("Daily email processor started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
