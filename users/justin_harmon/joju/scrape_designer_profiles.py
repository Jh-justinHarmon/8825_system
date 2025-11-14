#!/usr/bin/env python3
"""
Scrape designer-specific profiles (LinkedIn, Dribbble)
"""

import requests
import json
import re

def scrape_dribbble(username):
    """Scrape Dribbble profile"""
    print(f"🎨 Scraping Dribbble for: {username}")
    
    url = f"https://dribbble.com/{username}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        data = {
            "url": url,
            "username": username,
            "scraped": True
        }
        
        # Extract description from meta tag
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
        if desc_match:
            data['description'] = desc_match.group(1)
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', html)
        if title_match:
            data['title'] = title_match.group(1)
        
        # Try to find stats (shots, followers, etc.)
        # Look for common patterns in Dribbble HTML
        if 'shots' in html.lower():
            data['has_shots'] = True
        
        print(f"✅ Dribbble data found")
        return data
        
    except Exception as e:
        print(f"⚠️  Dribbble scraping failed: {e}")
        return {"url": url, "scraped": False, "error": str(e)}

def scrape_linkedin(profile_url):
    """Scrape LinkedIn profile (basic)"""
    print(f"💼 Scraping LinkedIn: {profile_url}")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(profile_url, headers=headers, timeout=10)
        html = response.text
        
        data = {
            "url": profile_url,
            "scraped": True
        }
        
        # Extract from meta tags using regex
        og_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if og_title:
            data['title'] = og_title.group(1)
        
        og_description = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        if og_description:
            data['description'] = og_description.group(1)
        
        og_image = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if og_image:
            data['image'] = og_image.group(1)
        
        # Extract page title
        title_match = re.search(r'<title>([^<]+)</title>', html)
        if title_match:
            data['page_title'] = title_match.group(1)
        
        print(f"✅ LinkedIn data found")
        return data
        
    except Exception as e:
        print(f"⚠️  LinkedIn scraping failed: {e}")
        return {"url": profile_url, "scraped": False, "error": str(e)}

if __name__ == "__main__":
    # Scrape Matthew Galley's profiles
    print("\n🎯 Scraping Matthew Galley's Designer Profiles\n")
    
    dribbble_data = scrape_dribbble("mgalley")
    linkedin_data = scrape_linkedin("https://linkedin.com/in/matthew-j-galley")
    
    # Save results
    results = {
        "dribbble": dribbble_data,
        "linkedin": linkedin_data
    }
    
    output_file = "output/matthewgalley_designer_data.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Saved to: {output_file}")
    
    # Print summary
    print("\n📊 Summary:")
    print(f"   Dribbble: {'✅ Success' if dribbble_data.get('scraped') else '❌ Failed'}")
    print(f"   LinkedIn: {'✅ Success' if linkedin_data.get('scraped') else '❌ Failed'}")
    
    if dribbble_data.get('description'):
        print(f"\n🎨 Dribbble Bio:")
        print(f"   {dribbble_data['description'][:200]}...")
    
    if linkedin_data.get('title'):
        print(f"\n💼 LinkedIn Title:")
        print(f"   {linkedin_data['title']}")
