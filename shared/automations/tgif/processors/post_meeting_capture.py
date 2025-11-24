#!/usr/bin/env python3
"""
Post-Meeting Notes Capture Tool

Quickly save status updates, text messages, and operational notes
that don't make it into formal meeting transcripts.

Usage:
    python post_meeting_capture.py --interactive
    python post_meeting_capture.py --text "Your status update here"
    python post_meeting_capture.py --from-clipboard
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import argparse
import subprocess


class PostMeetingCapture:
    """Capture and save post-meeting operational notes"""
    
    def __init__(self, output_dir=None):
        if output_dir is None:
            # Default to HCSS meetings folder
            base = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825"
            output_dir = base / "8825_files/HCSS/meetings/post_meeting_notes"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def capture_interactive(self):
        """Interactive mode - prompt for details"""
        print("\n=== Post-Meeting Notes Capture ===\n")
        
        # Get basic info
        topic = input("Topic (brief, e.g., 'tgif_status_update'): ").strip()
        source_type = input("Source type (text/email/slack/verbal): ").strip() or "text"
        recipient = input("Who did you tell? ").strip()
        
        print("\nEnter your status update (press Ctrl+D when done):")
        print("---")
        
        # Read multi-line input
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        content = "\n".join(lines)
        
        # Save
        filename = self._generate_filename(topic)
        self._save_note(filename, {
            'topic': topic,
            'source_type': source_type,
            'recipient': recipient,
            'content': content
        })
        
        print(f"\n✅ Saved to: {filename}")
    
    def capture_text(self, text, topic=None, source_type="text"):
        """Capture from text string"""
        if not topic:
            # Auto-generate topic from first few words
            words = text.split()[:3]
            topic = "_".join(words).lower()
            topic = "".join(c for c in topic if c.isalnum() or c == "_")
        
        filename = self._generate_filename(topic)
        self._save_note(filename, {
            'topic': topic,
            'source_type': source_type,
            'content': text
        })
        
        print(f"✅ Saved to: {filename}")
        return filename
    
    def capture_from_clipboard(self):
        """Capture from clipboard"""
        try:
            # Try to get clipboard content (macOS)
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
            content = result.stdout
            
            if not content.strip():
                print("❌ Clipboard is empty")
                return None
            
            print("Clipboard content:")
            print("---")
            print(content[:200] + "..." if len(content) > 200 else content)
            print("---")
            
            topic = input("\nTopic (brief): ").strip()
            source_type = input("Source type (text/email/slack): ").strip() or "text"
            
            return self.capture_text(content, topic, source_type)
            
        except Exception as e:
            print(f"❌ Error reading clipboard: {e}")
            return None
    
    def _generate_filename(self, topic):
        """Generate filename with date and topic"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_topic = "".join(c for c in topic if c.isalnum() or c == "_")
        return f"{date_str}_{safe_topic}.md"
    
    def _save_note(self, filename, data):
        """Save note to markdown file"""
        filepath = self.output_dir / filename
        
        # Build markdown content
        md_content = f"""# {data.get('topic', 'Status Update').replace('_', ' ').title()} - Post-Meeting Notes

**Date:** {datetime.now().strftime("%Y-%m-%d")}  
**Type:** {data.get('source_type', 'text')}  
**Source:** {data.get('recipient', 'N/A')}  
**Context:** Post-meeting operational update

---

## Status Update

{data['content']}

---

## Context Notes

**Why This Matters:**
Operational details not captured in formal meeting transcripts.

**Preservation Reason:**
Real-time status update for stakeholders.

---

*Captured via post_meeting_capture.py - preserving operational context*
"""
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        # Also save JSON version for structured access
        json_path = filepath.with_suffix('.json')
        json_data = {
            'date': datetime.now().isoformat(),
            'filename': filename,
            'metadata': {
                'topic': data.get('topic'),
                'source_type': data.get('source_type'),
                'recipient': data.get('recipient')
            },
            'content': data['content']
        }
        
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=2)
    
    def list_recent(self, days=7):
        """List recent post-meeting notes"""
        files = sorted(self.output_dir.glob("*.md"), reverse=True)
        
        print(f"\n📋 Recent post-meeting notes (last {days} days):\n")
        
        count = 0
        for f in files:
            # Check if within days
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            age = (datetime.now() - mtime).days
            
            if age <= days:
                print(f"  • {f.name} ({age} days ago)")
                count += 1
        
        if count == 0:
            print("  (none)")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Capture post-meeting operational notes"
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help="Interactive mode - prompt for details"
    )
    parser.add_argument(
        '--text', '-t',
        type=str,
        help="Capture text directly"
    )
    parser.add_argument(
        '--from-clipboard', '-c',
        action='store_true',
        help="Capture from clipboard"
    )
    parser.add_argument(
        '--topic',
        type=str,
        help="Topic/title for the note"
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help="List recent notes"
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        help="Output directory (default: HCSS meetings folder)"
    )
    
    args = parser.parse_args()
    
    # Create capture instance
    capture = PostMeetingCapture(output_dir=args.output_dir)
    
    # Handle commands
    if args.list:
        capture.list_recent()
    elif args.interactive:
        capture.capture_interactive()
    elif args.from_clipboard:
        capture.capture_from_clipboard()
    elif args.text:
        capture.capture_text(args.text, topic=args.topic)
    else:
        # Default to interactive
        capture.capture_interactive()


if __name__ == "__main__":
    main()
