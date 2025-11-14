#!/usr/bin/env python3
"""
Weekend Soccer Advisor
Detects soccer games, calculates travel time, sends "leave by" notifications
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googlemaps

# Configuration
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'  # For creating departure events
]

# Find workspace root - resolve to absolute path
SCRIPT_DIR = Path(__file__).resolve().parent
# Go up: implementation -> weekend_soccer_advisor -> poc -> jh_assistant -> justin_harmon -> users -> workspace root
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent.parent
CREDENTIALS_PATH = WORKSPACE_ROOT / '8825_core' / 'integrations' / 'google' / 'credentials.json'
TOKEN_PATH = WORKSPACE_ROOT / '8825_core' / 'integrations' / 'google' / 'token.json'

# Soccer settings
EARLY_ARRIVAL_MINUTES_GAME = 45  # Arrive 45 minutes early for games
EARLY_ARRIVAL_MINUTES_PRACTICE = 10  # Arrive 10 minutes early for practices
BUFFER_MINUTES = 10  # Extra buffer for safety
NOTIFICATION_ADVANCE_MINUTES = 10  # Alert 10 minutes before leave time

class SoccerAdvisor:
    def __init__(self):
        self.calendar_service = None
        self.maps_client = None
        # Home address
        self.home_location = "7247 Whispering Pines Dr, Dallas, TX 75248"
        
    def authenticate_calendar(self):
        """Authenticate with Google Calendar"""
        creds = None
        
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        
        self.calendar_service = build('calendar', 'v3', credentials=creds)
        print("✓ Calendar authenticated")
    
    def setup_maps(self):
        """Setup Google Maps client"""
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            print("⚠ GOOGLE_MAPS_API_KEY not set - travel time calculation disabled")
            return
        
        self.maps_client = googlemaps.Client(key=api_key)
        print("✓ Maps API ready")
    
    def get_weekend_events(self, date: datetime = None) -> List[Dict]:
        """Get all events for the upcoming weekend from all calendars"""
        if date is None:
            date = datetime.now()
        
        # Determine which weekend to check
        current_day = date.weekday()  # 0=Monday, 5=Saturday, 6=Sunday
        
        if current_day == 5:  # Saturday
            # Use today as Saturday
            saturday = date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif current_day == 6:  # Sunday
            # Use yesterday as Saturday
            saturday = (date - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # Find next Saturday
            days_until_saturday = (5 - current_day) % 7
            if days_until_saturday == 0:
                days_until_saturday = 7
            saturday = date + timedelta(days=days_until_saturday)
            saturday = saturday.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Weekend is Saturday + Sunday
        sunday = saturday + timedelta(days=1)
        monday = saturday + timedelta(days=2)
        
        # Query calendar
        time_min = saturday.isoformat() + 'Z'
        time_max = monday.isoformat() + 'Z'
        
        # Get all calendars
        calendar_list = self.calendar_service.calendarList().list().execute()
        
        all_events = []
        soccer_keywords = ['soccer', 'sting', 'zambrano', 'game', 'practice']
        
        # Check each calendar
        for calendar in calendar_list.get('items', []):
            cal_id = calendar['id']
            cal_name = calendar.get('summary', 'Unknown')
            
            try:
                events_result = self.calendar_service.events().list(
                    calendarId=cal_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                events = events_result.get('items', [])
                
                # Filter for soccer-related events
                for event in events:
                    summary = event.get('summary', '').lower()
                    # Check if any soccer keyword is in the event name
                    if any(keyword in summary for keyword in soccer_keywords):
                        event['_calendar_name'] = cal_name
                        all_events.append(event)
            except Exception as e:
                # Skip calendars we can't access
                continue
        
        print(f"✓ Found {len(all_events)} soccer events this weekend")
        return all_events
    
    def extract_event_details(self, event: Dict) -> Dict:
        """Extract relevant details from calendar event"""
        summary = event.get('summary', 'Soccer Event')
        
        # Get start time
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        
        # Get location
        location = event.get('location', '')
        
        # Check if this is an all-day event or midnight placeholder
        is_all_day = 'date' in event['start'] and 'dateTime' not in event['start']
        is_midnight = start_dt.hour == 0 and start_dt.minute == 0
        
        return {
            'id': event['id'],
            'name': summary,
            'start': start_dt,
            'location': location,
            'is_all_day': is_all_day,
            'is_midnight': is_midnight,
            'raw_event': event
        }
    
    def calculate_travel_time(self, destination: str) -> Optional[int]:
        """Calculate travel time in minutes using Google Maps"""
        if not self.maps_client:
            print("⚠ Maps API not available - using default 20 minutes")
            return 20
        
        if not destination:
            print("⚠ No destination specified - using default 20 minutes")
            return 20
        
        try:
            # Use home location as origin
            origin = self.home_location
            
            # Get directions with traffic
            now = datetime.now()
            directions = self.maps_client.directions(
                origin,
                destination,
                mode="driving",
                departure_time=now,
                traffic_model="best_guess"
            )
            
            if directions:
                duration = directions[0]['legs'][0]['duration_in_traffic']['value']
                minutes = int(duration / 60)
                print(f"  → Travel time: {minutes} minutes")
                return minutes
            
        except Exception as e:
            print(f"⚠ Maps API error: {e} - using default 20 minutes")
        
        return 20
    
    def calculate_leave_by(self, event_name: str, game_start: datetime, travel_minutes: int) -> Tuple[datetime, Dict]:
        """Calculate when to leave for the game or practice"""
        # Determine if it's a game or practice
        event_lower = event_name.lower()
        is_practice = 'practice' in event_lower or 'training' in event_lower or 'meeting' in event_lower
        
        # Use appropriate early arrival time
        early_arrival = EARLY_ARRIVAL_MINUTES_PRACTICE if is_practice else EARLY_ARRIVAL_MINUTES_GAME
        
        # Formula: leave_by = start - early_arrival - travel - buffer
        leave_by = game_start - timedelta(
            minutes=early_arrival + travel_minutes + BUFFER_MINUTES
        )
        
        # Calculate notification time
        notify_at = leave_by - timedelta(minutes=NOTIFICATION_ADVANCE_MINUTES)
        
        details = {
            'event_name': event_name,
            'is_practice': is_practice,
            'game_start': game_start,
            'early_arrival_minutes': early_arrival,
            'travel_minutes': travel_minutes,
            'buffer_minutes': BUFFER_MINUTES,
            'leave_by': leave_by,
            'notify_at': notify_at,
            'total_advance_minutes': early_arrival + travel_minutes + BUFFER_MINUTES
        }
        
        return leave_by, details
    
    def create_departure_event(self, event_name: str, leave_by: datetime, game_start: datetime, location: str, is_practice: bool) -> Optional[str]:
        """Create a calendar event for departure time"""
        try:
            event_type = "Practice" if is_practice else "Game"
            
            # Create Google Maps URL for directions
            maps_url = f"https://www.google.com/maps/dir/?api=1&origin={self.home_location.replace(' ', '+')}&destination={location.replace(' ', '+')}"
            
            departure_event = {
                'summary': f'🚗 Leave for {event_name}',
                'description': f'Departure time for {event_type}\n\nDestination: {location}\nEvent starts: {game_start.strftime("%I:%M %p")}\n\n🗺️ Directions: {maps_url}',
                'start': {
                    'dateTime': leave_by.isoformat(),
                    'timeZone': 'America/Chicago',
                },
                'end': {
                    'dateTime': (leave_by + timedelta(minutes=5)).isoformat(),
                    'timeZone': 'America/Chicago',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            created_event = self.calendar_service.events().insert(
                calendarId='primary',
                body=departure_event
            ).execute()
            
            return created_event.get('htmlLink')
            
        except Exception as e:
            print(f"⚠ Could not create departure event: {e}")
            return None
    
    def create_weekend_summary_event(self, events_data: List[Dict]) -> Optional[str]:
        """Create a single Friday evening event with all weekend games"""
        try:
            # Find next Friday at 5pm
            now = datetime.now()
            days_until_friday = (4 - now.weekday()) % 7
            if days_until_friday == 0 and now.hour >= 17:
                days_until_friday = 7
            friday = now + timedelta(days=days_until_friday)
            friday_5pm = friday.replace(hour=17, minute=0, second=0, microsecond=0)
            
            # Build description with all games
            description = "⚽ Weekend Soccer Schedule\n\n"
            
            for data in events_data:
                event_type = "Practice" if data['is_practice'] else "Game"
                day = data['start'].strftime('%A')
                time = data['start'].strftime('%I:%M %p')
                leave_time = data['leave_by'].strftime('%I:%M %p')
                
                # Create Google Maps URL
                maps_url = f"https://www.google.com/maps/dir/?api=1&origin={self.home_location.replace(' ', '+')}&destination={data['location'].replace(' ', '+')}"
                
                description += f"📍 {data['name']}\n"
                description += f"   {event_type} - {day} at {time}\n"
                description += f"   🚗 Leave by: {leave_time}\n"
                description += f"   📍 {data['location']}\n"
                description += f"   🗺️ Directions: {maps_url}\n\n"
            
            summary_event = {
                'summary': '⚽ Weekend Soccer Schedule',
                'description': description,
                'start': {
                    'dateTime': friday_5pm.isoformat(),
                    'timeZone': 'America/Chicago',
                },
                'end': {
                    'dateTime': (friday_5pm + timedelta(minutes=15)).isoformat(),
                    'timeZone': 'America/Chicago',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 0},
                    ],
                },
            }
            
            created_event = self.calendar_service.events().insert(
                calendarId='primary',
                body=summary_event
            ).execute()
            
            return created_event.get('htmlLink')
            
        except Exception as e:
            print(f"⚠ Could not create weekend summary: {e}")
            return None
    
    def generate_weekend_preview(self, events: List[Dict]) -> str:
        """Generate Friday evening preview of weekend soccer schedule"""
        if not events:
            return "📅 No soccer games scheduled this weekend. Enjoy your free time!"
        
        preview = "⚽ Weekend Soccer Schedule\n"
        preview += "=" * 50 + "\n\n"
        
        # Collect data for weekend summary event
        events_data = []
        
        for event in events:
            details = self.extract_event_details(event)
            
            # Skip all-day events and midnight placeholders
            if details['is_all_day'] or details['is_midnight']:
                preview += f"⏭️  Skipping: {details['name']} (all-day/placeholder event)\n\n"
                continue
            
            travel_time = self.calculate_travel_time(details['location'])
            leave_by, calc = self.calculate_leave_by(details['name'], details['start'], travel_time)
            
            day = details['start'].strftime('%A')
            time = details['start'].strftime('%I:%M %p')
            leave_time = leave_by.strftime('%I:%M %p')
            event_type = "Practice" if calc['is_practice'] else "Game"
            early_time = calc['early_arrival_minutes']
            
            # Store for weekend summary
            events_data.append({
                'name': details['name'],
                'start': details['start'],
                'leave_by': leave_by,
                'location': details['location'],
                'is_practice': calc['is_practice']
            })
            
            preview += f"📍 {details['name']}\n"
            preview += f"   {event_type} - {day} at {time}\n"
            if details['location']:
                preview += f"   Location: {details['location']}\n"
            preview += f"   🚗 Leave by: {leave_time}\n"
            preview += f"   (Travel: {travel_time} min + {early_time} min early + {calc['buffer_minutes']} min buffer)\n"
            
            # Create departure calendar event
            cal_link = self.create_departure_event(
                details['name'], 
                leave_by, 
                details['start'], 
                details['location'],
                calc['is_practice']
            )
            if cal_link:
                preview += f"   ✓ Departure reminder created\n"
            preview += "\n"
        
        # Create weekend summary event with all games
        if events_data:
            summary_link = self.create_weekend_summary_event(events_data)
            if summary_link:
                preview += "=" * 50 + "\n"
                preview += "✅ Weekend summary event created (Friday 5pm)\n"
                preview += f"   All games with directions in one place!\n"
        
        return preview
    
    def generate_game_day_alert(self, event: Dict) -> str:
        """Generate game day notification"""
        details = self.extract_event_details(event)
        travel_time = self.calculate_travel_time(details['location'])
        leave_by, calc = self.calculate_leave_by(details['name'], details['start'], travel_time)
        
        game_time = details['start'].strftime('%I:%M %p')
        leave_time = leave_by.strftime('%I:%M %p')
        event_type = "Practice" if calc['is_practice'] else "Game"
        
        alert = f"⚽ Soccer {event_type} Alert\n"
        alert += f"🕐 Leave by {leave_time} for {details['name']}\n"
        alert += f"📍 {event_type} starts at {game_time}\n"
        if details['location']:
            alert += f"📌 {details['location']}\n"
        alert += f"🚗 {travel_time} min drive + {calc['early_arrival_minutes']} min early arrival\n"
        
        return alert
    
    def process_weekend(self, preview_only: bool = False) -> Dict:
        """Main processing function"""
        print("\n⚽ Weekend Soccer Advisor")
        print("=" * 50)
        
        # Authenticate
        self.authenticate_calendar()
        self.setup_maps()
        
        # Get weekend events
        events = self.get_weekend_events()
        
        if not events:
            print("\n📅 No soccer games this weekend")
            return {'events': [], 'preview': None}
        
        # Generate preview
        preview = self.generate_weekend_preview(events)
        print("\n" + preview)
        
        # Generate game day alerts (for testing)
        if not preview_only:
            print("\n📱 Game Day Alerts Preview:")
            print("-" * 50)
            for event in events:
                alert = self.generate_game_day_alert(event)
                print(alert)
                print("-" * 50)
        
        # Return structured data
        result = {
            'events': [self.extract_event_details(e) for e in events],
            'preview': preview,
            'generated_at': datetime.now().isoformat()
        }
        
        return result

def main():
    """Main entry point"""
    advisor = SoccerAdvisor()
    
    # Check for preview mode
    preview_only = '--preview' in sys.argv
    
    try:
        result = advisor.process_weekend(preview_only=preview_only)
        
        # Save result
        output_dir = Path.home() / 'Downloads'
        output_file = output_dir / 'soccer_schedule.json'
        
        # Convert datetime objects to strings for JSON
        result_json = result.copy()
        for event in result_json.get('events', []):
            if 'start' in event:
                event['start'] = event['start'].isoformat()
            if 'raw_event' in event:
                del event['raw_event']
        
        with open(output_file, 'w') as f:
            json.dump(result_json, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
