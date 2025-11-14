#!/usr/bin/env python3
"""
Enhanced Duplicate File Checker
Detects:
1. Exact duplicates (same content hash)
2. Version files (v1, v2, final, etc.)
3. Sequential copies (file (1), file (2), etc.)
4. Date-stamped versions
"""

import os
import re
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
        return None

def format_bytes(bytes_val):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def normalize_filename(filename):
    """
    Remove version indicators to find base filename
    Examples:
    - logo_v1.ai → logo.ai
    - report_final.docx → report.docx
    - file (1).pdf → file.pdf
    - doc_2024-11-09.xlsx → doc.xlsx
    """
    name, ext = os.path.splitext(filename)
    
    # Remove common version patterns
    patterns = [
        r'_v\d+$',           # _v1, _v2, _v10
        r'_V\d+$',           # _V1, _V2
        r' v\d+$',           # (space)v1, v2
        r'_final$',          # _final
        r'_FINAL$',          # _FINAL
        r'_draft$',          # _draft
        r'_DRAFT$',          # _DRAFT
        r'_copy$',           # _copy
        r'_Copy$',           # _Copy
        r' \(\d+\)$',        # (1), (2), (3)
        r'_\d{4}-\d{2}-\d{2}$',  # _2024-11-09
        r' \d{4}-\d{2}-\d{2}$',  # (space)2024-11-09
        r'_old$',            # _old
        r'_OLD$',            # _OLD
        r'_backup$',         # _backup
        r'_BACKUP$',         # _BACKUP
        r'_new$',            # _new
        r'_NEW$',            # _NEW
        r'_latest$',         # _latest
        r'_LATEST$',         # _LATEST
        r' - Copy$',         # (space)- Copy
        r'_\d+$',            # _1, _2, _3
    ]
    
    normalized = name
    for pattern in patterns:
        normalized = re.sub(pattern, '', normalized)
    
    return normalized + ext

def extract_version_info(filename):
    """Extract version number/indicator from filename"""
    name, ext = os.path.splitext(filename)
    
    # Try to extract version number
    version_patterns = [
        (r'_v(\d+)$', 'v'),
        (r'_V(\d+)$', 'V'),
        (r' v(\d+)$', 'v'),
        (r' \((\d+)\)$', 'copy'),
        (r'_(\d{4}-\d{2}-\d{2})$', 'date'),
    ]
    
    for pattern, vtype in version_patterns:
        match = re.search(pattern, name)
        if match:
            return (vtype, match.group(1))
    
    # Check for keyword versions
    if name.endswith('_final') or name.endswith('_FINAL'):
        return ('final', 999)
    if name.endswith('_draft') or name.endswith('_DRAFT'):
        return ('draft', 0)
    if name.endswith('_latest') or name.endswith('_LATEST'):
        return ('latest', 1000)
    
    return (None, None)

def scan_folder(root_path):
    """Scan folder and find duplicates + versions"""
    print(f"\n🔍 Scanning: {root_path}")
    print("=" * 80)
    
    # Track exact duplicates
    file_hashes = defaultdict(list)
    
    # Track version groups
    version_groups = defaultdict(list)
    
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
                file_mtime = os.path.getmtime(filepath)
                total_files += 1
                total_size += file_size
                
                # Calculate hash for exact duplicates
                file_hash = calculate_file_hash(filepath)
                
                rel_path = os.path.relpath(filepath, root_path)
                rel_dir = os.path.dirname(rel_path)
                
                file_info = {
                    'path': rel_path,
                    'filename': filename,
                    'size': file_size,
                    'modified': file_mtime,
                    'hash': file_hash
                }
                
                # Track for exact duplicates
                if file_hash:
                    file_hashes[file_hash].append(file_info)
                
                # Track for version detection
                normalized = normalize_filename(filename)
                version_info = extract_version_info(filename)
                
                # Group by directory + normalized name
                version_key = f"{rel_dir}/{normalized}"
                version_groups[version_key].append({
                    **file_info,
                    'normalized': normalized,
                    'version_type': version_info[0],
                    'version_value': version_info[1]
                })
                
                # Progress indicator
                if total_files % 100 == 0:
                    print(f"  Scanned {total_files} files...", end='\r')
                    
            except (IOError, OSError) as e:
                skipped += 1
    
    print(f"  Scanned {total_files} files... Done!   ")
    
    # Find exact duplicates
    exact_duplicates = {k: v for k, v in file_hashes.items() if len(v) > 1}
    
    # Find version groups (2+ files with same normalized name in same folder)
    version_duplicates = {k: v for k, v in version_groups.items() if len(v) > 1}
    
    # Calculate stats
    exact_dup_files = sum(len(group) - 1 for group in exact_duplicates.values())
    exact_dup_size = sum(
        sum(f['size'] for f in group[1:])
        for group in exact_duplicates.values()
    )
    
    version_dup_files = sum(len(group) - 1 for group in version_duplicates.values())
    version_dup_size = sum(
        sum(f['size'] for f in sorted(group, key=lambda x: x['modified'], reverse=True)[1:])
        for group in version_duplicates.values()
    )
    
    return {
        'total_files': total_files,
        'total_size': total_size,
        'skipped': skipped,
        'exact_duplicates': exact_duplicates,
        'exact_dup_files': exact_dup_files,
        'exact_dup_size': exact_dup_size,
        'version_duplicates': version_duplicates,
        'version_dup_files': version_dup_files,
        'version_dup_size': version_dup_size
    }

