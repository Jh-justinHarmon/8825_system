#!/usr/bin/env python3
"""
Notion Task Sync - Read and write tasks to/from Notion
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    from notion_client import Client
except ImportError:
    print("❌ notion-client not installed. Run: pip3 install notion-client")
    exit(1)


class NotionSync:
    """Sync tasks with Notion database"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / 'config.json'
        
        self.config_path = Path(config_path)
        self.local_dir = Path(__file__).parent / 'local'
        self.local_dir.mkdir(exist_ok=True)
        
        # Load configuration
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}\n"
                f"Copy config.example.json to config.json and add your credentials"
            )
        
        with open(self.config_path) as f:
            self.config = json.load(f)
        
        # Initialize Notion client
        api_key = self.config['notion']['api_key']
        if api_key == "secret_YOUR_NOTION_API_KEY_HERE":
            raise ValueError("Please configure your Notion API key in config.json")
        
        self.notion = Client(auth=api_key)
        self.database_id = self.config['notion']['database_id']
    
    def test_connection(self) -> bool:
        """Test connection to Notion"""
        try:
            # Try to retrieve the database
            self.notion.databases.retrieve(database_id=self.database_id)
            print("✅ Connected to Notion successfully")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def pull(self) -> List[Dict]:
        """Pull all tasks from Notion
        
        IMPORTANT: Notion API returns max 100 results per page.
        This method implements pagination to retrieve ALL tasks.
        
        As of Nov 10, 2025: 238 total tasks in database.
        """
        print(f"\n{'='*80}")
        print("Pulling tasks from Notion...")
        print(f"{'='*80}\n")
        
        try:
            # Query the database with pagination
            # CRITICAL: Must paginate to get all tasks (238 total, not just 100)
            tasks = []
            has_more = True
            start_cursor = None
            
            while has_more:
                query_params = {'database_id': self.database_id}
                if start_cursor:
                    query_params['start_cursor'] = start_cursor
                
                response = self.notion.databases.query(**query_params)
                
                for page in response['results']:
                    task = self._parse_notion_page(page)
                    tasks.append(task)
                
                has_more = response.get('has_more', False)
                start_cursor = response.get('next_cursor')
            
            # Save to local cache
            cache_file = self.local_dir / 'tasks.json'
            with open(cache_file, 'w') as f:
                json.dump({
                    'last_sync': datetime.now().isoformat(),
                    'task_count': len(tasks),
                    'tasks': tasks
                }, f, indent=2)
            
            print(f"✅ Pulled {len(tasks)} tasks from Notion")
            print(f"✅ Cached to: {cache_file}")
            
            # Display summary
            self._display_summary(tasks)
            
            return tasks
            
        except Exception as e:
            print(f"❌ Error pulling tasks: {e}")
            return []
    
    def push(self, task: Dict) -> Optional[str]:
        """Push a task to Notion"""
        print(f"Pushing task to Notion: {task.get('title', 'Untitled')}")
        
        try:
            # Create page properties
            properties = self._build_notion_properties(task)
            
            # Create the page
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            task_id = response['id']
            print(f"✅ Task created: {task_id}")
            
            return task_id
            
        except Exception as e:
            print(f"❌ Error pushing task: {e}")
            return None
    
    def update(self, task_id: str, updates: Dict) -> bool:
        """Update a task in Notion"""
        print(f"Updating task: {task_id}")
        
        try:
            # Build update properties
            properties = self._build_notion_properties(updates, is_update=True)
            
            # Update the page
            self.notion.pages.update(
                page_id=task_id,
                properties=properties
            )
            
            print(f"✅ Task updated")
            return True
            
        except Exception as e:
            print(f"❌ Error updating task: {e}")
            return False
    
    def sync(self):
        """Two-way sync (pull then push any local changes)"""
        print(f"\n{'='*80}")
        print("Syncing with Notion...")
        print(f"{'='*80}\n")
        
        # For now, just pull
        # Future: detect local changes and push them
        tasks = self.pull()
        
        print(f"\n{'='*80}")
        print("Sync complete!")
        print(f"{'='*80}\n")
    
    def _parse_notion_page(self, page: Dict) -> Dict:
        """Parse a Notion page into a task dict"""
        props = page['properties']
        
        task = {
            'id': page['id'],
            'title': self._get_title(props.get('Task name', props.get('Task Name', {}))),
            'status': self._get_select(props.get('Status', {})),
            'priority': self._get_select(props.get('Priority', {})),
            'type': self._get_select(props.get('Type', props.get('Task Category', {}))),
            'owner': self._get_person(props.get('Owner', props.get('Assignee', {}))),
            'due_date': self._get_date(props.get('Due Date', props.get('Due', {}))),
            'effort': self._get_number(props.get('Effort', props.get('Sprint Points', {}))),
            'source': self._get_select(props.get('Source', {})),
            'tags': self._get_multi_select(props.get('Tags', {})),
            'description': self._get_text(props.get('Description', {})),
            'created': page.get('created_time'),
            'updated': page.get('last_edited_time'),
            'url': page.get('url')
        }
        
        return task
    
    def _build_notion_properties(self, task: Dict, is_update: bool = False) -> Dict:
        """Build Notion properties from task dict"""
        properties = {}
        
        if 'title' in task:
            properties['Task Name'] = {
                'title': [{'text': {'content': task['title']}}]
            }
        
        if 'status' in task:
            # CRITICAL: Status is a "status" type, NOT "select" type
            # Use {'status': {'name': 'Released'}} not {'select': {'name': 'Released'}}
            # Valid values: Icebox, Backlog, Ready, In progress, Ready Review, 
            #               In review, In queue for release, Released, Archived
            properties['Status'] = {'status': {'name': task['status']}}
        
        if 'priority' in task:
            properties['Priority'] = {'select': {'name': task['priority']}}
        
        if 'type' in task:
            properties['Type'] = {'select': {'name': task['type']}}
        
        if 'owner' in task and task['owner']:
            # For now, skip owner (requires person ID)
            pass
        
        if 'due_date' in task and task['due_date']:
            properties['Due Date'] = {'date': {'start': task['due_date']}}
        
        if 'effort' in task:
            properties['Effort'] = {'number': task['effort']}
        
        if 'source' in task:
            properties['Source'] = {'select': {'name': task['source']}}
        
        if 'tags' in task and task['tags']:
            properties['Tags'] = {
                'multi_select': [{'name': tag} for tag in task['tags']]
            }
        
        if 'description' in task:
            properties['Description'] = {
                'rich_text': [{'text': {'content': task['description']}}]
            }
        
        return properties
    
    def _get_title(self, prop: Dict) -> str:
        """Extract title from Notion property"""
        if prop.get('title'):
            return ''.join([t['plain_text'] for t in prop['title']])
        return ''
    
    def _get_select(self, prop: Dict) -> Optional[str]:
        """Extract select value from Notion property"""
        if prop.get('select'):
            return prop['select']['name']
        # Handle status type (newer Notion API)
        if prop.get('status'):
            return prop['status']['name']
        return None
    
    def _get_multi_select(self, prop: Dict) -> List[str]:
        """Extract multi-select values from Notion property"""
        if prop.get('multi_select'):
            return [item['name'] for item in prop['multi_select']]
        return []
    
    def _get_person(self, prop: Dict) -> Optional[str]:
        """Extract person name from Notion property"""
        if prop.get('people') and len(prop['people']) > 0:
            return prop['people'][0].get('name', 'Unknown')
        return None
    
    def _get_date(self, prop: Dict) -> Optional[str]:
        """Extract date from Notion property"""
        if prop.get('date'):
            return prop['date']['start']
        return None
    
    def _get_number(self, prop: Dict) -> Optional[float]:
        """Extract number from Notion property"""
        return prop.get('number')
    
    def _get_text(self, prop: Dict) -> str:
        """Extract rich text from Notion property"""
        if prop.get('rich_text'):
            return ''.join([t['plain_text'] for t in prop['rich_text']])
        return ''
    
    def _display_summary(self, tasks: List[Dict]):
        """Display task summary"""
        print(f"\n{'─'*80}")
        print("Task Summary")
        print(f"{'─'*80}\n")
        
        # Count by status
        status_counts = {}
        for task in tasks:
            status = task.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("By Status:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")
        
        # Count by priority
        priority_counts = {}
        for task in tasks:
            priority = task.get('priority', 'Unknown')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        print("\nBy Priority:")
        for priority, count in sorted(priority_counts.items()):
            print(f"  {priority}: {count}")
        
        print()


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 notion_sync.py test      # Test connection")
        print("  python3 notion_sync.py pull      # Pull tasks from Notion")
        print("  python3 notion_sync.py sync      # Two-way sync")
        print("  python3 notion_sync.py status    # Show sync status")
        return
    
    command = sys.argv[1]
    
    try:
        sync = NotionSync()
        
        if command == 'test':
            sync.test_connection()
        
        elif command == 'pull':
            sync.pull()
        
        elif command == 'sync':
            sync.sync()
        
        elif command == 'status':
            cache_file = Path(__file__).parent / 'local' / 'tasks.json'
            if cache_file.exists():
                with open(cache_file) as f:
                    data = json.load(f)
                print(f"\nLast sync: {data['last_sync']}")
                print(f"Tasks cached: {data['task_count']}")
            else:
                print("\nNo cached tasks. Run 'pull' to sync.")
        
        else:
            print(f"Unknown command: {command}")
    
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\nSetup required:")
        print("1. Copy config.example.json to config.json")
        print("2. Add your Notion API key and database ID")
        print("3. See SETUP.md for detailed instructions")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
