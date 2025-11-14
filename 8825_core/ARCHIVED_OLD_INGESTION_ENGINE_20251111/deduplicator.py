#!/usr/bin/env python3
"""
Deduplicator - Hash-based duplicate detection
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from classifier import InboxItem


class Deduplicator:
    """Hash-based duplicate detection"""
    
    def __init__(self, index_path: Optional[str] = None):
        if index_path is None:
            workspace = Path(__file__).parent.parent.parent
            index_path = workspace / '8825_index' / 'inbox_index.json'
        
        self.index_path = Path(index_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.index = self._load_index()
    
    def _load_index(self) -> Dict[str, Any]:
        """Load or create index"""
        if self.index_path.exists():
            with open(self.index_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'items': {}
            }
    
    def _save_index(self):
        """Save index to disk"""
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def calculate_hash(self, item: InboxItem) -> str:
        """
        Calculate content hash for item
        
        Uses: content + timestamp (to allow same content at different times)
        """
        # Create stable representation
        hash_data = {
            'content_type': item.content_type,
            'target_focus': item.target_focus,
            'content': item.content,
            # Don't include timestamp in hash - allow same content later
        }
        
        # Convert to stable JSON string
        json_str = json.dumps(hash_data, sort_keys=True)
        
        # Calculate hash
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def is_duplicate(self, item: InboxItem) -> bool:
        """
        Check if item is exact duplicate
        
        Returns True if exact same content exists
        """
        content_hash = self.calculate_hash(item)
        return content_hash in self.index['items']
    
    def find_similar(self, item: InboxItem, threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Find similar (but not exact) items
        
        Uses fuzzy matching on content
        """
        similar = []
        
        # Simple keyword-based similarity for now
        # TODO: Implement proper semantic similarity
        
        item_keywords = self._extract_keywords(item.content)
        
        for hash_id, indexed_item in self.index['items'].items():
            indexed_keywords = set(indexed_item.get('keywords', []))
            
            if not item_keywords or not indexed_keywords:
                continue
            
            # Jaccard similarity
            intersection = len(item_keywords & indexed_keywords)
            union = len(item_keywords | indexed_keywords)
            
            if union > 0:
                similarity = intersection / union
                
                if similarity >= threshold and similarity < 1.0:
                    similar.append({
                        'hash': hash_id,
                        'similarity': similarity,
                        'file': indexed_item.get('original_file'),
                        'timestamp': indexed_item.get('timestamp')
                    })
        
        return sorted(similar, key=lambda x: x['similarity'], reverse=True)
    
    def add_to_index(self, item: InboxItem, target_location: str):
        """
        Add item to index
        """
        content_hash = self.calculate_hash(item)
        
        self.index['items'][content_hash] = {
            'content_type': item.content_type,
            'target_focus': item.target_focus,
            'original_file': item.original_file,
            'target_location': target_location,
            'timestamp': item.timestamp.isoformat(),
            'keywords': list(self._extract_keywords(item.content)),
            'indexed_at': datetime.now().isoformat()
        }
        
        self._save_index()
    
    def _extract_keywords(self, content: dict) -> set:
        """
        Extract keywords from content for similarity matching
        """
        keywords = set()
        
        def extract_from_value(value):
            if isinstance(value, str):
                # Simple word extraction
                words = value.lower().split()
                # Filter out common words and short words
                meaningful = [w for w in words if len(w) > 3 and w not in STOPWORDS]
                keywords.update(meaningful)
            elif isinstance(value, dict):
                for v in value.values():
                    extract_from_value(v)
            elif isinstance(value, list):
                for item in value:
                    extract_from_value(item)
        
        extract_from_value(content)
        return keywords
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        return {
            'total_items': len(self.index['items']),
            'index_size_kb': self.index_path.stat().st_size / 1024 if self.index_path.exists() else 0,
            'created': self.index.get('created'),
            'version': self.index.get('version')
        }


# Common English stopwords
STOPWORDS = {
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
    'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
    'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did',
    'its', 'let', 'put', 'say', 'she', 'too', 'use', 'this', 'that', 'with',
    'from', 'have', 'they', 'will', 'your', 'what', 'been', 'call', 'find',
    'into', 'long', 'look', 'make', 'more', 'than', 'then', 'them', 'time',
    'very', 'when', 'come', 'here', 'just', 'like', 'over', 'such', 'take',
    'well', 'were'
}


if __name__ == '__main__':
    # Test deduplicator
    from classifier import InboxClassifier
    
    classifier = InboxClassifier()
    dedup = Deduplicator()
    
    test_data = {
        'content_type': 'note',
        'target_focus': 'hcss',
        'content': {
            'title': 'TGIF Meeting',
            'notes': 'Discussed project timeline and resource allocation'
        },
        'metadata': {
            'source': 'chatgpt',
            'timestamp': datetime.now().isoformat()
        }
    }
    
    item = classifier.classify(test_data, 'test.json')
    
    print(f"Is duplicate: {dedup.is_duplicate(item)}")
    print(f"Hash: {dedup.calculate_hash(item)}")
    
    # Add to index
    dedup.add_to_index(item, 'focuses/hcss/knowledge/test.md')
    
    print(f"Stats: {dedup.get_stats()}")
