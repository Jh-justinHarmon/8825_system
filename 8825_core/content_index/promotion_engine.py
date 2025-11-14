#!/usr/bin/env python3
"""
Promotion Engine
Auto-promotes files based on confidence scoring
"""

import sqlite3
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from collections import Counter


class PromotionEngine:
    """
    Confidence-based file promotion
    
    Confidence thresholds:
    - 0.85+: Auto-promote
    - 0.70-0.84: Suggest to user
    - 0.50-0.69: Manual decision
    - < 0.50: Wait for more signals
    """
    
    CONFIDENCE_THRESHOLDS = {
        'auto_promote': 0.85,
        'suggest': 0.70,
        'manual': 0.50
    }
    
    def __init__(self, db_path: Path, store_path: Path, usage_tracker):
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
        self.store_path = store_path
        self.usage_tracker = usage_tracker
    
    def calculate_confidence(self, file_hash: str) -> float:
        """
        Calculate confidence score for file attribution
        
        Weighted signals:
        - Similar files pattern: 40%
        - Keyword matching: 30%
        - Usage frequency: 20%
        - File type: 10%
        """
        
        metadata = self._get_metadata(file_hash)
        if not metadata:
            return 0.0
        
        # Signal 1: Similar files pattern (40%)
        pattern_confidence = self._calculate_pattern_confidence(file_hash, metadata)
        
        # Signal 2: Keyword matching (30%)
        keyword_confidence = self._calculate_keyword_confidence(metadata)
        
        # Signal 3: Usage frequency (20%)
        usage_confidence = min(metadata['access_count'] / 5, 1.0)
        
        # Signal 4: File type (10%)
        type_confidence = self._calculate_type_confidence(metadata['file_type'])
        
        # Weighted sum
        confidence = (
            pattern_confidence * 0.4 +
            keyword_confidence * 0.3 +
            usage_confidence * 0.2 +
            type_confidence * 0.1
        )
        
        return confidence
    
    def _get_metadata(self, file_hash: str) -> Optional[Dict]:
        """Get file metadata"""
        row = self.db.execute(
            'SELECT * FROM files WHERE hash = ?',
            (file_hash,)
        ).fetchone()
        
        return dict(row) if row else None
    
    def _calculate_pattern_confidence(self, file_hash: str, metadata: Dict) -> float:
        """Calculate confidence based on similar files pattern"""
        
        pattern = self.usage_tracker.get_pattern(file_hash)
        
        if not pattern:
            return 0.0
        
        return pattern['confidence']
    
    def _calculate_keyword_confidence(self, metadata: Dict) -> float:
        """Calculate confidence based on keyword matching to known locations"""
        
        keyword_patterns = {
            'focuses/hcss/knowledge/': ['RAL Portal', 'HCSS', 'Crunchtime', 'API', 'database'],
            'joju_sandbox/': ['Joju', 'achievement', 'contribution', 'library'],
            'focuses/team76/': ['Team76', 'soccer', 'Team 76'],
            'users/justinharmon/personal/': ['personal', 'note', 'meeting']
        }
        
        keywords = json.loads(metadata['keywords'])
        entities = json.loads(metadata['entities'])
        all_terms = keywords + entities
        
        best_match = 0.0
        
        for location, patterns in keyword_patterns.items():
            matches = sum(1 for term in all_terms if any(p.lower() in term.lower() for p in patterns))
            if matches > 0:
                match_score = matches / len(patterns)
                best_match = max(best_match, match_score)
        
        return best_match
    
    def _calculate_type_confidence(self, file_type: str) -> float:
        """Calculate confidence based on file type"""
        
        # Documentation files are easier to attribute
        doc_types = {'.md', '.txt', '.docx', '.pdf'}
        if file_type in doc_types:
            return 0.8
        
        # Code files need more context
        code_types = {'.py', '.js', '.java', '.cpp'}
        if file_type in code_types:
            return 0.5
        
        return 0.3
    
    def suggest_destination(self, file_hash: str) -> Optional[str]:
        """Suggest destination based on patterns and keywords"""
        
        # Try pattern first
        pattern = self.usage_tracker.get_pattern(file_hash)
        if pattern and pattern['confidence'] > 0.7:
            return pattern['destination']
        
        # Fall back to keyword matching
        metadata = self._get_metadata(file_hash)
        if not metadata:
            return None
        
        entities = json.loads(metadata['entities'])
        
        # Simple rules
        if 'RAL Portal' in entities or 'HCSS' in entities:
            return 'focuses/hcss/knowledge/'
        if 'Joju' in entities:
            return 'joju_sandbox/'
        if 'Team76' in entities:
            return 'focuses/team76/'
        
        return None
    
    def check_promotion_candidates(self) -> List[Dict]:
        """
        Find files ready for promotion
        
        Returns:
            List of candidates with confidence scores and suggested destinations
        """
        
        candidates = []
        
        # Get all unattributed files
        files = self.db.execute('''
            SELECT hash FROM files WHERE attributed = 0
        ''').fetchall()
        
        for file in files:
            file_hash = file['hash']
            confidence = self.calculate_confidence(file_hash)
            
            if confidence >= self.CONFIDENCE_THRESHOLDS['suggest']:
                destination = self.suggest_destination(file_hash)
                
                if destination:
                    candidates.append({
                        'hash': file_hash,
                        'confidence': confidence,
                        'destination': destination,
                        'auto_promote': confidence >= self.CONFIDENCE_THRESHOLDS['auto_promote']
                    })
        
        return candidates
    
    def promote_file(self, file_hash: str, destination: str, check_merge: bool = True) -> Dict:
        """
        Promote file to destination
        
        Steps:
        1. Check if should merge with existing file
        2. If merge: auto-merge and skip promotion
        3. If promote: copy file to destination
        4. Mark as attributed in index
        5. Record in usage tracker
        """
        
        # Check for merge opportunity
        if check_merge:
            try:
                from merge_engine import MergeEngine
                merge_engine = MergeEngine(self.db)
                
                similarity = merge_engine.check_similarity(file_hash, destination)
                
                if similarity['action'] == 'merge':
                    # Auto-merge instead of promoting
                    merge_result = merge_engine.auto_merge(
                        file_hash,
                        similarity['best_match']['file']
                    )
                    
                    if merge_result['status'] == 'merged':
                        # Mark as attributed (merged into existing)
                        self.db.execute('''
                            UPDATE files 
                            SET attributed = 1,
                                destination = ?,
                                promoted_date = ?
                            WHERE hash = ?
                        ''', (str(similarity['best_match']['file']), datetime.now().isoformat(), file_hash))
                        self.db.commit()
                        
                        # Clean up content_store immediately (content merged into existing file)
                        for store_file in self.store_path.glob(f"{file_hash}*"):
                            store_file.unlink()
                        
                        return {
                            'status': 'merged',
                            'destination': str(similarity['best_match']['file']),
                            'action': 'merged_into_existing'
                        }
                
                elif similarity['action'] == 'skip':
                    # Duplicate - mark as attributed but don't copy
                    self.db.execute('''
                        UPDATE files 
                        SET attributed = 1,
                            destination = ?,
                            promoted_date = ?
                        WHERE hash = ?
                    ''', (destination, datetime.now().isoformat(), file_hash))
                    self.db.commit()
                    
                    # Clean up content_store immediately (duplicate, not needed)
                    for store_file in self.store_path.glob(f"{file_hash}*"):
                        store_file.unlink()
                    
                    return {
                        'status': 'skipped',
                        'reason': 'duplicate',
                        'action': 'marked_attributed'
                    }
                
            except Exception as e:
                print(f"Merge check failed: {e}, proceeding with normal promotion")
        
        # Normal promotion
        metadata = self._get_metadata(file_hash)
        if not metadata:
            return {'status': 'error', 'reason': 'metadata not found'}
        
        # Find file in store
        store_files = list(self.store_path.glob(f"{file_hash}*"))
        if not store_files:
            return False
        
        store_file = store_files[0]
        
        # Determine final path
        dest_path = Path(destination)
        if not dest_path.is_absolute():
            # Relative to system root
            system_root = Path(__file__).parent.parent.parent
            dest_path = system_root / destination
        
        dest_path.mkdir(parents=True, exist_ok=True)
        final_path = dest_path / metadata['filename']
        
        # Handle duplicates
        if final_path.exists():
            base = final_path.stem
            ext = final_path.suffix
            counter = 1
            while final_path.exists():
                final_path = dest_path / f"{base}_{counter}{ext}"
                counter += 1
        
        # Copy file
        shutil.copy(store_file, final_path)
        
        # Update database
        self.db.execute('''
            UPDATE files 
            SET attributed = 1,
                destination = ?,
                promoted_date = ?
            WHERE hash = ?
        ''', (str(final_path), datetime.now().isoformat(), file_hash))
        self.db.commit()
        
        # Record usage
        self.usage_tracker.record_attribution(file_hash, destination)
        
        # Clean up content_store immediately (file is now in knowledge base)
        for store_file in self.store_path.glob(f"{file_hash}*"):
            store_file.unlink()
        
        return {
            'status': 'promoted',
            'destination': str(final_path),
            'action': 'new_file_created'
        }


if __name__ == '__main__':
    from index_engine import ContentIndexEngine
    from usage_tracker import UsageTracker
    
    index = ContentIndexEngine()
    tracker = UsageTracker(index.db_path)
    promotion = PromotionEngine(index.db_path, index.store_path, tracker)
    
    print("Checking promotion candidates...")
    candidates = promotion.check_promotion_candidates()
    
    print(f"\nFound {len(candidates)} candidates:")
    for c in candidates:
        metadata = promotion._get_metadata(c['hash'])
        print(f"\n  {metadata['filename']}")
        print(f"    Confidence: {c['confidence']:.2f}")
        print(f"    Destination: {c['destination']}")
        print(f"    Auto-promote: {c['auto_promote']}")
