#!/usr/bin/env python3
"""
Meeting Processor
Processes meeting transcripts and generates summaries
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict

class MeetingProcessor:
    """Process meeting transcripts"""
    
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.log_file = Path(config_path).parent / "logs/meeting_processor.log"
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Output directories
        self.output_base = Path(self.config['output']['knowledge_base'])
        self.transcripts_dir = self.output_base / self.config['output']['transcripts_dir']
        self.summaries_dir = self.output_base / self.config['output']['summaries_dir']
        self.json_dir = self.output_base / self.config['output']['json_dir']
        
        # Create directories
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)
        self.json_dir.mkdir(parents=True, exist_ok=True)
        
        self.log("📝 Meeting Processor initialized", "INFO")
    
    def process(self, transcript_data: Dict) -> bool:
        """
        Process meeting transcript
        
        Args:
            transcript_data: Dict with source, id, title, date, transcript, metadata
            
        Returns:
            True if successful
        """
        try:
            title = transcript_data['title']
            self.log(f"Processing: {title}", "INFO")
            
            # Generate filename
            date_str = self._parse_date(transcript_data['date'])
            safe_title = self._safe_filename(title)
            filename = f"{date_str}_{safe_title}"
            
            # Save transcript
            transcript_path = self.transcripts_dir / f"{filename}.txt"
            with open(transcript_path, 'w') as f:
                f.write(transcript_data['transcript'])
            self.log(f"  ✓ Saved transcript: {transcript_path.name}", "INFO")
            
            # Generate summary
            summary = self._generate_summary(transcript_data)
            
            # Save summary
            if 'markdown' in self.config['processing']['output_formats']:
                summary_path = self.summaries_dir / f"{filename}.md"
                with open(summary_path, 'w') as f:
                    f.write(summary)
                self.log(f"  ✓ Saved summary: {summary_path.name}", "INFO")
            
            # Save JSON
            if 'json' in self.config['processing']['output_formats']:
                json_path = self.json_dir / f"{filename}.json"
                json_data = {
                    'title': title,
                    'date': transcript_data['date'],
                    'source': transcript_data['source'],
                    'transcript': transcript_data['transcript'],
                    'summary': summary,
                    'metadata': transcript_data['metadata'],
                    'processed_at': datetime.now().isoformat()
                }
                with open(json_path, 'w') as f:
                    json.dump(json_data, f, indent=2)
                self.log(f"  ✓ Saved JSON: {json_path.name}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error processing: {e}", "ERROR")
            return False
    
    def _generate_summary(self, transcript_data: Dict) -> str:
        """Generate meeting summary"""
        # TODO: Use Chat Mining Agent or LLM for better summaries
        # For now, create basic summary
        
        title = transcript_data['title']
        date = transcript_data['date']
        transcript = transcript_data['transcript']
        metadata = transcript_data['metadata']
        
        summary = f"""# {title}

**Date:** {date}  
**Source:** {transcript_data['source']}  
**Duration:** {metadata.get('duration', 'N/A')}  
**Participants:** {', '.join(metadata.get('participants', ['N/A']))}

---

## Transcript

{transcript}

---

## Notes

- Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Source: {transcript_data['source']}

"""
        return summary
    
    def _parse_date(self, date_str: str) -> str:
        """Parse date to YYYYMMDD format"""
        try:
            # Try various date formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%a, %d %b %Y %H:%M:%S']:
                try:
                    dt = datetime.strptime(date_str.split('+')[0].strip(), fmt)
                    return dt.strftime('%Y%m%d')
                except:
                    continue
            
            # Fallback to today
            return datetime.now().strftime('%Y%m%d')
        except:
            return datetime.now().strftime('%Y%m%d')
    
    def _safe_filename(self, title: str) -> str:
        """Convert title to safe filename"""
        # Remove unsafe characters
        safe = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in title)
        # Limit length
        safe = safe[:50]
        # Remove extra spaces
        safe = '_'.join(safe.split())
        return safe
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Test meeting processor"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 meeting_processor.py <config_path>")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    processor = MeetingProcessor(config_path)
    
    # Test with sample data
    test_data = {
        'source': 'test',
        'id': 'test123',
        'title': 'TGIF Meeting Test',
        'date': '2025-11-11',
        'transcript': 'This is a test transcript.\n\nSpeaker 1: Hello\nSpeaker 2: Hi there',
        'metadata': {
            'duration': '30 min',
            'participants': ['Alice', 'Bob']
        }
    }
    
    success = processor.process(test_data)
    print(f"\nTest {'✅ PASSED' if success else '❌ FAILED'}")

if __name__ == '__main__':
    main()
