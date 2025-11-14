#!/usr/bin/env python3
"""
Analyze file usage metadata to infer which files are actively used
Focus on: access times, modification patterns, file relationships
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def get_file_metadata(filepath):
    """Extract all available metadata from a file"""
    try:
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'accessed': stat.st_atime,  # Last access time
            'created': stat.st_birthtime if hasattr(stat, 'st_birthtime') else stat.st_ctime,
            'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'accessed_date': datetime.fromtimestamp(stat.st_atime).isoformat(),
            'created_date': datetime.fromtimestamp(stat.st_birthtime if hasattr(stat, 'st_birthtime') else stat.st_ctime).isoformat(),
        }
    except Exception as e:
        return None

def get_macos_extended_attributes(filepath):
    """Get macOS extended attributes (Finder tags, Dropbox sync, etc.)"""
    attrs = {}
    try:
        import subprocess
        # Get extended attributes
        result = subprocess.run(
            ['xattr', '-l', filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            attrs['has_extended_attrs'] = True
            attrs['extended_attrs'] = result.stdout
            
            # Check for specific attributes
            if 'com.apple.metadata:kMDItemFinderComment' in result.stdout:
                attrs['has_finder_comment'] = True
            if 'com.apple.FinderInfo' in result.stdout:
                attrs['has_finder_info'] = True
            if 'com.dropbox' in result.stdout:
                attrs['has_dropbox_attrs'] = True
        else:
            attrs['has_extended_attrs'] = False
    except Exception as e:
        attrs['error'] = str(e)
    
    return attrs

def analyze_access_patterns(files_metadata):
    """Analyze access patterns to infer usage"""
    now = time.time()
    
    patterns = {
        'recently_accessed': [],      # Accessed in last 30 days
        'recently_modified': [],      # Modified in last 30 days
        'old_but_accessed': [],       # Old file, but recently accessed
        'created_never_accessed': [], # Created but never accessed since
        'stale': [],                  # Not accessed in 6+ months
        'active': [],                 # Both modified and accessed recently
    }
    
    for filepath, meta in files_metadata.items():
        if not meta:
            continue
        
        days_since_access = (now - meta['accessed']) / 86400
        days_since_modified = (now - meta['modified']) / 86400
        days_since_created = (now - meta['created']) / 86400
        
        # Recently accessed (strong signal of usage)
        if days_since_access < 30:
            patterns['recently_accessed'].append(filepath)
        
        # Recently modified
        if days_since_modified < 30:
            patterns['recently_modified'].append(filepath)
        
        # Old file but recently accessed (likely linked/referenced)
        if days_since_created > 180 and days_since_access < 30:
            patterns['old_but_accessed'].append(filepath)
        
        # Created but never accessed (might be unused)
        if abs(meta['accessed'] - meta['created']) < 60:  # Within 1 minute
            patterns['created_never_accessed'].append(filepath)
        
        # Stale (not accessed in 6+ months)
        if days_since_access > 180:
            patterns['stale'].append(filepath)
        
        # Active (both modified and accessed recently)
        if days_since_access < 30 and days_since_modified < 30:
            patterns['active'].append(filepath)
    
    return patterns

def find_linked_image_candidates(root_path, files_metadata):
    """
    Find images that are likely linked by AI/design files
    Based on:
    1. Access time correlation (accessed around same time as AI file)
    2. Folder proximity (in same or nearby folder)
    3. Naming patterns (similar base names)
    """
    
    # Separate design files from images
    design_exts = {'.ai', '.indd', '.psd', '.sketch', '.fig'}
    image_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.eps', '.pdf'}
    
    design_files = {}
    image_files = {}
    
    for filepath, meta in files_metadata.items():
        if not meta:
            continue
        ext = os.path.splitext(filepath)[1].lower()
        if ext in design_exts:
            design_files[filepath] = meta
        elif ext in image_exts:
            image_files[filepath] = meta
    
    # Find potential links based on access time correlation
    linked_candidates = defaultdict(list)
    
    for design_path, design_meta in design_files.items():
        design_access = design_meta['accessed']
        design_dir = os.path.dirname(design_path)
        
        # Look for images accessed within 1 hour of design file
        time_window = 3600  # 1 hour
        
        for image_path, image_meta in image_files.items():
            image_access = image_meta['accessed']
            image_dir = os.path.dirname(image_path)
            
            # Check time correlation
            time_diff = abs(design_access - image_access)
            
            # Check folder proximity
            same_folder = design_dir == image_dir
            nearby_folder = design_dir in image_dir or image_dir in design_dir
            
            if time_diff < time_window and (same_folder or nearby_folder):
                linked_candidates[design_path].append({
                    'image': image_path,
                    'time_diff_seconds': time_diff,
                    'same_folder': same_folder,
                    'design_accessed': design_meta['accessed_date'],
                    'image_accessed': image_meta['accessed_date']
                })
    
    return linked_candidates

def scan_folder(root_path):
    """Scan folder and collect all metadata"""
    print(f"\n🔍 Scanning: {root_path}")
    print("=" * 80)
    
    files_metadata = {}
    files_extended = {}
    total_files = 0
    
    print("\n📁 Collecting file metadata...")
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.startswith('.') or filename == 'Icon\r':
                continue
            
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_path)
            
            # Get basic metadata
            meta = get_file_metadata(filepath)
            if meta:
                files_metadata[rel_path] = meta
            
            # Get extended attributes (sample only, it's slow)
            if total_files < 50:  # Sample first 50 files
                ext_attrs = get_macos_extended_attributes(filepath)
                if ext_attrs:
                    files_extended[rel_path] = ext_attrs
            
            total_files += 1
            if total_files % 100 == 0:
                print(f"   Scanned {total_files} files...", end='\r')
    
    print(f"   Scanned {total_files} files... Done!")
    
    return files_metadata, files_extended

def print_report(root_path, files_metadata, files_extended):
    """Print usage analysis report"""
    
    print("\n" + "=" * 80)
    print("📊 FILE USAGE METADATA ANALYSIS")
    print("=" * 80)
    
    print(f"\n📁 Total Files Analyzed: {len(files_metadata):,}")
    
    # Analyze access patterns
    print("\n🔍 Analyzing access patterns...")
    patterns = analyze_access_patterns(files_metadata)
    
    print("\n" + "─" * 80)
    print("📈 ACCESS PATTERN ANALYSIS")
    print("─" * 80)
    
    print(f"\n🟢 Recently Accessed (< 30 days): {len(patterns['recently_accessed']):,}")
    print(f"🟢 Recently Modified (< 30 days): {len(patterns['recently_modified']):,}")
    print(f"🟢 Active (both modified & accessed): {len(patterns['active']):,}")
    print(f"🟡 Old but Recently Accessed: {len(patterns['old_but_accessed']):,}")
    print(f"🔴 Stale (not accessed in 6+ months): {len(patterns['stale']):,}")
    print(f"⚪ Created but Never Accessed: {len(patterns['created_never_accessed']):,}")
    
    # Calculate percentages
    total = len(files_metadata)
    if total > 0:
        print(f"\n📊 Usage Breakdown:")
        print(f"   Active usage: {len(patterns['active'])/total*100:.1f}%")
        print(f"   Recent access: {len(patterns['recently_accessed'])/total*100:.1f}%")
        print(f"   Stale: {len(patterns['stale'])/total*100:.1f}%")
    
    # Find linked image candidates
    print("\n🔗 Analyzing potential linked images...")
    linked_candidates = find_linked_image_candidates(root_path, files_metadata)
    
    if linked_candidates:
        print("\n" + "─" * 80)
        print("🎨 POTENTIAL LINKED IMAGES (by access time correlation)")
        print("─" * 80)
        print(f"\nFound {len(linked_candidates)} design files with potential linked images")
        
        # Show top 10
        sorted_links = sorted(
            linked_candidates.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:10]
        
        for i, (design_file, images) in enumerate(sorted_links, 1):
            print(f"\n{i}. {design_file}")
            print(f"   Potentially links to {len(images)} images:")
            for img_info in images[:3]:
                time_diff = img_info['time_diff_seconds']
                time_str = f"{time_diff/60:.0f} min" if time_diff < 3600 else f"{time_diff/3600:.1f} hrs"
                folder_str = "same folder" if img_info['same_folder'] else "nearby folder"
                print(f"   - {img_info['image']}")
                print(f"     (accessed within {time_str}, {folder_str})")
            if len(images) > 3:
                print(f"   ... and {len(images) - 3} more")
    else:
        print("\n⚠️  No strong time correlations found")
        print("   This could mean:")
        print("   - Images are embedded, not linked")
        print("   - Files haven't been opened recently")
        print("   - Access times not preserved by Dropbox sync")
    
    # Extended attributes analysis
    if files_extended:
        print("\n" + "─" * 80)
        print("🏷️  EXTENDED ATTRIBUTES SAMPLE (first 50 files)")
        print("─" * 80)
        
        has_dropbox = sum(1 for f in files_extended.values() if f.get('has_dropbox_attrs'))
        has_finder = sum(1 for f in files_extended.values() if f.get('has_finder_info'))
        
        print(f"\nFiles with Dropbox attributes: {has_dropbox}/{len(files_extended)}")
        print(f"Files with Finder info: {has_finder}/{len(files_extended)}")
    
    # Show sample of stale files
    if patterns['stale']:
        print("\n" + "─" * 80)
        print("🔴 SAMPLE STALE FILES (not accessed in 6+ months)")
        print("─" * 80)
        print("\nThese files might be safe to archive:")
        
        # Sort by last access time (oldest first)
        stale_with_meta = [
            (f, files_metadata[f]) for f in patterns['stale']
            if f in files_metadata
        ]
        stale_sorted = sorted(stale_with_meta, key=lambda x: x[1]['accessed'])[:20]
        
        for filepath, meta in stale_sorted:
            days_since_access = (time.time() - meta['accessed']) / 86400
            print(f"   {filepath}")
            print(f"     Last accessed: {meta['accessed_date']} ({days_since_access:.0f} days ago)")
    
    # Show old but recently accessed (likely linked!)
    if patterns['old_but_accessed']:
        print("\n" + "─" * 80)
        print("🟡 OLD FILES RECENTLY ACCESSED (likely linked/in use!)")
        print("─" * 80)
        print("\nThese old files were accessed recently - probably linked by design files:")
        
        old_accessed_with_meta = [
            (f, files_metadata[f]) for f in patterns['old_but_accessed']
            if f in files_metadata
        ]
        old_accessed_sorted = sorted(old_accessed_with_meta, key=lambda x: x[1]['accessed'], reverse=True)[:20]
        
        for filepath, meta in old_accessed_sorted:
            days_since_created = (time.time() - meta['created']) / 86400
            days_since_accessed = (time.time() - meta['accessed']) / 86400
            print(f"   {filepath}")
            print(f"     Created: {days_since_created:.0f} days ago")
            print(f"     Last accessed: {days_since_accessed:.0f} days ago")
            print(f"     ⚠️  DO NOT ARCHIVE - likely in use!")
    
    print("\n" + "=" * 80)
    print("💡 KEY INSIGHTS")
    print("=" * 80)
    print("""
