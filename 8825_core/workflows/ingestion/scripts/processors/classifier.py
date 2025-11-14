#!/usr/bin/env python3
"""
Classifier
Classifies files by project and confidence
"""

from pathlib import Path

def classify_file(file_path, metadata, content_data, config):
    """
    Classify file by project
    
    Returns:
        dict: Classification with project, confidence, category, tags
    """
    filename = Path(file_path).name.lower()
    keywords = content_data.get("keywords", [])
    entities = content_data.get("entities", [])
    
    # Project scoring
    scores = {
        "RAL": 0,
        "HCSS": 0,
        "TGIF": 0,
        "76": 0,
        "8825": 0,
        "Jh": 0,
        "Trustybits": 0,
        "WHEN76": 0
    }
    
    # Filename patterns
    if "joju" in filename:
        scores["76"] += 40
    if "8825" in filename:
        scores["8825"] += 40
    if "tgif" in filename or "meeting" in filename:
        scores["TGIF"] += 40
    if "hcss" in filename or "hammer" in filename:
        scores["HCSS"] += 30
    if "trusty" in filename or "forge" in filename:
        scores["Trustybits"] += 40
    if "when76" in filename or "when" in filename:
        scores["WHEN76"] += 40
    
    # Keyword scoring
    for keyword in keywords:
        if keyword in ["joju", "profile"]:
            scores["76"] += 15
        elif keyword in ["8825", "problem", "statement", "brief"]:
            scores["8825"] += 15
        elif keyword in ["tgif", "meeting"]:
            scores["TGIF"] += 15
        elif keyword in ["hcss", "business"]:
            scores["HCSS"] += 10
        elif keyword in ["trustybits", "forge"]:
            scores["Trustybits"] += 15
        elif keyword in ["when76", "when", "availability", "schedule", "group", "calendar", "time", "block"]:
            scores["WHEN76"] += 15
        elif keyword in ["ux", "design", "strategy"]:
            scores["76"] += 5
    
    # Entity scoring
    for entity in entities:
        if entity.get("name") in ["Trustybits", "Forge"]:
            scores["Trustybits"] += 10
        elif entity.get("name") == "HCSS":
            scores["HCSS"] += 10
    
    # Find best match
    best_project = max(scores, key=scores.get)
    confidence = min(scores[best_project], 100)
    
    # Determine subfolder based on best match
    subfolder = None
    
    # If Trustybits or WHEN76 scored high, map to 76
    if best_project == "Trustybits":
        best_project = "76"
        confidence = min(confidence + 10, 100)  # Boost confidence for 76
        subfolder = "Trustybits"
    elif best_project == "WHEN76":
        best_project = "76"
        confidence = min(confidence + 10, 100)
        subfolder = "when76"
    # If TGIF scored high, it's actually HCSS
    elif best_project == "TGIF":
        best_project = "HCSS"
        subfolder = "TGIF"
    
    # Determine category
    category = determine_category(metadata, content_data, keywords)
    
    # Generate tags
    tags = list(set(keywords[:5]))  # Top 5 unique keywords
    
    return {
        "project": best_project,
        "subfolder": subfolder,
        "confidence": confidence,
        "category": category,
        "tags": tags,
        "scores": scores  # Include all scores for debugging
    }

def determine_category(metadata, content_data, keywords):
    """Determine file category"""
    file_category = metadata.get("category", "other")
    
    # Map to semantic categories
    if file_category == "document":
        if any(k in keywords for k in ["meeting", "summary"]):
            return "Meeting Notes"
        elif any(k in keywords for k in ["problem", "statement"]):
            return "Problem Statement"
        elif any(k in keywords for k in ["brief", "project"]):
            return "Project Brief"
        else:
            return "Documentation"
    elif file_category == "spreadsheet":
        return "Data/Spreadsheet"
    elif file_category == "presentation":
        return "Presentation"
    elif file_category == "image":
        return "Image/Visual"
    elif file_category == "code":
        return "Code/Config"
    else:
        return "Other"
