#!/usr/bin/env python3
"""
End-to-End System Test
Test complete flow: ingest → name → index → promote/merge
"""

import os
import sys
from pathlib import Path

# API key should be set in environment (OPENAI_API_KEY)
# Check if set
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError('OPENAI_API_KEY environment variable not set')

from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine
from decay_engine import DecayEngine


def test_complete_flow():
    """
    Test the complete system with a real file
    """
    
    print("="*80)
    print("CONTENT INDEX SYSTEM - END-TO-END TEST")
    print("="*80)
    
    # Initialize system
    print("\n1. Initializing system...")
    index = ContentIndexEngine()
    tracker = UsageTracker(index.db_path)
    promotion = PromotionEngine(index.db_path, index.store_path, tracker)
    decay = DecayEngine(index.db_path)
    
    print("   ✅ System initialized")
    
    # Test file
    test_file = Path.home() / 'Downloads/8825_inbox/processing/lane_b/API_Endpoint_File_Upload_Documentation.md'
    
    if not test_file.exists():
        print(f"\n❌ Test file not found: {test_file}")
        return
    
    print(f"\n2. Testing with file: {test_file.name}")
    
    # Step 1: Ingest with intelligent naming
    print("\n3. Ingesting file (with intelligent naming)...")
    result = index.ingest(test_file, use_intelligent_naming=True)
    
    print(f"   Status: {result['status']}")
    
    if result['status'] == 'indexed':
        print(f"   Hash: {result['hash']}")
        print(f"   Intelligent filename: {result['metadata']['filename']}")
        
        if 'intelligent_metadata' in result:
            intel = result['intelligent_metadata']
            print(f"   Category: {intel['category']}")
            print(f"   Entities: {intel['entities']}")
            print(f"   Suggested destination: {intel['destination']}")
        
        # Step 2: Calculate confidence
        print("\n4. Calculating promotion confidence...")
        confidence = promotion.calculate_confidence(result['hash'])
        print(f"   Confidence: {confidence:.2f}")
        
        # Step 3: Check for promotion
        if confidence >= 0.85:
            print("\n5. High confidence - attempting promotion...")
            destination = promotion.suggest_destination(result['hash'])
            print(f"   Destination: {destination}")
            
            # Promote (with merge check)
            promo_result = promotion.promote_file(result['hash'], destination, check_merge=True)
            
            print(f"\n   Result: {promo_result['status']}")
            if promo_result['status'] == 'merged':
                print(f"   ✅ Merged into: {promo_result['destination']}")
            elif promo_result['status'] == 'promoted':
                print(f"   ✅ Promoted to: {promo_result['destination']}")
            elif promo_result['status'] == 'skipped':
                print(f"   ⚠️  Skipped: {promo_result['reason']}")
        
        elif confidence >= 0.70:
            print("\n5. Medium confidence - would suggest to user")
            destination = promotion.suggest_destination(result['hash'])
            print(f"   Suggested destination: {destination}")
        
        else:
            print("\n5. Low confidence - waiting for more signals")
    
    elif result['status'] == 'duplicate':
        print(f"   ⚠️  {result['message']}")
    
    # Step 4: Show stats
    print("\n" + "="*80)
    print("SYSTEM STATS")
    print("="*80)
    stats = index.get_stats()
    print(f"Total files: {stats['total']}")
    print(f"Unattributed: {stats['unattributed']}")
    print(f"Attributed: {stats['attributed']}")
    
    print("\nDecay report:")
    decay_report = decay.get_decay_report()
    for stage, count in decay_report.items():
        print(f"  {stage}: {count} files")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)


if __name__ == '__main__':
    test_complete_flow()
