#!/usr/bin/env python3
"""
Simple Sticky OCR
Just OCR the whole image - simpler approach for now
"""

import sys
from pathlib import Path
from PIL import Image
import pytesseract

def ocr_image(image_path):
    """Simple OCR of entire image"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def main():
    downloads = Path.home() / 'Downloads'
    images = list(downloads.glob('*sticky*.jpeg')) + list(downloads.glob('*sticky*.jpg')) + list(downloads.glob('*sticky*.png'))
    
    if not images:
        print("No sticky images found")
        return
    
    for img_path in images:
        print(f"\n{'='*50}")
        print(f"Image: {img_path.name}")
        print(f"{'='*50}")
        
        text = ocr_image(img_path)
        print(text)
        
        # Save to file
        output = downloads / f"{img_path.stem}_ocr.txt"
        with open(output, 'w') as f:
            f.write(text)
        print(f"\nSaved to: {output}")

if __name__ == '__main__':
    main()
