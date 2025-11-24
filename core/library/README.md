# 8825 Library System

A lightweight SQLite-based knowledge management system for AI-assisted workflows.

## Overview

The Library provides structured storage for:
- **Knowledge** - Facts, concepts, learnings
- **Decisions** - Choices made and rationale
- **Patterns** - Reusable solutions
- **Achievements** - Milestones and wins
- **ALS Runs** - Agentic Learning System executions

## Quick Start

```bash
# Initialize database
sqlite3 library.db < schema/init_library_db.sql

# Use the library
python examples/demo_library.py
```

## Schema

See `schema/init_library_db.sql` for complete database structure.

**Core tables**:
- `library_entries` - Main knowledge entries
- `entry_relationships` - Links between entries
- `tags` - Categorization
- `protocols` - Referenced protocols

## Usage

### Python

```python
import sqlite3

# Connect
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Insert knowledge
cursor.execute("""
    INSERT INTO library_entries (entry_id, entry_type, title, content, confidence)
    VALUES (?, ?, ?, ?, ?)
""", ('K-001', 'knowledge', 'Example', 'Content here', 0.9))

# Query
cursor.execute("SELECT * FROM library_entries WHERE entry_type = 'knowledge'")
results = cursor.fetchall()

conn.commit()
conn.close()
```

### CLI

```bash
# Search
sqlite3 library.db "SELECT title FROM library_entries WHERE content LIKE '%search%'"

# Export
sqlite3 library.db ".mode json" ".output export.json" "SELECT * FROM library_entries"
```

## Integration

The Library integrates with:
- **DLI Router** - Provides context for deep dives
- **Pattern Engine** - Stores extracted patterns
- **Memory Assimilator** - Imports external learnings
- **ALS** - Tracks learning iterations

## Architecture

```
library.db (SQLite)
├── library_entries     # Core knowledge
├── entry_relationships # Graph structure
├── tags               # Categorization
└── protocols          # Protocol references
```

## Examples

See `examples/` for:
- `demo_library.py` - Basic CRUD operations
- `search_example.py` - Full-text search
- `graph_example.py` - Relationship queries

## Documentation

- `docs/SCHEMA.md` - Database design details
- `docs/INTEGRATION.md` - How to integrate with your system

## License

MIT
