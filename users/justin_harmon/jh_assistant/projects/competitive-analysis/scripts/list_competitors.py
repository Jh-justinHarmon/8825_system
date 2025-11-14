#!/usr/bin/env python3
"""
List Competitors
View all tracked competitors
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_DIR = Path(__file__).parent.parent
COMPETITORS_FILE = PROJECT_DIR / "competitors.json"

def load_competitors():
    """Load competitors database"""
    if COMPETITORS_FILE.exists():
        with open(COMPETITORS_FILE, 'r') as f:
            return json.load(f)
    return {"competitors": [], "last_updated": ""}

def list_competitors():
    """Display all competitors"""
    data = load_competitors()
    competitors = data.get('competitors', [])
    
    if not competitors:
        print("📭 No competitors tracked yet")
        print("\n💡 Add one: python3 scripts/add_competitor.py")
        return
    
    print(f"\n📊 Tracked Competitors ({len(competitors)})")
    print("=" * 80)
    
    # Group by category
    categories = {}
    for comp in competitors:
        cat = comp.get('category', 'direct')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(comp)
    
    # Display by category
    for category, comps in sorted(categories.items()):
        print(f"\n🏷️  {category.upper()} ({len(comps)})")
        print("-" * 80)
        
        for comp in comps:
            print(f"\n   📌 {comp['name']}")
            print(f"      ID: {comp['competitor_id']}")
            print(f"      URL: {comp['url']}")
            print(f"      Added: {comp['added_date']}")
            
            # Show tech stack if available
            tech = comp.get('technology_stack', {})
            tech_items = []
            for key, values in tech.items():
                if values:
                    tech_items.extend(values)
            
            if tech_items:
                print(f"      Tech: {', '.join(tech_items[:5])}")
            
            # Show snapshots
            snapshots = comp.get('snapshots', [])
            if snapshots:
                print(f"      Snapshots: {len(snapshots)}")
            
            if comp.get('notes'):
                print(f"      Notes: {comp['notes']}")
    
    print("\n" + "=" * 80)
    print(f"Last updated: {data.get('last_updated', 'Never')}")
    print()

def main():
    print("🎯 Competitor List")
    list_competitors()

if __name__ == "__main__":
    main()
