#!/usr/bin/env python3
"""
Smart Classifier - Routes files by type and content
Part of Unified File Processing System
"""

import json
from pathlib import Path
from typing import Dict, Optional

class SmartClassifier:
    """Classify files and determine routing"""
    
    # File type categories
    INGESTION_TYPES = {'.json', '.txt', '.txf'}
    IMAGE_TYPES = {'.png', '.jpg', '.jpeg', '.gif', '.heic', '.heif'}
    DOCUMENT_TYPES = {'.pdf', '.doc', '.docx', '.xls', '.xlsx'}
    MEETING_TYPES = {'.txt', '.pdf', '.docx', '.srt'}  # Meeting transcript formats
    SKIP_TYPES = {'.zip', '.tmp'}  # Files to skip entirely
    
    # Protected files (never move)
    PROTECTED_PATTERNS = [
        'BRAIN_TRANSPORT',
        '8825_BRAIN',
        '.DS_Store'
    ]
    
    # Meeting transcript patterns
    MEETING_PATTERNS = [
        'otter',
        'tgif',
        'meeting',
        'transcript',
        'call',
        'conference'
    ]
    
    def __init__(self, config_path: Path):
        """Initialize with config"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.ingestion_path = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/ingestion"
    
    def classify(self, file_path: Path) -> Dict:
        """
        Classify file and return routing decision
        
        Returns:
            {
                'action': 'ingestion' | 'screenshot' | 'progressive' | 'protected',
                'destination': Path or None,
                'processor': 'ingestion_router' | 'screenshot_processor' | 'progressive_router',
                'reason': str
            }
        """
        file_path = Path(file_path)
        
        # Check file extension first
        ext = file_path.suffix.lower()
        
        # Skip certain file types entirely
        if ext in self.SKIP_TYPES:
            return {
                'action': 'skip',
                'destination': None,
                'processor': None,
                'reason': f'Skipping {ext} file - manual inspection only'
            }
        
        # Check if file is protected
        if self._is_protected(file_path):
            return {
                'action': 'protected',
                'destination': self.config['outputs']['brain'],
                'processor': 'output_manager',
                'reason': 'Protected file - copy to output, keep in place'
            }
        
        # Check for meeting transcripts (before ingestion check)
        if self._is_meeting_transcript(file_path):
            return {
                'action': 'meeting',
                'destination': None,  # Determined by user config
                'processor': 'meeting_router',
                'reason': 'Meeting transcript → User-specific processor'
            }
        
        # Route JSON/TXT/TXF to ingestion
        if ext in self.INGESTION_TYPES:
            return {
                'action': 'ingestion',
                'destination': self.ingestion_path,
                'processor': 'ingestion_router',
                'reason': f'File type {ext} → Ingestion system'
            }
        
        # Route screenshots
        if self._is_screenshot(file_path):
            return {
                'action': 'screenshot',
                'destination': None,  # Determined by protocol
                'processor': 'screenshot_processor',
                'reason': 'Screenshot → Protocol matching'
            }
        
        # Everything else to progressive router
        return {
            'action': 'progressive',
            'destination': None,  # Determined by router
            'processor': 'progressive_router',
            'reason': 'General file → Progressive router'
        }
    
    def _is_protected(self, file_path: Path) -> bool:
        """Check if file is protected"""
        filename = file_path.name
        for pattern in self.PROTECTED_PATTERNS:
            if pattern in filename:
                return True
        return False
    
    def _is_screenshot(self, file_path: Path) -> bool:
        """Check if file is a screenshot"""
        # Check if from Screenshots folder
        screenshots_path = Path(self.config['inputs']['screenshots'])
        if screenshots_path in file_path.parents:
            return True
        
        # Check filename patterns
        filename = file_path.name.lower()
        if 'screenshot' in filename or 'screen shot' in filename:
            return True
        
        return False
    
    def _is_meeting_transcript(self, file_path: Path) -> bool:
        """
        Check if file is a meeting transcript
        
        Detection logic:
        1. Check file extension (txt, pdf, docx, srt)
        2. Check filename for meeting keywords
        3. Check if from Otter.ai (email attachment pattern)
        """
        filename = file_path.name.lower()
        ext = file_path.suffix.lower()
        
        # Must be a meeting-compatible format
        if ext not in self.MEETING_TYPES:
            return False
        
        # Check for meeting patterns in filename
        for pattern in self.MEETING_PATTERNS:
            if pattern in filename:
                return True
        
        # Check for Otter.ai specific patterns
        # Otter files often have format: "Conversation with X - YYYY-MM-DD.txt"
        if 'conversation' in filename and ext == '.txt':
            return True
        
        return False

def main():
    """Test classifier"""
    config_path = Path(__file__).parent.parent / "sandbox_target_acquisition/user_config.json"
    classifier = SmartClassifier(config_path)
    
    # Test files
    test_files = [
        Path("/Users/test/Downloads/meeting_notes.json"),
        Path("/Users/test/Downloads/8825_BRAIN_TRANSPORT.json"),
        Path("/Users/test/Screenshots/Screenshot 2025-11-11.png"),
        Path("/Users/test/Downloads/invoice.pdf"),
    ]
    
    for file in test_files:
        result = classifier.classify(file)
        print(f"\n{file.name}:")
        print(f"  Action: {result['action']}")
        print(f"  Processor: {result['processor']}")
        print(f"  Reason: {result['reason']}")

if __name__ == '__main__':
    main()
