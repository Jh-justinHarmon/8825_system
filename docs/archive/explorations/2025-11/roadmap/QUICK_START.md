# Roadmap Quick Start

## View Current Items

### All Refactors
```bash
cd Documents/roadmap
cat refactor_queue.json | jq '.items[]'
```

### All Prototypes
```bash
cat foundation_sprint_backlog.json | jq '.items[]'
```

### High Priority Only
```bash
# Refactors
jq '.items[] | select(.priority == "high")' refactor_queue.json

# Prototypes
jq '.items[] | select(.priority == "high")' foundation_sprint_backlog.json
```

---

## Current Roadmap (2025-11-08)

### Refactor Queue
1. **refactor-001:** Extract shared ingestion core
   - Priority: HIGH
   - Effort: 4 hours (medium)
   - Impact: HIGH
   - Status: Queued
   - Prevents code duplication between inbox and input hub

### Foundation Sprint Backlog
1. **proto-001:** MCP Input Hub with context learning
   - Priority: HIGH
   - Effort: 6.5 hours (medium)
   - Impact: HIGH
   - Status: Queued
   - Depends on: refactor-001
   - Phase 1 complete (quick reference sync)
   - Phase 2 queued (full automation)

---

## Next Sprint Planning

### Ready to Start
**refactor-001** (no dependencies)
- Extract shared ingestion core
- 4 hours
- Enables proto-001

### Blocked
**proto-001** (depends on refactor-001)
- MCP Input Hub
- 6.5 hours
- Needs refactor-001 first

### Recommended Order
1. Complete refactor-001 (4h)
2. Build proto-001 (6.5h)
3. **Total: 10.5 hours (~1.5 days)**

---

## Quick Commands

### Add Item
```bash
# Edit the JSON file directly
vim refactor_queue.json
# or
vim foundation_sprint_backlog.json
```

### Mark In Progress
```bash
jq '.items[0].status = "in_progress"' refactor_queue.json > temp.json
mv temp.json refactor_queue.json
```

### Mark Complete
```bash
jq '.items[0].status = "complete"' refactor_queue.json > temp.json
mv temp.json refactor_queue.json
```

---

## Integration with Input Hub

### Phase 1 (Complete)
- ✅ Folder structure
- ✅ Manual sync script
- ✅ "checking sg" command
- ✅ Quick reference working

### Phase 2 (Roadmap)
- ⏳ Filed to foundation_sprint_backlog.json
- ⏳ ID: proto-001
- ⏳ Depends on: refactor-001
- ⏳ Status: Queued

**Location:** `INBOX_HUB/` (Phase 1 complete)  
**Next:** Refactor shared core, then build Phase 2
