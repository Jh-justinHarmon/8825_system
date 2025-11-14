#!/usr/bin/env python3
"""
Download Folder Wedge - Test Mode
Scans Downloads folder and shows what would be routed (without moving files)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from metadata_extractor import extract_metadata
from content_analyzer import analyze_content
from project_matcher import match_to_project

# Paths
PROJECT_DIR = Path(__file__).parent
CONFIG_FILE = PROJECT_DIR / "project_contexts.json"

def load_config():
    """Load project contexts configuration"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def test_downloads_folder(downloads_path, limit=20):
    """Test wedge on existing downloads folder"""
    
    print("🧪 DOWNLOAD FOLDER WEDGE - TEST MODE")
    print("="*60)
    print(f"📁 Scanning: {downloads_path}")
    print(f"🔍 Limit: {limit} files\n")
    
    # Load configuration
    config = load_config()
    
    # Get files from Downloads
    downloads = Path(downloads_path)
    if not downloads.exists():
        print(f"❌ Path not found: {downloads_path}")
        return
    
    files = [f for f in downloads.iterdir() if f.is_file()]
    
    if not files:
        print("❌ No files found in Downloads folder")
        return
    
    print(f"📊 Found {len(files)} files\n")
    
    # Test each file
    results = {
        "auto_route": [],
        "suggest": [],
        "ask_user": [],
        "errors": []
    }
    
    for i, file_path in enumerate(files[:limit]):
        try:
            print(f"[{i+1}/{min(limit, len(files))}] {file_path.name}")
            
            # Extract metadata
            metadata = extract_metadata(file_path)
            
            # Analyze content
            content_data = analyze_content(file_path, metadata)
            
            # Match to project
            match_result = match_to_project(file_path, metadata, content_data, config)
            
            # Categorize by confidence
            confidence = match_result.get("confidence", 0)
            project = match_result.get("project", "Unknown")
            destination = match_result.get("destination", "")
            
            result_data = {
                "file": file_path.name,
                "project": project,
                "confidence": confidence,
                "destination": destination,
                "size_mb": file_path.stat().st_size / (1024 * 1024)
            }
            
            if confidence >= 90:
                results["auto_route"].append(result_data)
                status = f"✅ AUTO-ROUTE → {project} ({confidence}%)"
            elif confidence >= 50:
                results["suggest"].append(result_data)
                status = f"💡 SUGGEST → {project} ({confidence}%)"
            else:
                results["ask_user"].append(result_data)
                status = f"❓ ASK USER ({confidence}%)"
            
            print(f"   {status}")
            print()
            
        except Exception as e:
            results["errors"].append({"file": file_path.name, "error": str(e)})
            print(f"   ⚠️  Error: {e}\n")
    
    # Summary Report
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60 + "\n")
    
    total_tested = len(results["auto_route"]) + len(results["suggest"]) + len(results["ask_user"])
    
    print(f"📈 OVERVIEW")
    print(f"   Files Tested: {total_tested}")
    print(f"   Errors: {len(results['errors'])}")
    
    # Auto-route
    print(f"\n✅ AUTO-ROUTE ({len(results['auto_route'])} files)")
    if results["auto_route"]:
        for item in results["auto_route"][:5]:
            print(f"   • {item['file'][:40]:40} → {item['project']} ({item['confidence']}%)")
        if len(results["auto_route"]) > 5:
            print(f"   ... and {len(results['auto_route']) - 5} more")
    else:
        print("   (none)")
    
    # Suggest
    print(f"\n💡 SUGGEST ({len(results['suggest'])} files)")
    if results["suggest"]:
        for item in results["suggest"][:5]:
            print(f"   • {item['file'][:40]:40} → {item['project']} ({item['confidence']}%)")
        if len(results["suggest"]) > 5:
            print(f"   ... and {len(results['suggest']) - 5} more")
    else:
        print("   (none)")
    
    # Ask user
    print(f"\n❓ ASK USER ({len(results['ask_user'])} files)")
    if results["ask_user"]:
        for item in results["ask_user"][:5]:
            print(f"   • {item['file'][:40]:40} (confidence: {item['confidence']}%)")
        if len(results["ask_user"]) > 5:
            print(f"   ... and {len(results['ask_user']) - 5} more")
    else:
        print("   (none)")
    
    # Errors
    if results["errors"]:
        print(f"\n⚠️  ERRORS ({len(results['errors'])} files)")
        for item in results["errors"][:3]:
            print(f"   • {item['file']}: {item['error']}")
    
    # Accuracy metrics
    if total_tested > 0:
        auto_rate = (len(results["auto_route"]) / total_tested) * 100
        suggest_rate = (len(results["suggest"]) / total_tested) * 100
        ask_rate = (len(results["ask_user"]) / total_tested) * 100
        
        print(f"\n📊 CONFIDENCE DISTRIBUTION")
        print(f"   Auto-route: {auto_rate:.1f}%")
        print(f"   Suggest:    {suggest_rate:.1f}%")
        print(f"   Ask user:   {ask_rate:.1f}%")
    
    print("\n" + "="*60)
    print("✅ Test complete! No files were moved.")
    print("="*60 + "\n")
    
    # Save results
    results_file = PROJECT_DIR / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved to: {results_file}")

def main():
    """Main entry point"""
    # Default Downloads path
    downloads_path = Path.home() / "Downloads"
    
    # Allow custom path
    if len(sys.argv) > 1:
        downloads_path = Path(sys.argv[1])
    
    # Allow custom limit
    limit = 20
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
    
    test_downloads_folder(downloads_path, limit)

if __name__ == "__main__":
    main()
