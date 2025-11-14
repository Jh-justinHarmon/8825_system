#!/usr/bin/env python3
"""
Test with a brand new file
"""

import os
from pathlib import Path

# API key should be set in environment (OPENAI_API_KEY)
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError('OPENAI_API_KEY environment variable not set')

from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine

# Create test file
test_content = '''# RAL Portal OAuth 2.0 Implementation Guide

This document describes the OAuth 2.0 authentication flow for the RAL Portal API.

## Overview
The RAL Portal uses OAuth 2.0 for secure API authentication.

## Flow Steps
1. Request authorization token
2. Exchange for access token  
3. Use access token in API requests
4. Refresh token when expired

## Implementation Details
- Token endpoint: /oauth/token
- Authorization endpoint: /oauth/authorize
- Scopes: read, write, admin
'''

test_file = Path('/tmp/crunchtime_meeting_notes.md')
if not test_file.exists():
    test_file.write_text(test_content)

print("="*80)
print("TESTING NEW FILE")
print("="*80)

# Initialize
index = ContentIndexEngine()
tracker = UsageTracker(index.db_path)
promotion = PromotionEngine(index.db_path, index.store_path, tracker)

# Ingest
print(f"\n1. Ingesting: {test_file.name}")
result = index.ingest(test_file, use_intelligent_naming=True)

print(f"\n2. Result:")
print(f"   Status: {result['status']}")

if result['status'] == 'indexed':
    print(f"   Hash: {result['hash']}")
    print(f"   Filename: {result['metadata']['filename']}")
    
    if 'intelligent_metadata' in result:
        intel = result['intelligent_metadata']
        print(f"\n3. Intelligent Analysis:")
        print(f"   Category: {intel['category']}")
        print(f"   Topic: {intel['main_topic']}")
        print(f"   Entities: {intel['entities']}")
        print(f"   Destination: {intel['destination']}")
    
    # Check confidence
    print(f"\n4. Promotion Check:")
    confidence = promotion.calculate_confidence(result['hash'])
    print(f"   Confidence: {confidence:.2f}")
    
    if confidence >= 0.70:
        destination = promotion.suggest_destination(result['hash'])
        print(f"   Suggested: {destination}")
        
        # Try to promote
        print(f"\n5. Attempting promotion...")
        promo_result = promotion.promote_file(result['hash'], destination, check_merge=True)
        
        print(f"   Status: {promo_result['status']}")
        if 'destination' in promo_result:
            print(f"   Destination: {promo_result['destination']}")
        if 'action' in promo_result:
            print(f"   Action: {promo_result['action']}")

print("\n" + "="*80)
