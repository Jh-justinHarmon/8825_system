#!/usr/bin/env python3
"""
Inbox Weighting - Calculate priority scores
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from classifier import InboxItem


class PriorityCalculator:
    """Calculate priority scores for inbox items"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path(__file__).parent / 'config' / 'classification_rules.json'
        
        with open(config_path, 'r') as f:
            self.rules = json.load(f)
        
        self.source_trust = self.rules['source_trust_scores']
    
    def calculate_priority(self, item: InboxItem) -> float:
        """
        Calculate overall priority score
        
        Formula:
        (0.4 * freshness) +
        (0.3 * source_trust) +
        (0.2 * structure_quality) -
        (0.1 * overlap_penalty)
        """
        # Calculate components
        item.freshness = self._calculate_freshness(item.timestamp)
        item.source_trust = self._get_source_trust(item.source_channel)
        item.structure_quality = self._calculate_structure_quality(item)
        overlap_penalty = 0.3 if item.overlap_detected else 0.0
        
        # Weighted sum
        priority = (
            (0.4 * item.freshness) +
            (0.3 * item.source_trust) +
            (0.2 * item.structure_quality) -
            (0.1 * overlap_penalty)
        )
        
        # Boost for high change pressure (needs attention)
        if item.change_pressure == 'high':
            priority *= 1.2
        
        # Boost for system-wide scope (important)
        if item.scope_intent == 'system-wide':
            priority *= 1.15
        
        # Clamp to 0-1
        item.priority_score = max(0.0, min(1.0, priority))
        
        return item.priority_score
    
    def _calculate_freshness(self, timestamp: datetime) -> float:
        """
        Calculate freshness score (0-1)
        
        < 24 hours: 1.0
        < 7 days: 0.7
        < 30 days: 0.4
        older: 0.2
        """
        now = datetime.now()
        
        # Handle timezone-aware timestamps
        if timestamp.tzinfo is not None and now.tzinfo is None:
            from datetime import timezone
            now = now.replace(tzinfo=timezone.utc)
        elif timestamp.tzinfo is None and now.tzinfo is not None:
            now = now.replace(tzinfo=None)
        
        age = now - timestamp
        
        if age < timedelta(hours=24):
            return 1.0
        elif age < timedelta(days=7):
            return 0.7
        elif age < timedelta(days=30):
            return 0.4
        else:
            return 0.2
    
    def _get_source_trust(self, source: str) -> float:
        """Get trust score for source"""
        return self.source_trust.get(source, 0.5)
    
    def _calculate_structure_quality(self, item: InboxItem) -> float:
        """
        Calculate structure quality (0-1)
        
        Based on:
        - Has all required fields
        - Content is well-formed
        - Metadata is complete
        """
        score = 0.0
        
        # Has content_type (required)
        if item.content_type:
            score += 0.3
        
        # Has target_focus
        if item.target_focus:
            score += 0.2
        
        # Content is dict with data
        if isinstance(item.content, dict) and item.content:
            score += 0.3
        
        # Metadata has timestamp and source
        if item.metadata.get('timestamp') and item.metadata.get('source'):
            score += 0.2
        
        return score


class ProcessingOrderer:
    """Determine processing order for inbox items"""
    
    PRIORITY_CATEGORIES = {
        'critical': 0.8,  # System integrity, conflicts
        'high': 0.6,      # Global proposals, active work
        'medium': 0.4,    # Focus-specific, recent
        'low': 0.2        # Old context, low-pressure
    }
    
    def categorize(self, item: InboxItem) -> str:
        """Categorize item by priority"""
        # Critical: validation errors, conflicts
        if item.change_pressure == 'high' and item.scope_intent == 'system-wide':
            return 'critical'
        
        # High: global proposals, recent high-pressure
        if item.scope_intent == 'system-wide' or \
           (item.change_pressure == 'high' and item.freshness > 0.7):
            return 'high'
        
        # Medium: focus-specific, recent
        if item.scope_intent == 'focus-wide' or item.freshness > 0.7:
            return 'medium'
        
        # Low: everything else
        return 'low'
    
    def sort_items(self, items: list[InboxItem]) -> list[InboxItem]:
        """Sort items by priority"""
        return sorted(items, key=lambda x: x.priority_score, reverse=True)


if __name__ == '__main__':
    # Test weighting
    from classifier import InboxClassifier
    
    classifier = InboxClassifier()
    calculator = PriorityCalculator()
    orderer = ProcessingOrderer()
    
    test_data = {
        'content_type': 'pattern',
        'target_focus': 'hcss',
        'content': {
            'title': 'New workflow for TGIF meetings',
            'description': 'Auto-route all Friday meetings to HCSS'
        },
        'metadata': {
            'source': 'chatgpt',
            'timestamp': datetime.now().isoformat()
        }
    }
    
    item = classifier.classify(test_data, 'test.json')
    priority = calculator.calculate_priority(item)
    category = orderer.categorize(item)
    
    print(f"Priority: {priority:.2f}")
    print(f"Category: {category}")
    print(f"Freshness: {item.freshness:.2f}")
    print(f"Source Trust: {item.source_trust:.2f}")
    print(f"Structure Quality: {item.structure_quality:.2f}")
