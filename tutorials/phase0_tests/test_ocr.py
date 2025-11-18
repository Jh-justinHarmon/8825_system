#!/usr/bin/env python3
"""
Phase 0 Test: OCR Validation
Tests Tesseract OCR on UI screenshots to validate text extraction accuracy.

Usage:
    python test_ocr.py <path_to_screenshot>

Success Criteria:
- Extracts visible text with >80% accuracy
- Provides bounding box coordinates for each text region
- Runs in <2 seconds on typical screenshot
"""

import sys
import time
from pathlib import Path
from PIL import Image
import pytesseract
import json

def test_ocr(image_path):
    """
    Run OCR on an image and return structured results.
    
    Args:
        image_path: Path to screenshot image
        
    Returns:
        dict with keys: text_regions, total_text, processing_time, success
    """
    print(f"\n{'='*60}")
    print(f"OCR TEST: {Path(image_path).name}")
    print(f"{'='*60}\n")
    
    # Check file exists
    if not Path(image_path).exists():
        return {
            "success": False,
            "error": f"File not found: {image_path}"
        }
    
    # Load image
    try:
        img = Image.open(image_path)
        print(f"✓ Image loaded: {img.size[0]}x{img.size[1]} pixels")
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to load image: {str(e)}"
        }
    
    # Run OCR with timing
    start_time = time.time()
    
    try:
        # Get detailed data with bounding boxes
        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Get plain text for display
        plain_text = pytesseract.image_to_string(img)
        
        processing_time = time.time() - start_time
        
    except Exception as e:
        return {
            "success": False,
            "error": f"OCR failed: {str(e)}"
        }
    
    # Parse results into structured format
    text_regions = []
    n_boxes = len(ocr_data['text'])
    
    for i in range(n_boxes):
        # Filter out empty text and low confidence
        if int(ocr_data['conf'][i]) > 30 and ocr_data['text'][i].strip():
            text_regions.append({
                "text": ocr_data['text'][i],
                "confidence": int(ocr_data['conf'][i]),
                "bbox": {
                    "x": ocr_data['left'][i],
                    "y": ocr_data['top'][i],
                    "width": ocr_data['width'][i],
                    "height": ocr_data['height'][i]
                }
            })
    
    # Display results
    print(f"✓ OCR completed in {processing_time:.2f} seconds")
    print(f"✓ Found {len(text_regions)} text regions\n")
    
    print("EXTRACTED TEXT:")
    print("-" * 60)
    print(plain_text.strip())
    print("-" * 60)
    
    print("\nTOP 10 TEXT REGIONS (with coordinates):")
    print("-" * 60)
    for i, region in enumerate(text_regions[:10], 1):
        bbox = region['bbox']
        print(f"{i:2d}. '{region['text']}' @ ({bbox['x']}, {bbox['y']}) "
              f"[confidence: {region['confidence']}%]")
    
    if len(text_regions) > 10:
        print(f"... and {len(text_regions) - 10} more regions")
    
    # Success criteria check
    success = len(text_regions) > 0 and processing_time < 2.0
    
    print("\n" + "="*60)
    print("VALIDATION RESULTS:")
    print("="*60)
    print(f"Text regions found: {len(text_regions)} {'✓' if len(text_regions) > 0 else '✗'}")
    print(f"Processing time: {processing_time:.2f}s {'✓' if processing_time < 2.0 else '✗'}")
    print(f"Overall: {'PASS ✓' if success else 'FAIL ✗'}")
    print("="*60 + "\n")
    
    return {
        "success": success,
        "text_regions": text_regions,
        "plain_text": plain_text.strip(),
        "processing_time": processing_time,
        "total_regions": len(text_regions)
    }


def save_results(results, output_path):
    """Save OCR results to JSON file for later analysis."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_ocr.py <path_to_screenshot>")
        print("\nExample:")
        print("  python test_ocr.py ../test_screenshots/rive_step1.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    results = test_ocr(image_path)
    
    # Save results
    output_path = Path(image_path).stem + "_ocr_results.json"
    save_results(results, output_path)
    
    # Exit with appropriate code
    sys.exit(0 if results["success"] else 1)