1. ACCESS TIME LIMITATIONS:
   - Dropbox sync may not preserve access times accurately
   - Some systems update access time on scan/backup
   - Access time can be unreliable for cloud-synced files

2. BEST INDICATORS OF USAGE:
   ✅ Recently modified (< 30 days) - definitely in use
   ✅ Old file, recently accessed - likely linked by design file
   ✅ Access time correlation - images accessed with design files
   ⚠️  Stale (6+ months) - candidate for archive, but verify first

3. SAFE ARCHIVE CANDIDATES:
   - Files not accessed in 12+ months
   - Old versions with newer versions available
   - Files in "old" or "archive" folders
   - Sequential numbered files (IMG_001, IMG_002...)

4. DO NOT ARCHIVE:
   ❌ Files accessed in last 6 months
   ❌ Old files recently accessed (likely linked!)
   ❌ Files with "final", "approved" in name
   ❌ Most recent version in a version group
    """)

def save_report(files_metadata, patterns, linked_candidates, output_path):
    """Save detailed report to JSON"""
    report = {
        'scan_date': datetime.now().isoformat(),
        'total_files': len(files_metadata),
        'patterns': {
            'recently_accessed': len(patterns['recently_accessed']),
            'recently_modified': len(patterns['recently_modified']),
            'active': len(patterns['active']),
            'old_but_accessed': len(patterns['old_but_accessed']),
            'stale': len(patterns['stale']),
            'created_never_accessed': len(patterns['created_never_accessed'])
        },
        'linked_candidates_count': len(linked_candidates),
        'files_by_pattern': {
            'recently_accessed': patterns['recently_accessed'][:100],
            'stale': patterns['stale'][:100],
            'old_but_accessed': patterns['old_but_accessed'][:100]
        },
        'linked_candidates': {
            k: v for k, v in list(linked_candidates.items())[:50]
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {output_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_file_usage_metadata.py <folder_path>")
        print("\nExample:")
        print('  python3 analyze_file_usage_metadata.py "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/ - PRTCL -/AIMEE KESTENBERG"')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not os.path.isdir(folder_path):
        print(f"❌ Error: Not a directory: {folder_path}")
        sys.exit(1)
    
    # Scan folder
    files_metadata, files_extended = scan_folder(folder_path)
    
    # Analyze patterns
    patterns = analyze_access_patterns(files_metadata)
    
    # Find linked candidates
    linked_candidates = find_linked_image_candidates(folder_path, files_metadata)
    
    # Print report
    print_report(folder_path, files_metadata, files_extended)
    
    # Save report
    output_file = "file_usage_analysis_report.json"
    save_report(files_metadata, patterns, linked_candidates, output_file)
    
    print("\n✅ Usage analysis complete!")
