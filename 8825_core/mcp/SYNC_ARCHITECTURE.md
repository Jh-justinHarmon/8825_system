# 8825 Sync & MCP Architecture

**Created:** 2025-11-08  
**Purpose:** Document the separation between sync infrastructure and MCP production services

---

## 🎯 Architecture Principles

### **1. Production MCP Services (Don't Touch Without Audit)**
- Core functionality for system operation
- Changes require dependency tracking
- Affects Goose integration
- Requires testing before modification

### **2. Sync Infrastructure (Configuration Layer)**
- Handles file movement between locations
- Safe to modify
- No impact on MCP core
- Supports production services

---

## 📊 Current Components

### **Production MCP Services:**

**1. `inbox_server.py`**
- Flask MCP server (localhost:8828)
- Receives from ChatGPT Custom GPT
- Writes to `~/Downloads/8825_inbox/pending/`
- **Dependencies:** None (standalone)
- **Status:** Production

**2. `universal_inbox_watch.py`**
- Monitors 3 inbox locations
- Validates JSON
- Moves to central pending
- **Dependencies:** Expects files in specific folders
- **Status:** Production
- **Watches:**
  - `~/Downloads/8825_inbox/`
  - `~/Library/.../Downloads/8825_inbox/`
  - `~/Dropbox/8825_inbox/`

### **Sync Infrastructure:**

**1. `downloads_sync.py` (v2.0)**
- Bidirectional sync: Desktop ⟷ iCloud Downloads
- Excludes "- old -" folders
- Real-time monitoring
- **Status:** Exists in v2.0, not migrated to v3.0

**2. Missing: Inbox-specific sync**
- Should sync 8825_inbox subfolders
- Should handle Dropbox sync
- Should route 8825 output files

---

## 🎯 Desired Architecture

### **Layer 1: File Arrival (Any Location)**
```
User saves file to:
- iCloud Downloads/
- Desktop Downloads/
- Dropbox/
- iCloud Downloads/8825_inbox/
- Desktop Downloads/8825_inbox/
- Dropbox/8825_inbox/
```

### **Layer 2: Sync Infrastructure (Configuration)**
```
downloads_sync.py (bidirectional)
    ↓
Desktop Downloads ⟷ iCloud Downloads (all contents)

inbox_sync.py (targeted)
    ↓
Desktop Downloads/8825_inbox ⟷ iCloud Downloads/8825_inbox ⟷ Dropbox/8825_inbox

output_sync.py (future)
    ↓
8825 output files → appropriate project folders in Downloads
```

### **Layer 3: MCP Production Services**
```
universal_inbox_watch.py
    ↓
Monitors 3 inbox locations
Validates & moves to central pending

inbox_server.py
    ↓
API endpoint for ChatGPT
Writes directly to central pending
```

### **Layer 4: Integration**
```
"fetch inbox" command
    ↓
Reads from central pending
Integrates into 8825 system
```

---

## 🔧 What Needs to Be Built

### **1. Migrate downloads_sync.py to v3.0**
- Copy from v2.0
- Update paths for v3.0 structure
- Keep bidirectional Desktop ⟷ iCloud sync

### **2. Create inbox_sync.py**
- Sync 8825_inbox subfolders specifically
- Handle Dropbox/8825_inbox ⟷ iCloud/Downloads/8825_inbox
- Handle Desktop/Downloads/8825_inbox ⟷ iCloud/Downloads/8825_inbox
- Exclude files already in central pending

### **3. Create output_sync.py (future)**
- Watch for 8825 output files
- Route to appropriate project folders
- Sync to both Downloads locations
- Rules TBD based on output protocols

### **4. Create unified startup script**
- Start all sync services
- Start MCP services
- Single command to run everything

---

## 📋 Dependencies to Track

### **universal_inbox_watch.py depends on:**
- Files being in 8825_inbox subfolders
- JSON format validation
- Central pending folder exists

### **inbox_sync.py will depend on:**
- downloads_sync.py running (for parent folder sync)
- 8825_inbox subfolders existing
- Dropbox installed and syncing

### **output_sync.py will depend on:**
- 8825 output protocols defined
- Project folder structure
- File naming conventions

---

## 🚨 Change Protocol

### **Before Modifying Production MCP:**
1. Check this document for dependencies
2. Test in isolation
3. Verify Goose integration still works
4. Update dependency list
5. Document changes

### **When Modifying Sync Infrastructure:**
1. Test file flow end-to-end
2. Verify no impact on MCP services
3. Update this document
4. No Goose testing needed

---

## 🎯 Implementation Plan

### **Phase 1: Migrate Existing (Now)**
1. Copy downloads_sync.py to v3.0
2. Update paths
3. Test bidirectional sync
4. Document

### **Phase 2: Build Inbox Sync (Next)**
1. Create inbox_sync.py
2. Handle 3-way sync (Desktop/iCloud/Dropbox)
3. Integrate with universal_inbox_watch
4. Test end-to-end

### **Phase 3: Unified Startup (After)**
1. Create start_all_services.sh
2. Start sync services
3. Start MCP services
4. Single command operation

### **Phase 4: Output Sync (Future)**
1. Define output protocols
2. Create output_sync.py
3. Integrate with project routing
4. Test workflows

---

## 📊 File Locations

### **v3.0 Structure:**
```
8825_core/
├── mcp/                          # Production MCP Services
│   ├── inbox_server.py          # ⚠️ Production
│   ├── universal_inbox_watch.py # ⚠️ Production
│   ├── start_inbox_server.sh
│   └── start_universal_watch.sh
│
└── sync/                         # Sync Infrastructure (NEW)
    ├── downloads_sync.py        # Desktop ⟷ iCloud (all)
    ├── inbox_sync.py            # 8825_inbox 3-way sync
    ├── output_sync.py           # 8825 output routing (future)
    ├── start_all_sync.sh        # Start all sync services
    └── SYNC_README.md           # Documentation
```

---

## ✅ Success Criteria

### **Sync Infrastructure:**
- Files saved anywhere end up in right place
- No manual file movement needed
- Bidirectional sync works
- No conflicts or loops

### **MCP Services:**
- Unchanged and working
- Dependencies documented
- Goose integration intact
- Easy to test in isolation

### **Overall:**
- Single command starts everything
- Clear separation of concerns
- Easy to debug
- Easy to extend

---

**Status:** Architecture defined, ready to implement  
**Next:** Migrate downloads_sync.py to v3.0
