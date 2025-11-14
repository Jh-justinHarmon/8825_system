#!/usr/bin/env python3
"""
Brain File Updater - Stage 9
Updates the main brain file with lightweight, pertinent information from libraries
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'utils'))
from paths import get_system_root

class BrainUpdater:
    """Update main brain file with library changes"""
    
    def __init__(self, brain_path=None):
        self.brain_path = brain_path or (get_system_root() / "8825_brain.json")
        self.brain = self._load_brain()
    
    def _load_brain(self):
        """Load existing brain file or create new"""
        if self.brain_path.exists():
            with open(self.brain_path, 'r') as f:
                return json.load(f)
        
        return self._init_brain()
    
    def _init_brain(self):
        """Initialize new brain structure"""
        return {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "purpose": "Lightweight context for external LLMs",
                "mcp_server": "goose://8825-ingestion-engine",
                "full_system": "8825 Ingestion Engine"
            },
            "projects": {},
            "entities": {},
            "recent_activity": [],
            "key_relationships": [],
            "quick_stats": {},
            "mcp_endpoints": {}
        }
    
    def analyze_library_changes(self, library_key, library_data):
        """
        Analyze what changed in library and extract pertinent info
        
        Returns:
            dict: Lightweight summary of changes
        """
        changes = {
            "project": library_key,
            "timestamp": datetime.now().isoformat(),
            "new_files": 0,
            "updated_files": 0,
            "new_entities": [],
            "new_relationships": [],
            "key_insights": []
        }
        
        # Count new files
        ingested_files = library_data.get("ingested_files", [])
        changes["new_files"] = len([f for f in ingested_files if self._is_recent(f)])
        
        # Extract new entities
        entities = library_data.get("entities", [])
        changes["new_entities"] = self._extract_key_entities(entities)
        
        # Extract key relationships
        relationships = library_data.get("relationships", [])
        changes["new_relationships"] = self._extract_key_relationships(relationships)
        
        # Generate insights
        changes["key_insights"] = self._generate_insights(library_data)
        
        return changes
    
    def _is_recent(self, file_entry, hours=24):
        """Check if file was ingested recently"""
        ingested_at = file_entry.get("ingested_at", "")
        if not ingested_at:
            return False
        
        try:
            ingested_time = datetime.fromisoformat(ingested_at)
            now = datetime.now()
            diff = (now - ingested_time).total_seconds() / 3600
            return diff <= hours
        except:
            return False
    
    def _extract_key_entities(self, entities, limit=5):
        """Extract most important entities"""
        # Sort by mention count or confidence
        sorted_entities = sorted(
            entities,
            key=lambda e: len(e.get("mentions", [])),
            reverse=True
        )
        
        return [
            {
                "name": e.get("name"),
                "type": e.get("type"),
                "mentions": len(e.get("mentions", []))
            }
            for e in sorted_entities[:limit]
        ]
    
    def _extract_key_relationships(self, relationships, limit=10):
        """Extract most important relationships"""
        # Filter for high-confidence relationships
        key_rels = [
            r for r in relationships
            if r.get("confidence", 0) >= 80
        ]
        
        return key_rels[:limit]
    
    def _generate_insights(self, library_data):
        """Generate key insights from library"""
        insights = []
        
        # File count insight
        file_count = len(library_data.get("ingested_files", []))
        if file_count > 0:
            insights.append(f"{file_count} files in library")
        
        # Entity diversity
        entities = library_data.get("entities", [])
        entity_types = set(e.get("type") for e in entities)
        if entity_types:
            insights.append(f"{len(entity_types)} entity types tracked")
        
        # Timeline span
        timeline = library_data.get("timeline", [])
        if len(timeline) > 1:
            insights.append(f"Timeline spans {len(timeline)} events")
        
        return insights
    
    def update_brain(self, library_key, library_changes):
        """
        Update brain with library changes
        
        Keeps brain lightweight by:
        - Summarizing rather than copying
        - Keeping only recent activity
        - Limiting entity/relationship counts
        - Providing MCP endpoints for deep access
        """
        # Update project summary
        if library_key not in self.brain["projects"]:
            self.brain["projects"][library_key] = {
                "name": library_key,
                "file_count": 0,
                "last_activity": None,
                "key_entities": [],
                "mcp_query": f"goose://8825/libraries/{library_key}"
            }
        
        project = self.brain["projects"][library_key]
        project["file_count"] += library_changes.get("new_files", 0)
        project["last_activity"] = library_changes.get("timestamp")
        
        # Update entities (keep only top entities)
        new_entities = library_changes.get("new_entities", [])
        for entity in new_entities:
            entity_name = entity.get("name")
            if entity_name not in self.brain["entities"]:
                self.brain["entities"][entity_name] = {
                    "name": entity_name,
                    "type": entity.get("type"),
                    "projects": [],
                    "mcp_query": f"goose://8825/entities/{entity_name}"
                }
            
            # Add project to entity
            if library_key not in self.brain["entities"][entity_name]["projects"]:
                self.brain["entities"][entity_name]["projects"].append(library_key)
        
        # Add to recent activity (keep last 20)
        activity = {
            "timestamp": library_changes.get("timestamp"),
            "project": library_key,
            "action": "library_update",
            "summary": f"{library_changes.get('new_files', 0)} new files",
            "insights": library_changes.get("key_insights", [])
        }
        self.brain["recent_activity"].insert(0, activity)
        self.brain["recent_activity"] = self.brain["recent_activity"][:20]
        
        # Update quick stats
        self._update_stats()
        
        # Update MCP endpoints
        self._update_mcp_endpoints()
        
        # Update timestamp
        self.brain["last_updated"] = datetime.now().isoformat()
    
    def _update_stats(self):
        """Update quick statistics"""
        self.brain["quick_stats"] = {
            "total_projects": len(self.brain["projects"]),
            "total_entities": len(self.brain["entities"]),
            "recent_activities": len(self.brain["recent_activity"]),
            "total_files": sum(p.get("file_count", 0) for p in self.brain["projects"].values())
        }
    
    def _update_mcp_endpoints(self):
        """Update MCP server endpoints for deep integration"""
        self.brain["mcp_endpoints"] = {
            "search": "goose://8825/search?q={query}",
            "library": "goose://8825/libraries/{project}",
            "entity": "goose://8825/entities/{name}",
            "timeline": "goose://8825/timeline?start={start}&end={end}",
            "relationships": "goose://8825/relationships/{entity}",
            "stats": "goose://8825/stats"
        }
    
    def save_brain(self):
        """Save brain file"""
        # Ensure directory exists
        self.brain_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.brain_path, 'w') as f:
            json.dump(self.brain, f, indent=2)
    
    def get_brain_summary(self):
        """Get human-readable brain summary"""
        summary = []
        
        summary.append("# 8825 Brain Summary")
        summary.append(f"Last Updated: {self.brain.get('last_updated')}")
        summary.append("")
        
        # Projects
        summary.append("## Projects")
        for project_key, project in self.brain["projects"].items():
            summary.append(f"- **{project_key}**: {project.get('file_count', 0)} files")
        summary.append("")
        
        # Entities
        summary.append("## Key Entities")
        for entity_name, entity in list(self.brain["entities"].items())[:10]:
            projects = ", ".join(entity.get("projects", []))
            summary.append(f"- **{entity_name}** ({entity.get('type')}): {projects}")
        summary.append("")
        
        # Recent Activity
        summary.append("## Recent Activity")
        for activity in self.brain["recent_activity"][:5]:
            summary.append(f"- {activity.get('timestamp')}: {activity.get('summary')}")
        summary.append("")
        
        # Stats
        stats = self.brain.get("quick_stats", {})
        summary.append("## Quick Stats")
        summary.append(f"- Total Projects: {stats.get('total_projects', 0)}")
        summary.append(f"- Total Entities: {stats.get('total_entities', 0)}")
        summary.append(f"- Total Files: {stats.get('total_files', 0)}")
        summary.append("")
        
        # MCP Integration
        summary.append("## MCP Integration")
        summary.append("For deeper access, use MCP endpoints:")
        for endpoint_name, endpoint_url in self.brain.get("mcp_endpoints", {}).items():
            summary.append(f"- **{endpoint_name}**: `{endpoint_url}`")
        
        return "\n".join(summary)
    
    def process_library_update(self, library_key, library_path):
        """
        Complete brain update process for a library
        
        Returns:
            dict: Update result
        """
        try:
            # Load library
            with open(library_path, 'r') as f:
                library_data = json.load(f)
            
            # Analyze changes
            changes = self.analyze_library_changes(library_key, library_data)
            
            # Update brain
            self.update_brain(library_key, changes)
            
            # Save brain
            self.save_brain()
            
            return {
                "success": True,
                "library": library_key,
                "changes": changes,
                "brain_path": str(self.brain_path)
            }
        
        except Exception as e:
            return {
                "success": False,
                "library": library_key,
                "error": str(e)
            }
