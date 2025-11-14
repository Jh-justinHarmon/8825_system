#!/usr/bin/env python3
"""
Deduplicator
Detects and handles duplicate files
"""

import hashlib
from pathlib import Path
from difflib import SequenceMatcher

def check_duplicate(file_path, tracker):
    """
    Check if file is a duplicate
    
    Args:
        file_path: Path to file to check
        tracker: Tracker instance with processed files
    
    Returns:
        dict: Duplicate check result
    """
    file_path = Path(file_path)
    
    result = {
        "is_duplicate": False,
        "match_type": None,
        "existing_file": None,
        "action": "process",
        "confidence": 0
    }
    
    # Get processed files
    processed_data = tracker._load_json(tracker.processed_file)
    processed_files = processed_data.get("processed", [])
    
    if not processed_files:
        return result
    
    # Check 1: Exact filename match
    for item in processed_files:
        if item.get("filename") == file_path.name:
            result["is_duplicate"] = True
            result["match_type"] = "exact_filename"
            result["existing_file"] = item.get("filename")
            result["action"] = "skip"
            result["confidence"] = 100
            return result
    
    # Check 2: Content hash (if file exists)
    if file_path.exists():
        file_hash = calculate_hash(file_path)
        
        for item in processed_files:
            existing_hash = item.get("metadata", {}).get("content_hash")
            if existing_hash and existing_hash == file_hash:
                result["is_duplicate"] = True
                result["match_type"] = "content_hash"
                result["existing_file"] = item.get("filename")
                result["action"] = "skip"
                result["confidence"] = 100
                return result
    
    # Check 3: Fuzzy filename match
    for item in processed_files:
        existing_name = item.get("filename", "")
        similarity = calculate_similarity(file_path.name, existing_name)
        
        if similarity > 0.85:  # 85% similar
            result["is_duplicate"] = True
            result["match_type"] = "fuzzy_filename"
            result["existing_file"] = existing_name
            result["action"] = "version"  # Create versioned copy
            result["confidence"] = int(similarity * 100)
            return result
    
    return result

def calculate_hash(file_path, chunk_size=8192):
    """Calculate SHA256 hash of file"""
    sha256 = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def calculate_similarity(str1, str2):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def generate_versioned_name(file_path, version=1):
    """Generate versioned filename"""
    file_path = Path(file_path)
    stem = file_path.stem
    suffix = file_path.suffix
    
    return f"{stem}_v{version}{suffix}"

def handle_duplicate(file_path, duplicate_result, tracker):
    """
    Handle duplicate file based on action
    
    Args:
        file_path: Path to duplicate file
        duplicate_result: Result from check_duplicate
        tracker: Tracker instance
    
    Returns:
        dict: Handling result
    """
    action = duplicate_result.get("action")
    
    if action == "skip":
        return {
            "handled": True,
            "action": "skipped",
            "reason": f"Duplicate of {duplicate_result.get('existing_file')}",
            "new_path": None
        }
    
    elif action == "version":
        # Create versioned filename
        version = 1
        new_name = generate_versioned_name(file_path, version)
        new_path = file_path.parent / new_name
        
        # Increment version if needed
        while new_path.exists():
            version += 1
            new_name = generate_versioned_name(file_path, version)
            new_path = file_path.parent / new_name
        
        # Rename file
        try:
            file_path.rename(new_path)
            return {
                "handled": True,
                "action": "versioned",
                "reason": f"Similar to {duplicate_result.get('existing_file')}",
                "new_path": str(new_path)
            }
        except Exception as e:
            return {
                "handled": False,
                "action": "error",
                "reason": str(e),
                "new_path": None
            }
    
    return {
        "handled": False,
        "action": "unknown",
        "reason": "Unknown action",
        "new_path": None
    }
