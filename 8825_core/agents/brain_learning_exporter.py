#!/usr/bin/env python3
"""
Brain Learning Exporter - Export brain learnings to external formats

Repurposed from AGENT-LIBRARY-CHAT-MINING-0001 to leverage brain's
learning_extractor and auto_memory_creator for consistent extraction.

Usage:
    # Export brain memories to markdown
    python3 brain_learning_exporter.py --source brain --format markdown
    
    # Extract from checkpoint and export as JSON
    python3 brain_learning_exporter.py --source checkpoint.md --format json
    
    # Export high-confidence learnings only
    python3 brain_learning_exporter.py --source brain --format cascade --min-confidence 0.8
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter

# Add brain directory to path
brain_dir = Path(__file__).parent.parent / "brain"
sys.path.insert(0, str(brain_dir))

from learning_extractor import LearningExtractor, Learning, LearningType
from auto_memory_creator import AutoMemoryCreator


class BrainLearningExporter:
    """Export brain learnings to various formats"""
    
    def __init__(self):
        self.extractor = LearningExtractor()
        self.memory_creator = AutoMemoryCreator()
    
    def load_source(self, source_type: str, source_path: Optional[str] = None) -> List[Learning]:
        """
        Load learnings from various sources
        
        Args:
            source_type: 'brain' | 'checkpoint' | 'text'
            source_path: Path to source file (for checkpoint/text)
        
        Returns:
            List of Learning objects
        """
        if source_type == "brain":
            return self._load_from_brain()
        elif source_type == "checkpoint":
            return self._load_from_checkpoint(source_path)
        elif source_type == "text":
            return self._load_from_text(source_path)
        else:
            raise ValueError(f"Unknown source type: {source_type}")
    
    def _load_from_brain(self) -> List[Learning]:
        """Load learnings from brain's memory store"""
        memories = self.memory_creator.get_all_memories()
        learnings = []
        
        for memory in memories.values():
            learning = Learning(
                type=LearningType(memory['type']),
                title=memory['title'],
                content=memory['content'],
                context=memory['context'],
                confidence=memory['confidence'],
                tags=memory['tags'],
                source=memory['source'],
                created_at=memory['created_at'],
                half_life_days=memory['half_life_days'],
                tries=memory['tries'],
                successes=memory['successes'],
                failures=memory['failures'],
                last_used=memory.get('last_used'),
                contexts=memory.get('contexts', []),
                sources=memory.get('sources', []),
                tools=memory.get('tools', []),
                superseded_by=memory.get('superseded_by'),
                supersedes=memory.get('supersedes'),
                status=memory.get('status', 'active')
            )
            learnings.append(learning)
        
        return learnings
    
    def _load_from_checkpoint(self, checkpoint_path: str) -> List[Learning]:
        """Extract learnings from checkpoint summary"""
        with open(checkpoint_path, 'r') as f:
            checkpoint_text = f.read()
        
        return self.extractor.extract_learnings(checkpoint_text, source=checkpoint_path)
    
    def _load_from_text(self, text_path: str) -> List[Learning]:
        """Extract learnings from arbitrary text"""
        with open(text_path, 'r') as f:
            text = f.read()
        
        return self.extractor.extract_learnings(text, source=text_path)
    
    def apply_filters(
        self,
        learnings: List[Learning],
        learning_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        date_range: Optional[tuple] = None
    ) -> List[Learning]:
        """
        Filter learnings by various criteria
        
        Args:
            learnings: List of learnings to filter
            learning_type: Filter by type (decision, pattern, policy, solution, mistake)
            tags: Filter by tags (must have at least one)
            min_confidence: Minimum confidence threshold
            date_range: Tuple of (start_date, end_date) as ISO strings
        
        Returns:
            Filtered list of learnings
        """
        filtered = learnings
        
        # Filter by type
        if learning_type:
            filtered = [l for l in filtered if l.type.value == learning_type]
        
        # Filter by tags
        if tags:
            filtered = [l for l in filtered if any(tag in l.tags for tag in tags)]
        
        # Filter by confidence
        filtered = [l for l in filtered if l.current_confidence >= min_confidence]
        
        # Filter by date range
        if date_range:
            start_date, end_date = date_range
            filtered = [
                l for l in filtered
                if start_date <= l.created_at <= end_date
            ]
        
        return filtered
    
    def export_to_mining_report(self, learnings: List[Learning]) -> Dict:
        """Export to original mining report format"""
        patterns = []
        lexicon = {}
        agents = []
        
        for learning in learnings:
            if learning.type == LearningType.PATTERN:
                patterns.append({
                    'title': learning.title,
                    'content': learning.content,
                    'confidence': learning.confidence,
                    'sources': learning.sources
                })
            elif learning.type == LearningType.DECISION:
                # Decisions become lexicon entries
                lexicon[learning.title] = learning.content
            elif learning.type == LearningType.SOLUTION:
                # Solutions could become agent recipes
                agents.append({
                    'name': learning.title,
                    'description': learning.content,
                    'context': learning.context
                })
        
        return {
            'patterns': patterns,
            'lexicon': lexicon,
            'agent_recipes': agents,
            'metadata': self._generate_metadata(learnings)
        }
    
    def export_to_cascade_memory(self, learnings: List[Learning]) -> List[Dict]:
        """Export to Cascade memory system format"""
        cascade_memories = []
        
        for learning in learnings:
            memory = {
                'Title': learning.title,
                'Content': learning.content,
                'Tags': learning.tags,
                'UserTriggered': False,
                'Metadata': {
                    'type': learning.type.value,
                    'confidence': learning.confidence,
                    'current_confidence': learning.current_confidence,
                    'age_days': learning.age_days,
                    'sources': learning.sources,
                    'created_at': learning.created_at,
                    'tries': learning.tries,
                    'successes': learning.successes,
                    'failures': learning.failures,
                    'success_rate': learning.success_rate,
                    'status': learning.status
                }
            }
            cascade_memories.append(memory)
        
        return cascade_memories
    
    def export_to_markdown(self, learnings: List[Learning]) -> str:
        """Export to human-readable markdown"""
        md = "# Brain Learnings Export\n\n"
        md += f"**Exported:** {datetime.now().isoformat()}\n"
        md += f"**Total Learnings:** {len(learnings)}\n\n"
        
        # Group by type
        by_type = {}
        for learning in learnings:
            type_name = learning.type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(learning)
        
        # Output each type
        for type_name, type_learnings in sorted(by_type.items()):
            md += f"## {type_name.title()}s ({len(type_learnings)})\n\n"
            
            for learning in sorted(type_learnings, key=lambda l: l.current_confidence, reverse=True):
                md += f"### {learning.title}\n\n"
                md += f"**Confidence:** {learning.confidence:.2f} (current: {learning.current_confidence:.2f})\n"
                md += f"**Age:** {learning.age_days} days\n"
                
                if learning.tries > 0:
                    md += f"**Usage:** {learning.tries} tries, {learning.success_rate:.1%} success rate\n"
                
                md += f"\n{learning.content}\n\n"
                
                if learning.context:
                    md += f"**Context:** {learning.context}\n\n"
                
                if learning.tags:
                    md += f"**Tags:** {', '.join(learning.tags)}\n\n"
                
                md += "---\n\n"
        
        # Statistics
        md += "## Statistics\n\n"
        md += self._generate_statistics_markdown(learnings)
        
        return md
    
    def export_to_json(self, learnings: List[Learning]) -> Dict:
        """Export to structured JSON"""
        return {
            'learnings': [
                {
                    'type': l.type.value,
                    'title': l.title,
                    'content': l.content,
                    'context': l.context,
                    'confidence': l.confidence,
                    'current_confidence': l.current_confidence,
                    'age_days': l.age_days,
                    'tags': l.tags,
                    'sources': l.sources,
                    'created_at': l.created_at,
                    'tries': l.tries,
                    'successes': l.successes,
                    'failures': l.failures,
                    'success_rate': l.success_rate,
                    'last_used': l.last_used,
                    'contexts': l.contexts,
                    'tools': l.tools,
                    'superseded_by': l.superseded_by,
                    'supersedes': l.supersedes,
                    'status': l.status
                }
                for l in learnings
            ],
            'metadata': self._generate_metadata(learnings)
        }
    
    def _generate_metadata(self, learnings: List[Learning]) -> Dict:
        """Generate metadata about the export"""
        if not learnings:
            return {
                'total': 0,
                'by_type': {},
                'confidence_distribution': {},
                'date_range': None
            }
        
        # Count by type
        type_counts = Counter(l.type.value for l in learnings)
        
        # Confidence distribution
        confidence_ranges = {
            'high (0.8-1.0)': sum(1 for l in learnings if l.current_confidence >= 0.8),
            'medium (0.5-0.8)': sum(1 for l in learnings if 0.5 <= l.current_confidence < 0.8),
            'low (0.0-0.5)': sum(1 for l in learnings if l.current_confidence < 0.5)
        }
        
        # Date range
        dates = [l.created_at for l in learnings if l.created_at]
        date_range = {
            'earliest': min(dates) if dates else None,
            'latest': max(dates) if dates else None
        }
        
        # Usage stats
        total_tries = sum(l.tries for l in learnings)
        total_successes = sum(l.successes for l in learnings)
        
        return {
            'total': len(learnings),
            'by_type': dict(type_counts),
            'confidence_distribution': confidence_ranges,
            'date_range': date_range,
            'usage': {
                'total_tries': total_tries,
                'total_successes': total_successes,
                'overall_success_rate': total_successes / total_tries if total_tries > 0 else 0
            },
            'exported_at': datetime.now().isoformat()
        }
    
    def _generate_statistics_markdown(self, learnings: List[Learning]) -> str:
        """Generate statistics section for markdown export"""
        metadata = self._generate_metadata(learnings)
        
        md = f"**Total Learnings:** {metadata['total']}\n\n"
        
        md += "**By Type:**\n"
        for type_name, count in sorted(metadata['by_type'].items()):
            md += f"- {type_name}: {count}\n"
        md += "\n"
        
        md += "**Confidence Distribution:**\n"
        for range_name, count in metadata['confidence_distribution'].items():
            md += f"- {range_name}: {count}\n"
        md += "\n"
        
        if metadata['usage']['total_tries'] > 0:
            md += "**Usage:**\n"
            md += f"- Total tries: {metadata['usage']['total_tries']}\n"
            md += f"- Total successes: {metadata['usage']['total_successes']}\n"
            md += f"- Overall success rate: {metadata['usage']['overall_success_rate']:.1%}\n"
        
        return md


