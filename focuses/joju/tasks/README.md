# Joju Task Layer

**Purpose:** Single source of truth for all Joju tasks, synced with Notion task board.

**Status:** Active  
**Created:** November 10, 2025

---

## ⚠️ CRITICAL SETUP REQUIREMENTS

**Before using this system, you MUST:**

1. **Install correct SDK version:**
   ```bash
   pip3 install notion-client==1.0.0
   ```
   ⚠️ **DO NOT use v2.7.0+** - it has breaking API changes!

2. **Configure credentials:**
   ```bash
   cp config.example.json config.json
   # Edit config.json with your Notion API key
   ```
   📍 **Credentials location:** If missing, check v2.0 workspace at `config/8825_config.json`

3. **Test connection:**
   ```bash
   python3 notion_sync.py test
   ```

**See [NOTION_SETUP_COMPLETE.md](NOTION_SETUP_COMPLETE.md) for complete troubleshooting guide.**

---

## 🎯 Overview

This is the **only** place in the 8825 system where the Notion Joju task board is accessible. All task management for Joju happens through this layer.

## 📁 Structure

```
tasks/
├── README.md              # This file
├── notion_sync.py         # Sync tasks with Notion
├── task_manager.py        # Local task management
├── config.json            # Notion board configuration
├── local/                 # Local task cache
│   └── tasks.json        # Cached tasks from Notion
└── templates/             # Task templates
    ├── feature.md
    ├── bug.md
    └── enhancement.md
```

---

## 🔗 Notion Integration

### **Notion Board:**
- **Name:** Joju Task Board
- **Type:** Database
- **Access:** Via this layer only

### **Properties:**
- Task Name (Title)
- Status (Select): Backlog / To Do / In Progress / In Review / Done
- Priority (Select): Critical / High / Medium / Low
- Type (Select): Feature / Bug / Enhancement / Research / Documentation
- Owner (Person)
- Due Date (Date)
- Effort (Number): Story points or hours
- Source (Select): User Feedback / Team Idea / Bug Report / Survey
- Related Feedback (Relation): Links to user engagement data
- Sprint (Select): Current sprint or backlog
- Tags (Multi-select)
- Description (Text)
- Created (Created Time)
- Last Updated (Last Edited Time)

---

## 🔄 Sync Workflow

### **Pull from Notion:**
```bash
python3 notion_sync.py pull
```
- Fetches all tasks from Notion
- Caches locally in `local/tasks.json`
- Updates task status

### **Push to Notion:**
```bash
python3 notion_sync.py push
```
- Creates new tasks in Notion
- Updates existing task properties
- Syncs status changes

### **Two-Way Sync:**
```bash
python3 notion_sync.py sync
```
- Pulls latest from Notion
- Pushes local changes
- Resolves conflicts (Notion wins)

---

## 📝 Task Management

### **Create New Task:**
```bash
python3 task_manager.py create --title "Task name" --type feature --priority high
```

### **List Tasks:**
```bash
python3 task_manager.py list --status "in progress"
python3 task_manager.py list --owner "Justin Harmon"
python3 task_manager.py list --priority critical
```

### **Update Task:**
```bash
python3 task_manager.py update TASK_ID --status done
python3 task_manager.py update TASK_ID --owner "Team Member"
```

### **Link to User Feedback:**
```bash
python3 task_manager.py link TASK_ID --feedback ../user_engagement/insights/INSIGHT_ID
```

---

## 🎨 Task Types

### **Feature**
New functionality or capability
- Template: `templates/feature.md`
- Requires: User story, acceptance criteria
- Links to: User feedback, survey data

### **Bug**
Something broken that needs fixing
- Template: `templates/bug.md`
- Requires: Steps to reproduce, expected vs actual
- Priority: Usually High or Critical

### **Enhancement**
Improvement to existing feature
- Template: `templates/enhancement.md`
- Requires: Current state, desired state
- Links to: User feedback

### **Research**
Investigation or exploration
- Requires: Research question, success criteria
- Output: Documentation or recommendation

### **Documentation**
Writing or updating docs
- Requires: Scope, audience
- Output: Published documentation

---

## 📊 Status Flow

```
Backlog → To Do → In Progress → In Review → Done
```

**Backlog:** Not yet prioritized or scheduled  
**To Do:** Ready to start, prioritized  
**In Progress:** Actively being worked on  
**In Review:** Complete, awaiting review/testing  
**Done:** Shipped and verified

