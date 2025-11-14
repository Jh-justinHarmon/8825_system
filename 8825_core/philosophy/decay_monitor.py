#!/usr/bin/env python3
"""
Decay Monitor - Flag and deprecate stale principles

Monitors principle ages and usage to:
- Flag principles not used in 30+ days (decaying)
- Auto-deprecate principles not used in 90+ days
- Notify user of deprecations
- Generate decay reports

Runs weekly to maintain philosophy health.
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class DecayMonitor:
    """Monitor and manage principle decay"""
    
    def __init__(self, philosophy_path: Path = None):
        if philosophy_path is None:
            philosophy_path = Path(__file__).parent.parent.parent / "PHILOSOPHY.md"
        self.philosophy_path = philosophy_path
        self.principles = self._load_principles()
        
        # Decay thresholds
        self.DECAY_THRESHOLD_DAYS = 30
        self.DEPRECATE_THRESHOLD_DAYS = 90
    
    def _load_principles(self) -> Dict[str, Dict]:
        """Load principles with metadata"""
        if not self.philosophy_path.exists():
            return {}
        
        content = self.philosophy_path.read_text()
        principles = {}
        
        # Parse principle sections
        sections = re.split(r'###\s+\d+\.\s+', content)
        
        for section in sections[1:]:
            lines = section.split('\n')
            title = lines[0].strip()
            
            metadata = {
                'title': title,
                'use_count': 0,
                'last_used': None,
                'added_date': None,
                'status': 'active',
                'is_iron_clad': False
            }
            
            # Check if iron-clad (in Core Principles section)
            if 'Core Principles (Iron-Clad)' in content.split(section)[0]:
                metadata['is_iron_clad'] = True
            
            # Parse metadata
            for line in lines:
                if 'Use Count:' in line:
                    match = re.search(r'Use Count:\*\*\s*(\d+)', line)
                    if match:
                        metadata['use_count'] = int(match.group(1))
                
                elif 'Last Used:' in line:
                    match = re.search(r'Last Used:\*\*\s*(.+?)(?:\n|$)', line)
                    if match:
                        last_used = match.group(1).strip()
                        if last_used != 'N/A':
                            metadata['last_used'] = last_used
                
                elif 'Added:' in line:
                    match = re.search(r'Added:\*\*\s*(.+?)(?:\n|$)', line)
                    if match:
                        metadata['added_date'] = match.group(1).strip()
                
                elif 'Status:' in line:
                    match = re.search(r'Status:\*\*\s*(\w+)', line)
                    if match:
                        metadata['status'] = match.group(1).lower()
            
            principles[title] = metadata
        
        return principles
    
    def check_decay(self) -> Dict[str, List[str]]:
        """Check all principles for decay
        
        Returns:
            {
                'decaying': [...],  # 30-89 days
                'deprecated': [...],  # 90+ days
                'healthy': [...]  # Used recently
            }
        """
        now = datetime.now()
        
        results = {
            'decaying': [],
            'deprecated': [],
            'healthy': [],
            'iron_clad': []
        }
        
        for title, meta in self.principles.items():
            # Skip iron-clad principles
            if meta['is_iron_clad']:
                results['iron_clad'].append(title)
                continue
            
            # Check if never used
            if meta['use_count'] == 0:
                # Check age since added
                if meta['added_date']:
                    added = datetime.strptime(meta['added_date'], "%B %d, %Y")
                    days_since_added = (now - added).days
                    
                    if days_since_added >= self.DEPRECATE_THRESHOLD_DAYS:
                        results['deprecated'].append(title)
                    elif days_since_added >= self.DECAY_THRESHOLD_DAYS:
                        results['decaying'].append(title)
                    else:
                        results['healthy'].append(title)
                continue
            
            # Check last used date
            if meta['last_used']:
                last_used = datetime.strptime(meta['last_used'], "%Y-%m-%d")
                days_since_used = (now - last_used).days
                
                if days_since_used >= self.DEPRECATE_THRESHOLD_DAYS:
                    results['deprecated'].append(title)
                elif days_since_used >= self.DECAY_THRESHOLD_DAYS:
                    results['decaying'].append(title)
                else:
                    results['healthy'].append(title)
            else:
                # No last used date, check added date
                if meta['added_date']:
                    added = datetime.strptime(meta['added_date'], "%B %d, %Y")
                    days_since_added = (now - added).days
                    
                    if days_since_added >= self.DEPRECATE_THRESHOLD_DAYS:
                        results['deprecated'].append(title)
                    elif days_since_added >= self.DECAY_THRESHOLD_DAYS:
                        results['decaying'].append(title)
        
        return results
    
    def flag_for_decay(self, principle_title: str) -> bool:
        """Flag a principle as decaying"""
        if principle_title not in self.principles:
            return False
        
        if self.principles[principle_title]['is_iron_clad']:
            print(f"⚠️  Cannot flag iron-clad principle: {principle_title}")
            return False
        
        # Update status in PHILOSOPHY.md
        content = self.philosophy_path.read_text()
        
        # Find and update status
        pattern = rf'(###\s+\d+\.\s+{re.escape(principle_title)}.*?)\*\*Status:\*\*\s*\w+'
        replacement = rf'\1**Status:** Decaying'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        self.philosophy_path.write_text(content)
        
        print(f"⚠️  Flagged for decay: {principle_title}")
        return True
    
    def deprecate_principle(self, principle_title: str, reason: str = "Not used in 90+ days") -> bool:
        """Deprecate a principle"""
        if principle_title not in self.principles:
            return False
        
        if self.principles[principle_title]['is_iron_clad']:
            print(f"❌ Cannot deprecate iron-clad principle: {principle_title}")
            return False
        
        # Log deprecation
        self._log_deprecation(principle_title, reason)
        
        # Update status in PHILOSOPHY.md
        content = self.philosophy_path.read_text()
        
        pattern = rf'(###\s+\d+\.\s+{re.escape(principle_title)}.*?)\*\*Status:\*\*\s*\w+'
        replacement = rf'\1**Status:** Deprecated'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        self.philosophy_path.write_text(content)
        
        print(f"🗑️  Deprecated: {principle_title}")
        print(f"   Reason: {reason}")
        
        return True
    
    def _log_deprecation(self, principle_title: str, reason: str):
        """Log deprecation to tracking file"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "deprecations.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'principle': principle_title,
            'reason': reason,
            'use_count': self.principles[principle_title]['use_count'],
            'last_used': self.principles[principle_title]['last_used']
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def auto_deprecate_stale(self, dry_run: bool = True) -> List[str]:
        """Auto-deprecate principles not used in 90+ days
        
        Args:
            dry_run: If True, only report what would be deprecated
        
        Returns:
            List of deprecated principle titles
        """
        decay_status = self.check_decay()
        deprecated = []
        
        for title in decay_status['deprecated']:
            if dry_run:
                print(f"[DRY RUN] Would deprecate: {title}")
            else:
                if self.deprecate_principle(title):
                    deprecated.append(title)
        
        return deprecated
    
    def generate_decay_report(self) -> str:
        """Generate decay monitoring report"""
        decay_status = self.check_decay()
        
        report = f"""# Principle Decay Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Summary

- **Healthy:** {len(decay_status['healthy'])} principles
- **Decaying:** {len(decay_status['decaying'])} principles (30-89 days)
- **Deprecated:** {len(decay_status['deprecated'])} principles (90+ days)
- **Iron-Clad:** {len(decay_status['iron_clad'])} principles (protected)

---

## ⚠️ Decaying Principles ({len(decay_status['decaying'])})

*Not used in 30-89 days*

"""
        
        for title in decay_status['decaying']:
            meta = self.principles[title]
            report += f"- **{title}**\n"
            report += f"  - Use count: {meta['use_count']}\n"
            report += f"  - Last used: {meta['last_used'] or 'Never'}\n"
            report += f"  - Added: {meta['added_date']}\n\n"
        
        report += f"\n---\n\n## 🗑️ Deprecated Candidates ({len(decay_status['deprecated'])})\n\n"
        report += "*Not used in 90+ days - recommend deprecation*\n\n"
        
        for title in decay_status['deprecated']:
            meta = self.principles[title]
            report += f"- **{title}**\n"
            report += f"  - Use count: {meta['use_count']}\n"
            report += f"  - Last used: {meta['last_used'] or 'Never'}\n"
            report += f"  - Added: {meta['added_date']}\n\n"
        
        report += f"\n---\n\n## ✅ Healthy Principles ({len(decay_status['healthy'])})\n\n"
        
        for title in decay_status['healthy']:
            meta = self.principles[title]
            report += f"- {title} ({meta['use_count']} uses)\n"
        
        report += "\n---\n\n## Actions Recommended\n\n"
        
        if decay_status['decaying']:
            report += f"1. Review {len(decay_status['decaying'])} decaying principles\n"
            report += "2. Consider if they're still relevant\n"
        
        if decay_status['deprecated']:
            report += f"3. Deprecate {len(decay_status['deprecated'])} stale principles\n"
            report += "4. Notify user of deprecations\n"
        
        return report

def main():
    """Example usage"""
    monitor = DecayMonitor()
    
    # Check decay
    print("\n" + "="*80)
    print("DECAY MONITORING")
    print("="*80 + "\n")
    
    decay_status = monitor.check_decay()
    
    print(f"Healthy: {len(decay_status['healthy'])}")
    print(f"Decaying: {len(decay_status['decaying'])}")
    print(f"Deprecated: {len(decay_status['deprecated'])}")
    
    # Generate report
    print("\n" + monitor.generate_decay_report())
    
    # Auto-deprecate (dry run)
    print("\n" + "="*80)
    print("AUTO-DEPRECATION (DRY RUN)")
    print("="*80 + "\n")
    
    monitor.auto_deprecate_stale(dry_run=True)

if __name__ == '__main__':
    main()
