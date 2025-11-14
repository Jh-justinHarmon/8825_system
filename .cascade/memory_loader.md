# Cascade Memory Loader

**Trigger Phrase:** "load MLP chat mode"

---

## Auto-Load Instructions for Cascade

When the user types "load MLP chat mode", execute the following:

### Step 1: Read MLP Chat Mode File
```
Read: Documents/MLP_CHAT_MODE.md
```

### Step 2: Load Latest Session Export
```
Read: Documents/SESSION_MEMORY_EXPORT_20251108.md
```

### Step 3: Confirm Context Loaded
Report to user:
- ✅ Systems loaded (count)
- ✅ Roadmap status loaded
- ✅ Time calibration factors loaded
- ✅ Key file locations loaded
- ✅ Ready to continue work

---

## Current Session Export

**File:** `Documents/SESSION_MEMORY_EXPORT_20251108.md`  
**Date:** 2025-11-08  
**Systems:** 6  
**Roadmap Items:** 6

---

## Quick Context Summary

### Systems Operational
1. Meeting Prep System (`8825_core/meeting_prep/`)
2. Time Calibration System (`8825_core/system/time_calibration.py`)
3. Inbox Ingestion System (`8825_core/workflows/ingestion/`)
4. Input Hub Phase 1 (`INBOX_HUB/`)
5. Roadmap System (`Documents/roadmap/`)
6. Partner Credit System Phase 1 (`8825_core/protocols/`)

### Roadmap (6 items, 81.5 hours total)
**Refactor Queue:**
- refactor-001: Shared ingestion core (4h)
- refactor-002: 8825+Goose integration (16h)
- refactor-003: Partner credit automation (20h)

**Foundation Sprint:**
- proto-001: MCP Input Hub Phase 2 (6.5h)
- proto-002: TV Memory Layer (20h)
- proto-004: Partner credit marketplace (15h)

### Time Calibration
1.77x faster than estimates
- Simple: 0.53x
- Medium: 0.56x
- Complex: 0.57x

---

**This file enables "load MLP chat mode" to work in any Cascade window.**
