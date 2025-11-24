# 8825 Open Source Publishing - Master Execution Plan

**Version**: 1.0.0  
**Created**: 2025-11-24  
**Status**: Ready to Execute  
**Timeline**: 2 weeks (14 days)

---

## Quick Navigation

- [Overview](#overview)
- [Phase 0: Foundation (Days 1-3)](#phase-0-foundation--safety-days-1-3)
- [Phase 1: Pilot (Days 4-5)](#phase-1-pilot-component-days-4-5)
- [Phase 2: Core Migration (Days 6-10)](#phase-2-core-components-days-6-10)
- [Phase 3: Launch (Days 11-14)](#phase-3-continuous-publishing-days-11-14)
- [Maintenance](#ongoing-maintenance)
- [Command Reference](#command-reference)

---

## Overview

### Goal
Establish automated pipeline to continuously publish OSS-safe components from private `8825-Jh` to public `8825-core` repository.

### Strategy
- Use `oss/` as clean staging area (not full repo scrub)
- Publish via `git subtree split` to preserve history
- Automated safety checks before every promotion
- OSS Evaluation Gate integrated into production workflow

### What's Already Done ✅
- ✅ OSS Policy document (`oss/OSS_POLICY.md`)
- ✅ Safety evaluation script (`scripts/oss_evaluate.sh`)
- ✅ Promotion script (`scripts/promote_to_oss.sh`)
- ✅ Publishing script (`scripts/publish_oss.sh`)

---

## Phase 0: Foundation & Safety (Days 1-3)

**Objective**: Establish policy, tools, and clean internal repository

### Day 1: Create OSS Evaluation Gate Protocol

**Task**: Document the evaluation process  
**File**: `8825_core/protocols/OSS_EVALUATION_GATE.md`

**Content Outline**:
```markdown
# OSS Evaluation Gate Protocol

## When to Trigger
- Creating *_COMPLETE.md
- Marking feature as "Production Ready"
- Tagging prod-* release

## Evaluation Checklist
1. Run: ./scripts/oss_evaluate.sh <component>
2. Check against OSS_POLICY.md
3. Test in isolation
4. Document in OSS_MIGRATION_LOG.md

## Approval Process
- Self-evaluate
- Automated checks
- Manual policy review
- Promote to oss/
- Test and commit
```

### Day 2: Internal Cleanup (NDA Compliance)

**Task 1**: Delete/Archive Client Data

```bash
# Create archive directory
mkdir -p 8825-archive-2025-11/client_data_removed/

# Move (don't delete) client data
mv focuses/hcss/ 8825-archive-2025-11/client_data_removed/
mv users/justin_harmon/hcss/ 8825-archive-2025-11/client_data_removed/
mv 8825_core/projects/8825_HCSS*.json 8825-archive-2025-11/client_data_removed/
mv shared/automations/tgif/ 8825-archive-2025-11/client_data_removed/

# Delete personal user data (safer to archive first)
mv users/justin_harmon/ 8825-archive-2025-11/client_data_removed/
mv INBOX_HUB/users/jh/ 8825-archive-2025-11/client_data_removed/
```

**Task 2**: Scrub Hardcoded Paths

```bash
# Find all hardcoded paths
grep -r "/Users/justinharmon" . --exclude-dir={node_modules,.venv,8825-archive-2025-11} > hardcoded_paths.txt

# Replace with environment variables (carefully!)
# Review each file manually or use safe regex replace
find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.venv/*" \
  -not -path "*/8825-archive-2025-11/*" \
  -exec sed -i '' 's|/Users/justinharmon|${HOME}|g' {} +
```

**Task 3**: OCR Cleanup (from CLEANUP_PLAN_OCR_NOV17.md)

```bash
# Archive experimental OCR
mkdir -p 8825-archive-2025-11/ocr_experimental
mv INBOX_HUB/EXPERIMENTAL_UNUSED_20251111/* 8825-archive-2025-11/ocr_experimental/

# Archive old backups (keep most recent)
mkdir -p 8825-archive-2025-11/old_backups
ls -td 8825-system-local-backup-* | tail -n +2 | xargs -I {} mv {} 8825-archive-2025-11/old_backups/
```

### Day 3: Validation

```bash
# Verify no broken imports
find 8825_core -name "*.py" -exec python3 -m py_compile {} \; 2>&1 | grep -v "^$"

# Verify no client references
grep -r "HCSS\|TGIF" . --exclude-dir=8825-archive-2025-11 --exclude-dir=node_modules

# Verify no hardcoded paths remain
grep -r "/Users/justinharmon" . --exclude-dir=8825-archive-2025-11 --exclude-dir=node_modules

# Verify no secrets
grep -rE "sk-[a-zA-Z0-9]{20,}" . --exclude-dir=node_modules --exclude-dir=.venv
```

**Deliverable**: Document results in `oss/PHASE_0_COMPLETE.md`

---

## Phase 1: Pilot Component (Days 4-5)

**Objective**: Test full workflow with Template Word Generator

### Day 4: Evaluate & Promote

**Task 1**: Run Safety Check
```bash
./scripts/oss_evaluate.sh 8825_core/scripts/template_word_generator_v2.py
```

**Task 2**: Create OSS Documentation

Create `oss/tools/template_word_generator/README.md`:
```markdown
# Template Word Generator

Generate styled Word documents from JSON or Markdown.

## Installation
pip install python-docx

## Usage
python template_word_generator_v2.py template.docx content.json output.docx
```

**Task 3**: Create Synthetic Examples
- `examples/demo_template.docx` (generic business template)
- `examples/demo_content.json` (sample data)
- `examples/demo_content.md` (markdown version)

**Task 4**: Promote to OSS
```bash
./scripts/promote_to_oss.sh \
  8825_core/scripts/template_word_generator_v2.py \
  tools/template_word_generator/
```

### Day 5: Test & Refine

**Test in Isolation**:
```bash
# Create temp environment
cd /tmp && mkdir test_oss && cd test_oss

# Copy only OSS files
cp -r ~/path/to/8825-Jh/oss/tools/template_word_generator .

# Test
pip install python-docx
python template_word_generator_v2.py examples/demo_template.docx examples/demo_content.json output.docx
```

**Deliverable**: `oss/PHASE_1_PILOT_COMPLETE.md` with lessons learned

---

## Phase 2: Core Components (Days 6-10)

**Objective**: Migrate essential framework components

### Day 6: Library Foundation

1. Extract library schema: `8825_core/library/init_library_db.sql` → `oss/core/library/schema/`
2. Extract engine code (generic CRUD) → `oss/core/library/engine/`
3. Create `oss/core/library/README.md`
4. Create `oss/core/library/examples/demo_library.py` (synthetic data)

### Day 7: Universal Inbox Pattern

1. Create `oss/tools/universal_inbox/file_watcher.py` (generic pattern)
2. Create `oss/tools/universal_inbox/README.md`
3. Create `oss/tools/universal_inbox/examples/simple_inbox.py`

### Day 8: DLI & Intelligence

1. Migrate architecture docs → `oss/core/architecture/`
   - DLI_ARCHITECTURE.md
   - TELEMETRY_ARCHITECTURE.md
   - PPM_ARCHITECTURE.md
2. Create toy DLI MCP → `oss/mcp/dli_example/`
3. Include telemetry schema → `oss/mcp/dli_example/schema/`

### Day 9: OCR & Tools

1. Extract tesseract-only OCR → `oss/mcp/ocr_mcp/`
2. Create Goose worker pattern → `oss/tools/goose_worker/`
3. Test all tools in isolation

### Day 10: Protocols & Examples

1. Migrate protocols: `8825_core/protocols/*.md` → `oss/core/protocols/` (scrubbed)
2. Create `oss/examples/demo_focus/` (empty template)
3. Create `oss/examples/tutorials/` (step-by-step guides)

**Deliverable**: `oss/PHASE_2_MIGRATION_COMPLETE.md`

---

## Phase 3: Continuous Publishing (Days 11-14)

**Objective**: Launch public repo and establish maintenance

### Day 11: GitHub Setup

1. Create public GitHub repo: `8825-core`
2. Add LICENSE (MIT or Apache 2.0)
3. Add basic README
4. Configure branch protection

**Setup Publishing**:
```bash
./scripts/publish_oss.sh --setup https://github.com/yourusername/8825-core.git
```

**Initial Push**:
```bash
# Final safety check
find oss/ -type f -exec ./scripts/oss_evaluate.sh {} \;

# Commit all OSS changes
git add oss/
git commit -m "Initial OSS migration"

# Push to public repo
./scripts/publish_oss.sh --push
```

### Day 12: CI/CD Pipeline

Create in public repo `.github/workflows/`:

**1. Safety Scan** (`safety-scan.yml`)
```yaml
name: Safety Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for hardcoded paths
        run: |
          if grep -r "/Users/" .; then exit 1; fi
```

**2. Tests** (`tests.yml`)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

**3. Smoke Test** (`smoke-test.yml`)
```yaml
name: Smoke Test
on: [push, pull_request]
jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cd examples/demo_library && python demo_library.py
```

### Day 13: Documentation & Governance

Create in public repo:
- `CONTRIBUTING.md` - How to contribute
- `CODE_OF_CONDUCT.md` - Community guidelines
- `GOVERNANCE.md` - Project governance

Create in private repo:
- `oss/MAINTENANCE.md` - Monthly/quarterly tasks
- `8825_core/system/RELEASE_PROTOCOL.md` - OSS gate integration

### Day 14: Validation & Launch

1. Fresh clone on different machine
2. Follow quick start guide
3. Run all examples
4. Verify no private data
5. Create launch announcement

**Deliverable**: `oss/PHASE_3_LAUNCH_COMPLETE.md`

---

## Ongoing Maintenance

### Monthly Tasks
1. Review new production components for OSS eligibility
2. Batch publish updates to public repo
3. Monitor issues/PRs
4. Security scan: `./scripts/oss_evaluate.sh oss/`

### Quarterly Tasks
1. Review and update OSS_POLICY.md
2. Review closed components (can any open now?)
3. Metrics review (stars, forks, contributors)
4. Archive cleanup

---

## Command Reference

**Evaluate component for OSS**:
```bash
./scripts/oss_evaluate.sh <path>
```

**Promote to OSS staging**:
```bash
./scripts/promote_to_oss.sh <source> <destination>
```

**Setup publishing (once)**:
```bash
./scripts/publish_oss.sh --setup <repo_url>
```

**Publish to public repo**:
```bash
./scripts/publish_oss.sh --push
```

**Batch safety check**:
```bash
find oss/ -type f \( -name "*.py" -o -name "*.sh" \) -exec ./scripts/oss_evaluate.sh {} \;
```

---

## Success Metrics

### Phase 0
- [ ] 0 client data files
- [ ] 0 hardcoded paths
- [ ] 0 secrets
- [ ] All validation passing

### Phase 1
- [ ] Pilot works in isolation
- [ ] Safety checks pass
- [ ] External user can use it

### Phase 2
- [ ] Library + 4 tools migrated
- [ ] 10+ protocols in OSS
- [ ] 3+ examples working

### Phase 3
- [ ] Public repo live
- [ ] 3 CI workflows passing
- [ ] Fresh install works

---

**Status**: Ready to begin Phase 0, Day 1

See detailed task breakdowns in individual phase completion documents.
