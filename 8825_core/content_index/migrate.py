#!/usr/bin/env python3
"""
Migration Script
Migrate existing teaching tickets and Lane B files to content index
"""

import sys
from pathlib import Path
from glob import glob
import json
import shutil

from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker


def migrate_teaching_tickets(inbox_path: Path, index: ContentIndexEngine):
    """Migrate teaching tickets to content index"""
    
    tickets_path = inbox_path / 'processing' / 'teaching_tickets'
    
    if not tickets_path.exists():
        print("No teaching tickets found")
        return 0
    
    tickets = list(tickets_path.glob('*.md'))
    
    print(f"Found {len(tickets)} teaching tickets")
    
    migrated = 0
    
    for ticket in tickets:
        try:
            # Read ticket to find original file
            content = ticket.read_text()
            
            # Extract source file path from ticket
            # Format: **Source File:** /path/to/file
            import re
            match = re.search(r'\*\*Source File:\*\* (.+)', content)
            
            if not match:
                print(f"  ⚠️  Could not find source file in {ticket.name}")
                continue
            
            source_path = Path(match.group(1).strip())
            
            if not source_path.exists():
                print(f"  ⚠️  Source file not found: {source_path}")
                continue
            
            # Ingest to content index
            result = index.ingest(source_path)
            
            if result['status'] in ['indexed', 'duplicate']:
                # Archive ticket
                archive_path = inbox_path / 'archived_tickets'
                archive_path.mkdir(exist_ok=True)
                shutil.move(ticket, archive_path / ticket.name)
                
                # Also archive JSON if exists
                json_ticket = ticket.with_suffix('.json')
                if json_ticket.exists():
                    shutil.move(json_ticket, archive_path / json_ticket.name)
                
                migrated += 1
                print(f"  ✅ Migrated: {source_path.name}")
            
        except Exception as e:
            print(f"  ❌ Error migrating {ticket.name}: {e}")
    
    return migrated


def migrate_lane_b_files(inbox_path: Path, index: ContentIndexEngine):
    """Migrate Lane B files to content index"""
    
    lane_b_path = inbox_path / 'processing' / 'lane_b'
    
    if not lane_b_path.exists():
        print("No Lane B files found")
        return 0
    
    files = list(lane_b_path.glob('*'))
    files = [f for f in files if f.is_file() and not f.name.startswith('.')]
    
    print(f"Found {len(files)} Lane B files")
    
    migrated = 0
    
    for file in files:
        try:
            result = index.ingest(file)
            
            if result['status'] in ['indexed', 'duplicate']:
                migrated += 1
                print(f"  ✅ Indexed: {file.name}")
            
        except Exception as e:
            print(f"  ❌ Error indexing {file.name}: {e}")
    
    return migrated


def cleanup_lane_a_pollution(system_root: Path, index: ContentIndexEngine):
    """Clean up Lane A file naming bug"""
    
    personal_path = system_root / 'users' / 'justinharmon' / 'personal'
    
    if not personal_path.exists():
        print("Personal folder not found")
        return 0
    
    # Find files with naming bug pattern
    broken_files = list(personal_path.glob('*_1_2_3_*.md'))
    
    if not broken_files:
        print("No broken files found")
        return 0
    
    print(f"Found {len(broken_files)} files with naming bug")
    
    seen_hashes = set()
    cleaned = 0
    
    for file in broken_files:
        try:
            content = file.read_bytes()
            file_hash = index.calculate_hash(content)
            
            if file_hash in seen_hashes:
                # Duplicate - delete
                file.unlink()
                cleaned += 1
                print(f"  🗑️  Deleted duplicate: {file.name}")
            else:
                # First occurrence - index
                result = index.ingest(file)
                seen_hashes.add(file_hash)
                
                if result['status'] == 'indexed':
                    print(f"  ✅ Indexed: {file.name}")
                
        except Exception as e:
            print(f"  ❌ Error processing {file.name}: {e}")
    
    return cleaned


def main():
    print("="*80)
    print("CONTENT INDEX MIGRATION")
    print("="*80)
    
    # Initialize
    inbox_path = Path.home() / 'Downloads' / '8825_inbox'
    system_root = Path(__file__).parent.parent.parent
    
    index = ContentIndexEngine(inbox_path / 'content_index')
    
    print(f"\nInbox: {inbox_path}")
    print(f"System: {system_root}")
    print(f"Index: {index.index_root}")
    
    # Migrate teaching tickets
    print("\n" + "="*80)
    print("MIGRATING TEACHING TICKETS")
    print("="*80)
    migrated_tickets = migrate_teaching_tickets(inbox_path, index)
    print(f"\n✅ Migrated {migrated_tickets} teaching tickets")
    
    # Migrate Lane B files
    print("\n" + "="*80)
    print("MIGRATING LANE B FILES")
    print("="*80)
    migrated_lane_b = migrate_lane_b_files(inbox_path, index)
    print(f"\n✅ Indexed {migrated_lane_b} Lane B files")
    
    # Cleanup Lane A pollution
    print("\n" + "="*80)
    print("CLEANING UP LANE A POLLUTION")
    print("="*80)
    cleaned = cleanup_lane_a_pollution(system_root, index)
    print(f"\n✅ Cleaned {cleaned} duplicate files")
    
    # Final stats
    print("\n" + "="*80)
    print("MIGRATION COMPLETE")
    print("="*80)
    stats = index.get_stats()
    print(f"\nIndex Stats:")
    print(f"  Total files: {stats['total']}")
    print(f"  Unattributed: {stats['unattributed']}")
    print(f"  Attributed: {stats['attributed']}")
    
    print("\nNext steps:")
    print("  1. Test search: python search_cli.py 'RAL Portal'")
    print("  2. Check promotions: python promotion_engine.py")
    print("  3. Run cleanup: python cleanup_engine.py")


if __name__ == '__main__':
    main()
