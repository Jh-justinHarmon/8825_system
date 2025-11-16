#!/usr/bin/env python3
"""
Otter.ai API Client
Fetches transcripts directly from Otter.ai API
"""

import os
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

class OtterAPIClient:
    """Client for Otter.ai API"""
    
    def __init__(self, api_key=None):
        """
        Initialize Otter API client
        
        Args:
            api_key: Otter.ai API key (or use OTTER_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('OTTER_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Otter API key required. Set OTTER_API_KEY environment variable "
                "or pass api_key parameter"
            )
        
        self.base_url = "https://otter.ai/forward/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_speeches(self, folder=None, page_size=50):
        """
        Get list of speeches (meetings)
        
        Args:
            folder: Folder ID to filter by (optional)
            page_size: Number of results per page
            
        Returns:
            List of speech objects
        """
        endpoint = f"{self.base_url}/speeches"
        
        params = {
            "page_size": page_size
        }
        
        if folder:
            params["folder"] = folder
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("speeches", [])
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching speeches: {e}")
            return []
    
    def get_speech(self, speech_id: str) -> Optional[Dict]:
        """
        Get details for a specific speech
        
        Args:
            speech_id: Speech ID
            
        Returns:
            Speech object with transcript
        """
        endpoint = f"{self.base_url}/speeches/{speech_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching speech {speech_id}: {e}")
            return None
    
    def get_transcript(self, speech_id: str) -> Optional[str]:
        """
        Get transcript text for a speech
        
        Args:
            speech_id: Speech ID
            
        Returns:
            Transcript text
        """
        speech = self.get_speech(speech_id)
        
        if not speech:
            return None
        
        # Extract transcript from speech data
        # Otter API returns transcript in 'transcripts' field
        transcripts = speech.get("transcripts", [])
        
        if not transcripts:
            return None
        
        # Combine all transcript segments
        full_transcript = "\n".join([
            segment.get("transcript", "")
            for segment in transcripts
        ])
        
        return full_transcript
    
    def extract_speech_id_from_link(self, otter_link: str) -> Optional[str]:
        """
        Extract speech ID from Otter.ai link
        
        Args:
            otter_link: Otter.ai URL (e.g., https://otter.ai/u/abc123)
            
        Returns:
            Speech ID
        """
        # Parse URL to extract ID
        # Format: https://otter.ai/u/{speech_id}
        if "/u/" in otter_link:
            return otter_link.split("/u/")[-1].split("?")[0]
        
        return None
    
    def fetch_transcript_from_link(self, otter_link: str) -> Optional[Dict]:
        """
        Fetch transcript from Otter.ai link
        
        Args:
            otter_link: Otter.ai URL
            
        Returns:
            Dict with transcript and metadata
        """
        speech_id = self.extract_speech_id_from_link(otter_link)
        
        if not speech_id:
            print(f"❌ Could not extract speech ID from link: {otter_link}")
            return None
        
        print(f"📥 Fetching transcript for speech: {speech_id}")
        
        speech = self.get_speech(speech_id)
        
        if not speech:
            return None
        
        # Extract relevant data
        return {
            "speech_id": speech_id,
            "title": speech.get("title", "Unknown"),
            "created_at": speech.get("created_at"),
            "duration": speech.get("duration"),
            "transcript": self.get_transcript(speech_id),
            "summary": speech.get("summary"),
            "speakers": speech.get("speakers", []),
            "raw_data": speech
        }


class OtterAPIIntegration:
    """Integration between Otter API and meeting automation"""
    
    def __init__(self, api_key=None):
        """
        Initialize integration
        
        Args:
            api_key: Otter.ai API key
        """
        try:
            self.client = OtterAPIClient(api_key)
            self.available = True
        except ValueError as e:
            print(f"⚠️  Otter API not configured: {e}")
            self.available = False
    
    def fetch_missing_transcripts(self, meetings_data: List[Dict]) -> List[Dict]:
        """
        Fetch transcripts for meetings with empty transcripts
        
        Args:
            meetings_data: List of meeting dicts with otter_link
            
        Returns:
            List of updated meeting dicts
        """
        if not self.available:
            print("⚠️  Otter API not available, skipping")
            return meetings_data
        
        updated = []
        
        for meeting in meetings_data:
            # Check if transcript is empty
            if meeting.get("transcript") and meeting["transcript"].strip():
                updated.append(meeting)
                continue
            
            # Try to fetch from Otter
            otter_link = meeting.get("otter_link")
            
            if not otter_link:
                print(f"⚠️  No Otter link for: {meeting.get('title', 'Unknown')}")
                updated.append(meeting)
                continue
            
            print(f"🔄 Fetching transcript from Otter API: {meeting.get('title')}")
            
            transcript_data = self.client.fetch_transcript_from_link(otter_link)
            
            if transcript_data and transcript_data.get("transcript"):
                # Update meeting with fetched transcript
                meeting["transcript"] = transcript_data["transcript"]
                meeting["otter_api_fetched"] = True
                meeting["otter_api_fetch_date"] = datetime.now().isoformat()
                
                print(f"   ✅ Fetched {len(transcript_data['transcript'])} chars")
            else:
                print(f"   ❌ Could not fetch transcript")
            
            updated.append(meeting)
        
        return updated


def main():
    """CLI interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch transcripts from Otter.ai API")
    parser.add_argument("--link", help="Otter.ai link to fetch")
    parser.add_argument("--list", action="store_true", help="List recent speeches")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    
    args = parser.parse_args()
    
    try:
        client = OtterAPIClient()
        
        if args.test:
            print("🔌 Testing Otter API connection...")
            speeches = client.get_speeches(page_size=1)
            if speeches:
                print(f"✅ Connected! Found {len(speeches)} speech(es)")
            else:
                print("⚠️  Connected but no speeches found")
        
        elif args.list:
            print("📋 Fetching recent speeches...")
            speeches = client.get_speeches(page_size=10)
            
            for i, speech in enumerate(speeches, 1):
                print(f"\n{i}. {speech.get('title', 'Unknown')}")
                print(f"   ID: {speech.get('id')}")
                print(f"   Created: {speech.get('created_at')}")
                print(f"   Duration: {speech.get('duration')}s")
        
        elif args.link:
            print(f"📥 Fetching transcript from: {args.link}")
            data = client.fetch_transcript_from_link(args.link)
            
            if data:
                print(f"\n✅ Fetched successfully!")
                print(f"   Title: {data['title']}")
                print(f"   Transcript length: {len(data['transcript'])} chars")
                print(f"\n--- First 500 chars ---")
                print(data['transcript'][:500])
            else:
                print("❌ Failed to fetch transcript")
        
        else:
            parser.print_help()
    
    except ValueError as e:
        print(f"❌ {e}")
        print("\nTo use Otter API:")
        print("1. Get API key from https://otter.ai/developer")
        print("2. Set environment variable: export OTTER_API_KEY='your-key'")


if __name__ == "__main__":
    main()
