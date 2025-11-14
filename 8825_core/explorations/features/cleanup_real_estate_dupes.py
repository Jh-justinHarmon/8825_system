#!/usr/bin/env python3
"""
Safe cleanup script for Real Estate folder duplicates
Only deletes exact duplicates, preserves originals
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def format_bytes(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def safe_delete_duplicates(root_path, dry_run=True):
    """Delete exact duplicates from Real Estate folder"""
    
    # Load the duplicate analysis report
    report_path = 'enhanced_duplicate_analysis_report.json'
    if not os.path.exists(report_path):
        print("❌ Error: enhanced_duplicate_analysis_report.json not found")
        print("   Run enhanced_duplicate_check.py first!")
        return
    
    with open(report_path, 'r') as f:
        report = json.load(f)
    
    # Define safe deletion rules
    safe_deletions = []
    
    # Rule 1: Delete duplicates in "Photos" folder if original in "Closing Binder"
    # Rule 2: Delete duplicates in nested "Curbio/Curbio" folder
    # Rule 3: Delete duplicates in "Trash" folders
    # Rule 4: Delete duplicates in dated folders (older dates)
    # Rule 5: Delete duplicates with " 2" suffix (duplicate folder marker)
    
    for group in report.get('exact_duplicates', []):
        files = group.get('files', [])
        if len(files) < 2:
            continue
        
        # Sort by priority (keep first, delete rest)
        # Priority: non-trash > non-duplicate-folder > shorter path
        def priority_score(filepath):
            score = 0
            path_lower = filepath.lower()
            
            # Prefer non-trash
            if '/trash/' in path_lower:
                score += 1000
            
            # Prefer non-duplicate folders
            if ' 2/' in filepath or ' 2.' in filepath:
                score += 500
            
            # Prefer non-nested Curbio
            if '/curbio/curbio/' in path_lower:
                score += 400
            
            # Prefer Closing Binder over Photos
            if '/photos/' in path_lower and any('/closing binder/' in f.lower() for f in files):
                score += 300
            
            # Prefer shorter paths (less nested)
            score += filepath.count('/')
            
            return score
        
        sorted_files = sorted(files, key=priority_score)
        keep_file = sorted_files[0]
        delete_files = sorted_files[1:]
        
        for delete_file in delete_files:
            # Verify it's safe to delete
            if any(marker in delete_file.lower() for marker in ['/trash/', ' 2/', '/curbio/curbio/', '/photos/']):
                safe_deletions.append({
                    'delete': delete_file,
                    'keep': keep_file,
                    'size': group.get('size', 0),
                    'reason': 'exact duplicate'
                })
    
    # Print summary
    print("\n" + "=" * 80)
    print("🗑️  SAFE DELETION PLAN - REAL ESTATE FOLDER")
    print("=" * 80)
    
    if not safe_deletions:
        print("\n✅ No safe deletions identified")
        return
    
    total_size = sum(d['size'] for d in safe_deletions)
    
    print(f"\n📊 Summary:")
    print(f"   Files to delete: {len(safe_deletions)}")
    print(f"   Space to save: {format_bytes(total_size)}")
    print(f"   Mode: {'DRY RUN (no files will be deleted)' if dry_run else 'LIVE (files will be deleted!)'}")
    
    print("\n" + "=" * 80)
    print("📋 DELETION LIST")
    print("=" * 80)
    
    # Group by reason
    by_reason = {}
    for deletion in safe_deletions:
        reason = deletion['reason']
        if reason not in by_reason:
            by_reason[reason] = []
        by_reason[reason].append(deletion)
    
    for reason, deletions in by_reason.items():
        print(f"\n{reason.upper()}:")
        for d in sorted(deletions, key=lambda x: x['size'], reverse=True)[:20]:
            rel_delete = os.path.relpath(d['delete'], root_path)
            rel_keep = os.path.relpath(d['keep'], root_path)
            print(f"\n   ❌ DELETE: {rel_delete}")
            print(f"      ({format_bytes(d['size'])})")
            print(f"   ✓ KEEP:   {rel_keep}")
        
        if len(deletions) > 20:
            print(f"\n   ... and {len(deletions) - 20} more files")
    
    # Execute deletions
    if not dry_run:
        print("\n" + "=" * 80)
        print("⚠️  EXECUTING DELETIONS")
        print("=" * 80)
        
        # Create backup manifest
        backup_dir = os.path.join(root_path, '---DELETED-BACKUP---', datetime.now().strftime('%Y%m%d_%H%M%S'))
        os.makedirs(backup_dir, exist_ok=True)
        
        manifest = {
            'date': datetime.now().isoformat(),
            'total_files': len(safe_deletions),
            'total_size': total_size,
            'deletions': []
        }
        
        deleted_count = 0
        deleted_size = 0
        
        for deletion in safe_deletions:
            delete_path = deletion['delete']
            
            try:
                if os.path.exists(delete_path):
                    # Move to backup instead of deleting
                    rel_path = os.path.relpath(delete_path, root_path)
                    backup_path = os.path.join(backup_dir, rel_path)
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    
                    shutil.move(delete_path, backup_path)
                    
                    deleted_count += 1
                    deleted_size += deletion['size']
                    
                    manifest['deletions'].append({
                        'original': delete_path,
                        'backup': backup_path,
                        'kept': deletion['keep'],
                        'size': deletion['size']
                    })
                    
                    print(f"   ✓ Moved to backup: {rel_path}")
            except Exception as e:
                print(f"   ❌ Error: {delete_path}")
                print(f"      {str(e)}")
        
        # Save manifest
        manifest_path = os.path.join(backup_dir, 'MANIFEST.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print("\n" + "=" * 80)
        print("✅ CLEANUP COMPLETE")
        print("=" * 80)
        print(f"\n   Files moved to backup: {deleted_count}")
        print(f"   Space saved: {format_bytes(deleted_size)}")
        print(f"   Backup location: {backup_dir}")
        print(f"   Manifest: {manifest_path}")
        print("\n   To rollback, restore files from backup folder")
    else:
        print("\n" + "=" * 80)
        print("ℹ️  DRY RUN COMPLETE - NO FILES DELETED")
        print("=" * 80)
        print("\n   To execute deletions, run with --execute flag:")
        print("   python3 cleanup_real_estate_dupes.py --execute")

def main():
    import sys
    
    root_path = "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/-- daisy --/Real Estate"
    
    # Check if execute flag is set
    dry_run = '--execute' not in sys.argv
    
    if not dry_run:
        print("\n⚠️  WARNING: This will move duplicate files to backup!")
        response = input("   Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("   Cancelled.")
            return
    
    safe_delete_duplicates(root_path, dry_run=dry_run)

if __name__ == "__main__":
    main()
