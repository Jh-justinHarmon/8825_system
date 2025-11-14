#!/usr/bin/env python3
"""
Search CLI
Interactive command-line interface for content index
"""

import sys
from pathlib import Path
from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine


def print_result(index: int, result: dict, full: bool = False):
    """Print search result"""
    
    print(f"\n{index + 1}. {result['filename']} ({result['size']} bytes)")
    
    if result['attributed']:
        print(f"   ✅ Attributed: {result['destination']}")
    else:
        print(f"   ⚪ Unattributed")
    
    # Show summary
    print(f"   {result['summary'][:200]}...")
    
    # Show keywords/entities
    import json
    keywords = json.loads(result['keywords'])
    entities = json.loads(result['entities'])
    
    if entities:
        print(f"   Entities: {', '.join(entities)}")
    if keywords:
        print(f"   Keywords: {', '.join(keywords[:5])}")
    
    # Show access info
    if result['access_count'] > 0:
        print(f"   Accessed: {result['access_count']} times")
    
    # Show decay info
    if not result['attributed']:
        decay_stages = {0: 'fresh', 1: 'aging', 2: 'stale', 3: 'expired'}
        stage = decay_stages.get(result['decay_score'], 'expired')
        print(f"   Decay: {stage}")
    
    print(f"   [v]iew full  [a]ttribute  [i]nvestigate  [d]elete")


def view_full(engine: ContentIndexEngine, file_hash: str):
    """View full content"""
    content = engine.get_full_content(file_hash)
    
    if not content:
        print("❌ Content not found")
        return
    
    try:
        text = content.decode('utf-8', errors='ignore')
        print("\n" + "="*80)
        print(text)
        print("="*80)
    except:
        print(f"❌ Cannot display binary content ({len(content)} bytes)")


def attribute_file(engine: ContentIndexEngine, promotion: PromotionEngine, file_hash: str):
    """Attribute file to destination"""
    
    # Get suggestion
    suggestion = promotion.suggest_destination(file_hash)
    confidence = promotion.calculate_confidence(file_hash)
    
    print(f"\nConfidence: {confidence:.2f}")
    if suggestion:
        print(f"Suggested: {suggestion}")
    
    destination = input("Destination (or Enter for suggestion): ").strip()
    
    if not destination and suggestion:
        destination = suggestion
    
    if not destination:
        print("❌ No destination specified")
        return
    
    success = promotion.promote_file(file_hash, destination)
    
    if success:
        print(f"✅ Promoted to {destination}")
    else:
        print("❌ Promotion failed")


def investigate(engine: ContentIndexEngine, file_hash: str):
    """Deep investigation of file"""
    
    metadata = engine.get_metadata(file_hash)
    if not metadata:
        print("❌ File not found")
        return
    
    print("\n" + "="*80)
    print("FULL METADATA")
    print("="*80)
    
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
    # Find similar files
    similar = engine.find_similar(file_hash)
    
    if similar:
        print(f"\nSIMILAR FILES ({len(similar)}):")
        for s in similar:
            status = "✅ Attributed" if s['attributed'] else "⚪ Unattributed"
            print(f"  - {s['filename']} ({status})")


def search_interactive(query: str):
    """Interactive search interface"""
    
    # Initialize engines
    engine = ContentIndexEngine()
    tracker = UsageTracker(engine.db_path)
    promotion = PromotionEngine(engine.db_path, engine.store_path, tracker)
    
    # Search
    results = engine.search(query)
    
    if not results:
        print(f"No results found for '{query}'")
        return
    
    print(f"\nFound {len(results)} results:\n")
    
    # Show results
    for i, result in enumerate(results):
        print_result(i, result)
    
    # Interactive commands
    while True:
        cmd = input("\nCommand (number + action, or q to quit): ").strip().lower()
        
        if cmd == 'q' or cmd == 'quit':
            break
        
        # Parse command (e.g., "1v" = view file 1)
        if len(cmd) >= 2:
            try:
                index = int(cmd[0]) - 1
                action = cmd[1]
                
                if index < 0 or index >= len(results):
                    print("❌ Invalid index")
                    continue
                
                file_hash = results[index]['hash']
                
                if action == 'v':
                    view_full(engine, file_hash)
                elif action == 'a':
                    attribute_file(engine, promotion, file_hash)
                elif action == 'i':
                    investigate(engine, file_hash)
                elif action == 'd':
                    confirm = input("Delete? (yes/no): ")
                    if confirm.lower() == 'yes':
                        # TODO: Add delete functionality
                        print("Delete not yet implemented")
                else:
                    print("❌ Unknown action")
            except ValueError:
                print("❌ Invalid command format")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python search_cli.py <query>")
        print("Example: python search_cli.py 'RAL Portal'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    search_interactive(query)
