# MLP Chat Mode - Memory Load Protocol

**Trigger:** Type "load MLP chat mode" in any Cascade window

**Purpose:** Instantly load all context from the most recent session export

---

## What This Does

When you type "load MLP chat mode", Cascade will:

1. Load the most recent session memory export
2. Restore context for all systems built
3. Load roadmap status and priorities
4. Restore file locations and usage patterns
5. Load time calibration factors
6. Restore meeting prep and Joju context

---

## Current Session Export

**Latest:** `Documents/SESSION_MEMORY_EXPORT_20251108.md`

**Date:** 2025-11-08  
**Systems:** 6 complete systems  
**Roadmap Items:** 6 items filed  
**Status:** All systems operational

---

## Quick Reference

### Systems Built
1. **Meeting Prep System** - `8825_core/meeting_prep/`
2. **Time Calibration System** - `8825_core/system/time_calibration.py`
3. **Inbox Ingestion System** - `8825_core/workflows/ingestion/`
4. **Input Hub Phase 1** - `INBOX_HUB/`
5. **Roadmap System** - `Documents/roadmap/`
6. **Partner Credit System Phase 1** - `8825_core/protocols/`

### Roadmap Status
**Refactor Queue (3 items):**
- refactor-001: Shared ingestion core (4h)
- refactor-002: 8825+Goose integration (16h)
- refactor-003: Partner credit automation (20h)

**Foundation Sprint (3 items):**
- proto-001: MCP Input Hub Phase 2 (6.5h)
- proto-002: TV Memory Layer (20h)
- proto-004: Partner credit marketplace (15h)

### Time Calibration
- Simple: 0.53x
- Medium: 0.56x
- Complex: 0.57x
- Overall: 1.77x faster than estimates

### Key Files
- Meeting Prep Draft: `~/Documents/8825/meeting_prep/20251108_Matthew_Galley_prep_DRAFT.md`
- Session Export: `Documents/SESSION_MEMORY_EXPORT_20251108.md`
- Roadmap: `Documents/roadmap/`
- Partner Credit: `8825_core/protocols/`

---

## Usage

### In Any Cascade Window

**Type:**
```
load MLP chat mode
```

**Cascade will:**
1. Read this file
2. Load `SESSION_MEMORY_EXPORT_20251108.md`
3. Restore full context
4. Confirm what was loaded

---

## Manual Load (If Needed)

If "load MLP chat mode" doesn't work, use:

```
Read Documents/MLP_CHAT_MODE.md and Documents/SESSION_MEMORY_EXPORT_20251108.md
```

---

## Update Protocol

When creating a new session export:

1. Create new `SESSION_MEMORY_EXPORT_YYYYMMDD.md`
2. Update this file's "Current Session Export" section
3. Update "Latest" date
4. Keep old exports for history

---

**MLP = Memory Load Protocol**

**Last Updated:** 2025-11-08 18:32
