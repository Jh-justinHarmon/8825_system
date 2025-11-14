# Phase 0: Document Discovery & Scoping
**Date:** 2025-11-13  
**Model:** Claude Sonnet 4.5  
**Scope:** Human-facing documents (.md, .txt, readable exports)

---

## Executive Summary

**Found:** 498 human-facing documents across 13 locations  
**Problem:** Scattered, duplicated, versioned, no clear structure  
**Severity:** 🔴 HIGH - Multiple output protocols, unclear findability

---

## The Numbers

### By Location
```
8825_core:      160 files (32%)
users:          114 files (23%)
INBOX_HUB:      108 files (22%)
focuses:         65 files (13%)
migrations:      20 files (4%)
shared:           8 files (2%)
sandbox:          7 files (1%)
Documents:        7 files (1%)
backups:          5 files (1%)
other:            4 files (<1%)
---
TOTAL:          498 files
```

### Top Offenders (Most Files)
1. **INBOX_HUB/users/jh/processed** - 91 files (processed outputs)
2. **users/justin_harmon/personal** - 60 files (personal notes)
3. **Root directory** - 30 files (scattered docs)
4. **users/justin_harmon/joju/docs_from_2.1** - 24 files (old version docs)
5. **8825_core/explorations/features** - 24 files (feature explorations)

---

## Document Categories

### 1. Generated Reports/Outputs
**Pattern:** COMPLETE, FINAL, SUMMARY, REPORT, AUDIT  
**Count:** ~80+ files  
**Problem:** Never cleaned up, many obsolete

**Examples:**
- `DOCUMENTATION_COMPLETE.md`
- `IMPLEMENTATION_COMPLETE.md`
- `MIGRATION_COMPLETE.md`
- `GOOSE_COMPLETE.md`
- `TASK_AUDIT_2025-11-10.md`
- `BUG_TESTING_REPORT.md`

**Recommendation:** Keep latest only, delete rest

---

### 2. Versioned Documents
**Pattern:** v1, v2, v3, version, _2.1, _3.0  
**Count:** ~30+ files  
**Problem:** Multiple versions of same doc

**Examples:**
- `PROFILE_BUILDER_V2.md`
- `docs_from_2.1/` (entire folder - 24 files)
- `20251111_note_1_2_3.md` (iteration versions)

**Recommendation:** Keep latest, archive/delete old

---

### 3. Duplicate Filenames
**Found:** 20 duplicate basenames across system

**Most Duplicated:**
- `README.md` - Multiple locations
- `STATUS.md` - Multiple locations
- `QUICKSTART.md` / `QUICK_START.md` - Naming inconsistency
- `SETUP.md` - Multiple locations
- `USER_GUIDE.md` - Multiple locations
- Daily notes (20251108_note.md, etc.) - Scattered

**Recommendation:** Consolidate, establish naming convention

---

### 4. Root Directory Clutter
**Count:** 30 files in root  
**Problem:** No organization, hard to find anything

**Current Root Files:**
```
8825_FULL_SCOPE_TEACHING.md
8825_SELF_EVALUATION_2025-11-10.md
8825_SELF_EVALUATION_2025-11-10_EVENING.md
API_REFERENCE.md
ARCHITECTURE.md
BRAIN_SYNC.md
DEPENDENCIES_UPDATED_2025-11-10.md
DEVELOPER_GUIDE.md
DOCUMENTATION_INDEX.md
GHOST_FOLDER_FIX_2025-11-10.md
GOOSE_INTEGRATION_ROADMAP.md
INBOX_PROCESSING_SUMMARY_2025-11-09.md
INTEGRATION_CHECKLIST.md
LAUNCH_READINESS_PLAN.md
MCP_BRIDGE_EXPLAINER.md
MCP_EXECUTIVE_SUMMARY.md
MCP_SERVER_DEEP_DIVE_2025-11-13.md
MCP_SERVER_VISUAL_MAP.md
MCP_STARTUP_CLARIFICATION.md
PHILOSOPHY.md
QUICK_COMMANDS.md
README.md
README_MCP_MIGRATION.md
REFACTOR_MASTER_PLAN.md
REFACTOR_PHASE_1_READY.md
SCRIPT_EVOLUTION_ANALYSIS.md
SETUP_GOOGLE_SHEETS.md
STARTUP_AUTOMATION.md
WORKFLOWS.md
requirements.txt
```

