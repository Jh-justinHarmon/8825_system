# MCP Server Visual Map
**Date:** 2025-11-13

---

## 🔴 THE PROBLEM IN ONE IMAGE

```
┌─────────────────────────────────────────────────────────────┐
│ RUNNING PROCESSES (Started Mon 11AM, still running)        │
├─────────────────────────────────────────────────────────────┤
│ PID 6520: /.../ windsurf-project - 8825 8825-system /...   │
│ PID 6528: /.../ windsurf-project - 8825 8825-system /...   │
│ PID 6534: /.../ windsurf-project - 8825 8825-system /...   │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ❌ PATH DOESN'T EXIST!
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ ACTUAL FILESYSTEM (After Nov 10 cleanup)                    │
├─────────────────────────────────────────────────────────────┤
│ ✅ 8825-system/  (renamed from "8825-system")              │
│ ✅ windsurf-project - 8825 8825-system/  (empty)           │
│ ❌ windsurf-project - 8825 8825-system/  (DELETED)         │
└─────────────────────────────────────────────────────────────┘
```

**Ghost processes running from deleted directory!**

---

## 📍 CURRENT STATE: 11 MCP Servers in 5 Locations

```
HOME (~)
└── mcp_servers/                           ← CENTRALIZED (4 servers)
    ├── 8825-core/server.py               ✅ Active
    ├── hcss-bridge/server.js             ✅ Active
    ├── figma-make-transformer/server.js  ✅ Active
    └── figjam/server.js                  ✅ Active

8825-system/
├── 8825_core/
│   ├── integrations/
│   │   ├── figjam/mcp-server/            ❌ DUPLICATE (old copy)
│   │   │   └── server.js
│   │   ├── goose/
│   │   │   ├── mcp-bridge/server.py      ⚠️  Bridge (keep?)
│   │   │   └── mcp-servers/
│   │   │       └── hcss-bridge/          ❌ DUPLICATE (old copy)
│   │   │           └── server.js
│   │   ├── mcp-servers/                  ← SCATTERED (2 servers)
│   │   │   ├── fds-mcp/server.py         🔄 Should move
│   │   │   └── meeting-automation-mcp/   🔄 Should move
│   │   │       └── server.py
│   │   └── mcp/mcp_template/             ✅ Template only
│   │       └── server.py
│   └── poc/infrastructure/
│       └── otter_integration/            🔄 Should move
│           └── server.py
├── focuses/
│   └── hcss/
│       ├── automation/
│       │   └── otter_mcp/                ❌ DUPLICATE #1
│       │       └── server.py
│       └── poc/tgif_automation/
│           └── otter_mcp/                ❌ DUPLICATE #2
│               └── server.py
└── mcp_servers/                          ← WRONG LOCATION
    └── ral_portal/server.py              🔄 Should move

8825_customers/
└── mcp_server/server.js                  🔄 Should move
```

**Legend:**
- ✅ Correct location
- ❌ Duplicate (delete)
- 🔄 Wrong location (move)
- ⚠️  Unclear (review)

---

## 🎯 TARGET STATE: 9 MCP Servers in 1 Location

```
HOME (~)
└── mcp_servers/                           ← ALL MCP SERVERS HERE
    ├── 8825-core/
    │   └── server.py
    ├── hcss-bridge/
    │   └── server.js
    ├── figma-make-transformer/
    │   └── server.js
    ├── figjam/
    │   └── server.js
    ├── otter-integration/                 ← Consolidated from 3 copies
    │   └── server.py
    ├── fds/                               ← Moved from 8825_core
    │   └── server.py
    ├── meeting-automation/                ← Moved from 8825_core
    │   └── server.py
    ├── ral-portal/                        ← Moved from 8825-system
    │   └── server.py
    └── customer-platform/                 ← Moved from 8825_customers
        └── server.js

8825-system/
├── 8825_core/
│   ├── integrations/
│   │   ├── goose/mcp-bridge/             ← Bridge only (not a server)
│   │   └── mcp/mcp_template/             ← Template only
│   └── system/
│       └── mcp_registry.json             ← Points to ~/mcp_servers/
└── focuses/
    ├── hcss/                              ← No mcp_server/ directory
    ├── joju/                              ← No mcp_server/ directory
    └── jh_assistant/                      ← No mcp_server/ directory
```

