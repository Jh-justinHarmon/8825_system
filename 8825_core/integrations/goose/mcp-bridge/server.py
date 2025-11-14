#!/usr/bin/env python3
"""
8825 MCP Bridge for Goose - Production Ready
Exposes 8825 system tools via MCP protocol

Version: 2.0.0 (Production)
Created: November 10, 2025
"""

import sys
import os
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add paths for imports
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / 'focuses' / 'joju' / 'tasks'))

# Import task management
try:
    from notion_sync import NotionSync
    from task_manager import TaskManager
    TASKS_AVAILABLE = True
except ImportError:
    TASKS_AVAILABLE = False
    logging.warning("Task management not available")

# Setup logging
LOG_DIR = Path(__file__).parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'mcp_bridge_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('8825-mcp-bridge')

# Configuration
CONFIG = {
    'workspace_root': WORKSPACE_ROOT,
    'inbox_hub': WORKSPACE_ROOT / 'INBOX_HUB',
    'core_inbox': WORKSPACE_ROOT / '8825_core' / 'inbox',
    'joju_tasks': WORKSPACE_ROOT / 'focuses' / 'joju' / 'tasks',
    'joju_engagement': WORKSPACE_ROOT / 'focuses' / 'joju' / 'user_engagement',
    'allowed_users': ['justin_harmon', 'matthew_galley', 'cam_watkins'],
    'max_retries': 3,
    'timeout': 300,  # 5 minutes
}


