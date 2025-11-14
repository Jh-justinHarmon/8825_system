#!/usr/bin/env python3
"""
Learning Extractor - Auto-extract learnings from sessions

Analyzes session transcripts and extracts:
- What worked
- What failed
- Why it happened
- Patterns identified
- Proposed principles

Runs after significant sessions to feed philosophy evolution.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class LearningExtractor:
    """Extract learnings from session transcripts"""
    
    def __init__(self, philosophy_path: Path = None):
        if philosophy_path is None:
            philosophy_path = Path(__file__).parent.parent.parent / "PHILOSOPHY.md"
        self.philosophy_path = philosophy_path
        self.existing_principles = self._load_existing_principles()
    
    def _load_existing_principles(self) -> List[str]:
        """Load existing principles from PHILOSOPHY.md"""
        if not self.philosophy_path.exists():
            return []
        
        content = self.philosophy_path.read_text()
        principles = []
        
        # Extract principle titles
        pattern = r'###\s+\d+\.\s+(.+?)(?:\n|$)'
        matches = re.findall(pattern, content)
        principles.extend(matches)
        
        return principles
    
    def extract_from_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract learnings from session data
        
        Args:
            session_data: {
                'date': '2025-11-11',
                'duration': '2 hours',
                'objective': 'Refine Notion board truth',
                'deliverables': [...],
                'transcript': '...',
                'outcomes': [...]
            }
        
        Returns:
            {
                'learnings': [...],
                'patterns': [...],
                'proposed_principles': [...],
                'validations': [...]  # Existing principles validated
            }
        """
        
        learnings = {
            'session_date': session_data.get('date'),
            'objective': session_data.get('objective'),
            'learnings': [],
            'patterns': [],
            'proposed_principles': [],
            'validations': []
        }
        
        # Extract learnings from transcript
        transcript = session_data.get('transcript', '')
        
        # Look for learning indicators
        learning_indicators = [
            'learned', 'learning', 'discovered', 'found that',
            'realized', 'key insight', 'important', 'critical',
            'mistake', 'error', 'failed', 'worked', 'success'
        ]
        
        # Extract sentences with learning indicators
        sentences = transcript.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in learning_indicators):
                learnings['learnings'].append({
                    'text': sentence,
                    'extracted_at': datetime.now().isoformat()
                })
        
        # Identify patterns
        learnings['patterns'] = self._identify_patterns(learnings['learnings'])
        
        # Propose new principles
        learnings['proposed_principles'] = self._propose_principles(
            learnings['patterns'],
            session_data.get('outcomes', [])
        )
        
        # Check for validations of existing principles
        learnings['validations'] = self._check_validations(
            learnings['learnings'],
            session_data.get('outcomes', [])
        )
        
        return learnings
    
    def _identify_patterns(self, learnings: List[Dict]) -> List[Dict]:
        """Identify patterns across learnings"""
        patterns = []
        
        # Group by theme
        themes = {
            'automation': ['automat', 'manual', 'friction', 'low friction'],
            'validation': ['validat', 'trust', 'confidence', 'precision', 'recall'],
            'documentation': ['document', 'discoverable', 'index', 'readme'],
            'workflow': ['workflow', 'process', 'pipeline', 'flow'],
            'architecture': ['architect', 'structure', 'layer', 'separation']
        }
        
        for theme, keywords in themes.items():
            matching_learnings = []
            for learning in learnings:
                text = learning['text'].lower()
                if any(kw in text for kw in keywords):
                    matching_learnings.append(learning)
            
            if matching_learnings:
                patterns.append({
                    'theme': theme,
                    'count': len(matching_learnings),
                    'learnings': matching_learnings
                })
        
        return patterns
    
    def _propose_principles(self, patterns: List[Dict], outcomes: List[str]) -> List[Dict]:
        """Propose new principles based on patterns"""
        proposals = []
        
        for pattern in patterns:
            if pattern['count'] >= 2:  # At least 2 learnings on same theme
                proposals.append({
                    'theme': pattern['theme'],
                    'proposed_title': f"New principle for {pattern['theme']}",
                    'evidence_count': pattern['count'],
                    'status': 'proposed',
                    'requires_approval': True
                })
        
        return proposals
    
    def _check_validations(self, learnings: List[Dict], outcomes: List[str]) -> List[Dict]:
        """Check if learnings validate existing principles"""
        validations = []
        
        for principle in self.existing_principles:
            principle_lower = principle.lower()
            
            # Check if any learning mentions this principle
            for learning in learnings:
                text = learning['text'].lower()
                
                # Simple keyword matching (could be improved with NLP)
                if any(word in text for word in principle_lower.split()):
                    validations.append({
                        'principle': principle,
                        'validated_by': learning['text'],
                        'validation_type': 'mention'
                    })
        
        return validations
    
    def generate_report(self, learnings: Dict[str, Any], output_path: Path = None) -> str:
        """Generate markdown report of learnings"""
        
        report = f"""# Session Learning Report

**Date:** {learnings['session_date']}
**Objective:** {learnings['objective']}

---

## Learnings Extracted ({len(learnings['learnings'])})

"""
        
        for i, learning in enumerate(learnings['learnings'], 1):
            report += f"{i}. {learning['text']}\n"
        
        report += f"\n---\n\n## Patterns Identified ({len(learnings['patterns'])})\n\n"
        
        for pattern in learnings['patterns']:
            report += f"### {pattern['theme'].title()} ({pattern['count']} learnings)\n\n"
        
        report += f"\n---\n\n## Proposed Principles ({len(learnings['proposed_principles'])})\n\n"
        
        for proposal in learnings['proposed_principles']:
            report += f"- **{proposal['proposed_title']}** (Evidence: {proposal['evidence_count']} learnings)\n"
        
        report += f"\n---\n\n## Validated Existing Principles ({len(learnings['validations'])})\n\n"
        
        for validation in learnings['validations']:
            report += f"- ✅ **{validation['principle']}**\n"
            report += f"  - Validated by: {validation['validated_by'][:100]}...\n\n"
        
        report += "\n---\n\n## Next Steps\n\n"
        report += "1. Review proposed principles\n"
        report += "2. Update use counts for validated principles\n"
        report += "3. Add new principles to PHILOSOPHY.md (with approval)\n"
        
        if output_path:
            output_path.write_text(report)
            print(f"✅ Report saved to: {output_path}")
        
        return report

def main():
    """Example usage"""
    
    # Example session data
    session_data = {
        'date': '2025-11-11',
        'duration': '2 hours',
        'objective': 'Refine Notion board truth',
        'transcript': """
        We learned that low friction automation is better than clever automation.
        The screengrab swap initially failed because it required manual selection.
        Discovered that precision is more important than recall in validation.
        Found that 4 high-confidence tasks are better than 22 mixed-confidence.
        Realized that file location should indicate processing state.
        """,
        'outcomes': [
            'Task Truth Pipeline shipped',
            'Enhanced validator created',
            'Word reports exported'
        ]
    }
    
    extractor = LearningExtractor()
    learnings = extractor.extract_from_session(session_data)
    
    # Generate report
    output_path = Path(__file__).parent / f"learning_report_{session_data['date']}.md"
    report = extractor.generate_report(learnings, output_path)
    
    print(report)

if __name__ == '__main__':
    main()
