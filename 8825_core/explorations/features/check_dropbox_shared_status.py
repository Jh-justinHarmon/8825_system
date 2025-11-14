#!/usr/bin/env python3
"""
Check which folders are actually Dropbox shared folders
Uses Dropbox extended attributes to detect sharing status
"""

import os
import subprocess
import json

def is_shared_folder(path):
    """Check if a folder is a Dropbox shared folder"""
    try:
        # Method 1: Check extended attributes
        result = subprocess.run(
            ['xattr', '-p', 'com.dropbox.attributes', path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout:
            # Parse the attribute data
            # Shared folders have specific markers
            return True
            
    except Exception:
        pass
    
    # Method 2: Check for .dropbox file (older method)
    dropbox_file = os.path.join(path, '.dropbox')
    if os.path.exists(dropbox_file):
        try:
            with open(dropbox_file, 'r') as f:
                data = json.load(f)
                if 'shared_folder_id' in data or 'ns_id' in data:
                    return True
        except Exception:
            pass
    
    # Method 3: Check Dropbox cache/info
    # Dropbox stores sharing info in ~/Dropbox/.dropbox.cache
    
    return False

def scan_folders(root_path, max_depth=2):
    """Scan folders and identify shared vs personal"""
    folders = {
        'shared': [],
        'personal': [],
        'unknown': []
    }
    
    for item in os.listdir(root_path):
        if item.startswith('.'):
            continue
            
        item_path = os.path.join(root_path, item)
        
        if os.path.isdir(item_path):
            try:
                # Check if shared
                if is_shared_folder(item_path):
                    folders['shared'].append({
                        'name': item,
                        'path': item_path
                    })
                else:
                    # Check subfolders
                    has_shared_subfolders = False
                    try:
                        for subitem in os.listdir(item_path):
                            if subitem.startswith('.'):
                                continue
                            subitem_path = os.path.join(item_path, subitem)
                            if os.path.isdir(subitem_path) and is_shared_folder(subitem_path):
                                has_shared_subfolders = True
                                folders['shared'].append({
                                    'name': f"{item}/{subitem}",
                                    'path': subitem_path
                                })
                    except Exception:
                        pass
                    
                    if not has_shared_subfolders:
                        folders['personal'].append({
                            'name': item,
                            'path': item_path
                        })
            except Exception as e:
                folders['unknown'].append({
                    'name': item,
                    'path': item_path,
                    'error': str(e)
                })
    
    return folders

def main(root_path):
    print(f"\n🔍 Scanning: {root_path}")
    print("=" * 80)
    
    folders = scan_folders(root_path)
    
    print(f"\n🔗 SHARED FOLDERS (DO NOT SCAN):")
    if folders['shared']:
        for folder in sorted(folders['shared'], key=lambda x: x['name']):
            print(f"   ❌ {folder['name']}")
    else:
        print("   None detected via extended attributes")
    
    print(f"\n📁 PERSONAL FOLDERS (SAFE TO SCAN):")
    if folders['personal']:
        for folder in sorted(folders['personal'], key=lambda x: x['name']):
            print(f"   ✅ {folder['name']}")
    else:
        print("   None found")
    
    print(f"\n❓ UNKNOWN STATUS:")
    if folders['unknown']:
        for folder in sorted(folders['unknown'], key=lambda x: x['name']):
            print(f"   ⚠️  {folder['name']}")
    else:
        print("   None")
    
    print("\n" + "=" * 80)
    print("⚠️  NOTE: Extended attribute detection may not be 100% reliable.")
    print("   Recommend manually verifying shared status in Dropbox web interface.")
    print("=" * 80)
    
    # Save report
    with open('shared_folders_report.json', 'w') as f:
        json.dump(folders, f, indent=2)
    
    print("\n💾 Report saved to: shared_folders_report.json")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 check_dropbox_shared_status.py <folder_path>")
        sys.exit(1)
    
    main(sys.argv[1])
