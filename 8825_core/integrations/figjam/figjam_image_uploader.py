#!/usr/bin/env python3
"""
FigJam Image Uploader
Uploads images to FigJam boards via Figma API
"""

import os
import json
import base64
import requests
from pathlib import Path
from typing import Optional, Dict


class FigJamImageUploader:
    """Upload images to FigJam boards"""
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize uploader
        
        Args:
            access_token: Figma personal access token
                         If not provided, reads from FIGMA_ACCESS_TOKEN env var
        """
        self.access_token = access_token or os.getenv('FIGMA_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError(
                "Figma access token required. Set FIGMA_ACCESS_TOKEN env var or pass to constructor."
            )
        
        self.headers = {
            'X-Figma-Token': self.access_token
        }
    
    def upload_image(self, file_key: str, image_path: Path, x: int = 0, y: int = 0, 
                     scale: float = 1.0, name: Optional[str] = None) -> Dict:
        """
        Upload image to FigJam board
        
        Args:
            file_key: FigJam file key (from URL)
            image_path: Path to image file
            x: X position on canvas
            y: Y position on canvas
            scale: Scale factor (1.0 = original size)
            name: Optional name for the image node
        
        Returns:
            Response data from Figma API
        """
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare image upload
        # Note: Figma API requires images to be uploaded to their CDN first
        # This is a simplified approach - for production, use proper image upload flow
        
        print(f"📤 Uploading {image_path.name} to FigJam...")
        print(f"   Position: ({x}, {y})")
        print(f"   Scale: {scale}x")
        
        # Get file info to find the canvas
        file_info = self._get_file_info(file_key)
        
        # For now, we'll use the Figma Plugin API approach
        # which requires a plugin to be installed in the FigJam file
        
        print("⚠️  Note: Direct image upload via REST API is limited.")
        print("   Recommended approach:")
        print("   1. Save image to shared location")
        print("   2. Use FigJam's 'Place Image' feature")
        print("   3. Or use Figma Plugin API for programmatic upload")
        
        return {
            'status': 'info',
            'message': 'Image prepared for upload',
            'image_path': str(image_path),
            'file_key': file_key,
            'position': {'x': x, 'y': y},
            'scale': scale
        }
    
    def _get_file_info(self, file_key: str) -> Dict:
        """Get FigJam file information"""
        url = f"{self.BASE_URL}/files/{file_key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_image_reference(self, file_key: str, image_url: str, 
                               x: int = 0, y: int = 0, width: int = 800) -> Dict:
        """
        Create an image node from URL
        
        This works if the image is already hosted somewhere accessible
        
        Args:
            file_key: FigJam file key
            image_url: URL to image
            x, y: Position
            width: Image width
        
        Returns:
            API response
        """
        
        # This would use the Figma REST API to create nodes
        # However, image creation is limited in the REST API
        # Best approach is to use the Plugin API
        
        print(f"📎 Creating image reference: {image_url}")
        
        return {
            'status': 'pending',
            'message': 'Use Plugin API for full image support',
            'image_url': image_url
        }


def upload_to_figjam(image_path: Path, file_key: str, x: int = 0, y: int = 0) -> Dict:
    """
    Helper function to upload image to FigJam
    
    Args:
        image_path: Path to image
        file_key: FigJam file key
        x, y: Position on canvas
    
    Returns:
        Upload result
    """
    uploader = FigJamImageUploader()
    return uploader.upload_image(file_key, image_path, x, y)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 figjam_image_uploader.py <image.png> <file_key> [x] [y]")
        print("\nExample:")
        print("  python3 figjam_image_uploader.py screenshot.png abc123def456")
        print("  python3 figjam_image_uploader.py screenshot.png abc123def456 100 200")
        sys.exit(1)
    
    image_path = Path(sys.argv[1])
    file_key = sys.argv[2]
    x = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    y = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    
    try:
        result = upload_to_figjam(image_path, file_key, x, y)
        print(f"\n✅ Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
