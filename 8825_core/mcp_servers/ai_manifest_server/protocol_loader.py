#!/usr/bin/env python3
"""
Protocol Loader
Loads protocol file contents for AI manifests
"""
from pathlib import Path
from typing import Dict, List


class ProtocolLoader:
    """Loads protocol file contents"""
    
    def __init__(self, protocols_dir: Path):
        self.protocols_dir = Path(protocols_dir)
    
    def get_priority_protocols(self, model_id: str, manifest_provider) -> Dict:
        """Get content of priority protocols for a model"""
        manifest = manifest_provider.get_manifest(model_id)
        if not manifest:
            return {"error": f"No manifest for {model_id}"}
        
        priority_protocols = manifest.get("priority_protocols", [])
        protocols_content = {}
        
        for protocol_name in priority_protocols:
            protocol_path = self.protocols_dir / protocol_name
            
            if protocol_path.exists():
                try:
                    with open(protocol_path, 'r') as f:
                        content = f.read()
                        protocols_content[protocol_name] = {
                            "path": str(protocol_path),
                            "content": content,
                            "length": len(content)
                        }
                except Exception as e:
                    protocols_content[protocol_name] = {
                        "error": f"Error loading: {e}"
                    }
            else:
                protocols_content[protocol_name] = {
                    "error": "File not found",
                    "expected_path": str(protocol_path)
                }
        
        return protocols_content
    
    def get_protocol(self, protocol_name: str) -> Dict:
        """Get a single protocol by name"""
        protocol_path = self.protocols_dir / protocol_name
        
        if protocol_path.exists():
            try:
                with open(protocol_path, 'r') as f:
                    return {
                        "name": protocol_name,
                        "path": str(protocol_path),
                        "content": f.read()
                    }
            except Exception as e:
                return {"error": f"Error loading: {e}"}
        
        return {"error": "File not found", "expected_path": str(protocol_path)}
