#!/usr/bin/env python3
"""
Check if files are linked/referenced by other files
Useful for determining which versions are actually used
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

def extract_links_from_pdf(filepath):
    """Extract image references from PDF files"""
    links = set()
    try:
        # PDFs can embed or link to images
        # This is a basic check - would need PyPDF2 for full parsing
        with open(filepath, 'rb') as f:
            content = f.read()
            # Look for common image file references in PDF
            # This is approximate - PDFs can embed images without filenames
            patterns = [
                rb'/F \(([^)]+\.(?:jpg|jpeg|png|tif|tiff|ai|psd))\)',
                rb'<<\s*/Type\s*/XObject.*?/Subtype\s*/Image.*?/Name\s*/([^\s>]+)',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                links.update(m.decode('utf-8', errors='ignore') for m in matches)
    except Exception as e:
        pass
    return links

def extract_links_from_ai(filepath):
    """Extract image references from Adobe Illustrator files"""
    links = set()
    try:
        # AI files are PDF-based, can contain linked images
        with open(filepath, 'rb') as f:
            content = f.read()
            # Look for linked file references
            patterns = [
                rb'%%PlacedGraphic:\s*([^\r\n]+)',
                rb'/FileSpec\s*<<.*?/F\s*\(([^)]+)\)',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                links.update(m.decode('utf-8', errors='ignore').strip() for m in matches)
    except Exception as e:
        pass
    return links

def extract_links_from_indd(filepath):
    """Extract image references from InDesign files"""
    links = set()
    # InDesign files are binary, would need InDesign SDK or IDML export
    # This is a placeholder for future implementation
    return links

def extract_links_from_text(filepath):
    """Extract file references from text-based files (HTML, MD, etc.)"""
    links = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Look for common file reference patterns
            patterns = [
                r'src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|svg|webp))["\']',
                r'href=["\']([^"\']+\.(?:pdf|ai|psd))["\']',
                r'\!\[.*?\]\(([^)]+)\)',  # Markdown images
                r'url\(["\']?([^"\'()]+\.(?:jpg|jpeg|png|gif|svg))["\']?\)',  # CSS
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                links.update(matches)
    except Exception as e:
        pass
    return links

def check_dropbox_shared_links(filepath):
    """Check if file has Dropbox shared links (from extended attributes)"""
    try:
        # macOS extended attributes can store Dropbox metadata
        import subprocess
        result = subprocess.run(
            ['xattr', '-l', filepath],
            capture_output=True,
            text=True
        )
        if 'com.dropbox' in result.stdout:
            # File has Dropbox metadata, might be shared
            return True
    except Exception:
        pass
    return False

def scan_for_links(root_path):
    """Scan folder and detect which files are linked/referenced"""
    print(f"\n🔍 Scanning for file links: {root_path}")
    print("=" * 80)
    
    all_files = {}
    file_links = defaultdict(set)  # file -> set of files it links to
    reverse_links = defaultdict(set)  # file -> set of files that link to it
    
    # First pass: collect all files
    print("\n📁 Pass 1: Collecting files...")
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            if filename.startswith('.') or filename == 'Icon\r':
                continue
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_path)
            all_files[rel_path] = filepath
    
    print(f"   Found {len(all_files)} files")
    
    # Second pass: extract links from files that can contain references
    print("\n🔗 Pass 2: Extracting links...")
    files_processed = 0
    
    for rel_path, filepath in all_files.items():
        ext = os.path.splitext(filepath)[1].lower()
        links = set()
        
        # Extract links based on file type
        if ext == '.pdf':
            links = extract_links_from_pdf(filepath)
        elif ext == '.ai':
            links = extract_links_from_ai(filepath)
        elif ext == '.indd':
            links = extract_links_from_indd(filepath)
        elif ext in ['.html', '.htm', '.md', '.css', '.js']:
            links = extract_links_from_text(filepath)
        
        if links:
            file_links[rel_path] = links
            # Try to resolve links to actual files
            for link in links:
                # Try different path resolutions
                link_basename = os.path.basename(link)
                for candidate_path in all_files.keys():
                    if os.path.basename(candidate_path) == link_basename:
                        reverse_links[candidate_path].add(rel_path)
        
        files_processed += 1
        if files_processed % 100 == 0:
            print(f"   Processed {files_processed}/{len(all_files)} files...", end='\r')
    
    print(f"   Processed {files_processed}/{len(all_files)} files... Done!")
    
    # Third pass: check Dropbox shared links
    print("\n📤 Pass 3: Checking Dropbox shared links...")
    shared_files = set()
    for rel_path, filepath in all_files.items():
        if check_dropbox_shared_links(filepath):
            shared_files.add(rel_path)
    
    print(f"   Found {len(shared_files)} files with Dropbox metadata")
    
    return {
        'all_files': all_files,
        'file_links': dict(file_links),
        'reverse_links': dict(reverse_links),
        'shared_files': shared_files
    }

def print_report(results):
    """Print link analysis report"""
    all_files = results['all_files']
    file_links = results['file_links']
    reverse_links = results['reverse_links']
    shared_files = results['shared_files']
    
    print("\n" + "=" * 80)
    print("📊 FILE LINK ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\n📁 Total Files: {len(all_files):,}")
    print(f"🔗 Files with outgoing links: {len(file_links):,}")
    print(f"📎 Files with incoming links: {len(reverse_links):,}")
    print(f"📤 Files with Dropbox metadata: {len(shared_files):,}")
    
    # Unreferenced files
    unreferenced = set(all_files.keys()) - set(reverse_links.keys())
    print(f"\n⚠️  Unreferenced files: {len(unreferenced):,}")
    
    # Image files specifically
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff', '.webp', '.heic'}
    all_images = {f for f in all_files.keys() if os.path.splitext(f)[1].lower() in image_exts}
    referenced_images = {f for f in reverse_links.keys() if os.path.splitext(f)[1].lower() in image_exts}
    unreferenced_images = all_images - referenced_images
    
    print(f"\n📷 Image Files:")
    print(f"   Total: {len(all_images):,}")
    print(f"   Referenced: {len(referenced_images):,}")
    print(f"   Unreferenced: {len(unreferenced_images):,} ({len(unreferenced_images)/len(all_images)*100:.1f}%)")
    
    # Most referenced files
    if reverse_links:
        print("\n" + "=" * 80)
        print("🔝 TOP 10 MOST REFERENCED FILES")
        print("=" * 80)
        sorted_refs = sorted(reverse_links.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (file, refs) in enumerate(sorted_refs, 1):
            print(f"\n{i}. {file}")
            print(f"   Referenced by {len(refs)} files:")
            for ref in list(refs)[:3]:
                print(f"   - {ref}")
            if len(refs) > 3:
                print(f"   ... and {len(refs) - 3} more")
    
    # Files that link to many others
    if file_links:
        print("\n" + "=" * 80)
        print("🔗 TOP 10 FILES WITH MOST OUTGOING LINKS")
        print("=" * 80)
        sorted_links = sorted(file_links.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (file, links) in enumerate(sorted_links, 1):
            print(f"\n{i}. {file}")
            print(f"   Links to {len(links)} files:")
            for link in list(links)[:3]:
                print(f"   - {link}")
            if len(links) > 3:
                print(f"   ... and {len(links) - 3} more")
    
    # Unreferenced images (potential candidates for cleanup)
    if unreferenced_images:
        print("\n" + "=" * 80)
        print("⚠️  SAMPLE UNREFERENCED IMAGES (potential cleanup candidates)")
        print("=" * 80)
        print("\nNote: These images are not referenced by any scanned files.")
        print("They might be:")
        print("- Unused versions/iterations")
        print("- Referenced by external files")
        print("- Shared via Dropbox links")
        print("- Used in applications not scanned")
        
        sample_unreferenced = sorted(unreferenced_images)[:20]
        for img in sample_unreferenced:
            shared_marker = " [SHARED]" if img in shared_files else ""
            print(f"   {img}{shared_marker}")
        if len(unreferenced_images) > 20:
            print(f"   ... and {len(unreferenced_images) - 20} more")
    
    print("\n" + "=" * 80)
    print("⚠️  IMPORTANT LIMITATIONS")
    print("=" * 80)
    print("""
