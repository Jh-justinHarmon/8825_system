# 8825 System - API Reference

**Version:** 3.0  
**Last Updated:** November 10, 2025

---

## 📚 Table of Contents

1. [Task Management API](#task-management-api)
2. [User Engagement API](#user-engagement-api)
3. [MCP Bridge API](#mcp-bridge-api)
4. [Inbox Processing API](#inbox-processing-api)
5. [Workflow APIs](#workflow-apis)

---

## 🎯 Task Management API

**Location:** `focuses/joju/tasks/`

### NotionSync

```python
from notion_sync import NotionSync

sync = NotionSync(config_path='config.json')
```

#### Methods

##### `test_connection() -> bool`
Test connection to Notion.

```python
success = sync.test_connection()
# Returns: True if connected, False otherwise
```

##### `pull() -> List[Dict]`
Pull all tasks from Notion.

```python
tasks = sync.pull()
# Returns: List of task dictionaries
# Side effect: Caches to local/tasks.json
```

**Response:**
```python
[
    {
        'id': 'notion-page-id',
        'title': 'Task title',
        'status': 'In Progress',
        'priority': 'High',
        'type': 'Feature',
        'owner': 'Justin Harmon',
        'due_date': '2025-12-31',
        'effort': 5,
        'source': 'User Feedback',
        'tags': ['tag1', 'tag2'],
        'description': 'Task description',
        'created': '2025-11-10T10:00:00Z',
        'updated': '2025-11-10T15:00:00Z',
        'url': 'https://notion.so/...'
    }
]
```

##### `push(task: Dict) -> Optional[str]`
Push a task to Notion.

```python
task_id = sync.push({
    'title': 'New task',
    'type': 'Feature',
    'priority': 'High',
    'status': 'Backlog',
    'source': 'Team Idea',
    'description': 'Task description',
    'tags': ['tag1'],
    'effort': 3,
    'due_date': '2025-12-31'
})
# Returns: Notion page ID or None on failure
```

##### `update(task_id: str, updates: Dict) -> bool`
Update a task in Notion.

```python
success = sync.update('task-id', {
    'status': 'Done',
    'priority': 'Critical'
})
# Returns: True if successful, False otherwise
```

---

### TaskManager

```python
from task_manager import TaskManager

manager = TaskManager()
```

#### Methods

##### `create(...) -> Optional[str]`
Create a new task.

```python
task_id = manager.create(
    title='Task title',              # Required
    task_type='Feature',             # Default: 'Feature'
    priority='Medium',               # Default: 'Medium'
    source='Team Idea',              # Default: 'Team Idea'
    description='Description',       # Default: ''
    tags=['tag1', 'tag2'],          # Default: []
    effort=5,                        # Default: None
    due_date='2025-12-31'           # Default: None
)
```

**Parameters:**
- `title` (str, required): Task title
- `task_type` (str): Feature, Bug, Enhancement, Research, Documentation
- `priority` (str): Critical, High, Medium, Low
- `source` (str): User Feedback, Team Idea, Bug Report, Survey, Competitive Analysis
- `description` (str): Task description
- `tags` (List[str]): Tags
- `effort` (int): Effort estimate
- `due_date` (str): Due date (YYYY-MM-DD)

**Returns:** Notion page ID or None

##### `list_tasks(...) -> List[Dict]`
List tasks with filters.

```python
tasks = manager.list_tasks(
    status='In Progress',
    priority='High',
    task_type='Feature',
    owner='Justin Harmon'
)
```

**Parameters:** All optional
- `status` (str): Filter by status
- `priority` (str): Filter by priority
- `task_type` (str): Filter by type
- `owner` (str): Filter by owner

**Returns:** List of task dictionaries

##### `update(...) -> bool`
Update a task.

```python
success = manager.update(
    task_id='task-id',
    status='Done',
    priority='Critical',
    owner='Team Member',
    due_date='2025-12-31'
)
```

**Parameters:**
- `task_id` (str, required): Task ID
- `status` (str, optional): New status
- `priority` (str, optional): New priority
- `owner` (str, optional): New owner
- `due_date` (str, optional): New due date

**Returns:** True if successful

##### `link_feedback(task_id: str, feedback_path: str) -> bool`
Link task to user feedback.

```python
success = manager.link_feedback(
    task_id='task-id',
    feedback_path='../user_engagement/insights/insight.md'
)
```

---

## 👥 User Engagement API

**Location:** `focuses/joju/user_engagement/`

### Data Structure

```python
{
    'total_sessions': 5,
    'total_quotes': 91,
    'sessions': [
        {
            'participant': 'Kayson',
            'date': '2025-10-15',
            'duration': '60 minutes',
            'format': 'Remote'
        }
    ],
    'all_quotes': [
        {
            'quote': 'User feedback text',
            'participant': 'Kayson',
            'date': '2025-10-15',
            'type': 'workflow',
            'sentiment': 'positive'
        }
    ],
    'grouped_insights': [
        {
            'theme': 'Workflow',
            'mention_count': 19,
            'quotes': [...]
        }
    ]
}
```

### Functions

##### `query_user_feedback(theme=None, participant=None) -> Dict`
Query user feedback data.

```python
feedback = query_user_feedback(
    theme='workflow',
    participant='Kayson'
)
```

**Parameters:**
- `theme` (str, optional): Filter by theme
- `participant` (str, optional): Filter by participant

**Returns:**
```python
{
    'status': 'success',
    'total_sessions': 5,
    'total_quotes': 91,
    'filtered_count': 19,
    'quotes': [...]
}
```

##### `get_feedback_summary() -> Dict`
Get summary of all feedback.

```python
summary = get_feedback_summary()
```

**Returns:**
```python
{
    'status': 'success',
    'total_sessions': 5,
    'total_quotes': 91,
    'sessions': [...],
    'grouped_insights': [...]
}
```

##### `create_task_from_feedback(feedback_quote: str, priority='High') -> str`
Create task from feedback.

```python
task_id = create_task_from_feedback(
    feedback_quote='Users want better customization',
    priority='High'
)
```

---

## 🌉 MCP Bridge API

**Location:** `8825_core/integrations/goose/mcp-bridge/`

### HTTP Endpoints (Joju MCP Server)

**Base URL:** `http://localhost:8827`

#### Task Endpoints

##### `POST /tasks/list`
List tasks with filters.

**Request:**
```json
{
    "status": "In Progress",
    "priority": "High",
    "type": "Feature",
    "owner": "Justin Harmon"
}
```

**Response:**
```json
{
    "success": true,
    "count": 5,
    "tasks": [...]
}
```

##### `POST /tasks/create`
Create a new task.

**Request:**
```json
{
    "title": "Task title",
    "type": "Feature",
    "priority": "High",
    "source": "User Feedback",
    "description": "Description",
    "tags": ["tag1"],
    "effort": 5,
    "due_date": "2025-12-31"
}
```

**Response:**
```json
{
    "success": true,
    "task_id": "notion-page-id",
    "message": "Task created: Task title"
}
```

##### `POST /tasks/update/<task_id>`
Update a task.

**Request:**
```json
{
    "status": "Done",
    "priority": "Critical"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Task updated"
}
```

##### `POST /tasks/sync`
Sync tasks with Notion.

**Response:**
```json
{
    "success": true,
    "count": 25,
    "message": "Synced 25 tasks from Notion"
}
```

##### `POST /tasks/search`
Search tasks by text.

**Request:**
```json
{
    "query": "AI features"
}
```

**Response:**
```json
{
    "success": true,
    "query": "AI features",
    "count": 3,
    "tasks": [...]
}
```

##### `GET /tasks/summary`
Get task statistics.

**Response:**
```json
{
    "success": true,
    "total_tasks": 25,
    "last_sync": "2025-11-10T15:00:00Z",
    "by_status": {
        "Backlog": 5,
        "To Do": 3,
        "In Progress": 7,
        "In Review": 2,
        "Done": 8
    },
    "by_priority": {
        "Critical": 2,
        "High": 5,
        "Medium": 10,
        "Low": 8
    },
    "by_type": {
        "Feature": 15,
        "Bug": 5,
        "Enhancement": 3,
        "Research": 2
    }
}
```

---

### MCP Protocol (Goose Bridge)

**Transport:** stdio (JSON-RPC)

#### Request Format

```json
{
    "method": "tools/call",
    "params": {
        "name": "list_tasks",
        "arguments": {
            "status": "In Progress"
        }
    }
}
```

#### Response Format

```json
{
    "content": [
        {
            "type": "text",
            "text": "{\"status\": \"success\", \"tasks\": [...]}"
        }
    ]
}
```

#### Available Tools

1. **process_inbox** - Run inbox pipeline
2. **check_status** - System status
3. **review_tickets** - Teaching tickets
4. **ocr_screenshot** - OCR screenshot
5. **list_tasks** - List tasks
6. **create_task** - Create task
7. **update_task** - Update task
8. **sync_tasks** - Sync with Notion
9. **search_tasks** - Search tasks
10. **query_user_feedback** - Query feedback
11. **get_feedback_summary** - Feedback summary
12. **create_task_from_feedback** - Create from feedback

---

## 📥 Inbox Processing API

**Location:** `8825_core/inbox/`

### IngestionEngine

```python
from ingestion_engine import IngestionEngine

engine = IngestionEngine()
```

#### Methods

##### `process_file(file_path: Path) -> Dict`
Process a single file.

```python
result = engine.process_file(Path('/path/to/file.pdf'))
```

**Returns:**
```python
{
    'status': 'success',
    'file': 'file.pdf',
    'classification': 'document',
    'target_focus': 'joju',
    'processed_path': '/path/to/processed/file.pdf'
}
```

##### `classify_file(file_path: Path) -> Dict`
Classify a file.

```python
classification = engine.classify_file(Path('/path/to/file.pdf'))
```

**Returns:**
```python
{
    'type': 'document',
    'target_focus': 'joju',
    'confidence': 0.95,
    'keywords': ['joju', 'user testing']
}
```

---

## 🔄 Workflow APIs

### Meeting Summary Pipeline

**Location:** `8825_core/workflows/meeting_summary_pipeline.py`

```python
from meeting_summary_pipeline import MeetingSummaryPipeline

pipeline = MeetingSummaryPipeline()
```

#### Methods

##### `process_meeting(meeting_file: Path) -> Path`
Process a meeting JSON file.

```python
output_path = pipeline.process_meeting(
    Path('meetings/TGIF_2025-11-10.json')
)
# Returns: Path to generated Word document
```

##### `scan_for_meetings(start_date, end_date) -> List[Path]`
Scan for meeting files in date range.

```python
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=14)

meeting_files = pipeline.scan_for_meetings(start_date, end_date)
```

---

### User Testing Analysis

**Location:** `8825_core/workflows/analyze_user_testing.py`

```python
from analyze_user_testing import analyze_session

results = analyze_session(
    session_file='sessions/kayson_session.json'
)
```

**Returns:**
```python
{
    'participant': 'Kayson',
    'insights': [...],
    'pain_points': [...],
    'positive_feedback': [...],
    'themes': ['workflow', 'AI', 'customization']
}
```

---

## 🔐 Authentication

### Notion API

```python
# In config.json
{
    "notion": {
        "api_key": "secret_YOUR_KEY",
        "database_id": "YOUR_DATABASE_ID"
    }
}

# Usage
from notion_client import Client
client = Client(auth=api_key)
```

### Google APIs

```python
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/drive']
)
```

---

## ⚠️ Error Handling

### Standard Error Response

```python
{
    'status': 'error',
    'error': 'Error message',
    'code': 'ERROR_CODE',
    'details': {...}
}
```

### Common Error Codes

- `NOTION_CONNECTION_ERROR` - Can't connect to Notion
- `TASK_NOT_FOUND` - Task ID doesn't exist
- `INVALID_PARAMETERS` - Invalid parameters
- `PERMISSION_DENIED` - Insufficient permissions
- `RATE_LIMIT_EXCEEDED` - API rate limit hit

### Retry Logic

```python
from time import sleep

def with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            sleep(2 ** attempt)  # Exponential backoff
```

---

## 📊 Rate Limits

### Notion API
- **Rate Limit:** 3 requests per second
- **Handling:** Automatic retry with backoff

### Google APIs
- **Rate Limit:** Varies by service
- **Handling:** Check quotas in console

---

## 🔍 Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View API Calls

```python
# In notion_sync.py
logger.debug(f"API call: {method} {endpoint}")
logger.debug(f"Response: {response}")
```

---

## 📚 Examples

### Complete Task Workflow

```python
from task_manager import TaskManager
from notion_sync import NotionSync

# Initialize
manager = TaskManager()
sync = NotionSync()

# Sync latest tasks
tasks = sync.pull()
print(f"Synced {len(tasks)} tasks")

# Create new task
task_id = manager.create(
    title="Implement AI features",
    task_type="Feature",
    priority="High",
    source="User Feedback",
    description="Based on Kayson feedback",
    tags=["AI", "user-feedback"]
)
print(f"Created task: {task_id}")

# Update task
manager.update(task_id, status="In Progress")
print("Task updated")

# Search tasks
results = manager.list_tasks(priority="High")
print(f"Found {len(results)} high priority tasks")
```

### User Feedback to Task

```python
# Query feedback
feedback = query_user_feedback(theme="workflow")
print(f"Found {feedback['filtered_count']} workflow quotes")

# Get top quote
top_quote = feedback['quotes'][0]

# Create task
task_id = create_task_from_feedback(
    feedback_quote=top_quote['quote'],
    priority="High"
)
print(f"Created task from feedback: {task_id}")
```

---

**Version:** 3.0  
**Last Updated:** November 10, 2025  
**For Questions:** See DEVELOPER_GUIDE.md
