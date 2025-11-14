#!/usr/bin/env python3
"""
Decay Engine
Manages file lifecycle and decay scoring
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path


class DecayEngine:
    """
    File decay management
    
    Decay stages:
    - fresh (0-7 days): New, keep visible
    - aging (7-30 days): Starting to age
    - stale (30-90 days): Probably not valuable
    - expired (90+ days): Delete candidate
    
    Decay score = age_penalty - value_signals
    """
    
    DECAY_STAGES = {
        'fresh': 0,
        'aging': 1,
        'stale': 2,
        'expired': 3
    }
    
    def __init__(self, db_path: Path):
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
    
    def calculate_decay_score(self, file_metadata: Dict) -> int:
        """
        Calculate decay score for a file
        
        Age penalty:
        - 0-7 days: 0 points
        - 7-30 days: +1 point
        - 30-90 days: +2 points
        - 90+ days: +3 points
        
        Value signals (subtract from penalty):
        - Accessed once: -1 point
        - Accessed 2+ times: -2 points
        - Attributed: -999 (never decays)
        - Similar to attributed files: -1 point
        """
        
        # Attributed files never decay
        if file_metadata['attributed']:
            return -999
        
        # Calculate age
        created = datetime.fromisoformat(file_metadata['created'])
        age_days = (datetime.now() - created).days
        
        # Age penalty
        if age_days < 7:
            penalty = 0
        elif age_days < 30:
            penalty = 1
        elif age_days < 90:
            penalty = 2
        else:
            penalty = 3
        
        # Value signals
        value = 0
        
        access_count = file_metadata.get('access_count', 0)
        if access_count >= 1:
            value += 1
        if access_count >= 2:
            value += 1
        
        # Check if similar files are attributed
        if self._has_similar_attributed(file_metadata['hash']):
            value += 1
        
        return max(0, penalty - value)
    
    def _has_similar_attributed(self, file_hash: str) -> bool:
        """Check if similar files have been attributed"""
        
        # Get file keywords/entities
        row = self.db.execute(
            'SELECT keywords, entities FROM files WHERE hash = ?',
            (file_hash,)
        ).fetchone()
        
        if not row:
            return False
        
        import json
        keywords = json.loads(row['keywords'])
        entities = json.loads(row['entities'])
        
        # Simple check: any attributed files with same entities?
        for entity in entities:
            result = self.db.execute('''
                SELECT COUNT(*) as count FROM files 
                WHERE attributed = 1 
                AND (keywords LIKE ? OR entities LIKE ?)
            ''', (f'%{entity}%', f'%{entity}%')).fetchone()
            
            if result['count'] > 0:
                return True
        
        return False
    
    def get_decay_stage(self, decay_score: int) -> str:
        """Convert decay score to stage name"""
        if decay_score <= 0:
            return 'fresh'
        elif decay_score == 1:
            return 'aging'
        elif decay_score == 2:
            return 'stale'
        else:
            return 'expired'
    
    def update_all_scores(self):
        """Recalculate decay scores for all unattributed files"""
        
        files = self.db.execute('''
            SELECT * FROM files WHERE attributed = 0
        ''').fetchall()
        
        updated = 0
        for file in files:
            file_dict = dict(file)
            new_score = self.calculate_decay_score(file_dict)
            
            self.db.execute('''
                UPDATE files SET decay_score = ? WHERE hash = ?
            ''', (new_score, file_dict['hash']))
            
            updated += 1
        
        self.db.commit()
        return updated
    
    def get_decay_report(self) -> Dict[str, int]:
        """Get count of files in each decay stage"""
        
        report = {}
        
        for stage, score in self.DECAY_STAGES.items():
            if stage == 'fresh':
                count = self.db.execute(
                    'SELECT COUNT(*) FROM files WHERE decay_score = 0 AND attributed = 0'
                ).fetchone()[0]
            elif stage == 'aging':
                count = self.db.execute(
                    'SELECT COUNT(*) FROM files WHERE decay_score = 1 AND attributed = 0'
                ).fetchone()[0]
            elif stage == 'stale':
                count = self.db.execute(
                    'SELECT COUNT(*) FROM files WHERE decay_score = 2 AND attributed = 0'
                ).fetchone()[0]
            else:  # expired
                count = self.db.execute(
                    'SELECT COUNT(*) FROM files WHERE decay_score >= 3 AND attributed = 0'
                ).fetchone()[0]
            
            report[stage] = count
        
        return report


if __name__ == '__main__':
    from index_engine import ContentIndexEngine
    
    index = ContentIndexEngine()
    decay = DecayEngine(index.db_path)
    
    print("Updating decay scores...")
    updated = decay.update_all_scores()
    print(f"Updated {updated} files")
    
    print("\nDecay Report:")
    report = decay.get_decay_report()
    for stage, count in report.items():
        print(f"  {stage}: {count} files")
