# 8825 Registry & Startup System

**Created:** 2025-11-10  
**Updated:** 2025-11-13 (Agent Reclassification)  
**Status:** Phase 2 Complete  
**Version:** 2.0

---

## What This Is

**Unified registry system for all 8825 capabilities: agents, pipelines, workflows, protocols, scripts, and system components.**

One command = full confidence system is ready.

---

## 🆕 Agent Reclassification (2025-11-13)

**New Registries Added:**
- `agents.json` - 6 true agents (make autonomous decisions)
- `pipelines.json` - 4 pipelines (automated sequences)
- `workflows.json` - 8 workflows (manual processes)
- `protocols_registry.json` - 2 protocols (methodologies)

**See:** `RECLASSIFICATION_SUMMARY.md` for full details

---

## Quick Start

### **Every Morning:**
```bash
8825 start
```

### **Before Any Work:**
```bash
8825 start
```

### **After Pulling Changes:**
```bash
8825 start
```

---

## Commands

### **`8825 start`**
Full startup protocol:
1. Registry validation (auto-detects new scripts)
2. Dependency checking (auto-installs if missing)
3. Health checks (validates system state)
4. System ready confirmation

### **`8825 health`**
Health check only:
- Daemon status
- Downloads folder size
- BRAIN_TRANSPORT presence
- Junk file detection

### **`8825 deps`**
Dependency check only:
- Verifies all required dependencies
- Auto-installs missing ones

### **`8825 registry`**
Registry validation only:
- Scans for new scripts
- Reports registry status

### **`8825 audit`** ✨ NEW
Inspect system components:

#### **`8825 audit path <path>`**
Shows everything that touches a specific path:
- All scripts and daemons
- Exclusion patterns
- Conflict detection
- Risk assessment

Example: `8825 audit path ~/Downloads`

#### **`8825 audit component <name>`**
Deep dive on a specific component:
- Purpose and location
- What it touches
- Dependencies
- How to control it
- Safety assessment

Example: `8825 audit component downloads_sync`

#### **`8825 audit dependency <dep>`**
Shows what requires a dependency:
- Installation status
- Required by which components
- Impact if removed/updated
- Recommendations

Example: `8825 audit dependency watchdog`

#### **`8825 audit conflicts`**
Finds system conflicts:
- Duplicate implementations
- Exclusion pattern conflicts
- Overlapping touchpoints
- Orphaned processes

Example: `8825 audit conflicts`

---

## What It Checks

### **1. Registry Validation**
- Scans filesystem for all scripts (.sh, .py)
- Compares to registered components
- Reports new scripts found
- (Future: Auto-registers new scripts)

### **2. Dependencies**
Checks and installs if missing:
- `python3` (3.9+)
- `watchdog` (Python package)
- `jq` (JSON processor)
- `rsync` (file sync)
- `bash` (shell)

### **3. Health Status**
- **Daemons:** Are they running when they should be?
- **Downloads:** Size < 100MB? (junk accumulation check)
- **BRAIN_TRANSPORT:** Present in both locations?
- **Junk Files:** Any old/, sticky_*, brainstorm files?

### **4. System Ready**
- Green light if all checks pass
- Warnings if attention needed
- Clear next steps

---

## The Registry

**Location:** `8825_core/registry/SYSTEM_REGISTRY.json`

