#!/usr/bin/env python3
"""
Manifest Provider
Loads and provides AI personality manifests
"""
import json
from pathlib import Path
from typing import Dict, List, Optional


class ManifestProvider:
    """Loads and provides AI manifests"""
    
    def __init__(self, manifests_dir: Path):
        self.manifests_dir = Path(manifests_dir)
        self._cache = {}
        self._load_manifests()
    
    def _load_manifests(self):
        """Load all manifest files"""
        if not self.manifests_dir.exists():
            print(f"Warning: Manifests directory not found: {self.manifests_dir}")
            return
        
        for file in self.manifests_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    if 'model_id' in data:
                        self._cache[data['model_id']] = data
                        print(f"Loaded manifest: {data.get('name', file.name)}")
            except Exception as e:
                print(f"Warning: Could not load {file}: {e}")
    
    def get_manifest(self, model_id: str) -> Optional[Dict]:
        """Get manifest for a specific model"""
        return self._cache.get(model_id)
    
    def list_models(self) -> List[Dict]:
        """List all available models"""
        return [
            {
                "model_id": m["model_id"],
                "name": m.get("name", "Unknown"),
                "description": m.get("description", "")
            }
            for m in self._cache.values()
        ]
    
    def get_all_manifests(self) -> Dict[str, Dict]:
        """Get all manifests"""
        return self._cache.copy()
