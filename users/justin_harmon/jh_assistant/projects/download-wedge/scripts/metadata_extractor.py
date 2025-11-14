#!/usr/bin/env python3
"""
Metadata Extractor
Extracts filename patterns, file type, size, and other metadata
"""

import os
import mimetypes
from pathlib import Path
from datetime import datetime

def extract_metadata(file_path):
    """
    Extract metadata from file
    
    Returns:
        dict: Metadata including filename, extension, size, type, etc.
    """
    file_path = Path(file_path)
    
    # Basic file info
    stat = file_path.stat()
    
    # MIME type
    mime_type, _ = mimetypes.guess_type(str(file_path))
    
    metadata = {
        "filename": file_path.name,
        "basename": file_path.stem,
        "extension": file_path.suffix.lower(),
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "mime_type": mime_type or "unknown",
        "path": str(file_path.absolute())
    }
    
    # Extract patterns from filename
    metadata["patterns"] = extract_filename_patterns(file_path.name)
    
    # Determine file category
    metadata["category"] = categorize_file(metadata)
    
    return metadata

def extract_filename_patterns(filename):
    """
    Extract meaningful patterns from filename
    
    Returns:
        list: Detected patterns (dates, keywords, etc.)
    """
    patterns = []
    
    filename_lower = filename.lower()
    
    # Common patterns
    pattern_keywords = [
        'tgif', 'meeting', 'summary', 'proposal', 'contract',
        'design', 'mockup', 'prototype', 'wireframe',
        'joju', 'forge', 'trustybit', '76',
        'protocol', 'workflow', 'agent',
        'ral', 'hcss', '8825'
    ]
    
    for keyword in pattern_keywords:
        if keyword in filename_lower:
            patterns.append(keyword)
    
    # Date patterns (YYYY-MM-DD, YYYYMMDD, etc.)
    import re
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # 2025-11-07
        r'\d{8}',               # 20251107
        r'\d{4}_\d{2}_\d{2}'    # 2025_11_07
    ]
    
    for pattern in date_patterns:
        if re.search(pattern, filename):
            patterns.append('has_date')
            break
    
    return patterns

def categorize_file(metadata):
    """
    Categorize file based on extension and MIME type
    
    Returns:
        str: File category
    """
    ext = metadata['extension']
    mime = metadata['mime_type']
    
    # Document types
    if ext in ['.pdf', '.docx', '.doc', '.txt', '.md', '.rtf']:
        return 'document'
    
    # Spreadsheet
    if ext in ['.xlsx', '.xls', '.csv', '.numbers']:
        return 'spreadsheet'
    
    # Presentation
    if ext in ['.pptx', '.ppt', '.key']:
        return 'presentation'
    
    # Image
    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'] or (mime and 'image' in mime):
        return 'image'
    
    # Design
    if ext in ['.psd', '.ai', '.fig', '.sketch', '.xd']:
        return 'design'
    
    # Code
    if ext in ['.py', '.js', '.html', '.css', '.json', '.sh']:
        return 'code'
    
    # Archive
    if ext in ['.zip', '.tar', '.gz', '.rar', '.7z']:
        return 'archive'
    
    return 'other'

if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        metadata = extract_metadata(sys.argv[1])
        import json
        print(json.dumps(metadata, indent=2))