---

## 🔗 Integration Points

### **User Engagement Layer**
- Tasks can be created from user feedback
- Link tasks to specific insights or quotes
- Track which feedback led to which features

### **Competitive Intelligence**
- Tasks for implementing features seen in competitors
- Reference AI feature analyses

### **Surveys**
- Auto-create tasks from high-priority survey results
- Link to survey data for context

---

## Important Notes

⚠️ **Pagination Required**: The Notion API returns a maximum of 100 results per page. Always use pagination when querying tasks. See `notion_sync.py` for implementation.

⚠️ **Status Property Type**: The Status field is a "status" type, not "select". Use `{'status': {'name': 'Released'}}` not `{'select': {'name': 'Released'}}`.

⚠️ **Completion Statuses**: Tasks are complete if status is "Released" OR "Archived". Both indicate completed work.

⚠️ **Total Tasks**: As of Nov 10, 2025, there are 238 total tasks (not 100). Always pull all pages.

---

## 🚀 Quick Start

### **1. Set Up Notion Integration**
```bash
# Add Notion API credentials
cp config.example.json config.json
# Edit config.json with your Notion API key and database ID
```

### **2. Initial Sync**
```bash
# Pull existing tasks from Notion
python3 notion_sync.py pull
```

### **3. Create Your First Task**
```bash
python3 task_manager.py create \
  --title "Implement context-aware AI" \
  --type feature \
  --priority high \
  --source "User Feedback" \
  --description "Based on Kayson's feedback about Teal"
```

### **4. Link to User Feedback**
```bash
python3 task_manager.py link TASK_ID \
  --feedback ../user_engagement/competitive_intelligence/ai_features/Kayson_Teal_Platform_Analysis.md
```

---

## 📋 Configuration

### **config.json Structure:**
```json
{
  "notion": {
    "api_key": "secret_xxx",
    "database_id": "xxx-xxx-xxx",
    "workspace": "Joju"
  },
  "sync": {
    "auto_sync": false,
    "sync_interval_minutes": 30,
    "conflict_resolution": "notion_wins"
  },
  "defaults": {
    "status": "Backlog",
    "priority": "Medium",
    "owner": "Unassigned"
  }
}
```

---

## 🔒 Access Control

**This layer is the ONLY place where:**
- Notion API credentials are stored
- Notion sync happens
- Tasks are created/updated

**Other layers can:**
- Read cached task data from `local/tasks.json`
- Request task creation (via this layer)
- Link to tasks (read-only)

**Other layers CANNOT:**
- Directly access Notion API
- Modify tasks without going through this layer
- Store Notion credentials

---

## 📈 Metrics

Track task metrics:
- Tasks created from user feedback
- Average time in each status
- Tasks completed per sprint
- Priority distribution
- Source breakdown (feedback vs team ideas)

---

## 🛠️ Development

### **Adding New Task Types:**
1. Create template in `templates/`
2. Add to `task_manager.py` type validation
3. Update Notion board Select options

### **Custom Workflows:**
Create workflow scripts in this directory:
- `create_from_feedback.py` - Auto-create from user engagement
- `sprint_planning.py` - Bulk task operations
- `report_generator.py` - Status reports

---

## 📝 Best Practices

### **Do:**
- ✅ Always sync before making changes
- ✅ Link tasks to user feedback when relevant
- ✅ Keep descriptions clear and actionable
- ✅ Update status regularly
- ✅ Use templates for consistency

### **Don't:**
- ❌ Bypass this layer to access Notion directly
- ❌ Store Notion credentials elsewhere
- ❌ Create duplicate tasks
- ❌ Leave tasks in "In Progress" indefinitely
- ❌ Forget to link to user feedback

---

## 🔄 Sync Schedule

**Manual:** Run sync commands as needed  
**Automated (future):** Cron job every 30 minutes  
**Real-time (future):** Webhook-based instant sync

---

## 📚 Related Documentation

- [User Engagement Layer](../user_engagement/README.md)
- [Competitive Intelligence](../user_engagement/competitive_intelligence/README.md)
- [Notion Integration Plan](../../8825_core/explorations/surveys/notion_integration_plan.md)

---

**Created:** November 10, 2025  
**Owner:** Product Team  
**Status:** ✅ Active
