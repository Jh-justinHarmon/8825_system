#!/usr/bin/env python3
"""
Compare Dropbox fonts against macOS system font libraries
Find duplicates that can be safely removed from Dropbox
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict

def calculate_hash(filepath):
    """Calculate SHA256 hash of file"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def scan_fonts(folder_path):
    """Scan folder for font files"""
    font_exts = {'.ttf', '.otf', '.ttc', '.dfont', '.suit'}
    fonts = {}
    
    for dirpath, dirnames, filenames in os.walk(folder_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in font_exts:
                filepath = os.path.join(dirpath, filename)
                file_hash = calculate_hash(filepath)
                
                if file_hash:
                    fonts[filepath] = {
                        'name': filename,
                        'hash': file_hash,
                        'size': os.path.getsize(filepath),
                        'path': filepath
                    }
    
    return fonts

def format_bytes(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def main(dropbox_fonts_path):
    print("\n🔍 Comparing Dropbox fonts to system libraries...")
    print("=" * 80)
    
    # System font locations on macOS
    system_font_paths = [
        '/System/Library/Fonts',
        '/Library/Fonts',
        os.path.expanduser('~/Library/Fonts')
    ]
    
    print("\n📁 Scanning system font libraries...")
    system_fonts = {}
    for path in system_font_paths:
        if os.path.exists(path):
            print(f"   Scanning: {path}")
            fonts = scan_fonts(path)
            system_fonts.update(fonts)
    
    print(f"   Found {len(system_fonts):,} system fonts")
    
    print("\n📁 Scanning Dropbox fonts...")
    dropbox_fonts = scan_fonts(dropbox_fonts_path)
    print(f"   Found {len(dropbox_fonts):,} Dropbox fonts")
    
    # Build hash index for system fonts
    system_hashes = {info['hash']: path for path, info in system_fonts.items()}
    
    # Find duplicates
    print("\n🔍 Finding duplicates...")
    duplicates = []
    unique_dropbox = []
    
    for db_path, db_info in dropbox_fonts.items():
        if db_info['hash'] in system_hashes:
            # Duplicate found in system
            duplicates.append({
                'dropbox': db_path,
                'dropbox_name': db_info['name'],
                'system': system_hashes[db_info['hash']],
                'size': db_info['size']
            })
        else:
            unique_dropbox.append(db_info)
    
    # Report
    print("\n" + "=" * 80)
    print("📊 COMPARISON REPORT")
    print("=" * 80)
    
    print(f"\n📈 Summary:")
    print(f"   System fonts: {len(system_fonts):,}")
    print(f"   Dropbox fonts: {len(dropbox_fonts):,}")
    print(f"   Duplicates (in both): {len(duplicates):,}")
    print(f"   Unique to Dropbox: {len(unique_dropbox):,}")
    
    if duplicates:
        total_duplicate_size = sum(d['size'] for d in duplicates)
        print(f"\n💰 Space savings if duplicates removed: {format_bytes(total_duplicate_size)}")
        
        print("\n" + "=" * 80)
        print("🗑️  FONTS SAFE TO DELETE FROM DROPBOX")
        print("=" * 80)
        print("\nThese fonts are already installed in your system:")
        
        # Sort by size (largest first)
        for dup in sorted(duplicates, key=lambda x: x['size'], reverse=True):
            print(f"\n   {dup['dropbox_name']} ({format_bytes(dup['size'])})")
            print(f"      Dropbox: {dup['dropbox']}")
            print(f"      System:  {dup['system']}")
    else:
        print("\n✅ No duplicates found - all Dropbox fonts are unique!")
    
    if unique_dropbox:
        print("\n" + "=" * 80)
        print("📦 UNIQUE FONTS IN DROPBOX")
        print("=" * 80)
        print(f"\nThese {len(unique_dropbox)} fonts are NOT in your system library:")
        
        # Show top 20 by size
        for font in sorted(unique_dropbox, key=lambda x: x['size'], reverse=True)[:20]:
            print(f"   {font['name']} ({format_bytes(font['size'])})")
        
        if len(unique_dropbox) > 20:
            print(f"   ... and {len(unique_dropbox) - 20} more")
    
    # Generate deletion script
    if duplicates:
        print("\n" + "=" * 80)
        print("🔧 CLEANUP SCRIPT")
        print("=" * 80)
        
        script_path = 'delete_duplicate_fonts.sh'
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Delete duplicate fonts from Dropbox\n")
            f.write("# These fonts are already installed in system libraries\n\n")
            f.write("set -e\n\n")
            
            for dup in duplicates:
                # Escape path for shell
                safe_path = dup['dropbox'].replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)')
                f.write(f'echo "Deleting: {dup["dropbox_name"]}"\n')
                f.write(f'rm "{dup["dropbox"]}"\n\n')
            
            f.write(f'echo "Deleted {len(duplicates)} duplicate fonts"\n')
            f.write(f'echo "Space saved: {format_bytes(total_duplicate_size)}"\n')
        
        os.chmod(script_path, 0o755)
        print(f"\n💾 Cleanup script saved to: {script_path}")
        print(f"   Review and run with: ./{script_path}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 compare_fonts_to_system.py <dropbox_fonts_folder>")
        print("\nExample:")
        print('  python3 compare_fonts_to_system.py "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/meFONT"')
        sys.exit(1)
    
    main(sys.argv[1])