def main():
    parser = argparse.ArgumentParser(description="Export brain learnings to various formats")
    
    # Source options
    parser.add_argument(
        '--source',
        choices=['brain', 'checkpoint', 'text'],
        default='brain',
        help='Source of learnings'
    )
    parser.add_argument(
        '--source-path',
        help='Path to source file (for checkpoint/text)'
    )
    
    # Export format
    parser.add_argument(
        '--format',
        choices=['mining_report', 'cascade', 'markdown', 'json'],
        default='markdown',
        help='Export format'
    )
    
    # Filters
    parser.add_argument(
        '--type',
        choices=['decision', 'pattern', 'policy', 'solution', 'mistake'],
        help='Filter by learning type'
    )
    parser.add_argument(
        '--tags',
        nargs='+',
        help='Filter by tags'
    )
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.0,
        help='Minimum confidence threshold (0.0-1.0)'
    )
    
    # Output
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Validate source path
    if args.source in ['checkpoint', 'text'] and not args.source_path:
        parser.error(f"--source-path required for source type '{args.source}'")
    
    # Create exporter
    exporter = BrainLearningExporter()
    
    # Load learnings
    print(f"Loading learnings from {args.source}...", file=sys.stderr)
    learnings = exporter.load_source(args.source, args.source_path)
    print(f"Loaded {len(learnings)} learnings", file=sys.stderr)
    
    # Apply filters
    if args.type or args.tags or args.min_confidence > 0:
        print(f"Applying filters...", file=sys.stderr)
        learnings = exporter.apply_filters(
            learnings,
            learning_type=args.type,
            tags=args.tags,
            min_confidence=args.min_confidence
        )
        print(f"Filtered to {len(learnings)} learnings", file=sys.stderr)
    
    # Export
    print(f"Exporting to {args.format}...", file=sys.stderr)
    if args.format == 'mining_report':
        output = json.dumps(exporter.export_to_mining_report(learnings), indent=2)
    elif args.format == 'cascade':
        output = json.dumps(exporter.export_to_cascade_memory(learnings), indent=2)
    elif args.format == 'markdown':
        output = exporter.export_to_markdown(learnings)
    elif args.format == 'json':
        output = json.dumps(exporter.export_to_json(learnings), indent=2)
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ Exported to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
