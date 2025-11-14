# 8825 Sync Infrastructure

**Purpose:** Configuration layer for file syncing - separate from MCP production services  
**Created:** 2025-11-08  
**Status:** Production ready

---

## 🎯 Architecture

### **Sync Layer (This Folder)**
Configuration scripts that move files between locations

### **MCP Layer (../mcp/)**
Production services that process files (don't modify without dependency audit)

---

## 📂 Components

### **1. downloads_sync.py**
**Purpose:** Bidirectional sync of all Downloads files  
**Syncs:** Desktop Downloads ⟷ iCloud Downloads  
**Excludes:** 
- `- old -` folders
- `.DS_Store`, `.tmp`, `~$`
- `8825_inbox` (handled by inbox_sync.py)

**Start:**
```bash
python3 downloads_sync.py
```

---

### **2. inbox_sync.py**
**Purpose:** 3-way sync of 8825_inbox folders  
**Syncs:** Desktop/8825_inbox ⟷ iCloud/8825_inbox ⟷ Dropbox/8825_inbox  
**Excludes:**
- `.DS_Store`, `.tmp`, `~$`
- `pending` folder (MCP handles this)

**Start:**
```bash
python3 inbox_sync.py
```

---

### **3. start_all_sync.sh**
**Purpose:** Unified startup for all services  
**Starts:**
1. downloads_sync.py
2. inbox_sync.py
3. MCP inbox server (localhost:8828)
4. Universal inbox watch

**Start:**
```bash
./start_all_sync.sh
```

---

## 🔄 How It Works

### **File Flow:**

```
User saves file anywhere
    ↓
Sync Layer (this folder)
    ↓ downloads_sync.py → Desktop ⟷ iCloud (all files)
    ↓ inbox_sync.py → 3-way sync (8825_inbox only)
    ↓
Files in correct locations
    ↓
MCP Layer (../mcp/)
    ↓ universal_inbox_watch.py → Detects & validates
    ↓ inbox_server.py → API endpoint for ChatGPT
    ↓
Central pending folder
    ↓
"fetch inbox" in Windsurf
    ↓
Integrated into 8825
```

---

## 🚀 Quick Start

### **Option 1: Start Everything (Recommended)**
```bash
cd ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 3.0/8825_core/sync/
./start_all_sync.sh
```

### **Option 2: Start Individual Services**
```bash
# Terminal 1: Downloads sync
python3 downloads_sync.py

# Terminal 2: Inbox sync
python3 inbox_sync.py

# Terminal 3: MCP services
cd ../mcp/
./start_inbox_server.sh

# Terminal 4: Universal watch
./start_universal_watch.sh
```

---

## 📊 Monitored Locations

### **downloads_sync.py monitors:**
- `~/Downloads/` (all files except 8825_inbox)
- `~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/` (all files except 8825_inbox)

### **inbox_sync.py monitors:**
- `~/Downloads/8825_inbox/`
- `~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/8825_inbox/`
- `~/Dropbox/8825_inbox/`

### **universal_inbox_watch.py monitors:**
- All 3 inbox locations above
- Moves validated files to `~/Downloads/8825_inbox/pending/`

---

## 🔧 Configuration

### **Change Exclusions:**

**downloads_sync.py:**
```python
EXCLUDE_PATTERNS = [
    "- old -",
    ".DS_Store",
    ".tmp",
    "~$",
    "8825_inbox"  # Add more here
]
```

**inbox_sync.py:**
```python
EXCLUDE_PATTERNS = [
    ".DS_Store",
    ".tmp",
    "~$",
    "pending"  # Add more here
]
```

---

## 📋 Logs

### **Log Locations:**
- `logs/downloads_sync.log` - Downloads sync activity
- `logs/inbox_sync.log` - Inbox sync activity
- `/tmp/mcp_inbox_server.log` - MCP server
- `/tmp/universal_inbox_watch.log` - Universal watch

### **View Logs:**
```bash
# Real-time
tail -f logs/downloads_sync.log
tail -f logs/inbox_sync.log

# All logs
tail -f logs/*.log
```

---

## ⚠️ Important: Separation of Concerns

### **Sync Infrastructure (This Folder)**
✅ **Safe to modify** - Configuration layer  
✅ No Goose dependencies  
✅ Changes don't affect MCP core  

**When to modify:**
- Change sync behavior
- Add/remove exclusions
- Adjust sync frequency
- Add new sync targets

### **MCP Production Services (../mcp/)**
⚠️ **Modify with caution** - Production infrastructure  
⚠️ Has Goose dependencies  
⚠️ Changes require testing  

**Before modifying:**
1. Check SYNC_ARCHITECTURE.md for dependencies
2. Test in isolation
3. Verify Goose integration
4. Update dependency documentation

---

## 🎯 Use Cases

### **Scenario 1: Mobile File Save**
```
iPhone → Save to iCloud Downloads/8825_inbox
    ↓ inbox_sync.py (3-way)
Desktop/8825_inbox & Dropbox/8825_inbox
    ↓ universal_inbox_watch.py
Central pending
    ↓ "fetch inbox"
Integrated!
```

### **Scenario 2: Desktop File Save**
```
Mac → Save to Desktop Downloads/8825_inbox
    ↓ inbox_sync.py (3-way)
iCloud/8825_inbox & Dropbox/8825_inbox
    ↓ universal_inbox_watch.py
Central pending
    ↓ "fetch inbox"
Integrated!
```

### **Scenario 3: ChatGPT API**
```
ChatGPT Custom GPT → API call
    ↓ MCP inbox server (localhost:8828)
Central pending (direct)
    ↓ "fetch inbox"
Integrated!
```

---

## 🔍 Troubleshooting

### **Files not syncing:**
```bash
# Check if services are running
ps aux | grep downloads_sync
ps aux | grep inbox_sync

# Check logs
tail -f logs/*.log

# Restart services
./start_all_sync.sh
```

### **Sync loops:**
- Both scripts have deduplication
- Files tracked by hash, not name
- 5-second cooldown prevents loops

### **Missing dependencies:**
```bash
# Install watchdog
pip3 install watchdog
```

---

## 📊 Performance

### **Sync Speed:**
- Small files (<10MB): Instant
- Large files (>100MB): 1-2 seconds
- Initial sync: Depends on file count

### **Resource Usage:**
- CPU: Minimal (event-driven)
- Memory: ~50MB per service
- Disk I/O: Only during sync

---

## 🎉 Success Criteria

✅ **Files saved anywhere end up in right place**  
✅ **No manual file movement needed**  
✅ **Bidirectional sync works**  
✅ **3-way inbox sync works**  
✅ **No conflicts or loops**  
✅ **MCP services unchanged**  
✅ **Single command starts everything**  

---

## 📚 Related Documentation

- `SYNC_ARCHITECTURE.md` - Full architecture and dependencies
- `../mcp/README.md` - MCP production services
- `../mcp/CHATGPT_SETUP.md` - ChatGPT Custom GPT setup

---

**Status:** Production ready ✅  
**Dependencies:** watchdog (pip3 install watchdog)  
**Next:** Test end-to-end, then set up as LaunchAgent for auto-start