class MCPBridge:
    """MCP Bridge for 8825 System"""
    
    def __init__(self):
        self.task_manager = None
        self.notion_sync = None
        
        if TASKS_AVAILABLE:
            try:
                self.task_manager = TaskManager()
                self.notion_sync = NotionSync()
                logger.info("Task management initialized")
            except Exception as e:
                logger.error(f"Failed to initialize task management: {e}")
    
    def execute_with_retry(self, func, *args, max_retries=3, **kwargs):
        """Execute function with retry logic"""
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise
                logger.warning(f"Attempt {attempt + 1} failed, retrying: {e}")
        
    def run_command(self, cmd: List[str], cwd: Path = None, timeout: int = 300) -> Dict[str, Any]:
        """Run shell command with error handling"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or CONFIG['workspace_root'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s: {' '.join(cmd)}")
            return {
                'success': False,
                'error': f'Command timed out after {timeout}s'
            }
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    # ========================================================================
    # CORE 8825 TOOLS
    # ========================================================================
    
    def process_inbox(self) -> Dict[str, Any]:
        """Process the 8825 inbox pipeline"""
        logger.info("Processing inbox")
        
        script = CONFIG['inbox_hub'] / 'simple_sync_and_process.sh'
        result = self.run_command(['bash', str(script)], cwd=CONFIG['inbox_hub'])
        
        if result['success']:
            return {
                'status': 'success',
                'message': 'Inbox processing complete',
                'output': result['stdout']
            }
        else:
            return {
                'status': 'error',
                'message': 'Inbox processing failed',
                'error': result.get('stderr', result.get('error'))
            }
    
    def check_status(self) -> Dict[str, Any]:
        """Check 8825 system status"""
        logger.info("Checking system status")
        
        script = CONFIG['core_inbox'] / 'ingestion_engine.py'
        result = self.run_command(
            ['python3', str(script), 'stats'],
            cwd=CONFIG['core_inbox']
        )
        
        return {
            'status': 'success' if result['success'] else 'error',
            'output': result['stdout'],
            'error': result.get('stderr')
        }
    
    def review_tickets(self, limit: int = 10) -> Dict[str, Any]:
        """List teaching tickets"""
        logger.info(f"Reviewing tickets (limit: {limit})")
        
        script = CONFIG['core_inbox'] / 'ingestion_engine.py'
        result = self.run_command(
            ['python3', str(script), 'tickets', 'list'],
            cwd=CONFIG['core_inbox']
        )
        
        if result['success']:
            lines = result['stdout'].strip().split('\n')[:limit]
            return {
                'status': 'success',
                'count': len(lines),
                'tickets': lines
            }
        else:
            return {
                'status': 'error',
                'error': result.get('stderr', result.get('error'))
            }
    
    def ocr_screenshot(self) -> Dict[str, Any]:
        """OCR the latest screenshot"""
        logger.info("OCR'ing latest screenshot")
        
        script = CONFIG['inbox_hub'] / 'ocr_latest_screenshot.sh'
        result = self.run_command(['bash', str(script)], cwd=CONFIG['inbox_hub'])
        
        return {
            'status': 'success' if result['success'] else 'error',
            'message': 'Screenshot prepared at /tmp/latest_screenshot.png',
            'output': result['stdout']
        }
    
    # ========================================================================
    # TASK MANAGEMENT TOOLS
    # ========================================================================
    
    def list_tasks(self, status: str = None, priority: str = None, 
                   task_type: str = None, owner: str = None) -> Dict[str, Any]:
        """List Joju tasks with filters"""
        if not self.task_manager:
            return {'status': 'error', 'error': 'Task management not available'}
        
        logger.info(f"Listing tasks (status={status}, priority={priority})")
        
        try:
            tasks = self.task_manager.list_tasks(
                status=status,
                priority=priority,
                task_type=task_type,
                owner=owner
            )
            
            return {
                'status': 'success',
                'count': len(tasks),
                'tasks': tasks
            }
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def create_task(self, title: str, task_type: str = 'Feature',
                   priority: str = 'Medium', source: str = 'Team Idea',
                   description: str = '', tags: List[str] = None,
                   effort: int = None, due_date: str = None) -> Dict[str, Any]:
        """Create a new Joju task"""
        if not self.task_manager:
            return {'status': 'error', 'error': 'Task management not available'}
        
        logger.info(f"Creating task: {title}")
        
        try:
            task_id = self.task_manager.create(
                title=title,
                task_type=task_type,
                priority=priority,
                source=source,
                description=description,
                tags=tags or [],
                effort=effort,
                due_date=due_date
            )
            
            return {
                'status': 'success',
                'task_id': task_id,
                'message': f'Task created: {title}'
            }
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def update_task(self, task_id: str, status: str = None,
                   priority: str = None, owner: str = None,
                   due_date: str = None) -> Dict[str, Any]:
        """Update a Joju task"""
        if not self.task_manager:
            return {'status': 'error', 'error': 'Task management not available'}
        
        logger.info(f"Updating task: {task_id}")
        
        try:
            success = self.task_manager.update(
                task_id=task_id,
                status=status,
                priority=priority,
                owner=owner,
                due_date=due_date
            )
            
            return {
                'status': 'success' if success else 'error',
                'message': 'Task updated' if success else 'Update failed'
            }
        except Exception as e:
            logger.error(f"Failed to update task: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def sync_tasks(self) -> Dict[str, Any]:
        """Sync tasks with Notion"""
        if not self.notion_sync:
            return {'status': 'error', 'error': 'Task sync not available'}
        
        logger.info("Syncing tasks with Notion")
        
        try:
            tasks = self.notion_sync.pull()
            return {
                'status': 'success',
                'count': len(tasks),
                'message': f'Synced {len(tasks)} tasks from Notion'
            }
        except Exception as e:
            logger.error(f"Failed to sync tasks: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def search_tasks(self, query: str) -> Dict[str, Any]:
        """Search tasks by text"""
        if not self.task_manager:
            return {'status': 'error', 'error': 'Task management not available'}
        
        logger.info(f"Searching tasks: {query}")
        
        try:
            cache_file = CONFIG['joju_tasks'] / 'local' / 'tasks.json'
            
            if not cache_file.exists():
                return {'status': 'error', 'error': 'No cached tasks. Run sync first.'}
            
            with open(cache_file) as f:
                data = json.load(f)
            
            query_lower = query.lower()
            matching = []
            
            for task in data['tasks']:
                if (query_lower in task.get('title', '').lower() or
                    query_lower in task.get('description', '').lower() or
                    any(query_lower in tag.lower() for tag in task.get('tags', []))):
                    matching.append(task)
            
            return {
                'status': 'success',
                'query': query,
                'count': len(matching),
                'tasks': matching
            }
        except Exception as e:
            logger.error(f"Failed to search tasks: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    # ========================================================================
    # USER ENGAGEMENT TOOLS
    # ========================================================================
    
    def query_user_feedback(self, theme: str = None, participant: str = None) -> Dict[str, Any]:
        """Query user engagement data"""
        logger.info(f"Querying user feedback (theme={theme}, participant={participant})")
        
        try:
            data_file = CONFIG['joju_engagement'] / 'all_user_testing_data.json'
            
            if not data_file.exists():
                return {'status': 'error', 'error': 'No user feedback data found'}
            
            with open(data_file) as f:
                data = json.load(f)
            
            quotes = data['all_quotes']
            
            # Apply filters
            if theme:
                quotes = [q for q in quotes if q.get('type') == theme.lower()]
            
            if participant:
                quotes = [q for q in quotes if q.get('participant', '').lower() == participant.lower()]
            
            return {
                'status': 'success',
                'total_sessions': data['total_sessions'],
                'total_quotes': data['total_quotes'],
                'filtered_count': len(quotes),
                'quotes': quotes[:20]  # Limit to 20 for readability
            }
        except Exception as e:
            logger.error(f"Failed to query feedback: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get summary of user engagement data"""
        logger.info("Getting feedback summary")
        
        try:
            data_file = CONFIG['joju_engagement'] / 'all_user_testing_data.json'
            
            if not data_file.exists():
                return {'status': 'error', 'error': 'No user feedback data found'}
            
            with open(data_file) as f:
                data = json.load(f)
            
            return {
                'status': 'success',
                'total_sessions': data['total_sessions'],
                'total_quotes': data['total_quotes'],
                'sessions': data['sessions'],
                'grouped_insights': data.get('grouped_insights', [])
            }
        except Exception as e:
            logger.error(f"Failed to get summary: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def create_task_from_feedback(self, feedback_quote: str, priority: str = 'High') -> Dict[str, Any]:
        """Create task from user feedback"""
        if not self.task_manager:
            return {'status': 'error', 'error': 'Task management not available'}
        
        logger.info("Creating task from feedback")
        
        try:
            # Extract title from quote (first 50 chars)
            title = feedback_quote[:50] + ('...' if len(feedback_quote) > 50 else '')
            
            task_id = self.task_manager.create(
                title=title,
                task_type='Feature',
                priority=priority,
                source='User Feedback',
                description=feedback_quote,
                tags=['user-feedback']
            )
            
            return {
                'status': 'success',
                'task_id': task_id,
                'message': f'Task created from feedback'
            }
        except Exception as e:
            logger.error(f"Failed to create task from feedback: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    # ========================================================================
    # MCP PROTOCOL
    # ========================================================================
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request"""
        method = request.get('method')
        params = request.get('params', {})
        
        logger.info(f"Handling request: {method}")
        
        try:
            if method == 'tools/list':
                return self.list_tools()
            
            elif method == 'tools/call':
                tool_name = params.get('name')
                args = params.get('arguments', {})
                return self.call_tool(tool_name, args)
            
            else:
                return {
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {method}'
                    }
                }
        except Exception as e:
            logger.error(f"Request handling error: {e}")
            return {
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }
    
    def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        tools = [
            # Core 8825 tools
            {
                'name': 'process_inbox',
                'description': 'Process the 8825 inbox pipeline',
                'inputSchema': {'type': 'object', 'properties': {}}
            },
            {
                'name': 'check_status',
                'description': 'Check 8825 system status',
                'inputSchema': {'type': 'object', 'properties': {}}
            },
            {
                'name': 'review_tickets',
                'description': 'List teaching tickets',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'limit': {'type': 'number', 'default': 10}
                    }
                }
            },
            {
                'name': 'ocr_screenshot',
                'description': 'OCR the latest screenshot',
                'inputSchema': {'type': 'object', 'properties': {}}
            },
        ]
        
        # Add task management tools if available
        if TASKS_AVAILABLE:
            tools.extend([
                {
                    'name': 'list_tasks',
                    'description': 'List Joju tasks with optional filters',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'},
                            'priority': {'type': 'string'},
                            'type': {'type': 'string'},
                            'owner': {'type': 'string'}
                        }
                    }
                },
                {
                    'name': 'create_task',
                    'description': 'Create a new Joju task',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'title': {'type': 'string'},
                            'type': {'type': 'string', 'default': 'Feature'},
                            'priority': {'type': 'string', 'default': 'Medium'},
                            'source': {'type': 'string', 'default': 'Team Idea'},
                            'description': {'type': 'string'},
                            'tags': {'type': 'array'},
                            'effort': {'type': 'number'},
                            'due_date': {'type': 'string'}
                        },
                        'required': ['title']
                    }
                },
                {
                    'name': 'update_task',
                    'description': 'Update a Joju task',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'task_id': {'type': 'string'},
                            'status': {'type': 'string'},
                            'priority': {'type': 'string'},
                            'owner': {'type': 'string'},
                            'due_date': {'type': 'string'}
                        },
                        'required': ['task_id']
                    }
                },
                {
                    'name': 'sync_tasks',
                    'description': 'Sync tasks with Notion',
                    'inputSchema': {'type': 'object', 'properties': {}}
                },
                {
                    'name': 'search_tasks',
                    'description': 'Search tasks by text query',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'query': {'type': 'string'}
                        },
                        'required': ['query']
                    }
                },
                {
                    'name': 'query_user_feedback',
                    'description': 'Query user engagement data',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'theme': {'type': 'string'},
                            'participant': {'type': 'string'}
                        }
                    }
                },
                {
                    'name': 'get_feedback_summary',
                    'description': 'Get summary of user feedback',
                    'inputSchema': {'type': 'object', 'properties': {}}
                },
                {
                    'name': 'create_task_from_feedback',
                    'description': 'Create task from user feedback quote',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'feedback_quote': {'type': 'string'},
                            'priority': {'type': 'string', 'default': 'High'}
                        },
                        'required': ['feedback_quote']
                    }
                }
            ])
        
        return {'tools': tools}
    
    def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool"""
        logger.info(f"Calling tool: {tool_name}")
        
        # Core tools
        if tool_name == 'process_inbox':
            result = self.process_inbox()
        elif tool_name == 'check_status':
            result = self.check_status()
        elif tool_name == 'review_tickets':
            result = self.review_tickets(args.get('limit', 10))
        elif tool_name == 'ocr_screenshot':
            result = self.ocr_screenshot()
        
        # Task management tools
        elif tool_name == 'list_tasks':
            result = self.list_tasks(**args)
        elif tool_name == 'create_task':
            result = self.create_task(**args)
        elif tool_name == 'update_task':
            result = self.update_task(**args)
        elif tool_name == 'sync_tasks':
            result = self.sync_tasks()
        elif tool_name == 'search_tasks':
            result = self.search_tasks(args['query'])
        
        # User engagement tools
        elif tool_name == 'query_user_feedback':
            result = self.query_user_feedback(**args)
        elif tool_name == 'get_feedback_summary':
            result = self.get_feedback_summary()
        elif tool_name == 'create_task_from_feedback':
            result = self.create_task_from_feedback(**args)
        
        else:
            return {
                'error': {
                    'code': -32602,
                    'message': f'Unknown tool: {tool_name}'
                }
            }
        
        return {
            'content': [
                {
                    'type': 'text',
                    'text': json.dumps(result, indent=2)
                }
            ]
        }


def main():
    """Main entry point"""
    logger.info("Starting 8825 MCP Bridge v2.0")
    
    bridge = MCPBridge()
    
    # Read from stdin, write to stdout (MCP protocol)
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = bridge.handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            error_response = {
                'error': {
                    'code': -32700,
                    'message': 'Parse error'
                }
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            error_response = {
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == '__main__':
    main()