**Contains:**
- All daemons (what they do, dependencies, status)
- All scripts (paths, dependencies, what they touch)
- Critical paths (who touches them)
- System dependencies (what's required)
- Health status (last check results)
- Change history (what was modified and why)

**Updated:**
- Manually when major changes made
- Auto-scanned on every startup
- (Future: Auto-registered on detection)

---

## The Tether

**Registry ↔ Startup ↔ Health ↔ Dependencies**

Everything is connected:
- Startup reads registry for dependencies
- Health checks write status to registry
- Registry tracks all components
- Dependencies ensure system ready

**Result:** No more "I didn't know that was running"

---

## Example Output

```bash
$ 8825 start

╔════════════════════════════════════════╗
║     8825 UNIFIED STARTUP PROTOCOL     ║
╚════════════════════════════════════════╝

[1/4] Registry Validation
  ✅ Registry last updated: 2025-11-10T06:15:00Z
  ⚠️  Found 109 new scripts (will be registered in future)
  Registry contains:
    • 7 scripts
    • 2 daemons
    • 3 critical paths

[2/4] Dependency Check
  ✅ bash
  ✅ jq
  ✅ python3
  ✅ rsync
  ✅ watchdog
  ✅ All dependencies satisfied (5/5)

[3/4] Health Check
  ✅ downloads_sync: stopped (expected)
  ✅ inbox_sync: stopped (expected)
  ✅ Local Downloads: 22MB (healthy)
  ✅ iCloud Downloads: 22MB (healthy)
  ✅ BRAIN_TRANSPORT: Present in both locations
  ✅ No junk files detected
  ✅ Overall Status: HEALTHY

[4/4] System Status

╔════════════════════════════════════════╗
║          ✅ SYSTEM READY ✅           ║
╚════════════════════════════════════════╝
```

---

## Files

- `SYSTEM_REGISTRY.json` - Central registry
- `8825.sh` - Command wrapper (symlinked to /usr/local/bin/8825)
- `8825_start.sh` - Main startup orchestrator
- `check_health.sh` - Health checks
- `check_dependencies.sh` - Dependency verification
- `validate_registry.sh` - Registry validation

---

## Why This Exists

**The Problem:**
- System sprawl (109+ scripts)
- Hidden daemons running for days
- Duplicate implementations
- No way to know "what will break if I change X"
- 12-cycle cleanup loops

**The Solution:**
- One command validates everything
- Registry tracks all components
- Health checks catch problems early
- Dependencies auto-install
- Full confidence before work

---

## Phase 2 Complete ✅

### **Session 1: Audit Tools** - DELIVERED
- ✅ `8825 audit path <path>` - Show what touches a path
- ✅ `8825 audit component <name>` - Show component details
- ✅ `8825 audit dependency <dep>` - Show dependency usage
- ✅ `8825 audit conflicts` - Find system conflicts

### **Session 2: Auto-Registration** - DELIVERED
- ✅ Auto-register new scripts on startup
- ✅ `8825 registry review` - Review auto-registered items
- ✅ `8825 registry update` - Manual refinement
- ✅ Git hook template for commit-time registration
- ✅ Registry: 7 → 116 scripts (100% coverage)

### **Session 3: Impact Analysis** - DELIVERED
- ✅ `8825 impact <change>` - Predict consequences
- ✅ Risk assessment (LOW/MEDIUM/HIGH)
- ✅ Pattern detection for common changes
- ✅ Recommendations and warnings

**Key Achievements:**
- 116 scripts registered (100% coverage)
- 10 components touch ~/Downloads
- 7 duplicate implementations found
- Exclusion pattern conflicts detected
- Zero-friction maintenance
- Predictive safety before changes

---

## Future Enhancements (Phase 3)

### **Phase 3: Brain Integration (Optional)**
- System topology in BRAIN_TRANSPORT
- Scripts check brain before acting
- Change history tracking
- Self-healing capabilities

---

## Troubleshooting

### **Command not found: 8825**
```bash
# Re-create symlink
sudo ln -sf "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/registry/8825.sh" /usr/local/bin/8825
```

### **Dependency installation fails**
```bash
# Check Homebrew
brew --version

# Install manually
brew install jq
pip3 install watchdog
```

### **Health check warnings**
```bash
# Run cleanup
bash INBOX_HUB/sync_downloads_folders.sh

# Check again
8825 health
```

---

## Success Criteria

Phase 1 is successful if:
- [x] `8825 start` runs without errors
- [x] Registry tracks core components
- [x] Dependencies auto-install
- [x] Health checks detect daemon status
- [x] Health checks detect Downloads bloat
- [x] BRAIN_TRANSPORT presence verified
- [x] Command accessible from anywhere

**All criteria met. Phase 1 complete.**

---

## Next Steps

1. **Use it daily** - Run `8825 start` every morning
2. **Monitor** - Watch for warnings
3. **Refine** - Adjust checks as needed
4. **Phase 2** - Add audit tools when ready

---

**The 12-cycle loop is broken. The tether is in place.**
