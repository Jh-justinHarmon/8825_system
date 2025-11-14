#!/usr/bin/env python3
"""
Extract images from Jh-ARCHV folder for Joju profile
Handles PDFs, videos, and existing images
"""

import os
import json
from pathlib import Path
from PIL import Image
import shutil

# Try to import PDF tools
try:
    import fitz  # PyMuPDF
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("⚠️  PyMuPDF not installed. Install with: pip install PyMuPDF")

# Try to import video tools
try:
    import cv2
    HAS_VIDEO = True
except ImportError:
    HAS_VIDEO = False
    print("⚠️  OpenCV not installed. Install with: pip install opencv-python")


class ArchiveImageExtractor:
    def __init__(self, archive_path: str, output_dir: str):
        self.archive_path = Path(archive_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Project mapping
        self.project_files = {
            'amare': ['Amare_presentation.pdf'],
            'shinola': [
                'shinola_collab_collection.pdf',
                'shinola_collab_collection_0_DECK_062821_rev02.pdf',
                'shinola_collab_collection_1_watch_monster_102121.pdf',
                'shinola_collab_collection_2_runwell-COMBO_102421.pdf'
            ],
            'nike_vision': ['2013_NKvsn-DD.pdf', 'nikeTrainingProposal.pdf'],
            'costa': [
                '2017_costa-Catalogue.pdf',
                'COSTA Spring 2018 HD.mp4',
                'COSTA Fall 2018 Rough 03.mp4',
                'LSD_Costa - Design Strategy 2016.pdf'
            ],
            'tiger_cut': ['SP12_TIGER-CUT_SKETCHBOOK.pdf'],
            'dragon': [
                'dragon_prelim-moodboards_092118_outline.pdf',
                'dragon_sketchbook_review_102318_marchonFEEDBACK.pdf'
            ],
            'profile': ['discord-profile-pic.jpg']
        }
    
    def extract_pdf_images(self, pdf_path: Path, project_name: str, max_images: int = 5) -> list:
        """Extract images from PDF"""
        if not HAS_PDF:
            print(f"⚠️  Skipping {pdf_path.name} (PyMuPDF not installed)")
            return []
        
        images = []
        try:
            doc = fitz.open(pdf_path)
            print(f"📄 Extracting from {pdf_path.name} ({len(doc)} pages)...")
            
            image_count = 0
            for page_num in range(min(len(doc), 10)):  # First 10 pages max
                page = doc[page_num]
                
                # Get images from page
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    if image_count >= max_images:
                        break
                    
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Save image
                    output_name = f"{project_name}-{page_num+1}-{img_index+1}.png"
                    output_path = self.output_dir / output_name
                    
                    with open(output_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    # Get dimensions
                    with Image.open(output_path) as pil_img:
                        width, height = pil_img.size
                    
                    images.append({
                        "type": "image",
                        "width": width,
                        "height": height,
                        "url": f"/content/media/{output_name}"
                    })
                    
                    image_count += 1
                    print(f"  ✅ Extracted: {output_name} ({width}x{height})")
            
            doc.close()
        except Exception as e:
            print(f"  ❌ Error extracting from {pdf_path.name}: {e}")
        
        return images
    
    def extract_video_frame(self, video_path: Path, project_name: str, timestamp: float = 5.0) -> list:
        """Extract a frame from video"""
        if not HAS_VIDEO:
            print(f"⚠️  Skipping {video_path.name} (OpenCV not installed)")
            return []
        
        try:
            print(f"🎥 Extracting frame from {video_path.name}...")
            
            cap = cv2.VideoCapture(str(video_path))
            
            # Set position to timestamp (in seconds)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(fps * timestamp)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            if ret:
                output_name = f"{project_name}-video-frame.png"
                output_path = self.output_dir / output_name
                
                cv2.imwrite(str(output_path), frame)
                
                # Get dimensions
                height, width = frame.shape[:2]
                
                cap.release()
                
                print(f"  ✅ Extracted: {output_name} ({width}x{height})")
                
                return [{
                    "type": "image",
                    "width": width,
                    "height": height,
                    "url": f"/content/media/{output_name}"
                }]
            
            cap.release()
        except Exception as e:
            print(f"  ❌ Error extracting from {video_path.name}: {e}")
        
        return []
    
    def copy_image(self, image_path: Path, project_name: str) -> list:
        """Copy existing image file"""
        try:
            print(f"🖼️  Copying {image_path.name}...")
            
            output_name = f"{project_name}-{image_path.name}"
            output_path = self.output_dir / output_name
            
            shutil.copy2(image_path, output_path)
            
            # Get dimensions
            with Image.open(output_path) as img:
                width, height = img.size
            
            print(f"  ✅ Copied: {output_name} ({width}x{height})")
            
            return [{
                "type": "image",
                "width": width,
                "height": height,
                "url": f"/content/media/{output_name}"
            }]
        except Exception as e:
            print(f"  ❌ Error copying {image_path.name}: {e}")
        
        return []
    
    def extract_all(self) -> dict:
        """Extract images for all projects"""
        print("\n🎨 Starting archive image extraction...\n")
        
        results = {}
        
        for project_name, file_list in self.project_files.items():
            print(f"\n📦 Processing project: {project_name}")
            project_images = []
            
            for filename in file_list:
                # Search in archive and subdirectories
                file_paths = list(self.archive_path.rglob(filename))
                
                if not file_paths:
                    print(f"  ⚠️  File not found: {filename}")
                    continue
                
                file_path = file_paths[0]
                
                # Determine file type and extract
                if file_path.suffix.lower() == '.pdf':
                    images = self.extract_pdf_images(file_path, project_name, max_images=3)
                    project_images.extend(images)
                
                elif file_path.suffix.lower() in ['.mp4', '.mov']:
                    images = self.extract_video_frame(file_path, project_name)
                    project_images.extend(images)
                
                elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    images = self.copy_image(file_path, project_name)
                    project_images.extend(images)
            
            if project_images:
                results[project_name] = project_images
                print(f"  ✅ Total images for {project_name}: {len(project_images)}")
        
        print(f"\n✅ Extraction complete! Total projects: {len(results)}")
        return results
    
    def save_mapping(self, results: dict, output_file: str = "image_mapping.json"):
        """Save project-to-image mapping"""
        output_path = self.output_dir.parent / output_file
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Saved image mapping to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract images from Jh-ARCHV')
    parser.add_argument('--archive', required=True, help='Path to Jh-ARCHV folder')
    parser.add_argument('--output', default='content/media', help='Output directory')
    
    args = parser.parse_args()
    
    extractor = ArchiveImageExtractor(args.archive, args.output)
    results = extractor.extract_all()
    extractor.save_mapping(results)
    
    print("\n🎉 Done! Images ready for Joju profile.")
    print(f"📁 Check: {args.output}")


if __name__ == '__main__':
    main()
