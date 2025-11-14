#!/usr/bin/env python3
"""
Joju Image Capture System
Automated screenshot capture and image management for Joju profiles

Features:
- Capture screenshots from URLs at multiple viewports
- Connect to Figma API for design exports
- Auto-generate attachment JSON entries
- Get image dimensions automatically
- Organize files in /content/media/
"""

import json
import os
from pathlib import Path
from PIL import Image
import requests
from playwright.sync_api import sync_playwright
from typing import List, Dict, Optional
import time

class JojuImageCapture:
    def __init__(self, config_path: str):
        """Initialize the image capture system"""
        self.config_path = Path(config_path)
        self.project_root = self.config_path.parent
        self.media_dir = self.project_root / "content" / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)
        
        # Load Joju profile data
        with open(self.config_path, 'r') as f:
            self.profile_data = json.load(f)
    
    def capture_screenshot(self, url: str, output_name: str, viewport: Dict[str, int] = None) -> Optional[Dict]:
        """
        Capture screenshot from URL using Playwright
        
        Args:
            url: URL to capture
            output_name: Base name for output file (without extension)
            viewport: Dict with 'width' and 'height' keys
        
        Returns:
            Dict with attachment info or None if failed
        """
        if viewport is None:
            viewport = {'width': 1920, 'height': 1080}
        
        output_path = self.media_dir / f"{output_name}.png"
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport=viewport)
                page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait a bit for animations/lazy loading
                time.sleep(2)
                
                # Take screenshot
                page.screenshot(path=str(output_path), full_page=False)
                browser.close()
            
            # Get actual dimensions
            with Image.open(output_path) as img:
                width, height = img.size
            
            return {
                "type": "image",
                "width": width,
                "height": height,
                "url": f"/content/media/{output_name}.png"
            }
        
        except Exception as e:
            print(f"❌ Failed to capture {url}: {e}")
            return None
    
    def capture_multiple_viewports(self, url: str, base_name: str) -> List[Dict]:
        """
        Capture screenshots at multiple viewport sizes
        
        Args:
            url: URL to capture
            base_name: Base name for output files
        
        Returns:
            List of attachment dicts
        """
        viewports = {
            'desktop': {'width': 1920, 'height': 1080},
            'tablet': {'width': 768, 'height': 1024},
            'mobile': {'width': 375, 'height': 812}
        }
        
        attachments = []
        
        for viewport_name, viewport_size in viewports.items():
            output_name = f"{base_name}-{viewport_name}"
            print(f"📸 Capturing {viewport_name} view of {url}...")
            
            attachment = self.capture_screenshot(url, output_name, viewport_size)
            if attachment:
                attachments.append(attachment)
                print(f"✅ Saved: {output_name}.png")
        
        return attachments
    
    def export_from_figma(self, figma_url: str, output_name: str, figma_token: str) -> Optional[Dict]:
        """
        Export image from Figma using API
        
        Args:
            figma_url: Figma file/frame URL
            output_name: Base name for output file
            figma_token: Figma personal access token
        
        Returns:
            Dict with attachment info or None if failed
        """
        # Parse Figma URL to get file key and node ID
        # Format: https://www.figma.com/file/{file_key}/{title}?node-id={node_id}
        
        try:
            parts = figma_url.split('/')
            file_key = parts[4] if len(parts) > 4 else None
            
            if not file_key:
                print(f"❌ Invalid Figma URL: {figma_url}")
                return None
            
            # Extract node ID from URL if present
            node_id = None
            if 'node-id=' in figma_url:
                node_id = figma_url.split('node-id=')[1].split('&')[0]
            
            headers = {'X-Figma-Token': figma_token}
            
            # Get image export URL from Figma API
            api_url = f"https://api.figma.com/v1/images/{file_key}"
            params = {
                'format': 'png',
                'scale': 2
            }
            
            if node_id:
                params['ids'] = node_id
            
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'images' not in data or not data['images']:
                print(f"❌ No images returned from Figma API")
                return None
            
            # Get first image URL
            image_url = list(data['images'].values())[0]
            
            # Download image
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            output_path = self.media_dir / f"{output_name}.png"
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            # Get dimensions
            with Image.open(output_path) as img:
                width, height = img.size
            
            print(f"✅ Exported from Figma: {output_name}.png")
            
            return {
                "type": "image",
                "width": width,
                "height": height,
                "url": f"/content/media/{output_name}.png"
            }
        
        except Exception as e:
            print(f"❌ Failed to export from Figma: {e}")
            return None
    
    def scan_existing_images(self) -> Dict[str, Dict]:
        """
        Scan /content/media/ folder and generate attachment entries for existing images
        
        Returns:
            Dict mapping filenames to attachment info
        """
        attachments = {}
        
        if not self.media_dir.exists():
            return attachments
        
        for img_path in self.media_dir.glob('*.png'):
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                
                attachments[img_path.name] = {
                    "type": "image",
                    "width": width,
                    "height": height,
                    "url": f"/content/media/{img_path.name}"
                }
            except Exception as e:
                print(f"⚠️  Skipping {img_path.name}: {e}")
        
        return attachments
    
    def update_project_attachments(self, project_id: str, attachments: List[Dict]):
        """
        Update a project's attachments in the Joju profile JSON
        
        Args:
            project_id: Project ID to update
            attachments: List of attachment dicts
        """
        # Find and update project
        for project in self.profile_data.get('projects', []):
            if project.get('id') == project_id:
                project['attachments'] = attachments
                print(f"✅ Updated attachments for project: {project.get('title', project_id)}")
                return True
        
        print(f"⚠️  Project not found: {project_id}")
        return False
    
    def save_profile(self):
        """Save updated profile data back to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.profile_data, f, indent=2)
        print(f"✅ Saved profile to: {self.config_path}")
    
    def capture_portfolio_projects(self, portfolio_url: str, figma_token: Optional[str] = None):
        """
        Automated workflow: Capture images for all projects with URLs
        
        Args:
            portfolio_url: Base portfolio URL
            figma_token: Optional Figma API token
        """
        print("\n🎨 Starting automated image capture...\n")
        
        for project in self.profile_data.get('projects', []):
            project_id = project.get('id')
            project_title = project.get('title', 'Untitled')
            project_url = project.get('url')
            
            if not project_url:
                print(f"⏭️  Skipping {project_title} (no URL)")
                continue
            
            print(f"\n📦 Processing: {project_title}")
            print(f"   URL: {project_url}")
            
            # Determine if it's a Figma URL
            if 'figma.com' in project_url and figma_token:
                # Export from Figma
                attachment = self.export_from_figma(
                    project_url,
                    f"{project_id}",
                    figma_token
                )
                if attachment:
                    self.update_project_attachments(project_id, [attachment])
            else:
                # Capture screenshot (desktop only for now)
                attachment = self.capture_screenshot(
                    project_url,
                    f"{project_id}",
                    {'width': 1920, 'height': 1080}
                )
                if attachment:
                    self.update_project_attachments(project_id, [attachment])
        
        # Save updated profile
        self.save_profile()
        print("\n✅ Image capture complete!")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Joju Image Capture System')
    parser.add_argument('--config', required=True, help='Path to joju_upload_ready.json')
    parser.add_argument('--figma-token', help='Figma personal access token')
    parser.add_argument('--portfolio-url', help='Base portfolio URL')
    parser.add_argument('--scan-only', action='store_true', help='Only scan existing images')
    
    args = parser.parse_args()
    
    capturer = JojuImageCapture(args.config)
    
    if args.scan_only:
        print("🔍 Scanning existing images...")
        images = capturer.scan_existing_images()
        print(f"\n✅ Found {len(images)} images:")
        for filename, info in images.items():
            print(f"   {filename}: {info['width']}x{info['height']}")
    else:
        capturer.capture_portfolio_projects(
            args.portfolio_url or "https://favorite-day-425385.framer.app/",
            args.figma_token
        )


if __name__ == '__main__':
    main()
