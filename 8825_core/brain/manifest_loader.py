import os
import json
from typing import Dict, List, Optional

class ManifestLoader:
    """
    Loads and manages AI Personality Manifests from the filesystem.
    """
    def __init__(self, manifests_dir: str):
        if not os.path.isdir(manifests_dir):
            raise FileNotFoundError(f"Manifests directory not found: {manifests_dir}")
        self.manifests_dir = manifests_dir
        self._manifests = self._load_all_manifests()

    def _load_all_manifests(self) -> Dict[str, Dict]:
        """Loads all .json manifests from the specified directory."""
        manifests = {}
        for filename in os.listdir(self.manifests_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.manifests_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        if 'model_id' in data:
                            manifests[data['model_id']] = data
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not load or parse manifest {filepath}: {e}")
        return manifests

    def get_manifest(self, model_id: str) -> Optional[Dict]:
        """
        Retrieves a specific manifest by its model_id.

        Args:
            model_id: The unique identifier for the model.

        Returns:
            A dictionary containing the manifest data, or None if not found.
        """
        return self._manifests.get(model_id)

    def list_manifests(self) -> List[Dict]:
        """
        Returns a list of all loaded manifests.

        Returns:
            A list of manifest dictionaries.
        """
        return list(self._manifests.values())

    def get_available_models(self) -> List[str]:
        """
        Returns a list of model_ids for all available manifests.
        """
        return list(self._manifests.keys())

# Example usage (for testing or as a CLI)
if __name__ == '__main__':
    # Assuming the script is run from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    manifests_path = os.path.join(project_root, '8825_core', 'ai_manifests')
    
    try:
        loader = ManifestLoader(manifests_path)
        
        print("✅ Manifest Loader Initialized")
        print("-" * 20)
        
        available_models = loader.get_available_models()
        print(f"Found {len(available_models)} manifests for models: {', '.join(available_models)}")
        print("-" * 20)

        # Test getting a specific manifest
        sonnet_id = 'claude-3.5-sonnet-20240620'
        sonnet_manifest = loader.get_manifest(sonnet_id)
        if sonnet_manifest:
            print(f"Successfully loaded manifest for '{sonnet_manifest.get('name')}':")
            print(json.dumps(sonnet_manifest, indent=2))
        else:
            print(f"❌ Could not find manifest for model_id: {sonnet_id}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure the 'ai_manifests' directory exists and contains manifest files.")
