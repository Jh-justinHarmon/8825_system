#!/usr/bin/env python3
"""
URL Shortener Tool
Quickly shorten URLs using is.gd API (no account needed)
"""

import sys
import requests
import subprocess

def shorten_url(long_url, custom_name=None):
    """
    Shorten a URL using is.gd API
    
    Args:
        long_url: The URL to shorten
        custom_name: Optional custom short name
    
    Returns:
        Shortened URL or error message
    """
    api_url = "https://is.gd/create.php"
    
    params = {
        'format': 'simple',
        'url': long_url
    }
    
    if custom_name:
        params['shorturl'] = custom_name
    
    try:
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            short_url = response.text.strip()
            
            # Check if it's an error message
            if short_url.startswith('Error'):
                return f"❌ {short_url}"
            
            return short_url
        else:
            return f"❌ Error: HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"

def main():
    print("🔗 URL Shortener Tool")
    print("=" * 50)
    
    # Get URL from command line or prompt
    if len(sys.argv) > 1:
        long_url = sys.argv[1]
    else:
        long_url = input("\n📎 Enter URL to shorten: ").strip()
    
    if not long_url:
        print("❌ No URL provided")
        return
    
    # Optional custom name
    custom = input("✏️  Custom name (optional, press Enter to skip): ").strip()
    custom_name = custom if custom else None
    
    print("\n⏳ Shortening URL...")
    
    # Shorten the URL
    result = shorten_url(long_url, custom_name)
    
    print(f"\n✅ Result: {result}")
    
    # Copy to clipboard if successful (macOS)
    if not result.startswith('❌'):
        try:
            subprocess.run(['pbcopy'], input=result.encode(), check=True)
            print("📋 Copied to clipboard!")
        except Exception as e:
            print(f"⚠️  Could not copy to clipboard: {e}")
    
    print()

if __name__ == "__main__":
    main()
