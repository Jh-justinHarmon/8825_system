#!/usr/bin/env python3
"""
Content Processor
Analyzes file content for classification
"""

import re
from pathlib import Path

def analyze_content(file_path, metadata):
    """
    Analyze file content
    
    Args:
        file_path: Path to file
        metadata: Metadata dict from metadata_processor
    
    Returns:
        dict: Content analysis results
    """
    category = metadata.get('category', 'other')
    extension = metadata.get('extension', '')
    
    content_data = {
        "text_sample": "",
        "keywords": [],
        "entities": [],
        "has_content": False
    }
    
    # Text files - read directly
    if category == "document" and extension in [".txt", ".md"]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read(5000)  # First 5000 chars
                content_data["text_sample"] = text[:500]
                content_data["keywords"] = extract_keywords(text)
                content_data["entities"] = extract_entities(text)
                content_data["has_content"] = True
        except Exception:
            pass
    
    # JSON files
    elif extension == ".json":
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read(5000)
                content_data["keywords"] = extract_keywords(text)
                content_data["has_content"] = True
        except Exception:
            pass
    
    # For other files, rely on filename
    else:
        filename_lower = Path(file_path).name.lower()
        content_data["keywords"] = extract_keywords(filename_lower)
    
    return content_data

def extract_keywords(text):
    """Extract keywords from text"""
    text_lower = text.lower()
    
    # Common 8825 keywords
    keywords = []
    keyword_patterns = [
        "joju", "8825", "tgif", "meeting", "trustybits", "forge",
        "profile", "ux", "design", "strategy", "problem", "statement",
        "project", "brief", "hcss", "ral", "costa", "nike", "marchon",
        "innovation", "lab", "eyewear", "watch", "timepiece",
        "when76", "when", "availability", "schedule", "group", "calendar", "time", "block"
    ]
    
    for keyword in keyword_patterns:
        if keyword in text_lower:
            keywords.append(keyword)
    
    return keywords

def extract_entities(text):
    """Extract named entities from text"""
    entities = []
    
    # Simple entity patterns
    entity_patterns = {
        "person": ["Justin", "Gamal", "Prather"],
        "company": ["Trustybits", "HCSS", "Marchon", "COSTA", "Nike", "Fossil"],
        "project": ["Joju", "Forge", "8825", "TGIF"]
    }
    
    for entity_type, names in entity_patterns.items():
        for name in names:
            if name in text:
                entities.append({"type": entity_type, "name": name})
    
    return entities
