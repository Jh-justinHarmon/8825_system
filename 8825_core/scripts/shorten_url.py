#!/usr/bin/env python3
"""
URL Shortener Tool - 8825 Core Utility

Quickly shorten URLs using is.gd and v.gd APIs (no account needed)

Usage:
    python3 shorten_url.py [URL] [custom_name]
    
Examples:
    # Interactive mode
    python3 shorten_url.py
    
    # With URL
    python3 shorten_url.py "https://example.com/very/long/url"
    
    # With custom name
    python3 shorten_url.py "https://example.com" "my-custom-name"

Features:
    - No account required (uses is.gd/v.gd free APIs)
    - Custom short names (if available)
    - Automatic clipboard copy (macOS)
    - Fallback to v.gd if is.gd fails
    - Support for underscores in custom names

Services Used:
    - is.gd (primary)
    - v.gd (fallback, supports underscores)

Location: 8825_core/scripts/shorten_url.py
Last Updated: November 10, 2025
"""

import sys
import requests
import subprocess

def shorten_url(long_url, custom_name=None):
    """
    Shorten a URL using is.gd or v.gd API
    
    Args:
        long_url: The URL to shorten
        custom_name: Optional custom short name (use underscores, NOT hyphens!)
    
    Returns:
        Shortened URL or error message
        
    IMPORTANT:
        - Hyphens (-) in custom names WILL FAIL on free services
        - Always use underscores (_) instead: joju_screener not joju-screener
        
    Note:
        - is.gd is tried first
        - v.gd is used as fallback (better support for custom names with underscores)
        - Custom names may not be available on free services
    """
    # Try is.gd first
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
                # Try v.gd as fallback (better for custom names)
                if custom_name:
                    print("⚠️  is.gd failed, trying v.gd...")
                    vgd_url = "https://v.gd/create.php"
                    vgd_response = requests.get(vgd_url, params=params, timeout=10)
                    if vgd_response.status_code == 200:
                        vgd_result = vgd_response.text.strip()
                        if not vgd_result.startswith('Error'):
                            return vgd_result
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
    custom = input("✏️  Custom name (use underscores, NOT hyphens - press Enter to skip): ").strip()
    
    # Warn if hyphen detected
    if custom and '-' in custom:
        print("⚠️  WARNING: Hyphens (-) will likely FAIL on free services!")
        print("💡 Suggestion: Replace hyphens with underscores (_)")
        suggested = custom.replace('-', '_')
        print(f"   Try: {suggested}")
        confirm = input("   Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Cancelled")
            return
    
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
