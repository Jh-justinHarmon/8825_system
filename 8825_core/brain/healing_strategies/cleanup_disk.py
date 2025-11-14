#!/usr/bin/env python3
"""
Cleanup Disk Healing Strategy
Frees disk space by cleaning old files
"""

import subprocess
from typing import Dict, Any
from pathlib import Path
from datetime import datetime, timedelta

class CleanupDiskStrategy:
    """Strategy to free disk space"""
    
    def heal(self, issue: Dict[str, Any], brain_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Heal by cleaning up old files
        
        Args:
            issue: Issue details
            brain_state: Current brain state
        
        Returns:
            Healing result
        """
        
        # Find old files to clean
        old_files = self.find_old_files()
        
        if not old_files:
            return {
                "success": False,
                "error": "No old files found to clean"
            }
        
        # Move to deep archive
        freed_space = 0
        moved_count = 0
        
        for file_path in old_files:
            try:
                size = file_path.stat().st_size
                self.move_to_archive(file_path)
                freed_space += size
                moved_count += 1
            except Exception as e:
                print(f"  ⚠️  Failed to archive {file_path}: {e}")
        
        freed_gb = freed_space / (1024**3)
        
        return {
            "success": True,
            "message": f"Freed {freed_gb:.2f}GB by archiving {moved_count} files",
            "freed_bytes": freed_space,
            "files_moved": moved_count
        }
    
    def find_old_files(self, age_days: int = 30) -> list:
        """Find files older than age_days"""
        old_files = []
        cutoff = datetime.now() - timedelta(days=age_days)
        
        # Search in common archive locations
        search_paths = [
            Path.home() / "Downloads" / "8825_archive",
            Path.home() / "Downloads" / "8825_inbox" / "archive"
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            for file_path in search_path.rglob("*"):
                if not file_path.is_file():
                    continue
                
                # Check age
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff:
                    old_files.append(file_path)
        
        return old_files[:50]  # Limit to 50 files per cleanup
    
    def move_to_archive(self, file_path: Path):
        """Move file to deep archive"""
        deep_archive = Path.home() / "Downloads" / "8825_deep_archive"
        deep_archive.mkdir(exist_ok=True)
        
        # Preserve directory structure
        relative = file_path.relative_to(Path.home() / "Downloads")
        target = deep_archive / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        file_path.rename(target)
