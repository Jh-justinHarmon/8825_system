#!/usr/bin/env python3
"""
Cleanup Manager - Stage 8
Post-ingestion file cleanup: delete, compress, or keep
"""

import os
import gzip
import shutil
from pathlib import Path
from datetime import datetime

class CleanupManager:
    """Manage post-ingestion file cleanup"""
    
    def __init__(self, config=None):
        self.config = config or self._default_config()
    
    def _default_config(self):
        """Default cleanup configuration"""
        return {
            "enabled": True,
            "delete_simple_files": True,
            "compress_complex_files": True,
            "compress_threshold_mb": 10,
            "keep_originals": ["3dm", "psd", "ai", "fig", "mp4", "mov"]
        }
    
    def assess_file(self, file_path, processing_result):
        """
        Assess what to do with file after ingestion
        
        Returns:
            dict: Cleanup action and reasoning
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {"action": "none", "reason": "file_not_found"}
        
        # Check if ingestion was successful
        if not processing_result.get("success"):
            return {"action": "keep", "reason": "ingestion_failed"}
        
        # Get file info
        extension = file_path.suffix.lower()
        size_mb = file_path.stat().st_size / (1024 * 1024)
        
        # Check if library captured the file
        library_merged = processing_result.get("library", {}).get("merged", False)
        
        # Determine action
        if extension in self.config.get("keep_originals", []):
            return {
                "action": "keep",
                "reason": "original_required",
                "details": f"Format {extension} needs original"
            }
        
        if self._is_simple_file(extension) and library_merged:
            return {
                "action": "delete",
                "reason": "fully_captured",
                "details": "Simple file fully captured in library"
            }
        
        if size_mb > self.config.get("compress_threshold_mb", 10) and library_merged:
            return {
                "action": "compress",
                "reason": "large_file",
                "details": f"File size {size_mb:.1f}MB exceeds threshold"
            }
        
        if self._is_complex_file(extension) and library_merged:
            return {
                "action": "compress",
                "reason": "complex_format",
                "details": f"Complex format {extension} may need reference"
            }
        
        return {
            "action": "keep",
            "reason": "default_keep",
            "details": "Keeping as fallback"
        }
    
    def _is_simple_file(self, extension):
        """Check if file is simple format"""
        simple_formats = [".txt", ".md", ".json", ".csv", ".log"]
        return extension in simple_formats
    
    def _is_complex_file(self, extension):
        """Check if file is complex format"""
        complex_formats = [".pdf", ".docx", ".xlsx", ".pptx", ".png", ".jpg", ".jpeg"]
        return extension in complex_formats
    
    def execute_cleanup(self, file_path, assessment):
        """
        Execute cleanup action
        
        Returns:
            dict: Cleanup result
        """
        file_path = Path(file_path)
        action = assessment.get("action")
        
        result = {
            "success": False,
            "action": action,
            "original_path": str(file_path),
            "new_path": None,
            "error": None
        }
        
        try:
            if action == "delete":
                file_path.unlink()
                result["success"] = True
                result["message"] = f"Deleted {file_path.name}"
            
            elif action == "compress":
                compressed_path = self._compress_file(file_path)
                if compressed_path:
                    file_path.unlink()  # Delete original after compression
                    result["success"] = True
                    result["new_path"] = str(compressed_path)
                    result["message"] = f"Compressed {file_path.name}"
            
            elif action == "keep":
                result["success"] = True
                result["message"] = f"Kept {file_path.name}"
            
            else:
                result["message"] = f"No action for {file_path.name}"
        
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Error: {e}"
        
        return result
    
    def _compress_file(self, file_path):
        """Compress file using gzip"""
        file_path = Path(file_path)
        compressed_path = file_path.parent / f"{file_path.name}.gz"
        
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            return compressed_path
        except Exception:
            return None
    
    def process_file(self, file_path, processing_result):
        """
        Complete cleanup process for a file
        
        Returns:
            dict: Cleanup result
        """
        if not self.config.get("enabled", True):
            return {
                "success": True,
                "action": "skip",
                "message": "Cleanup disabled"
            }
        
        # Assess what to do
        assessment = self.assess_file(file_path, processing_result)
        
        # Execute action
        result = self.execute_cleanup(file_path, assessment)
        
        # Add assessment details
        result["assessment"] = assessment
        result["timestamp"] = datetime.now().isoformat()
        
        return result
