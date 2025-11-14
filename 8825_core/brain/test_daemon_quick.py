#!/usr/bin/env python3
"""
Quick daemon test - runs 3 cycles then stops
"""

import time
from brain_sync_daemon import BrainSyncDaemon

def test_daemon():
    """Test daemon for 3 cycles"""
    
    print("Starting daemon test (3 cycles, 5 seconds each)...\n")
    
    daemon = BrainSyncDaemon(check_interval_seconds=5)
    
    try:
        for i in range(3):
            print(f"\n--- Cycle {i+1}/3 ---")
            daemon._run_cycle()
            
            if i < 2:  # Don't sleep after last cycle
                print(f"Waiting 5 seconds...")
                time.sleep(5)
        
        print("\n✅ Daemon test complete!")
        print(f"Total cycles: {daemon.cycle_count}")
        
        # Show status
        status = daemon.get_status()
        print("\nDaemon Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    test_daemon()
