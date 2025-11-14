#!/usr/bin/env python3
"""
8825 v3.0 Index Builder
Builds per-focus and master indexes for fast discovery
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class IndexBuilder:
    """Builds indexes for 8825 v3.0"""
    
    def __init__(self, v3_root: Path):
        self.v3_root = Path(v3_root)
        self.index_dir = self.v3_root / "8825_index"
        self.focuses = ["joju", "hcss", "jh_assistant"]
        
    def build_focus_index(self, focus: str) -> Dict[str, Any]:
        """Build index for a specific focus"""
        print(f"Building index for {focus}...")
        
        focus_dir = self.v3_root / "focuses" / focus
        user_data_dir = self.v3_root / "users" / "justin_harmon" / focus
        
        index = {
            "focus": focus,
            "version": "3.0.0",
            "built_at": datetime.now().isoformat(),
            "files": {},
            "concepts": {},
            "stats": {
                "total_files": 0,
                "total_size": 0,
                "file_types": {}
            }
        }
        
        # Index focus directory
        if focus_dir.exists():
            index["files"].update(self._index_directory(focus_dir, "focus"))
        
        # Index user data
        if user_data_dir.exists():
            index["files"].update(self._index_directory(user_data_dir, "user"))
        
        # Update stats
        index["stats"]["total_files"] = len(index["files"])
        
        return index
    
    def _index_directory(self, directory: Path, source: str) -> Dict[str, Any]:
        """Index all files in a directory"""
        files = {}
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                rel_path = str(file_path.relative_to(self.v3_root))
                
                files[rel_path] = {
                    "type": file_path.suffix[1:] if file_path.suffix else "unknown",
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "source": source
                }
        
        return files
    
    def build_master_index(self, focus_indexes: Dict[str, Dict]) -> Dict[str, Any]:
        """Build master cross-focus index"""
        print("Building master index...")
        
        master = {
            "version": "3.0.0",
            "built_at": datetime.now().isoformat(),
            "focuses": list(focus_indexes.keys()),
            "files": {},
            "concepts": {},
            "stats": {
                "total_files": 0,
                "total_focuses": len(focus_indexes),
                "by_focus": {}
            }
        }
        
        # Aggregate all files
        for focus, index in focus_indexes.items():
            master["files"].update(index["files"])
            master["stats"]["by_focus"][focus] = index["stats"]
            master["stats"]["total_files"] += index["stats"]["total_files"]
        
        return master
    
    def build_concept_index(self) -> Dict[str, Any]:
        """Build concept index (cross-focus concepts)"""
        print("Building concept index...")
        
        # Placeholder - would extract concepts from all files
        concepts = {
            "version": "3.0.0",
            "built_at": datetime.now().isoformat(),
            "concepts": {
                "Achievement of Fact": {
                    "definition": "Proof-based achievement validation",
                    "files": ["users/justin_harmon/joju/master_library.json"],
                    "focuses": ["joju"]
                },
                "Scope Discipline": {
                    "definition": "Minimal viable solution approach",
                    "files": ["8825_core/system/8825_core.json"],
                    "focuses": ["all"]
                }
            }
        }
        
        return concepts
    
    def build_refs_graph(self) -> Dict[str, Any]:
        """Build references graph (knowledge graph)"""
        print("Building refs graph...")
        
        # Placeholder - would build actual graph
        graph = {
            "version": "3.0.0",
            "built_at": datetime.now().isoformat(),
            "nodes": {},
            "edges": []
        }
        
        return graph
    
    def build_all(self):
        """Build all indexes"""
        print("=" * 70)
        print("8825 v3.0 Index Builder")
        print("=" * 70)
        print()
        
        # Create index directory
        self.index_dir.mkdir(exist_ok=True)
        
        # Build per-focus indexes
        focus_indexes = {}
        for focus in self.focuses:
            index = self.build_focus_index(focus)
            focus_indexes[focus] = index
            
            # Save focus index
            output_file = self.index_dir / f"{focus}_index.json"
            with open(output_file, 'w') as f:
                json.dump(index, f, indent=2)
            print(f"  ✅ Saved {output_file.name}")
        
        print()
        
        # Build master index
        master = self.build_master_index(focus_indexes)
        output_file = self.index_dir / "master_index.json"
        with open(output_file, 'w') as f:
            json.dump(master, f, indent=2)
        print(f"  ✅ Saved {output_file.name}")
        
        # Build concept index
        concepts = self.build_concept_index()
        output_file = self.index_dir / "concept_index.json"
        with open(output_file, 'w') as f:
            json.dump(concepts, f, indent=2)
        print(f"  ✅ Saved {output_file.name}")
        
        # Build refs graph
        graph = self.build_refs_graph()
        output_file = self.index_dir / "refs_graph.json"
        with open(output_file, 'w') as f:
            json.dump(graph, f, indent=2)
        print(f"  ✅ Saved {output_file.name}")
        
        print()
        print("=" * 70)
        print("Index Building Complete!")
        print("=" * 70)
        print(f"Total files indexed: {master['stats']['total_files']}")
        print(f"Focuses indexed: {', '.join(self.focuses)}")
        print()

if __name__ == "__main__":
    # Get v3.0 root directory
    v3_root = Path(__file__).parent.parent.parent
    
    # Build all indexes
    builder = IndexBuilder(v3_root)
    builder.build_all()
