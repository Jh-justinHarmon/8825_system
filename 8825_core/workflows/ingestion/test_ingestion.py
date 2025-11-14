#!/usr/bin/env python3
"""
Test Ingestion Script
Process files in the ingestion folder
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from ingestion_engine import IngestionEngine

def main():
    """Test ingestion on real files"""
    
    print("=" * 60)
    print("🚀 8825 INGESTION ENGINE - TEST RUN")
    print("=" * 60)
    print()
    
    # Initialize engine
    engine = IngestionEngine()
    
    # Scan ingestion folder
    print("🔍 Scanning ingestion folder...")
    print()
    
    engine.scan_ingestion_folder()
    
    print()
    print("=" * 60)
    print("✅ SCAN COMPLETE")
    print("=" * 60)
    print()
    
    # Show stats
    stats = engine.tracker.get_stats()
    print(f"📊 Statistics:")
    print(f"   Processed: {stats['total_processed']}")
    print(f"   In Queue: {stats['in_queue']}")
    print(f"   Failed: {stats['failed']}")
    print()
    
    # Show sample results
    print("📋 Sample Results:")
    processed_data = engine.tracker._load_json(engine.tracker.processed_file)
    
    for i, item in enumerate(processed_data.get("processed", [])[:5], 1):
        print(f"\n{i}. {item.get('filename')}")
        print(f"   Project: {item.get('classification', {}).get('project')}")
        print(f"   Confidence: {item.get('classification', {}).get('confidence')}%")
        print(f"   Category: {item.get('classification', {}).get('category')}")
        
        routing = item.get('routing', {})
        if routing.get('success'):
            dests = routing.get('destinations', [])
            if dests:
                print(f"   Routed to: {dests[0]}")
        
        library = item.get('library', {})
        if library.get('merged'):
            print(f"   Library: {library.get('library')} ({library.get('action')})")


if __name__ == "__main__":
    main()
