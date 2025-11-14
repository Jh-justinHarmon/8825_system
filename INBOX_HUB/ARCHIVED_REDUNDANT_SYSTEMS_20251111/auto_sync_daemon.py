#!/usr/bin/env python3
"""
Input Hub Phase 2: Auto-Sync Daemon
Watches source directories and auto-syncs files to intake folders
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
HOME = Path.home()
SCRIPT_DIR = Path(__file__).parent.resolve()

# Source directories to watch
WATCH_DIRS = [
    HOME / "Desktop",
    HOME / "Downloads",
    HOME / "Hammer Consulting Dropbox" / "Justin Harmon" / "Screenshots",
]

# Intake destinations
INTAKE_SCREENSHOTS = SCRIPT_DIR / "users" / "jh" / "intake" / "screenshots"
INTAKE_DOCUMENTS = SCRIPT_DIR / "users" / "jh" / "intake" / "documents"
INTAKE_UPLOADS = SCRIPT_DIR / "users" / "jh" / "intake" / "uploads"

# File type mappings
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'}
DOCUMENT_EXTENSIONS = {'.json', '.md', '.txt', '.docx', '.pdf', '.doc', '.rtf'}

# Ensure intake directories exist
INTAKE_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
INTAKE_DOCUMENTS.mkdir(parents=True, exist_ok=True)
INTAKE_UPLOADS.mkdir(parents=True, exist_ok=True)


def get_destination(file_path: Path) -> Path:
    """Determine destination based on file extension"""
    ext = file_path.suffix.lower()
    
    if ext in IMAGE_EXTENSIONS:
        return INTAKE_SCREENSHOTS
    elif ext in DOCUMENT_EXTENSIONS:
        return INTAKE_DOCUMENTS
    else:
        return INTAKE_UPLOADS


def should_sync(file_path: Path) -> bool:
    """Check if file should be synced"""
    # Skip hidden files
    if file_path.name.startswith('.'):
        return False
    
    # Skip temp files
    if file_path.name.endswith('.tmp') or file_path.name.endswith('.crdownload'):
        return False
    
    # Only sync specific patterns
    name = file_path.name
    ext = file_path.suffix.lower()
    
    # Screenshots
    if any(name.startswith(prefix) for prefix in ['Screenshot', 'Screen Shot', 'CleanShot']):
        return True
    
    # Documents and images
    if ext in IMAGE_EXTENSIONS or ext in DOCUMENT_EXTENSIONS:
        return True
    
    return False


def sync_file(file_path: Path):
    """Sync a single file to appropriate intake folder"""
    if not file_path.exists() or not file_path.is_file():
        return
    
    if not should_sync(file_path):
        return
    
    dest_dir = get_destination(file_path)
    dest_path = dest_dir / file_path.name
    
    # Skip if already exists
    if dest_path.exists():
        return
    
    try:
        # Copy with metadata preserved
        shutil.copy2(file_path, dest_path)
        
        # Log the sync
        file_type = "IMG" if dest_dir == INTAKE_SCREENSHOTS else "DOC" if dest_dir == INTAKE_DOCUMENTS else "FILE"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✓ [{file_type}] {file_path.name}")
        
    except Exception as e:
        print(f"[ERROR] Failed to sync {file_path.name}: {e}")


class InputHubHandler(FileSystemEventHandler):
    """Handle file system events for auto-sync"""
    
    def on_created(self, event):
        """Handle file creation"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Wait a moment for file to finish writing
        time.sleep(0.5)
        
        sync_file(file_path)
    
    def on_modified(self, event):
        """Handle file modification (for downloads completing)"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Only sync if it's a new file (not already in intake)
        if not any(str(file_path).startswith(str(intake)) for intake in [INTAKE_SCREENSHOTS, INTAKE_DOCUMENTS, INTAKE_UPLOADS]):
            time.sleep(0.5)
            sync_file(file_path)


def main():
    """Start the auto-sync daemon"""
    print("🚀 Input Hub Phase 2: Auto-Sync Daemon")
    print("=" * 50)
    print(f"Watching {len(WATCH_DIRS)} directories:")
    for watch_dir in WATCH_DIRS:
        if watch_dir.exists():
            print(f"  ✓ {watch_dir}")
        else:
            print(f"  ✗ {watch_dir} (not found)")
    print()
    print("Syncing to:")
    print(f"  Screenshots: {INTAKE_SCREENSHOTS}")
    print(f"  Documents:   {INTAKE_DOCUMENTS}")
    print(f"  Uploads:     {INTAKE_UPLOADS}")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 50)
    print()
    
    # Create observer and handlers
    observer = Observer()
    handler = InputHubHandler()
    
    # Watch each directory
    for watch_dir in WATCH_DIRS:
        if watch_dir.exists():
            observer.schedule(handler, str(watch_dir), recursive=False)
    
    # Start watching
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping auto-sync daemon...")
        observer.stop()
    
    observer.join()
    print("✓ Auto-sync daemon stopped")


if __name__ == "__main__":
    main()
