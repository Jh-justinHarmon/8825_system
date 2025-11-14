#!/usr/bin/env python3
"""
Project Matcher
Matches files to projects based on metadata and content
"""

import os
import fnmatch
from pathlib import Path

def match_to_project(file_path, metadata, content_data, config):
    """
    Match file to best project based on scoring
    
    Args:
        file_path: Path to file
        metadata: Metadata dict
        content_data: Content analysis dict
        config: Project configuration
    
    Returns:
        dict: Match result with project, confidence, and reasoning
    """
    projects = config['projects']
    scores = {}
    reasoning = {}
    
    # Score each project
    for project_name, project_config in projects.items():
        score, reasons = score_project(metadata, content_data, project_config)
        scores[project_name] = score
        reasoning[project_name] = reasons
    
    # Find best match
    best_project = max(scores, key=scores.get)
    best_score = scores[best_project]
    
    # Determine action based on confidence
    settings = config['global_settings']
    
    if best_score >= settings['auto_route_threshold']:
        action = 'auto_route'
    elif best_score >= settings['suggest_threshold']:
        action = 'suggest'
    else:
        action = 'ask'
    
    return {
        "project": best_project,
        "confidence": best_score,
        "action": action,
        "all_scores": scores,
        "reasoning": reasoning[best_project],
        "destination": projects[best_project]['destination']
    }

def score_project(metadata, content_data, project_config):
    """
    Score how well a file matches a project
    
    Returns:
        tuple: (score, reasoning list)
    """
    score = 0
    reasoning = []
    
    filename = metadata['filename'].lower()
    extension = metadata['extension']
    patterns = metadata.get('patterns', [])
    
    # 1. Filename pattern matching (30 points max)
    for pattern in project_config.get('patterns', []):
        if fnmatch.fnmatch(filename, pattern.lower()):
            score += 30
            reasoning.append(f"Filename matches pattern: {pattern}")
            break
    
    # 2. Keyword matching in filename (20 points max)
    keywords = project_config.get('keywords', [])
    matched_keywords = []
    for keyword in keywords:
        if keyword.lower() in filename:
            score += 5
            matched_keywords.append(keyword)
    
    if matched_keywords:
        score = min(score, 50)  # Cap at 50 from filename
        reasoning.append(f"Keywords in filename: {', '.join(matched_keywords)}")
    
    # 3. File type matching (15 points)
    if extension in project_config.get('file_types', []):
        score += 15
        reasoning.append(f"File type matches: {extension}")
    
    # 4. Content keyword matching (25 points max)
    content_keywords = content_data.get('keywords', [])
    if content_keywords:
        matched_content = []
        for keyword in keywords:
            if keyword.lower() in [k.lower() for k in content_keywords]:
                score += 5
                matched_content.append(keyword)
        
        if matched_content:
            score = min(score + 25, 100)  # Cap total at 100
            reasoning.append(f"Keywords in content: {', '.join(matched_content)}")
    
    # 5. Entity matching (10 points max)
    entities = content_data.get('entities', [])
    if entities:
        matched_entities = []
        for entity in entities:
            if any(entity.lower() in k.lower() for k in keywords):
                score += 5
                matched_entities.append(entity)
        
        if matched_entities:
            reasoning.append(f"Entities found: {', '.join(matched_entities)}")
    
    # 6. Pattern matching from metadata (10 points)
    for pattern in patterns:
        if any(pattern.lower() in k.lower() for k in keywords):
            score += 5
            reasoning.append(f"Pattern detected: {pattern}")
    
    # Cap score at 100
    score = min(score, 100)
    
    if not reasoning:
        reasoning.append("No strong indicators found")
    
    return score, reasoning

if __name__ == "__main__":
    # Test
    import sys
    import json
    from metadata_extractor import extract_metadata
    from content_analyzer import analyze_content
    from pathlib import Path
    
    if len(sys.argv) > 1:
        # Load config
        config_file = Path(__file__).parent.parent / "project_contexts.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Analyze file
        metadata = extract_metadata(sys.argv[1])
        content = analyze_content(sys.argv[1], metadata)
        result = match_to_project(sys.argv[1], metadata, content, config)
        
        print(json.dumps(result, indent=2))