**Should Keep in Root (5-7 files max):**
- README.md
- ARCHITECTURE.md
- WORKFLOWS.md
- QUICK_COMMANDS.md (maybe)

**Should Move:**
- All COMPLETE/SUMMARY docs → archive
- All dated docs → archive
- All MCP docs → docs/reference/mcp/
- All guides → docs/reference/

---

## Output Protocol Audit

### Found 6+ Different Output Patterns:

#### 1. **Root Directory Dumps**
**Location:** `/`  
**Pattern:** `[TOPIC]_[STATUS]_[DATE].md`  
**Examples:** `DEPENDENCIES_UPDATED_2025-11-10.md`  
**Problem:** No organization

#### 2. **INBOX_HUB Processed**
**Location:** `INBOX_HUB/users/jh/processed/`  
**Pattern:** `[TIMESTAMP]_[NAME].[json|txt]`  
**Examples:** `20251108_075545_note_jh.json`  
**Problem:** 91 files, never cleaned

#### 3. **Migration Folder**
**Location:** `migrations/2025-11-cleanup/`  
**Pattern:** `[TOPIC]_COMPLETE.md`  
**Examples:** 19 COMPLETE docs  
**Problem:** Good location, but needs cleanup

#### 4. **Focus-Specific Outputs**
**Location:** `focuses/[focus]/`  
**Pattern:** Varies by focus  
**Examples:** `focuses/joju/tasks/TASK_AUDIT_2025-11-10.md`  
**Problem:** Inconsistent, mixed with code

#### 5. **User Personal Notes**
**Location:** `users/justin_harmon/personal/`  
**Pattern:** `[DATE]_note.md`  
**Examples:** 60 personal notes  
**Problem:** Good location, but 60 files is too many

#### 6. **Old Version Dumps**
**Location:** `users/justin_harmon/joju/docs_from_2.1/`  
**Pattern:** Various  
**Examples:** 24 old docs  
**Problem:** Should be archived or deleted

---

## Pain Points Identified

### 1. **No Single Source of Truth**
- 13 different locations for docs
- No clear "this is where docs go"
- Developers/AI don't know where to output

### 2. **Never Cleaned Up**
- COMPLETE docs pile up
- Generated reports never deleted
- Versioned docs kept forever

### 3. **Duplicate Naming**
- Multiple README.md files
- Multiple STATUS.md files
- Inconsistent naming (QUICK_START vs QUICKSTART)

### 4. **Root Directory Chaos**
- 30 files in root
- Mix of active/archive/obsolete
- Hard to find anything

### 5. **No Folder Limits**
- INBOX processed: 91 files
- Personal notes: 60 files
- Violates "max 10 files per folder" principle

### 6. **Versioned Docs Not Collapsed**
- `docs_from_2.1/` entire folder
- Multiple `note_1_2_3.md` iterations
- No auto-cleanup of old versions

---

## Current Document Locations (All 13)

