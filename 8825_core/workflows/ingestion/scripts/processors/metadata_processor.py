#!/usr/bin/env python3
"""
Metadata Processor
Extracts file metadata for classification
"""

import os
from pathlib import Path
from datetime import datetime

def extract_metadata(file_path):
    """
    Extract metadata from file
    
    Returns:
        dict: Metadata including filename, size, dates, type
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {}
    
    stat = file_path.stat()
    
    metadata = {
        "filename": file_path.name,
        "extension": file_path.suffix.lower(),
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "category": categorize_by_extension(file_path.suffix.lower())
    }
    
    return metadata

def categorize_by_extension(extension):
    """Categorize file by extension"""
    categories = {
        "document": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"],
        "spreadsheet": [".xls", ".xlsx", ".csv", ".numbers"],
        "presentation": [".ppt", ".pptx", ".key"],
        "image": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
        "video": [".mp4", ".mov", ".avi", ".mkv"],
        "audio": [".mp3", ".wav", ".m4a", ".aac"],
        "archive": [".zip", ".tar", ".gz", ".rar", ".7z"],
        "code": [".py", ".js", ".html", ".css", ".json", ".xml"],
        "3d": [".3dm", ".stl", ".obj", ".fbx"],
        "design": [".psd", ".ai", ".sketch", ".fig"]
    }
    
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    
    return "other"
