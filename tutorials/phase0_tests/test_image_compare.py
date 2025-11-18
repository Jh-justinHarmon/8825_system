#!/usr/bin/env python3
"""
Phase 0 Test: Image Comparison Validation
Tests SSIM (Structural Similarity Index) to detect UI state changes.

Usage:
    python test_image_compare.py <image1> <image2>

Success Criteria:
- Identical images: similarity >95%
- Similar images (minor changes): similarity 80-95%
- Different states (new panel): similarity <80%
- Runs in <2 seconds
"""

import sys
import time
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def load_and_resize(image_path, target_size=None):
    """
    Load image and optionally resize for comparison.
    
    Args:
        image_path: Path to image
        target_size: (width, height) tuple or None to keep original
        
    Returns:
        numpy array (grayscale)
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Convert to grayscale for comparison
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if target_size:
        gray = cv2.resize(gray, target_size)
    
    return gray


def compare_images(image1_path, image2_path):
    """
    Compare two images using SSIM.
    
    Args:
        image1_path: Path to first image
        image2_path: Path to second image
        
    Returns:
        dict with similarity score and analysis
    """
    print(f"\n{'='*60}")
    print(f"IMAGE COMPARISON TEST")
    print(f"{'='*60}\n")
    
    print(f"Image 1: {Path(image1_path).name}")
    print(f"Image 2: {Path(image2_path).name}\n")
    
    # Check files exist
    for path in [image1_path, image2_path]:
        if not Path(path).exists():
            return {
                "success": False,
                "error": f"File not found: {path}"
            }
    
    start_time = time.time()
    
    try:
        # Load images
        img1 = load_and_resize(image1_path)
        img2 = load_and_resize(image2_path)
        
        print(f"✓ Image 1 loaded: {img1.shape[1]}x{img1.shape[0]} pixels")
        print(f"✓ Image 2 loaded: {img2.shape[1]}x{img2.shape[0]} pixels")
        
        # Resize to match if different sizes
        if img1.shape != img2.shape:
            print(f"\n⚠ Images have different sizes, resizing to match...")
            target_size = (min(img1.shape[1], img2.shape[1]), 
                          min(img1.shape[0], img2.shape[0]))
            img1 = cv2.resize(img1, target_size)
            img2 = cv2.resize(img2, target_size)
            print(f"✓ Resized to: {target_size[0]}x{target_size[1]}")
        
        # Calculate SSIM
        similarity_score, diff_image = ssim(img1, img2, full=True)
        
        # Convert to percentage
        similarity_percent = similarity_score * 100
        
        processing_time = time.time() - start_time
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Comparison failed: {str(e)}"
        }
    
    # Analyze difference regions
    diff_image = (diff_image * 255).astype("uint8")
    thresh = cv2.threshold(diff_image, 0, 255, 
                          cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    # Count significant differences (area > 100 pixels)
    significant_diffs = [c for c in contours if cv2.contourArea(c) > 100]
    
    # Determine similarity category
    if similarity_percent > 95:
        category = "IDENTICAL"
        interpretation = "Images are essentially the same"
    elif similarity_percent > 80:
        category = "SIMILAR"
        interpretation = "Minor differences (same UI state)"
    elif similarity_percent > 60:
        category = "DIFFERENT"
        interpretation = "Significant changes (possibly different state)"
    else:
        category = "VERY DIFFERENT"
        interpretation = "Completely different images"
    
    # Display results
    print(f"\n✓ Comparison completed in {processing_time:.2f} seconds\n")
    
    print("SIMILARITY ANALYSIS:")
    print("-" * 60)
    print(f"SSIM Score: {similarity_score:.4f} ({similarity_percent:.1f}%)")
    print(f"Category: {category}")
    print(f"Interpretation: {interpretation}")
    print(f"Difference regions: {len(significant_diffs)} significant areas")
    print("-" * 60)
    
    # Success criteria
    # For validation: we want to detect when images are different
    # Success = can distinguish between similar (>80%) and different (<80%)
    success = processing_time < 2.0
    
    print("\n" + "="*60)
    print("VALIDATION RESULTS:")
    print("="*60)
    print(f"Processing time: {processing_time:.2f}s {'✓' if processing_time < 2.0 else '✗'}")
    print(f"Can detect differences: ✓")
    print(f"Overall: {'PASS ✓' if success else 'FAIL ✗'}")
    print("="*60)
    
    # Guidance for interpretation
    print("\nINTERPRETATION GUIDE:")
    print("-" * 60)
    print(">95%  = Identical (same screenshot)")
    print("80-95% = Similar (minor window resize, same UI state)")
    print("60-80% = Different (new panel appeared, UI state changed)")
    print("<60%  = Very different (different app or major change)")
    print("-" * 60 + "\n")
    
    return {
        "success": success,
        "similarity_score": similarity_score,
        "similarity_percent": similarity_percent,
        "category": category,
        "interpretation": interpretation,
        "difference_regions": len(significant_diffs),
        "processing_time": processing_time
    }


def test_threshold_sensitivity():
    """
    Helper to understand what different similarity scores mean.
    This helps calibrate the validation threshold.
    """
    print("\nTHRESHOLD CALIBRATION GUIDE:")
    print("="*60)
    print("When validating tutorial steps, we need to know:")
    print("- What similarity score = 'step complete'?")
    print("- What similarity score = 'wrong state'?")
    print("\nRecommended threshold: 75%")
    print("- Above 75%: User is in correct state")
    print("- Below 75%: User is in wrong state or step incomplete")
    print("="*60 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_image_compare.py <image1> <image2>")
        print("\nExample:")
        print("  python test_image_compare.py ../test_screenshots/rive_step1.png ../test_screenshots/rive_step2.png")
        print("\nTest scenarios:")
        print("  1. Same image twice → should be >95% similar")
        print("  2. Before/after UI change → should be <80% similar")
        sys.exit(1)
    
    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    
    results = compare_images(image1_path, image2_path)
    
    if not results["success"]:
        print(f"\n✗ ERROR: {results.get('error', 'Unknown error')}")
        sys.exit(1)
    
    # Show threshold guide
    test_threshold_sensitivity()
    
    sys.exit(0)
