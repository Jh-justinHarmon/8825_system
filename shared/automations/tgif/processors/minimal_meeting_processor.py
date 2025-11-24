#!/usr/bin/env python3
"""
Minimal Meeting Processor

Extracts ONLY what's needed for timesheets:
- Date/time
- Duration
- Attendees
- Meeting title

Preserves full transcript for Cascade to read when needed.

NO heavy summarization. NO OpenAI calls. Just metadata + raw transcript.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class MinimalMeetingProcessor:
    """Extract minimal metadata from meeting transcripts"""
    
    def __init__(self, output_dir=None):
        if output_dir is None:
            base = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825"
            output_dir = base / "8825_files/HCSS/meetings"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "transcripts").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
    
    def process_otter_transcript(self, transcript_text: str, email_data: Dict = None) -> Dict:
        """
        Process Otter transcript - extract minimal metadata only
        
        Args:
            transcript_text: Raw transcript from Otter
            email_data: Optional email metadata (date, title, etc.)
        
        Returns:
            Dict with metadata and paths to saved files
        """
        # Extract metadata
        metadata = self._extract_metadata(transcript_text, email_data)
        
        # Generate filename
        date_str = metadata['date'].replace('-', '')
        safe_title = self._sanitize_filename(metadata['title'])
        base_filename = f"{date_str}_{safe_title}"
        
        # Save full transcript
        transcript_path = self.output_dir / "transcripts" / f"{base_filename}.txt"
        with open(transcript_path, 'w') as f:
            f.write(transcript_text)
        
        # Save metadata JSON
        metadata_path = self.output_dir / "metadata" / f"{base_filename}.json"
        metadata['transcript_path'] = str(transcript_path)
        metadata['processed_at'] = datetime.now().isoformat()
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'metadata': metadata,
            'transcript_path': str(transcript_path),
            'metadata_path': str(metadata_path)
        }
    
    def _extract_metadata(self, transcript: str, email_data: Dict = None) -> Dict:
        """Extract minimal metadata from transcript"""
        
        metadata = {
            'title': 'Unknown Meeting',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': None,
            'duration_minutes': None,
            'attendees': [],
            'source': 'otter'
        }
        
        # Use email data if available
        if email_data:
            metadata['title'] = email_data.get('subject', metadata['title'])
            if 'date' in email_data:
                metadata['date'] = email_data['date']
        
        # Extract attendees from transcript
        # Otter format: "Name  timestamp\ntext"
        attendee_pattern = r'^([A-Z][a-z]+(?: [A-Z][a-z]+)*)\s+\d+:\d+\s*$'
        attendees = set()
        
        for line in transcript.split('\n'):
            match = re.match(attendee_pattern, line.strip())
            if match:
                attendees.add(match.group(1))
        
        metadata['attendees'] = sorted(list(attendees))
        
        # Try to extract duration from transcript length (rough estimate)
        # Assume ~150 words per minute of speaking
        word_count = len(transcript.split())
        estimated_minutes = max(15, round(word_count / 150))  # Min 15 min
        metadata['duration_minutes'] = estimated_minutes
        
        return metadata
    
    def _sanitize_filename(self, title: str) -> str:
        """Convert title to safe filename"""
        # Remove special chars, convert to lowercase, replace spaces with underscores
        safe = re.sub(r'[^\w\s-]', '', title.lower())
        safe = re.sub(r'[-\s]+', '_', safe)
        return safe[:50]  # Limit length
    
    def process_from_email(self, email_body: str, email_subject: str, email_date: str) -> Dict:
        """Process meeting from email"""
        
        # Extract transcript from email body
        # Otter emails typically have transcript after certain markers
        transcript = self._extract_transcript_from_email(email_body)
        
        email_data = {
            'subject': email_subject,
            'date': email_date
        }
        
        return self.process_otter_transcript(transcript, email_data)
    
    def _extract_transcript_from_email(self, email_body: str) -> str:
        """Extract transcript text from Otter email body"""
        # This is a simple extraction - adjust based on actual email format
        # Usually transcript is after "Transcript:" or similar
        
        # Try to find transcript section
        markers = ['Transcript:', 'Conversation:', '---']
        
        for marker in markers:
            if marker in email_body:
                parts = email_body.split(marker, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        
        # If no marker found, return whole body
        return email_body
    
    def generate_timesheet_entry(self, metadata_path: str) -> Dict:
        """Generate timesheet entry from metadata"""
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        return {
            'date': metadata['date'],
            'duration_minutes': metadata['duration_minutes'],
            'duration_hours': round(metadata['duration_minutes'] / 60, 2),
            'title': metadata['title'],
            'attendees': metadata['attendees'],
            'project': 'HCSS/TGIF',  # Could be extracted from title
            'billable': True
        }


def main():
    """Test the processor"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python minimal_meeting_processor.py <transcript_file>")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    
    with open(transcript_file, 'r') as f:
        transcript = f.read()
    
    processor = MinimalMeetingProcessor()
    result = processor.process_otter_transcript(transcript)
    
    print("\n✅ Processed meeting:")
    print(f"   Transcript: {result['transcript_path']}")
    print(f"   Metadata: {result['metadata_path']}")
    print("\nMetadata:")
    print(json.dumps(result['metadata'], indent=2))
    
    print("\nTimesheet entry:")
    timesheet = processor.generate_timesheet_entry(result['metadata_path'])
    print(json.dumps(timesheet, indent=2))


if __name__ == "__main__":
    main()
