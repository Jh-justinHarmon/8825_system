#!/usr/bin/env python3
"""
Process all 79 remaining files through the new system
"""

import os
from pathlib import Path

# API key should be set in environment (OPENAI_API_KEY)
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError('OPENAI_API_KEY environment variable not set')

from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine
from merge_engine import MergeEngine
from intelligent_naming import IntelligentNamingEngine
import time

print("="*80)
print("PROCESSING ALL FILES THROUGH NEW SYSTEM")
print("="*80)

index = ContentIndexEngine()
tracker = UsageTracker(index.db_path)
promotion = PromotionEngine(index.db_path, index.store_path, tracker)
merge = MergeEngine(index)
naming = IntelligentNamingEngine()

# Get all files
all_files = index.db.execute('SELECT * FROM files WHERE attributed = 0').fetchall()

print(f"\nProcessing {len(all_files)} files...\n")

stats = {
    'merged': 0,
    'promoted': 0,
    'skipped': 0,
    'errors': 0
}

for i, file in enumerate(all_files):
    print(f"[{i+1}/{len(all_files)}] {file['filename'][:60]}...")
    
    try:
        # Get content
        content = index.get_full_content(file['hash'])
        if not content:
            print("  ⚠️  No content")
            stats['errors'] += 1
            continue
        
        # Intelligent naming
        temp_path = Path(f"/tmp/{file['filename']}")
        result = naming.analyze_and_name(temp_path, content)
        
        # Check similarity
        similarity = merge.check_similarity(file['hash'], result['destination'])
        
        if similarity['action'] == 'merge':
            # Auto-merge
            merge_result = merge.auto_merge(file['hash'], similarity['best_match']['file'])
            
            if merge_result['status'] == 'merged':
                # Mark as attributed
                index.db.execute('''
                    UPDATE files 
                    SET attributed = 1,
                        destination = ?
                    WHERE hash = ?
                ''', (str(similarity['best_match']['file']), file['hash']))
                index.db.commit()
                
                # Delete from store
                store_files = list(index.store_path.glob(f"{file['hash']}*"))
                for sf in store_files:
                    sf.unlink()
                
                print(f"  ✅ Merged into: {similarity['best_match']['file'].name}")
                stats['merged'] += 1
            else:
                print(f"  ⚠️  Merge failed: {merge_result.get('reason', 'unknown')}")
                stats['errors'] += 1
        
        elif similarity['action'] == 'promote':
            # Promote as new file
            promo_result = promotion.promote_file(file['hash'], result['destination'], check_merge=False)
            
            if promo_result['status'] == 'promoted':
                print(f"  ✅ Promoted to: {result['destination']}")
                stats['promoted'] += 1
            else:
                print(f"  ⚠️  Promotion failed")
                stats['errors'] += 1
        
        else:  # skip
            # Mark as attributed (duplicate)
            index.db.execute('''
                UPDATE files 
                SET attributed = 1,
                    destination = ?
                WHERE hash = ?
            ''', (result['destination'], file['hash']))
            index.db.commit()
            
            # Delete from store
            store_files = list(index.store_path.glob(f"{file['hash']}*"))
            for sf in store_files:
                sf.unlink()
            
            print(f"  ✅ Skipped (duplicate)")
            stats['skipped'] += 1
        
        # Rate limit protection
        time.sleep(0.5)
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        stats['errors'] += 1

print("\n" + "="*80)
print("PROCESSING COMPLETE")
print("="*80)
print(f"\nResults:")
print(f"  Merged: {stats['merged']}")
print(f"  Promoted: {stats['promoted']}")
print(f"  Skipped: {stats['skipped']}")
print(f"  Errors: {stats['errors']}")

print(f"\nFinal index stats:")
final_stats = index.get_stats()
print(f"  Total: {final_stats['total']}")
print(f"  Unattributed: {final_stats['unattributed']}")
print(f"  Attributed: {final_stats['attributed']}")
