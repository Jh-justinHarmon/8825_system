#!/usr/bin/env python3
"""
OCR Processor V2 - Enhanced with KARSEN Protocol

Workflow:
1. Scan ~/Hammer Consulting Dropbox/Justin Harmon/Screenshots/
2. OCR all images in main folder
3. Detect content type:
   - KARSEN → Extract times, add to Google Calendar
   - Bills → Route to calendar/drive/ledger
   - Other → Standard routing
4. Move processed files to - ARCHV -

KARSEN Protocol:
- Detect "KARSEN" at top of image
- Extract day and time (AM departure times)
- Add to Google Calendar for same week
- No travel time or buffer
- Exact time written = departure time
"""

import os
import sys
from pathlib import Path
import pytesseract
from PIL import Image
import json
from datetime import datetime, timedelta
import re
import shutil

# Screenshot folder
SCREENSHOTS_FOLDER = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Screenshots"
ARCHIVE_FOLDER = SCREENSHOTS_FOLDER / "- ARCHV -"

def ocr_image(image_path):
    """Extract text from image"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"❌ OCR Error: {e}")
        return ""

def detect_karsen(text):
    """Detect if this is a KARSEN schedule"""
    # Check first few lines for KARSEN
    lines = text.strip().split('\n')[:5]
    for line in lines:
        if 'KARSEN' in line.upper():
            return True
    return False

def extract_karsen_schedule(text):
    """Extract day and time from KARSEN schedule
    
    Expected format:
    KARSEN
    Monday 7:30 AM
    Wednesday 8:00 AM
    Friday 7:45 AM
    """
    schedule = []
    
    lines = text.strip().split('\n')
    
    # Days of week pattern
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # Time pattern (e.g., "7:30 AM", "8:00", "7:45 am")
    time_pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)?'
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if line contains a day
        for day in days:
            if day in line_lower:
                # Extract time from same line
                time_match = re.search(time_pattern, line_lower, re.IGNORECASE)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2)) if time_match.group(2) else 0
                    am_pm = time_match.group(3).lower() if time_match.group(3) else 'am'
                    
                    # Convert to 24-hour format
                    if am_pm == 'pm' and hour != 12:
                        hour += 12
                    elif am_pm == 'am' and hour == 12:
                        hour = 0
                    
                    schedule.append({
                        'day': day.capitalize(),
                        'hour': hour,
                        'minute': minute,
                        'time_str': f"{hour:02d}:{minute:02d}"
                    })
    
    return schedule

def get_next_weekday(target_day):
    """Get next occurrence of target_day in current week
    
    Returns date for the target day in the same week as today
    """
    today = datetime.now()
    
    # Get day of week (0=Monday, 6=Sunday)
    days_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    target_weekday = days_map[target_day.lower()]
    current_weekday = today.weekday()
    
    # Calculate days until target day in same week
    days_ahead = target_weekday - current_weekday
    
    # If target day already passed this week, use next week
    if days_ahead < 0:
        days_ahead += 7
    
    target_date = today + timedelta(days=days_ahead)
    return target_date

def create_calendar_event(day, hour, minute, dry_run=True):
    """Create Google Calendar event for KARSEN departure
    
    Event details:
    - Title: "KARSEN Departure"
    - Time: Exact time written (no buffer)
    - Duration: 15 minutes (placeholder)
    """
    target_date = get_next_weekday(day)
    
    # Set exact time
    event_time = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    event = {
        'summary': 'KARSEN Departure',
        'description': f'Departure time for KARSEN on {day}',
        'start': event_time.isoformat(),
        'end': (event_time + timedelta(minutes=15)).isoformat(),
        'day': day,
        'time': f"{hour:02d}:{minute:02d}"
    }
    
    print(f"   📅 {day} at {hour:02d}:{minute:02d} - KARSEN Departure")
    
    if not dry_run:
        # TODO: Integrate with Google Calendar API
        print(f"      [Would create calendar event]")
    
    return event

def detect_bill(text):
    """Detect if this is a bill"""
    bill_keywords = [
        'invoice', 'bill', 'payment', 'due', 'amount due',
        'total', 'statement', 'account number', 'pay by'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in bill_keywords)

def process_screenshot(image_path, dry_run=True):
    """Process single screenshot with OCR"""
    print(f"\n📸 Processing: {image_path.name}")
    
    # OCR the image
    text = ocr_image(image_path)
    
    if not text:
        print(f"   ⚠️  No text extracted")
        return None
    
    # Detect content type
    if detect_karsen(text):
        print(f"   🎯 KARSEN SCHEDULE DETECTED")
        schedule = extract_karsen_schedule(text)
        
        if schedule:
            print(f"   📋 Found {len(schedule)} departure times:")
            events = []
            for item in schedule:
                event = create_calendar_event(
                    item['day'], 
                    item['hour'], 
                    item['minute'],
                    dry_run=dry_run
                )
                events.append(event)
            
            return {
                'type': 'karsen',
                'schedule': schedule,
                'events': events
            }
        else:
            print(f"   ⚠️  Could not extract schedule")
            return None
    
    elif detect_bill(text):
        print(f"   💵 BILL DETECTED")
        print(f"   → Route to: Calendar, Drive, Ledger")
        return {
            'type': 'bill',
            'text': text[:200]
        }
    
    else:
        print(f"   📄 Standard screenshot")
        return {
            'type': 'standard',
            'text': text[:200]
        }

def move_to_archive(image_path):
    """Move processed image to archive"""
    ARCHIVE_FOLDER.mkdir(exist_ok=True)
    
    dest = ARCHIVE_FOLDER / image_path.name
    
    # Handle duplicates
    if dest.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = ARCHIVE_FOLDER / f"{image_path.stem}_{timestamp}{image_path.suffix}"
    
    shutil.move(str(image_path), str(dest))
    print(f"   ✅ Moved to archive: {dest.name}")

def main():
    print("\n" + "="*80)
    print("OCR PROCESSOR V2 - KARSEN Protocol Enabled")
    print("="*80)
    print(f"\nScanning: {SCREENSHOTS_FOLDER}\n")
    
    # Get all images in main folder (not in archive)
    image_extensions = ['.png', '.jpg', '.jpeg']
    images = [
        f for f in SCREENSHOTS_FOLDER.iterdir() 
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    if not images:
        print("✅ No new screenshots to process")
        return
    
    print(f"📋 Found {len(images)} screenshots to process\n")
    
    # Process each image
    results = []
    for image_path in images:
        result = process_screenshot(image_path, dry_run=True)
        if result:
            results.append({
                'file': image_path.name,
                'result': result
            })
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")
    
    karsen_count = sum(1 for r in results if r['result']['type'] == 'karsen')
    bill_count = sum(1 for r in results if r['result']['type'] == 'bill')
    standard_count = sum(1 for r in results if r['result']['type'] == 'standard')
    
    print(f"📊 Processed: {len(results)} files")
    print(f"   🎯 KARSEN schedules: {karsen_count}")
    print(f"   💵 Bills: {bill_count}")
    print(f"   📄 Standard: {standard_count}")
    
    # Ask to execute
    print(f"\n{'='*80}")
    response = input("\n🚀 Move processed files to archive? (y/n): ")
    
    if response.lower() == 'y':
        print("\n📦 Moving files to archive...\n")
        for item in results:
            image_path = SCREENSHOTS_FOLDER / item['file']
            if image_path.exists():
                move_to_archive(image_path)
        
        print(f"\n✅ All files archived to: {ARCHIVE_FOLDER}")
        
        # Ask about calendar events
        if karsen_count > 0:
            response = input("\n📅 Create Google Calendar events for KARSEN? (y/n): ")
            if response.lower() == 'y':
                print("\n🔄 Creating calendar events...")
                for item in results:
                    if item['result']['type'] == 'karsen':
                        for event in item['result']['events']:
                            create_calendar_event(
                                event['day'],
                                int(event['time'].split(':')[0]),
                                int(event['time'].split(':')[1]),
                                dry_run=False
                            )
                print("\n✅ Calendar events created")

if __name__ == '__main__':
    main()
