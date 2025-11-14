#!/usr/bin/env python3
"""
Test immediate cleanup of attributed files
"""

from index_engine import ContentIndexEngine
from cleanup_engine import CleanupEngine

print("Testing cleanup of attributed files...")

index = ContentIndexEngine()
cleanup = CleanupEngine(index.db_path, index.store_path)

# Find attributed files
attributed = index.db.execute('''
    SELECT hash, filename, attributed, destination 
    FROM files 
    WHERE attributed = 1
''').fetchall()

print(f"\nFound {len(attributed)} attributed files")

for file in attributed:
    print(f"  - {file['filename']}")
    print(f"    Destination: {file['destination']}")
    
    # Check if content_store file exists
    store_files = list(index.store_path.glob(f"{file['hash']}*"))
    if store_files:
        print(f"    ⚠️  Still in content_store: {store_files[0].name}")
    else:
        print(f"    ✅ Cleaned from content_store")

print("\n" + "="*80)
print("Running cleanup...")
stats = cleanup.daily_cleanup(dry_run=False)

print(f"\nCleanup complete:")
print(f"  Deleted: {stats['deleted']}")
print(f"  Archived: {stats['archived']}")
print(f"  Review: {stats['review']}")
