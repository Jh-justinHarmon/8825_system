#!/usr/bin/env python3
"""
Check which folders are Dropbox shared folders
"""

import os
import subprocess
import json

def check_shared_status(path):
    """Check if a folder is shared via Dropbox attributes"""
    try:
        # Get extended attributes
        result = subprocess.run(
            ['xattr', '-l', path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Check for Dropbox sharing attributes
        if 'com.dropbox.attributes' in result.stdout:
            # Try to parse Dropbox attributes
            return 'shared'
        
        # Alternative: check if folder name contains sharing indicators
        # Dropbox shared folders often have specific naming patterns
        
        return 'unknown'
    except Exception as e:
        return 'error'

def list_folders_with_status(root_path):
    """List all folders in root with their sharing status"""
    folders = []
    
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        
        if os.path.isdir(item_path) and not item.startswith('.'):
            # Get folder info
            try:
                stat = os.stat(item_path)
                item_count = len(os.listdir(item_path)) if os.path.isdir(item_path) else 0
                
                # Check sharing status
                shared_status = check_shared_status(item_path)
                
                folders.append({
                    'name': item,
                    'path': item_path,
                    'items': item_count,
                    'shared': shared_status,
                    'modified': stat.st_mtime
                })
            except Exception as e:
                folders.append({
                    'name': item,
                    'path': item_path,
                    'error': str(e)
                })
    
    return folders

def analyze_root_files(root_path):
    """Analyze files in root folder for cleanup candidates"""
    files = []
    
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        
        if os.path.isfile(item_path) and not item.startswith('.'):
            try:
                stat = os.stat(item_path)
                
                files.append({
                    'name': item,
                    'path': item_path,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'ext': os.path.splitext(item)[1].lower()
                })
            except Exception as e:
                pass
    
    return files

def format_bytes(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def main(root_path):
    print(f"\n📁 Analyzing: {root_path}")
    print("=" * 80)
    
    # List folders
    print("\n📂 FOLDERS:")
    folders = list_folders_with_status(root_path)
    
    shared_folders = [f for f in folders if f.get('shared') == 'shared']
    unknown_folders = [f for f in folders if f.get('shared') == 'unknown']
    
    print(f"\n🔗 Potentially Shared Folders: {len(shared_folders)}")
    for folder in shared_folders:
        print(f"   - {folder['name']} ({folder['items']} items)")
    
    print(f"\n📁 Other Folders: {len(unknown_folders)}")
    for folder in sorted(unknown_folders, key=lambda x: x['items'], reverse=True):
        print(f"   - {folder['name']} ({folder['items']} items)")
    
    # Analyze files
    print("\n" + "=" * 80)
    print("📄 FILES IN ROOT FOLDER:")
    files = analyze_root_files(root_path)
    
    print(f"\nTotal files: {len(files)}")
    print(f"Total size: {format_bytes(sum(f['size'] for f in files))}")
    
    # Group by extension
    by_ext = {}
    for f in files:
        ext = f['ext'] or 'no extension'
        if ext not in by_ext:
            by_ext[ext] = []
        by_ext[ext].append(f)
    
    print(f"\n📊 By file type:")
    for ext, ext_files in sorted(by_ext.items(), key=lambda x: sum(f['size'] for f in x[1]), reverse=True):
        total_size = sum(f['size'] for f in ext_files)
        print(f"   {ext}: {len(ext_files)} files, {format_bytes(total_size)}")
    
    # Find duplicates
    print("\n" + "=" * 80)
    print("🔍 POTENTIAL DUPLICATES:")
    
    # Check for similar names
    base_names = {}
    for f in files:
        base = os.path.splitext(f['name'])[0]
        if base not in base_names:
            base_names[base] = []
        base_names[base].append(f)
    
    duplicates = {k: v for k, v in base_names.items() if len(v) > 1}
    
    if duplicates:
        for base, dups in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n   {base}:")
            for f in sorted(dups, key=lambda x: x['modified'], reverse=True):
                from datetime import datetime
                date_str = datetime.fromtimestamp(f['modified']).strftime('%Y-%m-%d')
                print(f"      - {f['name']} ({format_bytes(f['size'])}, {date_str})")
    else:
        print("   No obvious duplicates found")
    
    # Old files
    import time
    from datetime import datetime, timedelta
    
    old_threshold = time.time() - (365 * 86400)  # 1 year
    old_files = [f for f in files if f['modified'] < old_threshold]
    
    print("\n" + "=" * 80)
    print(f"📅 OLD FILES (> 1 year): {len(old_files)}")
    
    if old_files:
        print("\nSorted by size (largest first):")
        for f in sorted(old_files, key=lambda x: x['size'], reverse=True)[:10]:
            date_str = datetime.fromtimestamp(f['modified']).strftime('%Y-%m-%d')
            print(f"   - {f['name']}")
            print(f"     {format_bytes(f['size'])}, last modified: {date_str}")
    
    # Save report
    report = {
        'folders': folders,
        'files': files,
        'duplicates': {k: [f['name'] for f in v] for k, v in duplicates.items()},
        'old_files': [f['name'] for f in old_files]
    }
    
    with open('root_folder_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 80)
    print("💾 Report saved to: root_folder_analysis.json")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 check_shared_folders.py <folder_path>")
        sys.exit(1)
    
    main(sys.argv[1])
