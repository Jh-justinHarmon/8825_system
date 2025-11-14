# Quick Start - Managing Notion Tasks from 8825

## ⚠️ CRITICAL: Read This First!

**This system requires specific setup. Skipping these steps WILL cause errors.**

### Required SDK Version
```bash
pip3 install notion-client==1.0.0
```
⚠️ **DO NOT use v2.7.0+** - it has breaking API changes!

### Need Help?
- **Setup issues?** See [NOTION_SETUP_COMPLETE.md](NOTION_SETUP_COMPLETE.md)
- **Errors?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Quick check:** Run `./check_setup.sh`

---

## 🚀 One-Time Setup

### 1. Install Dependencies
```bash
pip3 install notion-client==1.0.0  # MUST be v1.0.0
```

### 2. Configure Notion
```bash
cd focuses/joju/tasks
cp config.example.json config.json
# Edit config.json with your Notion API key and database ID
```

**Need credentials?** Check v2.0 workspace: `8825-system (v2.0 deleted)/config/8825_config.json`

See [SETUP.md](SETUP.md) for detailed Notion setup instructions.

### 3. Test Connection
```bash
python3 notion_sync.py test
```

Should output: `✅ Connected to Notion successfully`

---

## 📖 Daily Usage

### **Pull Tasks from Notion**
```bash
python3 notion_sync.py pull
```
Downloads all tasks and caches them locally.

### **List All Tasks**
```bash
python3 task_manager.py list
```

### **List by Status**
```bash
python3 task_manager.py list --status "In Progress"
python3 task_manager.py list --status "To Do"
```

### **List by Priority**
```bash
python3 task_manager.py list --priority Critical
python3 task_manager.py list --priority High
```

### **Create a New Task**
```bash
python3 task_manager.py create \
  --title "Implement context-aware AI" \
  --type Feature \
  --priority High \
  --source "User Feedback" \
  --description "Based on Kayson's feedback about Teal platform"
```

### **Update Task Status**
```bash
python3 task_manager.py update TASK_ID --status "In Progress"
python3 task_manager.py update TASK_ID --status "Done"
```

### **Update Task Priority**
```bash
python3 task_manager.py update TASK_ID --priority Critical
```

### **Link Task to User Feedback**
```bash
python3 task_manager.py link TASK_ID \
  --feedback ../user_engagement/competitive_intelligence/ai_features/Kayson_Teal_Platform_Analysis.md
```

### **Check Sync Status**
```bash
python3 notion_sync.py status
```

---

## 🔄 Typical Workflow

### **Morning: Pull Latest Tasks**
```bash
cd focuses/joju/tasks
python3 notion_sync.py pull
python3 task_manager.py list --status "To Do"
```

### **During Day: Create Tasks from Feedback**
```bash
# After reviewing user feedback
python3 task_manager.py create \
  --title "Add workflow automation" \
  --type Feature \
  --priority High \
  --source "User Feedback" \
  --tags workflow automation
```

### **Update Progress**
```bash
# Started working on a task
python3 task_manager.py update TASK_ID --status "In Progress"

# Completed a task
python3 task_manager.py update TASK_ID --status "Done"
```

### **End of Day: Sync**
```bash
python3 notion_sync.py pull  # Get any changes from team
```

---

## 💡 Common Commands

### **See All In Progress Tasks**
```bash
python3 task_manager.py list --status "In Progress"
```

### **See All Critical Tasks**
```bash
python3 task_manager.py list --priority Critical
```

### **See All Bugs**
```bash
python3 task_manager.py list --type Bug
```

### **Create Bug Report**
```bash
python3 task_manager.py create \
  --title "Fix login error" \
  --type Bug \
  --priority Critical \
  --source "Bug Report"
```

### **Create Enhancement**
```bash
python3 task_manager.py create \
  --title "Improve dashboard performance" \
  --type Enhancement \
  --priority Medium
```

---

## 📊 Task Properties

### **Types:**
- Feature
- Bug
- Enhancement
- Research
- Documentation

### **Priorities:**
- Critical
- High
- Medium
- Low

### **Statuses:**
- Backlog
- To Do
- In Progress
- In Review
- Done

### **Sources:**
- User Feedback
- Team Idea
- Bug Report
- Survey
- Competitive Analysis

---

## 🔗 Integration with User Engagement

### **Create Task from User Feedback**
```bash
# 1. Review user engagement dashboard
# 2. Identify high-priority feedback
# 3. Create task

python3 task_manager.py create \
  --title "Implement feature from user feedback" \
  --type Feature \
  --priority High \
  --source "User Feedback" \
  --tags "user-requested"

# 4. Link to specific feedback
python3 task_manager.py link TASK_ID \
  --feedback ../user_engagement/insights/INSIGHT_FILE.md
```

---

## 🆘 Troubleshooting

### **"Config file not found"**
```bash
cp config.example.json config.json
# Then edit config.json with your credentials
```

### **"notion-client not installed"**
```bash
pip3 install notion-client
```

### **"No cached tasks"**
```bash
python3 notion_sync.py pull
```

### **"Connection failed"**
- Check API key in config.json
- Verify database ID is correct
- Ensure database is shared with integration

---

## 📝 Tips

- **Pull regularly** to stay synced with team
- **Use descriptive titles** for easy searching
- **Link to user feedback** when creating features
- **Update status** as you work
- **Use tags** for better organization
- **Set due dates** for time-sensitive tasks

---

## 🎯 Next Steps

1. Pull your first tasks: `python3 notion_sync.py pull`
2. List them: `python3 task_manager.py list`
3. Create a test task: `python3 task_manager.py create --title "Test task"`
4. Update it: `python3 task_manager.py update TASK_ID --status "Done"`

**You're ready to manage all Notion tasks from 8825!** 🎉
