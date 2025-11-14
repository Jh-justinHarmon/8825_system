#!/usr/bin/env python3
"""
Content Index Engine
Core indexing system with SQLite + FTS5
"""

import os
import json
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import shutil
import sys


class ContentIndexEngine:
    """
    Content-addressed index with full-text search
    
    Features:
    - Hash-based deduplication
    - FTS5 full-text search
    - Metadata extraction (no LLM)
    - Fast search (< 50ms)
    - Progressive disclosure (summary → full content)
    """
    
    def __init__(self, index_root: Optional[Path] = None):
        if index_root is None:
            index_root = Path.home() / 'Downloads' / '8825_inbox' / 'content_index'
        
        self.index_root = Path(index_root)
        self.db_path = self.index_root / 'index.db'
        self.store_path = self.index_root / 'content_store'
        
        # Ensure directories exist
        self.index_root.mkdir(parents=True, exist_ok=True)
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.db = sqlite3.connect(str(self.db_path))
        self.db.row_factory = sqlite3.Row
        self._init_database()
    
    def _init_database(self):
        """Create database schema"""
        self.db.executescript('''
            -- Main files table
            CREATE TABLE IF NOT EXISTS files (
                hash TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_type TEXT,
                size INTEGER,
                summary TEXT,
                keywords TEXT,
                entities TEXT,
                created DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_accessed DATETIME,
                access_count INTEGER DEFAULT 0,
                attributed BOOLEAN DEFAULT 0,
                destination TEXT,
                promoted_date DATETIME,
                archived BOOLEAN DEFAULT 0,
                archived_date DATETIME,
                decay_score INTEGER DEFAULT 0
            );
            
            -- FTS5 full-text search
            CREATE VIRTUAL TABLE IF NOT EXISTS files_fts USING fts5(
                filename,
                summary,
                keywords,
                entities,
                content=files,
                content_rowid=rowid
            );
            
            -- Triggers to keep FTS in sync
            CREATE TRIGGER IF NOT EXISTS files_ai AFTER INSERT ON files BEGIN
                INSERT INTO files_fts(rowid, filename, summary, keywords, entities)
                VALUES (new.rowid, new.filename, new.summary, new.keywords, new.entities);
            END;
            
            CREATE TRIGGER IF NOT EXISTS files_ad AFTER DELETE ON files BEGIN
                DELETE FROM files_fts WHERE rowid = old.rowid;
            END;
            
            CREATE TRIGGER IF NOT EXISTS files_au AFTER UPDATE ON files BEGIN
                UPDATE files_fts 
                SET filename = new.filename,
                    summary = new.summary,
                    keywords = new.keywords,
                    entities = new.entities
                WHERE rowid = new.rowid;
            END;
            
            -- Indexes
            CREATE INDEX IF NOT EXISTS idx_files_created ON files(created DESC);
            CREATE INDEX IF NOT EXISTS idx_files_attributed ON files(attributed);
            CREATE INDEX IF NOT EXISTS idx_files_decay ON files(decay_score);
        ''')
        self.db.commit()
    
    def calculate_hash(self, content: bytes) -> str:
        """Calculate SHA256 hash of content"""
        return hashlib.sha256(content).hexdigest()
    
    def extract_metadata(self, file_path: Path, content: bytes) -> Dict[str, Any]:
        """
        Extract metadata without LLM
        - Keywords (frequency analysis)
        - Entities (pattern matching)
        - File type detection
        """
        
        # Decode content
        try:
            text = content.decode('utf-8', errors='ignore')
        except:
            text = str(content)
        
        # Extract keywords (simple frequency)
        keywords = self._extract_keywords(text)
        
        # Extract entities (pattern matching)
        entities = self._extract_entities(text)
        
        # Summary (first 500 chars)
        summary = text[:500].strip()
        
        return {
            'filename': file_path.name,
            'file_type': file_path.suffix.lower(),
            'size': len(content),
            'summary': summary,
            'keywords': json.dumps(keywords),
            'entities': json.dumps(entities)
        }
    
    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract top keywords by frequency"""
        # Simple word frequency
        words = text.lower().split()
        
        # Filter common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = [w for w in words if len(w) > 3 and w not in stopwords]
        
        # Count frequency
        from collections import Counter
        freq = Counter(words)
        
        return [word for word, count in freq.most_common(top_n)]
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities using pattern matching"""
        import re
        
        entities = []
        
        # Known entity patterns
        patterns = {
            'RAL Portal': r'RAL\s+Portal',
            'HCSS': r'HCSS',
            'Crunchtime': r'Crunchtime',
            'Joju': r'Joju',
            'Team76': r'Team\s*76',
            'OAuth': r'OAuth',
            'API': r'\bAPI\b',
            'Database': r'Database|database',
            'ERD': r'\bERD\b'
        }
        
        for entity, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                entities.append(entity)
        
        return entities
    
    def ingest(self, file_path: Path, use_intelligent_naming: bool = True) -> Dict[str, Any]:
        """
        Ingest file into index
        
        Args:
            file_path: Path to file
            use_intelligent_naming: Use LLM to generate intelligent filename
        
        Returns:
            dict with hash, status, metadata
        """
        
        # Read file content
        content = file_path.read_bytes()
        
        # Calculate hash
        file_hash = self.calculate_hash(content)
        
        # Check if already exists
        existing = self.db.execute(
            'SELECT hash FROM files WHERE hash = ?',
            (file_hash,)
        ).fetchone()
        
        if existing:
            return {
                'status': 'duplicate',
                'hash': file_hash,
                'message': 'File already indexed (duplicate content)'
            }
        
        # Use intelligent naming if enabled
        if use_intelligent_naming:
            try:
                from intelligent_naming import IntelligentNamingEngine
                naming_engine = IntelligentNamingEngine()
                intelligent_metadata = naming_engine.analyze_and_name(file_path, content)
                
                # Use intelligent filename
                filename = intelligent_metadata['suggested_filename']
                
                # Add intelligent metadata to keywords/entities
                entities_list = intelligent_metadata.get('entities', [])
                
            except Exception as e:
                print(f"Intelligent naming failed: {e}, using fallback")
                filename = file_path.name
                intelligent_metadata = None
                entities_list = []
        else:
            filename = file_path.name
            intelligent_metadata = None
            entities_list = []
        
        # Extract basic metadata
        metadata = self.extract_metadata(file_path, content)
        
        # Override with intelligent filename
        metadata['filename'] = filename
        
        # Merge entities
        if entities_list:
            existing_entities = json.loads(metadata['entities'])
            all_entities = list(set(existing_entities + entities_list))
            metadata['entities'] = json.dumps(all_entities)
        
        # Store full content with intelligent name
        store_file = self.store_path / f"{file_hash}{metadata['file_type']}"
        store_file.write_bytes(content)
        
        # Insert into database
        self.db.execute('''
            INSERT INTO files (hash, filename, file_type, size, summary, keywords, entities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            file_hash,
            metadata['filename'],
            metadata['file_type'],
            metadata['size'],
            metadata['summary'],
            metadata['keywords'],
            metadata['entities']
        ))
        self.db.commit()
        
        result = {
            'status': 'indexed',
            'hash': file_hash,
            'metadata': metadata,
            'searchable': True
        }
        
        # Add intelligent metadata if available
        if intelligent_metadata:
            result['intelligent_metadata'] = intelligent_metadata
        
        return result
    
    def search(self, query: str, attributed: Optional[bool] = None, limit: int = 20) -> List[Dict]:
        """
        Search index using FTS5
        
        Args:
            query: Search query
            attributed: Filter by attribution status (None = all)
            limit: Max results
        
        Returns:
            List of matching files with metadata
        """
        
        sql = '''
            SELECT f.*, 
                   bm25(files_fts) as relevance
            FROM files f
            JOIN files_fts ON f.rowid = files_fts.rowid
            WHERE files_fts MATCH ?
        '''
        
        params = [query]
        
        if attributed is not None:
            sql += ' AND f.attributed = ?'
            params.append(1 if attributed else 0)
        
        sql += ' ORDER BY relevance LIMIT ?'
        params.append(limit)
        
        results = self.db.execute(sql, params).fetchall()
        
        return [dict(row) for row in results]
    
    def get_full_content(self, file_hash: str) -> Optional[bytes]:
        """Load full content from store"""
        
        # Find file in store
        matches = list(self.store_path.glob(f"{file_hash}*"))
        
        if not matches:
            return None
        
        # Update access tracking
        self.db.execute('''
            UPDATE files 
            SET last_accessed = ?,
                access_count = access_count + 1
            WHERE hash = ?
        ''', (datetime.now().isoformat(), file_hash))
        self.db.commit()
        
        return matches[0].read_bytes()
    
    def get_metadata(self, file_hash: str) -> Optional[Dict]:
        """Get file metadata"""
        row = self.db.execute(
            'SELECT * FROM files WHERE hash = ?',
            (file_hash,)
        ).fetchone()
        
        return dict(row) if row else None
    
    def find_similar(self, file_hash: str, limit: int = 5) -> List[Dict]:
        """Find similar files based on keywords/entities"""
        
        metadata = self.get_metadata(file_hash)
        if not metadata:
            return []
        
        # Parse keywords and entities
        keywords = json.loads(metadata['keywords'])
        entities = json.loads(metadata['entities'])
        
        # Build search query
        search_terms = keywords[:3] + entities
        query = ' OR '.join(search_terms)
        
        # Search excluding current file
        results = self.search(query, limit=limit + 1)
        
        return [r for r in results if r['hash'] != file_hash][:limit]
    
    def get_stats(self) -> Dict[str, int]:
        """Get index statistics"""
        
        stats = {}
        
        stats['total'] = self.db.execute('SELECT COUNT(*) FROM files').fetchone()[0]
        stats['unattributed'] = self.db.execute('SELECT COUNT(*) FROM files WHERE attributed = 0').fetchone()[0]
        stats['attributed'] = self.db.execute('SELECT COUNT(*) FROM files WHERE attributed = 1').fetchone()[0]
        stats['archived'] = self.db.execute('SELECT COUNT(*) FROM files WHERE archived = 1').fetchone()[0]
        
        return stats


if __name__ == '__main__':
    # Test
    index = ContentIndexEngine()
    print("Content Index Engine initialized")
    print(f"Database: {index.db_path}")
    print(f"Store: {index.store_path}")
    print(f"Stats: {index.get_stats()}")
