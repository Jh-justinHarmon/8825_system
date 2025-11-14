#!/usr/bin/env python3
"""
Otter.ai API Client (Unofficial)
Uses: https://github.com/gmchad/otterai-api
"""

import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class OtterClient:
    """Unofficial Otter.ai API client"""
    
    def __init__(self, email: str, password: str):
        """
        Initialize Otter client
        
        Args:
            email: Otter.ai account email
            password: Otter.ai account password
        """
        self.email = email
        self.password = password
        self._otter = None
    
    def _get_client(self):
        """Get or create Otter client"""
        if self._otter is None:
            try:
                from otter import Otter
                self._otter = Otter(self.email, self.password)
            except ImportError:
                raise ImportError(
                    "Otter.ai API not installed. Install with:\n"
                    "pip install git+https://github.com/gmchad/otterai-api.git"
                )
        return self._otter
    
    def get_speeches(self, limit: int = 10) -> List[Dict]:
        """
        Get recent speeches/transcripts
        
        Args:
            limit: Maximum number of speeches to return
            
        Returns:
            List of speech objects with id, title, date, etc.
        """
        try:
            otter = self._get_client()
            speeches = otter.get_speeches(limit=limit)
            
            # Convert to dict format
            results = []
            for speech in speeches:
                results.append({
                    'id': speech.id,
                    'title': speech.title,
                    'date': speech.created_at,
                    'duration': getattr(speech, 'duration', None),
                    'participants': getattr(speech, 'participants', [])
                })
            
            return results
            
        except Exception as e:
            raise Exception(f"Failed to get speeches: {e}")
    
    def download_speech(self, speech_id: str, format: str = 'txt') -> str:
        """
        Download speech transcript
        
        Args:
            speech_id: Speech ID
            format: Format (txt, pdf, docx, srt)
            
        Returns:
            Transcript content as string
        """
        try:
            otter = self._get_client()
            
            if format == 'txt':
                content = otter.get_transcript_text(speech_id)
            elif format == 'pdf':
                content = otter.download_pdf(speech_id)
            elif format == 'docx':
                content = otter.download_docx(speech_id)
            elif format == 'srt':
                content = otter.download_srt(speech_id)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return content
            
        except Exception as e:
            raise Exception(f"Failed to download speech {speech_id}: {e}")
    
    def test_connection(self) -> bool:
        """Test if connection works"""
        try:
            speeches = self.get_speeches(limit=1)
            return True
        except Exception:
            return False

def main():
    """Test Otter client"""
    import sys
    import json
    
    if len(sys.argv) < 3:
        print("Usage: python3 otter_client.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    print("Testing Otter.ai connection...")
    client = OtterClient(email, password)
    
    if client.test_connection():
        print("✅ Connection successful!")
        
        speeches = client.get_speeches(limit=5)
        print(f"\nFound {len(speeches)} recent speeches:")
        
        for speech in speeches:
            print(f"\n- {speech['title']}")
            print(f"  ID: {speech['id']}")
            print(f"  Date: {speech['date']}")
    else:
        print("❌ Connection failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
