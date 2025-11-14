#!/usr/bin/env python3
"""
8825 Dropbox Watch Service
Monitors Dropbox folder for new JSON files from ChatGPT and auto-moves to inbox.
"""

import os
import time
import json
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Configuration
DROPBOX_WATCH_FOLDER = Path.home() / "Dropbox" / "8825_inbox"
INBOX_PENDING = Path.home() / "Downloads" / "8825_inbox" / "pending"
CHECK_INTERVAL = 5  # seconds
PROCESSED_LOG = Path.home() / "Downloads" / "8825_inbox" / ".processed_files.txt"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_folders():
    """Create necessary folders if they don't exist"""
    DROPBOX_WATCH_FOLDER.mkdir(parents=True, exist_ok=True)
    INBOX_PENDING.mkdir(parents=True, exist_ok=True)
    logger.info(f"Watching: {DROPBOX_WATCH_FOLDER}")
    logger.info(f"Target: {INBOX_PENDING}")

def load_processed_files():
    """Load list of already processed files"""
    if PROCESSED_LOG.exists():
        with open(PROCESSED_LOG, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def mark_as_processed(filename):
    """Mark a file as processed"""
    with open(PROCESSED_LOG, 'a') as f:
        f.write(f"{filename}\n")

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

def process_file(filepath):
    """Move file from Dropbox to inbox"""
    try:
        # Validate JSON
        if not validate_json(filepath):
            logger.warning(f"Skipping invalid file: {filepath.name}")
            return False
        
        # Move to inbox
        dest = INBOX_PENDING / filepath.name
        shutil.move(str(filepath), str(dest))
        
        logger.info(f"✅ Moved to inbox: {filepath.name}")
        mark_as_processed(filepath.name)
        return True
    
    except Exception as e:
        logger.error(f"Error processing {filepath.name}: {e}")
        return False

def watch_folder():
    """Main watch loop"""
    logger.info("=" * 60)
    logger.info("8825 Dropbox Watch Service Started")
    logger.info("=" * 60)
    logger.info(f"Watching: {DROPBOX_WATCH_FOLDER}")
    logger.info(f"Target: {INBOX_PENDING}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info("=" * 60)
    logger.info("Waiting for files... (Press Ctrl+C to stop)")
    logger.info("")
    
    processed_files = load_processed_files()
    
    while True:
        try:
            # Check for JSON files
            json_files = list(DROPBOX_WATCH_FOLDER.glob("*.json"))
            
            for filepath in json_files:
                # Skip if already processed
                if filepath.name in processed_files:
                    continue
                
                # Wait a moment to ensure file is fully written
                time.sleep(1)
                
                # Process the file
                if process_file(filepath):
                    processed_files.add(filepath.name)
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("\n" + "=" * 60)
            logger.info("Dropbox watch service stopped")
            logger.info("=" * 60)
            break
        
        except Exception as e:
            logger.error(f"Error in watch loop: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    ensure_folders()
    watch_folder()
