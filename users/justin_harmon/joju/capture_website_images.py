#!/usr/bin/env python3
"""
Capture screenshots from Justin's portfolio websites
"""

from playwright.sync_api import sync_playwright
from PIL import Image
from pathlib import Path
import json
import time

class WebsiteCapture:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Websites to capture
        self.sites = {
            'portfolio_main': {
                'url': 'https://favorite-day-425385.framer.app/',
                'captures': [
                    {'name': 'hero', 'scroll': 0},
                    {'name': 'value-props', 'scroll': 800},
                    {'name': 'projects', 'scroll': 1600}
                ]
            },
            'justin_harmon_com': {
                'url': 'https://www.justin-harmon.com/',
                'captures': [
                    {'name': 'hero', 'scroll': 0},
                    {'name': 'work', 'scroll': 800},
                    {'name': 'about', 'scroll': 1600}
                ]
            },
            'art_portfolio': {
                'url': 'https://www.justin-harmon.art/',
                'captures': [
                    {'name': 'hero', 'scroll': 0},
                    {'name': 'gallery', 'scroll': 800}
                ]
            }
        }
    
    def capture_screenshot(self, url: str, output_name: str, 
                          scroll_y: int = 0, viewport: dict = None) -> dict:
        """
        Capture screenshot from URL
        
        Args:
            url: URL to capture
            output_name: Output filename (without extension)
            scroll_y: Vertical scroll position
            viewport: Dict with 'width' and 'height'
        
        Returns:
            Dict with attachment info or None if failed
        """
        if viewport is None:
            viewport = {'width': 1920, 'height': 1080}
        
        output_path = self.output_dir / f"{output_name}.png"
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )
                page = browser.new_page(
                    viewport=viewport,
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                print(f"  📸 Loading {url}...")
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                # Wait for content to load
                time.sleep(5)
                
                # Scroll if needed
                if scroll_y > 0:
                    page.evaluate(f"window.scrollTo(0, {scroll_y})")
                    time.sleep(1)
                
                # Take screenshot
                page.screenshot(path=str(output_path), full_page=False)
                browser.close()
            
            # Get dimensions
            with Image.open(output_path) as img:
                width, height = img.size
            
            print(f"  ✅ Captured: {output_name}.png ({width}x{height})")
            
            return {
                "type": "image",
                "width": width,
                "height": height,
                "url": f"/content/media/{output_name}.png"
            }
        
        except Exception as e:
            print(f"  ❌ Failed to capture {url}: {e}")
            return None
    
    def capture_all(self) -> dict:
        """Capture all website screenshots"""
        print("\n🌐 Capturing website screenshots...\n")
        
        results = {}
        
        for site_id, site_info in self.sites.items():
            print(f"\n📦 Capturing: {site_id}")
            print(f"   URL: {site_info['url']}")
            
            site_images = []
            
            for capture in site_info['captures']:
                output_name = f"{site_id}-{capture['name']}"
                
                attachment = self.capture_screenshot(
                    site_info['url'],
                    output_name,
                    scroll_y=capture.get('scroll', 0)
                )
                
                if attachment:
                    site_images.append(attachment)
            
            if site_images:
                results[site_id] = site_images
                print(f"  ✅ Total captures for {site_id}: {len(site_images)}")
        
        print(f"\n✅ Website capture complete! Total sites: {len(results)}")
        return results
    
    def save_mapping(self, results: dict, output_file: str = "website_images.json"):
        """Save website image mapping"""
        output_path = self.output_dir.parent / output_file
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Saved website image mapping to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Capture website screenshots')
    parser.add_argument('--output', default='content/media', help='Output directory')
    
    args = parser.parse_args()
    
    capturer = WebsiteCapture(args.output)
    results = capturer.capture_all()
    capturer.save_mapping(results)
    
    print("\n🎉 Done! Website images captured.")
    print(f"📂 Check: {args.output}")


if __name__ == '__main__':
    main()
