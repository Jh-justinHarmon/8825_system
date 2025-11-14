#!/usr/bin/env python3
"""
8825 Inbox Sync
3-way sync for 8825_inbox folders: Desktop ⟷ iCloud ⟷ Dropbox
"""

import os
import sys
import time
import shutil
import hashlib
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Paths
DESKTOP_INBOX = Path.home() / "Downloads" / "8825_inbox"
ICLOUD_INBOX = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Downloads/8825_inbox"
DROPBOX_INBOX = Path.home() / "Dropbox" / "8825_inbox"

ALL_INBOXES = [DESKTOP_INBOX, ICLOUD_INBOX, DROPBOX_INBOX]

# Exclusions
EXCLUDE_PATTERNS = [
    ".DS_Store",
    ".tmp",
    "~$",
    "pending"  # Don't sync the pending folder (MCP handles this)
]

# Log file
LOG_FILE = Path(__file__).parent / "logs" / "inbox_sync.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Track processed files to avoid loops
PROCESSED_FILES = {}

def log(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    
    print(log_message)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

def get_file_hash(file_path):
    """Get MD5 hash of file for deduplication"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        log(f"⚠️  Error hashing {file_path.name}: {e}", "WARN")
        return None

def should_exclude(file_path):
    """Check if file should be excluded from sync"""
    path_str = str(file_path)
    
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    
    return False

def get_inbox_name(inbox_path):
    """Get friendly name for inbox location"""
    path_str = str(inbox_path)
    if "iCloud" in path_str or "CloudDocs" in path_str:
        return "iCloud"
    elif "Dropbox" in path_str:
        return "Dropbox"
    else:
        return "Desktop"

def sync_file_to_all(source_path, source_inbox):
    """
    Sync file from source inbox to all other inboxes
    
    Args:
        source_path: Path to source file
        source_inbox: Source inbox folder
    """
    if should_exclude(source_path):
        return
    
    if not source_path.exists():
        return
    
    # Get file hash for deduplication
    file_hash = get_file_hash(source_path)
    if not file_hash:
        return
    
    # Check if we've already processed this file recently
    if file_hash in PROCESSED_FILES:
        last_time = PROCESSED_FILES[file_hash]
        if (datetime.now() - last_time).seconds < 5:
            return  # Skip if processed in last 5 seconds
    
    PROCESSED_FILES[file_hash] = datetime.now()
    
    try:
        # Get relative path from source inbox
        rel_path = source_path.relative_to(source_inbox)
        source_name = get_inbox_name(source_inbox)
        
        # Sync to all other inboxes
        for dest_inbox in ALL_INBOXES:
            if dest_inbox == source_inbox:
                continue
            
            if not dest_inbox.exists():
                continue
            
            dest_path = dest_inbox / rel_path
            
            # Skip if destination already exists and is same size
            if dest_path.exists():
                if dest_path.stat().st_size == source_path.stat().st_size:
                    continue
            
            # Create parent directories if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            dest_name = get_inbox_name(dest_inbox)
            log(f"✅ [{source_name}] {source_path.name} → [{dest_name}]", "INFO")
        
    except Exception as e:
        log(f"❌ Error syncing {source_path.name}: {e}", "ERROR")

def initial_sync():
    """Perform initial 3-way sync"""
    log("🔄 Starting initial 3-way sync...", "INFO")
    
    # Collect all files from all inboxes
    all_files = {}
    
    for inbox in ALL_INBOXES:
        if not inbox.exists():
            log(f"⚠️  Inbox not found: {inbox}", "WARN")
            continue
        
        inbox_name = get_inbox_name(inbox)
        log(f"📂 Scanning {inbox_name} inbox...", "INFO")
        
        for file_path in inbox.rglob("*"):
            if file_path.is_file() and not should_exclude(file_path):
                file_hash = get_file_hash(file_path)
                if file_hash:
                    if file_hash not in all_files:
                        all_files[file_hash] = []
                    all_files[file_hash].append((file_path, inbox))
    
    # Sync files that don't exist in all locations
    log("🔄 Syncing missing files...", "INFO")
    for file_hash, locations in all_files.items():
        if len(locations) < len([i for i in ALL_INBOXES if i.exists()]):
            # File doesn't exist in all locations, sync it
            source_path, source_inbox = locations[0]
            sync_file_to_all(source_path, source_inbox)
    
    log("✅ Initial sync complete", "INFO")

class InboxSyncHandler(FileSystemEventHandler):
    """Handle file system events for inbox folders"""
    
    def __init__(self, inbox_folder):
        self.inbox_folder = inbox_folder
        self.processing = set()
    
    def on_created(self, event):
        """Handle file creation"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path in self.processing:
            return
        
        self.processing.add(file_path)
        
        try:
            # Wait for file to finish writing
            time.sleep(0.5)
            
            inbox_name = get_inbox_name(self.inbox_folder)
            log(f"📥 [{inbox_name}] New file: {file_path.name}", "INFO")
            sync_file_to_all(file_path, self.inbox_folder)
            
        finally:
            time.sleep(1)
            self.processing.discard(file_path)
    
    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path in self.processing:
            return
        
        try:
            if file_path.exists() and file_path.stat().st_size > 0:
                sync_file_to_all(file_path, self.inbox_folder)
        except Exception as e:
            log(f"⚠️  Error checking modified file: {e}", "WARN")

def main():
    """Main entry point"""
    print("="*60)
    print("📥 8825 INBOX 3-WAY SYNC")
    print("="*60)
    print(f"\n📁 Desktop Inbox: {DESKTOP_INBOX}")
    print(f"☁️  iCloud Inbox:  {ICLOUD_INBOX}")
    print(f"📦 Dropbox Inbox: {DROPBOX_INBOX}")
    print(f"\n🚫 Excluding: {', '.join(EXCLUDE_PATTERNS)}")
    print("\n" + "="*60 + "\n")
    
    # Create inbox folders if they don't exist
    for inbox in ALL_INBOXES:
        inbox.mkdir(parents=True, exist_ok=True)
        if inbox.exists():
            log(f"✅ {get_inbox_name(inbox)} inbox ready", "INFO")
        else:
            log(f"❌ Failed to create {get_inbox_name(inbox)} inbox", "ERROR")
    
    # Perform initial sync
    initial_sync()
    
    print("\n⏳ Starting live 3-way sync... (Press Ctrl+C to stop)\n")
    
    # Create event handlers and observers for each inbox
    observers = []
    
    for inbox in ALL_INBOXES:
        if inbox.exists():
            handler = InboxSyncHandler(inbox)
            observer = Observer()
            observer.schedule(handler, str(inbox), recursive=True)
            observer.start()
            observers.append(observer)
            log(f"👀 Watching {get_inbox_name(inbox)} inbox", "INFO")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping sync...")
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
        log("✅ Sync stopped", "INFO")
        print("✅ Sync stopped")

if __name__ == "__main__":
    main()
