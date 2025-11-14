#!/usr/bin/env python3
"""
FigJam API Client
Creates sticky notes in FigJam from processed data
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional

class FigJamClient:
    """Client for FigJam REST API"""
    
    BASE_URL = "https://api.figma.com/v1"
    
    # Sticky note colors in FigJam
    COLORS = {
        'yellow': '#FFF59D',
        'pink': '#FFB6C1',
        'blue': '#ADD8E6',
        'green': '#90EE90',
        'orange': '#FFC87C',
        'purple': '#D8BFD8',
        'white': '#FFFFFF'
    }
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize FigJam client
        
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
            'X-Figma-Token': self.access_token,
            'Content-Type': 'application/json'
        }
    
    def create_figjam_file(self, name: str = "Sticky Notes Board") -> str:
        """
        Create a new FigJam file
        
        Returns:
            file_key: The key of the created file
        """
        # Note: FigJam file creation requires team/project context
        # This is a placeholder - actual implementation depends on your Figma setup
        raise NotImplementedError(
            "File creation requires team context. "
            "Create a FigJam file manually and use add_stickies_to_file() instead."
        )
    
    def add_stickies_to_file(self, file_key: str, stickies_data: Dict) -> Dict:
        """
        Add sticky notes to an existing FigJam file
        
        Args:
            file_key: The FigJam file key (from URL)
            stickies_data: Processed sticky note data from sticky_processor
        
        Returns:
            Response data from Figma API
        """
        # Build node tree for sticky notes
        nodes = self._build_sticky_nodes(stickies_data)
        
        # Make API request
        url = f"{self.BASE_URL}/files/{file_key}/nodes"
        payload = {
            'nodes': nodes
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def _build_sticky_nodes(self, stickies_data: Dict) -> List[Dict]:
        """
        Build FigJam node structure from sticky data
        """
        nodes = []
        
        for cluster in stickies_data.get('clusters', []):
            for sticky in cluster.get('stickies', []):
                node = self._create_sticky_node(sticky)
                nodes.append(node)
        
        return nodes
    
    def _create_sticky_node(self, sticky: Dict) -> Dict:
        """
        Create a FigJam sticky note node
        """
        x, y, w, h = sticky['bbox']
        text = sticky['text']
        color = sticky['color']
        
        # Scale positions (photo pixels to FigJam coordinates)
        # FigJam uses different coordinate system
        figjam_x = x * 0.5  # Scale factor
        figjam_y = y * 0.5
        
        node = {
            'type': 'STICKY',
            'x': figjam_x,
            'y': figjam_y,
            'width': max(w * 0.5, 200),  # Minimum width
            'height': max(h * 0.5, 200),  # Minimum height
            'fills': [{
                'type': 'SOLID',
                'color': self._hex_to_rgb(self.COLORS.get(color, self.COLORS['yellow']))
            }],
            'characters': text,
            'style': {
                'fontFamily': 'Inter',
                'fontSize': 16,
                'textAlignHorizontal': 'LEFT',
                'textAlignVertical': 'TOP'
            }
        }
        
        return node
    
    def _hex_to_rgb(self, hex_color: str) -> Dict:
        """Convert hex color to RGB dict for Figma API"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return {'r': r, 'g': g, 'b': b}
    
    def get_file_info(self, file_key: str) -> Dict:
        """Get information about a FigJam file"""
        url = f"{self.BASE_URL}/files/{file_key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

class FigJamConverter:
    """Convert processed sticky data to FigJam"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.client = FigJamClient(access_token)
    
    def convert_and_upload(self, stickies_json_path: Path, file_key: str) -> Dict:
        """
        Convert processed sticky notes JSON to FigJam
        
        Args:
            stickies_json_path: Path to sticky_notes_processed.json
            file_key: FigJam file key to add stickies to
        
        Returns:
            API response
        """
        # Load processed data
        with open(stickies_json_path) as f:
            data = json.load(f)
        
        # Upload to FigJam
        print(f"Uploading {data[0]['total_stickies']} stickies to FigJam...")
        result = self.client.add_stickies_to_file(file_key, data[0])
        
        print("✓ Upload complete!")
        return result

def main():
    """
    Upload processed sticky notes to FigJam
    
    Usage:
        export FIGMA_ACCESS_TOKEN=your_token_here
        python3 figjam_api.py <file_key>
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 figjam_api.py <figjam_file_key>")
        print("\nGet file key from FigJam URL:")
        print("https://www.figma.com/file/FILE_KEY/...")
        print("\nSet your access token:")
        print("export FIGMA_ACCESS_TOKEN=your_token")
        sys.exit(1)
    
    file_key = sys.argv[1]
    
    # Find processed JSON
    downloads = Path.home() / 'Downloads'
    json_file = downloads / 'sticky_notes_processed.json'
    
    if not json_file.exists():
        print(f"Error: {json_file} not found")
        print("Run sticky_processor.py first to process images")
        sys.exit(1)
    
    # Convert and upload
    converter = FigJamConverter()
    converter.convert_and_upload(json_file, file_key)

if __name__ == '__main__':
    main()
