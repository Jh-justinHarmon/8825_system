#!/usr/bin/env python3
"""
Teaching Ticket Generator - Create tickets for Lane B items
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

from classifier import InboxItem
from ai_sweep import AISweepResult


@dataclass
class ProposedChange:
    """Description of proposed change"""
    summary: str
    original_context: str
    scope: str
    estimated_effort: str


@dataclass
class TeachingTicket:
    """Complete teaching ticket for human review"""
    ticket_id: str
    source_file: str
    proposed_change: ProposedChange
    ai_sweep_result: AISweepResult
    questions: List[str]
    required_mode: str  # teaching_mode, brainstorm_mode
    export_target: str  # windsurf
    status: str  # pending, reviewed, approved, rejected
    created_at: str


class TeachingTicketGenerator:
    """Generate teaching tickets for Lane B items"""
    
    TICKET_TEMPLATE = """# Teaching Ticket: {ticket_id}

## Proposed Change

{summary}

**Original Context:** {context}  
**Source File:** {source_file}  
**Scope:** {scope}  
**Estimated Effort:** {effort}

---

## AI System-Wide Analysis

### Touchpoints ({touchpoint_count})

{touchpoints}

### Related Patterns ({related_count})

{related_patterns}

### Potential Conflicts ({conflict_count})

{conflicts}

### Blast Radius

**Scope:** {blast_radius}  
**Affected Files:** {file_count}  
**Confidence:** {confidence}%

---

## Questions for Review

{questions}

---

## AI Recommendation

{recommendation}

---

## Next Steps

1. Review in **{required_mode}**
2. Decide: **Approve** / **Narrow Scope** / **Reject** / **Refactor Existing**
3. If approved → Brainstorm → Export to Windsurf

---

