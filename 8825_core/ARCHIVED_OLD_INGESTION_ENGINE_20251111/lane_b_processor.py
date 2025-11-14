#!/usr/bin/env python3
"""
Lane B Processor - AI sweep and teaching ticket generation
"""

import json
from pathlib import Path
from typing import Dict, Any

from classifier import InboxItem
from ai_sweep import AISystemSweep
from teaching_ticket_generator import TeachingTicketGenerator


class LaneBProcessor:
    """Process Lane B items (AI sweep + teaching tickets)"""
    
    def __init__(self):
        self.sweep = AISystemSweep()
        self.ticket_generator = TeachingTicketGenerator()
    
    def process(self, item: InboxItem) -> Dict[str, Any]:
        """
        Process Lane B item
        
        Steps:
        1. Run AI system-wide sweep
        2. Generate teaching ticket
        3. Save ticket for human review
        4. Return summary
        """
        result = {
            'item': item.original_file,
            'status': 'processing',
            'target_focus': item.target_focus
        }
        
        try:
            # Run AI sweep
            sweep_result = self.sweep.sweep(item)
            
            result['sweep_complete'] = True
            result['touchpoints_found'] = len(sweep_result.touchpoints)
            result['conflicts_found'] = len(sweep_result.conflicts)
            result['blast_radius'] = sweep_result.blast_radius
            result['confidence'] = sweep_result.confidence
            
            # Generate teaching ticket
            ticket = self.ticket_generator.generate(item, sweep_result)
            
            result['ticket_id'] = ticket.ticket_id
            result['required_mode'] = ticket.required_mode
            result['questions_count'] = len(ticket.questions)
            result['status'] = 'ticket_created'
            result['action'] = 'needs_human_review'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result


if __name__ == '__main__':
    # Test Lane B processor
    from classifier import InboxClassifier
    
    classifier = InboxClassifier()
    processor = LaneBProcessor()
    
    test_data = {
        'content_type': 'pattern',
        'target_focus': 'hcss',
        'content': {
            'title': 'New TGIF auto-route workflow',
            'description': 'Automatically route all Friday meetings to HCSS',
            'keywords': ['workflow', 'auto-route', 'tgif']
        },
        'metadata': {
            'source': 'chatgpt',
            'timestamp': '2025-11-08T16:00:00',
            'note': 'Proposed during workflow discussion'
        }
    }
    
    item = classifier.classify(test_data, 'test_lane_b.json')
    result = processor.process(item)
    
    print(json.dumps(result, indent=2))
