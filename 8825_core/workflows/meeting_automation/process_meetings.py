#!/usr/bin/env python3
"""
Process Meetings - Main Workflow
Poll Gmail → Process with GPT-4 → Save to files
"""

import sys
from pathlib import Path

# Import our modules
from gmail_otter_poller import GmailOtterPoller
from meeting_processor import MeetingProcessor
from check_downloads_for_transcripts import find_otter_transcripts, process_transcript_files

def main():
    """Main workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process new meeting transcripts from Gmail')
    parser.add_argument('--no-mark-read', action='store_true', help='Do not mark emails as read')
    parser.add_argument('--dry-run', action='store_true', help='Poll but do not process')
    
    args = parser.parse_args()
    
    print("="*80)
    print("MEETING AUTOMATION - High-Fidelity Processing")
    print("="*80)
    print()
    
    # Step 1: Poll Gmail
    print("STEP 1: Polling Gmail for new Otter.ai emails")
    print("-"*80)
    
    poller = GmailOtterPoller()
    
    try:
        meetings = poller.poll(
            mark_read=not args.no_mark_read,
            save_raw=True
        )
    except Exception as e:
        print(f"\n❌ Error polling Gmail: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    if not meetings:
        print("\n✅ No new meetings to process")
        return
    
    if args.dry_run:
        print(f"\n✅ Dry run complete - found {len(meetings)} meeting(s)")
        return
    
    # Step 2: Process with GPT-4
    print(f"\n{'='*80}")
    print(f"STEP 2: Processing {len(meetings)} meeting(s) with GPT-4")
    print("-"*80)
    
    processor = MeetingProcessor()
    
    # Output directory in 8825_files
    output_dir = Path(__file__).parent.parent.parent.parent.parent / "8825_files" / "HCSS" / "meetings"
    
    processed_count = 0
    failed_count = 0
    manual_needed_count = 0
    manual_needed_meetings = []
    
    for i, meeting_data in enumerate(meetings, 1):
        print(f"\n[{i}/{len(meetings)}] Processing: {meeting_data.get('title', 'Unknown')}")
        
        # Check if manual transcript needed
        if meeting_data.get('needs_manual_transcript'):
            print(f"   ⚠️  NEEDS MANUAL TRANSCRIPT")
            print(f"   📎 Link: {meeting_data.get('otter_link')}")
            manual_needed_count += 1
            manual_needed_meetings.append({
                'title': meeting_data.get('title'),
                'link': meeting_data.get('otter_link'),
                'gmail_id': meeting_data.get('gmail_id')
            })
            continue
        
        try:
            processed = processor.process(meeting_data)
            
            if processed:
                # Save to 8825_files
                processor.save_results(meeting_data, processed, output_dir)
                processed_count += 1
            else:
                failed_count += 1
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed_count += 1
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print("-"*80)
    print(f"✅ Successfully processed: {processed_count}")
    if failed_count > 0:
        print(f"❌ Failed: {failed_count}")
    if manual_needed_count > 0:
        print(f"⚠️  Needs manual transcript: {manual_needed_count}")
    print(f"📁 Output directory: {output_dir}")
    print(f"{'='*80}\n")
    
    if manual_needed_count > 0:
        print("⚠️  MEETINGS NEED MANUAL TRANSCRIPTS:")
        print("-"*80)
        for mtg in manual_needed_meetings:
            print(f"\nMeeting: {mtg['title']}")
            print(f"Link: {mtg['link']}")
            print(f"\n📋 WORKFLOW:")
            print(f"  1. Open: {mtg['link']}")
            print(f"  2. Click 'Export' → 'Export to text (.txt)'")
            print(f"  3. Save to Downloads folder")
            print(f"  4. Run this script again - it will auto-detect and process")
        print(f"\n{'='*80}")
        
        # Check Downloads folder for exported transcripts
        print("\n🔍 Checking Downloads folder for exported transcripts...")
        transcripts_in_downloads = find_otter_transcripts()
        
        if transcripts_in_downloads:
            print(f"\n✨ FOUND {len(transcripts_in_downloads)} TRANSCRIPT(S) IN DOWNLOADS!")
            print("Processing them now...\n")
            
            downloads_processed = process_transcript_files(move_after_processing=True)
            
            if downloads_processed > 0:
                processed_count += downloads_processed
                manual_needed_count -= downloads_processed
        else:
            print("   No transcripts found yet. Export from Otter.ai and run again.")
        
        print(f"\n{'='*80}\n")
    
    if processed_count > 0:
        print("Next steps:")
        print("  1. Review processed meetings in 8825_files/HCSS/meetings/")
        print("  2. Query meetings: python3 meeting_recall.py --from 2025-11-12")
        print("  3. Generate summary: python3 meeting_recall.py --last-week")

if __name__ == '__main__':
    main()
