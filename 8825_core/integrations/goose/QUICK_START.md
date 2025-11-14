# Goose MCP Bridge - Quick Start Guide

**Get up and running in 5 minutes!**

---

## 🚀 For End Users

### Step 1: Install Goose (1 minute)
```bash
pip install goose-ai
```

### Step 2: Start Goose (30 seconds)
```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
goose session start
```

### Step 3: Try It! (30 seconds)
```
> "List available tools"
> "Show me all tasks"
> "Get user feedback summary"
```

**Done!** See [USER_GUIDE.md](USER_GUIDE.md) for more.

---

## 🔧 For Admins

### Step 1: Run Setup (2 minutes)
```bash
cd 8825_core/integrations/goose
./SETUP_GOOSE.sh
```

### Step 2: Configure Notion (2 minutes)
```bash
cd focuses/joju/tasks
cp config.example.json config.json
# Edit config.json with Notion API key and database ID
python3 notion_sync.py test
```

### Step 3: Initial Sync (1 minute)
```bash
python3 notion_sync.py pull
```

**Done!** See [ADMIN_GUIDE.md](ADMIN_GUIDE.md) for more.

---

## 💬 First Commands to Try

### Task Management
```
"Show me all tasks in progress"
"Create a test task"
"Search for tasks about AI"
```

### User Feedback
```
"Get user feedback summary"
"What did users say about workflow?"
"Show me all user testing data"
```

### System
```
"Check 8825 status"
"List available tools"
```

---

## 📚 Full Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide
- **[ADMIN_GUIDE.md](ADMIN_GUIDE.md)** - Admin guide
- **[PRODUCTION_READY.md](PRODUCTION_READY.md)** - Technical details
- **[INDEX.md](INDEX.md)** - All documentation

---

## 🆘 Need Help?

**Can't see tools?**
```bash
./SETUP_GOOSE.sh
```

**Task management not working?**
```bash
cd focuses/joju/tasks
python3 notion_sync.py test
```

**Still stuck?**
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review logs: `mcp-bridge/logs/`
- Ask your admin

---

**Version:** 2.0.0  
**Ready to go!** 🎉
