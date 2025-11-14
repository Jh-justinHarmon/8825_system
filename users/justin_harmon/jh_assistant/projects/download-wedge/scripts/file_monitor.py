#!/usr/bin/env python3
"""
Download Folder Wedge - File Monitor
Watches download folders and triggers analysis for new files
"""

import os
import sys
import time
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from metadata_extractor import extract_metadata
from content_analyzer import analyze_content
from project_matcher import match_to_project
from router import route_file

# Paths
PROJECT_DIR = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_DIR / "project_contexts.json"
LOG_FILE = PROJECT_DIR / "logs" / "wedge.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Load configuration
def load_config():
    """Load project contexts configuration"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# Logging
def log(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    
    print(log_message)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

class DownloadHandler(FileSystemEventHandler):
    """Handle file system events in download folders"""
    
    def __init__(self, config):
        self.config = config
        self.processing = set()  # Track files being processed
    
    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Skip if already processing
        if file_path in self.processing:
            return
        
        # Skip temporary files
        if self._is_temp_file(file_path):
            return
        
        # Wait for file to finish downloading
        time.sleep(1)
        
        # Process the file
        self.process_file(file_path)
    
    def _is_temp_file(self, file_path):
        """Check if file is temporary"""
        temp_extensions = ['.crdownload', '.part', '.tmp', '.download']
        temp_prefixes = ['.', '~$']
        
        filename = os.path.basename(file_path)
        
        # Check extensions
        if any(file_path.endswith(ext) for ext in temp_extensions):
            return True
        
        # Check prefixes
        if any(filename.startswith(prefix) for prefix in temp_prefixes):
            return True
        
        return False
    
    def process_file(self, file_path):
        """Process a new file"""
        self.processing.add(file_path)
        
        try:
            log(f"📥 New file detected: {os.path.basename(file_path)}")
            
            # Step 1: Extract metadata
            log("📋 Extracting metadata...")
            metadata = extract_metadata(file_path)
            
            # Step 2: Analyze content (if needed)
            log("🔍 Analyzing content...")
            content_data = analyze_content(file_path, metadata)
            
            # Step 3: Match to project
            log("🎯 Matching to project...")
            match_result = match_to_project(file_path, metadata, content_data, self.config)
            
            # Step 4: Route file
            log(f"📂 Routing decision: {match_result['project']} ({match_result['confidence']}%)")
            route_file(file_path, match_result, self.config)
            
            log(f"✅ Processing complete for {os.path.basename(file_path)}\n")
            
        except Exception as e:
            log(f"❌ Error processing {file_path}: {str(e)}", "ERROR")
        
        finally:
            self.processing.discard(file_path)

def main():
    """Main function to start file monitoring"""
    print("🚀 Download Folder Wedge - File Monitor")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Monitor locations
    monitor_paths = [
        os.path.expanduser("~/Downloads/"),
        os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/")
    ]
    
    # Filter to existing paths
    monitor_paths = [p for p in monitor_paths if os.path.exists(p)]
    
    if not monitor_paths:
        print("❌ No download folders found to monitor")
        return
    
    print(f"\n📂 Monitoring {len(monitor_paths)} location(s):")
    for path in monitor_paths:
        print(f"   - {path}")
    
    print(f"\n🎯 Configured for {len(config['projects'])} projects:")
    for project_name in config['projects'].keys():
        print(f"   - {project_name}")
    
    print("\n⏳ Watching for new files... (Press Ctrl+C to stop)\n")
    
    # Create event handler
    event_handler = DownloadHandler(config)
    
    # Create observers for each path
    observers = []
    for path in monitor_paths:
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        observers.append(observer)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping file monitor...")
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
        print("✅ File monitor stopped")

if __name__ == "__main__":
    main()
