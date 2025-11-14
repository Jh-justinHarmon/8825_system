#!/usr/bin/env python3
"""
Brain Update Tracker - Track what's changed in Brain knowledge

Monitors changes to:
- Principles (new, updated, deprecated)
- Protocols (new, modified)
- Learnings (from sessions)
- Decision matrix updates
- PromptGen changes

Provides API for Cascades to query: "What's new since timestamp X?"
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set
import hashlib

from safe_file_ops import safe_read_json, safe_write_json, safe_append_jsonl

class BrainUpdateTracker:
    """Track Brain knowledge updates for Cascade synchronization"""
    
    def __init__(self, brain_root: Path = None):
        if brain_root is None:
            brain_root = Path(__file__).parent.parent.parent
        
        self.brain_root = brain_root
        self.state_file = Path(__file__).parent / "state" / "brain_state.json"
        self.update_log = Path(__file__).parent / "state" / "update_log.jsonl"
        
        # Ensure state directory exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Tracked files
        self.tracked_files = {
            'philosophy': brain_root / "PHILOSOPHY.md",
            'decision_matrix': brain_root / "8825_core" / "brain" / "decision_matrix.json",
            'learning_principles': brain_root / "8825_core" / "brain" / "learning_principles.md",
            'prompt_gen': brain_root / "8825_core" / "brain" / "prompt_generator.py"
        }
        
        self.current_state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load current state of tracked files"""
        default_state = {
            'last_update': datetime.now().isoformat(),
            'file_hashes': {},
            'update_count': 0
        }
        return safe_read_json(self.state_file, default=default_state)
    
    def _save_state(self):
        """Save current state"""
        safe_write_json(self.state_file, self.current_state, backup=True)
    
    def _get_file_hash(self, file_path: Path) -> Optional[str]:
        """Get hash of file contents"""
        try:
            if not file_path.exists():
                return None
            
            content = file_path.read_text()
            return hashlib.sha256(content.encode()).hexdigest()
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return None
    
    def check_for_updates(self) -> Dict[str, any]:
        """Check all tracked files for updates
        
        Returns:
            {
                'has_updates': bool,
                'updated_files': [...],
                'changes': {...},
                'timestamp': '...'
            }
        """
        updates = {
            'has_updates': False,
            'updated_files': [],
            'changes': {},
            'timestamp': datetime.now().isoformat()
        }
        
        updated_files = []
        all_changes = {}
        
        for file_type, file_path in self.tracked_files.items():
            try:
                current_hash = self._get_file_hash(file_path)
                previous_hash = self.current_state['file_hashes'].get(file_type)
                
                if current_hash != previous_hash and current_hash is not None:
                    updated_files.append(file_type)
                    
                    # Analyze what changed
                    changes = self._detect_changes(file_type, file_path)
                    all_changes[file_type] = changes
                    
                    # Update state
                    self.current_state['file_hashes'][file_type] = current_hash
            except Exception as e:
                print(f"⚠️  Error checking {file_type}: {e}")
                continue
        
        if updated_files:
            updates['has_updates'] = True
            updates['updated_files'] = updated_files
            updates['changes'] = all_changes
            
            self.current_state['last_update'] = updates['timestamp']
            self.current_state['update_count'] += 1
            self._save_state()
            self._log_update(updates)
        
        return updates
    
    def _detect_changes(self, file_type: str, file_path: Path) -> Dict:
        """Detect specific changes in file"""
        try:
            if not file_path.exists():
                return {}
        except Exception as e:
            print(f"⚠️  Error detecting changes in {file_type}: {e}")
            return {}
        
        changes = {
            'type': file_type,
            'detected_at': datetime.now().isoformat()
        }
        
        content = file_path.read_text()
        
        if file_type == 'philosophy':
            # Detect new/updated principles
            changes['new_principles'] = self._extract_new_principles(content)
            changes['deprecated_principles'] = self._extract_deprecated(content)
        
        elif file_type == 'decision_matrix':
            # Detect priority changes
            changes['priority_updates'] = True
        
        elif file_type == 'learning_principles':
            # Detect new learning protocols
            changes['new_protocols'] = True
        
        elif file_type == 'prompt_gen':
            # Detect prompt generation changes
            changes['prompt_updates'] = True
        
        return changes
    
    def _extract_new_principles(self, content: str) -> List[str]:
        """Extract principle titles from philosophy content"""
        import re
        pattern = r'###\s+\d+\.\s+(.+?)(?:\n|$)'
        matches = re.findall(pattern, content)
        return matches
    
    def _extract_deprecated(self, content: str) -> List[str]:
        """Extract deprecated principles"""
        deprecated = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if '**Status:** Deprecated' in line:
                # Look backwards for principle title
                for j in range(i-1, max(0, i-10), -1):
                    if line.startswith('###'):
                        import re
                        match = re.search(r'###\s+\d+\.\s+(.+?)(?:\n|$)', lines[j])
                        if match:
                            deprecated.append(match.group(1))
                        break
        
        return deprecated
    
    def _log_update(self, update_info: Dict):
        """Log update to update log"""
        safe_append_jsonl(self.update_log, update_info)
    
    def get_updates_since(self, timestamp: str, relevant_to: Optional[List[str]] = None) -> Dict:
        """Get updates since a specific timestamp
        
        Args:
            timestamp: ISO format timestamp
            relevant_to: List of task types or focus areas to filter by
        
        Returns:
            {
                'updates': [...],
                'count': N,
                'most_recent': '...'
            }
        """
        if not self.update_log.exists():
            return {'updates': [], 'count': 0, 'most_recent': None}
        
        updates = []
        target_time = datetime.fromisoformat(timestamp)
        
        with open(self.update_log, 'r') as f:
            for line in f:
                update = json.loads(line)
                update_time = datetime.fromisoformat(update['timestamp'])
                
                if update_time > target_time:
                    # Filter by relevance if specified
                    if relevant_to:
                        if self._is_relevant(update, relevant_to):
                            updates.append(update)
                    else:
                        updates.append(update)
        
        return {
            'updates': updates,
            'count': len(updates),
            'most_recent': updates[-1]['timestamp'] if updates else None
        }
    
    def _is_relevant(self, update: Dict, relevant_to: List[str]) -> bool:
        """Check if update is relevant to task types"""
        # Simple keyword matching - can be enhanced
        update_str = json.dumps(update).lower()
        return any(keyword.lower() in update_str for keyword in relevant_to)
    
    def get_current_snapshot(self) -> Dict:
        """Get current snapshot of Brain state"""
        return {
            'timestamp': datetime.now().isoformat(),
            'last_update': self.current_state['last_update'],
            'update_count': self.current_state['update_count'],
            'tracked_files': list(self.tracked_files.keys()),
            'file_status': {
                name: {
                    'exists': path.exists(),
                    'hash': self._get_file_hash(path)
                }
                for name, path in self.tracked_files.items()
            }
        }
    
    def generate_update_summary(self, updates: Dict) -> str:
        """Generate human-readable update summary"""
        if not updates['has_updates']:
            return "No updates since last check."
        
        summary = f"🧠 Brain Updates Detected ({updates['timestamp']})\n\n"
        
        for file_type in updates['updated_files']:
            summary += f"**{file_type.replace('_', ' ').title()}** updated\n"
            
            if file_type in updates['changes']:
                changes = updates['changes'][file_type]
                
                if 'new_principles' in changes and changes['new_principles']:
                    summary += f"  - New principles: {len(changes['new_principles'])}\n"
                
                if 'deprecated_principles' in changes and changes['deprecated_principles']:
                    summary += f"  - Deprecated: {len(changes['deprecated_principles'])}\n"
                
                if changes.get('priority_updates'):
                    summary += "  - Priority matrix updated\n"
                
                if changes.get('new_protocols'):
                    summary += "  - New learning protocols\n"
        
        return summary

def main():
    """Example usage"""
    tracker = BrainUpdateTracker()
    
    # Check for updates
    print("Checking for Brain updates...")
    updates = tracker.check_for_updates()
    
    if updates['has_updates']:
        print("\n" + tracker.generate_update_summary(updates))
    else:
        print("No updates detected.")
    
    # Get current snapshot
    snapshot = tracker.get_current_snapshot()
    print(f"\nBrain State:")
    print(f"  Last update: {snapshot['last_update']}")
    print(f"  Update count: {snapshot['update_count']}")
    print(f"  Tracked files: {len(snapshot['tracked_files'])}")

if __name__ == '__main__':
    main()
