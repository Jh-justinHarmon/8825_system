#!/usr/bin/env python3
"""
Analogy Generator - Inspired by "It's This for That"
Rapidly generates and collects useful analogies for brainstorming
"""

import requests
import time
import json
from pathlib import Path

# Output file
OUTPUT_FILE = Path(__file__).parent / "collected_analogies.json"

def fetch_analogy():
    """Fetch a random analogy from itsthisforthat.com"""
    try:
        response = requests.get("https://itsthisforthat.com/api.php?json", timeout=5)
        data = response.json()
        
        this = data.get('this', '')
        that = data.get('that', '')
        
        return {
            'this': this,
            'that': that,
            'phrase': f"It's like {this} for {that}",
            'timestamp': time.time()
        }
    except Exception as e:
        print(f"Error fetching: {e}")
        return None

def load_collected():
    """Load previously collected analogies"""
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            return json.load(f)
    return []

def save_collected(analogies):
    """Save collected analogies"""
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(analogies, f, indent=2)

def interactive_mode():
    """Interactive mode - cycle through and collect"""
    print("\n🎯 ANALOGY GENERATOR")
    print("=" * 60)
    print("\nCommands:")
    print("  [ENTER]  - Get next analogy")
    print("  s        - Save this one")
    print("  l        - List saved analogies")
    print("  q        - Quit")
    print("=" * 60 + "\n")
    
    collected = load_collected()
    current = None
    count = 0
    
    while True:
        # Get new analogy
        current = fetch_analogy()
        if not current:
            print("❌ Failed to fetch analogy")
            time.sleep(1)
            continue
        
        count += 1
        
        # Display
        print(f"\n[{count}] 💡 {current['phrase']}")
        print(f"    This: {current['this']}")
        print(f"    That: {current['that']}")
        
        # Get input
        choice = input("\n> ").strip().lower()
        
        if choice == 'q':
            print(f"\n✅ Generated {count} analogies")
            print(f"✅ Saved {len(collected)} analogies")
            break
        elif choice == 's':
            collected.append(current)
            save_collected(collected)
            print(f"✅ Saved! ({len(collected)} total)")
        elif choice == 'l':
            print(f"\n📚 SAVED ANALOGIES ({len(collected)}):")
            for i, a in enumerate(collected, 1):
                print(f"  {i}. {a['phrase']}")
            input("\nPress ENTER to continue...")
        # else: just continue (ENTER pressed)

def batch_mode(count=50):
    """Batch mode - generate many at once"""
    print(f"\n🎯 Generating {count} analogies...")
    print("=" * 60 + "\n")
    
    analogies = []
    
    for i in range(count):
        analogy = fetch_analogy()
        if analogy:
            analogies.append(analogy)
            print(f"[{i+1}/{count}] {analogy['phrase']}")
        time.sleep(0.5)  # Be nice to their server
    
    # Save to file
    output = Path(__file__).parent / f"analogies_batch_{int(time.time())}.json"
    with open(output, 'w') as f:
        json.dump(analogies, f, indent=2)
    
    print(f"\n✅ Generated {len(analogies)} analogies")
    print(f"✅ Saved to: {output}")
    
    return analogies

def search_mode(keyword):
    """Search mode - find analogies containing keyword"""
    print(f"\n🔍 Searching for analogies with '{keyword}'...")
    print("=" * 60 + "\n")
    
    found = []
    attempts = 0
    max_attempts = 200
    
    while len(found) < 10 and attempts < max_attempts:
        analogy = fetch_analogy()
        attempts += 1
        
        if analogy:
            text = f"{analogy['this']} {analogy['that']}".lower()
            if keyword.lower() in text:
                found.append(analogy)
                print(f"[{len(found)}] {analogy['phrase']}")
        
        time.sleep(0.3)
    
    print(f"\n✅ Found {len(found)} matches in {attempts} attempts")
    
    if found:
        save = input("\nSave these? (y/n): ").strip().lower()
        if save == 'y':
            collected = load_collected()
            collected.extend(found)
            save_collected(collected)
            print(f"✅ Saved {len(found)} analogies")
    
    return found

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'batch':
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            batch_mode(count)
        elif command == 'search':
            keyword = sys.argv[2] if len(sys.argv) > 2 else 'ai'
            search_mode(keyword)
        elif command == 'list':
            collected = load_collected()
            print(f"\n📚 SAVED ANALOGIES ({len(collected)}):")
            for i, a in enumerate(collected, 1):
                print(f"  {i}. {a['phrase']}")
        else:
            print("Unknown command. Use: interactive, batch [count], search [keyword], or list")
    else:
        interactive_mode()
