#!/usr/bin/env python3
"""
Email Campaign → FigJam Pipeline
Complete automation: .eml → screenshot → FigJam upload
"""

import sys
from pathlib import Path
from eml_to_screenshot import eml_to_screenshot


def process_email_to_figjam(eml_path: Path, figjam_file_key: str = None, 
                             x: int = 0, y: int = 0, width: int = 800) -> dict:
    """
    Complete pipeline: .eml → screenshot → FigJam
    
    Args:
        eml_path: Path to .eml file
        figjam_file_key: FigJam file key (optional for now)
        x, y: Position on FigJam canvas
        width: Screenshot width
    
    Returns:
        Result dict with paths and status
    """
    
    print("="*60)
    print("EMAIL CAMPAIGN → FIGJAM PIPELINE")
    print("="*60)
    
    # Step 1: Convert .eml to screenshot
    print("\n📧 Step 1: Converting email to screenshot...")
    screenshot_path = eml_to_screenshot(eml_path, width=width)
    
    # Step 2: Manual FigJam upload (for now)
    print("\n📋 Step 2: FigJam upload...")
    print("   ⚠️  Figma REST API has limited image upload support")
    print("   📌 Manual step required:")
    print(f"      1. Open FigJam: https://www.figma.com/file/{figjam_file_key if figjam_file_key else 'YOUR_FILE_KEY'}/")
    print(f"      2. Drag and drop: {screenshot_path}")
    print(f"      3. Position at: ({x}, {y})")
    
    result = {
        'status': 'success',
        'eml_file': str(eml_path),
        'screenshot': str(screenshot_path),
        'figjam_file_key': figjam_file_key,
        'position': {'x': x, 'y': y},
        'next_steps': 'Manual drag-and-drop to FigJam'
    }
    
    print("\n✅ Pipeline complete!")
    print(f"   Screenshot ready: {screenshot_path}")
    
    return result


def batch_process_emails(eml_dir: Path, figjam_file_key: str = None, 
                         start_x: int = 0, start_y: int = 0, 
                         spacing: int = 1000, width: int = 800):
    """
    Process multiple .eml files in a directory
    
    Args:
        eml_dir: Directory containing .eml files
        figjam_file_key: FigJam file key
        start_x, start_y: Starting position
        spacing: Vertical spacing between screenshots
        width: Screenshot width
    """
    
    eml_files = list(eml_dir.glob("*.eml"))
    
    if not eml_files:
        print(f"❌ No .eml files found in {eml_dir}")
        return
    
    print(f"📧 Found {len(eml_files)} email files")
    print("="*60)
    
    results = []
    y_offset = start_y
    
    for i, eml_path in enumerate(eml_files, 1):
        print(f"\n[{i}/{len(eml_files)}] Processing: {eml_path.name}")
        
        try:
            result = process_email_to_figjam(
                eml_path, 
                figjam_file_key, 
                start_x, 
                y_offset, 
                width
            )
            results.append(result)
            y_offset += spacing
            
        except Exception as e:
            print(f"❌ Error processing {eml_path.name}: {e}")
            continue
    
    print("\n" + "="*60)
    print(f"✅ Processed {len(results)}/{len(eml_files)} emails")
    print("="*60)
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Email Campaign → FigJam Pipeline")
        print("\nUsage:")
        print("  Single file:")
        print("    python3 email_to_figjam.py <email.eml> [figjam_key] [x] [y] [width]")
        print("\n  Batch process:")
        print("    python3 email_to_figjam.py --batch <directory> [figjam_key] [spacing]")
        print("\nExamples:")
        print("  python3 email_to_figjam.py campaign.eml")
        print("  python3 email_to_figjam.py campaign.eml abc123def456 0 0 1000")
        print("  python3 email_to_figjam.py --batch ~/Downloads/ abc123def456 1200")
        sys.exit(1)
    
    # Batch mode
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("❌ Error: Directory required for batch mode")
            sys.exit(1)
        
        eml_dir = Path(sys.argv[2])
        figjam_key = sys.argv[3] if len(sys.argv) > 3 else None
        spacing = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
        
        batch_process_emails(eml_dir, figjam_key, spacing=spacing)
    
    # Single file mode
    else:
        eml_path = Path(sys.argv[1])
        figjam_key = sys.argv[2] if len(sys.argv) > 2 else None
        x = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        y = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        width = int(sys.argv[5]) if len(sys.argv) > 5 else 800
        
        try:
            result = process_email_to_figjam(eml_path, figjam_key, x, y, width)
            print(f"\n✅ Success!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