1. **8825_core/** - 160 files
   - Mix of protocols, explorations, brainstorms
   - Some should be in docs/, some in archive

2. **users/** - 114 files
   - Personal notes (60 in justin_harmon/personal)
   - Old version docs (24 in joju/docs_from_2.1)
   - Project docs scattered

3. **INBOX_HUB/** - 108 files
   - 91 in processed/ (never cleaned)
   - Intake documents
   - Brain transport files

4. **focuses/** - 65 files
   - Task reports, workflow docs
   - Mix of active and obsolete
   - Some should be in docs/

5. **migrations/** - 20 files
   - Good location for migration docs
   - Needs cleanup of COMPLETE docs

6. **shared/** - 8 files
   - TGIF automation docs
   - Appropriate location

7. **sandbox/** - 7 files
   - POC documentation
   - Appropriate location

8. **Documents/** - 7 files
   - Roadmap docs
   - Unclear purpose, should consolidate

9. **mcp_migration_backup_20251113_110156/** - 5 files
   - Backup folder
   - Should be in migrations/ or deleted

10. **.windsurf/** - 1 file
    - IDE config
    - Appropriate location

11. **core/** - 1 file
    - README.md
    - Appropriate location

12. **docs/** - 1 file
    - Only 1 file! Should be THE location

13. **.cascade/** - 1 file
    - IDE config
    - Appropriate location

---

## Key Insights

### 1. **docs/ Folder Exists But Unused**
- Only 1 file in `docs/`
- Should be THE central location
- Currently ignored by all output protocols

### 2. **Root is Default Dump**
- 30 files in root
- Becomes default when unsure where to put things
- Needs to be locked down (only 5-7 files max)

### 3. **INBOX_HUB is Second Dump**
- 91 processed files
- Never cleaned up
- Needs auto-cleanup protocol

### 4. **Old Versions Never Deleted**
- `docs_from_2.1/` still exists
- Versioned files accumulate
- No cleanup protocol

### 5. **No Consistent Naming**
- QUICK_START vs QUICKSTART
- COMPLETE vs FINAL vs SUMMARY
- Dates in different formats

### 6. **Personal Notes Overwhelming**
- 60 files in personal/
- Needs archiving or different system
- Daily notes should auto-archive after 30 days

---

## Recommendations for Phase 1

### 1. **Establish docs/ as Central Hub**
```
docs/
├── active/          # 5-10 living docs
├── reference/       # Stable reference docs
├── generated/       # Auto-generated (auto-cleanup)
├── archive/         # Historical (by date)
└── templates/       # Document templates
```

### 2. **Root Directory Lockdown**
**Keep only:**
- README.md
- ARCHITECTURE.md
- WORKFLOWS.md
- version.json
- requirements.txt (if needed)

**Move everything else to docs/**

### 3. **Auto-Cleanup Protocols**
- Generated reports: Keep latest 5 only
- INBOX processed: Auto-archive after 30 days
- Personal notes: Auto-archive after 30 days
- Versioned docs: Keep latest only

### 4. **Naming Conventions**
- Use underscores: `QUICK_START.md` (not `QUICKSTART.md`)
- Date format: `YYYY-MM-DD` (not `YYYYMMDD`)
- Status suffixes: `_COMPLETE`, `_SUMMARY`, `_REPORT`

### 5. **Dropbox Mirror Strategy**
**Local (working):**
`~/8825-system/docs/`

**Dropbox (shareable):**
`~/Dropbox/.../8825-system-docs/`

**Sync command:**
`sync-docs-to-dropbox` (one-way mirror)

### 6. **Aggressive Deletion Targets**
**High confidence deletions (~200 files):**
- All COMPLETE docs (except latest migration summary)
- All versioned docs (keep latest only)
- All `docs_from_2.1/` (24 files)
- All duplicate README/STATUS files (keep canonical only)
- All dated self-evaluations (archive, don't keep in active)
- All INBOX processed older than 30 days (~60 files)

---

## Phase 1 Questions to Answer

1. **What's the canonical location for each doc type?**
2. **What's the auto-cleanup protocol for generated reports?**
3. **How do we handle personal notes (60 files)?**
4. **What stays in root (5-7 files max)?**
5. **How do we prevent root dumps in future?**
6. **What's the Dropbox mirror sync strategy?**
7. **What's the naming convention standard?**

---

## Metrics

**Current State:**
- Total docs: 498
- Locations: 13
- Root files: 30
- Duplicates: 20+ basenames
- COMPLETE docs: ~80
- Versioned docs: ~30
- INBOX processed: 91
- Personal notes: 60

**Target State (Phase 3):**
- Total docs: ~150 (70% reduction)
- Locations: 3 (docs/, users/, focuses/)
- Root files: 5-7 (77% reduction)
- Duplicates: 0
- COMPLETE docs: 1 (latest migration summary)
- Versioned docs: 0 (latest only)
- INBOX processed: <10 (recent only)
- Personal notes: <10 active (rest archived)

**Estimated Deletions:** ~300-350 files (60-70%)

---

## Status

✅ Discovery complete  
✅ Pain points identified  
✅ Output protocols mapped  
✅ Deletion targets identified  

**Ready for Phase 1: Ideal State Design (4.5 Thinking)**

---

**Next:** Design the perfect document architecture that prevents this chaos from ever happening again.
