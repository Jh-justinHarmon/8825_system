#!/usr/bin/env python3
"""
Task Manager - Create, list, update, and manage Joju tasks
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from notion_sync import NotionSync


class TaskManager:
    """Manage Joju tasks"""
    
    def __init__(self):
        self.sync = NotionSync()
        self.local_dir = Path(__file__).parent / 'local'
        self.cache_file = self.local_dir / 'tasks.json'
    
    def create(self, title: str, task_type: str = 'Feature', 
               priority: str = 'Medium', source: str = 'Team Idea',
               description: str = '', tags: List[str] = None,
               effort: int = None, due_date: str = None) -> Optional[str]:
        """Create a new task"""
        
        print(f"\n{'='*80}")
        print(f"Creating Task: {title}")
        print(f"{'='*80}\n")
        
        task = {
            'title': title,
            'type': task_type,
            'priority': priority,
            'status': 'Backlog',
            'source': source,
            'description': description,
            'tags': tags or [],
        }
        
        if effort:
            task['effort'] = effort
        
        if due_date:
            task['due_date'] = due_date
        
        # Display task details
        print("Task Details:")
        print(f"  Title: {task['title']}")
        print(f"  Type: {task['type']}")
        print(f"  Priority: {task['priority']}")
        print(f"  Status: {task['status']}")
        print(f"  Source: {task['source']}")
        if task['description']:
            print(f"  Description: {task['description'][:100]}...")
        if task['tags']:
            print(f"  Tags: {', '.join(task['tags'])}")
        if effort:
            print(f"  Effort: {effort}")
        if due_date:
            print(f"  Due: {due_date}")
        print()
        
        # Push to Notion
        task_id = self.sync.push(task)
        
        if task_id:
            print(f"\n{'='*80}")
            print(f"✅ Task Created Successfully!")
            print(f"{'='*80}\n")
            print(f"Task ID: {task_id}")
            print(f"\nRun 'python3 notion_sync.py pull' to update local cache")
        
        return task_id
    
    def list_tasks(self, status: str = None, priority: str = None, 
                   task_type: str = None, owner: str = None) -> List[Dict]:
        """List tasks with optional filters"""
        
        # Load from cache
        if not self.cache_file.exists():
            print("❌ No cached tasks. Run 'python3 notion_sync.py pull' first")
            return []
        
        with open(self.cache_file) as f:
            data = json.load(f)
        
        tasks = data['tasks']
        
        # Apply filters
        if status:
            tasks = [t for t in tasks if t.get('status') == status]
        
        if priority:
            tasks = [t for t in tasks if t.get('priority') == priority]
        
        if task_type:
            tasks = [t for t in tasks if t.get('type') == task_type]
        
        if owner:
            tasks = [t for t in tasks if t.get('owner') == owner]
        
        # Display
        print(f"\n{'='*80}")
        print(f"Joju Tasks ({len(tasks)} found)")
        print(f"{'='*80}\n")
        
        if not tasks:
            print("No tasks found matching filters")
            return []
        
        # Group by status
        by_status = {}
        for task in tasks:
            status = task.get('status', 'Unknown')
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(task)
        
        # Display by status
        for status in ['Backlog', 'To Do', 'In Progress', 'In Review', 'Done']:
            if status in by_status:
                print(f"\n{'─'*80}")
                print(f"{status} ({len(by_status[status])})")
                print(f"{'─'*80}")
                
                for task in by_status[status]:
                    self._display_task_summary(task)
        
        return tasks
    
    def update(self, task_id: str, status: str = None, priority: str = None,
               owner: str = None, due_date: str = None) -> bool:
        """Update a task"""
        
        print(f"\n{'='*80}")
        print(f"Updating Task: {task_id}")
        print(f"{'='*80}\n")
        
        updates = {}
        
        if status:
            updates['status'] = status
            print(f"  Status → {status}")
        
        if priority:
            updates['priority'] = priority
            print(f"  Priority → {priority}")
        
        if owner:
            updates['owner'] = owner
            print(f"  Owner → {owner}")
        
        if due_date:
            updates['due_date'] = due_date
            print(f"  Due Date → {due_date}")
        
        if not updates:
            print("❌ No updates specified")
            return False
        
        print()
        
        # Update in Notion
        success = self.sync.update(task_id, updates)
        
        if success:
            print(f"\n✅ Task updated successfully")
            print(f"Run 'python3 notion_sync.py pull' to update local cache")
        
        return success
    
    def link_feedback(self, task_id: str, feedback_path: str):
        """Link a task to user feedback"""
        
        print(f"\n{'='*80}")
        print(f"Linking Task to Feedback")
        print(f"{'='*80}\n")
        
        print(f"Task ID: {task_id}")
        print(f"Feedback: {feedback_path}")
        
        # For now, add as a tag
        # Future: use Notion relations
        
        feedback_name = Path(feedback_path).stem
        
        updates = {
            'tags': [f"Feedback: {feedback_name}"]
        }
        
        success = self.sync.update(task_id, updates)
        
        if success:
            print(f"\n✅ Linked successfully")
        
        return success
    
    def _display_task_summary(self, task: Dict):
        """Display a single task summary"""
        priority_emoji = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        
        emoji = priority_emoji.get(task.get('priority'), '⚪')
        
        print(f"\n{emoji} {task['title']}")
        print(f"   Type: {task.get('type', 'Unknown')} | Priority: {task.get('priority', 'Unknown')}")
        
        if task.get('owner'):
            print(f"   Owner: {task['owner']}")
        
        if task.get('due_date'):
            print(f"   Due: {task['due_date']}")
        
        if task.get('tags'):
            print(f"   Tags: {', '.join(task['tags'])}")
        
        if task.get('url'):
            print(f"   URL: {task['url']}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Manage Joju tasks')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new task')
    create_parser.add_argument('--title', required=True, help='Task title')
    create_parser.add_argument('--type', default='Feature', 
                              choices=['Feature', 'Bug', 'Enhancement', 'Research', 'Documentation'],
                              help='Task type')
    create_parser.add_argument('--priority', default='Medium',
                              choices=['Critical', 'High', 'Medium', 'Low'],
                              help='Task priority')
    create_parser.add_argument('--source', default='Team Idea',
                              choices=['User Feedback', 'Team Idea', 'Bug Report', 'Survey', 'Competitive Analysis'],
                              help='Task source')
    create_parser.add_argument('--description', default='', help='Task description')
    create_parser.add_argument('--tags', nargs='*', help='Task tags')
    create_parser.add_argument('--effort', type=int, help='Effort estimate')
    create_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--priority', help='Filter by priority')
    list_parser.add_argument('--type', help='Filter by type')
    list_parser.add_argument('--owner', help='Filter by owner')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', help='Task ID to update')
    update_parser.add_argument('--status', help='New status')
    update_parser.add_argument('--priority', help='New priority')
    update_parser.add_argument('--owner', help='New owner')
    update_parser.add_argument('--due', help='New due date (YYYY-MM-DD)')
    
    # Link command
    link_parser = subparsers.add_parser('link', help='Link task to feedback')
    link_parser.add_argument('task_id', help='Task ID')
    link_parser.add_argument('--feedback', required=True, help='Path to feedback file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        manager = TaskManager()
        
        if args.command == 'create':
            manager.create(
                title=args.title,
                task_type=args.type,
                priority=args.priority,
                source=args.source,
                description=args.description,
                tags=args.tags,
                effort=args.effort,
                due_date=args.due
            )
        
        elif args.command == 'list':
            manager.list_tasks(
                status=args.status,
                priority=args.priority,
                task_type=args.type,
                owner=args.owner
            )
        
        elif args.command == 'update':
            manager.update(
                task_id=args.task_id,
                status=args.status,
                priority=args.priority,
                owner=args.owner,
                due_date=args.due
            )
        
        elif args.command == 'link':
            manager.link_feedback(
                task_id=args.task_id,
                feedback_path=args.feedback
            )
    
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\nSetup required:")
        print("1. Copy config.example.json to config.json")
        print("2. Add your Notion API key and database ID")
        print("3. See SETUP.md for detailed instructions")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
