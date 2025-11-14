#!/usr/bin/env python3
"""
Add Competitor Tool
Quickly add a new competitor to track
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import uuid

# Paths
PROJECT_DIR = Path(__file__).parent.parent
COMPETITORS_FILE = PROJECT_DIR / "competitors.json"

def load_competitors():
    """Load competitors database"""
    if COMPETITORS_FILE.exists():
        with open(COMPETITORS_FILE, 'r') as f:
            return json.load(f)
    return {"competitors": [], "categories": {}, "last_updated": ""}

def save_competitors(data):
    """Save competitors database"""
    data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(COMPETITORS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_competitor(url, name, category="direct", notes=""):
    """Add a new competitor"""
    
    # Load existing data
    data = load_competitors()
    
    # Check if already exists
    for comp in data['competitors']:
        if comp['url'] == url:
            print(f"⚠️  Competitor already exists: {comp['name']}")
            return
    
    # Create new competitor entry
    competitor = {
        "competitor_id": str(uuid.uuid4())[:8],
        "name": name,
        "url": url,
        "added_date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "technology_stack": {
            "cms": [],
            "analytics": [],
            "hosting": [],
            "frameworks": [],
            "other": []
        },
        "company_info": {
            "description": "",
            "employees": "",
            "funding": "",
            "location": ""
        },
        "snapshots": [],
        "notes": notes
    }
    
    # Add to database
    data['competitors'].append(competitor)
    save_competitors(data)
    
    print(f"✅ Added competitor: {name}")
    print(f"   ID: {competitor['competitor_id']}")
    print(f"   URL: {url}")
    print(f"   Category: {category}")
    print(f"\n💡 Next steps:")
    print(f"   - Run analysis: python3 scripts/analyze_tech.py {competitor['competitor_id']}")
    print(f"   - View all: python3 scripts/list_competitors.py")

def main():
    print("🎯 Add Competitor Tool")
    print("=" * 50)
    
    # Get URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\n🌐 Enter competitor URL: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get name
    if len(sys.argv) > 2:
        name = sys.argv[2]
    else:
        name = input("📝 Enter competitor name: ").strip()
    
    if not name:
        print("❌ No name provided")
        return
    
    # Get category
    print("\n📊 Select category:")
    print("   1. Direct competitor")
    print("   2. Indirect competitor")
    print("   3. Potential competitor")
    
    if len(sys.argv) > 3:
        cat_input = sys.argv[3]
    else:
        cat_input = input("   Choice (1-3, default: 1): ").strip() or "1"
    
    category_map = {"1": "direct", "2": "indirect", "3": "potential"}
    category = category_map.get(cat_input, "direct")
    
    # Get notes
    if len(sys.argv) > 4:
        notes = sys.argv[4]
    else:
        notes = input("\n📋 Notes (optional): ").strip()
    
    # Add competitor
    print(f"\n⏳ Adding competitor...")
    add_competitor(url, name, category, notes)
    print()

if __name__ == "__main__":
    main()
