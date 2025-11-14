# 8825 System - Developer Guide

**Version:** 3.0  
**Last Updated:** November 10, 2025  
**For:** Developers working on 8825 system

---

## 🏗️ System Architecture

### High-Level Overview

```
8825 System v3.0
│
├── 8825_core/                  # Shared core system
│   ├── agents/                 # AI agents and tools
│   ├── integrations/           # External service integrations
│   ├── inbox/                  # Inbox processing pipeline
│   ├── workflows/              # Automated workflows
│   ├── protocols/              # System protocols
│   └── projects/               # Project configurations
│
├── focuses/                    # Focus-specific workspaces
│   ├── joju/                   # Joju product focus
│   ├── hcss/                   # HCSS client focus
│   └── [symlinks to users/]
│
├── users/                      # User-specific data
│   └── justin_harmon/
│       ├── joju/               # User's Joju data
│       ├── hcss/               # User's HCSS data
│       └── jh_assistant/       # Personal assistant
│
├── INBOX_HUB/                  # Inbox automation
│   └── simple_sync_and_process.sh
│
└── Documents/                  # Generated outputs
    ├── HCSS/                   # HCSS meeting summaries
    └── roadmap/                # Roadmaps and plans
```

---

## 🎯 Core Concepts

### 1. Focuses
**What:** Isolated workspaces for different projects/clients  
**Why:** Clean separation, independent evolution  
**How:** Symlinks from `focuses/` to `users/[user]/[focus]/`

**Example:**
```bash
focuses/joju -> users/justin_harmon/joju
```

### 2. MCP Servers
**What:** Model Context Protocol servers for AI tool access  
**Why:** Expose 8825 tools to AI assistants (Goose, Claude, etc.)  
**How:** Each focus can have its own MCP server

**Ports:**
- HCSS MCP: 8826
- Joju MCP: 8827
- JH Assistant: 8828

### 3. Inbox Pipeline
**What:** Automated file processing system  
**Why:** Process screenshots, documents, uploads automatically  
**How:** LaunchAgent runs hourly, processes files through Lane A/B

### 4. Workflows
**What:** Automated multi-step processes  
**Why:** Reduce manual work, ensure consistency  
**How:** Python scripts in `8825_core/workflows/`

---

## 🔧 Development Setup

### Prerequisites

```bash
# Python 3.7+
python3 --version

# Required packages
pip install -r requirements.txt

# Optional: Goose
pip install goose-ai
```

### ⚠️ Notion Integration (Joju Tasks)

**CRITICAL:** Notion integration requires specific SDK version:

```bash
# MUST use v1.0.0 (v2.7.0+ has breaking changes)
pip3 install notion-client==1.0.0
```

**Setup:**
1. Copy credentials from v2.0: `config/8825_config.json`
2. Create `focuses/joju/tasks/config.json`
3. Test: `python3 notion_sync.py test`

**See:** `focuses/joju/tasks/NOTION_SETUP_COMPLETE.md` for full details.

### Environment Setup

```bash
# Clone/navigate to workspace
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

# Set up Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify structure
ls -la 8825_core/
ls -la focuses/
```

---

## 📂 Directory Structure

### 8825_core/

```
8825_core/
├── agents/                     # AI agents
│   ├── agent_registry.json     # Agent definitions
│   └── AGENT_INDEX.md          # Agent documentation
│
├── integrations/               # External services
│   ├── google/                 # Google Drive, Gmail, Calendar
│   ├── notion/                 # Notion API (via focuses)
│   ├── figjam/                 # FigJam sticky notes
│   ├── dropbox/                # Dropbox API
│   ├── goose/                  # Goose MCP bridge
│   └── mcp/                    # MCP server framework
│
├── inbox/                      # Inbox processing
│   ├── ingestion_engine.py     # Main processor
│   ├── classifier.py           # File classification
│   └── config/                 # Classification rules
│
├── workflows/                  # Automated workflows
│   ├── meeting_summary_pipeline.py    # HCSS meetings
│   ├── analyze_user_testing.py        # User testing
│   └── extract_all_tasks.py           # Task extraction
│
├── protocols/                  # System protocols
│   ├── PARTNER_CREDIT_README.md
│   └── WORK_ORDER_TEMPLATE.md
│
└── projects/                   # Project configs
    ├── 8825_00-general.json
    ├── 8825_76-joju.json
    └── 8825_00-hcss.json
```

