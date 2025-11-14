#!/usr/bin/env python3
"""
Inbox Classifier - Extract 5 dimensions for routing
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class InboxItem:
    """Normalized inbox item with classification"""
    # Original fields
    content_type: str
    target_focus: str
    content: dict
    metadata: dict
    
    # Classification (computed)
    scope_intent: str  # local, focus-wide, system-wide
    change_pressure: str  # low, medium, high
    source_channel: str  # chatgpt, windsurf, manual, external
    
    # Weighting (computed later)
    priority_score: float = 0.0
    freshness: float = 0.0
    source_trust: float = 0.0
    structure_quality: float = 0.0
    overlap_detected: bool = False
    
    # Routing
    lane: str = ''  # A or B
    
    # Provenance
    original_file: str = ''
    timestamp: datetime = None
    processing_id: str = ''
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class InboxClassifier:
    """Classifies inbox items across 5 dimensions"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).parent / 'config' / 'classification_rules.json'
        
        with open(config_path, 'r') as f:
            self.rules = json.load(f)
    
    def classify(self, data: Dict[str, Any], original_file: str = '') -> InboxItem:
        """
        Extract 5 dimensions and create InboxItem
        """
        # Extract original fields
        content_type = data.get('content_type', 'note')
        content = data.get('content', {})
        metadata = data.get('metadata', {})
        
        # Infer target_focus from content if not explicitly set
        target_focus = data.get('target_focus')
        if not target_focus or target_focus == 'jh':
            # Try to infer from filename and content
            inferred_focus = self.infer_target_focus(original_file, content, metadata)
            if inferred_focus:
                target_focus = inferred_focus
            else:
                target_focus = 'jh'  # Default fallback
        
        # Compute classifications
        scope_intent = self.infer_scope(content, content_type)
        change_pressure = self.infer_change_pressure(content, content_type)
        source_channel = self.infer_source(metadata)
        
        # Create item
        item = InboxItem(
            content_type=content_type,
            target_focus=target_focus,
            content=content,
            metadata=metadata,
            scope_intent=scope_intent,
            change_pressure=change_pressure,
            source_channel=source_channel,
            original_file=original_file,
            timestamp=self._parse_timestamp(metadata.get('timestamp'))
        )
        
        return item
    
    def infer_target_focus(self, filename: str, content: dict, metadata: dict) -> Optional[str]:
        """
        Infer target focus from filename and content keywords
        
        Returns:
            Focus name (joju, hcss, jh) or None if can't determine
        """
        if 'focus_routing_keywords' not in self.rules:
            return None
        
        # Combine filename, content, and metadata into searchable text
        search_text = f"{filename} {json.dumps(content)} {json.dumps(metadata)}".lower()
        
        # Check each focus for keyword matches
        focus_scores = {}
        for focus, keywords in self.rules['focus_routing_keywords'].items():
            score = sum(1 for keyword in keywords if keyword.lower() in search_text)
            if score > 0:
                focus_scores[focus] = score
        
        # Return focus with highest score
        if focus_scores:
            return max(focus_scores, key=focus_scores.get)
        
        return None
    
    def infer_scope(self, content: dict, content_type: str) -> str:
        """
        Infer scope from keywords
        
        Keywords: "global", "system-wide" → system-wide
        Keywords: "HCSS", "Joju" → focus-wide
        Default: local
        """
        content_str = json.dumps(content).lower()
        
        # Check system-wide keywords
        for keyword in self.rules['scope_keywords']['system-wide']:
            if keyword.lower() in content_str:
                return 'system-wide'
        
        # Check focus-wide keywords
        for keyword in self.rules['scope_keywords']['focus-wide']:
            if keyword.lower() in content_str:
                return 'focus-wide'
        
        # Default to local
        return 'local'
    
    def infer_change_pressure(self, content: dict, content_type: str) -> str:
        """
        Infer change pressure from keywords and content_type
        
        Keywords: "workflow", "protocol", "agent" → high
        Keywords: "pattern", "feature" → medium
        Default: low
        """
        content_str = json.dumps(content).lower()
        
        # Check high pressure keywords
        for keyword in self.rules['change_pressure_keywords']['high']:
            if keyword.lower() in content_str:
                return 'high'
        
        # Check medium pressure keywords
        for keyword in self.rules['change_pressure_keywords']['medium']:
            if keyword.lower() in content_str:
                return 'medium'
        
        # Content type based pressure
        if content_type in ['pattern', 'feature']:
            return 'medium'
        elif content_type in ['decision']:
            return 'high'
        
        # Default to low
        return 'low'
    
    def infer_source(self, metadata: dict) -> str:
        """
        Infer source channel from metadata
        """
        source = metadata.get('source', 'manual').lower()
        
        if 'chatgpt' in source:
            return 'chatgpt'
        elif 'windsurf' in source:
            return 'windsurf'
        elif 'external' in source:
            return 'external'
        else:
            return 'manual'
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> datetime:
        """Parse timestamp from string"""
        if not timestamp_str:
            return datetime.now()
        
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            return datetime.now()


class FocusInferencer:
    """Infer focus from content when not specified"""
    
    FOCUS_KEYWORDS = {
        'hcss': ['fridays', 'tgif', 'meeting', 'hcss', 'hammer consulting'],
        'joju': ['joju', 'achievement', 'pattern', 'justin', 'jh'],
        'team76': ['team76', 'project', 'team 76'],
        'jh': ['personal', 'reminder', 'note', 'todo']
    }
    
    def infer(self, content: dict) -> tuple[str, float]:
        """
        Infer focus from keywords
        
        Returns: (focus, confidence)
        """
        content_str = json.dumps(content).lower()
        
        scores = {}
        for focus, keywords in self.FOCUS_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in content_str)
            if score > 0:
                scores[focus] = score
        
        if not scores:
            return 'jh', 0.3  # Default to personal with low confidence
        
        # Get focus with highest score
        best_focus = max(scores, key=scores.get)
        max_score = scores[best_focus]
        total_keywords = len(self.FOCUS_KEYWORDS[best_focus])
        confidence = min(max_score / total_keywords, 1.0)
        
        return best_focus, confidence


if __name__ == '__main__':
    # Test classifier
    classifier = InboxClassifier()
    
    test_data = {
        'content_type': 'pattern',
        'target_focus': 'hcss',
        'content': {
            'title': 'New workflow for TGIF meetings',
            'description': 'Auto-route all Friday meetings to HCSS'
        },
        'metadata': {
            'source': 'chatgpt',
            'timestamp': '2025-11-08T15:00:00'
        }
    }
    
    item = classifier.classify(test_data, 'test.json')
    print(f"Classified item:")
    print(f"  Scope: {item.scope_intent}")
    print(f"  Change Pressure: {item.change_pressure}")
    print(f"  Source: {item.source_channel}")
