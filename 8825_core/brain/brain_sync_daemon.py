#!/usr/bin/env python3
"""
Brain Sync Daemon - Monitor Brain updates and broadcast to Cascades

Runs continuously to:
1. Check Brain files every 30 seconds
2. Detect updates to philosophy, protocols, etc.
3. Broadcast updates to active Cascades
4. Log synchronization activity

Run as background daemon:
    python3 brain_sync_daemon.py --daemon
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict
import argparse

from brain_update_tracker import BrainUpdateTracker
from cascade_check_in import CascadeCoordinator
from safe_file_ops import safe_append_jsonl
from system_health_monitor import SystemHealthMonitor
from brain_transport_generator import BrainTransportGenerator

class BrainSyncDaemon:
    """Daemon to sync Brain updates with active Cascades"""
    
    def __init__(self, check_interval_seconds: int = 30):
        """
        Args:
            check_interval_seconds: How often to check for updates (default: 30s)
        """
        self.check_interval = check_interval_seconds
        self.tracker = BrainUpdateTracker()
        self.coordinator = CascadeCoordinator()
        
        # NEW: System health monitoring and Brain Transport generation
        self.health_monitor = SystemHealthMonitor()
        self.transport_generator = BrainTransportGenerator()
        
        self.log_file = Path(__file__).parent / "state" / "daemon_log.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.running = False
        self.cycle_count = 0
    
    def _log(self, message: str, level: str = "INFO"):
        """Log daemon activity"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'cycle': self.cycle_count
        }
        
        safe_append_jsonl(self.log_file, log_entry)
        print(f"[{level}] {message}")
    
    def start(self):
        """Start the daemon"""
        self.running = True
        self._log("Brain Sync Daemon starting...")
        self._log(f"Check interval: {self.check_interval}s")
        
        try:
            while self.running:
                self.cycle_count += 1
                self._run_cycle()
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            self._log("Daemon stopped by user", "INFO")
        except Exception as e:
            self._log(f"Daemon error: {str(e)}", "ERROR")
            raise
        finally:
            self.stop()
    
    def _run_cycle(self):
        """Run one sync cycle"""
        cycle_start = datetime.now()
        
        try:
            # Check for Brain updates
            updates = self.tracker.check_for_updates()
            
            if updates['has_updates']:
                self._log(f"Updates detected: {len(updates['updated_files'])} files", "UPDATE")
                
                # Get active Cascades
                active_cascades = self.coordinator.get_active_cascades()
                
                if active_cascades:
                    # Generate update message
                    summary = self.tracker.generate_update_summary(updates)
                    
                    # Broadcast to Cascades
                    self.coordinator.broadcast_update(summary)
                    
                    self._log(f"Broadcast to {len(active_cascades)} active Cascades", "BROADCAST")
                else:
                    self._log("No active Cascades to notify", "INFO")
            
            # NEW: Check system health and auto-regenerate Brain Transport
            system_changes = self.health_monitor.check_system_state()
            
            if system_changes['regenerate_brain_transport']:
                self._log(f"System changes detected (score: {system_changes['accumulated_score']})", "HEALTH")
                
                if system_changes['changes_summary']:
                    for change in system_changes['changes_summary']:
                        self._log(f"  - {change}", "HEALTH")
                
                self._log("Regenerating Brain Transport...", "TRANSPORT")
                try:
                    self.transport_generator.generate()
                    self._log("Brain Transport regenerated successfully", "TRANSPORT")
                except Exception as e:
                    self._log(f"Error regenerating Brain Transport: {str(e)}", "ERROR")
            
            # Cleanup dead Cascades every 10 cycles (5 minutes at 30s intervals)
            if self.cycle_count % 10 == 0:
                cleaned = self.coordinator.cleanup_dead_cascades(inactivity_threshold_hours=24)
                if cleaned > 0:
                    self._log(f"Cleaned up {cleaned} dead Cascade(s)", "CLEANUP")
        
        except Exception as e:
            self._log(f"Error in cycle: {str(e)}", "ERROR")
            # Continue running despite errors
        
        # Log cycle completion
        cycle_duration = (datetime.now() - cycle_start).total_seconds()
        
        if self.cycle_count % 10 == 0:  # Log every 10 cycles
            self._log(f"Cycle {self.cycle_count} complete ({cycle_duration:.2f}s)", "INFO")
    
    def stop(self):
        """Stop the daemon"""
        self.running = False
        self._log("Brain Sync Daemon stopped")
    
    def get_status(self) -> Dict:
        """Get daemon status"""
        active_cascades = self.coordinator.get_active_cascades()
        
        return {
            'running': self.running,
            'cycle_count': self.cycle_count,
            'check_interval': self.check_interval,
            'active_cascades': len(active_cascades),
            'uptime': 'N/A'  # Would need start time tracking
        }

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Brain Sync Daemon")
    parser.add_argument('--daemon', action='store_true', help="Run as daemon")
    parser.add_argument('--interval', type=int, default=30, help="Check interval in seconds")
    parser.add_argument('--status', action='store_true', help="Show daemon status")
    parser.add_argument('--regenerate-transport', action='store_true', help="Force regenerate Brain Transport now")
    parser.add_argument('--check-health', action='store_true', help="Check system health without regenerating")
    
    args = parser.parse_args()
    
    if args.status:
        # Show status
        coordinator = CascadeCoordinator()
        print(coordinator.get_coordination_status())
        return
    
    if args.regenerate_transport:
        # Force regenerate Brain Transport
        print("🧠 Force regenerating Brain Transport...")
        generator = BrainTransportGenerator()
        generator.generate()
        return
    
    if args.check_health:
        # Check system health
        print("🔍 Checking system health...\n")
        monitor = SystemHealthMonitor()
        result = monitor.check_system_state()
        
        print(f"Accumulated Score: {result['accumulated_score']}/{monitor.REGENERATION_THRESHOLD}")
        print(f"Regenerate Needed: {result['regenerate_brain_transport']}")
        
        if result['changes_summary']:
            print("\nChanges Detected:")
            for change in result['changes_summary']:
                print(f"  - {change}")
        else:
            print("\nNo changes detected")
        
        return
    
    # Start daemon
    daemon = BrainSyncDaemon(check_interval_seconds=args.interval)
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          BRAIN SYNC DAEMON                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Starting Brain synchronization daemon...

Configuration:
  Check Interval: {args.interval} seconds
  Tracked Files: 4 (philosophy, decision_matrix, learning_principles, prompt_gen)
  
Press Ctrl+C to stop

""")
    
    daemon.start()

if __name__ == '__main__':
    main()
