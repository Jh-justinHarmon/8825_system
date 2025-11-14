# 8825 System Refactor - Master Plan
**Date:** 2025-11-13  
**Status:** Active  
**Decisions Locked In:** ✅

---

## Decision Log

### 1. Graduation Path
**Approved:** sandbox → shared → core  
**Rationale:** Clear promotion signal, prevents focus burial

### 2. POC Audit
**Current:** Manual review  
**Future:** Automated (after criteria proven through doing)  
**Cascade will prompt:** When criteria ready for automation

### 3. Deletion Strategy
**Approach:** Delete aggressively with high confidence  
**Safety:** Maintain deleted items reference log  
**Scope:** Limited to `/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825`  
**Rationale:** Git history available, but reference log prevents searching

### 4. Cascade Lock Timeout
**Duration:** 15 minutes auto-unlock  
**Rationale:** Balance safety vs not blocking work if Cascade crashes

---

## Phase 1: Immediate Cleanup (Week 1)

### Task 1.1: MCP Server Migration ⏳
**Status:** Scripted, ready to execute  
**Time:** 3 minutes  
**Script:** `migrate_mcp_servers.sh`  
**What:** Consolidate 11 servers → 9 unique in ~/mcp_servers/  
**Safety:** Automatic backup created

### Task 1.2: Cascade Lock System 🔨
**Status:** Build now  
**Time:** 30 minutes  
**Deliverables:**
- `~/.8825/cascade.lock` mechanism
- `8825_core/system/cascade_lock.sh` helpers
- 15-minute auto-unlock
- Lock status checker

### Task 1.3: Deleted Items Log 📋
**Status:** Build now  
**Time:** 10 minutes  
**Location:** `8825-system/migrations/deleted_items_log.json`  
**Format:** Date, path, reason, git commit

### Task 1.4: Username Consolidation 🔧
**Status:** Ready to execute  
**Time:** 10 minutes  
**What:** justinharmon → justin_harmon + symlink  
**Files affected:** 62 items in users/justinharmon/

### Task 1.5: Version Reference Cleanup 🔧
**Status:** Ready to execute  
**Time:** 15 minutes  
**What:** Replace 37 "8825-system" and "8825-system" references  
**Tool:** Automated sed script

### Task 1.6: Archive Completion Docs 📦
**Status:** Ready to execute  
**Time:** 10 minutes  
**What:** Move 34 COMPLETE/FINAL docs to migrations/  
**Deletion:** High confidence items deleted, logged

---

## Phase 2: Structure Refactor (Week 2-3)

### Task 2.1: Create Layered Architecture 🏗️
**Status:** Pending Phase 1  
**Time:** 1 hour  
**What:**
```
8825-system/
├── core/           (system essentials)
├── shared/         (cross-focus)
├── focuses/        (focus-specific only)
└── sandbox/        (experiments/POCs)
```

