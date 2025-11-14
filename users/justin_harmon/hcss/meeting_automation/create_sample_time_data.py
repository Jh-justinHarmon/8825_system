#!/usr/bin/env python3
"""
Create sample meeting data with duration for testing time tracker
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

def create_sample_meetings():
    """Create sample meeting data for last 2 weeks"""
    
    # Base path
    json_dir = Path("users/justin_harmon/hcss/knowledge/meetings/json")
    json_dir.mkdir(parents=True, exist_ok=True)
    
    # Start date: 2 weeks ago from today (Oct 28, 2025)
    start_date = datetime(2025, 10, 28)
    
    # Sample meetings with realistic durations
    meetings = [
        # Week 1 (Oct 28 - Nov 3)
        {"date": "2025-10-28", "title": "TGIF Weekly Sync", "duration": "1 hour", "client": "TGIF"},
        {"date": "2025-10-29", "title": "HCSS Technical Review", "duration": "45 min", "client": "HCSS"},
        {"date": "2025-10-30", "title": "TGIF Operations Meeting", "duration": "1 hour 30 min", "client": "TGIF"},
        {"date": "2025-10-31", "title": "RAL Project Kickoff", "duration": "2 hours", "client": "RAL"},
        {"date": "2025-11-01", "title": "TGIF Store Rollout Planning", "duration": "1 hour 15 min", "client": "TGIF"},
        
        # Week 2 (Nov 4 - Nov 10)
        {"date": "2025-11-04", "title": "TGIF Weekly Sync - Store Rollout", "duration": "1 hour", "client": "TGIF"},
        {"date": "2025-11-05", "title": "HCSS Architecture Review", "duration": "2 hours", "client": "HCSS"},
        {"date": "2025-11-06", "title": "TGIF Operations Review", "duration": "1 hour 30 min", "client": "TGIF"},
        {"date": "2025-11-06", "title": "RAL Sprint Planning", "duration": "1 hour", "client": "RAL"},
        {"date": "2025-11-07", "title": "HCSS Integration Meeting", "duration": "45 min", "client": "HCSS"},
        {"date": "2025-11-08", "title": "TGIF Pricing Strategy Session", "duration": "2 hours", "client": "TGIF"},
        {"date": "2025-11-08", "title": "RAL Technical Deep Dive", "duration": "1 hour 30 min", "client": "RAL"},
    ]
    
    print("Creating sample meeting data...\n")
    
    for meeting in meetings:
        # Create filename
        date_str = meeting['date'].replace('-', '')
        safe_title = meeting['title'].replace(' ', '_').replace('-', '_')
        filename = f"{date_str}_{safe_title}.json"
        
        # Create meeting data structure
        data = {
            "title": meeting['title'],
            "date": meeting['date'],
            "source": "sample_data",
            "transcript": f"Sample transcript for {meeting['title']}",
            "summary": f"# {meeting['title']}\n\nSample meeting summary.",
            "metadata": {
                "duration": meeting['duration'],
                "participants": ["Justin Harmon", "Team"],
                "client": meeting['client']
            },
            "processed_at": datetime.now().isoformat()
        }
        
        # Save to file
        filepath = json_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Created: {filename}")
        print(f"   Date: {meeting['date']}, Duration: {meeting['duration']}, Client: {meeting['client']}")
    
    print(f"\n✅ Created {len(meetings)} sample meetings in:")
    print(f"   {json_dir.absolute()}")

if __name__ == '__main__':
    create_sample_meetings()
