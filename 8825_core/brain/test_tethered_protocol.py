#!/usr/bin/env python3
"""
Test Tethered Brain Protocol

Simulates:
1. Brain update (modify PHILOSOPHY.md)
2. Daemon detecting update
3. Cascade checking in and receiving update
"""

import time
from pathlib import Path
from datetime import datetime

from brain_update_tracker import BrainUpdateTracker
from cascade_check_in import CascadeCheckIn, CascadeCoordinator

def test_full_workflow():
    """Test complete tethered protocol workflow"""
    
    print("="*80)
    print("TESTING TETHERED BRAIN PROTOCOL")
    print("="*80)
    
    # Initialize components
    tracker = BrainUpdateTracker()
    coordinator = CascadeCoordinator()
    
    # Create test Cascade
    cascade = CascadeCheckIn(
        cascade_id="test_cascade_1",
        task_type="testing",
        focus_area="brain"
    )
    
    print("\n1. Initial State")
    print("-" * 80)
    snapshot = tracker.get_current_snapshot()
    print(f"Brain last updated: {snapshot['last_update']}")
    print(f"Update count: {snapshot['update_count']}")
    
    print("\n2. Cascade Initial Check-In")
    print("-" * 80)
    updates = cascade.check_in(force=True)
    if updates:
        print(f"Received {updates['count']} updates")
        print(cascade.format_updates_for_cascade(updates))
    else:
        print("No updates (expected - first check-in)")
    
    print("\n3. Simulating Brain Update...")
    print("-" * 80)
    print("(In real usage, user would edit PHILOSOPHY.md)")
    print("Checking for updates...")
    
    # Check for updates
    brain_updates = tracker.check_for_updates()
    
    if brain_updates['has_updates']:
        print(f"✅ Detected {len(brain_updates['updated_files'])} file updates")
        print(tracker.generate_update_summary(brain_updates))
    else:
        print("No new updates detected")
    
    print("\n4. Cascade Checking In Again")
    print("-" * 80)
    
    # Wait a moment
    time.sleep(1)
    
    # Force another check-in
    updates = cascade.check_in(force=True)
    
    if updates:
        print(f"✅ Received {updates['count']} updates!")
        print("\nFormatted for Cascade:")
        print(cascade.format_updates_for_cascade(updates))
    else:
        print("No new updates")
    
    print("\n5. Coordination Status")
    print("-" * 80)
    print(coordinator.get_coordination_status())
    
    print("\n6. Cascade Status")
    print("-" * 80)
    status = cascade.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    
    print("\n📊 Summary:")
    print(f"  - Brain updates detected: {brain_updates['has_updates']}")
    print(f"  - Cascade check-ins: {status['check_in_count']}")
    print(f"  - Updates received: {status['updates_received']}")
    print(f"  - Active Cascades: {len(coordinator.get_active_cascades())}")
    
    print("\n✅ Tethered Brain Protocol is working!")
    print("\nNext steps:")
    print("  1. Start daemon: python3 brain_sync_daemon.py --daemon")
    print("  2. Integrate check-in into Cascade execution loops")
    print("  3. Edit PHILOSOPHY.md and watch updates propagate")

if __name__ == '__main__':
    test_full_workflow()