### Task 2.2: Migrate POCs to Sandbox 🔄
**Status:** Pending 2.1  
**Time:** 2 hours  
**What:**
- 8825_core/poc/* → sandbox/experimental/
- focuses/*/poc/* → sandbox/experimental/
- Tag each with origin metadata

### Task 2.3: Promote Production POCs 🎓
**Status:** Pending 2.2  
**Time:** 3 hours  
**Manual Review Required:** Yes (first iteration)  
**What:**
- otter_integration → shared/integrations/
- tgif_automation → shared/automations/ (consolidate 3 copies)
- Delete duplicates (logged)

### Task 2.4: Focus Cleanup 🧹
**Status:** Pending 2.3  
**Time:** 2 hours  
**What:**
- Keep only focus-specific items in focuses/
- Move shared items to shared/
- Document what stayed and why

---

## Phase 3: Tooling (Week 4)

### Task 3.1: POC Auditor 🔍
**Status:** Pending Phase 2  
**Time:** 4 hours  
**Deliverable:** `8825 audit poc` command  
**Features:**
- Age detection
- Production usage detection
- Stability analysis
- Promotion recommendations

### Task 3.2: Promotion Helper 🚀
**Status:** Pending 3.1  
**Time:** 3 hours  
**Deliverable:** `8825 promote <source> <destination>` command  
**Features:**
- Move files
- Update references
- Create migration log
- Validate post-move

### Task 3.3: Version Metadata System 📊
**Status:** Pending Phase 2  
**Time:** 2 hours  
**Deliverable:** `8825-system/version.json`  
**Features:**
- System version
- Schema version
- Migration level
- Compatibility info

---

## Phase 4: Documentation (Week 5)

### Task 4.1: Architecture Documentation 📚
**Status:** Pending Phase 3  
**Time:** 2 hours  
**Deliverable:** `ARCHITECTURE.md`  
**Content:**
- Layered structure explanation
- Promotion paths
- Naming conventions
- Location guidelines

### Task 4.2: Workflow Documentation 📖
**Status:** Pending 4.1  
**Time:** 2 hours  
**Deliverable:** `WORKFLOWS.md`  
**Content:**
- How to promote POCs
- How to create new focuses
- How to use Cascade lock
- Common operations

### Task 4.3: Migration Summary 📝
**Status:** Pending 4.2  
**Time:** 1 hour  
**Deliverable:** `migrations/2025-11-refactor/COMPLETE.md`  
**Content:**
- What changed
- Why changed
- Lessons learned
- Metrics (time saved, duplicates removed, etc.)

### Task 4.4: Aggressive Cleanup 🗑️
**Status:** Pending 4.3  
**Time:** 1 hour  
**What:**
- Delete old completion docs (logged)
- Consolidate duplicate READMEs
- Remove outdated guides
- Final sweep

---

## Success Metrics

### Quantitative
- [ ] MCP servers: 11 locations → 1 location
- [ ] Duplicates: 5+ → 0
- [ ] User directories: 2 → 1 (+ symlink)
- [ ] Version references: 37 → 0
- [ ] Completion docs: 34 → 0 (archived)
- [ ] POCs in production: 3+ → 0
- [ ] Time to find resource: 5-10 min → <30 sec

### Qualitative
- [ ] Can explain where anything belongs
- [ ] New person could navigate system
- [ ] Multi-Cascade safe
- [ ] Clear what's experimental vs production
- [ ] Upgrade path doesn't break references

---

## Risk Mitigation

### High Risk Items
1. **MCP Migration** - Ghost processes, broken references
   - Mitigation: Automatic backup, can rollback
   
2. **POC Promotion** - Might move wrong things
   - Mitigation: Manual review first iteration
   
3. **Aggressive Deletion** - Might delete needed items
   - Mitigation: Deleted items log, git history

### Medium Risk Items
1. **Username consolidation** - Might break references
   - Mitigation: Symlink maintains compatibility
   
2. **Version cleanup** - Might miss some references
   - Mitigation: Grep verification before/after

### Low Risk Items
1. **Cascade lock** - New system, might have bugs
   - Mitigation: 15-min auto-unlock prevents deadlock
   
2. **Documentation** - Can't really break anything
   - Mitigation: N/A

---

## Rollback Plan

### Per Phase
**Phase 1:** Individual task rollback from backups  
**Phase 2:** Git revert + restore from migrations/  
**Phase 3:** Disable tools, revert to manual  
**Phase 4:** Docs only, no rollback needed

### Emergency Rollback
```bash
# Nuclear option: restore from pre-refactor state
git checkout <pre-refactor-commit>
# Or restore from migrations/pre-refactor-backup/
```

---

## Timeline

**Week 1:** Phase 1 (Immediate Cleanup)  
**Week 2-3:** Phase 2 (Structure Refactor)  
**Week 4:** Phase 3 (Tooling)  
**Week 5:** Phase 4 (Documentation)

**Total:** 5 weeks to complete refactor  
**Usable after:** Week 1 (basics work, just not optimal)

---

## Communication Protocol

### Cascade Will Prompt When:
- POC audit criteria ready for automation
- High-confidence deletion about to happen
- Structural change affects multiple subsystems
- Manual review needed
- Risk level increases

### User Reviews Required:
- First POC promotion (set precedent)
- Aggressive deletions (first few times)
- Major structural changes
- Tool automation criteria

---

## Next Actions

1. ✅ Build Cascade lock system
2. ✅ Build deleted items log
3. ✅ Execute Task 1.1 (MCP migration)
4. Review results, iterate

---

**Status:** Ready to execute Phase 1  
**Cascade will prompt before each major step**
