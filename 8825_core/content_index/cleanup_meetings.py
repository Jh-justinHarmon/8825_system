#!/usr/bin/env python3
"""
Clean up meeting notes from index
"""

import json
from pathlib import Path
from index_engine import ContentIndexEngine

index = ContentIndexEngine()

# Find meeting-related files
meeting_files = []

all_files = index.db.execute('SELECT * FROM files').fetchall()

for file in all_files:
    filename = file['filename'].lower()
    
    # Check if it's a meeting file
    if any(term in filename for term in ['meeting', 'notes', 'sync', 'call', 'touchbase', 'user testing', 'user test']):
        meeting_files.append(dict(file))

print(f'Found {len(meeting_files)} meeting-related files')
print('\nDeleting from index and content_store...')

deleted = 0
for f in meeting_files:
    # Delete from content_store
    store_files = list(index.store_path.glob(f"{f['hash']}*"))
    for store_file in store_files:
        store_file.unlink()
        print(f"  Deleted: {store_file.name}")
    
    # Delete from database
    index.db.execute('DELETE FROM files WHERE hash = ?', (f['hash'],))
    deleted += 1

index.db.commit()

print(f'\n✅ Deleted {deleted} meeting files')
print(f'\nRemaining files: {index.get_stats()["total"]}')
