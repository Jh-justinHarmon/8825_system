#!/usr/bin/env python3
"""
Demo Library - Basic CRUD Operations
Demonstrates how to use the 8825 Library system
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

def init_database(db_path='demo_library.db'):
    """Initialize a new library database"""
    # Get schema path relative to this file
    current_dir = Path(__file__).parent
    schema_path = current_dir.parent / 'schema' / 'init_library_db.sql'
    
    if not schema_path.exists():
        print(f"❌ Schema not found at: {schema_path}")
        print(f"   Current directory: {current_dir}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    conn = sqlite3.connect(db_path)
    
    with open(schema_path, 'r') as f:
        schema = f.read()
        conn.executescript(schema)
    
    print(f"✅ Database initialized: {db_path}")
    return conn

def insert_knowledge(conn, entry_id, title, content, confidence=0.9):
    """Insert a knowledge entry"""
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO library_entries (
            entry_id, entry_type, title, content, 
            confidence, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entry_id, 'knowledge', title, content,
        confidence, datetime.now().isoformat(), datetime.now().isoformat()
    ))
    
    conn.commit()
    print(f"✅ Inserted: {entry_id} - {title}")

def insert_decision(conn, entry_id, title, content, rationale):
    """Insert a decision entry"""
    cursor = conn.cursor()
    
    metadata = json.dumps({'rationale': rationale})
    
    cursor.execute("""
        INSERT INTO library_entries (
            entry_id, entry_type, title, content, 
            metadata, confidence, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry_id, 'decision', title, content,
        metadata, 1.0, datetime.now().isoformat(), datetime.now().isoformat()
    ))
    
    conn.commit()
    print(f"✅ Inserted: {entry_id} - {title}")

def add_tag(conn, entry_id, tag):
    """Add a tag to an entry"""
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tags (entry_id, tag) VALUES (?, ?)
    """, (entry_id, tag))
    
    conn.commit()
    print(f"✅ Tagged {entry_id} with: {tag}")

def link_entries(conn, from_id, to_id, relationship_type='relates_to'):
    """Create a relationship between entries"""
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO entry_relationships (from_entry_id, to_entry_id, relationship_type, created_at)
        VALUES (?, ?, ?, ?)
    """, (from_id, to_id, relationship_type, datetime.now().isoformat()))
    
    conn.commit()
    print(f"✅ Linked {from_id} → {to_id} ({relationship_type})")

def search_entries(conn, search_term):
    """Search for entries"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT entry_id, entry_type, title, content
        FROM library_entries
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY created_at DESC
    """, (f'%{search_term}%', f'%{search_term}%'))
    
    results = cursor.fetchall()
    
    print(f"\n🔍 Search results for '{search_term}':")
    for entry_id, entry_type, title, content in results:
        print(f"  [{entry_type}] {entry_id}: {title}")
        print(f"    {content[:100]}...")
    
    return results

def get_related_entries(conn, entry_id):
    """Get entries related to this one"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            e.entry_id, e.entry_type, e.title, r.relationship_type
        FROM entry_relationships r
        JOIN library_entries e ON r.to_entry_id = e.entry_id
        WHERE r.from_entry_id = ?
    """, (entry_id,))
    
    results = cursor.fetchall()
    
    print(f"\n🔗 Entries related to {entry_id}:")
    for rel_id, rel_type, title, rel_kind in results:
        print(f"  [{rel_type}] {rel_id}: {title} ({rel_kind})")
    
    return results

def export_to_json(conn, output_file='library_export.json'):
    """Export all entries to JSON"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM library_entries")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    entries = [dict(zip(columns, row)) for row in rows]
    
    with open(output_file, 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"✅ Exported {len(entries)} entries to {output_file}")

def main():
    """Demo workflow"""
    print("=" * 60)
    print("8825 Library Demo")
    print("=" * 60)
    print()
    
    # Initialize
    conn = init_database()
    print()
    
    # Insert some knowledge
    print("Adding knowledge entries...")
    insert_knowledge(
        conn, 'K-001', 
        'DLI Routing Pattern',
        'Three-tier routing: Pattern matching (FREE) → Cheap model → Expensive model. Optimizes cost while maintaining quality.',
        confidence=0.95
    )
    
    insert_knowledge(
        conn, 'K-002',
        'Universal Inbox Pattern',
        'Single entry point for all file types. Watch directory → Classify → Route to appropriate handler.',
        confidence=0.9
    )
    
    insert_knowledge(
        conn, 'K-003',
        'Library System',
        'SQLite-based knowledge management. Stores knowledge, decisions, patterns, achievements, and ALS runs.',
        confidence=1.0
    )
    print()
    
    # Insert a decision
    print("Adding decision entry...")
    insert_decision(
        conn, 'D-001',
        'Use SQLite for Library',
        'Chose SQLite over PostgreSQL for library storage.',
        rationale='Lightweight, no server needed, perfect for local-first architecture. Easy to backup and sync.'
    )
    print()
    
    # Add tags
    print("Adding tags...")
    add_tag(conn, 'K-001', 'dli')
    add_tag(conn, 'K-001', 'routing')
    add_tag(conn, 'K-001', 'cost-optimization')
    add_tag(conn, 'K-002', 'inbox')
    add_tag(conn, 'K-002', 'automation')
    add_tag(conn, 'K-003', 'library')
    add_tag(conn, 'D-001', 'architecture')
    print()
    
    # Link entries
    print("Creating relationships...")
    link_entries(conn, 'K-003', 'D-001', 'implements')
    link_entries(conn, 'K-001', 'K-002', 'relates_to')
    print()
    
    # Search
    search_entries(conn, 'routing')
    print()
    
    # Get related
    get_related_entries(conn, 'K-003')
    print()
    
    # Export
    export_to_json(conn)
    print()
    
    # Stats
    cursor = conn.cursor()
    cursor.execute("SELECT entry_type, COUNT(*) FROM library_entries GROUP BY entry_type")
    stats = cursor.fetchall()
    
    print("📊 Library Statistics:")
    for entry_type, count in stats:
        print(f"  {entry_type}: {count}")
    print()
    
    conn.close()
    
    print("=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)
    print()
    print("Database: demo_library.db")
    print("Export: library_export.json")
    print()
    print("Try:")
    print("  sqlite3 demo_library.db 'SELECT * FROM library_entries'")
    print("  cat library_export.json")

if __name__ == '__main__':
    main()
