#!/usr/bin/env python3
"""
Google Vision Sticky Note Processor
Uses Google Cloud Vision API for superior handwriting OCR
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple
import io

try:
    from google.cloud import vision
    from PIL import Image, ImageDraw
    import cv2
    import numpy as np
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("Install: pip3 install google-cloud-vision pillow opencv-python")

class VisionStickyProcessor:
    """Process sticky notes using Google Vision API"""
    
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
        
        # Initialize Vision API client
        # Uses Service Account credentials
        creds_path = Path(__file__).parent.parent / 'google' / 'vision_credentials.json'
        if not creds_path.exists():
            raise FileNotFoundError(
                f"Vision credentials not found at {creds_path}\n"
                "Download Service Account JSON from Google Cloud Console"
            )
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(creds_path)
        self.client = vision.ImageAnnotatorClient()
    
    def detect_text_regions(self, image_path: Path) -> List[Dict]:
        """
        Detect text regions using Google Vision API
        Returns list of text blocks with bounding boxes
        """
        # Load image
        with io.open(str(image_path), 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # Detect text with document text detection (best for handwriting)
        response = self.client.document_text_detection(image=image)
        
        if response.error.message:
            raise Exception(f'Vision API error: {response.error.message}')
        
        # Extract text blocks
        blocks = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                # Get bounding box
                vertices = block.bounding_box.vertices
                x_coords = [v.x for v in vertices]
                y_coords = [v.y for v in vertices]
                
                bbox = (
                    min(x_coords),
                    min(y_coords),
                    max(x_coords) - min(x_coords),
                    max(y_coords) - min(y_coords)
                )
                
                # Extract text from paragraphs
                text_parts = []
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        text_parts.append(word_text)
                
                text = ' '.join(text_parts)
                
                # Get confidence
                confidence = block.confidence if hasattr(block, 'confidence') else 0.9
                
                blocks.append({
                    'bbox': bbox,
                    'text': text,
                    'confidence': confidence
                })
        
        return blocks
    
    def detect_sticky_color(self, image_path: Path, bbox: Tuple) -> str:
        """Detect dominant color in bounding box region"""
        img = cv2.imread(str(image_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        x, y, w, h = bbox
        region = img_rgb[y:y+h, x:x+w]
        
        # Calculate average color
        avg_color = region.mean(axis=(0, 1))
        
        # Find closest sticky color
        min_dist = float('inf')
        closest_color = 'yellow'
        
        for color_name, color_rgb in self.STICKY_COLORS.items():
            dist = np.linalg.norm(np.array(color_rgb) - avg_color)
            if dist < min_dist:
                min_dist = dist
                closest_color = color_name
        
        return closest_color
    
    def cluster_blocks(self, blocks: List[Dict], max_distance: int = 300) -> List[List[Dict]]:
        """Group text blocks that are close together (same sticky)"""
        if not blocks:
            return []
        
        clusters = []
        used = set()
        
        for i, block in enumerate(blocks):
            if i in used:
                continue
            
            cluster = [block]
            used.add(i)
            
            # Get center of this block
            x1, y1, w1, h1 = block['bbox']
            center1 = (x1 + w1//2, y1 + h1//2)
            
            # Find nearby blocks
            for j, other in enumerate(blocks):
                if j in used:
                    continue
                
                x2, y2, w2, h2 = other['bbox']
                center2 = (x2 + w2//2, y2 + h2//2)
                
                dist = np.linalg.norm(np.array(center1) - np.array(center2))
                
                if dist < max_distance:
                    cluster.append(other)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def process_image(self, image_path: Path) -> Dict:
        """Process image and return structured sticky note data"""
        print(f"\nProcessing: {image_path.name}")
        
        # Detect text regions
        print("  → Running Google Vision OCR...")
        blocks = self.detect_text_regions(image_path)
        print(f"  ✓ Found {len(blocks)} text regions")
        
        if not blocks:
            return {
                'source_image': str(image_path),
                'total_stickies': 0,
                'clusters': []
            }
        
        # Cluster into stickies
        clusters = self.cluster_blocks(blocks)
        print(f"  ✓ Organized into {len(clusters)} sticky notes")
        
        # Build result
        result = {
            'source_image': str(image_path),
            'total_stickies': len(clusters),
            'clusters': []
        }
        
        for i, cluster in enumerate(clusters):
            # Combine text from all blocks in cluster
            texts = [b['text'] for b in cluster]
            combined_text = '\n'.join(texts)
            
            # Use first block's bbox as representative
            bbox = cluster[0]['bbox']
            
            # Detect color
            color = self.detect_sticky_color(image_path, bbox)
            
            # Average confidence
            avg_confidence = sum(b['confidence'] for b in cluster) / len(cluster)
            
            sticky_data = {
                'id': f'sticky_{i}',
                'bbox': list(bbox),
                'text': combined_text,
                'color': color,
                'confidence': avg_confidence,
                'position': [bbox[0] + bbox[2]//2, bbox[1] + bbox[3]//2]
            }
            
            result['clusters'].append({
                'id': f'cluster_{i}',
                'stickies': [sticky_data]
            })
            
            print(f"  → Sticky {i+1}: \"{combined_text[:30]}...\" ({color})")
        
        return result
    
    def save_debug_image(self, image_path: Path, result: Dict, output_path: Path):
        """Save image with detected stickies highlighted"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        for cluster in result['clusters']:
            for sticky in cluster['stickies']:
                x, y, w, h = sticky['bbox']
                # Draw rectangle
                draw.rectangle([x, y, x+w, y+h], outline='red', width=5)
                # Draw text label
                label = f"{sticky['color']}: {sticky['text'][:20]}..."
                draw.text((x, y-30), label, fill='red')
        
        img.save(output_path)
        print(f"  ✓ Debug image saved: {output_path}")

def main():
    """Process sticky notes from Downloads"""
    processor = VisionStickyProcessor()
    
    # Find images
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
    
    print(f"Found {len(images)} images to process")
    
    results = []
    for image_path in images:
        try:
            result = processor.process_image(image_path)
            results.append(result)
            
            # Save debug image
            debug_path = image_path.parent / f"{image_path.stem}_vision_debug.png"
            processor.save_debug_image(image_path, result, debug_path)
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    # Save results
    if results:
        output_file = downloads / 'sticky_notes_vision.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}")
        print(f"✓ Processed {sum(r['total_stickies'] for r in results)} sticky notes")

if __name__ == '__main__':
    main()
