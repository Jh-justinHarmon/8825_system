#!/usr/bin/env python3
"""
Demo: Tethered Brain Protocol in Action

Shows complete workflow:
1. Multiple Cascades start working
2. User updates PHILOSOPHY.md
3. Brain detects update
4. Cascades check in and receive updates
5. Cascades adjust behavior
"""

import time
from datetime import datetime
from pathlib import Path

from brain_update_tracker import BrainUpdateTracker
from cascade_check_in import CascadeCheckIn, CascadeCoordinator

class DemoCascade:
    """Simulated Cascade with check-in capability"""
    
    def __init__(self, cascade_id: str, task_type: str, focus_area: str):
        self.cascade_id = cascade_id
        self.task_type = task_type
        self.check_in = CascadeCheckIn(cascade_id, task_type, focus_area, check_in_interval_minutes=0.1)  # 6 seconds for demo
        self.work_cycles = 0
        self.adjustments_made = 0
    
    def do_work(self):
        """Simulate doing work"""
        self.work_cycles += 1
        print(f"  [{self.cascade_id}] Working... (cycle {self.work_cycles})")
        
        # Check in with Brain
        if self.check_in.should_check_in():
            updates = self.check_in.check_in()
            
            if updates:
                print(f"  [{self.cascade_id}] 🔔 RECEIVED UPDATE!")
                print(f"  [{self.cascade_id}] {updates['count']} changes detected")
                
                # Show formatted update
                message = self.check_in.format_updates_for_cascade(updates)
                for line in message.split('\n')[:5]:  # Show first 5 lines
                    print(f"  [{self.cascade_id}]   {line}")
                
                # Adjust behavior
                self.adjustments_made += 1
                print(f"  [{self.cascade_id}] ✅ Adjusted behavior based on update")

def run_demo():
    """Run complete demo"""
    
    print("="*80)
    print("TETHERED BRAIN PROTOCOL - LIVE DEMO")
    print("="*80)
    
    # Initialize
    tracker = BrainUpdateTracker()
    coordinator = CascadeCoordinator()
    
    # Create demo Cascades
    cascades = [
        DemoCascade("automation_cascade", "automation", "inbox_hub"),
        DemoCascade("validation_cascade", "validation", "joju"),
        DemoCascade("documentation_cascade", "documentation", "hcss")
    ]
    
    print("\n📋 Scenario:")
    print("  - 3 Cascades are working on different tasks")
    print("  - Each checks in with Brain every 6 seconds")
    print("  - We'll simulate a Brain update")
    print("  - Watch Cascades receive and respond to update")
    
    print("\n" + "-"*80)
    print("PHASE 1: Cascades Start Working")
    print("-"*80)
    
    # Initial work cycles (no updates)
    for i in range(2):
        print(f"\nWork Cycle {i+1}:")
        for cascade in cascades:
            cascade.do_work()
        time.sleep(2)
    
    print("\n" + "-"*80)
    print("PHASE 2: Brain Update Detected")
    print("-"*80)
    
    # Check for Brain updates
    print("\nChecking Brain for updates...")
    brain_updates = tracker.check_for_updates()
    
    if brain_updates['has_updates']:
        print(f"✅ Brain updated! {len(brain_updates['updated_files'])} files changed")
        print(tracker.generate_update_summary(brain_updates))
    else:
        print("ℹ️  No new Brain updates (PHILOSOPHY.md hasn't changed)")
        print("   (In real usage, user would edit PHILOSOPHY.md between cycles)")
    
    print("\n" + "-"*80)
    print("PHASE 3: Cascades Check In and Receive Updates")
    print("-"*80)
    
    # More work cycles (Cascades will check in and get updates)
    for i in range(3):
        print(f"\nWork Cycle {i+3}:")
        for cascade in cascades:
            cascade.do_work()
        time.sleep(2)
    
    print("\n" + "-"*80)
    print("FINAL STATUS")
    print("-"*80)
    
    print("\nCascade Statistics:")
    for cascade in cascades:
        status = cascade.check_in.get_status()
        print(f"\n{cascade.cascade_id}:")
        print(f"  Work cycles: {cascade.work_cycles}")
        print(f"  Check-ins: {status['check_in_count']}")
        print(f"  Updates received: {status['updates_received']}")
        print(f"  Adjustments made: {cascade.adjustments_made}")
    
    print("\n" + coordinator.get_coordination_status())
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    
    print("\n✅ Key Takeaways:")
    print("  1. Cascades work independently but stay synchronized")
    print("  2. Brain updates propagate automatically")
    print("  3. Each Cascade receives relevant updates")
    print("  4. Behavior adjusts based on new knowledge")
    print("  5. All activity is logged for monitoring")
    
    print("\n🚀 To use in production:")
    print("  1. Start daemon: python3 brain_sync_daemon.py --daemon")
    print("  2. Add check-in to your Cascade code")
    print("  3. Edit PHILOSOPHY.md to test")
    print("  4. Watch updates propagate in real-time")

if __name__ == '__main__':
    run_demo()
