#!/usr/bin/env python3
"""Test meeting transcript classification"""

from pathlib import Path
from smart_classifier import SmartClassifier

def test_meeting_classification():
    """Test meeting transcript detection"""
    config_path = Path(__file__).parent.parent / "sandbox_target_acquisition/user_config.json"
    classifier = SmartClassifier(config_path)
    
    # Test files
    test_files = [
        # Meeting transcripts (should be detected)
        Path("/Users/test/Downloads/TGIF_Meeting_2025-11-11.txt"),
        Path("/Users/test/Downloads/Otter_Transcript_Nov_11.txt"),
        Path("/Users/test/Downloads/Meeting_Notes_2025-11-11.pdf"),
        Path("/Users/test/Downloads/Conversation with Team - 2025-11-11.txt"),
        Path("/Users/test/Downloads/conference_call_transcript.docx"),
        
        # Not meeting transcripts (should not be detected)
        Path("/Users/test/Downloads/meeting_notes.json"),  # JSON = ingestion
        Path("/Users/test/Downloads/random_document.txt"),  # No meeting keywords
        Path("/Users/test/Downloads/invoice.pdf"),  # PDF but no meeting keywords
    ]
    
    print("=" * 60)
    print("MEETING TRANSCRIPT CLASSIFICATION TEST")
    print("=" * 60)
    print()
    
    for file in test_files:
        result = classifier.classify(file)
        
        is_meeting = result['action'] == 'meeting'
        icon = "✅" if is_meeting else "❌"
        
        print(f"{icon} {file.name}")
        print(f"   Action: {result['action']}")
        print(f"   Processor: {result['processor']}")
        print(f"   Reason: {result['reason']}")
        print()
    
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_meeting_classification()
