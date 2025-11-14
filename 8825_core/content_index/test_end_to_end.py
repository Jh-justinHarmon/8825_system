#!/usr/bin/env python3
"""
Complete end-to-end test
"""

import os
from pathlib import Path

# API key should be set in environment (OPENAI_API_KEY)
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError('OPENAI_API_KEY environment variable not set')

from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine

print("="*80)
print("END-TO-END TEST: Complete Flow")
print("="*80)

# Pick a real file from index
index = ContentIndexEngine()
tracker = UsageTracker(index.db_path)
promotion = PromotionEngine(index.db_path, index.store_path, tracker)

# Get RAL API file
file = index.db.execute(
    "SELECT * FROM files WHERE filename = 'RAL_REST_API_Documentation.txt'"
).fetchone()

if not file:
    print("Test file not found")
    exit(1)

print(f"\nTest file: {file['filename']}")
print(f"Hash: {file['hash']}")

# Step 1: Get content
print("\n1. Getting content from store...")
content = index.get_full_content(file['hash'])
if content:
    print(f"   ✅ Content loaded ({len(content)} bytes)")
else:
    print("   ❌ Content not found")
    exit(1)

# Step 2: Re-analyze with intelligent naming
print("\n2. Analyzing with intelligent naming...")
from intelligent_naming import IntelligentNamingEngine
naming = IntelligentNamingEngine()

temp_path = Path(f"/tmp/{file['filename']}")
result = naming.analyze_and_name(temp_path, content)

print(f"   New name: {result['suggested_filename']}")
print(f"   Category: {result['category']}")
print(f"   Destination: {result['destination']}")
print(f"   Reasoning: {result.get('reasoning', 'N/A')}")

# Step 3: Calculate confidence
print("\n3. Calculating promotion confidence...")
confidence = promotion.calculate_confidence(file['hash'])
print(f"   Confidence: {confidence:.2f}")

# Step 4: Check for merge
print("\n4. Checking for similar files (merge check)...")
from merge_engine import MergeEngine
merge = MergeEngine(index)

similarity = merge.check_similarity(file['hash'], result['destination'])
print(f"   Action: {similarity['action']}")

if similarity['action'] == 'merge':
    print(f"   Would merge into: {similarity['best_match']['file'].name}")
    print(f"   Similarity score: {similarity['best_match']['score']:.2f}")
    
    # Step 5: Actually merge
    print("\n5. Performing merge...")
    merge_result = merge.auto_merge(file['hash'], similarity['best_match']['file'])
    
    if merge_result['status'] == 'merged':
        print(f"   ✅ Merged into: {merge_result['file']}")
        
        # Step 6: Mark as attributed and cleanup
        print("\n6. Marking as attributed and cleaning up...")
        index.db.execute('''
            UPDATE files 
            SET attributed = 1,
                destination = ?
            WHERE hash = ?
        ''', (str(similarity['best_match']['file']), file['hash']))
        index.db.commit()
        
        # Delete from content_store
        store_files = list(index.store_path.glob(f"{file['hash']}*"))
        for sf in store_files:
            sf.unlink()
            print(f"   ✅ Deleted from store: {sf.name}")
        
        print("\n" + "="*80)
        print("END-TO-END TEST COMPLETE")
        print("="*80)
        print("\nWhat happened:")
        print("1. ✅ Loaded file from index")
        print("2. ✅ Analyzed with intelligent naming")
        print("3. ✅ Calculated confidence")
        print("4. ✅ Detected similar file")
        print("5. ✅ Auto-merged content")
        print("6. ✅ Marked as attributed")
        print("7. ✅ Cleaned up from store")
        print("\nResult: File content merged into knowledge base, index cleaned up")
    else:
        print(f"   ❌ Merge failed: {merge_result}")

elif similarity['action'] == 'promote':
    print("\n5. Would promote as new file")
    print("   (Skipping actual promotion in test)")

elif similarity['action'] == 'skip':
    print("\n5. Would skip (duplicate)")
    print("   (Would cleanup from index)")
