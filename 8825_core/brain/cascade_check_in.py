#!/usr/bin/env python3
"""
Cascade Check-In Protocol - Allow Cascades to sync with Brain

Provides mechanism for active Cascades to:
1. Check in with Brain periodically
2. Get updates since last check
3. Receive new protocols/principles
4. Adjust behavior based on new knowledge

Usage in Cascade:
    from cascade_check_in import CascadeCheckIn
    
    check_in = CascadeCheckIn(cascade_id="cascade_a", task_type="automation")
    
    # Periodically (every 5 min)
    if check_in.should_check_in():
        updates = check_in.check_in()
        if updates:
            apply_updates(updates)
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from brain_update_tracker import BrainUpdateTracker
from safe_file_ops import safe_read_json, safe_write_json, safe_append_jsonl

class CascadeCheckIn:
    """Handle Cascade check-ins with Brain"""
    
    def __init__(self, cascade_id: str, task_type: Optional[str] = None,
                 focus_area: Optional[str] = None, check_in_interval_minutes: int = 5):
        """
        Args:
            cascade_id: Unique identifier for this Cascade
            task_type: Type of task (automation, validation, documentation, etc.)
            focus_area: Focus area (joju, hcss, jh, etc.)
            check_in_interval_minutes: How often to check in (default: 5 min)
        """
        self.cascade_id = cascade_id
        self.task_type = task_type
        self.focus_area = focus_area
        self.check_in_interval = timedelta(minutes=check_in_interval_minutes)
        
        self.tracker = BrainUpdateTracker()
        self.state_file = Path(__file__).parent / "state" / f"cascade_{cascade_id}.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load Cascade state"""
        default_state = {
            'cascade_id': self.cascade_id,
            'task_type': self.task_type,
            'focus_area': self.focus_area,
            'started_at': datetime.now().isoformat(),
            'last_check_in': datetime.now().isoformat(),
            'check_in_count': 0,
            'updates_received': 0
        }
        return safe_read_json(self.state_file, default=default_state)
    
    def _save_state(self):
        """Save Cascade state"""
        safe_write_json(self.state_file, self.state, backup=True)
    
    def should_check_in(self) -> bool:
        """Check if it's time to check in with Brain"""
        last_check = datetime.fromisoformat(self.state['last_check_in'])
        now = datetime.now()
        
        return (now - last_check) >= self.check_in_interval
    
    def check_in(self, force: bool = False) -> Optional[Dict]:
        """Check in with Brain for updates
        
        Args:
            force: Force check-in even if interval hasn't elapsed
        
        Returns:
            Updates dict if there are updates, None otherwise
        """
        if not force and not self.should_check_in():
            return None
        
        # Get updates since last check
        last_check = self.state['last_check_in']
        
        # Build relevance filter
        relevant_to = []
        if self.task_type:
            relevant_to.append(self.task_type)
        if self.focus_area:
            relevant_to.append(self.focus_area)
        
        updates = self.tracker.get_updates_since(
            last_check,
            relevant_to=relevant_to if relevant_to else None
        )
        
        # Update state
        self.state['last_check_in'] = datetime.now().isoformat()
        self.state['check_in_count'] += 1
        
        if updates['count'] > 0:
            self.state['updates_received'] += updates['count']
            self._log_check_in(updates)
        
        self._save_state()
        
        return updates if updates['count'] > 0 else None
    
    def _log_check_in(self, updates: Dict):
        """Log check-in to tracking file"""
        log_file = Path(__file__).parent / "state" / "check_in_log.jsonl"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'cascade_id': self.cascade_id,
            'task_type': self.task_type,
            'focus_area': self.focus_area,
            'updates_count': updates['count'],
            'check_in_number': self.state['check_in_count']
        }
        
        safe_append_jsonl(log_file, log_entry)
    
    def format_updates_for_cascade(self, updates: Dict) -> str:
        """Format updates in a way Cascade can understand
        
        Returns human-readable update message
        """
        if not updates or updates['count'] == 0:
            return ""
        
        message = f"⚠️ BRAIN UPDATE ({updates['count']} changes)\n\n"
        
        for update in updates['updates']:
            timestamp = datetime.fromisoformat(update['timestamp']).strftime("%H:%M")
            message += f"**[{timestamp}]** "
            
            for file_type in update.get('updated_files', []):
                message += f"{file_type.replace('_', ' ').title()} updated\n"
                
                if file_type in update.get('changes', {}):
                    changes = update['changes'][file_type]
                    
                    if 'new_principles' in changes and changes['new_principles']:
                        message += f"  📚 New principles:\n"
                        for principle in changes['new_principles'][:3]:  # Show first 3
                            message += f"    - {principle}\n"
                    
                    if 'deprecated_principles' in changes and changes['deprecated_principles']:
                        message += f"  🗑️ Deprecated:\n"
                        for principle in changes['deprecated_principles']:
                            message += f"    - {principle}\n"
                    
                    if changes.get('priority_updates'):
                        message += "  🎯 Decision matrix updated\n"
                    
                    if changes.get('new_protocols'):
                        message += "  📋 New learning protocols available\n"
            
            message += "\n"
        
        message += "💡 Consider adjusting approach based on new knowledge.\n"
        
        return message
    
    def get_status(self) -> Dict:
        """Get current Cascade status"""
        started = datetime.fromisoformat(self.state['started_at'])
        last_check = datetime.fromisoformat(self.state['last_check_in'])
        now = datetime.now()
        
        return {
            'cascade_id': self.cascade_id,
            'task_type': self.task_type,
            'focus_area': self.focus_area,
            'running_for': str(now - started),
            'last_check_in': str(now - last_check) + ' ago',
            'check_in_count': self.state['check_in_count'],
            'updates_received': self.state['updates_received'],
            'next_check_in': str(self.check_in_interval - (now - last_check))
        }

