#!/usr/bin/env python3
"""
Protocol Tracker - Track protocol usage and apply Proof Protocol

Monitors when protocols are consulted during work and tracks:
- Use count
- Last used date
- Success rate (did following the protocol work?)
- Contexts where used
- Time since creation

Applies Proof Protocol (Usage-Driven Evolution):
- Protocols with 3+ successful uses get promoted
- Protocols unused for 30+ days start decaying
- Protocols unused for 90+ days get deprecated
- Success rate determines survival
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class ProtocolTracker:
    """Track protocol usage and apply Proof Protocol"""
    
    def __init__(self, protocols_dir: Path = None):
        if protocols_dir is None:
            protocols_dir = Path(__file__).parent
        
        self.protocols_dir = protocols_dir
        self.state_dir = protocols_dir / "state"
        self.state_dir.mkdir(exist_ok=True)
        
        self.usage_log_path = self.state_dir / "protocol_usage.jsonl"
        self.metadata_path = self.state_dir / "protocol_metadata.json"
        
        self.protocols = self._discover_protocols()
        self.metadata = self._load_metadata()
    
    def _discover_protocols(self) -> Dict[str, Dict]:
        """Discover all protocols in the directory"""
        protocols = {}
        
        # Find all .md and .json protocol files
        for file_path in self.protocols_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in ['.md', '.json', '']:
                # Skip state directory and README
                if file_path.name in ['README.md', 'state']:
                    continue
                
                protocol_id = file_path.stem
                protocols[protocol_id] = {
                    'id': protocol_id,
                    'name': self._format_name(protocol_id),
                    'file': file_path.name,
                    'path': str(file_path),
                    'type': file_path.suffix or 'protocol',
                    'discovered_at': datetime.now().isoformat()
                }
        
        return protocols
    
    def _format_name(self, protocol_id: str) -> str:
        """Format protocol ID into readable name"""
        # Remove 8825_ prefix if present
        name = protocol_id.replace('8825_', '')
        # Replace underscores with spaces
        name = name.replace('_', ' ')
        # Title case
        return name.title()
    
    def _load_metadata(self) -> Dict[str, Dict]:
        """Load protocol metadata (usage stats)"""
        if not self.metadata_path.exists():
            return {}
        
        try:
            with open(self.metadata_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading metadata: {e}")
            return {}
    
    def _save_metadata(self):
        """Save protocol metadata"""
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving metadata: {e}")
    
    def record_usage(self, protocol_id: str, success: bool, 
                    context: str = "", notes: str = "") -> bool:
        """
        Record that a protocol was consulted
        
        Args:
            protocol_id: ID of protocol used (filename without extension)
            success: Did following the protocol work?
            context: What task/project was this for?
            notes: Any additional notes
        
        Returns:
            True if recorded successfully
        """
        
        if protocol_id not in self.protocols:
            print(f"⚠️  Protocol not found: {protocol_id}")
            print(f"   Available protocols: {', '.join(list(self.protocols.keys())[:5])}...")
            return False
        
        # Initialize metadata if first use
        if protocol_id not in self.metadata:
            self.metadata[protocol_id] = {
                'use_count': 0,
                'successes': 0,
                'failures': 0,
                'contexts': [],
                'created_at': self.protocols[protocol_id]['discovered_at'],
                'last_used': None,
                'status': 'active',
                'confidence': 0.8  # Start with 80% confidence
            }
        
        # Update metadata
        meta = self.metadata[protocol_id]
        meta['use_count'] += 1
        
        if success:
            meta['successes'] += 1
        else:
            meta['failures'] += 1
        
        meta['last_used'] = datetime.now().isoformat()
        
        # Add context if new
        if context and context not in meta['contexts']:
            meta['contexts'].append(context)
        
        # Calculate success rate
        tries = meta['use_count']
        success_rate = meta['successes'] / tries if tries > 0 else 0
        
        # Log the usage
        self._log_usage(protocol_id, success, context, notes, success_rate)
        
        # Apply Proof Protocol rules
        self._apply_proof_protocol(protocol_id)
        
        # Save
        self._save_metadata()
        
        protocol_name = self.protocols[protocol_id]['name']
        print(f"✅ Recorded usage: {protocol_name}")
        print(f"   Use count: {meta['use_count']}, Success rate: {success_rate:.0%}")
        
        return True
    
    def _log_usage(self, protocol_id: str, success: bool, context: str, 
                   notes: str, success_rate: float):
        """Log usage to JSONL file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'protocol_id': protocol_id,
            'protocol_name': self.protocols[protocol_id]['name'],
            'success': success,
            'context': context,
            'notes': notes,
            'success_rate': success_rate
        }
        
        with open(self.usage_log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _apply_proof_protocol(self, protocol_id: str):
        """Apply Proof Protocol rules to determine status"""
        meta = self.metadata[protocol_id]
        
        # Calculate age
        created_at = meta.get('created_at')
        if created_at:
            try:
                created = datetime.fromisoformat(created_at)
                age_days = (datetime.now() - created).days
            except:
                age_days = 0
        else:
            age_days = 0
        
        # Calculate days since last use
        last_used = meta.get('last_used')
        if last_used:
            try:
                last_used_dt = datetime.fromisoformat(last_used)
                days_since_use = (datetime.now() - last_used_dt).days
            except:
                days_since_use = 999
        else:
            days_since_use = age_days
        
        # Calculate success rate
        tries = meta['use_count']
        success_rate = meta['successes'] / tries if tries > 0 else 0
        
        # Proof Protocol Rules:
        
        # 1. Promotion: 3+ uses with 70%+ success rate
        if tries >= 3 and success_rate >= 0.7:
            meta['status'] = 'promoted'
            meta['confidence'] = min(0.95, 0.8 + (success_rate - 0.7) * 0.5)
        
        # 2. Decaying: Not used in 30+ days
        elif days_since_use >= 30:
            meta['status'] = 'decaying'
            # Apply decay
            half_life = 90  # 90 day half-life
            decay_factor = 0.5 ** (days_since_use / half_life)
            meta['confidence'] = 0.8 * decay_factor
        
        # 3. Deprecated: Not used in 90+ days OR low success rate
        if days_since_use >= 90 or (tries >= 5 and success_rate < 0.4):
            meta['status'] = 'deprecated'
            meta['confidence'] = 0.2
        
        # 4. Active: Used recently with decent success
        elif days_since_use < 30 and success_rate >= 0.5:
            meta['status'] = 'active'
            meta['confidence'] = 0.8
    
    def get_usage_stats(self, protocol_id: str) -> Optional[Dict]:
        """Get usage statistics for a protocol"""
        if protocol_id not in self.protocols:
            return None
        
        if protocol_id not in self.metadata:
            return {
                'use_count': 0,
                'successes': 0,
                'failures': 0,
                'success_rate': 0,
                'status': 'unused',
                'confidence': 0.8,
                'contexts': [],
                'last_used': None
            }
        
        meta = self.metadata[protocol_id]
        tries = meta['use_count']
        success_rate = meta['successes'] / tries if tries > 0 else 0
        
        return {
            'use_count': tries,
            'successes': meta['successes'],
            'failures': meta['failures'],
            'success_rate': success_rate,
            'status': meta.get('status', 'active'),
            'confidence': meta.get('confidence', 0.8),
            'contexts': meta.get('contexts', []),
            'last_used': meta.get('last_used')
        }
    
    def generate_usage_report(self) -> str:
        """Generate comprehensive usage report"""
        
        # Calculate stats
        total_protocols = len(self.protocols)
        tracked_protocols = len(self.metadata)
        total_uses = sum(m['use_count'] for m in self.metadata.values())
        
        # Categorize by status
        by_status = {'promoted': [], 'active': [], 'decaying': [], 'deprecated': [], 'unused': []}
        
        for protocol_id, protocol in self.protocols.items():
            if protocol_id in self.metadata:
                meta = self.metadata[protocol_id]
                status = meta.get('status', 'active')
                by_status[status].append((protocol_id, meta))
            else:
                by_status['unused'].append((protocol_id, None))
        
        # Build report
        report = f"""# Protocol Usage Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Summary

- **Total Protocols:** {total_protocols}
- **Tracked Protocols:** {tracked_protocols}
- **Total Uses:** {total_uses}
- **Average Uses:** {total_uses / max(tracked_protocols, 1):.1f}

---

## By Status (Proof Protocol)

### ✨ Promoted ({len(by_status['promoted'])})
*3+ uses with 70%+ success rate*

"""
        
        for protocol_id, meta in sorted(by_status['promoted'], 
                                       key=lambda x: x[1]['use_count'], 
                                       reverse=True):
            protocol = self.protocols[protocol_id]
            success_rate = meta['successes'] / meta['use_count']
            report += f"- **{protocol['name']}** - {meta['use_count']} uses, {success_rate:.0%} success\n"
        
        report += f"\n### ✅ Active ({len(by_status['active'])})\n*Used recently with decent success*\n\n"
        
        for protocol_id, meta in sorted(by_status['active'], 
                                       key=lambda x: x[1]['use_count'], 
                                       reverse=True):
            protocol = self.protocols[protocol_id]
            success_rate = meta['successes'] / meta['use_count']
            report += f"- **{protocol['name']}** - {meta['use_count']} uses, {success_rate:.0%} success\n"
        
        report += f"\n### ⏳ Decaying ({len(by_status['decaying'])})\n*Not used in 30+ days*\n\n"
        
        for protocol_id, meta in by_status['decaying']:
            protocol = self.protocols[protocol_id]
            last_used = meta.get('last_used', 'Never')
            if last_used != 'Never':
                try:
                    last_used_dt = datetime.fromisoformat(last_used)
                    days_ago = (datetime.now() - last_used_dt).days
                    last_used = f"{days_ago} days ago"
                except:
                    pass
            report += f"- **{protocol['name']}** - Last used: {last_used}\n"
        
        report += f"\n### ❌ Deprecated ({len(by_status['deprecated'])})\n*Not used in 90+ days OR low success rate*\n\n"
        
        for protocol_id, meta in by_status['deprecated']:
            protocol = self.protocols[protocol_id]
            success_rate = meta['successes'] / meta['use_count'] if meta['use_count'] > 0 else 0
            report += f"- **{protocol['name']}** - {meta['use_count']} uses, {success_rate:.0%} success\n"
        
        report += f"\n### 🆕 Unused ({len(by_status['unused'])})\n*Never tracked*\n\n"
        
        for protocol_id, _ in sorted(by_status['unused'])[:10]:  # Show first 10
            protocol = self.protocols[protocol_id]
            report += f"- {protocol['name']}\n"
        
        if len(by_status['unused']) > 10:
            report += f"\n*...and {len(by_status['unused']) - 10} more*\n"
        
        return report
    
    def list_protocols(self, status: Optional[str] = None) -> List[Dict]:
        """List all protocols, optionally filtered by status"""
        results = []
        
        for protocol_id, protocol in self.protocols.items():
            stats = self.get_usage_stats(protocol_id)
            
            if status and stats['status'] != status:
                continue
            
            results.append({
                'id': protocol_id,
                'name': protocol['name'],
                'file': protocol['file'],
                'type': protocol['type'],
                **stats
            })
        
        return sorted(results, key=lambda x: x['use_count'], reverse=True)


def main():
    """Example usage"""
    tracker = ProtocolTracker()
    
    print("📊 Protocol Tracker - Proof Protocol in Action\n")
    print(f"Discovered {len(tracker.protocols)} protocols\n")
    
    # Example: Record usage
    print("Recording example usage...\n")
    tracker.record_usage(
        "DEEP_DIVE_RESEARCH_PROTOCOL",
        success=True,
        context="Debugging Downloads sync issue",
        notes="Helped identify Universal Inbox Watch was running"
    )
    
    # Generate report
    print("\n" + "="*80)
    print(tracker.generate_usage_report())


if __name__ == '__main__':
    main()