def print_report(results):
    """Print analysis report"""
    total_files = results['total_files']
    total_size = results['total_size']
    
    print("\n" + "=" * 80)
    print("📊 ENHANCED DUPLICATE ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\n📁 Total Files Scanned: {total_files:,}")
    print(f"💾 Total Storage Used: {format_bytes(total_size)}")
    if results['skipped'] > 0:
        print(f"⏭️  Files Skipped: {results['skipped']} (hidden/system files)")
    
    # Exact duplicates
    print("\n" + "─" * 80)
    print("🔄 EXACT DUPLICATES (Same content hash)")
    print("─" * 80)
    print(f"Files: {results['exact_dup_files']:,}")
    print(f"Storage: {format_bytes(results['exact_dup_size'])}")
    print(f"Percentage: {(results['exact_dup_files'] / total_files * 100):.1f}% of files, {(results['exact_dup_size'] / total_size * 100):.1f}% of storage")
    print(f"Groups: {len(results['exact_duplicates']):,}")
    
    # Version duplicates
    print("\n" + "─" * 80)
    print("📝 VERSION DUPLICATES (Multiple versions of same file)")
    print("─" * 80)
    print(f"Files: {results['version_dup_files']:,}")
    print(f"Storage: {format_bytes(results['version_dup_size'])}")
    print(f"Percentage: {(results['version_dup_files'] / total_files * 100):.1f}% of files, {(results['version_dup_size'] / total_size * 100):.1f}% of storage")
    print(f"Groups: {len(results['version_duplicates']):,}")
    
    # Combined totals
    total_dup_files = results['exact_dup_files'] + results['version_dup_files']
    total_dup_size = results['exact_dup_size'] + results['version_dup_size']
    
    print("\n" + "─" * 80)
    print("💰 COMBINED TOTALS")
    print("─" * 80)
    print(f"Total Duplicate Files: {total_dup_files:,}")
    print(f"Total Duplicate Storage: {format_bytes(total_dup_size)}")
    print(f"Total Percentage: {(total_dup_files / total_files * 100):.1f}% of files, {(total_dup_size / total_size * 100):.1f}% of storage")
    
    # Hypothesis check
    print("\n" + "=" * 80)
    print("🧪 HYPOTHESIS CHECK")
    print("=" * 80)
    if total_files > 0:
        dup_pct = (total_dup_files / total_files) * 100
        print(f"\n📊 Total Duplication: {dup_pct:.1f}%")
        print(f"   - Exact duplicates: {(results['exact_dup_files'] / total_files * 100):.1f}%")
        print(f"   - Version duplicates: {(results['version_dup_files'] / total_files * 100):.1f}%")
        
        if dup_pct >= 20:
            print(f"\n✅ STRONGLY VALIDATED - {dup_pct:.1f}% duplicates (above expected 10-20%)")
            print("   Recommendation: Definitely build file reduction tool")
        elif dup_pct >= 10:
            print(f"\n✅ VALIDATED - {dup_pct:.1f}% duplicates (within expected 10-20%)")
            print("   Recommendation: Build file reduction tool")
        elif dup_pct >= 5:
            print(f"\n⚠️  PARTIALLY VALIDATED - {dup_pct:.1f}% duplicates (below expected)")
            print("   Recommendation: Calculate ROI before building")
        else:
            print(f"\n❌ INVALIDATED - {dup_pct:.1f}% duplicates (well below expected)")
            print("   Recommendation: Not worth building tool")
    
    # Top exact duplicates
    if results['exact_duplicates']:
        print("\n" + "=" * 80)
        print("🔝 TOP 10 EXACT DUPLICATES (by wasted space)")
        print("=" * 80)
        
        sorted_exact = sorted(
            results['exact_duplicates'].items(),
            key=lambda x: sum(f['size'] for f in x[1][1:]),
            reverse=True
        )[:10]
        
        for i, (hash_key, files) in enumerate(sorted_exact, 1):
            wasted = sum(f['size'] for f in files[1:])
            print(f"\n{i}. {len(files)} copies, {format_bytes(wasted)} wasted")
            print(f"   Hash: {hash_key[:16]}...")
            for j, file in enumerate(files[:3]):
                marker = "✓ KEEP" if j == 0 else "□ archive"
                print(f"   {marker} {file['path']}")
            if len(files) > 3:
                print(f"   ... and {len(files) - 3} more copies")
    
    # Top version groups
    if results['version_duplicates']:
        print("\n" + "=" * 80)
        print("🔝 TOP 10 VERSION GROUPS (by wasted space)")
        print("=" * 80)
        
        sorted_versions = sorted(
            results['version_duplicates'].items(),
            key=lambda x: sum(f['size'] for f in sorted(x[1], key=lambda f: f['modified'], reverse=True)[1:]),
            reverse=True
        )[:10]
        
        for i, (base_name, files) in enumerate(sorted_versions, 1):
            # Sort by modified date (newest first)
            sorted_files = sorted(files, key=lambda x: x['modified'], reverse=True)
            wasted = sum(f['size'] for f in sorted_files[1:])
            
            print(f"\n{i}. {len(files)} versions, {format_bytes(wasted)} wasted")
            print(f"   Base: {sorted_files[0]['normalized']}")
            for j, file in enumerate(sorted_files[:5]):
                marker = "✓ KEEP" if j == 0 else "□ archive"
                date_str = datetime.fromtimestamp(file['modified']).strftime('%Y-%m-%d')
                version_str = f" [{file['version_type']}:{file['version_value']}]" if file['version_type'] else ""
                print(f"   {marker} {file['filename']} ({date_str}){version_str}")
            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more versions")
    
    print("\n" + "=" * 80)

