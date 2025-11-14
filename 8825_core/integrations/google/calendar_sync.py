#!/usr/bin/env python3
"""
HCSS Calendar Sync
Syncs HCSS meetings from personal calendar to harmon.justin@gmail.com
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# Paths
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'
TOKEN_FILE = SCRIPT_DIR / 'token.json'

# HCSS meeting patterns to sync
HCSS_PATTERNS = [
    'JustinBecky',
    'Justin/Becky',
    'Portal Development',
    'TGIF',
    'TGI Friday',
    'Crunchtime',
    'Toast',
    'HCSS'
]

class CalendarSync:
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
    
    def get_all_calendars(self) -> List[Dict]:
        """Get list of all calendars"""
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            return calendars
        except Exception as e:
            print(f"✗ Error listing calendars: {e}")
            return []
    
    def get_primary_calendar_events(self, days_ahead: int = 7) -> List[Dict]:
        """Get events from ALL calendars for next N days"""
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=days_ahead)).isoformat() + 'Z'
        
        all_events = []
        
        # Get all calendars
        calendars = self.get_all_calendars()
        print(f"✓ Found {len(calendars)} calendars")
        
        # Get events from each calendar
        for calendar in calendars:
            cal_id = calendar['id']
            cal_name = calendar.get('summary', cal_id)
            
            try:
                events_result = self.service.events().list(
                    calendarId=cal_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                events = events_result.get('items', [])
                if events:
                    print(f"  → {cal_name}: {len(events)} events")
                    all_events.extend(events)
            except Exception as e:
                print(f"  ✗ Error reading {cal_name}: {e}")
        
        print(f"✓ Total events found: {len(all_events)}")
        return all_events
    
    def is_hcss_meeting(self, event: Dict) -> bool:
        """Check if event is an HCSS meeting"""
        summary = event.get('summary', '').lower()
        description = event.get('description', '').lower()
        
        # Check if any HCSS pattern matches
        for pattern in HCSS_PATTERNS:
            if pattern.lower() in summary or pattern.lower() in description:
                return True
        
        return False
    
    def event_exists_in_target(self, event: Dict, target_calendar_id: str) -> bool:
        """Check if event already exists in target calendar"""
        summary = event.get('summary', '')
        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
        
        if not start:
            return False
        
        # Parse start time
        try:
            if 'T' in start:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            else:
                start_dt = datetime.fromisoformat(start)
        except:
            return False
        
        # Search for existing event
        time_min = (start_dt - timedelta(minutes=5)).isoformat()
        time_max = (start_dt + timedelta(minutes=5)).isoformat()
        
        try:
            events_result = self.service.events().list(
                calendarId=target_calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                q=summary,
                singleEvents=True
            ).execute()
            
            events = events_result.get('items', [])
            return len(events) > 0
        except:
            return False
    
    def create_placeholder(self, event: Dict, target_calendar_id: str) -> bool:
        """Create placeholder event in target calendar"""
        try:
            # Build event body
            event_body = {
                'summary': event.get('summary', 'HCSS Meeting'),
                'description': f"Synced from personal calendar\n\n{event.get('description', '')}",
                'start': event.get('start'),
                'end': event.get('end'),
                'location': event.get('location', ''),
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10}
                    ]
                }
            }
            
            # Add conferenceData if present (Teams/Zoom links)
            if 'conferenceData' in event:
                event_body['conferenceData'] = event['conferenceData']
            
            # Create event
            created_event = self.service.events().insert(
                calendarId=target_calendar_id,
                body=event_body
            ).execute()
            
            print(f"  ✓ Created: {event.get('summary')}")
            return True
        except Exception as e:
            print(f"  ✗ Failed to create {event.get('summary')}: {e}")
            return False
    
    def sync_hcss_meetings(self, target_email: str = 'harmon.justin@gmail.com', days_ahead: int = 7):
        """Main sync function"""
        print(f"\n🔄 HCSS Calendar Sync")
        print(f"Target: {target_email}")
        print(f"Period: Next {days_ahead} days\n")
        
        # Get events from primary calendar
        events = self.get_primary_calendar_events(days_ahead)
        
        if not events:
            print("No events found in primary calendar")
            return
        
        # Filter HCSS meetings
        hcss_events = [e for e in events if self.is_hcss_meeting(e)]
        print(f"✓ Found {len(hcss_events)} HCSS meetings\n")
        
        if not hcss_events:
            print("No HCSS meetings to sync")
            return
        
        # Sync each meeting
        created = 0
        skipped = 0
        
        for event in hcss_events:
            summary = event.get('summary', 'Untitled')
            start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'Unknown'))
            
            print(f"Processing: {summary}")
            print(f"  Time: {start}")
            
            # Check if already exists
            if self.event_exists_in_target(event, target_email):
                print(f"  → Already exists, skipping")
                skipped += 1
            else:
                # Create placeholder
                if self.create_placeholder(event, target_email):
                    created += 1
            
            print()
        
        # Summary
        print("=" * 50)
        print(f"Sync complete!")
        print(f"Created: {created}")
        print(f"Skipped: {skipped}")
        print(f"Total: {len(hcss_events)}")
        print("=" * 50)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sync HCSS meetings to harmon.justin@gmail.com')
    parser.add_argument('--days', type=int, default=7, help='Number of days ahead to sync (default: 7)')
    parser.add_argument('--target', type=str, default='harmon.justin@gmail.com', help='Target calendar email')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be synced without creating events')
    
    args = parser.parse_args()
    
    # Create syncer
    syncer = CalendarSync()
    
    # Run sync
    syncer.sync_hcss_meetings(target_email=args.target, days_ahead=args.days)

if __name__ == '__main__':
    main()
