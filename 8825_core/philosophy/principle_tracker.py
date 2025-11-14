#!/usr/bin/env python3
"""
Principle Tracker - Track philosophy principle usage in real-time

Monitors when principles are applied during decision-making and updates:
- Use count
- Last used date
- Decision impact

Integrates with PHILOSOPHY.md to maintain tracking metadata.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class PrincipleTracker:
    """Track principle usage and update PHILOSOPHY.md"""
    
    def __init__(self, philosophy_path: Path = None):
        if philosophy_path is None:
            philosophy_path = Path(__file__).parent.parent.parent / "PHILOSOPHY.md"
        self.philosophy_path = philosophy_path
        self.principles = self._load_principles()
    
    def _load_principles(self) -> Dict[str, Dict]:
        """Load principles from PHILOSOPHY.md with metadata"""
        if not self.philosophy_path.exists():
            return {}
        
        content = self.philosophy_path.read_text()
        principles = {}
        
        # Parse each principle section
        # Looking for pattern: ### N. Title
        sections = re.split(r'###\s+\d+\.\s+', content)
        
        for section in sections[1:]:  # Skip first split (before first ###)
            lines = section.split('\n')
            title = lines[0].strip()
            
            # Extract metadata
            metadata = {
                'title': title,
                'use_count': 0,
                'last_used': None,
                'added_date': None,
                'status': 'active'
            }
            
            # Parse metadata from section
            for line in lines:
                if 'Use Count:' in line:
                    match = re.search(r'Use Count:\*\*\s*(\d+)', line)
                    if match:
                        metadata['use_count'] = int(match.group(1))
                
                elif 'Last Used:' in line:
                    match = re.search(r'Last Used:\*\*\s*(.+?)(?:\n|$)', line)
                    if match:
                        metadata['last_used'] = match.group(1).strip()
                
                elif 'Added:' in line:
                    match = re.search(r'Added:\*\*\s*(.+?)(?:\n|$)', line)
                    if match:
                        metadata['added_date'] = match.group(1).strip()
            
            principles[title] = metadata
        
        return principles
    
    def record_usage(self, principle_title: str, decision_context: str, 
                    impact_type: Optional[str] = None) -> bool:
        """Record that a principle was used
        
        Args:
            principle_title: Title of principle used
            decision_context: What decision was being made
            impact_type: 'design', 'prevented_mistake', or 'improved_ux'
        
        Returns:
            True if recorded successfully
        """
        
        if principle_title not in self.principles:
            print(f"⚠️  Principle not found: {principle_title}")
            return False
        
        # Update metadata
        self.principles[principle_title]['use_count'] += 1
        self.principles[principle_title]['last_used'] = datetime.now().strftime("%Y-%m-%d")
        
        # Log the usage
        self._log_usage(principle_title, decision_context, impact_type)
        
        # Update PHILOSOPHY.md
        self._update_philosophy_file(principle_title)
        
        print(f"✅ Recorded usage of: {principle_title}")
        print(f"   Use count: {self.principles[principle_title]['use_count']}")
        print(f"   Context: {decision_context[:100]}...")
        
        return True
    
    def _log_usage(self, principle_title: str, context: str, impact_type: Optional[str]):
        """Log usage to tracking file"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "principle_usage.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'principle': principle_title,
            'context': context,
            'impact_type': impact_type,
            'use_count': self.principles[principle_title]['use_count']
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _update_philosophy_file(self, principle_title: str):
        """Update PHILOSOPHY.md with new metadata"""
        content = self.philosophy_path.read_text()
        
        metadata = self.principles[principle_title]
        
        # Find the principle section
        pattern = rf'(###\s+\d+\.\s+{re.escape(principle_title)}.*?)\*\*Use Count:\*\*\s*\d+'
        replacement = rf'\1**Use Count:** {metadata["use_count"]}'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Update last used
        pattern = rf'(###\s+\d+\.\s+{re.escape(principle_title)}.*?)\*\*Last Used:\*\*\s*[^\n]+'
        replacement = rf'\1**Last Used:** {metadata["last_used"]}'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        self.philosophy_path.write_text(content)
    
    def get_usage_stats(self) -> Dict[str, any]:
        """Get usage statistics across all principles"""
        stats = {
            'total_principles': len(self.principles),
            'total_uses': sum(p['use_count'] for p in self.principles.values()),
            'most_used': None,
            'least_used': None,
            'never_used': [],
            'recently_used': []
        }
        
        # Find most/least used
        if self.principles:
            sorted_by_use = sorted(
                self.principles.items(),
                key=lambda x: x[1]['use_count'],
                reverse=True
            )
            
            stats['most_used'] = {
                'title': sorted_by_use[0][0],
                'count': sorted_by_use[0][1]['use_count']
            }
            
            stats['least_used'] = {
                'title': sorted_by_use[-1][0],
                'count': sorted_by_use[-1][1]['use_count']
            }
            
            # Never used
            stats['never_used'] = [
                title for title, meta in self.principles.items()
                if meta['use_count'] == 0
            ]
            
            # Recently used (last 7 days)
            from datetime import timedelta
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            stats['recently_used'] = [
                title for title, meta in self.principles.items()
                if meta['last_used'] and meta['last_used'] >= week_ago
            ]
        
        return stats
    
    def check_for_promotion(self, principle_title: str) -> Optional[str]:
        """Check if principle should be promoted
        
        Returns:
            Promotion recommendation or None
        """
        if principle_title not in self.principles:
            return None
        
        meta = self.principles[principle_title]
        
        # Promotion criteria: 3+ uses
        if meta['use_count'] >= 3 and meta['status'] == 'active':
            return f"✨ PROMOTION CANDIDATE: {principle_title} has {meta['use_count']} uses"
        
        return None
    
    def generate_usage_report(self) -> str:
        """Generate usage report"""
        stats = self.get_usage_stats()
        
        report = f"""# Principle Usage Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Summary

- **Total Principles:** {stats['total_principles']}
- **Total Uses:** {stats['total_uses']}
- **Average Uses:** {stats['total_uses'] / max(stats['total_principles'], 1):.1f}

---

## Most Used

**{stats['most_used']['title']}** - {stats['most_used']['count']} uses

---

## Never Used ({len(stats['never_used'])})

"""
        
        for title in stats['never_used']:
            report += f"- {title}\n"
        
        report += f"\n---\n\n## Recently Used (Last 7 Days)\n\n"
        
        for title in stats['recently_used']:
            count = self.principles[title]['use_count']
            report += f"- {title} ({count} total uses)\n"
        
        report += "\n---\n\n## Promotion Candidates\n\n"
        
        for title, meta in self.principles.items():
            recommendation = self.check_for_promotion(title)
            if recommendation:
                report += f"- {recommendation}\n"
        
        return report

def main():
    """Example usage"""
    tracker = PrincipleTracker()
    
    # Example: Record usage
    tracker.record_usage(
        "Friction is a Feature Flag",
        "Deciding whether to require manual screenshot selection",
        impact_type="prevented_mistake"
    )
    
    # Get stats
    print("\n" + "="*80)
    print(tracker.generate_usage_report())

if __name__ == '__main__':
    main()