def save_report(results, output_path):
    """Save detailed report to JSON"""
    report = {
        'scan_date': datetime.now().isoformat(),
        'summary': {
            'total_files': results['total_files'],
            'total_size_bytes': results['total_size'],
            'total_size_readable': format_bytes(results['total_size']),
            
            'exact_duplicates': {
                'files': results['exact_dup_files'],
                'size_bytes': results['exact_dup_size'],
                'size_readable': format_bytes(results['exact_dup_size']),
                'percentage': (results['exact_dup_files'] / results['total_files'] * 100) if results['total_files'] > 0 else 0,
                'groups': len(results['exact_duplicates'])
            },
            
            'version_duplicates': {
                'files': results['version_dup_files'],
                'size_bytes': results['version_dup_size'],
                'size_readable': format_bytes(results['version_dup_size']),
                'percentage': (results['version_dup_files'] / results['total_files'] * 100) if results['total_files'] > 0 else 0,
                'groups': len(results['version_duplicates'])
            },
            
            'combined': {
                'files': results['exact_dup_files'] + results['version_dup_files'],
                'size_bytes': results['exact_dup_size'] + results['version_dup_size'],
                'size_readable': format_bytes(results['exact_dup_size'] + results['version_dup_size']),
                'percentage': ((results['exact_dup_files'] + results['version_dup_files']) / results['total_files'] * 100) if results['total_files'] > 0 else 0
            }
        },
        
        'exact_duplicate_groups': [
            {
                'hash': hash_key,
                'file_count': len(files),
                'wasted_bytes': sum(f['size'] for f in files[1:]),
                'files': files
            }
            for hash_key, files in results['exact_duplicates'].items()
        ],
        
        'version_groups': [
            {
                'base_name': base_name,
                'file_count': len(files),
                'wasted_bytes': sum(f['size'] for f in sorted(files, key=lambda x: x['modified'], reverse=True)[1:]),
                'files': sorted(files, key=lambda x: x['modified'], reverse=True)
            }
            for base_name, files in results['version_duplicates'].items()
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {output_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 enhanced_duplicate_check.py <folder_path>")
        print("\nExample:")
        print('  python3 enhanced_duplicate_check.py "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/HCSS/TGI Fridays"')
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
    output_file = "enhanced_duplicate_analysis_report.json"
    save_report(results, output_file)
    
    print("\n✅ Enhanced analysis complete!")
