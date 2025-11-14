#!/usr/bin/env python3
"""
8825 Universal Inbox Watch Service
Monitors multiple inbox locations and funnels all files to central pending folder.
"""

import os
import time
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import logging

# Configuration
WATCH_LOCATIONS = [
    Path.home() / "Downloads" / "8825_inbox",
    Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Downloads" / "8825_inbox",
    Path.home() / "Dropbox" / "8825_inbox",
    # ADDED 2025-11-12: Monitor raw Downloads folders (not just 8825_inbox subfolders)
    Path.home() / "Downloads",
    Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Downloads"
]

CENTRAL_PENDING = Path.home() / "Downloads" / "8825_inbox" / "pending"
CHECK_INTERVAL = 5  # seconds
PROCESSED_LOG = Path.home() / "Downloads" / "8825_inbox" / ".processed_files.txt"

# Exclusion patterns - files/folders to skip
EXCLUDE_PATTERNS = [
    "8825_processed",
    "8825_inbox",  # Don't double-process
    ".DS_Store",
    "8825_BRAIN_TRANSPORT.json",  # Don't process Brain Transport
    "0-8825_BRAIN_TRANSPORT.json",
    "BRAIN_TRANSPORT.json"
]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_folders():
    """Create necessary folders if they don't exist"""
    for location in WATCH_LOCATIONS:
        location.mkdir(parents=True, exist_ok=True)
    
    CENTRAL_PENDING.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("Watching locations:")
    for i, location in enumerate(WATCH_LOCATIONS, 1):
        status = "✅" if location.exists() else "❌"
        logger.info(f"  {i}. {status} {location}")
    logger.info(f"Central: {CENTRAL_PENDING}")
    logger.info("=" * 60)

def get_file_hash(filepath):
    """Get MD5 hash of file content for deduplication"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        logger.error(f"Error hashing {filepath.name}: {e}")
        return None

def load_processed_files():
    """Load list of already processed file hashes"""
    if PROCESSED_LOG.exists():
        with open(PROCESSED_LOG, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def mark_as_processed(file_hash, filename, source):
    """Mark a file as processed with metadata"""
    with open(PROCESSED_LOG, 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{file_hash}|{filename}|{source}|{timestamp}\n")

def validate_json(filepath):
    """Validate JSON file has required 8825 inbox format"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Check required fields
        required = ['content_type', 'target_focus', 'content', 'metadata']
        if not all(field in data for field in required):
            logger.warning(f"Missing required fields in {filepath.name}")
            return False
        
        # Validate enums
        valid_types = ['mining_report', 'achievement', 'pattern', 'note', 'feature', 'decision']
        valid_focuses = ['joju', 'hcss', 'team76', 'jh']
        
        if data['content_type'] not in valid_types:
            logger.warning(f"Invalid content_type in {filepath.name}: {data['content_type']}")
            return False
        
        if data['target_focus'] not in valid_focuses:
            logger.warning(f"Invalid target_focus in {filepath.name}: {data['target_focus']}")
            return False
        
        return True
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath.name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error validating {filepath.name}: {e}")
        return False

def get_source_name(filepath):
    """Get friendly name for source location"""
    path_str = str(filepath)
    if "iCloud" in path_str or "CloudDocs" in path_str:
        return "iCloud"
    elif "Dropbox" in path_str:
        return "Dropbox"
    else:
        return "Local"

def process_file(filepath, file_hash, processed_hashes):
    """Move file from any inbox to central pending"""
    try:
        # Skip if already processed
        if file_hash in processed_hashes:
            logger.debug(f"Already processed: {filepath.name}")
            # Still remove duplicate
            filepath.unlink()
            return False
        
        # Validate JSON
        if not validate_json(filepath):
            logger.warning(f"Skipping invalid file: {filepath.name}")
            return False
        
        # Move to central pending
        dest = CENTRAL_PENDING / filepath.name
        
        # Handle filename collision
        if dest.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = filepath.stem.split('_')
            dest = CENTRAL_PENDING / f"{name_parts[0]}_{timestamp}_{'_'.join(name_parts[1:])}.json"
        
        shutil.move(str(filepath), str(dest))
        
        source = get_source_name(filepath)
        logger.info(f"✅ [{source}] → {filepath.name}")
        mark_as_processed(file_hash, filepath.name, source)
        processed_hashes.add(file_hash)
        return True
    
    except Exception as e:
        logger.error(f"Error processing {filepath.name}: {e}")
        return False

def should_process(filepath):
    """Check if file should be processed based on exclusion patterns"""
    path_str = str(filepath)
    filename = filepath.name
    
    # Check exclusion patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str or pattern in filename:
            return False
    
    # Skip if in pending folder (that's our destination)
    if filepath.parent == CENTRAL_PENDING:
        return False
    
    # Skip if in processed archive
    if "8825_processed" in path_str:
        return False
    
    return True

def scan_location(location, processed_hashes):
    """Scan a single location for JSON files"""
    if not location.exists():
        return []
    
    try:
        # Get all JSON files, excluding the pending folder itself
        json_files = []
        for filepath in location.glob("*.json"):
            # Apply exclusion filters
            if should_process(filepath):
                json_files.append(filepath)
        
        return json_files
    except Exception as e:
        logger.error(f"Error scanning {location}: {e}")
        return []

def watch_all_locations():
    """Main watch loop for all locations"""
    logger.info("=" * 60)
    logger.info("8825 Universal Inbox Watch Service Started")
    logger.info("=" * 60)
    logger.info(f"Monitoring {len(WATCH_LOCATIONS)} locations")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"Central pending: {CENTRAL_PENDING}")
    logger.info("=" * 60)
    logger.info("Waiting for files... (Press Ctrl+C to stop)")
    logger.info("")
    
    processed_hashes = load_processed_files()
    
    while True:
        try:
            files_found = []
            
            # Scan all locations
            for location in WATCH_LOCATIONS:
                files = scan_location(location, processed_hashes)
                files_found.extend(files)
            
            # Process all found files
            for filepath in files_found:
                # Wait a moment to ensure file is fully written
                time.sleep(1)
                
                # Get file hash for deduplication
                file_hash = get_file_hash(filepath)
                if file_hash:
                    process_file(filepath, file_hash, processed_hashes)
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("\n" + "=" * 60)
            logger.info("Universal inbox watch service stopped")
            logger.info("=" * 60)
            break
        
        except Exception as e:
            logger.error(f"Error in watch loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    ensure_folders()
    watch_all_locations()