### focuses/

```
focuses/
├── joju/                       # Joju product focus
│   ├── tasks/                  # Task management (Notion)
│   │   ├── notion_sync.py      # Sync with Notion
│   │   ├── task_manager.py     # Task operations
│   │   └── config.json         # Notion credentials
│   │
│   ├── user_engagement/        # User feedback
│   │   ├── sessions/           # Testing sessions
│   │   ├── insights/           # Extracted insights
│   │   └── dashboard.html      # Feedback dashboard
│   │
│   └── mcp_server/             # Joju MCP server
│       ├── server.py           # Flask server
│       ├── task_tools.py       # Task management tools
│       └── config.json         # Server config
│
├── hcss/                       # HCSS client focus
│   ├── workflows/              # HCSS workflows
│   ├── automation/             # Automation scripts
│   └── projects/               # Project data
│
└── [user]/jh_assistant/        # Personal assistant
    └── poc/                    # Proof of concepts
```

---

## 🔌 Key Integrations

### 1. Notion (Task Management)

**Location:** `focuses/joju/tasks/`

**Setup:**
```bash
cd focuses/joju/tasks
cp config.example.json config.json
# Edit config.json with API key and database ID
python3 notion_sync.py test
```

**Usage:**
```python
from notion_sync import NotionSync
from task_manager import TaskManager

sync = NotionSync()
tasks = sync.pull()  # Get all tasks

manager = TaskManager()
task_id = manager.create(
    title="New task",
    priority="High"
)
```

