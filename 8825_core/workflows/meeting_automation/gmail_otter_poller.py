#!/usr/bin/env python3
"""
Gmail Otter.ai Poller
Searches Gmail for new Otter.ai meeting transcripts and extracts them
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "integrations" / "google"))

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailOtterPoller:
    """Poll Gmail for Otter.ai meeting transcripts"""
    
    def __init__(self, credentials_path=None, token_path=None):
        """
        Initialize poller
        
        Args:
            credentials_path: Path to Gmail OAuth credentials
            token_path: Path to Gmail OAuth token
        """
        if credentials_path is None:
            credentials_path = Path(__file__).parent.parent.parent / "integrations" / "google" / "credentials.json"
        if token_path is None:
            token_path = Path(__file__).parent.parent.parent / "integrations" / "google" / "token.json"
        
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self.service = None
    
    def _get_service(self):
        """Get or create Gmail service"""
        if self.service is None:
            if not self.token_path.exists():
                raise FileNotFoundError(
                    f"Gmail token not found at {self.token_path}\n"
                    "Run the Gmail search script first to authenticate."
                )
            
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
            self.service = build('gmail', 'v1', credentials=creds)
        
        return self.service
    
    def search_otter_emails(self, unread_only=True):
        """
        Search for Otter.ai emails
        
        Args:
            unread_only: Only return unread emails
            
        Returns:
            List of message IDs
        """
        service = self._get_service()
        
        query = 'from:otter.ai'
        if unread_only:
            query += ' is:unread'
        
        try:
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            return messages
        
        except Exception as e:
            print(f"❌ Error searching Gmail: {e}")
            return []
    
    def get_email_content(self, msg_id):
        """
        Get full email content
        
        Args:
            msg_id: Gmail message ID
            
        Returns:
            Dict with email details
        """
        service = self._get_service()
        
        try:
            message = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            # Get headers
            headers = message.get('payload', {}).get('headers', [])
            subject = ''
            date = ''
            from_addr = ''
            
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'Date':
                    date = header['value']
                elif header['name'] == 'From':
                    from_addr = header['value']
            
            # Get body
            body = self._get_body(message.get('payload', {}))
            
            # Extract Otter.ai specific data
            meeting_data = self._parse_otter_email(subject, body, date)
            
            if meeting_data is None:
                return None
            
            meeting_data['gmail_id'] = msg_id
            meeting_data['from'] = from_addr
            
            return meeting_data
        
        except Exception as e:
            print(f"❌ Error getting email {msg_id}: {e}")
            return None
    
    def _get_body(self, payload):
        """Extract body from email payload"""
        body_text = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] in ['text/plain', 'text/html']:
                    data = part['body'].get('data', '')
                    if data:
                        decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        body_text += decoded
        elif 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        return body_text
    
    def _is_meeting_email(self, subject, body):
        """
        Check if email is an actual meeting transcript
        
        Args:
            subject: Email subject
            body: Email body
            
        Returns:
            Boolean - True if meeting, False if promotional/other
        """
        # Check if it's a meeting summary
        if 'Meeting Summary for' not in subject:
            return False
        
        # Exclude promotional emails by subject keywords
        promotional_keywords = [
            'payment',
            'thank you for',
            'starter guide',
            'training webinar',
            'otterpilot',
            'upcoming meetings',
            'record your first',
            'save time by',
            'answers faster',
            'let otter take'
        ]
        
        subject_lower = subject.lower()
        for keyword in promotional_keywords:
            if keyword in subject_lower:
                return False
        
        # If we get here, it has "Meeting Summary for" and no promotional keywords
        # This is likely a real meeting
        
        # Additional checks if body is available
        if body and len(body) > 0:
            # Check if body contains actual transcript content
            if 'Speaker' in body or 'Transcript' in body or 'shared notes from' in body.lower():
                return True
        
        # If subject looks like a meeting and no promotional keywords, assume it's real
        # (Some Otter emails have empty body or HTML-only)
        return True
    
    def _parse_otter_email(self, subject, body, date_str):
        """
        Parse Otter.ai email to extract meeting data
        
        Args:
            subject: Email subject
            body: Email body
            date_str: Email date string
            
        Returns:
            Dict with meeting data or None if not a meeting
        """
        # Check if this is actually a meeting
        if not self._is_meeting_email(subject, body):
            return None
        
        # Extract meeting title from subject
        # Format: "Meeting Summary for [Title]"
        title_match = re.search(r'Meeting Summary for (.+)', subject)
        title = title_match.group(1) if title_match else subject
        
        # Try to extract date from title or body
        # Otter format: "Meeting Title, Nov 13"
        date_match = re.search(r',\s*([A-Z][a-z]+\s+\d{1,2})', title)
        meeting_date = None
        if date_match:
            # Parse "Nov 13" format
            date_str_short = date_match.group(1)
            try:
                # Add current year
                current_year = datetime.now().year
                meeting_date = datetime.strptime(f"{date_str_short} {current_year}", "%b %d %Y").strftime("%Y-%m-%d")
            except:
                pass
        
        # Extract Otter.ai link first (we'll need it if transcript is empty)
        otter_link = self._extract_otter_link(body)
        
        # Extract transcript from body
        # Otter emails contain the transcript in the body
        transcript = self._extract_transcript(body)
        
        # If transcript is empty and we have an Otter link, fetch from Otter
        if (not transcript or len(transcript) == 0) and otter_link:
            transcript = self._fetch_transcript_from_otter(otter_link)
        
        # Extract Otter's summary if present
        otter_summary = self._extract_otter_summary(body)
        
        return {
            'title': title.strip(),
            'date': meeting_date,
            'email_date': date_str,
            'transcript': transcript,
            'otter_summary': otter_summary,
            'otter_link': otter_link,
            'raw_body': body,
            'needs_manual_transcript': (not transcript or transcript.startswith('[TRANSCRIPT NOT IN EMAIL'))
        }
    
    def _extract_transcript(self, body):
        """Extract transcript text from email body"""
        if not body or len(body) == 0:
            return ""
        
        # Otter emails have transcript in the body
        # Try to find transcript section
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', body)
        
        # Look for transcript markers
        # Otter format varies, so we'll take the main content
        # after removing common email elements
        
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        
        # Remove email headers/footers
        text = re.sub(r'Justin Harmon has shared notes.*', '', text, flags=re.DOTALL)
        text = re.sub(r'View in Otter.*', '', text, flags=re.DOTALL)
        text = re.sub(r'Download.*', '', text, flags=re.DOTALL)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def _fetch_transcript_from_otter(self, otter_link):
        """
        Fetch transcript from Otter.ai link
        
        This is a placeholder - in production, you would either:
        1. Use unofficial Otter API (requires credentials)
        2. Use web scraping (fragile)
        3. Require manual paste (most reliable)
        
        For now, we'll return a note that transcript needs to be fetched
        """
        return f"[TRANSCRIPT NOT IN EMAIL - View at: {otter_link}]\n\nTo process this meeting, either:\n1. Set up Otter.ai API credentials\n2. Manually copy transcript from Otter.ai and re-process"
    
    def _extract_otter_summary(self, body):
        """Extract Otter.ai's AI-generated summary"""
        # Look for summary section in email
        summary_match = re.search(r'Summary:?\s*(.+?)(?:\n\n|View in Otter)', body, re.DOTALL | re.IGNORECASE)
        if summary_match:
            return summary_match.group(1).strip()
        return None
    
    def _extract_otter_link(self, body):
        """Extract Otter.ai link from email"""
        link_match = re.search(r'(https://otter\.ai/[^\s<>"]+)', body)
        if link_match:
            return link_match.group(1)
        return None
    
    def mark_as_read(self, msg_id):
        """Mark email as read"""
        service = self._get_service()
        
        try:
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            print(f"❌ Error marking email as read: {e}")
            return False
    
    def _is_already_processed(self, gmail_id, title):
        """
        Check if meeting already processed
        
        Args:
            gmail_id: Gmail message ID
            title: Meeting title
            
        Returns:
            Boolean - True if already processed
        """
        # Check in data/raw directory
        raw_dir = Path(__file__).parent / "data" / "raw"
        if raw_dir.exists():
            # Check if gmail_id already exists in any file
            for json_file in raw_dir.glob("*_" + gmail_id + ".json"):
                return True
        
        # Check in processed directory (8825_files)
        processed_dir = Path(__file__).parent.parent.parent.parent.parent / "8825_files" / "HCSS" / "meetings"
        if processed_dir.exists():
            # Check if any processed file contains this gmail_id
            for json_file in processed_dir.glob("*.json"):
                try:
                    with open(json_file) as f:
                        data = json.load(f)
                        if data.get('original_data', {}).get('gmail_id') == gmail_id:
                            return True
                except:
                    pass
        
        return False
    
    def poll(self, mark_read=True, save_raw=True):
        """
        Poll Gmail for new Otter.ai emails
        
        Args:
            mark_read: Mark emails as read after processing
            save_raw: Save raw email data
            
        Returns:
            List of meeting data dicts
        """
        print("🔍 Searching Gmail for Otter.ai emails...")
        
        messages = self.search_otter_emails(unread_only=True)
        
        if not messages:
            print("✅ No new Otter.ai emails found")
            return []
        
        print(f"📧 Found {len(messages)} new email(s)")
        
        meetings = []
        skipped_count = 0
        
        for msg in messages:
            msg_id = msg['id']
            print(f"\n📄 Processing email {msg_id}...")
            
            meeting_data = self.get_email_content(msg_id)
            
            if not meeting_data:
                print(f"   ⏭️  Skipped: Not a meeting transcript")
                skipped_count += 1
                if mark_read:
                    self.mark_as_read(msg_id)
                continue
            
            # Check if already processed
            if self._is_already_processed(msg_id, meeting_data.get('title', '')):
                print(f"   ⏭️  Skipped: Already processed")
                skipped_count += 1
                if mark_read:
                    self.mark_as_read(msg_id)
                continue
            
            print(f"   Title: {meeting_data['title']}")
            print(f"   Date: {meeting_data.get('date', 'Unknown')}")
            
            if save_raw:
                # Save raw data
                raw_dir = Path(__file__).parent / "data" / "raw"
                raw_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                raw_file = raw_dir / f"{timestamp}_{msg_id}.json"
                
                with open(raw_file, 'w') as f:
                    json.dump(meeting_data, f, indent=2)
                
                print(f"   💾 Saved raw data to: {raw_file}")
            
            meetings.append(meeting_data)
            
            if mark_read:
                if self.mark_as_read(msg_id):
                    print(f"   ✅ Marked as read")
        
        if skipped_count > 0:
            print(f"\n⏭️  Skipped {skipped_count} non-meeting/duplicate email(s)")
        
        return meetings

def main():
    """Test poller"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Poll Gmail for Otter.ai meeting transcripts')
    parser.add_argument('--no-mark-read', action='store_true', help='Do not mark emails as read')
    parser.add_argument('--no-save-raw', action='store_true', help='Do not save raw email data')
    
    args = parser.parse_args()
    
    poller = GmailOtterPoller()
    
    try:
        meetings = poller.poll(
            mark_read=not args.no_mark_read,
            save_raw=not args.no_save_raw
        )
        
        print(f"\n{'='*80}")
        print(f"✅ Processed {len(meetings)} meeting(s)")
        print(f"{'='*80}\n")
        
        if meetings:
            print("Next step: Run meeting processor to extract structured data")
            print("Command: python3 meeting_processor.py")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
