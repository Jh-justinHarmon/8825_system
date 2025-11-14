# Phase 1: Immediate Cleanup - Ready to Execute
**Date:** 2025-11-13  
**Status:** ✅ Ready  
**Infrastructure Built:** ✅ Complete

---

## Infrastructure Built

### 1. Cascade Lock System ✅
**Location:** `8825_core/system/cascade_lock.sh`  
**Features:**
- Prevents multi-Cascade collisions
- 15-minute auto-unlock (as requested)
- Lock status checking
- Force unlock option

**Usage:**
```bash
# In any system-wide operation script:
source 8825_core/system/cascade_lock.sh
acquire_lock "operation description" || exit 1
# ... do work ...
release_lock
```

**Test it:**
```bash
cd 8825_core/system
./cascade_lock.sh check          # Check if locked
./cascade_lock.sh acquire "test" # Acquire lock
./cascade_lock.sh check          # Should show lock
./cascade_lock.sh release        # Release lock
```

### 2. Deleted Items Log ✅
**Location:** `migrations/deleted_items_log.json`  
**Helper:** `8825_core/system/log_deletion.sh`

**Features:**
- Tracks all deletions
- Records path, reason, confidence, git commit
- Scoped to 8825 folder only
- Prevents git searching

**Usage:**
```bash
# Before deleting anything:
./8825_core/system/log_deletion.sh "/path/to/item" "reason" "high"
# Then delete the item
```

### 3. Master Plan ✅
**Location:** `REFACTOR_MASTER_PLAN.md`  
**Contains:**
- All decisions locked in
- 4-phase execution plan
- Success metrics
- Risk mitigation
- Rollback procedures

---

## Phase 1 Tasks - Ready to Execute

### Task 1.1: MCP Server Migration
**Script:** `migrate_mcp_servers.sh` (already created, executable)  
**What:** Consolidate 11 servers → 9 unique in ~/mcp_servers/  
**Time:** 3 minutes  
**Backup:** Automatic  
**Risk:** Low (has rollback)

**Will do:**
1. Acquire Cascade lock
2. Create backup
3. Move 5 scattered servers to ~/mcp_servers/
4. Delete 5 duplicates (logged)
5. Update registry
6. Kill ghost processes
7. Release lock

### Task 1.2: Username Consolidation
**What:** Merge `users/justinharmon/` → `users/justin_harmon/`  
**Time:** 10 minutes  
**Safety:** Symlink created for compatibility

**Will do:**
1. Move 62 items from justinharmon/ to justin_harmon/
2. Create symlink: justinharmon → justin_harmon
3. Verify no broken references
4. Log if anything deleted

### Task 1.3: Version Reference Cleanup
**What:** Replace 37 references to "8825-system" and "8825-system"  
**Time:** 15 minutes  
**Tool:** Automated sed script

**Will do:**
1. Find all references with grep
2. Replace with "8825-system"
3. Verify with post-grep
4. Show before/after counts

### Task 1.4: Archive Completion Docs
**What:** Move 34 COMPLETE/FINAL docs to migrations/  
**Time:** 10 minutes  
**Deletion:** High-confidence duplicates deleted (logged)

**Will do:**
1. Find all *COMPLETE*.md and *FINAL*.md files
2. Review each for deletion vs archive
3. Move keepers to migrations/2025-11-cleanup/
4. Delete high-confidence duplicates (logged)
5. Show summary report

### Task 1.5: Rename 8825-system Folder
**What:** `windsurf-project - 8825 8825-system/` → `8825-archive-2025-11/`  
**Time:** 2 minutes  
**Why:** Date-based archiving, no version in path

---

## Execution Order

```
1. Test Cascade Lock (verify it works)
2. Execute MCP Migration (biggest impact, do first)
3. Username Consolidation (structural change)
4. Version Reference Cleanup (fixes references)
5. Rename 8825-system folder (cleanup)
6. Archive Completion Docs (cleanup)
```

---

## Before Each Task

I will:
1. **Explain** what I'm about to do
2. **Show** the command(s)
3. **Acquire** Cascade lock (if system-wide)
4. **Wait** for your approval
5. **Execute** the task
6. **Report** results
7. **Release** lock

---

## High-Confidence Deletions

These will be deleted with logging (not archived):

### MCP Duplicates (5 items)
- `8825_core/integrations/figjam/mcp-server/` - duplicate of ~/mcp_servers/figjam/
- `8825_core/integrations/goose/mcp-servers/hcss-bridge/` - duplicate of ~/mcp_servers/hcss-bridge/
- `focuses/hcss/automation/otter_mcp/` - duplicate 1 of 3
- `focuses/hcss/poc/tgif_automation/otter_mcp/` - duplicate 2 of 3
- `8825-system/mcp_servers/` if empty - wrong location

**Confidence:** 100% (already documented as duplicates)

### Completion Docs (subset, TBD)
Will review each, but likely candidates:
- Docs that just say "Complete" with no useful info
- Duplicates of content already in git
- Phase completion markers with no content

**Confidence:** 90%+ (will show you list before deleting)

---

## Safety Measures

1. **Cascade Lock** - Prevents other Cascade from interfering
2. **Backups** - MCP script creates automatic backup
3. **Deletion Log** - Every deletion logged with git commit
4. **Symlinks** - Maintain compatibility (username)
5. **Git History** - Everything recoverable
6. **Incremental** - One task at a time, verify each

---

## Expected Outcomes After Phase 1

### File Structure
```
8825/
├── 8825-system/           (current, no version)
├── 8825-archive-2025-11/  (old v2.1, archived)
├── 8825_customers/
├── 8825_keys/
└── ...

8825-system/
├── users/
│   ├── justin_harmon/     (consolidated)
│   └── justinharmon@      (symlink)
└── ...

~/mcp_servers/
├── 8825-core/
├── hcss-bridge/
├── figma-make-transformer/
├── figjam/
├── otter-integration/     (consolidated)
├── fds/
├── meeting-automation/
├── ral-portal/
└── customer-platform/
```

### Metrics
- MCP locations: 5 → 1
- MCP duplicates: 5 → 0
- User directories: 2 → 1 (+symlink)
- Version references: 37 → 0
- Completion docs: 34 → ~10 (kept useful ones)
- Ghost processes: 3 → 0

### Clean State
- All MCP servers findable in one location
- No version numbers in paths
- Consistent username
- Clean references
- Ready for Phase 2 (structure refactor)

---

## Verification Steps

After each task:
1. **Grep verify** - Check references updated
2. **Symlink verify** - Check compatibility maintained
3. **Process verify** - Check ghost processes killed
4. **Registry verify** - Check MCP registry accurate
5. **Function verify** - Test that things work

---

## Ready to Proceed?

**All infrastructure built.**  
**All tasks planned.**  
**Safety measures in place.**

**Shall I:**
1. Test the Cascade lock system (verify it works)
2. Then proceed with Task 1.1 (MCP Migration)?

Or would you like to review anything first?
