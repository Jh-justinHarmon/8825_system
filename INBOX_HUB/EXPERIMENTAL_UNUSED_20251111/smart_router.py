#!/usr/bin/env python3
"""
Input Hub Phase 2: Smart Router
Routes screenshots to correct project folders based on OCR metadata
Learns from user corrections to improve routing accuracy
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
INTAKE_SCREENSHOTS = SCRIPT_DIR / "users" / "jh" / "intake" / "screenshots"
METADATA_DIR = SCRIPT_DIR / "users" / "jh" / "metadata"
PROCESSED_DIR = SCRIPT_DIR / "users" / "jh" / "processed"
LEARNING_LOG = SCRIPT_DIR / "users" / "jh" / "routing_learning.json"

# Project destinations
PROJECT_DIRS = {
    "joju": SCRIPT_DIR.parent / "focuses" / "joju" / "screenshots",
    "hcss": SCRIPT_DIR.parent / "focuses" / "hcss" / "screenshots",
    "jh_assistant": SCRIPT_DIR.parent / "focuses" / "jh_assistant" / "screenshots",
    "8825": SCRIPT_DIR.parent / "8825_core" / "screenshots",
}

# Ensure directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
for project_dir in PROJECT_DIRS.values():
    project_dir.mkdir(parents=True, exist_ok=True)


def load_learning_data() -> dict:
    """Load routing learning data"""
    if LEARNING_LOG.exists():
        with open(LEARNING_LOG, 'r') as f:
            return json.load(f)
    return {
        "corrections": [],
        "keyword_weights": {},
        "accuracy_stats": {
            "total_routed": 0,
            "corrections": 0,
            "accuracy": 1.0
        }
    }


def save_learning_data(data: dict):
    """Save routing learning data"""
    with open(LEARNING_LOG, 'w') as f:
        json.dump(data, f, indent=2)


def get_metadata(screenshot_path: Path) -> dict:
    """Get metadata for screenshot"""
    metadata_file = METADATA_DIR / f"{screenshot_path.stem}.json"
    
    if not metadata_file.exists():
        return None
    
    with open(metadata_file, 'r') as f:
        return json.load(f)


def route_screenshot(screenshot_path: Path, metadata: dict, dry_run: bool = False) -> dict:
    """Route screenshot to appropriate project folder"""
    project = metadata.get("project", "unknown")
    confidence = metadata.get("confidence", 0.0)
    
    # If unknown or low confidence, keep in intake
    if project == "unknown" or confidence < 0.3:
        return {
            "action": "keep_in_intake",
            "reason": f"Low confidence ({confidence})",
            "destination": None
        }
    
    # Get destination
    dest_dir = PROJECT_DIRS.get(project)
    if not dest_dir:
        return {
            "action": "keep_in_intake",
            "reason": f"Unknown project: {project}",
            "destination": None
        }
    
    dest_path = dest_dir / screenshot_path.name
    
    # Skip if already exists
    if dest_path.exists():
        return {
            "action": "skip",
            "reason": "Already exists in destination",
            "destination": str(dest_path)
        }
    
    # Route the file
    if not dry_run:
        try:
            shutil.copy2(screenshot_path, dest_path)
            
            # Move to processed
            processed_path = PROCESSED_DIR / screenshot_path.name
            shutil.move(screenshot_path, processed_path)
            
            # Update learning data
            learning_data = load_learning_data()
            learning_data["accuracy_stats"]["total_routed"] += 1
            save_learning_data(learning_data)
            
        except Exception as e:
            return {
                "action": "error",
                "reason": str(e),
                "destination": None
            }
    
    return {
        "action": "routed",
        "project": project,
        "confidence": confidence,
        "destination": str(dest_path)
    }


def learn_from_correction(screenshot_name: str, predicted_project: str, actual_project: str):
    """Learn from user correction"""
    learning_data = load_learning_data()
    
    # Log the correction
    correction = {
        "screenshot": screenshot_name,
        "predicted": predicted_project,
        "actual": actual_project,
        "timestamp": datetime.now().isoformat()
    }
    learning_data["corrections"].append(correction)
    
    # Update accuracy stats
    stats = learning_data["accuracy_stats"]
    stats["corrections"] += 1
    stats["accuracy"] = 1 - (stats["corrections"] / stats["total_routed"])
    
    # Update keyword weights (simple learning)
    # In future: analyze OCR text from corrected screenshots to adjust weights
    
    save_learning_data(learning_data)
    
    print(f"✓ Learned from correction: {predicted_project} → {actual_project}")
    print(f"  Current accuracy: {stats['accuracy']:.1%}")


def route_all_screenshots(dry_run: bool = False, verbose: bool = True):
    """Route all screenshots in intake folder"""
    screenshots = list(INTAKE_SCREENSHOTS.glob("*.png"))
    
    if not screenshots:
        print("No screenshots to route")
        return
    
    if dry_run:
        print("DRY RUN - No files will be moved")
        print()
    
    print(f"Routing {len(screenshots)} screenshots...")
    print()
    
    results = {
        "routed": 0,
        "kept": 0,
        "skipped": 0,
        "errors": 0
    }
    
    for screenshot in screenshots:
        # Get metadata
        metadata = get_metadata(screenshot)
        if not metadata:
            if verbose:
                print(f"⚠️  {screenshot.name} - No metadata (run OCR first)")
            results["kept"] += 1
            continue
        
        # Route
        result = route_screenshot(screenshot, metadata, dry_run)
        
        if verbose:
            action = result["action"]
            if action == "routed":
                print(f"✓ {screenshot.name} → {result['project']} (confidence: {result['confidence']})")
                results["routed"] += 1
            elif action == "keep_in_intake":
                print(f"⏸️  {screenshot.name} - {result['reason']}")
                results["kept"] += 1
            elif action == "skip":
                print(f"⏭️  {screenshot.name} - {result['reason']}")
                results["skipped"] += 1
            else:
                print(f"❌ {screenshot.name} - {result['reason']}")
                results["errors"] += 1
    
    print()
    print("Summary:")
    print(f"  Routed:  {results['routed']}")
    print(f"  Kept:    {results['kept']}")
    print(f"  Skipped: {results['skipped']}")
    print(f"  Errors:  {results['errors']}")
    
    # Show accuracy
    learning_data = load_learning_data()
    accuracy = learning_data["accuracy_stats"]["accuracy"]
    print()
    print(f"Routing accuracy: {accuracy:.1%}")


def main():
    """CLI for smart router"""
    import sys
    
    dry_run = "--dry-run" in sys.argv
    
    route_all_screenshots(dry_run=dry_run)


if __name__ == "__main__":
    main()
