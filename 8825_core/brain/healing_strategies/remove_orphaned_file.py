#!/usr/bin/env python3
"""
Remove Orphaned File Healing Strategy
Removes orphaned PID files, sockets, etc.
"""

import os
from typing import Dict, Any
from pathlib import Path

class RemoveOrphanedFileStrategy:
    """Strategy to remove orphaned files"""
    
    def heal(self, issue: Dict[str, Any], brain_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Heal by removing orphaned file
        
        Args:
            issue: Issue details
            brain_state: Current brain state
        
        Returns:
            Healing result
        """
        
        file_path = issue.get('file')
        if not file_path:
            return {
                "success": False,
                "error": "No file specified"
            }
        
        try:
            # Remove file
            path = Path(file_path)
            if path.exists():
                path.unlink()
                
                return {
                    "success": True,
                    "message": f"Removed orphaned file: {file_path}"
                }
            else:
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
