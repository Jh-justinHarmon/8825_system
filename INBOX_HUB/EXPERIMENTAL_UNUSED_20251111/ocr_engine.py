#!/usr/bin/env python3
"""
Input Hub Phase 2: OCR Engine
Extracts text and metadata from screenshots for smart routing
"""

import json
from pathlib import Path
from datetime import datetime
from PIL import Image
import pytesseract

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
INTAKE_SCREENSHOTS = SCRIPT_DIR / "users" / "jh" / "intake" / "screenshots"
METADATA_DIR = SCRIPT_DIR / "users" / "jh" / "metadata"

# Ensure metadata directory exists
METADATA_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_image(image_path: Path) -> str:
    """Extract text from image using OCR"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR failed for {image_path.name}: {e}")
        return ""


def detect_project_context(text: str) -> dict:
    """Detect project context from OCR text"""
    text_lower = text.lower()
    
    # Project keywords
    projects = {
        "joju": ["joju", "library", "achievement", "profile", "mining"],
        "hcss": ["hcss", "crunchtime", "tgif", "ral", "otter"],
        "jh_assistant": ["personal", "calendar", "email", "task"],
        "8825": ["8825", "protocol", "agent", "workflow", "focus"],
    }
    
    # Score each project
    scores = {}
    for project, keywords in projects.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            scores[project] = score
    
    # Get top project
    if scores:
        top_project = max(scores, key=scores.get)
        confidence = scores[top_project] / len(projects[top_project])
        return {
            "project": top_project,
            "confidence": round(confidence, 2),
            "scores": scores
        }
    
    return {
        "project": "unknown",
        "confidence": 0.0,
        "scores": {}
    }


def extract_metadata(image_path: Path) -> dict:
    """Extract full metadata from screenshot"""
    # Get file stats
    stats = image_path.stat()
    
    # Extract text via OCR
    text = extract_text_from_image(image_path)
    
    # Detect project context
    context = detect_project_context(text)
    
    # Build metadata
    metadata = {
        "filename": image_path.name,
        "path": str(image_path),
        "size_bytes": stats.st_size,
        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "ocr_text": text[:500],  # First 500 chars
        "ocr_length": len(text),
        "project": context["project"],
        "confidence": context["confidence"],
        "project_scores": context["scores"],
        "processed_at": datetime.now().isoformat()
    }
    
    return metadata


def save_metadata(image_path: Path, metadata: dict):
    """Save metadata to JSON file"""
    metadata_file = METADATA_DIR / f"{image_path.stem}.json"
    
    try:
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save metadata for {image_path.name}: {e}")


def process_screenshot(image_path: Path, verbose: bool = True) -> dict:
    """Process a screenshot: OCR + metadata extraction"""
    if verbose:
        print(f"Processing: {image_path.name}")
    
    # Extract metadata
    metadata = extract_metadata(image_path)
    
    # Save metadata
    save_metadata(image_path, metadata)
    
    if verbose:
        print(f"  OCR text: {len(metadata['ocr_text'])} chars")
        print(f"  Project: {metadata['project']} (confidence: {metadata['confidence']})")
        if metadata['project_scores']:
            print(f"  Scores: {metadata['project_scores']}")
    
    return metadata


def process_all_screenshots(verbose: bool = True):
    """Process all screenshots in intake folder"""
    screenshots = list(INTAKE_SCREENSHOTS.glob("*.png"))
    
    if not screenshots:
        print("No screenshots to process")
        return
    
    print(f"Processing {len(screenshots)} screenshots...")
    print()
    
    results = []
    for screenshot in screenshots:
        # Skip if metadata already exists
        metadata_file = METADATA_DIR / f"{screenshot.stem}.json"
        if metadata_file.exists():
            if verbose:
                print(f"Skipping {screenshot.name} (already processed)")
            continue
        
        metadata = process_screenshot(screenshot, verbose)
        results.append(metadata)
        
        if verbose:
            print()
    
    print(f"✓ Processed {len(results)} new screenshots")
    return results


def main():
    """CLI for OCR engine"""
    import sys
    
    if len(sys.argv) > 1:
        # Process specific file
        image_path = Path(sys.argv[1])
        if not image_path.exists():
            print(f"Error: File not found: {image_path}")
            sys.exit(1)
        
        metadata = process_screenshot(image_path)
        print()
        print("Metadata:")
        print(json.dumps(metadata, indent=2))
    else:
        # Process all screenshots
        process_all_screenshots()


if __name__ == "__main__":
    main()
