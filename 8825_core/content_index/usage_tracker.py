#!/usr/bin/env python3
"""
Usage Tracker
Tracks file usage patterns and attribution decisions
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from collections import Counter


class UsageTracker:
    """
    Track file usage and learn attribution patterns
    """
    
    def __init__(self, db_path: Path):
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
        self._init_tables()
    
    def _init_tables(self):
        """Create usage tracking tables"""
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS usage_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT NOT NULL,
                destination TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hash) REFERENCES files(hash)
            );
            
            CREATE INDEX IF NOT EXISTS idx_usage_hash ON usage_history(hash);
            CREATE INDEX IF NOT EXISTS idx_usage_dest ON usage_history(destination);
        ''')
        self.db.commit()
    
    def record_attribution(self, file_hash: str, destination: str):
        """Record that a file was attributed to a destination"""
        self.db.execute('''
            INSERT INTO usage_history (hash, destination)
            VALUES (?, ?)
        ''', (file_hash, destination))
        self.db.commit()
    
    def get_destination(self, file_hash: str) -> Optional[str]:
        """Get destination for a file (if attributed)"""
        row = self.db.execute('''
            SELECT destination FROM usage_history 
            WHERE hash = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (file_hash,)).fetchone()
        
        return row['destination'] if row else None
    
    def get_pattern(self, file_hash: str) -> Optional[Dict]:
        """
        Find attribution pattern based on similar files
        
        Returns:
            dict with destination, confidence, reason
        """
        
        # Get file metadata
        file_row = self.db.execute(
            'SELECT keywords, entities FROM files WHERE hash = ?',
            (file_hash,)
        ).fetchone()
        
        if not file_row:
            return None
        
        import json
        keywords = json.loads(file_row['keywords'])
        entities = json.loads(file_row['entities'])
        
        # Find similar attributed files
        similar_destinations = []
        
        for entity in entities:
            rows = self.db.execute('''
                SELECT uh.destination
                FROM files f
                JOIN usage_history uh ON f.hash = uh.hash
                WHERE (f.keywords LIKE ? OR f.entities LIKE ?)
            ''', (f'%{entity}%', f'%{entity}%')).fetchall()
            
            similar_destinations.extend([r['destination'] for r in rows])
        
        if not similar_destinations:
            return None
        
        # Most common destination
        dest_counts = Counter(similar_destinations)
        most_common_dest, count = dest_counts.most_common(1)[0]
        
        confidence = count / len(similar_destinations)
        
        return {
            'destination': most_common_dest,
            'confidence': confidence,
            'reason': f'{count}/{len(similar_destinations)} similar files went here',
            'sample_count': len(similar_destinations)
        }
    
    def get_usage_count(self, file_hash: str) -> int:
        """Get number of times file was accessed/attributed"""
        row = self.db.execute('''
            SELECT COUNT(*) as count FROM usage_history WHERE hash = ?
        ''', (file_hash,)).fetchone()
        
        return row['count'] if row else 0
    
    def get_destination_stats(self) -> Dict[str, int]:
        """Get count of files attributed to each destination"""
        rows = self.db.execute('''
            SELECT destination, COUNT(*) as count
            FROM usage_history
            GROUP BY destination
            ORDER BY count DESC
        ''').fetchall()
        
        return {row['destination']: row['count'] for row in rows}


if __name__ == '__main__':
    from index_engine import ContentIndexEngine
    
    index = ContentIndexEngine()
    tracker = UsageTracker(index.db_path)
    
    print("Usage Tracker initialized")
    print("\nDestination Stats:")
    stats = tracker.get_destination_stats()
    for dest, count in stats.items():
        print(f"  {dest}: {count} files")
