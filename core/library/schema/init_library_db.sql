-- 8825 Library Database Schema
-- SQLite database for knowledge, decisions, patterns, achievements, and ALS runs

-- Unified Library Entries Table
CREATE TABLE IF NOT EXISTS library_entries (
    entry_id TEXT PRIMARY KEY,
    entry_type TEXT NOT NULL CHECK(entry_type IN ('knowledge', 'decision', 'pattern', 'achievement', 'als')),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT, -- JSON object stored as text
    confidence REAL CHECK(confidence >= 0 AND confidence <= 1),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_entry_type ON library_entries(entry_type);
CREATE INDEX IF NOT EXISTS idx_entry_created ON library_entries(created_at);
CREATE INDEX IF NOT EXISTS idx_entry_confidence ON library_entries(confidence);

-- Tags Table
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES library_entries(entry_id) ON DELETE CASCADE,
    UNIQUE(entry_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_tags_entry ON tags(entry_id);
CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag);

-- Entry Relationships
CREATE TABLE IF NOT EXISTS entry_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entry_id TEXT NOT NULL,
    to_entry_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (from_entry_id) REFERENCES library_entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (to_entry_id) REFERENCES library_entries(entry_id) ON DELETE CASCADE,
    UNIQUE(from_entry_id, to_entry_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_rel_from ON entry_relationships(from_entry_id);
CREATE INDEX IF NOT EXISTS idx_rel_to ON entry_relationships(to_entry_id);
CREATE INDEX IF NOT EXISTS idx_rel_type ON entry_relationships(relationship_type);

-- Protocols Table (optional - for protocol references)
CREATE TABLE IF NOT EXISTS protocols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id TEXT NOT NULL,
    protocol_name TEXT NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES library_entries(entry_id) ON DELETE CASCADE,
    UNIQUE(entry_id, protocol_name)
);

CREATE INDEX IF NOT EXISTS idx_protocols_entry ON protocols(entry_id);
CREATE INDEX IF NOT EXISTS idx_protocols_name ON protocols(protocol_name);

-- Metadata table for library versioning
CREATE TABLE IF NOT EXISTS library_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT OR REPLACE INTO library_metadata (key, value) VALUES ('schema_version', '2.0.0');
INSERT OR REPLACE INTO library_metadata (key, value) VALUES ('created_at', datetime('now'));