This analysis has limitations:
1. Cannot detect links in binary formats (InDesign, Photoshop, etc.)
2. Cannot detect links in external systems (websites, emails, etc.)
3. Cannot detect Dropbox shared links reliably
4. May miss embedded images (vs linked images)
5. Path resolution is approximate

Recommendation:
- Use this as a GUIDE, not absolute truth
- Manually verify before deleting "unreferenced" files
- Check Dropbox sharing history
- Consider file modification dates (recent = likely in use)
    """)

def save_report(results, output_path):
    """Save detailed report to JSON"""
    report = {
        'total_files': len(results['all_files']),
        'files_with_links': len(results['file_links']),
        'referenced_files': len(results['reverse_links']),
        'shared_files': len(results['shared_files']),
        'file_links': results['file_links'],
        'reverse_links': {k: list(v) for k, v in results['reverse_links'].items()},
        'shared_files': list(results['shared_files'])
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {output_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 check_file_links.py <folder_path>")
        print("\nExample:")
        print('  python3 check_file_links.py "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/ - PRTCL -/AIMEE KESTENBERG"')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not os.path.isdir(folder_path):
        print(f"❌ Error: Not a directory: {folder_path}")
        sys.exit(1)
    
    # Scan for links
    results = scan_for_links(folder_path)
    
    # Print report
    print_report(results)
    
    # Save detailed report
    output_file = "file_links_report.json"
    save_report(results, output_file)
    
    print("\n✅ Link analysis complete!")
