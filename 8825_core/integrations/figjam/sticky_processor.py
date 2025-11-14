#!/usr/bin/env python3
"""
Sticky Note Processor
Detects and OCRs sticky notes from photos, preserving layout and colors
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import numpy as np

try:
    from PIL import Image, ImageDraw
    import pytesseract
    import cv2
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("Warning: Install dependencies: pip3 install pillow pytesseract opencv-python")

class StickyNote:
    """Represents a detected sticky note"""
    def __init__(self, bbox, text, color, confidence):
        self.bbox = bbox  # (x, y, width, height)
        self.text = text
        self.color = color  # RGB tuple or color name
        self.confidence = confidence
        self.position = (bbox[0] + bbox[2]//2, bbox[1] + bbox[3]//2)  # Center point
    
    def to_dict(self):
        return {
            'bbox': self.bbox,
            'text': self.text,
            'color': self.color,
            'confidence': self.confidence,
            'position': self.position
        }

class StickyProcessor:
    """Process photos of sticky notes"""
    
    # Common sticky note colors (RGB)
    STICKY_COLORS = {
        'yellow': (255, 255, 153),
        'pink': (255, 182, 193),
        'blue': (173, 216, 230),
        'green': (144, 238, 144),
        'orange': (255, 200, 124),
        'purple': (216, 191, 216),
        'white': (255, 255, 255)
    }
    
    def __init__(self):
        if not HAS_DEPS:
            raise ImportError("Required dependencies not installed")
    
    def detect_stickies(self, image_path: Path) -> List[StickyNote]:
        """
        Detect sticky notes in an image
        Returns list of StickyNote objects
        """
        # Load image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to RGB for PIL
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect rectangular regions (potential stickies)
        regions = self._detect_rectangular_regions(img)
        
        stickies = []
        for region in regions:
            x, y, w, h = region
            
            # Extract region
            sticky_img = img_rgb[y:y+h, x:x+w]
            
            # Detect color
            color = self._detect_sticky_color(sticky_img)
            
            # OCR the text
            pil_img = Image.fromarray(sticky_img)
            text = pytesseract.image_to_string(pil_img).strip()
            
            # Calculate confidence (simple heuristic)
            confidence = self._calculate_confidence(text, w, h)
            
            if text and confidence > 0.3:  # Only keep if we got text
                sticky = StickyNote(
                    bbox=(x, y, w, h),
                    text=text,
                    color=color,
                    confidence=confidence
                )
                stickies.append(sticky)
        
        return stickies
    
    def _detect_rectangular_regions(self, img) -> List[Tuple[int, int, int, int]]:
        """
        Detect rectangular regions that might be sticky notes
        Returns list of (x, y, width, height) tuples
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        regions = []
        img_area = img.shape[0] * img.shape[1]
        
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # Filter by size (sticky notes are typically 5-20% of image)
            if area < img_area * 0.01 or area > img_area * 0.3:
                continue
            
            # Filter by aspect ratio (stickies are roughly square)
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                continue
            
            regions.append((x, y, w, h))
        
        return regions
    
    def _detect_sticky_color(self, sticky_img) -> str:
        """
        Detect the dominant color of a sticky note
        Returns color name
        """
        # Calculate average color
        avg_color = sticky_img.mean(axis=(0, 1))
        
        # Find closest sticky color
        min_dist = float('inf')
        closest_color = 'yellow'
        
        for color_name, color_rgb in self.STICKY_COLORS.items():
            dist = np.linalg.norm(np.array(color_rgb) - avg_color)
            if dist < min_dist:
                min_dist = dist
                closest_color = color_name
        
        return closest_color
    
    def _calculate_confidence(self, text: str, width: int, height: int) -> float:
        """
        Calculate confidence score for detected sticky
        Based on text length, region size, etc.
        """
        if not text:
            return 0.0
        
        # More text = higher confidence
        text_score = min(len(text) / 50.0, 1.0)
        
        # Reasonable size = higher confidence
        area = width * height
        size_score = 1.0 if 10000 < area < 100000 else 0.5
        
        return (text_score + size_score) / 2.0
    
    def cluster_stickies(self, stickies: List[StickyNote]) -> List[List[StickyNote]]:
        """
        Group stickies that are close together
        Returns list of clusters
        """
        if not stickies:
            return []
        
        # Simple clustering based on distance
        clusters = []
        used = set()
        
        for i, sticky in enumerate(stickies):
            if i in used:
                continue
            
            cluster = [sticky]
            used.add(i)
            
            # Find nearby stickies
            for j, other in enumerate(stickies):
                if j in used:
                    continue
                
                # Calculate distance between centers
                dist = np.linalg.norm(
                    np.array(sticky.position) - np.array(other.position)
                )
                
                # If close enough, add to cluster
                if dist < 300:  # pixels
                    cluster.append(other)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def process_image(self, image_path: Path) -> Dict:
        """
        Process an image and return structured data
        """
        print(f"Processing: {image_path.name}")
        
        # Detect stickies
        stickies = self.detect_stickies(image_path)
        print(f"  Found {len(stickies)} sticky notes")
        
        # Cluster them
        clusters = self.cluster_stickies(stickies)
        print(f"  Organized into {len(clusters)} clusters")
        
        # Build result
        result = {
            'source_image': str(image_path),
            'total_stickies': len(stickies),
            'clusters': []
        }
        
        for i, cluster in enumerate(clusters):
            cluster_data = {
                'id': f'cluster_{i}',
                'stickies': [s.to_dict() for s in cluster]
            }
            result['clusters'].append(cluster_data)
        
        return result
    
    def save_debug_image(self, image_path: Path, stickies: List[StickyNote], output_path: Path):
        """
        Save image with detected stickies highlighted
        """
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        for sticky in stickies:
            x, y, w, h = sticky.bbox
            # Draw rectangle
            draw.rectangle([x, y, x+w, y+h], outline='red', width=3)
            # Draw text label
            draw.text((x, y-20), f"{sticky.color}: {sticky.text[:20]}...", fill='red')
        
        img.save(output_path)
        print(f"  Debug image saved: {output_path}")

def main():
    """Process sticky notes from Downloads"""
    processor = StickyProcessor()
    
    # Find images in Downloads
    downloads = Path.home() / 'Downloads'
    image_extensions = ['.jpg', '.jpeg', '.png']
    
    images = []
    for ext in image_extensions:
        images.extend(downloads.glob(f'*sticky*{ext}'))
        images.extend(downloads.glob(f'*whiteboard*{ext}'))
    
    if not images:
        print("No sticky note images found in Downloads")
        print("Tip: Name your files with 'sticky' or 'whiteboard'")
        return
    
    print(f"Found {len(images)} images to process\n")
    
    results = []
    for image_path in images:
        result = processor.process_image(image_path)
        results.append(result)
        
        # Save debug image
        debug_path = image_path.parent / f"{image_path.stem}_debug.png"
        stickies = []
        for cluster in result['clusters']:
            for sticky_data in cluster['stickies']:
                sticky = StickyNote(
                    bbox=tuple(sticky_data['bbox']),
                    text=sticky_data['text'],
                    color=sticky_data['color'],
                    confidence=sticky_data['confidence']
                )
                stickies.append(sticky)
        processor.save_debug_image(image_path, stickies, debug_path)
        
        print()
    
    # Save results
    output_file = downloads / 'sticky_notes_processed.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_file}")

if __name__ == '__main__':
    main()
