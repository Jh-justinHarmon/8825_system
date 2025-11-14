#!/usr/bin/env python3
"""
Meeting Automation Poller
Polls both Otter API and Gmail for new transcripts
"""

import json
import time
import signal
import sys
from pathlib import Path
from datetime import datetime

from dual_source_manager import DualSourceManager
from meeting_processor import MeetingProcessor

class MeetingPoller:
    """Automated polling for meeting transcripts"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.log_file = Path(config_path).parent / "logs/poller.log"
        self.log_file.parent.mkdir(exist_ok=True)
        
        self.pid_file = Path(config_path).parent / ".poller.pid"
        
        self.manager = DualSourceManager(config_path)
        self.processor = MeetingProcessor(config_path)
        
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        self.log("🚀 Meeting Poller initialized", "INFO")
    
    def start(self, daemon: bool = False):
        """Start polling"""
        if self.is_running():
            self.log("⚠️  Poller already running", "WARN")
            return
        
        # Write PID file
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        self.running = True
        self.log("▶️  Starting poller...", "INFO")
        
        try:
            while self.running:
                self._poll_cycle()
                
                # Sleep until next poll
                interval = min(
                    self.config['otter_api']['poll_interval_minutes'],
                    self.config['gmail']['poll_interval_minutes']
                )
                
                if self.running:
                    self.log(f"💤 Sleeping for {interval} minutes...", "INFO")
                    time.sleep(interval * 60)
        
        finally:
            self._cleanup()
    
    def _poll_cycle(self):
        """Single poll cycle"""
        self.log("🔄 Starting poll cycle...", "INFO")
        
        try:
            # Get transcripts from both sources
            transcripts = self.manager.get_transcripts()
            
            if not transcripts:
                self.log("  No new transcripts found", "INFO")
                return
            
            self.log(f"  Found {len(transcripts)} new transcripts", "INFO")
            
            # Process each transcript
            for transcript in transcripts:
                success = self.processor.process(transcript)
                if success:
                    self.log(f"  ✅ Processed: {transcript['title']}", "INFO")
                else:
                    self.log(f"  ❌ Failed: {transcript['title']}", "ERROR")
        
        except Exception as e:
            self.log(f"❌ Poll cycle error: {e}", "ERROR")
    
    def stop(self):
        """Stop polling"""
        if not self.is_running():
            self.log("⚠️  Poller not running", "WARN")
            return
        
        # Read PID and send signal
        with open(self.pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        import os
        os.kill(pid, signal.SIGTERM)
        
        self.log("⏹️  Stopped poller", "INFO")
    
    def is_running(self) -> bool:
        """Check if poller is running"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            import os
            os.kill(pid, 0)  # Check if process exists
            return True
        except:
            return False
    
    def get_status(self) -> dict:
        """Get poller status"""
        return {
            'running': self.is_running(),
            'config': self.config_path.name,
            'health': self.manager.get_health_status()
        }
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.log("🛑 Received shutdown signal", "INFO")
        self.running = False
    
    def _cleanup(self):
        """Cleanup on shutdown"""
        if self.pid_file.exists():
            self.pid_file.unlink()
        self.log("✅ Poller stopped", "INFO")
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Main entry point"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Meeting Automation Poller')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--stop', action='store_true', help='Stop running poller')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    config_path = Path(__file__).parent / args.config
    
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        print("Copy config.example.json to config.json and configure it")
        sys.exit(1)
    
    poller = MeetingPoller(config_path)
    
    if args.stop:
        poller.stop()
    elif args.status:
        status = poller.get_status()
        print(json.dumps(status, indent=2))
    else:
        poller.start(daemon=args.daemon)

if __name__ == '__main__':
    main()
