"""
Task Tracker - Manages action items from meetings and emails
"""

import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TaskTracker:
    """Track and manage action items from all sources"""
    
    def __init__(self, tracker_file=None):
        if tracker_file is None:
            tracker_file = os.getenv(
                'TASK_TRACKER_PATH',
                'focuses/hcss/knowledge/task_tracker.json'
            )
        
        self.tracker_file = tracker_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                logger.info(f"Loaded {len(self.tasks)} tasks from tracker")
            except Exception as e:
                logger.error(f"Error loading tasks: {e}")
                self.tasks = []
        else:
            logger.info("No existing task tracker, starting fresh")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.tracker_file), exist_ok=True)
            
            data = {
                'tasks': self.tasks,
                'metadata': self.calculate_metadata()
            }
            
            with open(self.tracker_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.tasks)} tasks to tracker")
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
    
    def add_task(self, task: Dict) -> str:
        """Add new task to tracker"""
        # Generate ID if not provided
        if 'id' not in task:
            task['id'] = self._generate_task_id(task)
        
        # Set timestamps
        task['created_at'] = datetime.now().isoformat()
        task['updated_at'] = datetime.now().isoformat()
        
        # Set defaults
        task.setdefault('status', 'todo')
        task.setdefault('priority', 'medium')
        task.setdefault('overdue', False)
        
        # Check if task already exists
        existing = self.get_task(task['id'])
        if existing:
            logger.warning(f"Task {task['id']} already exists, updating instead")
            return self.update_task(task['id'], task)
        
        self.tasks.append(task)
        self.save_tasks()
        
        logger.info(f"Added task: {task['id']} - {task.get('what', 'No description')}")
        return task['id']
    
    def update_task(self, task_id: str, updates: Dict) -> str:
        """Update existing task"""
        task = self.get_task(task_id)
        
        if not task:
            logger.error(f"Task {task_id} not found")
            return None
        
        # Update fields
        task.update(updates)
        task['updated_at'] = datetime.now().isoformat()
        
        self.save_tasks()
        logger.info(f"Updated task: {task_id}")
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_tasks_by_owner(self, owner: str) -> List[Dict]:
        """Get all tasks for specific owner"""
        return [t for t in self.tasks if t.get('who') == owner]
    
    def get_tasks_by_status(self, status: str) -> List[Dict]:
        """Get all tasks with specific status"""
        return [t for t in self.tasks if t.get('status') == status]
    
    def get_overdue_tasks(self) -> List[Dict]:
        """Get all overdue tasks"""
        return [t for t in self.tasks if t.get('overdue', False)]
    
    def check_overdue(self):
        """Check all tasks for overdue status"""
        today = date.today()
        updated_count = 0
        
        for task in self.tasks:
            if task.get('status') == 'done':
                continue
            
            due_date_str = task.get('due')
            if not due_date_str:
                continue
            
            try:
                due_date = datetime.fromisoformat(due_date_str).date()
                
                if due_date < today:
                    if not task.get('overdue', False):
                        task['overdue'] = True
                        task['updated_at'] = datetime.now().isoformat()
                        updated_count += 1
                        logger.warning(f"Task {task['id']} is now overdue")
            except Exception as e:
                logger.error(f"Error parsing due date for task {task['id']}: {e}")
        
        if updated_count > 0:
            self.save_tasks()
            logger.info(f"Marked {updated_count} tasks as overdue")
    
    def flag_overdue(self, task_id: str):
        """Mark specific task as overdue"""
        return self.update_task(task_id, {'overdue': True})
    
    def complete_task(self, task_id: str):
        """Mark task as complete"""
        return self.update_task(task_id, {
            'status': 'done',
            'overdue': False,
            'completed_at': datetime.now().isoformat()
        })
    
    def get_state(self) -> Dict:
        """Get current tracker state"""
        return {
            'tasks': self.tasks,
            'metadata': self.calculate_metadata()
        }
    
    def calculate_metadata(self) -> Dict:
        """Calculate task statistics"""
        by_status = {}
        by_owner = {}
        by_priority = {}
        
        for task in self.tasks:
            # Count by status
            status = task.get('status', 'unknown')
            by_status[status] = by_status.get(status, 0) + 1
            
            # Count by owner
            owner = task.get('who', 'unassigned')
            by_owner[owner] = by_owner.get(owner, 0) + 1
            
            # Count by priority
            priority = task.get('priority', 'medium')
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            'last_updated': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'overdue_count': len(self.get_overdue_tasks()),
            'by_status': by_status,
            'by_owner': by_owner,
            'by_priority': by_priority
        }
    
    def _generate_task_id(self, task: Dict) -> str:
        """Generate unique task ID"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        source = task.get('source', 'unknown').upper()
        
        # Count existing tasks from same source today
        today_tasks = [t for t in self.tasks if t['id'].startswith(f"ACT-{date_str}-{source}")]
        count = len(today_tasks) + 1
        
        return f"ACT-{date_str}-{source}-{count:03d}"
    
    def group_by_owner(self) -> Dict[str, List[Dict]]:
        """Group tasks by owner"""
        grouped = {}
        
        for task in self.tasks:
            owner = task.get('who', 'unassigned')
            if owner not in grouped:
                grouped[owner] = []
            grouped[owner].append(task)
        
        return grouped
    
    def group_by_status(self) -> Dict[str, List[Dict]]:
        """Group tasks by status"""
        grouped = {}
        
        for task in self.tasks:
            status = task.get('status', 'unknown')
            if status not in grouped:
                grouped[status] = []
            grouped[status].append(task)
        
        return grouped
    
    def get_summary(self) -> Dict:
        """Get summary of task tracker"""
        metadata = self.calculate_metadata()
        
        return {
            'total_tasks': metadata['total_tasks'],
            'overdue': metadata['overdue_count'],
            'by_status': metadata['by_status'],
            'by_owner': metadata['by_owner'],
            'by_priority': metadata['by_priority'],
            'last_updated': metadata['last_updated']
        }


if __name__ == '__main__':
    # Test the tracker
    logging.basicConfig(level=logging.INFO)
    
    tracker = TaskTracker()
    
    # Add test task
    task_id = tracker.add_task({
        'what': 'Test task',
        'who': 'Justin',
        'due': '2025-11-15',
        'priority': 'high',
        'source': 'test'
    })
    
    print(f"Added task: {task_id}")
    print(f"Summary: {tracker.get_summary()}")
