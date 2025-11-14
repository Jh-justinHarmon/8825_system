#!/usr/bin/env python3
"""
Email (.eml) to Screenshot Converter
Extracts HTML from .eml files and generates PNG screenshots
"""

import email
from email import policy
from pathlib import Path
import sys
import time
from playwright.sync_api import sync_playwright


def extract_html_from_eml(eml_path: Path) -> str:
    """Extract HTML content from .eml file"""
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    # Find HTML part
    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_content()
            break
    
    if not html_content:
        raise ValueError("No HTML content found in email")
    
    return html_content


def html_to_screenshot(html_content: str, output_path: Path, width: int = 800):
    """Convert HTML to PNG screenshot using Playwright"""
    
    with sync_playwright() as p:
        # Launch browser with longer timeout
        browser = p.chromium.launch(
            headless=True,
            timeout=60000  # 60 second timeout
        )
        
        try:
            # Create page with specified width
            page = browser.new_page(viewport={'width': width, 'height': 1200})
            
            # Set HTML content with longer timeout
            page.set_content(html_content, wait_until='domcontentloaded', timeout=60000)
            
            # Wait for network to be idle (images loaded)
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
            except:
                # If networkidle times out, continue anyway
                pass
            
            # Take full page screenshot
            page.screenshot(path=str(output_path), full_page=True, timeout=30000)
            
        finally:
            try:
                browser.close()
            except:
                pass  # Ignore close errors


def eml_to_screenshot(eml_path: Path, output_path: Path = None, width: int = 800) -> Path:
    """
    Convert .eml file to PNG screenshot
    
    Args:
        eml_path: Path to .eml file
        output_path: Output PNG path (optional, auto-generated if not provided)
        width: Screenshot width in pixels (default 800)
    
    Returns:
        Path to generated screenshot
    """
    
    if not eml_path.exists():
        raise FileNotFoundError(f"Email file not found: {eml_path}")
    
    # Auto-generate output path if not provided
    if output_path is None:
        output_path = eml_path.parent / f"{eml_path.stem}_screenshot.png"
    
    print(f"📧 Processing: {eml_path.name}")
    
    # Extract HTML
    print("  → Extracting HTML...")
    html_content = extract_html_from_eml(eml_path)
    
    # Generate screenshot
    print(f"  → Generating screenshot ({width}px wide)...")
    html_to_screenshot(html_content, output_path, width)
    
    print(f"✅ Screenshot saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 eml_to_screenshot.py <email.eml> [output.png] [width]")
        print("\nExample:")
        print("  python3 eml_to_screenshot.py campaign.eml")
        print("  python3 eml_to_screenshot.py campaign.eml output.png 1000")
        sys.exit(1)
    
    eml_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 800
    
    try:
        result = eml_to_screenshot(eml_path, output_path, width)
        print(f"\n✅ Done! Screenshot: {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