class CascadeCoordinator:
    """Coordinate multiple Cascades and their check-ins"""
    
    def __init__(self):
        self.state_dir = Path(__file__).parent / "state"
        self.tracker = BrainUpdateTracker()
    
    def get_active_cascades(self, activity_threshold_hours: int = 1) -> List[Dict]:
        """Get list of active Cascades
        
        Args:
            activity_threshold_hours: Consider Cascade dead if no check-in for this many hours
        
        Returns:
            List of active Cascade states
        """
        if not self.state_dir.exists():
            return []
        
        cascades = []
        for state_file in self.state_dir.glob("cascade_*.json"):
            try:
                state = safe_read_json(state_file)
                
                # Check if Cascade is still active
                last_check = datetime.fromisoformat(state['last_check_in'])
                if (datetime.now() - last_check) < timedelta(hours=activity_threshold_hours):
                    cascades.append(state)
            except Exception as e:
                print(f"⚠️  Error reading {state_file}: {e}")
                continue
        
        return cascades
    
    def cleanup_dead_cascades(self, inactivity_threshold_hours: int = 24) -> int:
        """Clean up state files for dead Cascades
        
        Args:
            inactivity_threshold_hours: Remove Cascades inactive for this many hours
        
        Returns:
            Number of Cascades cleaned up
        """
        if not self.state_dir.exists():
            return 0
        
        cleaned = 0
        now = datetime.now()
        
        for state_file in self.state_dir.glob("cascade_*.json"):
            try:
                state = safe_read_json(state_file)
                last_check = datetime.fromisoformat(state['last_check_in'])
                
                # If inactive for threshold period, remove
                if (now - last_check) > timedelta(hours=inactivity_threshold_hours):
                    cascade_id = state.get('cascade_id', 'unknown')
                    print(f"🧹 Cleaning up dead Cascade: {cascade_id} (inactive for {(now - last_check).total_seconds() / 3600:.1f}h)")
                    
                    # Remove state file
                    state_file.unlink()
                    cleaned += 1
            
            except Exception as e:
                print(f"⚠️  Error checking {state_file}: {e}")
                continue
        
        if cleaned > 0:
            print(f"✅ Cleaned up {cleaned} dead Cascade(s)")
        
        return cleaned
    
    def broadcast_update(self, update_message: str):
        """Broadcast update to all active Cascades
        
        In practice, this would notify Cascade windows
        For now, just logs the broadcast
        """
        broadcast_log = self.state_dir / "broadcasts.jsonl"
        
        broadcast = {
            'timestamp': datetime.now().isoformat(),
            'message': update_message,
            'active_cascades': len(self.get_active_cascades())
        }
        
        safe_append_jsonl(broadcast_log, broadcast)
        
        print(f"📢 Broadcast to {broadcast['active_cascades']} active Cascades:")
        print(f"   {update_message}")
    
    def get_coordination_status(self) -> str:
        """Get status of all Cascades"""
        cascades = self.get_active_cascades()
        
        status = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CASCADE COORDINATION STATUS                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Active Cascades: {len(cascades)}

"""
        
        for cascade in cascades:
            started = datetime.fromisoformat(cascade['started_at'])
            last_check = datetime.fromisoformat(cascade['last_check_in'])
            running_time = datetime.now() - started
            
            status += f"**{cascade['cascade_id']}**\n"
            status += f"  Task: {cascade.get('task_type', 'N/A')}\n"
            status += f"  Focus: {cascade.get('focus_area', 'N/A')}\n"
            status += f"  Running: {running_time}\n"
            status += f"  Check-ins: {cascade['check_in_count']}\n"
            status += f"  Updates: {cascade['updates_received']}\n\n"
        
        return status

def main():
    """Example usage"""
    
    # Example: Cascade checks in
    check_in = CascadeCheckIn(
        cascade_id="cascade_automation_1",
        task_type="automation",
        focus_area="inbox_hub"
    )
    
    print("Cascade Status:")
    print(json.dumps(check_in.get_status(), indent=2))
    
    # Force check-in
    print("\nChecking in with Brain...")
    updates = check_in.check_in(force=True)
    
    if updates:
        print("\n" + check_in.format_updates_for_cascade(updates))
    else:
        print("No updates from Brain.")
    
    # Coordinator status
    print("\n" + "="*80)
    coordinator = CascadeCoordinator()
    print(coordinator.get_coordination_status())

if __name__ == '__main__':
    main()
