#!/usr/bin/env python3
"""
Quick Duplicate File Checker
Scans a folder and calculates duplicate percentage
"""

import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    md5 = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5.update(chunk)
        return md5.hexdigest()
    except (IOError, OSError) as e:
        print(f"Error reading {filepath}: {e}")
        return None

def format_bytes(bytes_val):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def scan_folder(root_path):
    """Scan folder and find duplicates"""
    print(f"\n🔍 Scanning: {root_path}")
    print("=" * 80)
    
    file_hashes = defaultdict(list)
    total_files = 0
    total_size = 0
    skipped = 0
    
    # Walk directory
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip hidden folders
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            # Skip hidden files and system files
            if filename.startswith('.') or filename == 'Icon\r':
                skipped += 1
                continue
            
            filepath = os.path.join(dirpath, filename)
            
            try:
                file_size = os.path.getsize(filepath)
                total_files += 1
                total_size += file_size
                
                # Calculate hash
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    rel_path = os.path.relpath(filepath, root_path)
                    file_hashes[file_hash].append({
                        'path': rel_path,
                        'size': file_size,
                        'modified': os.path.getmtime(filepath)
                    })
                
                # Progress indicator
                if total_files % 100 == 0:
                    print(f"  Scanned {total_files} files...", end='\r')
                    
            except (IOError, OSError) as e:
                print(f"  Error accessing {filepath}: {e}")
                skipped += 1
    
    print(f"  Scanned {total_files} files... Done!   ")
    
    # Find duplicates
    duplicate_groups = {k: v for k, v in file_hashes.items() if len(v) > 1}
    
    # Calculate stats
    duplicate_files = sum(len(group) - 1 for group in duplicate_groups.values())
    duplicate_size = sum(
        sum(f['size'] for f in group[1:])
        for group in duplicate_groups.values()
    )
    
    return {
        'total_files': total_files,
        'total_size': total_size,
        'skipped': skipped,
        'duplicate_groups': duplicate_groups,
        'duplicate_files': duplicate_files,
        'duplicate_size': duplicate_size
    }

def print_report(results):
    """Print analysis report"""
    total_files = results['total_files']
    total_size = results['total_size']
    duplicate_files = results['duplicate_files']
    duplicate_size = results['duplicate_size']
    duplicate_groups = results['duplicate_groups']
    
    print("\n" + "=" * 80)
    print("📊 DUPLICATE ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\n📁 Total Files Scanned: {total_files:,}")
    print(f"💾 Total Storage Used: {format_bytes(total_size)}")
    if results['skipped'] > 0:
        print(f"⏭️  Files Skipped: {results['skipped']} (hidden/system files)")
    
    print(f"\n🔄 Duplicate Files Found: {duplicate_files:,}")
    print(f"💰 Duplicate Storage: {format_bytes(duplicate_size)}")
    
    if total_files > 0:
        dup_pct = (duplicate_files / total_files) * 100
        size_pct = (duplicate_size / total_size) * 100 if total_size > 0 else 0
        print(f"📈 Duplicate Percentage: {dup_pct:.1f}% of files, {size_pct:.1f}% of storage")
    
    print(f"\n📦 Duplicate Groups: {len(duplicate_groups):,}")
    
    # Hypothesis check
    print("\n" + "=" * 80)
    print("🧪 HYPOTHESIS CHECK")
    print("=" * 80)
    if total_files > 0:
        dup_pct = (duplicate_files / total_files) * 100
        if dup_pct >= 15:
            print(f"✅ VALIDATED - {dup_pct:.1f}% duplicates (expected 10-20%)")
            print("   Recommendation: Build file reduction tool")
        elif dup_pct >= 10:
            print(f"✅ VALIDATED - {dup_pct:.1f}% duplicates (expected 10-20%)")
            print("   Recommendation: Build file reduction tool")
        elif dup_pct >= 5:
            print(f"⚠️  PARTIALLY VALIDATED - {dup_pct:.1f}% duplicates (below expected)")
            print("   Recommendation: Calculate ROI before building")
        else:
            print(f"❌ INVALIDATED - {dup_pct:.1f}% duplicates (well below expected)")
            print("   Recommendation: Not worth building tool")
    
    # Top duplicate groups
    if duplicate_groups:
        print("\n" + "=" * 80)
        print("🔝 TOP 10 DUPLICATE GROUPS (by wasted space)")
        print("=" * 80)
        
        # Sort by wasted space
        sorted_groups = sorted(
            duplicate_groups.items(),
            key=lambda x: sum(f['size'] for f in x[1][1:]),
            reverse=True
        )[:10]
        
        for i, (hash_key, files) in enumerate(sorted_groups, 1):
            wasted = sum(f['size'] for f in files[1:])
            print(f"\n{i}. {len(files)} copies, {format_bytes(wasted)} wasted")
            print(f"   Hash: {hash_key[:16]}...")
            for j, file in enumerate(files[:5]):  # Show first 5
                marker = "✓ KEEP" if j == 0 else "□ archive"
                print(f"   {marker} {file['path']}")
            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more copies")
    
    print("\n" + "=" * 80)

def save_report(results, output_path):
    """Save detailed report to JSON"""
    # Convert for JSON serialization
    report = {
        'scan_date': datetime.now().isoformat(),
        'summary': {
            'total_files': results['total_files'],
            'total_size_bytes': results['total_size'],
            'total_size_readable': format_bytes(results['total_size']),
            'duplicate_files': results['duplicate_files'],
            'duplicate_size_bytes': results['duplicate_size'],
            'duplicate_size_readable': format_bytes(results['duplicate_size']),
            'duplicate_percentage': (results['duplicate_files'] / results['total_files'] * 100) if results['total_files'] > 0 else 0,
            'duplicate_groups': len(results['duplicate_groups'])
        },
        'duplicate_groups': [
            {
                'hash': hash_key,
                'file_count': len(files),
                'wasted_bytes': sum(f['size'] for f in files[1:]),
                'files': files
            }
            for hash_key, files in results['duplicate_groups'].items()
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {output_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 quick_duplicate_check.py <folder_path>")
        print("\nExample:")
        print('  python3 quick_duplicate_check.py "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/TGI Fridays"')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not os.path.isdir(folder_path):
        print(f"❌ Error: Not a directory: {folder_path}")
        sys.exit(1)
    
    # Scan folder
    results = scan_folder(folder_path)
    
    # Print report
    print_report(results)
    
    # Save detailed report
    output_file = "duplicate_analysis_report.json"
    save_report(results, output_file)
    
    print("\n✅ Analysis complete!")