**Clean, consolidated, single source of truth!**

---

## 🔄 MIGRATION FLOW

```
BEFORE: 11 servers in 5 locations
    ↓
STEP 1: Consolidate scattered servers
    ├── Move otter_integration → ~/mcp_servers/otter-integration/
    ├── Move fds-mcp → ~/mcp_servers/fds/
    ├── Move meeting-automation-mcp → ~/mcp_servers/meeting-automation/
    ├── Move ral_portal → ~/mcp_servers/ral-portal/
    └── Move customer mcp_server → ~/mcp_servers/customer-platform/
    ↓
STEP 2: Remove duplicates
    ├── Delete 8825_core/integrations/figjam/mcp-server/
    ├── Delete 8825_core/integrations/goose/mcp-servers/hcss-bridge/
    ├── Delete focuses/hcss/automation/otter_mcp/
    ├── Delete focuses/hcss/poc/tgif_automation/otter_mcp/
    └── Delete 8825_core/integrations/mcp-servers/ (now empty)
    ↓
STEP 3: Update registry
    └── Edit mcp_registry.json → point to ~/mcp_servers/
    ↓
STEP 4: Restart processes
    ├── Kill ghost processes (8825-system paths)
    └── Let Windsurf restart with correct paths
    ↓
AFTER: 9 servers in 1 location
```

---

## 📊 DUPLICATION BREAKDOWN

### Otter Integration (3 copies!)
```
1. 8825_core/poc/infrastructure/otter_integration/  ← Keep this one
2. focuses/hcss/automation/otter_mcp/               ← Delete
3. focuses/hcss/poc/tgif_automation/otter_mcp/      ← Delete
```

### HCSS Bridge (2 copies)
```
1. ~/mcp_servers/hcss-bridge/                       ← Keep this one
2. 8825_core/integrations/goose/mcp-servers/        ← Delete
```

### FigJam (2 copies)
```
1. ~/mcp_servers/figjam/                            ← Keep this one
2. 8825_core/integrations/figjam/mcp-server/        ← Delete
```

**Total duplicates to remove: 5 files/directories**

---

## 🏗️ DIRECTORY STRUCTURE COMPARISON

### Current (Chaos)
```
5 different locations
11 MCP server files
5 duplicates
Registry out of sync
Ghost processes
```

### Proposed (Clean)
```
1 location (~/mcp_servers/)
9 unique MCP servers
0 duplicates
Registry accurate
Fresh processes
```

---

## ⚡ QUICK REFERENCE

### Where to find MCP servers NOW:
```bash
# Centralized (4)
ls ~/mcp_servers/

# Scattered in 8825_core (4)
find 8825-system/8825_core -name "server.py" -o -name "server.js"

# In focuses (2)
find 8825-system/focuses -name "server.py"

# Other (1)
ls 8825_customers/mcp_server/
```

### Where to find MCP servers AFTER migration:
```bash
# Everything in one place
ls ~/mcp_servers/
```

**That's it. One command. All servers.**

---

## 🎯 SUCCESS CRITERIA

Migration is complete when:

- [ ] `ls ~/mcp_servers/` shows 9 directories
- [ ] `find 8825-system -name "server.py" -o -name "server.js"` shows only template
- [ ] `ps aux | grep "8825-system"` returns nothing
- [ ] `ps aux | grep mcp_server` shows processes from ~/mcp_servers/
- [ ] `cat mcp_registry.json` points to ~/mcp_servers/
- [ ] Windsurf can access all MCP servers
- [ ] No duplicates anywhere

---

**Visual clarity on the chaos and the solution.**
