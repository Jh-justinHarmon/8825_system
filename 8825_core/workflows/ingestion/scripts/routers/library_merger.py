#!/usr/bin/env python3
"""
Library Merger
Merges ingested files into project libraries
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'utils'))
from paths import get_system_root, get_user_dir

# Library paths
BASE_PATH = get_system_root()
JOJU_LIBRARY = get_user_dir('justin_harmon') / "joju/libraries/justin_harmon_master_library.json"
HCSS_LIBRARY = BASE_PATH / "Documents/HCSS/library/hcss_master_library.json"
RAL_LIBRARY = BASE_PATH / "Documents/RAL/library/ral_master_library.json"
PROJECTS_LIBRARY = BASE_PATH / "Documents/76/library/projects_master_library.json"
WHEN76_LIBRARY = BASE_PATH / "Documents/76/when76/library/when76_master_library.json"
SYSTEM_LIBRARY = BASE_PATH / "Documents/8825/library/system_master_library.json"

class LibraryMerger:
    """Merge files into project libraries"""
    
    def __init__(self):
        self.libraries = {
            "joju": JOJU_LIBRARY,
            "hcss": HCSS_LIBRARY,
            "ral": RAL_LIBRARY,
            "76": PROJECTS_LIBRARY,
            "when76": WHEN76_LIBRARY,
            "8825": SYSTEM_LIBRARY
        }
        
        # Ensure library directories exist
        for library_path in self.libraries.values():
            library_path.parent.mkdir(parents=True, exist_ok=True)
            if not library_path.exists():
                self._init_library(library_path)
    
    def merge_to_library(self, file_data, classification, routing_result):
        """
        Merge file metadata into appropriate library
        
        Args:
            file_data: File metadata and content
            classification: Classification result
            routing_result: Routing result
        
        Returns:
            dict: Merge result
        """
        project = classification.get("project")
        category = classification.get("category")
        
        result = {
            "merged": False,
            "library": None,
            "action": None,
            "entry_id": None
        }
        
        # Route to appropriate library based on project and subfolder
        library_key = None
        subfolder = classification.get("subfolder")
        
        if project == "76" and self._is_profile_related(file_data, classification):
            library_key = "joju"
        elif project == "76" and subfolder == "when76":
            library_key = "when76"
        elif project == "HCSS":
            library_key = "hcss"
        elif project == "RAL":
            library_key = "ral"
        elif project == "76":
            library_key = "76"
        elif project == "8825":
            library_key = "8825"
        
        if library_key:
            return self._merge_to_library(library_key, file_data, classification)
        
        result["action"] = "no_library_match"
        return result
    
    def _is_profile_related(self, file_data, classification):
        """Check if file is profile-related"""
        keywords = file_data.get("content_data", {}).get("keywords", [])
        tags = classification.get("tags", [])
        
        profile_indicators = ["joju", "profile", "cv", "resume", "portfolio"]
        
        return any(indicator in keywords + tags for indicator in profile_indicators)
    
    def _init_library(self, library_path):
        """Initialize empty library file"""
        library = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "ingested_files": [],
            "entities": [],
            "relationships": [],
            "timeline": []
        }
        with open(library_path, 'w') as f:
            json.dump(library, f, indent=2)
    
    def _merge_to_library(self, library_key, file_data, classification):
        """Universal library merge method"""
        result = {
            "merged": False,
            "library": library_key,
            "action": None,
            "entry_id": None
        }
        
        library_path = self.libraries.get(library_key)
        if not library_path or not library_path.exists():
            result["action"] = "library_not_found"
            return result
        
        try:
            # Load library
            with open(library_path, 'r') as f:
                library = json.load(f)
            
            # Extract relevant data
            filename = file_data.get("metadata", {}).get("filename")
            category = classification.get("category")
            tags = classification.get("tags", [])
            
            # Create library entry
            entry = {
                "id": self._generate_entry_id(filename),
                "source_file": filename,
                "ingested_at": datetime.now().isoformat(),
                "category": category,
                "tags": tags,
                "metadata": file_data.get("metadata", {}),
                "classification": classification
            }
            
            # Check if entry already exists
            existing_entry = self._find_existing_entry(library, filename)
            
            if existing_entry:
                # Update existing entry
                result["action"] = "updated"
                result["entry_id"] = existing_entry.get("id")
                self._update_entry(library, existing_entry["id"], entry)
            else:
                # Add new entry
                result["action"] = "created"
                result["entry_id"] = entry["id"]
                self._add_entry(library, entry)
            
            # Save library
            with open(library_path, 'w') as f:
                json.dump(library, f, indent=2)
            
            result["merged"] = True
            
        except Exception as e:
            result["action"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _generate_entry_id(self, filename):
        """Generate unique entry ID"""
        import hashlib
        timestamp = datetime.now().isoformat()
        hash_input = f"{filename}_{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def _find_existing_entry(self, library, filename):
        """Find existing entry in library"""
        # Check if library has ingestion tracking
        if "ingested_files" not in library:
            library["ingested_files"] = []
        
        for entry in library.get("ingested_files", []):
            if entry.get("source_file") == filename:
                return entry
        
        return None
    
    def _update_entry(self, library, entry_id, new_data):
        """Update existing library entry"""
        for i, entry in enumerate(library.get("ingested_files", [])):
            if entry.get("id") == entry_id:
                # Merge data
                entry.update({
                    "updated_at": datetime.now().isoformat(),
                    "metadata": new_data.get("metadata"),
                    "classification": new_data.get("classification")
                })
                library["ingested_files"][i] = entry
                break
    
    def _add_entry(self, library, entry):
        """Add new entry to library"""
        if "ingested_files" not in library:
            library["ingested_files"] = []
        
        library["ingested_files"].append(entry)
    
    def get_library_stats(self, library_name):
        """Get statistics for a library"""
        if library_name not in self.libraries:
            return None
        
        library_path = self.libraries[library_name]
        
        if not library_path.exists():
            return None
        
        try:
            with open(library_path, 'r') as f:
                library = json.load(f)
            
            return {
                "total_entries": len(library.get("ingested_files", [])),
                "last_updated": library.get("ingested_files", [{}])[-1].get("ingested_at") if library.get("ingested_files") else None,
                "categories": self._count_categories(library)
            }
        except Exception:
            return None
    
    def _count_categories(self, library):
        """Count entries by category"""
        categories = {}
        for entry in library.get("ingested_files", []):
            category = entry.get("category", "Unknown")
            categories[category] = categories.get(category, 0) + 1
        return categories
