#!/usr/bin/env python3
"""
Check Downloads folder for Otter.ai exported txt transcripts
and process them automatically
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from meeting_processor import MeetingProcessor

def find_otter_transcripts(downloads_dir="/Users/justinharmon/Downloads"):
    """
    Find Otter.ai txt transcripts in Downloads folder
    
    Pattern: Looks for .txt files with otter_ai in name or meeting-like names
    """
    downloads = Path(downloads_dir)
    
    if not downloads.exists():
        print(f"❌ Downloads folder not found: {downloads_dir}")
        return []
    
    # Find all txt files
    txt_files = list(downloads.glob("*.txt"))
    
    # Filter for Otter transcripts (have timestamps like "0:06" and speaker names)
    otter_transcripts = []
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read(500)  # Check first 500 chars
                
                # Look for Otter patterns: "Speaker Name  0:06"
                if re.search(r'\w+\s+\d+:\d+', content):
                    otter_transcripts.append(txt_file)
                    print(f"✓ Found Otter transcript: {txt_file.name}")
        except:
            continue
    
    return otter_transcripts


def parse_transcript_file(txt_file):
    """
    Parse an Otter.ai txt file and create meeting_data dict
    
    Args:
        txt_file: Path to txt file
        
    Returns:
        meeting_data dict compatible with MeetingProcessor
    """
    with open(txt_file, 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    # Extract title from filename
    # Patterns: "Meeting Name_otter_ai.txt" or "Meeting Name Today at 10-30 am.txt"
    filename = txt_file.stem
    
    # Remove common suffixes
    title = filename.replace('_otter_ai', '')
    title = re.sub(r'\s+Today at \d+-\d+ \w+', '', title)
    title = title.strip()
    
    # Get file modified date as meeting date
    mtime = txt_file.stat().st_mtime
    meeting_date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    
    return {
        'title': title,
        'date': meeting_date,
        'email_date': datetime.fromtimestamp(mtime).isoformat(),
        'transcript': transcript,
        'otter_summary': None,
        'otter_link': None,
        'raw_body': None,
        'gmail_id': f"downloads_{txt_file.name}",
        'from': 'Downloads folder',
        'source': 'manual_export'
    }


def process_transcript_files(move_after_processing=True):
    """
    Find and process all Otter transcripts in Downloads
    
    Args:
        move_after_processing: Move processed files to archive subfolder
    """
    print("="*80)
    print("CHECKING DOWNLOADS FOR OTTER TRANSCRIPTS")
    print("="*80)
    
    # Find transcripts
    transcripts = find_otter_transcripts()
    
    if not transcripts:
        print("✅ No Otter transcripts found in Downloads")
        return 0
    
    print(f"\n📄 Found {len(transcripts)} transcript(s)")
    print("-"*80)
    
    # Setup processor
    processor = MeetingProcessor()
    output_dir = Path(__file__).parent.parent.parent.parent.parent / "8825_files" / "HCSS" / "meetings"
    
    processed_count = 0
    
    for i, txt_file in enumerate(transcripts, 1):
        print(f"\n[{i}/{len(transcripts)}] Processing: {txt_file.name}")
        
        try:
            # Parse txt file
            meeting_data = parse_transcript_file(txt_file)
            print(f"   Title: {meeting_data['title']}")
            print(f"   Date: {meeting_data['date']}")
            
            # Process with GPT-4
            processed = processor.process(meeting_data)
            
            if processed:
                # Save results
                processor.save_results(meeting_data, processed, output_dir)
                processed_count += 1
                print(f"   ✅ Processed successfully")
                
                # Move to archive
                if move_after_processing:
                    archive_dir = txt_file.parent / "processed_transcripts"
                    archive_dir.mkdir(exist_ok=True)
                    
                    archive_path = archive_dir / txt_file.name
                    txt_file.rename(archive_path)
                    print(f"   📦 Moved to: {archive_path}")
            else:
                print(f"   ❌ Processing failed")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print("-"*80)
    print(f"✅ Successfully processed: {processed_count}/{len(transcripts)}")
    print(f"📁 Output directory: {output_dir}")
    print(f"{'='*80}\n")
    
    return processed_count


if __name__ == '__main__':
    import sys
    
    # Check if --no-move flag
    move_files = '--no-move' not in sys.argv
    
    processed_count = process_transcript_files(move_after_processing=move_files)
    
    if processed_count > 0:
        print("\nNext steps:")
        print("  1. Review processed meetings in 8825_files/HCSS/meetings/")
        print("  2. Query meetings: python3 meeting_recall.py --from 2025-11-12")
