#!/usr/bin/env python3
"""
Screengrab Swap - Find files from folder screenshots

When you screenshot a folder location, this tool:
1. OCRs the screenshot to find the folder path
2. Asks what you're looking for
3. Searches that folder
4. Takes a screenshot of the found file
5. Saves it to Downloads, replacing the original screenshot

Usage:
    python3 screengrab_swap.py <screenshot_path>
    python3 screengrab_swap.py --latest  # Process latest screenshot
"""

import sys
import os
from pathlib import Path
import pytesseract
from PIL import Image
import subprocess
from datetime import datetime
import re

def extract_folder_path(screenshot_path):
    """Extract folder path from screenshot using OCR"""
    print(f"🔍 Reading screenshot: {screenshot_path}")
    
    try:
        img = Image.open(screenshot_path)
        text = pytesseract.image_to_string(img)
        
        print(f"\n📝 OCR Text:\n{text[:500]}\n")
        
        # Look for common folder path patterns
        patterns = [
            r'/Users/[^\s]+',
            r'~/[^\s]+',
            r'/Volumes/[^\s]+',
            r'Dropbox/[^\s]+',
        ]
        
        paths = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            paths.extend(matches)
        
        if paths:
            print(f"📁 Found {len(paths)} potential paths:")
            for i, path in enumerate(paths, 1):
                print(f"   {i}. {path}")
            return paths
        else:
            print("⚠️  No folder paths detected in screenshot")
            return []
            
    except Exception as e:
        print(f"❌ Error reading screenshot: {e}")
        return []

def search_folder(folder_path, query):
    """Search for files in folder matching query"""
    print(f"\n🔎 Searching in: {folder_path}")
    print(f"   Query: {query}")
    
    folder = Path(folder_path).expanduser()
    
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        return []
    
    # Search for files matching query
    matches = []
    query_lower = query.lower()
    
    for file in folder.rglob('*'):
        if file.is_file():
            if query_lower in file.name.lower():
                matches.append(file)
    
    return matches

def take_file_screenshot(file_path, output_path):
    """Take a screenshot of a file (Quick Look)"""
    print(f"\n📸 Taking screenshot of: {file_path.name}")
    
    try:
        # Open file in Quick Look
        subprocess.run(['qlmanage', '-p', str(file_path)], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      timeout=2)
        
        # Wait a moment for Quick Look to open
        import time
        time.sleep(1)
        
        # Take screenshot
        subprocess.run([
            'screencapture',
            '-i',  # Interactive selection
            str(output_path)
        ])
        
        # Close Quick Look
        subprocess.run(['killall', 'Quick Look UI Helper'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        
        if output_path.exists():
            print(f"✅ Screenshot saved to: {output_path}")
            return True
        else:
            print(f"❌ Screenshot not created")
            return False
            
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("SCREENGRAB SWAP - Find Files from Folder Screenshots")
    print("="*80 + "\n")
    
    # Get screenshot path
    if len(sys.argv) > 1:
        if sys.argv[1] == '--latest':
            # Find latest screenshot
            screenshots_dir = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/intake/screenshots"
            screenshots = sorted(screenshots_dir.glob('Screenshot*.png'), key=lambda p: p.stat().st_mtime, reverse=True)
            if screenshots:
                screenshot_path = screenshots[0]
            else:
                print("❌ No screenshots found")
                return
        else:
            screenshot_path = Path(sys.argv[1])
    else:
        print("Usage: python3 screengrab_swap.py <screenshot_path>")
        print("   or: python3 screengrab_swap.py --latest")
        return
    
    if not screenshot_path.exists():
        print(f"❌ Screenshot not found: {screenshot_path}")
        return
    
    # Extract folder paths
    paths = extract_folder_path(screenshot_path)
    
    if not paths:
        print("\n💡 Tip: Screenshot should show a Finder window with folder path visible")
        return
    
    # Let user choose path if multiple
    if len(paths) > 1:
        choice = input(f"\nWhich path? (1-{len(paths)}): ")
        try:
            folder_path = paths[int(choice) - 1]
        except:
            folder_path = paths[0]
    else:
        folder_path = paths[0]
    
    # Ask what to look for
    query = input("\n🔍 What are you looking for? ")
    
    if not query:
        print("❌ No search query provided")
        return
    
    # Search folder
    matches = search_folder(folder_path, query)
    
    if not matches:
        print(f"\n❌ No files found matching '{query}'")
        return
    
    print(f"\n✅ Found {len(matches)} files:")
    for i, match in enumerate(matches, 1):
        print(f"   {i}. {match.name} ({match.stat().st_size:,} bytes)")
    
    # Let user choose file
    if len(matches) > 1:
        choice = input(f"\nWhich file? (1-{len(matches)}): ")
        try:
            selected_file = matches[int(choice) - 1]
        except:
            selected_file = matches[0]
    else:
        selected_file = matches[0]
    
    # Take screenshot of file
    downloads = Path.home() / "Downloads"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = downloads / f"Screengrab_Swap_{selected_file.stem}_{timestamp}.png"
    
    success = take_file_screenshot(selected_file, output_path)
    
    if success:
        print(f"\n🎉 Screengrab Swap complete!")
        print(f"   Original: {screenshot_path}")
        print(f"   New: {output_path}")
        
        # Optionally delete original
        delete = input("\nDelete original screenshot? (y/n): ")
        if delete.lower() == 'y':
            screenshot_path.unlink()
            print(f"🗑️  Deleted: {screenshot_path}")

if __name__ == '__main__':
    main()
