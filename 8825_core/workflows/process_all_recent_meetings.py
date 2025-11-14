#!/usr/bin/env python3
"""
Process all recent HCSS meetings - extended date range
"""

from meeting_summary_pipeline import MeetingSummaryPipeline
from datetime import datetime, timedelta

def main():
    """Process all meetings from the past 2 weeks"""
    pipeline = MeetingSummaryPipeline()
    
    # Get date range for past 2 weeks
    today = datetime.now().date()
    two_weeks_ago = today - timedelta(days=14)
    
    print(f"\n{'='*60}")
    print(f"Processing ALL meetings from {two_weeks_ago} to {today}")
    print(f"{'='*60}\n")
    
    # Convert to datetime
    start_date = datetime.combine(two_weeks_ago, datetime.min.time())
    end_date = datetime.combine(today, datetime.max.time())
    
    # Scan for meetings
    meeting_files = pipeline.scan_for_meetings(start_date, end_date)
    
    if not meeting_files:
        print(f"⚠️  No meetings found")
        return
    
    print(f"Found {len(meeting_files)} meeting(s):\n")
    
    # Process each meeting
    generated_docs = []
    all_meetings = []
    
    for meeting_file in meeting_files:
        print(f"Processing: {meeting_file.name}")
        
        try:
            # Parse meeting
            meeting = pipeline.parse_meeting_file(meeting_file)
            all_meetings.append(meeting)
            
            # Generate Word doc
            doc_path = pipeline.generate_word_doc(meeting)
            generated_docs.append(doc_path)
            
            print(f"✅ Generated: {doc_path.name}\n")
        
        except Exception as e:
            print(f"❌ Error processing {meeting_file.name}: {e}\n")
    
    # Generate weekly summary
    if all_meetings:
        print("Generating weekly summary...")
        summary_path = pipeline.generate_weekly_summary(all_meetings)
        print(f"✅ Generated: {summary_path.name}\n")
        generated_docs.append(summary_path)
    
    print(f"\n{'='*60}")
    print(f"Summary: Generated {len(generated_docs)} Word document(s)")
    print(f"Output directory: {pipeline.output_dir}")
    print(f"{'='*60}\n")
    
    # List all generated files
    print("Generated files:")
    for doc in generated_docs:
        print(f"  • {doc.name}")
    print()

if __name__ == "__main__":
    main()
