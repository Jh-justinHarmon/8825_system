#!/usr/bin/env python3
"""
Render PDF pages as high-quality images for Joju profile
Focuses on project and work-related PDFs
"""

import fitz  # PyMuPDF
from pathlib import Path
from PIL import Image
import json

class PDFPageRenderer:
    def __init__(self, archive_path: str, output_dir: str):
        self.archive_path = Path(archive_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Project/work PDFs to render
        # Format: {project_id: [(filename, [page_numbers])]}
        self.pdf_mapping = {
            'amare_stoudemire': [
                ('Amare_presentation.pdf', [1, 2, 3, 4])  # First 4 pages
            ],
            'shinola': [
                ('shinola_collab_collection.pdf', [1, 3, 5, 7]),
                ('shinola_collab_collection_1_watch_monster_102121.pdf', [1, 2, 3])
            ],
            'nike_vision': [
                ('2013_NKvsn-DD.pdf', [1, 2, 3, 5]),
                ('nikeTrainingProposal.pdf', [1, 2, 3])
            ],
            'costa': [
                ('2017_costa-Catalogue.pdf', [1, 2, 5, 10, 15]),
                ('LSD_Costa - Design Strategy 2016.pdf', [1, 3, 5, 10])
            ],
            'tiger_cut': [
                ('SP12_TIGER-CUT_SKETCHBOOK.pdf', [1, 2, 3, 4])
            ],
            'dragon': [
                ('dragon_prelim-moodboards_092118_outline.pdf', [1, 2, 3]),
                ('dragon_sketchbook_review_102318_marchonFEEDBACK.pdf', [1, 2, 3, 5])
            ],
            'fossil': [
                ('relic_cnsmrPRFL.pdf', [1, 2, 3])
            ],
            'marchon': [
                ('High End 1 Sun - 3D - live model.pdf', [1, 2, 3]),
                ('freestyle_02.pdf', [1, 2])
            ]
        }
    
    def find_pdf(self, filename: str) -> Path:
        """Find PDF in archive (search recursively)"""
        results = list(self.archive_path.rglob(filename))
        if results:
            return results[0]
        return None
    
    def render_page(self, pdf_path: Path, page_num: int, project_id: str, 
                   dpi: int = 150) -> dict:
        """
        Render a single PDF page as high-quality image
        
        Args:
            pdf_path: Path to PDF file
            page_num: Page number (1-indexed)
            project_id: Project identifier
            dpi: Resolution (150 = good quality, 300 = high quality)
        
        Returns:
            Dict with attachment info or None if failed
        """
        try:
            doc = fitz.open(pdf_path)
            
            # Convert to 0-indexed
            page_index = page_num - 1
            
            if page_index >= len(doc):
                print(f"  ⚠️  Page {page_num} doesn't exist in {pdf_path.name}")
                doc.close()
                return None
            
            page = doc[page_index]
            
            # Calculate zoom for desired DPI
            # Default is 72 DPI, so zoom = desired_dpi / 72
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Save as PNG
            output_name = f"{project_id}-page{page_num}.png"
            output_path = self.output_dir / output_name
            
            pix.save(str(output_path))
            
            # Get dimensions
            width = pix.width
            height = pix.height
            
            doc.close()
            
            print(f"  ✅ Rendered: {output_name} ({width}x{height})")
            
            return {
                "type": "image",
                "width": width,
                "height": height,
                "url": f"/content/media/{output_name}"
            }
        
        except Exception as e:
            print(f"  ❌ Error rendering page {page_num} from {pdf_path.name}: {e}")
            return None
    
    def render_all(self, dpi: int = 150, max_per_project: int = 5) -> dict:
        """
        Render all specified PDF pages
        
        Args:
            dpi: Resolution (150 = good, 300 = high)
            max_per_project: Maximum images per project
        
        Returns:
            Dict mapping project_id to list of attachments
        """
        print(f"\n🎨 Rendering PDF pages at {dpi} DPI...\n")
        
        results = {}
        
        for project_id, pdf_list in self.pdf_mapping.items():
            print(f"\n📦 Processing project: {project_id}")
            project_images = []
            
            for filename, page_numbers in pdf_list:
                # Find PDF
                pdf_path = self.find_pdf(filename)
                
                if not pdf_path:
                    print(f"  ⚠️  PDF not found: {filename}")
                    continue
                
                print(f"📄 Rendering {filename}...")
                
                # Render specified pages
                for page_num in page_numbers[:max_per_project]:
                    if len(project_images) >= max_per_project:
                        print(f"  ⏭️  Reached max {max_per_project} images for {project_id}")
                        break
                    
                    attachment = self.render_page(pdf_path, page_num, project_id, dpi)
                    if attachment:
                        project_images.append(attachment)
                
                if len(project_images) >= max_per_project:
                    break
            
            if project_images:
                results[project_id] = project_images
                print(f"  ✅ Total images for {project_id}: {len(project_images)}")
        
        print(f"\n✅ Rendering complete! Total projects: {len(results)}")
        return results
    
    def save_mapping(self, results: dict, output_file: str = "image_mapping.json"):
        """Save project-to-image mapping"""
        output_path = self.output_dir.parent / output_file
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Saved image mapping to: {output_path}")
    
    def generate_summary(self, results: dict):
        """Print summary of rendered images"""
        print("\n" + "="*60)
        print("📊 RENDERING SUMMARY")
        print("="*60)
        
        total_images = sum(len(images) for images in results.values())
        
        print(f"\n✅ Total Projects: {len(results)}")
        print(f"✅ Total Images: {total_images}")
        print(f"\n📁 Images saved to: {self.output_dir}")
        
        print("\n📋 Images per project:")
        for project_id, images in sorted(results.items()):
            print(f"  • {project_id}: {len(images)} images")
        
        print("\n" + "="*60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Render PDF pages as images')
    parser.add_argument('--archive', required=True, help='Path to Jh-ARCHV folder')
    parser.add_argument('--output', default='content/media', help='Output directory')
    parser.add_argument('--dpi', type=int, default=150, 
                       help='Resolution (150=good, 300=high)')
    parser.add_argument('--max-per-project', type=int, default=5,
                       help='Maximum images per project')
    
    args = parser.parse_args()
    
    renderer = PDFPageRenderer(args.archive, args.output)
    results = renderer.render_all(dpi=args.dpi, max_per_project=args.max_per_project)
    renderer.save_mapping(results)
    renderer.generate_summary(results)
    
    print("\n🎉 Done! Review images and delete any you don't want.")
    print(f"📂 Open folder: open {args.output}")


if __name__ == '__main__':
    main()
