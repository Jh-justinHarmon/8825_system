#!/usr/bin/env python3
"""
Downloads Folder Sync
Keeps Desktop/Downloads and iCloud/Downloads in sync (bidirectional)
Excludes '- old -' folders and 8825_inbox (handled by inbox_sync.py)
"""

import os
import sys
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Paths
DESKTOP_DOWNLOADS = Path.home() / "Downloads"
ICLOUD_DOWNLOADS = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Downloads"

# Exclusions - UPDATED 2025-11-09 to prevent junk re-pollution
EXCLUDE_PATTERNS = [
    "- old -",
    "old",  # Any "old" folder
    ".DS_Store",
    ".tmp",
    "~$",  # Office temp files
    "8825_inbox",  # Handled by inbox_sync.py
    "sticky_",  # Debug sticky note files
    "brainstorm",  # Brainstorm text files
    "client_secret",  # OAuth secrets
    "mythic",  # Mythic JSON files
    "phils_book",  # Phil's book files
    "IMG_",  # iPhone/iPad images (HEIC, jpeg)
]

# Log file
LOG_FILE = Path(__file__).parent / "logs" / "downloads_sync.log"
LOG_FILE.parent.mkdir(exist_ok=True)

def log(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    
    print(log_message)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

def should_exclude(file_path):
    """Check if file should be excluded from sync"""
    path_str = str(file_path)
    
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    
    return False

def sync_file(source_path, dest_folder):
    """
    Copy file from source to destination folder
    
    Args:
        source_path: Path to source file
        dest_folder: Destination folder path
    """
    if should_exclude(source_path):
        log(f"⏭️  Skipping excluded: {source_path.name}", "DEBUG")
        return
    
    if not source_path.exists():
        log(f"⚠️  Source file no longer exists: {source_path.name}", "WARN")
        return
    
    # Preserve relative path structure
    try:
        # Get relative path from source Downloads folder
        if DESKTOP_DOWNLOADS in source_path.parents:
            rel_path = source_path.relative_to(DESKTOP_DOWNLOADS)
        elif ICLOUD_DOWNLOADS in source_path.parents:
            rel_path = source_path.relative_to(ICLOUD_DOWNLOADS)
        else:
            log(f"⚠️  File not in monitored folders: {source_path}", "WARN")
            return
        
        # Build destination path
        dest_path = dest_folder / rel_path
        
        # Skip if destination already exists and is same size
        if dest_path.exists():
            if dest_path.stat().st_size == source_path.stat().st_size:
                return
        
        # Create parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        log(f"✅ Synced: {source_path.name} → {dest_folder.name}/", "INFO")
        
    except Exception as e:
        log(f"❌ Error syncing {source_path.name}: {e}", "ERROR")

def initial_sync():
    """Perform initial sync of both folders"""
    log("🔄 Starting initial sync...", "INFO")
    
    # Sync Desktop → iCloud
    log("📤 Syncing Desktop → iCloud...", "INFO")
    for file_path in DESKTOP_DOWNLOADS.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            sync_file(file_path, ICLOUD_DOWNLOADS)
    
    # Sync iCloud → Desktop
    log("📥 Syncing iCloud → Desktop...", "INFO")
    for file_path in ICLOUD_DOWNLOADS.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            sync_file(file_path, DESKTOP_DOWNLOADS)
    
    log("✅ Initial sync complete", "INFO")

class DownloadsSyncHandler(FileSystemEventHandler):
    """Handle file system events for Downloads folders"""
    
    def __init__(self, source_folder, dest_folder):
        self.source_folder = source_folder
        self.dest_folder = dest_folder
        self.processing = set()  # Track files being processed to avoid loops
    
    def on_created(self, event):
        """Handle file creation"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Avoid processing the same file twice
        if file_path in self.processing:
            return
        
        self.processing.add(file_path)
        
        try:
            # Wait a moment for file to finish writing
            time.sleep(0.5)
            
            log(f"📥 New file detected: {file_path.name}", "INFO")
            sync_file(file_path, self.dest_folder)
            
        finally:
            # Remove from processing set after a delay
            time.sleep(1)
            self.processing.discard(file_path)
    
    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Avoid processing the same file twice
        if file_path in self.processing:
            return
        
        # Only sync if file size changed significantly
        try:
            if file_path.exists() and file_path.stat().st_size > 0:
                sync_file(file_path, self.dest_folder)
        except Exception as e:
            log(f"⚠️  Error checking modified file: {e}", "WARN")

def main():
    """Main entry point"""
    print("="*60)
    print("📂 DOWNLOADS FOLDER SYNC")
    print("="*60)
    print(f"\n📁 Desktop Downloads: {DESKTOP_DOWNLOADS}")
    print(f"☁️  iCloud Downloads:  {ICLOUD_DOWNLOADS}")
    print(f"\n🚫 Excluding: {', '.join(EXCLUDE_PATTERNS)}")
    print("\n" + "="*60 + "\n")
    
    # Check if folders exist
    if not DESKTOP_DOWNLOADS.exists():
        log(f"❌ Desktop Downloads folder not found: {DESKTOP_DOWNLOADS}", "ERROR")
        sys.exit(1)
    
    if not ICLOUD_DOWNLOADS.exists():
        log(f"❌ iCloud Downloads folder not found: {ICLOUD_DOWNLOADS}", "ERROR")
        sys.exit(1)
    
    # Perform initial sync
    initial_sync()
    
    print("\n⏳ Starting live sync... (Press Ctrl+C to stop)\n")
    
    # Create event handlers
    desktop_handler = DownloadsSyncHandler(DESKTOP_DOWNLOADS, ICLOUD_DOWNLOADS)
    icloud_handler = DownloadsSyncHandler(ICLOUD_DOWNLOADS, DESKTOP_DOWNLOADS)
    
    # Create observers
    desktop_observer = Observer()
    desktop_observer.schedule(desktop_handler, str(DESKTOP_DOWNLOADS), recursive=True)
    desktop_observer.start()
    
    icloud_observer = Observer()
    icloud_observer.schedule(icloud_handler, str(ICLOUD_DOWNLOADS), recursive=True)
    icloud_observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping sync...")
        desktop_observer.stop()
        icloud_observer.stop()
        desktop_observer.join()
        icloud_observer.join()
        log("✅ Sync stopped", "INFO")
        print("✅ Sync stopped")

if __name__ == "__main__":
    main()
