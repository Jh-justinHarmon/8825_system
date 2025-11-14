#!/usr/bin/env python3
"""
Enhanced Routing Rules for Inbox Hub

File Type Routing:
- Bills → Calendar, Drive, Ledger
- Post-its → FigJam
- TXT/JSON/TXF → Ingest & file
- Word docs → Inquire (ingest or just file)
- PDFs → TBD
- Screenshots of folders → Screengrab Swap
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import pytesseract
from PIL import Image

# Routing destinations
ROUTES = {
    'bills': {
        'destinations': ['calendar', 'drive', 'ledger'],
        'keywords': ['invoice', 'bill', 'payment', 'due', 'amount', '$', 'total', 'statement'],
        'extensions': ['.pdf', '.png', '.jpg', '.jpeg']
    },
    'postits': {
        'destinations': ['figjam'],
        'keywords': ['note', 'reminder', 'todo', 'task', 'sticky'],
        'extensions': ['.png', '.jpg', '.jpeg'],
        'color_detection': True  # Yellow/bright colors
    },
    'ingest_files': {
        'destinations': ['ingest'],
        'extensions': ['.txt', '.json', '.txf', '.md'],
        'auto_process': True
    },
    'word_docs': {
        'destinations': ['inquire'],  # Ask user
        'extensions': ['.docx', '.doc'],
        'prompt': 'Ingest and file, or just file?'
    },
    'pdfs': {
        'destinations': ['tbd'],
        'extensions': ['.pdf'],
        'needs_classification': True
    },
    'folder_screenshots': {
        'destinations': ['screengrab_swap'],
        'detection': 'finder_window',
        'action': 'prompt_search'
    }
}

def detect_file_type(file_path):
    """Detect what type of file this is for routing"""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    # Check extension-based routes first
    for route_name, route_config in ROUTES.items():
        if 'extensions' in route_config:
            if ext in route_config['extensions']:
                return route_name, route_config
    
    # For images, do content detection
    if ext in ['.png', '.jpg', '.jpeg']:
        return detect_image_type(path)
    
    return 'unknown', {}

def detect_image_type(image_path):
    """Detect if image is a bill, post-it, or folder screenshot"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img).lower()
        
        # Check for bill keywords
        bill_keywords = ROUTES['bills']['keywords']
        if any(kw in text for kw in bill_keywords):
            return 'bills', ROUTES['bills']
        
        # Check for folder/Finder window
        if 'finder' in text or '/users/' in text or 'dropbox' in text:
            # Check if it's showing a folder structure
            if text.count('/') > 3:  # Multiple path separators
                return 'folder_screenshots', ROUTES['folder_screenshots']
        
        # Check for post-it colors (yellow/bright)
        # This is a simple heuristic - could be improved
        colors = img.getcolors(maxcolors=10)
        if colors:
            # Check for yellow-ish colors
            for count, color in colors:
                if isinstance(color, tuple) and len(color) >= 3:
                    r, g, b = color[:3]
                    # Yellow is high R and G, low B
                    if r > 200 and g > 200 and b < 150:
                        return 'postits', ROUTES['postits']
        
        return 'screenshot', {}
        
    except Exception as e:
        print(f"⚠️  Error detecting image type: {e}")
        return 'unknown', {}

def route_file(file_path, dry_run=True):
    """Route file to appropriate destination(s)"""
    file_type, config = detect_file_type(file_path)
    
    print(f"\n📄 File: {Path(file_path).name}")
    print(f"   Type: {file_type}")
    
    if not config:
        print(f"   ⚠️  No routing rule")
        return
    
    destinations = config.get('destinations', [])
    print(f"   → Destinations: {', '.join(destinations)}")
    
    if dry_run:
        print(f"   [DRY RUN - not actually routing]")
        return
    
    # Execute routing
    for dest in destinations:
        if dest == 'inquire':
            # Ask user
            prompt = config.get('prompt', 'What should we do with this file?')
            response = input(f"\n❓ {prompt} ")
            print(f"   User chose: {response}")
        
        elif dest == 'screengrab_swap':
            # Launch screengrab swap
            print(f"   🔄 Launching Screengrab Swap...")
            os.system(f"python3 screengrab_swap.py '{file_path}'")
        
        elif dest == 'ingest':
            # Auto-ingest
            print(f"   📥 Ingesting file...")
            # Call ingest pipeline
        
        else:
            print(f"   📤 Routing to: {dest}")

def process_inbox(inbox_path, dry_run=True):
    """Process all files in inbox"""
    inbox = Path(inbox_path)
    
    if not inbox.exists():
        print(f"❌ Inbox not found: {inbox}")
        return
    
    files = list(inbox.glob('*'))
    print(f"\n📋 Processing {len(files)} files in inbox...\n")
    
    for file in files:
        if file.is_file():
            route_file(file, dry_run=dry_run)

def main():
    print("\n" + "="*80)
    print("ENHANCED ROUTING RULES - Inbox Hub")
    print("="*80)
    
    # Default inbox locations
    screenshots = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/intake/screenshots"
    documents = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/intake/documents"
    uploads = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/intake/uploads"
    
    # Process each inbox
    for inbox in [screenshots, documents, uploads]:
        if inbox.exists():
            print(f"\n{'='*80}")
            print(f"Inbox: {inbox.name}")
            print(f"{'='*80}")
            process_inbox(inbox, dry_run=True)
    
    print(f"\n{'='*80}")
    print("Routing Rules Summary:")
    print(f"{'='*80}\n")
    
    for route_name, config in ROUTES.items():
        print(f"📌 {route_name.upper()}")
        if 'destinations' in config:
            print(f"   → {', '.join(config['destinations'])}")
        if 'extensions' in config:
            print(f"   Extensions: {', '.join(config['extensions'])}")
        if 'keywords' in config:
            print(f"   Keywords: {', '.join(config['keywords'][:5])}...")
        print()

if __name__ == '__main__':
    main()
