#!/usr/bin/env python3
"""
Tracker utility for 8825 Ingestion Engine
Tracks processed files, queue, and failures
"""

import json
from pathlib import Path
from datetime import datetime

class Tracker:
    """Track ingestion activity"""
    
    def __init__(self, data_dir):
        """Initialize tracker with data directory"""
        self.data_dir = Path(data_dir)
        self.processed_file = self.data_dir / "processed_files.json"
        self.queue_file = self.data_dir / "ingestion_queue.json"
        self.failed_file = self.data_dir / "failed_items.json"
        
        # Ensure files exist
        self._init_file(self.processed_file, {"processed": []})
        self._init_file(self.queue_file, {"queue": []})
        self._init_file(self.failed_file, {"failed": []})
    
    def _init_file(self, file_path, default_data):
        """Initialize JSON file if it doesn't exist"""
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def _load_json(self, file_path):
        """Load JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _save_json(self, file_path, data):
        """Save JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def is_processed(self, file_path):
        """Check if file has been processed"""
        data = self._load_json(self.processed_file)
        filename = Path(file_path).name
        
        for item in data["processed"]:
            if item.get("filename") == filename:
                return True
        
        return False
    
    def add_processed(self, result):
        """Add processed file to registry"""
        data = self._load_json(self.processed_file)
        data["processed"].append(result)
        self._save_json(self.processed_file, data)
    
    def add_to_queue(self, item):
        """Add item to processing queue"""
        data = self._load_json(self.queue_file)
        data["queue"].append({
            **item,
            "queued_at": datetime.now().isoformat()
        })
        self._save_json(self.queue_file, data)
    
    def remove_from_queue(self, filename):
        """Remove item from queue"""
        data = self._load_json(self.queue_file)
        data["queue"] = [
            item for item in data["queue"] 
            if item.get("filename") != filename
        ]
        self._save_json(self.queue_file, data)
    
    def add_failed(self, error_info):
        """Add failed item to log"""
        data = self._load_json(self.failed_file)
        data["failed"].append(error_info)
        self._save_json(self.failed_file, data)
    
    def get_stats(self):
        """Get processing statistics"""
        processed_data = self._load_json(self.processed_file)
        queue_data = self._load_json(self.queue_file)
        failed_data = self._load_json(self.failed_file)
        
        return {
            "total_processed": len(processed_data["processed"]),
            "in_queue": len(queue_data["queue"]),
            "failed": len(failed_data["failed"])
        }
