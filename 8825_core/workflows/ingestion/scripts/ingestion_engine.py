#!/usr/bin/env python3
"""
8825 Ingestion Engine - Core
Central processing system for all incoming data
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

# Add file router to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "config"))
from file_router import get_intake

from utils.logger import log, setup_logging
from utils.tracker import Tracker
from processors.metadata_processor import extract_metadata
from processors.content_processor import analyze_content
from processors.classifier import classify_file
from processors.deduplicator import check_duplicate, handle_duplicate, calculate_hash
from processors.cleanup_manager import CleanupManager
from processors.brain_updater import BrainUpdater
from routers.project_router import route_to_projects
from routers.library_merger import LibraryMerger

# Paths
ENGINE_DIR = Path(__file__).parent.parent
CONFIG_FILE = ENGINE_DIR / "config" / "ingestion_config.json"
DATA_DIR = ENGINE_DIR / "data"
LOGS_DIR = ENGINE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

class IngestionEngine:
    """Main ingestion engine"""
    
    def __init__(self, config_path=CONFIG_FILE):
        """Initialize engine with configuration"""
        self.config = self.load_config(config_path)
        self.tracker = Tracker(DATA_DIR)
        self.library_merger = LibraryMerger()
        self.cleanup_manager = CleanupManager(self.config.get("cleanup"))
        self.brain_updater = BrainUpdater()
        setup_logging(LOGS_DIR / "ingestion.log")
        
        log("🚀 Initializing 8825 Ingestion Engine", "INFO")
        log(f"📁 Config: {config_path}", "INFO")
    
    def load_config(self, config_path):
        """Load configuration file"""
        if not config_path.exists():
            log(f"⚠️  Config not found, using defaults", "WARN")
            return self.default_config()
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def default_config(self):
        """Default configuration"""
        return {
            "sources": {
                "downloads": {
                    "enabled": True,
                    "path": str(get_intake()),
                    "poll_interval": 10
                }
            },
            "processing": {
                "parallel_workers": 2,
                "retry_attempts": 3,
                "timeout_seconds": 60
            },
            "routing": {
                "auto_route_threshold": 70,
                "suggest_threshold": 50
            }
        }
    
    def process_file(self, file_path):
        """
        Process a single file through the ingestion pipeline
        
        Pipeline:
        0. Check for duplicates
        1. Extract metadata
        2. Analyze content
        3. Classify by project
        4. Route to destinations
        5. Merge to libraries
        6. Track processing
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            log(f"⚠️  File not found: {file_path.name}", "WARN")
            return None
        
        log(f"📥 Processing: {file_path.name}", "INFO")
        
        try:
            # Stage 0: Check for duplicates
            log(f"   0️⃣  Checking for duplicates...", "DEBUG")
            duplicate_check = check_duplicate(file_path, self.tracker)
            
            if duplicate_check.get("is_duplicate"):
                match_type = duplicate_check.get("match_type")
                existing = duplicate_check.get("existing_file")
                log(f"   ⚠️  Duplicate detected ({match_type}): {existing}", "INFO")
                
                # Handle duplicate
                handle_result = handle_duplicate(file_path, duplicate_check, self.tracker)
                
                if handle_result.get("action") == "skipped":
                    log(f"⏭️  Skipped duplicate: {file_path.name}", "INFO")
                    return None
                elif handle_result.get("action") == "versioned":
                    new_path = handle_result.get("new_path")
                    log(f"📝 Versioned: {file_path.name} → {Path(new_path).name}", "INFO")
                    file_path = Path(new_path)
            
            # Stage 1: Extract metadata
            log(f"   1️⃣  Extracting metadata...", "DEBUG")
            metadata = extract_metadata(file_path)
            
            # Add content hash to metadata
            metadata["content_hash"] = calculate_hash(file_path)
            
            # Stage 2: Analyze content
            log(f"   2️⃣  Analyzing content...", "DEBUG")
            content_data = analyze_content(file_path, metadata)
            
            # Stage 3: Classify
            log(f"   3️⃣  Classifying...", "DEBUG")
            classification = classify_file(file_path, metadata, content_data, self.config)
            
            # Stage 4: Route
            log(f"   4️⃣  Routing...", "DEBUG")
            routing_result = route_to_projects(
                file_path, 
                classification, 
                self.config
            )
            
            # Stage 5: Merge to libraries
            log(f"   5️⃣  Merging to libraries...", "DEBUG")
            file_data = {
                "metadata": metadata,
                "content_data": content_data
            }
            library_result = self.library_merger.merge_to_library(
                file_data,
                classification,
                routing_result
            )
            
            if library_result.get("merged"):
                library = library_result.get("library")
                action = library_result.get("action")
                log(f"   📚 Library {action}: {library}", "INFO")
                
                # Stage 6: Update Brain (after library merge)
                log(f"   6️⃣  Updating brain...", "DEBUG")
                library_path = self.library_merger.libraries.get(library)
                if library_path:
                    brain_result = self.brain_updater.process_library_update(library, library_path)
                    if brain_result.get("success"):
                        log(f"   🧠 Brain updated: {library}", "DEBUG")
            
            # Stage 7: Track
            result = {
                "filename": file_path.name,
                "processed_at": datetime.now().isoformat(),
                "metadata": metadata,
                "classification": classification,
                "routing": routing_result,
                "library": library_result,
                "duplicate_check": duplicate_check,
                "success": routing_result.get("success", False)
            }
            
            self.tracker.add_processed(result)
            
            # Stage 8: Cleanup
            if result.get("success"):
                log(f"   8️⃣  Cleaning up...", "DEBUG")
                cleanup_result = self.cleanup_manager.process_file(file_path, result)
                result["cleanup"] = cleanup_result
                
                action = cleanup_result.get("action")
                if action == "delete":
                    log(f"   🗑️  Deleted: {file_path.name}", "INFO")
                elif action == "compress":
                    log(f"   📦 Compressed: {file_path.name}", "INFO")
                elif action == "keep":
                    log(f"   📌 Kept: {file_path.name}", "DEBUG")
            
            # Log result
            project = classification.get("project", "Unknown")
            confidence = classification.get("confidence", 0)
            
            if routing_result.get("success"):
                log(f"✅ Processed: {file_path.name} → {project} ({confidence}%)", "INFO")
            else:
                log(f"⚠️  Processing incomplete: {file_path.name}", "WARN")
            
            return result
            
        except Exception as e:
            log(f"❌ Error processing {file_path.name}: {e}", "ERROR")
            self.tracker.add_failed({
                "filename": file_path.name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return None
    
    def scan_ingestion_folder(self):
        """Scan ingestion folder for existing files"""
        source_config = self.config["sources"]["downloads"]
        
        if not source_config["enabled"]:
            log("⏭️  Downloads source disabled", "INFO")
            return
        
        ingestion_path = Path(source_config["path"])
        
        if not ingestion_path.exists():
            log(f"⚠️  Ingestion folder not found: {ingestion_path}", "WARN")
            return
        
        log(f"🔍 Scanning: {ingestion_path}", "INFO")
        
        files = [f for f in ingestion_path.iterdir() if f.is_file()]
        
        if not files:
            log("   No files found", "INFO")
            return
        
        log(f"   Found {len(files)} files", "INFO")
        
        processed_count = 0
        for file_path in files:
            # Skip hidden files and system files
            if file_path.name.startswith('.'):
                continue
            
            result = self.process_file(file_path)
            if result and result.get("success"):
                processed_count += 1
        
        log(f"✅ Scan complete: {processed_count}/{len(files)} processed", "INFO")
    
    def start_monitoring(self):
        """Start real-time monitoring of ingestion folder"""
        source_config = self.config["sources"]["downloads"]
        
        if not source_config["enabled"]:
            log("⏭️  Monitoring disabled", "INFO")
            return
        
        ingestion_path = Path(source_config["path"])
        
        if not ingestion_path.exists():
            log(f"❌ Ingestion folder not found: {ingestion_path}", "ERROR")
            return
        
        log(f"👁️  Monitoring: {ingestion_path}", "INFO")
        
        # Create event handler
        handler = IngestionHandler(self)
        
        # Create observer
        observer = Observer()
        observer.schedule(handler, str(ingestion_path), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log("\n⏹️  Stopping engine...", "INFO")
            observer.stop()
            observer.join()
            log("✅ Engine stopped", "INFO")

class IngestionHandler(FileSystemEventHandler):
    """Handle file system events in ingestion folder"""
    
    def __init__(self, engine):
        self.engine = engine
        self.processing = set()
    
    def on_created(self, event):
        """Handle new file"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip hidden files
        if file_path.name.startswith('.'):
            return
        
        # Avoid duplicate processing
        if file_path in self.processing:
            return
        
        self.processing.add(file_path)
        
        try:
            # Wait for file to finish writing
            time.sleep(1)
            
            log(f"📥 New file detected: {file_path.name}", "INFO")
            self.engine.process_file(file_path)
            
        finally:
            time.sleep(0.5)
            self.processing.discard(file_path)

def main():
    """CLI interface - compatible with old engine"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='8825 Ingestion Engine v2')
    parser.add_argument('command', nargs='?', choices=['process', 'watch', 'stats'], 
                       default='process', help='Command to run')
    parser.add_argument('--file', help='Process specific file')
    parser.add_argument('--scan', action='store_true', help='Scan only, no monitoring')
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = IngestionEngine()
    
    if args.command == 'process':
        # Process mode - scan and exit (compatible with old engine)
        print("="*60)
        print("🚀 8825 INGESTION ENGINE v2")
        print("="*60)
        print()
        
        if args.file:
            # Process single file
            log(f"📥 Processing single file: {args.file}", "INFO")
            result = engine.process_file(Path(args.file))
            if result:
                print(json.dumps(result, indent=2))
        else:
            # Scan and process all files in ingestion folder
            log("🔍 Scanning ingestion folder...", "INFO")
            engine.scan_ingestion_folder()
            
            # Return simple success message
            print("\n✅ Processing complete")
    
    elif args.command == 'watch':
        # Watch mode - continuous monitoring
        print("="*60)
        print("🚀 8825 INGESTION ENGINE v2 - WATCH MODE")
        print("="*60)
        print()
        
        log("🔍 Initial scan...", "INFO")
        engine.scan_ingestion_folder()
        
        print("\n⏳ Starting real-time monitoring... (Press Ctrl+C to stop)\n")
        engine.start_monitoring()
    
    elif args.command == 'stats':
        # Stats mode
        stats = {
            "engine": "v2",
            "config": engine.config,
            "data_dir": str(DATA_DIR)
        }
        print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
