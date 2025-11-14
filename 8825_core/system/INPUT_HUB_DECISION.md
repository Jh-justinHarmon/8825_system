# Input Hub + Roadmap Decision

## Your Requirements

1. **Screenshot frequency:** Multiple times per day (HIGH volume)
2. **Context complexity:** Even more challenging than inbox ingestion
3. **Immediate need:** Quick reference sync (not full automation yet)
4. **Long-term:** MCP Input Hub is right solution

---

## Decision: Two-Phase Approach

### Phase 1: Quick Reference Sync (NOW)
**Time:** ~30 minutes (calibrated)

**What:**
- Mirror screenshots to 8825 structure
- Basic metadata (filename, timestamp, source)
- Quick reference via "checking sg" command
- NO automation, NO OCR, NO complex routing

**Why:**
- Solves immediate need (reference screenshots)
- Validates folder structure
- Tests workflow before automation

**Deliverable:**
- Folder structure
- Manual sync script
- "checking sg" command
- Works today

---

### Phase 2: Full MCP Input Hub (NEXT RELEASE)
**Time:** ~6.5 hours (calibrated)
**Status:** → Roadmap (Foundation Sprint Backlog)

**What:**
- Watchdog auto-sync
- OCR integration
- Complex context routing
- Learning from patterns
- Full MCP integration

**Why:**
- Needs proper design (context is harder than inbox)
- Requires refactoring to avoid duplication
- Should integrate with existing inbox patterns
- Worth doing right, not rushed

**Deliverable:**
- Teaching ticket for architecture review
- Foundation sprint backlog item
- Proper integration plan

---

## Refactoring Analysis

### Current State
- **Inbox system:** Complete (validator, classifier, router, AI sweep)
- **Input Hub needs:** Similar logic but different context

### Refactoring Required

#### Option A: Duplicate Logic (BAD)
- Copy classifier, router, validator
- Maintain two systems
- **Time:** 2.5 hours
- **Tech debt:** HIGH

#### Option B: Extract Shared Core (GOOD)
- Extract common ingestion patterns
- Both inbox + input hub use shared core
- **Time:** 4 hours refactor + 2.5 hours input hub = 6.5 hours
- **Tech debt:** LOW

#### Option C: Unified Ingestion System (BEST)
- One system handles all inputs (JSON, screenshots, files, etc.)
- Input type = just another classification dimension
- **Time:** 6.5 hours
- **Tech debt:** ZERO

**Recommendation:** Option C for next release

---

## Roadmap Filing

### Refactor Queue Item
```json
{
  "id": "refactor-003",
  "title": "Extract shared ingestion core",
  "description": "Create unified ingestion system for inbox + input hub",
  "source": "input_hub_analysis",
  "priority": "high",
  "effort": "medium",
  "impact": "high",
  "dependencies": [],
  "tags": ["architecture", "ingestion", "v3.0"],
  "status": "queued",
  "notes": "Prevents duplication between inbox and input hub systems"
}
```

### Foundation Sprint Backlog Item
```json
{
  "id": "proto-003",
  "title": "MCP Input Hub with context learning",
  "description": "Full screenshot/file ingestion with OCR and context routing",
  "source": "input_hub_analysis",
  "priority": "high",
  "effort": "medium",
  "impact": "high",
  "dependencies": ["refactor-003"],
  "tags": ["mcp", "automation", "context", "screenshots"],
  "status": "queued",
  "prototype_goals": [
    "Auto-sync screenshots from Desktop/Downloads",
    "Extract context via OCR + window title",
    "Route to correct project/focus",
    "Learn from user corrections"
  ],
  "success_criteria": "Can auto-route 80% of screenshots correctly",
  "created": "2025-11-08"
}
```

---

## Implementation Plan

### TODAY: Phase 1 Quick Reference (30 min)

**Build:**
1. Folder structure (3m)
2. Manual sync script (12m)
3. "checking sg" command (10m)
4. Test (5m)

**Result:**
- Can reference screenshots immediately
- Validates structure
- No automation overhead

### NEXT RELEASE: Phase 2 Full System

**Prerequisites:**
1. Refactor shared ingestion core
2. Design context extraction strategy
3. Review teaching ticket for architecture

**Build:**
1. Unified ingestion system
2. Screenshot handler
3. OCR integration
4. Context learning
5. MCP integration

---

## Recommendation

### Do Now (30 min)
✅ Build Phase 1 quick reference sync  
✅ Create roadmap items for Phase 2  
✅ File to appropriate queues  

### Do Next Release
✅ Refactor shared ingestion core  
✅ Build full MCP Input Hub  
✅ Integrate with existing systems  

**This avoids:**
- Rushed implementation
- Duplicate code
- Technical debt
- Major refactoring later

**This enables:**
- Quick reference today
- Proper design for Phase 2
- Clean integration
- Learning from Phase 1 usage

---

## Questions

1. **Build Phase 1 now?** (30 min quick reference sync)
2. **File Phase 2 to roadmap?** (Foundation sprint backlog)
3. **Create roadmap system first?** (If you want to use it for filing)

**My recommendation:** 
1. Build Phase 1 quick sync (30m)
2. Create roadmap system (20m)
3. File Phase 2 to backlog
4. Review and prioritize for next release
