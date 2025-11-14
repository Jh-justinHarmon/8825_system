#!/usr/bin/env python3
"""
Downloads Manager - Enhanced Download Wedge
Handles: Sync + Routing + Document Management + Cleanup

Workflow:
1. Sync Desktop ⟷ iCloud Downloads
2. Copy 8825-created files → [8825/Documents] (filed appropriately)
3. Copy all synced files → [8825/Documents ingestion]
4. Delete filed files from Downloads after 24 hours
"""

import os
import sys
import time
import shutil
import json
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# Add file router to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "8825_core" / "config"))
from file_router import get_root, get_intake

from metadata_extractor import extract_metadata
from content_analyzer import analyze_content
from project_matcher import match_to_project

# Paths
DESKTOP_DOWNLOADS = Path.home() / "Downloads"
ICLOUD_DOWNLOADS = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Downloads"
DOCUMENTS_8825 = get_root()
DOCUMENTS_INGESTION = get_intake()
PROJECT_DIR = Path(__file__).parent
CONFIG_FILE = PROJECT_DIR / "project_contexts.json"
TRACKING_FILE = PROJECT_DIR / "data" / "filed_files.json"

# Exclusions
EXCLUDE_PATTERNS = ["- old -", ".DS_Store", ".tmp", "~$"]

# Log file
LOG_FILE = PROJECT_DIR / "logs" / "manager.log"
LOG_FILE.parent.mkdir(exist_ok=True)
TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
DOCUMENTS_INGESTION.mkdir(parents=True, exist_ok=True)

