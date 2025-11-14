#!/usr/bin/env python3
"""
Project Router
Routes files to appropriate project folders
"""

import sys
import shutil
from pathlib import Path

# Add file router to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "config"))
from file_router import get_root, get_destination

def route_to_projects(file_path, classification, config):
    """
    Route file to project folders based on classification
    
    Args:
        file_path: Source file path
        classification: Classification dict from classifier
        config: Engine configuration
    
    Returns:
        dict: Routing result with success status and destinations
    """
    file_path = Path(file_path)
    project = classification.get("project", "Other")
    subfolder = classification.get("subfolder")
    confidence = classification.get("confidence", 0)
    
    # Get routing threshold
    auto_route_threshold = config.get("routing", {}).get("auto_route_threshold", 70)
    
    result = {
        "success": False,
        "destinations": [],
        "action": None,
        "confidence": confidence
    }
    
    # Determine action based on confidence
    if confidence >= auto_route_threshold:
        result["action"] = "auto_route"
    else:
        result["action"] = "manual_review"
        result["success"] = True  # Mark as success but no routing
        return result
    
    # Build destination path using file router
    project_base = get_destination(project)
    if subfolder:
        dest_folder = project_base / subfolder
    else:
        dest_folder = project_base
    
    # Ensure destination exists
    dest_folder.mkdir(parents=True, exist_ok=True)
    
    # Copy file (don't move, keep in ingestion)
    dest_path = dest_folder / file_path.name
    
    try:
        # Skip if already exists
        if dest_path.exists():
            result["success"] = True
            result["destinations"].append(str(dest_path))
            result["note"] = "File already exists at destination"
            return result
        
        # Copy file
        shutil.copy2(file_path, dest_path)
        
        result["success"] = True
        result["destinations"].append(str(dest_path))
        
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
    
    return result
