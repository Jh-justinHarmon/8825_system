#!/usr/bin/env python3
"""
Basic Competitor Analysis
Gather basic information without requiring paid APIs
"""

import json
import sys
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import re

# Paths
PROJECT_DIR = Path(__file__).parent.parent
COMPETITORS_FILE = PROJECT_DIR / "competitors.json"
DATA_DIR = PROJECT_DIR / "data" / "snapshots"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_competitors():
    """Load competitors database"""
    if COMPETITORS_FILE.exists():
        with open(COMPETITORS_FILE, 'r') as f:
            return json.load(f)
    return {"competitors": []}

def save_competitors(data):
    """Save competitors database"""
    data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(COMPETITORS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def fetch_page(url):
    """Fetch webpage content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        return response.text if response.status_code == 200 else None
    except:
        return None

def extract_meta_tags(html):
    """Extract meta tags from HTML"""
    meta_data = {}
    
    # Description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.I)
    if desc_match:
        meta_data['description'] = desc_match.group(1)
    
    # Keywords
    keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', html, re.I)
    if keywords_match:
        meta_data['keywords'] = keywords_match.group(1)
    
    # Title
    title_match = re.search(r'<title>([^<]+)</title>', html, re.I)
    if title_match:
        meta_data['title'] = title_match.group(1).strip()
    
    # OG tags
    og_title = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html, re.I)
    if og_title:
        meta_data['og_title'] = og_title.group(1)
    
    og_desc = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']', html, re.I)
    if og_desc:
        meta_data['og_description'] = og_desc.group(1)
    
    return meta_data

def detect_technologies(html):
    """Detect technologies used (basic detection)"""
    tech = {
        "cms": [],
        "analytics": [],
        "frameworks": [],
        "other": []
    }
    
    # CMS detection
    if 'wp-content' in html or 'wordpress' in html.lower():
        tech['cms'].append('WordPress')
    if 'shopify' in html.lower():
        tech['cms'].append('Shopify')
    if 'wix.com' in html:
        tech['cms'].append('Wix')
    if 'squarespace' in html.lower():
        tech['cms'].append('Squarespace')
    
    # Analytics
    if 'google-analytics' in html or 'gtag' in html:
        tech['analytics'].append('Google Analytics')
    if 'mixpanel' in html.lower():
        tech['analytics'].append('Mixpanel')
    if 'segment' in html.lower():
        tech['analytics'].append('Segment')
    
    # Frameworks
    if 'react' in html.lower():
        tech['frameworks'].append('React')
    if 'vue' in html.lower():
        tech['frameworks'].append('Vue.js')
    if 'angular' in html.lower():
        tech['frameworks'].append('Angular')
    if 'next.js' in html.lower() or '_next' in html:
        tech['frameworks'].append('Next.js')
    
    # Other
    if 'stripe' in html.lower():
        tech['other'].append('Stripe')
    if 'intercom' in html.lower():
        tech['other'].append('Intercom')
    if 'hubspot' in html.lower():
        tech['other'].append('HubSpot')
    
    return tech

def analyze_competitor(competitor_id):
    """Analyze a specific competitor"""
    data = load_competitors()
    
    # Find competitor
    competitor = None
    for comp in data['competitors']:
        if comp['competitor_id'] == competitor_id or comp['name'].lower() == competitor_id.lower():
            competitor = comp
            break
    
    if not competitor:
        print(f"❌ Competitor not found: {competitor_id}")
        return
    
    print(f"\n🔍 Analyzing: {competitor['name']}")
    print(f"   URL: {competitor['url']}")
    print("=" * 60)
    
    # Fetch page
    print("\n⏳ Fetching webpage...")
    html = fetch_page(competitor['url'])
    
    if not html:
        print("❌ Could not fetch webpage")
        return
    
    print("✅ Page fetched")
    
    # Extract meta tags
    print("\n📋 Extracting meta information...")
    meta_data = extract_meta_tags(html)
    
    if meta_data.get('title'):
        print(f"   Title: {meta_data['title']}")
    if meta_data.get('description'):
        print(f"   Description: {meta_data['description'][:100]}...")
    
    # Detect technologies
    print("\n🔧 Detecting technologies...")
    tech = detect_technologies(html)
    
    for category, items in tech.items():
        if items:
            print(f"   {category.upper()}: {', '.join(items)}")
            competitor['technology_stack'][category] = list(set(
                competitor['technology_stack'].get(category, []) + items
            ))
    
    # Update company info
    if meta_data.get('description'):
        competitor['company_info']['description'] = meta_data['description']
    
    # Create snapshot
    snapshot = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "meta_data": meta_data,
        "technology_stack": tech,
        "page_size": len(html),
        "analysis_type": "basic"
    }
    
    competitor['snapshots'].append(snapshot)
    
    # Save snapshot to file
    snapshot_file = DATA_DIR / f"{competitor['competitor_id']}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"\n💾 Snapshot saved: {snapshot_file.name}")
    
    # Save updated data
    save_competitors(data)
    
    print("\n✅ Analysis complete!")
    print(f"\n📊 Total snapshots for {competitor['name']}: {len(competitor['snapshots'])}")
    print()

def main():
    print("🎯 Basic Competitor Analysis")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage: python3 analyze_basic.py <competitor_id or name>")
        print("\n💡 List competitors: python3 list_competitors.py")
        return
    
    competitor_id = sys.argv[1]
    analyze_competitor(competitor_id)

if __name__ == "__main__":
    main()