def log(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

def load_config():
    """Load project contexts configuration"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def load_tracking():
    """Load filed files tracking data"""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, 'r') as f:
            return json.load(f)
    return {"filed_files": []}

def save_tracking(data):
    """Save filed files tracking data"""
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def should_exclude(file_path):
    """Check if file should be excluded"""
    path_str = str(file_path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def is_8825_created(file_path):
    """Check if file was created by 8825 system"""
    # Check filename patterns that indicate 8825 creation
    name = file_path.name.lower()
    
    # 8825 patterns
    patterns = [
        "8825",
        "joju",
        "tgif_meeting",
        "_meeting_",
        "problem_statement",
        "project_brief"
    ]
    
    return any(pattern in name for pattern in patterns)

def get_project_destination(file_path, config):
    """Determine destination folder in Documents based on project match"""
    try:
        metadata = extract_metadata(file_path)
        content_data = analyze_content(file_path, metadata)
        match_result = match_to_project(file_path, metadata, content_data, config)
        
        project = match_result.get("project", "Other")
        confidence = match_result.get("confidence", 0)
        
        # Map projects to Documents subfolders
        project_folders = {
            "RAL": "RAL",
            "HCSS": "HCSS",
            "TGIF": "HCSS/TGIF",
            "76": "76",
            "8825": "8825",
            "Jh": "Jh",
            "Trustybits": "76/Trustybits"
        }
        
        folder = project_folders.get(project, "Other")
        return DOCUMENTS_8825 / folder, project, confidence
        
    except Exception as e:
        log(f"⚠️  Error determining destination: {e}", "WARN")
        return DOCUMENTS_8825 / "Other", "Other", 0

def sync_file(source_path, dest_folder):
    """Sync file between Downloads folders"""
    if should_exclude(source_path):
        return False
    
    if not source_path.exists():
        return False
    
    try:
        # Get relative path
        if DESKTOP_DOWNLOADS in source_path.parents:
            rel_path = source_path.relative_to(DESKTOP_DOWNLOADS)
        elif ICLOUD_DOWNLOADS in source_path.parents:
            rel_path = source_path.relative_to(ICLOUD_DOWNLOADS)
        else:
            return False
        
        dest_path = dest_folder / rel_path
        
        # Skip if already synced
        if dest_path.exists() and dest_path.stat().st_size == source_path.stat().st_size:
            return False
        
        # Copy file
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        log(f"✅ Synced: {source_path.name} → {dest_folder.name}/", "INFO")
        return True
        
    except Exception as e:
        log(f"❌ Error syncing {source_path.name}: {e}", "ERROR")
        return False

def copy_to_ingestion(file_path):
    """Copy file to Documents/ingestion"""
    if should_exclude(file_path):
        return False
    
    try:
        dest_path = DOCUMENTS_INGESTION / file_path.name
        
        # Skip if already exists
        if dest_path.exists():
            return False
        
        shutil.copy2(file_path, dest_path)
        log(f"📥 Ingested: {file_path.name} → Documents/ingestion/", "INFO")
        return True
        
    except Exception as e:
        log(f"❌ Error copying to ingestion: {e}", "ERROR")
        return False

def file_to_documents(file_path, config):
    """File 8825-created file to appropriate Documents subfolder"""
    if should_exclude(file_path):
        return False
    
    try:
        dest_folder, project, confidence = get_project_destination(file_path, config)
        dest_path = dest_folder / file_path.name
        
        # Create destination folder
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(file_path, dest_path)
        log(f"📁 Filed: {file_path.name} → Documents/{project}/ ({confidence}%)", "INFO")
        
        # Track filed file
        tracking = load_tracking()
        tracking["filed_files"].append({
            "filename": file_path.name,
            "filed_at": datetime.now().isoformat(),
            "project": project,
            "confidence": confidence,
            "desktop_path": str(DESKTOP_DOWNLOADS / file_path.name),
            "icloud_path": str(ICLOUD_DOWNLOADS / file_path.name)
        })
        save_tracking(tracking)
        
        return True
        
    except Exception as e:
        log(f"❌ Error filing to documents: {e}", "ERROR")
        return False

def cleanup_old_filed_files():
    """Delete filed files from Downloads after 24 hours"""
    tracking = load_tracking()
    now = datetime.now()
    remaining_files = []
    
    for entry in tracking["filed_files"]:
        filed_at = datetime.fromisoformat(entry["filed_at"])
        age = now - filed_at
        
        if age > timedelta(hours=24):
            # Delete from both Downloads folders
            for path_str in [entry["desktop_path"], entry["icloud_path"]]:
                path = Path(path_str)
                if path.exists():
                    try:
                        path.unlink()
                        log(f"🗑️  Cleaned up: {entry['filename']} (filed {age.days}d ago)", "INFO")
                    except Exception as e:
                        log(f"⚠️  Error deleting {entry['filename']}: {e}", "WARN")
        else:
            remaining_files.append(entry)
    
    # Update tracking
    tracking["filed_files"] = remaining_files
    save_tracking(tracking)

class DownloadsManagerHandler(FileSystemEventHandler):
    """Handle file system events with full workflow"""
    
    def __init__(self, source_folder, dest_folder, config):
        self.source_folder = source_folder
        self.dest_folder = dest_folder
        self.config = config
        self.processing = set()
    
    def on_created(self, event):
        """Handle new file"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path in self.processing or should_exclude(file_path):
            return
        
        self.processing.add(file_path)
        
        try:
            # Wait for file to finish writing
            time.sleep(0.5)
            
            log(f"📥 New file: {file_path.name}", "INFO")
            
            # 1. Sync to other Downloads folder
            synced = sync_file(file_path, self.dest_folder)
            
            # 2. Copy to ingestion
            copy_to_ingestion(file_path)
            
            # 3. If 8825-created, file to Documents
            if is_8825_created(file_path):
                log(f"🔧 8825 file detected: {file_path.name}", "INFO")
                file_to_documents(file_path, self.config)
            
        finally:
            time.sleep(1)
            self.processing.discard(file_path)

def initial_sync(config):
    """Perform initial sync and processing"""
    log("🔄 Starting initial sync...", "INFO")
    
    # Sync Desktop → iCloud
    log("📤 Syncing Desktop → iCloud...", "INFO")
    for file_path in DESKTOP_DOWNLOADS.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            sync_file(file_path, ICLOUD_DOWNLOADS)
            copy_to_ingestion(file_path)
            if is_8825_created(file_path):
                file_to_documents(file_path, config)
    
    # Sync iCloud → Desktop
    log("📥 Syncing iCloud → Desktop...", "INFO")
    for file_path in ICLOUD_DOWNLOADS.rglob("*"):
        if file_path.is_file() and not should_exclude(file_path):
            sync_file(file_path, DESKTOP_DOWNLOADS)
            copy_to_ingestion(file_path)
            if is_8825_created(file_path):
                file_to_documents(file_path, config)
    
    log("✅ Initial sync complete", "INFO")

def main():
    """Main entry point"""
    print("="*60)
    print("📂 DOWNLOADS MANAGER - Enhanced Download Wedge")
    print("="*60)
    print(f"\n📁 Desktop Downloads: {DESKTOP_DOWNLOADS}")
    print(f"☁️  iCloud Downloads:  {ICLOUD_DOWNLOADS}")
    print(f"📂 Documents/8825:     {DOCUMENTS_8825}")
    print(f"📥 Ingestion:          {DOCUMENTS_INGESTION}")
    print(f"\n🚫 Excluding: {', '.join(EXCLUDE_PATTERNS)}")
    print("\n" + "="*60 + "\n")
    
    # Check folders
    if not DESKTOP_DOWNLOADS.exists():
        log(f"❌ Desktop Downloads not found", "ERROR")
        sys.exit(1)
    
    if not ICLOUD_DOWNLOADS.exists():
        log(f"❌ iCloud Downloads not found", "ERROR")
        sys.exit(1)
    
    # Load config
    config = load_config()
    
    # Initial sync and processing
    initial_sync(config)
    
    # Cleanup old files
    log("🗑️  Checking for old filed files...", "INFO")
    cleanup_old_filed_files()
    
    print("\n⏳ Starting live management... (Press Ctrl+C to stop)\n")
    
    # Create handlers
    desktop_handler = DownloadsManagerHandler(DESKTOP_DOWNLOADS, ICLOUD_DOWNLOADS, config)
    icloud_handler = DownloadsManagerHandler(ICLOUD_DOWNLOADS, DESKTOP_DOWNLOADS, config)
    
    # Create observers
    desktop_observer = Observer()
    desktop_observer.schedule(desktop_handler, str(DESKTOP_DOWNLOADS), recursive=True)
    desktop_observer.start()
    
    icloud_observer = Observer()
    icloud_observer.schedule(icloud_handler, str(ICLOUD_DOWNLOADS), recursive=True)
    icloud_observer.start()
    
    try:
        while True:
            time.sleep(3600)  # Check for cleanup every hour
            cleanup_old_filed_files()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping manager...")
        desktop_observer.stop()
        icloud_observer.stop()
        desktop_observer.join()
        icloud_observer.join()
        log("✅ Manager stopped", "INFO")
        print("✅ Manager stopped")

if __name__ == "__main__":
    main()
