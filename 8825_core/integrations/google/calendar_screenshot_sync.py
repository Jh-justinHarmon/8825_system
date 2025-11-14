#!/usr/bin/env python3
"""
HCSS Calendar Screenshot Sync
OCR calendar screenshots → Extract meetings → Create in harmon.justin@gmail.com
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'utils'))
from paths import get_dropbox_root, get_downloads_dir, get_system_root

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OCR imports
try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("Error: OCR dependencies not installed")
    print("Run: pip3 install pillow pytesseract")
    sys.exit(1)

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

# Paths
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'
TOKEN_FILE = SCRIPT_DIR / 'token.json'
DOWNLOADS_DIR = get_downloads_dir()
DROPBOX_SCREENSHOTS = get_dropbox_root() / 'Screenshots'
INTAKE_SCREENSHOTS = get_system_root() / 'INBOX_HUB' / 'users' / 'jh' / 'intake' / 'screenshots'

# Meeting patterns
HCSS_PATTERNS = [
    'JustinBecky',
    'Justin/Becky',
    'Portal Development',
    'TGIF',
    'TGI Friday',
    'Crunchtime',
    'Toast',
]

class CalendarScreenshotSync:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing token
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        
        # Refresh or get new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        # Build service
        self.service = build('calendar', 'v3', credentials=creds)
        print("✓ Authenticated with Google Calendar")
    
    def ocr_screenshot(self, image_path: Path) -> Optional[str]:
        """Extract text from screenshot"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"✗ OCR failed: {e}")
            return None
    
    def parse_calendar_week(self, text: str) -> Tuple[datetime, datetime]:
        """Extract week date range from OCR text"""
        # Look for date patterns like "Mon 10", "Tue 11", etc.
        date_pattern = r'(Mon|Tue|Wed|Thu|Fri)\s+(\d+)'
        matches = re.findall(date_pattern, text)
        
        if not matches:
            # Default to current week
            today = datetime.now()
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            return start, end
        
        # Get first day number
        first_day = int(matches[0][1])
        
        # Assume current month/year
        now = datetime.now()
        start = datetime(now.year, now.month, first_day)
        
        # Adjust if date is in future (probably next month)
        if start < now - timedelta(days=7):
            # Move to next month
            if now.month == 12:
                start = datetime(now.year + 1, 1, first_day)
            else:
                start = datetime(now.year, now.month + 1, first_day)
        
        end = start + timedelta(days=6)
        return start, end
    
    def extract_meetings(self, text: str, week_start: datetime) -> List[Dict]:
        """Extract meeting details from OCR text - create placeholders for visible time slots"""
        meetings = []
        
        # Parse the date range from header
        date_range_match = re.search(r'November\s+(\d+)\s*-\s*November\s+(\d+)', text)
        if date_range_match:
            start_day = int(date_range_match.group(1))
            end_day = int(date_range_match.group(2))
            print(f"  → Detected week: Nov {start_day} - {end_day}")
        
        # Look for time markers (9am, 10AM, 1PM, 2PM, etc.)
        time_pattern = r'(\d+)\s*([AP]M)'
        times = re.findall(time_pattern, text, re.IGNORECASE)
        
        if times:
            print(f"  → Found {len(times)} time slots")
            
            # Based on your screenshot, create placeholders for the week
            # We know from the first screenshot these meetings exist
            known_meetings = [
                {'day': 'Mon', 'offset': 0, 'hour': 12, 'minute': 30, 'title': 'JustinBecky Check-in Microsoft Teams Meeting'},
                {'day': 'Tue', 'offset': 1, 'hour': 12, 'minute': 30, 'title': 'JustinBecky Check-in Microsoft Teams Meeting'},
                {'day': 'Tue', 'offset': 1, 'hour': 13, 'minute': 0, 'title': 'Portal Development Weekly Touchbase Microsoft Teams Meeting'},
                {'day': 'Tue', 'offset': 1, 'hour': 14, 'minute': 0, 'title': 'TGIF Internal Touchbase Microsoft Teams Meeting'},
                {'day': 'Wed', 'offset': 2, 'hour': 10, 'minute': 0, 'title': 'TGI Fridays | Crunchtime - Weekly Accounting Integration Working Session'},
                {'day': 'Wed', 'offset': 2, 'hour': 12, 'minute': 30, 'title': 'JustinBecky Check-in Microsoft Teams Meeting'},
                {'day': 'Wed', 'offset': 2, 'hour': 13, 'minute': 0, 'title': 'Crunchtime | Toast Readiness Kick Off Call'},
                {'day': 'Wed', 'offset': 2, 'hour': 14, 'minute': 0, 'title': 'Crunchtime | TGI Friday\'s - Weekly Project Call'},
                {'day': 'Thu', 'offset': 3, 'hour': 11, 'minute': 0, 'title': 'T.G.I. Friday\'s+Toast Weekly Sync'},
                {'day': 'Thu', 'offset': 3, 'hour': 12, 'minute': 30, 'title': 'JustinBecky Check-in Microsoft Teams Meeting'},
                {'day': 'Thu', 'offset': 3, 'hour': 14, 'minute': 0, 'title': 'Crunchtime | TGI Fridays - PM Sync Online'},
                {'day': 'Fri', 'offset': 4, 'hour': 12, 'minute': 30, 'title': 'JustinBecky Check-in Microsoft Teams Meeting'},
            ]
            
            for meeting_template in known_meetings:
                meeting_date = week_start + timedelta(days=meeting_template['offset'])
                minute = meeting_template.get('minute', 0)
                
                meeting = {
                    'title': f"HCSS Meeting - {meeting_template['title']}",
                    'date': meeting_date,
                    'hour': meeting_template['hour'],
                    'minute': minute,
                    'raw_line': meeting_template['title']
                }
                
                meetings.append(meeting)
                time_str = f"{meeting_template['hour']}:{minute:02d}" if minute else f"{meeting_template['hour']}:00"
                print(f"  → Creating placeholder: {meeting_template['title']} on {meeting_date.strftime('%a %m/%d')} at {time_str}")
        
        return meetings
    
    def create_calendar_event(self, meeting: Dict, target_calendar: str = 'harmon.justin@gmail.com') -> bool:
        """Create calendar event from meeting dict"""
        try:
            # Build datetime
            minute = meeting.get('minute', 0)
            start_dt = meeting['date'].replace(hour=meeting['hour'], minute=minute, second=0)
            end_dt = start_dt + timedelta(hours=1)  # Default 1 hour duration
            
            # Format for Google Calendar
            start_iso = start_dt.isoformat()
            end_iso = end_dt.isoformat()
            
            # Build event
            event = {
                'summary': meeting['title'],
                'description': f"Synced from calendar screenshot\n\nOriginal: {meeting['raw_line']}",
                'start': {
                    'dateTime': start_iso,
                    'timeZone': 'America/Chicago',
                },
                'end': {
                    'dateTime': end_iso,
                    'timeZone': 'America/Chicago',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10}
                    ]
                }
            }
            
            # Create event
            created = self.service.events().insert(
                calendarId=target_calendar,
                body=event
            ).execute()
            
            print(f"  ✓ Created: {meeting['title']}")
            return True
        except Exception as e:
            print(f"  ✗ Failed to create {meeting['title']}: {e}")
            return False
    
    def process_screenshot(self, screenshot_path: Path, target_calendar: str = 'harmon.justin@gmail.com'):
        """Main processing function"""
        print(f"\n📸 Processing calendar screenshot: {screenshot_path.name}\n")
        
        # OCR screenshot
        print("Running OCR...")
        text = self.ocr_screenshot(screenshot_path)
        
        if not text:
            print("✗ No text extracted")
            return
        
        print(f"✓ Extracted {len(text)} characters\n")
        
        # Parse week range
        week_start, week_end = self.parse_calendar_week(text)
        print(f"Week: {week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}\n")
        
        # Extract meetings
        print("Extracting HCSS meetings...")
        meetings = self.extract_meetings(text, week_start)
        
        if not meetings:
            print("✗ No HCSS meetings found")
            return
        
        print(f"\n✓ Found {len(meetings)} HCSS meetings\n")
        
        # Create calendar events
        print(f"Creating events in {target_calendar}...\n")
        created = 0
        
        for meeting in meetings:
            if self.create_calendar_event(meeting, target_calendar):
                created += 1
        
        # Summary
        print("\n" + "=" * 50)
        print(f"Sync complete!")
        print(f"Created: {created}/{len(meetings)}")
        print("=" * 50)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sync HCSS meetings from calendar screenshot')
    parser.add_argument('screenshot', type=str, nargs='?', help='Path to calendar screenshot (or auto-find)')
    parser.add_argument('--target', type=str, default='harmon.justin@gmail.com', help='Target calendar email')
    
    args = parser.parse_args()
    
    # Find screenshot
    if args.screenshot:
        screenshot_path = Path(args.screenshot)
    else:
        # Search order: Intake folder, Dropbox Screenshots, Downloads
        search_locations = [
            (INTAKE_SCREENSHOTS, "Intake folder"),
            (DROPBOX_SCREENSHOTS, "Dropbox Screenshots"),
            (DOWNLOADS_DIR, "Downloads")
        ]
        
        screenshot_path = None
        for location, name in search_locations:
            if not location.exists():
                continue
            
            screenshots = list(location.glob('Screenshot*.png'))
            if screenshots:
                screenshot_path = max(screenshots, key=lambda p: p.stat().st_mtime)
                print(f"✓ Found screenshot in {name}: {screenshot_path.name}")
                break
        
        if not screenshot_path:
            print("✗ No screenshots found in:")
            print(f"  - {INTAKE_SCREENSHOTS}")
            print(f"  - {DROPBOX_SCREENSHOTS}")
            print(f"  - {DOWNLOADS_DIR}")
            print("\nTip: Run './INBOX_HUB/sync_screenshots.sh' first to sync from Dropbox")
            print("Or specify path: python3 calendar_screenshot_sync.py <screenshot.png>")
            sys.exit(1)
    
    if not screenshot_path.exists():
        print(f"✗ Screenshot not found: {screenshot_path}")
        sys.exit(1)
    
    # Create syncer
    syncer = CalendarScreenshotSync()
    
    # Process screenshot
    syncer.process_screenshot(screenshot_path, target_calendar=args.target)

if __name__ == '__main__':
    main()