**API Docs:** [Notion API](https://developers.notion.com/)

### 2. Google Services

**Location:** `8825_core/integrations/google/`

**Services:**
- Drive API (file storage)
- Gmail API (email processing)
- Calendar API (event management)
- Vision API (OCR)

**Setup:**
```bash
# Credentials in service account JSON
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

**Usage:**
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    'credentials.json'
)
drive_service = build('drive', 'v3', credentials=credentials)
```

### 3. Goose MCP Bridge

**Location:** `8825_core/integrations/goose/mcp-bridge/`

**Architecture:**
```
Goose → MCP Bridge → Task Layer → Notion API
                  → User Engagement Data
                  → 8825 Core Scripts
```

**Adding New Tools:**
```python
# In server.py

def my_new_tool(self, param: str) -> Dict[str, Any]:
    """Tool description"""
    logger.info(f"Running tool: {param}")
    
    try:
        result = do_something(param)
        return {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        logger.error(f"Tool failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }

# Register in list_tools()
# Add to call_tool()
```

---

## 🛠️ Common Development Tasks

### Adding a New Focus

```bash
# 1. Create user directory
mkdir -p users/justin_harmon/new_focus

# 2. Create symlink
ln -s ../users/justin_harmon/new_focus focuses/new_focus

# 3. Create structure
mkdir -p focuses/new_focus/{workflows,data,config}

# 4. Add to project config
# Edit 8825_core/projects/8825_00-general.json
```

### Creating a New Workflow

```python
#!/usr/bin/env python3
"""
New Workflow - Description
"""

import sys
from pathlib import Path

# Add to path
WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

def main():
    """Main workflow logic"""
    print("Starting workflow...")
    
    # Your logic here
    
    print("Workflow complete!")

if __name__ == "__main__":
    main()
```

### Adding a New Integration

```bash
# 1. Create integration directory
mkdir -p 8825_core/integrations/new_service

# 2. Create main module
touch 8825_core/integrations/new_service/__init__.py
touch 8825_core/integrations/new_service/client.py

# 3. Add configuration
touch 8825_core/integrations/new_service/config.json

# 4. Add documentation
touch 8825_core/integrations/new_service/README.md
```

### Creating an MCP Tool

```python
# In focuses/[focus]/mcp_server/server.py

@app.route('/tools/my_tool', methods=['POST'])
def my_tool():
    """
    My new tool
    
    Request body:
    {
        "param1": "value",
        "param2": 123
    }
    """
    data = request.get_json()
    
    try:
        result = process_tool(data)
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
```

---

## 🧪 Testing

### Unit Tests

```python
# tests/test_workflow.py

import unittest
from workflows.my_workflow import MyWorkflow

class TestMyWorkflow(unittest.TestCase):
    
    def setUp(self):
        self.workflow = MyWorkflow()
    
    def test_process(self):
        result = self.workflow.process("test input")
        self.assertEqual(result['status'], 'success')
    
    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.workflow.process(None)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```bash
# Test Notion integration
cd focuses/joju/tasks
python3 notion_sync.py test

# Test MCP bridge
cd 8825_core/integrations/goose/mcp-bridge
echo '{"method":"tools/list"}' | python3 server.py

# Test workflow
cd 8825_core/workflows
python3 meeting_summary_pipeline.py --test
```

### Manual Testing

```bash
# Test inbox processing
cd INBOX_HUB
./simple_sync_and_process.sh

# Test task creation
cd focuses/joju/tasks
python3 task_manager.py create --title "Test task"

# Test user engagement query
cd focuses/joju/user_engagement
python3 -c "import json; print(json.load(open('all_user_testing_data.json'))['total_quotes'])"
```

---

## 📊 Logging & Debugging

### Log Locations

```
8825_core/integrations/goose/mcp-bridge/logs/    # MCP bridge logs
8825_core/inbox/logs/                            # Inbox processing
focuses/joju/tasks/local/                        # Task cache
INBOX_HUB/logs/                                  # Inbox automation
```

### Viewing Logs

```bash
# Real-time MCP logs
tail -f 8825_core/integrations/goose/mcp-bridge/logs/mcp_bridge_*.log

# Search for errors
grep "ERROR" 8825_core/integrations/goose/mcp-bridge/logs/*.log

# View task sync history
cat focuses/joju/tasks/local/tasks.json | python3 -m json.tool
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in scripts
logger.setLevel(logging.DEBUG)
```

---

## 🔐 Security Best Practices

### Credentials Management

```bash
# Never commit credentials
# Use .gitignore

# Store in config files
focuses/joju/tasks/config.json          # Notion API
8825_core/integrations/google/creds.json # Google

# Use environment variables
export NOTION_API_KEY="secret_xxx"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/creds.json"
```

### API Keys

```python
# Load from config
import json
with open('config.json') as f:
    config = json.load(f)
    api_key = config['api_key']

# Or from environment
import os
api_key = os.getenv('API_KEY')

# Never hardcode
# ❌ api_key = "secret_abc123"
```

### Access Control

```python
# Check user permissions
ALLOWED_USERS = ['justin_harmon', 'matthew_galley', 'cam_watkins']

def check_access(user_id: str) -> bool:
    return user_id in ALLOWED_USERS

# Log access attempts
logger.info(f"Access attempt by {user_id}")
```

---

## 🚀 Deployment

### Production Checklist

- [ ] All tests passing
- [ ] Credentials configured
- [ ] Logs directory exists
- [ ] Permissions set correctly
- [ ] Documentation updated
- [ ] Error handling tested
- [ ] Performance validated

### Starting Services

**MCP Servers:**
```bash
# Start all MCP servers (recommended)
./start_all_mcps.sh

# Or start individual servers
cd ~/mcp_servers/figma-make-transformer
./start_mcp.sh

# Verify running
curl http://localhost:8827/health
ps aux | grep mcp
```

**MCP Servers Auto-Start:**
- HCSS MCP (port 8826)
- Joju MCP (port 8827)
- JH Assistant MCP (port 8828)

**LaunchAgent:** Configured to auto-start on login  
**See:** [STARTUP_AUTOMATION.md](STARTUP_AUTOMATION.md) for details

### Monitoring

```bash
# Check service status
ps aux | grep "mcp"

# Check logs for errors
grep "ERROR" */logs/*.log

# Monitor performance
tail -f 8825_core/integrations/goose/mcp-bridge/logs/mcp_bridge_*.log | grep "seconds"
```

---

## 📚 Code Style

### Python Style Guide

```python
# Follow PEP 8
# Use type hints
def process_data(input: str, count: int = 10) -> Dict[str, Any]:
    """
    Process data with given parameters.
    
    Args:
        input: Input string to process
        count: Number of items to return
    
    Returns:
        Dictionary with processed results
    """
    pass

# Use descriptive names
# ✅ user_engagement_data
# ❌ ued

# Document classes
class TaskManager:
    """
    Manages Joju tasks and Notion integration.
    
    Attributes:
        sync: NotionSync instance
        cache_file: Path to local cache
    """
    pass
```

### File Organization

```python
# Standard structure
#!/usr/bin/env python3
"""
Module description
"""

# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import requests
from notion_client import Client

# Local imports
from .utils import helper_function

# Constants
CONFIG_FILE = Path(__file__).parent / 'config.json'

# Classes and functions
class MyClass:
    pass

def main():
    pass

if __name__ == "__main__":
    main()
```

---

## 🔄 Git Workflow

### Branch Strategy

```bash
# Main branch: production-ready
main

# Development branch
dev

# Feature branches
feature/task-management
feature/user-engagement
fix/notion-sync-bug
```

### Commit Messages

```bash
# Format: <type>: <description>

# Types:
feat: Add new feature
fix: Bug fix
docs: Documentation
refactor: Code refactoring
test: Add tests
chore: Maintenance

# Examples:
git commit -m "feat: Add task search functionality"
git commit -m "fix: Handle Notion API timeout"
git commit -m "docs: Update developer guide"
```

---

## 📖 API Documentation

### Task Management API

```python
# List tasks
tasks = task_manager.list_tasks(
    status="In Progress",
    priority="High"
)

# Create task
task_id = task_manager.create(
    title="Task title",
    task_type="Feature",
    priority="High",
    description="Description"
)

# Update task
task_manager.update(
    task_id="abc123",
    status="Done"
)

# Search tasks
results = task_manager.search_tasks("AI features")
```

### User Engagement API

```python
# Get summary
summary = get_feedback_summary()
# Returns: {total_sessions, total_quotes, themes}

# Query feedback
feedback = query_user_feedback(
    theme="workflow",
    participant="Kayson"
)

# Create task from feedback
task_id = create_task_from_feedback(
    feedback_quote="Users want better customization",
    priority="High"
)
```

---

## 🆘 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Permission Errors:**
```bash
chmod +x script.py
chmod +x INBOX_HUB/*.sh
```

**Notion Connection:**
```bash
cd focuses/joju/tasks
python3 notion_sync.py test
# Check API key and database ID
```

**MCP Bridge Not Responding:**
```bash
# Check if running
ps aux | grep server.py

# Check logs
tail -f mcp-bridge/logs/*.log

# Restart
killall python3
python3 mcp-bridge/server.py
```

---

## 📞 Getting Help

### Documentation
- This guide (system-wide)
- Focus-specific READMEs
- Integration-specific docs
- MCP bridge guides

### Code Examples
- `8825_core/workflows/` - Workflow examples
- `focuses/joju/tasks/` - Task management
- `8825_core/integrations/` - Integration examples

### Team Resources
- Team wiki
- Slack channels
- Code reviews

---

## 🎯 Next Steps

### For New Developers
1. Read this guide
2. Set up development environment
3. Run existing workflows
4. Make a small change
5. Submit for review

### For Contributing
1. Create feature branch
2. Write tests
3. Update documentation
4. Submit pull request
5. Address review feedback

---

**Version:** 3.0  
**Last Updated:** November 10, 2025  
**Maintained By:** 8825 Development Team
