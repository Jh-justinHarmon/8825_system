#!/usr/bin/env python3
"""
WHEN76 CSV Parser
Parses WHEN76 task CSV and extracts metadata
"""

import csv
import json
from pathlib import Path
from datetime import datetime

class WHEN76Parser:
    """Parse WHEN76 task CSV files"""
    
    def __init__(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "config"))
        from file_router import get_intake
        self.csv_path = get_intake() / "WHEN76 Tasks 233fe28ff8d6806184b3d2f3dd051069_all.csv"
    
    def parse_csv(self):
        """
        Parse WHEN76 CSV file
        
        Returns:
            list: Task records
        """
        if not self.csv_path.exists():
            return []
        
        tasks = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    task = self._parse_row(row)
                    if task:
                        tasks.append(task)
        
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            return []
        
        return tasks
    
    def _parse_row(self, row):
        """Parse single CSV row into task dict"""
        # Extract common fields (adjust based on actual CSV structure)
        task = {
            "id": row.get("id", ""),
            "title": row.get("title", row.get("name", "")),
            "description": row.get("description", ""),
            "status": row.get("status", ""),
            "created": row.get("created", ""),
            "updated": row.get("updated", ""),
            "assignee": row.get("assignee", ""),
            "tags": self._parse_tags(row.get("tags", "")),
            "raw": row  # Keep original data
        }
        
        return task
    
    def _parse_tags(self, tags_str):
        """Parse tags string into list"""
        if not tags_str:
            return []
        
        # Handle comma-separated or space-separated tags
        tags = [t.strip() for t in tags_str.replace(',', ' ').split()]
        return tags
    
    def get_task_by_id(self, task_id):
        """Get specific task by ID"""
        tasks = self.parse_csv()
        
        for task in tasks:
            if task.get("id") == task_id:
                return task
        
        return None
    
    def get_tasks_by_status(self, status):
        """Get tasks by status"""
        tasks = self.parse_csv()
        
        return [t for t in tasks if t.get("status", "").lower() == status.lower()]
    
    def search_tasks(self, query):
        """Search tasks by query"""
        tasks = self.parse_csv()
        query_lower = query.lower()
        
        matching = []
        for task in tasks:
            # Search in title and description
            if query_lower in task.get("title", "").lower():
                matching.append(task)
            elif query_lower in task.get("description", "").lower():
                matching.append(task)
        
        return matching
    
    def export_to_json(self, output_path):
        """Export tasks to JSON"""
        tasks = self.parse_csv()
        
        output = {
            "source": str(self.csv_path),
            "parsed_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "tasks": tasks
        }
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        return output_path
    
    def get_statistics(self):
        """Get task statistics"""
        tasks = self.parse_csv()
        
        stats = {
            "total": len(tasks),
            "by_status": {},
            "by_assignee": {},
            "tags": set()
        }
        
        for task in tasks:
            # Count by status
            status = task.get("status", "unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # Count by assignee
            assignee = task.get("assignee", "unassigned")
            stats["by_assignee"][assignee] = stats["by_assignee"].get(assignee, 0) + 1
            
            # Collect tags
            stats["tags"].update(task.get("tags", []))
        
        stats["tags"] = list(stats["tags"])
        
        return stats
