#!/usr/bin/env python3
"""
Ingestion Engine - Main orchestrator for inbox processing
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from validators import InboxValidator, ValidationResult
from classifier import InboxClassifier, InboxItem
from weighting import PriorityCalculator, ProcessingOrderer
from lane_b_processor import LaneBProcessor

# Import content index system
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'content_index'))
from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine
from decay_engine import DecayEngine


class IngestionEngine:
    """Main orchestrator for inbox ingestion"""
    
    def __init__(self, inbox_path: Optional[str] = None):
        if inbox_path is None:
            inbox_path = Path.home() / 'Downloads' / '8825_inbox'
        
        self.inbox_path = Path(inbox_path)
        self.pending_path = self.inbox_path / 'pending'
        self.processing_path = self.inbox_path / 'processing'
        self.completed_path = self.inbox_path / 'completed'
        self.errors_path = self.inbox_path / 'errors'
        
        # Ensure folders exist
        for path in [self.pending_path, self.processing_path, 
                     self.completed_path, self.errors_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.validator = InboxValidator()
        self.classifier = InboxClassifier()
        self.calculator = PriorityCalculator()
        self.orderer = ProcessingOrderer()
        
        # Initialize content index system (replaces Lane A/B)
        self.content_index = ContentIndexEngine(self.inbox_path / 'content_index')
        self.usage_tracker = UsageTracker(self.content_index.db_path)
        self.promotion_engine = PromotionEngine(
            self.content_index.db_path,
            self.content_index.store_path,
            self.usage_tracker
        )
        self.decay_engine = DecayEngine(self.content_index.db_path)
        
        # Keep Lane B for backward compatibility (will be phased out)
        self.lane_b = LaneBProcessor()
    
    def process_inbox(self) -> dict:
        """
        Process all files in pending/
        
        Returns summary of processing
        """
        # Get all pending files (JSON, TXT, MD, DOCX, PDF)
        pending_files = (
            list(self.pending_path.glob('*.json')) + 
            list(self.pending_path.glob('*.txt')) +
            list(self.pending_path.glob('*.md')) +
            list(self.pending_path.glob('*.docx')) +
            list(self.pending_path.glob('*.pdf'))
        )
        
        if not pending_files:
            return {
                'status': 'empty',
                'message': 'No files in pending/',
                'processed': 0
            }
        
        results = {
            'total': len(pending_files),
            'lane_a': 0,
            'lane_b': 0,
            'errors': 0,
            'items': []
        }
        
        # Process each file
        for file_path in pending_files:
            try:
                result = self.process_file(file_path)
                results['items'].append(result)
                
                if result['lane'] == 'A':
                    results['lane_a'] += 1
                elif result['lane'] == 'B':
                    results['lane_b'] += 1
                    
            except Exception as e:
                results['errors'] += 1
                self._move_to_errors(file_path, str(e))
        
        return results
    
    def process_file(self, file_path: Path) -> dict:
        """
        Process single inbox file
        
        Returns processing result
        """
        # Validate
        validation = self.validator.validate_and_normalize(str(file_path))
        
        if not validation.valid:
            self._move_to_errors(file_path, validation.error_message)
            return {
                'file': file_path.name,
                'status': 'error',
                'error': validation.error_message,
                'lane': None
            }
        
        # Classify
        item = self.classifier.classify(validation.data, str(file_path))
        
        # Calculate priority
        self.calculator.calculate_priority(item)
        
        # Route to lane
        lane = self.route(item)
        item.lane = lane
        
        # Log result
        result = {
            'file': file_path.name,
            'status': 'classified',
            'lane': lane,
            'priority': item.priority_score,
            'scope': item.scope_intent,
            'change_pressure': item.change_pressure,
            'target_focus': item.target_focus,
            'category': self.orderer.categorize(item)
        }
        
        # Move to processing with metadata
        self._move_to_processing(file_path, item)
        
        # NEW: Content index system (replaces Lane A/B)
        try:
            # Ingest to content index
            index_result = self.content_index.ingest(file_path)
            
            result['index_result'] = index_result
            result['status'] = index_result['status']
            
            # Check for auto-promotion
            if index_result['status'] == 'indexed':
                confidence = self.promotion_engine.calculate_confidence(index_result['hash'])
                
                if confidence >= 0.85:
                    # Auto-promote
                    destination = self.promotion_engine.suggest_destination(index_result['hash'])
                    if destination:
                        promoted = self.promotion_engine.promote_file(index_result['hash'], destination)
                        if promoted:
                            result['auto_promoted'] = True
                            result['destination'] = destination
                            result['confidence'] = confidence
                
                elif confidence >= 0.70:
                    # Suggest to user
                    result['suggestion'] = {
                        'destination': self.promotion_engine.suggest_destination(index_result['hash']),
                        'confidence': confidence
                    }
            
        except Exception as e:
            # Fallback to Lane B if content index fails
            print(f"Content index error: {e}, falling back to Lane B")
            lane_b_result = self.lane_b.process(item)
            result['lane_b_result'] = lane_b_result
        
        return result
    
    def route(self, item: InboxItem) -> str:
        """
        Route item to Lane B (teaching tickets)
        
        Lane A removed - all items require human review
        Decision matrix (legacy, now unused):
        - change_pressure=medium/high → Lane B
        - scope_intent=system-wide → Lane B
        """
        # Lane B triggers
        if item.change_pressure in ['medium', 'high']:
            return 'B'
        
        if item.scope_intent == 'system-wide':
            return 'B'
        
        # Default to Lane A
        return 'A'
    
    def _move_to_errors(self, file_path: Path, error_message: str):
        """Move file to errors/ with error log"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        error_file = self.errors_path / f"{timestamp}_{file_path.name}"
        
        # Move file
        file_path.rename(error_file)
        
        # Write error log
        error_log = error_file.with_suffix('.error.txt')
        with open(error_log, 'w') as f:
            f.write(f"Error: {error_message}\n")
            f.write(f"Original file: {file_path.name}\n")
            f.write(f"Timestamp: {timestamp}\n")
    
    def _move_to_processing(self, file_path: Path, item: InboxItem):
        """Move file to processing/ with metadata"""
        # Create lane subfolder
        lane_path = self.processing_path / f"lane_{item.lane.lower()}"
        lane_path.mkdir(exist_ok=True)
        
        # Move file
        new_path = lane_path / file_path.name
        file_path.rename(new_path)
        
        # Write metadata
        metadata_file = new_path.with_suffix('.meta.json')
        metadata = {
            'lane': item.lane,
            'priority': item.priority_score,
            'scope': item.scope_intent,
            'change_pressure': item.change_pressure,
            'target_focus': item.target_focus,
            'source': item.source_channel,
            'freshness': item.freshness,
            'processed_at': datetime.now().isoformat()
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def get_stats(self) -> dict:
        """Get inbox statistics"""
        pending = len(list(self.pending_path.glob('*.json')))
        lane_a = len(list((self.processing_path / 'lane_a').glob('*.json'))) if (self.processing_path / 'lane_a').exists() else 0
        lane_b = len(list((self.processing_path / 'lane_b').glob('*.json'))) if (self.processing_path / 'lane_b').exists() else 0
        completed = len(list(self.completed_path.glob('*.json')))
        errors = len(list(self.errors_path.glob('*.json')))
        
        return {
            'pending': pending,
            'lane_a': lane_a,
            'lane_b': lane_b,
            'completed': completed,
            'errors': errors,
            'total_processing': lane_a + lane_b
        }


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='8825 Inbox Ingestion Engine')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process inbox files')
    process_parser.add_argument('--file', help='Process specific file')
    
    # Stats command
    subparsers.add_parser('stats', help='Show inbox statistics')
    
    # Tickets command
    tickets_parser = subparsers.add_parser('tickets', help='Manage teaching tickets')
    tickets_parser.add_argument('action', choices=['list', 'view', 'approve', 'reject'],
                               help='Ticket action')
    tickets_parser.add_argument('ticket_id', nargs='?', help='Ticket ID')
    tickets_parser.add_argument('--reason', help='Rejection reason')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    engine = IngestionEngine()
    
    if args.command == 'process':
        if args.file:
            result = engine.process_file(Path(args.file))
            print(json.dumps(result, indent=2))
        else:
            results = engine.process_inbox()
            print(json.dumps(results, indent=2))
    
    elif args.command == 'stats':
        stats = engine.get_stats()
        print(json.dumps(stats, indent=2))
    
    elif args.command == 'tickets':
        tickets_path = engine.inbox_path / 'processing' / 'teaching_tickets'
        
        if args.action == 'list':
            tickets = list(tickets_path.glob('*.md'))
            print(f"\n📋 Teaching Tickets ({len(tickets)}):\n")
            for ticket_file in sorted(tickets):
                ticket_id = ticket_file.stem
                # Read first line for summary
                with open(ticket_file, 'r') as f:
                    first_line = f.readline().strip()
                print(f"  • {ticket_id}")
            print()
        
        elif args.action == 'view':
            if not args.ticket_id:
                print("Error: ticket_id required")
                return
            
            ticket_file = tickets_path / f"{args.ticket_id}.md"
            if ticket_file.exists():
                with open(ticket_file, 'r') as f:
                    print(f.read())
            else:
                print(f"Ticket not found: {args.ticket_id}")
        
        elif args.action == 'approve':
            if not args.ticket_id:
                print("Error: ticket_id required")
                return
            
            print(f"✅ Approved: {args.ticket_id}")
            print("Next: Review in teaching/brainstorm mode, then export to Windsurf")
        
        elif args.action == 'reject':
            if not args.ticket_id:
                print("Error: ticket_id required")
                return
            
            reason = args.reason or "No reason provided"
            print(f"❌ Rejected: {args.ticket_id}")
            print(f"Reason: {reason}")


if __name__ == '__main__':
    main()