**Status:** {status}  
**Created:** {created_at}  
**Ticket ID:** {ticket_id}
"""
    
    def __init__(self, tickets_path: Optional[str] = None):
        if tickets_path is None:
            inbox_path = Path.home() / 'Downloads' / '8825_inbox'
            tickets_path = inbox_path / 'processing' / 'teaching_tickets'
        
        self.tickets_path = Path(tickets_path)
        self.tickets_path.mkdir(parents=True, exist_ok=True)
    
    def generate(self, item: InboxItem, sweep_result: AISweepResult) -> TeachingTicket:
        """
        Generate complete teaching ticket
        """
        # Generate ticket ID
        ticket_id = self._generate_ticket_id()
        
        # Create proposed change
        proposed_change = self._create_proposed_change(item)
        
        # Generate questions
        questions = self.generate_questions(item, sweep_result)
        
        # Determine required mode
        required_mode = self.recommend_mode(item, sweep_result)
        
        # Create ticket
        ticket = TeachingTicket(
            ticket_id=ticket_id,
            source_file=item.original_file,
            proposed_change=proposed_change,
            ai_sweep_result=sweep_result,
            questions=questions,
            required_mode=required_mode,
            export_target='windsurf',
            status='pending',
            created_at=datetime.now().isoformat()
        )
        
        # Save ticket
        self._save_ticket(ticket)
        
        return ticket
    
    def generate_questions(self, item: InboxItem, sweep_result: AISweepResult) -> List[str]:
        """
        Generate smart questions based on AI findings
        """
        questions = []
        
        # Scope questions
        if item.scope_intent == 'system-wide':
            questions.append("Should this be system-wide or focus-specific?")
        
        # Conflict questions
        if sweep_result.conflicts:
            high_severity = [c for c in sweep_result.conflicts if c.severity == 'high']
            if high_severity:
                questions.append("Should we refactor existing patterns instead of adding new one?")
            else:
                questions.append("How should we resolve the detected conflicts?")
        
        # Related pattern questions
        if sweep_result.related_patterns:
            questions.append(f"Should we consolidate with existing patterns in {sweep_result.related_patterns[0].location}?")
        
        # Touchpoint questions
        if len(sweep_result.touchpoints) > 5:
            questions.append("Is the wide impact intentional or should we narrow the scope?")
        
        # Default questions
        if not questions:
            questions.append("What is the minimal version we should ship?")
            questions.append("Are there any dependencies or prerequisites?")
        
        return questions
    
    def recommend_mode(self, item: InboxItem, sweep_result: AISweepResult) -> str:
        """
        Recommend teaching_mode or brainstorm_mode
        """
        # If high conflicts or complex, start with teaching
        if sweep_result.conflicts and any(c.severity == 'high' for c in sweep_result.conflicts):
            return 'teaching_mode'
        
        # If system-wide impact, start with teaching
        if sweep_result.blast_radius == 'system-wide':
            return 'teaching_mode'
        
        # If clear and straightforward, go to brainstorm
        if not sweep_result.conflicts and sweep_result.confidence > 0.7:
            return 'brainstorm_mode'
        
        # Default to teaching
        return 'teaching_mode'
    
    def _generate_ticket_id(self) -> str:
        """Generate unique ticket ID"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        return f"T-8825-{timestamp}"
    
    def _create_proposed_change(self, item: InboxItem) -> ProposedChange:
        """Extract proposed change from item"""
        # Try to get summary from content
        summary = "No summary provided"
        
        if isinstance(item.content, dict):
            # Try common summary fields first
            summary = (
                item.content.get('title') or
                item.content.get('summary') or
                item.content.get('description') or
                item.content.get('achievement')
            )
            
            # If still no summary, try to build one from content
            if not summary:
                # Look for meaningful text fields
                for key in ['text', 'content', 'body', 'message']:
                    if key in item.content and isinstance(item.content[key], str):
                        summary = item.content[key][:100]
                        break
                
                # If still nothing, try to create from structure
                if not summary:
                    # Get first few keys and values
                    parts = []
                    for k, v in list(item.content.items())[:3]:
                        if isinstance(v, str):
                            parts.append(f"{k}: {v[:30]}")
                        elif isinstance(v, list) and v:
                            parts.append(f"{k}: {len(v)} items")
                    
                    if parts:
                        summary = ", ".join(parts)
                    else:
                        summary = f"{item.content_type.replace('_', ' ').title()} for {item.target_focus}"
        
        return ProposedChange(
            summary=summary,
            original_context=item.metadata.get('note', 'No context provided'),
            scope=item.scope_intent,
            estimated_effort='Unknown'
        )
    
    def _save_ticket(self, ticket: TeachingTicket):
        """Save ticket as markdown file"""
        # Format ticket content
        content = self._format_ticket(ticket)
        
        # Save as markdown
        ticket_file = self.tickets_path / f"{ticket.ticket_id}.md"
        with open(ticket_file, 'w') as f:
            f.write(content)
        
        # Also save as JSON for programmatic access
        json_file = self.tickets_path / f"{ticket.ticket_id}.json"
        with open(json_file, 'w') as f:
            json.dump(self._ticket_to_dict(ticket), f, indent=2)
    
    def _format_ticket(self, ticket: TeachingTicket) -> str:
        """Format ticket using template"""
        # Format touchpoints
        touchpoints_text = []
        for i, tp in enumerate(ticket.ai_sweep_result.touchpoints[:10], 1):
            touchpoints_text.append(
                f"{i}. **{tp.file_path}** ({tp.type})\n"
                f"   - Relevance: {tp.relevance:.0%}\n"
                f"   - {tp.description}"
            )
        
        # Format related patterns
        related_text = []
        for i, rp in enumerate(ticket.ai_sweep_result.related_patterns[:5], 1):
            related_text.append(
                f"{i}. **{rp.pattern_name}** in `{rp.location}`\n"
                f"   - Similarity: {rp.similarity:.0%}\n"
                f"   - {rp.context}"
            )
        
        # Format conflicts
        conflicts_text = []
        for i, c in enumerate(ticket.ai_sweep_result.conflicts, 1):
            conflicts_text.append(
                f"{i}. **{c.type.upper()}** (Severity: {c.severity})\n"
                f"   - {c.description}\n"
                f"   - Affected: {', '.join(c.affected_files[:3])}"
            )
        
        # Format questions
        questions_text = '\n'.join(f"{i}. {q}" for i, q in enumerate(ticket.questions, 1))
        
        return self.TICKET_TEMPLATE.format(
            ticket_id=ticket.ticket_id,
            summary=ticket.proposed_change.summary,
            context=ticket.proposed_change.original_context,
            source_file=ticket.source_file,
            scope=ticket.proposed_change.scope,
            effort=ticket.proposed_change.estimated_effort,
            touchpoint_count=len(ticket.ai_sweep_result.touchpoints),
            touchpoints='\n\n'.join(touchpoints_text) if touchpoints_text else 'None found',
            related_count=len(ticket.ai_sweep_result.related_patterns),
            related_patterns='\n\n'.join(related_text) if related_text else 'None found',
            conflict_count=len(ticket.ai_sweep_result.conflicts),
            conflicts='\n\n'.join(conflicts_text) if conflicts_text else 'None detected',
            blast_radius=ticket.ai_sweep_result.blast_radius,
            file_count=len(ticket.ai_sweep_result.touchpoints),
            confidence=int(ticket.ai_sweep_result.confidence * 100),
            questions=questions_text,
            recommendation=ticket.ai_sweep_result.recommendation,
            required_mode=ticket.required_mode,
            status=ticket.status,
            created_at=ticket.created_at
        )
    
    def _ticket_to_dict(self, ticket: TeachingTicket) -> dict:
        """Convert ticket to dict for JSON serialization"""
        return {
            'ticket_id': ticket.ticket_id,
            'source_file': ticket.source_file,
            'proposed_change': asdict(ticket.proposed_change),
            'ai_sweep_result': {
                'touchpoints': [asdict(t) for t in ticket.ai_sweep_result.touchpoints],
                'related_patterns': [asdict(r) for r in ticket.ai_sweep_result.related_patterns],
                'conflicts': [asdict(c) for c in ticket.ai_sweep_result.conflicts],
                'blast_radius': ticket.ai_sweep_result.blast_radius,
                'recommendation': ticket.ai_sweep_result.recommendation,
                'confidence': ticket.ai_sweep_result.confidence
            },
            'questions': ticket.questions,
            'required_mode': ticket.required_mode,
            'export_target': ticket.export_target,
            'status': ticket.status,
            'created_at': ticket.created_at
        }


if __name__ == '__main__':
    # Test ticket generator
    from classifier import InboxClassifier
    from ai_sweep import AISystemSweep
    
    classifier = InboxClassifier()
    sweep = AISystemSweep()
    generator = TeachingTicketGenerator()
    
    test_data = {
        'content_type': 'pattern',
        'target_focus': 'hcss',
        'content': {
            'title': 'New TGIF auto-route workflow',
            'description': 'Automatically route all Friday meetings to HCSS'
        },
        'metadata': {
            'source': 'chatgpt',
            'timestamp': '2025-11-08T16:00:00',
            'note': 'Proposed during ChatGPT conversation about HCSS workflows'
        }
    }
    
    item = classifier.classify(test_data, 'test.json')
    sweep_result = sweep.sweep(item)
    ticket = generator.generate(item, sweep_result)
    
    print(f"Generated ticket: {ticket.ticket_id}")
    print(f"Mode: {ticket.required_mode}")
    print(f"Questions: {len(ticket.questions)}")
