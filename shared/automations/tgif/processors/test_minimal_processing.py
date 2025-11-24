#!/usr/bin/env python3
"""
Test minimal processing on existing meetings from Nov 11-13
"""

import json
import sys
from pathlib import Path
from minimal_meeting_processor import MinimalMeetingProcessor

def main():
    # Path to meetings
    meetings_dir = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825_files/HCSS/meetings"
    
    # Find all JSON files from Nov 11-13
    meeting_files = []
    for date in ['2025-11-11', '2025-11-12', '2025-11-13']:
        meeting_files.extend(meetings_dir.glob(f"{date.replace('-', '-')}*.json"))
    
    # Also check for None_ prefixed files (from email processing)
    meeting_files.extend([f for f in meetings_dir.glob("None_*.json") if f.stat().st_mtime > 1731283200])  # Nov 11
    
    print(f"\n🔍 Found {len(meeting_files)} meetings to process\n")
    
    # Initialize processor
    processor = MinimalMeetingProcessor()
    
    results = []
    
    for meeting_file in meeting_files:
        print(f"📄 Processing: {meeting_file.name}")
        
        try:
            # Load existing meeting data
            with open(meeting_file, 'r') as f:
                data = json.load(f)
            
            # Extract transcript
            transcript = None
            title = "Unknown Meeting"
            date = "2025-11-13"
            
            if 'original_data' in data:
                transcript = data['original_data'].get('transcript', '')
                title = data['original_data'].get('title', title)
                date = data['original_data'].get('date', date)
            elif 'transcript' in data:
                transcript = data['transcript']
                title = data.get('title', title)
                date = data.get('date', date)
            
            if not transcript:
                print(f"   ⚠️  No transcript found, skipping\n")
                continue
            
            # Process with minimal processor
            email_data = {
                'subject': title,
                'date': date
            }
            
            result = processor.process_otter_transcript(transcript, email_data)
            results.append(result)
            
            print(f"   ✅ Saved:")
            print(f"      Transcript: {Path(result['transcript_path']).name}")
            print(f"      Metadata: {Path(result['metadata_path']).name}")
            print(f"      Duration: {result['metadata']['duration_minutes']} min")
            print(f"      Attendees: {', '.join(result['metadata']['attendees'][:3])}")
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            continue
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Processed {len(results)} meetings")
    print(f"{'='*60}\n")
    
    # Show timesheet summary
    print("📊 Timesheet Summary:\n")
    total_hours = 0
    for result in results:
        timesheet = processor.generate_timesheet_entry(result['metadata_path'])
        print(f"   {timesheet['date']} | {timesheet['duration_hours']}h | {timesheet['title'][:40]}")
        total_hours += timesheet['duration_hours']
    
    print(f"\n   Total: {total_hours:.2f} hours")
    print()


if __name__ == "__main__":
    main()
