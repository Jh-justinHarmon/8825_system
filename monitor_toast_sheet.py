#!/usr/bin/env python3
"""
Monitor Toast Installation Schedule for changes
Sends macOS notifications and email alerts when sheet is updated
"""

import time
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from toast_sheet_manager import ToastScheduleManager
import subprocess

class SheetMonitor:
    def __init__(self, check_interval=300):  # 5 minutes default
        self.check_interval = check_interval
        self.state_file = Path.home() / '.config' / 'toast_monitor_state.json'
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.manager = ToastScheduleManager()
        self.manager.connect("Toast Equipment Schedule")
        
    def get_sheet_hash(self, data):
        """Create hash of sheet data to detect changes"""
        return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def load_state(self):
        """Load previous state"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return None
    
    def save_state(self, data, data_hash):
        """Save current state"""
        state = {
            'hash': data_hash,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.state_file.write_text(json.dumps(state, indent=2))
    
    def send_macos_notification(self, title, message):
        """Send macOS notification banner"""
        script = f'''
        display notification "{message}" with title "{title}" sound name "Glass"
        '''
        subprocess.run(['osascript', '-e', script])
    
    def send_email_alert(self, subject, body):
        """Send email alert via Gmail"""
        sender = "harmon.justin@gmail.com"
        recipient = "harmon.justin@gmail.com"
        password = "tyit dhqe twcv qmdf"  # App password from memory
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = f"Toast Schedule Alert: {subject}"
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.send_message(msg)
            print(f"✓ Email sent: {subject}")
        except Exception as e:
            print(f"✗ Email failed: {e}")
    
    def detect_changes(self, old_data, new_data):
        """Detect what changed between two states"""
        changes = []
        
        old_dict = {store['Store ID']: store for store in old_data}
        new_dict = {store['Store ID']: store for store in new_data}
        
        for store_id, new_store in new_dict.items():
            if store_id in old_dict:
                old_store = old_dict[store_id]
                store_changes = []
                
                for field in ['Toast Equipment Status', 'Network Equipment Status', 
                             'On-Site Resources Status', 'Notes']:
                    if old_store.get(field) != new_store.get(field):
                        store_changes.append({
                            'field': field,
                            'old': old_store.get(field, 'N/A'),
                            'new': new_store.get(field, 'N/A')
                        })
                
                if store_changes:
                    changes.append({
                        'store_id': store_id,
                        'location': new_store['Location'],
                        'changes': store_changes
                    })
        
        return changes
    
    def format_changes_message(self, changes):
        """Format changes for notification"""
        if not changes:
            return "No changes detected"
        
        msg = []
        for change in changes:
            msg.append(f"\n{change['store_id']} - {change['location']}:")
            for field_change in change['changes']:
                msg.append(f"  {field_change['field']}:")
                msg.append(f"    Was: {field_change['old'][:50]}...")
                msg.append(f"    Now: {field_change['new'][:50]}...")
        
        return '\n'.join(msg)
    
    def check_for_updates(self):
        """Check sheet for updates"""
        current_data = self.manager.get_all_stores()
        current_hash = self.get_sheet_hash(current_data)
        
        previous_state = self.load_state()
        
        if previous_state is None:
            # First run - just save state
            print("First run - saving initial state")
            self.save_state(current_data, current_hash)
            return
        
        if current_hash != previous_state['hash']:
            # Changes detected!
            changes = self.detect_changes(previous_state['data'], current_data)
            
            if changes:
                print(f"\n{'='*60}")
                print(f"CHANGES DETECTED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                changes_msg = self.format_changes_message(changes)
                print(changes_msg)
                
                # Send notifications
                self.send_macos_notification(
                    "Toast Schedule Updated",
                    f"{len(changes)} store(s) updated"
                )
                
                self.send_email_alert(
                    f"{len(changes)} Store Update(s)",
                    changes_msg
                )
                
                # Save new state
                self.save_state(current_data, current_hash)
            else:
                print("Hash changed but no meaningful changes detected")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No changes")
    
    def run(self):
        """Run monitoring loop"""
        print("="*60)
        print("TOAST SCHEDULE MONITOR")
        print("="*60)
        print(f"Checking every {self.check_interval} seconds")
        print(f"Notifications: macOS banner + Email to harmon.justin@gmail.com")
        print(f"Press Ctrl+C to stop")
        print("="*60)
        
        try:
            while True:
                self.check_for_updates()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped")


if __name__ == "__main__":
    import sys
    
    # Default: check every 5 minutes
    interval = 300
    
    if len(sys.argv) > 1:
        interval = int(sys.argv[1])
    
    monitor = SheetMonitor(check_interval=interval)
    monitor.run()
