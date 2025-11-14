#!/usr/bin/env python3
"""
Convert HTML email files to PNG images
"""

from pathlib import Path
from html2image import Html2Image
import os

# Paths
html_dir = Path.home() / 'Library' / 'Mobile Documents' / 'com~apple~CloudDocs' / 'Documents' / 'Joju' / 'Jh email campaign images'
output_dir = html_dir  # Same folder

print("="*60)
print("HTML → PNG CONVERTER")
print("="*60)

# Find all HTML files
html_files = list(html_dir.glob("*.html"))

if not html_files:
    print(f"❌ No HTML files found in {html_dir}")
    exit(1)

print(f"\n📄 Found {len(html_files)} HTML files")
print(f"📁 Output: {output_dir}\n")

# Initialize converter
hti = Html2Image(output_path=str(output_dir), size=(800, 1200))

# Convert each file
for i, html_file in enumerate(html_files, 1):
    try:
        print(f"[{i}/{len(html_files)}] {html_file.name[:60]}...")
        
        # Read HTML
        html_content = html_file.read_text(encoding='utf-8')
        
        # Output filename
        png_name = html_file.stem + '.png'
        
        # Convert
        hti.screenshot(
            html_str=html_content,
            save_as=png_name,
            size=(800, 2400)  # Tall for full email
        )
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")
        continue

print(f"\n✅ Done! {len(html_files)} images created")
print(f"📁 Location: {output_dir}")
