# Phase 2: Audit Tools & Auto-Registration - Brainstorm

**Date:** 2025-11-10  
**Status:** BRAINSTORM - Awaiting Review  
**Prerequisites:** Phase 1 Complete ✅

---

## Problem Statement

**Phase 1 gave us:**
- Registry of components
- Health monitoring
- Dependency checking
- Startup validation

**But we still can't answer:**
- "What will break if I change this script?"
- "What else touches Downloads?"
- "Is it safe to start this daemon?"
- "What depends on this dependency?"

**And:** Registry has 7 scripts registered, but 109 exist. Manual registration doesn't scale.

---

## Phase 2 Goals

### **1. Visibility (Audit Tools)**
Answer "what touches what" instantly

### **2. Impact Analysis**
Predict consequences before making changes

### **3. Auto-Registration**
Keep registry current without manual work

---

## Component 1: Audit Tools

### **Purpose:**
Commands to inspect system and understand relationships

---

### **Tool 1: `8825 audit path <path>`**

**What it does:**
Shows everything that touches a specific path

**Example:**
```bash
$ 8825 audit path ~/Downloads

=== Audit: ~/Downloads ===

Scripts (8):
  1. sync_downloads_folders.sh
     • Type: sync
     • Purpose: Manual sync with auto-cleanup
     • Last modified: 2025-11-09
     • Safe to run: YES
     • Excludes: old, sticky_*, brainstorm, IMG_*
  
  2. simple_sync_and_process.sh
     • Type: sync
     • Purpose: One-way sync iCloud → Local
     • Last modified: 2025-11-09
     • Safe to run: YES
     • Excludes: 8825_processed, old, sticky_*
  
  3. cleanup_downloads.sh
     • Type: cleanup
     • Purpose: Move 8825 files to archive
     • Last modified: 2025-11-08
     • Safe to run: YES
  
  [... 5 more scripts ...]

Daemons (1):
  • downloads_sync.py
    - Status: STOPPED
    - Purpose: Bidirectional sync
    - Last run: 2025-11-09 (killed after 3 days)
    - Excludes: old, sticky_*, brainstorm, IMG_*
    - Safe to start: YES (exclusions match scripts)

Conflicts:
  ✅ No conflicts detected
  ✅ All exclusion patterns match

Recommendations:
  • Keep daemon stopped unless continuous sync needed
  • Use sync_downloads_folders.sh for manual sync
  • Monitor Downloads size with 8825 health

Total touchpoints: 9
Risk level: LOW (all components coordinated)
```

**Implementation:**
```bash
#!/bin/bash
# 8825 audit path

path=$1
registry="8825_core/registry/SYSTEM_REGISTRY.json"

# Normalize path
path=$(echo "$path" | sed "s|^~|$HOME|")

# Find scripts that touch this path
scripts=$(jq -r --arg path "$path" '
  .scripts[] | 
  select(.touches[]? | contains($path)) | 
  .name
' "$registry")

# Find daemons that touch this path
daemons=$(jq -r --arg path "$path" '
  .daemons[] | 
  select(.touches[]? | contains($path)) | 
  .name
' "$registry")

# Display results with details
# Check for conflicts (different exclusion patterns)
# Provide recommendations
```

**Feasibility:** ✅ HIGH - JSON querying, straightforward

---

### **Tool 2: `8825 audit component <name>`**

**What it does:**
Shows details about a specific component

**Example:**
```bash
$ 8825 audit component downloads_sync

=== Component: downloads_sync ===

Type: Daemon
Path: 8825_core/sync/downloads_sync.py
Status: STOPPED

Purpose:
  Bidirectional synchronization between local and iCloud Downloads.
  Watches both locations and syncs changes in real-time.

What it touches:
  • ~/Downloads
  • ~/Library/Mobile Documents/com~apple~CloudDocs/Downloads

Exclusions:
  • old, - old -, .DS_Store, .tmp, ~$
  • 8825_inbox (synced by different daemon)
  • sticky_*, brainstorm, client_secret
  • mythic, phils_book, IMG_*

Dependencies:
  • python3 (3.9+) ✅ installed
  • watchdog ✅ installed

Started by:
  8825_core/sync/start_all_sync.sh

Log file:
  8825_core/sync/logs/downloads_sync.log

Last activity:
  • Started: 2025-11-06 09:00
  • Killed: 2025-11-09 21:47
  • Duration: 3 days 12 hours
  • Reason for kill: Fixed exclusion patterns

Conflicts with:
  ✅ None (exclusions now match other scripts)

Safe to start: YES
  • Exclusions updated 2025-11-09
  • Matches sync_downloads_folders.sh patterns
  • No other daemons touching same paths

To start:
  cd 8825_core/sync && bash start_all_sync.sh

To stop:
  pkill -f downloads_sync.py

To monitor:
  tail -f 8825_core/sync/logs/downloads_sync.log
```

**Implementation:**
```bash
#!/bin/bash
# 8825 audit component

component=$1
registry="8825_core/registry/SYSTEM_REGISTRY.json"

# Check if it's a daemon
daemon_data=$(jq -r --arg name "$component" '
  .daemons[] | select(.name == $name)
' "$registry")

# Check if it's a script
script_data=$(jq -r --arg name "$component" '
  .scripts[] | select(.name == $name)
' "$registry")

# Display comprehensive details
# Check dependencies
# Check conflicts
# Provide usage instructions
```

**Feasibility:** ✅ HIGH - JSON querying, formatting

---

### **Tool 3: `8825 audit dependency <dep>`**

**What it does:**
Shows what requires a specific dependency

**Example:**
```bash
$ 8825 audit dependency watchdog

=== Dependency: watchdog ===

Type: Python package
Status: ✅ Installed
Version: 3.0.0
Check: python3 -c 'import watchdog'
Install: pip3 install watchdog

Required by (2):
  1. downloads_sync.py (daemon)
     • Purpose: Bidirectional Downloads sync
     • Status: STOPPED
  
  2. inbox_sync.py (daemon)
     • Purpose: 3-way inbox sync
     • Status: STOPPED

Impact if removed:
  ⚠️  HIGH - Both sync daemons will fail
  
Impact if updated:
  ⚠️  MEDIUM - Test daemons after upgrade
  
Recommendation:
  Keep installed. Critical for sync infrastructure.
```

**Implementation:**
```bash
#!/bin/bash
# 8825 audit dependency

dep=$1
registry="8825_core/registry/SYSTEM_REGISTRY.json"

# Get dependency info
dep_info=$(jq -r --arg dep "$dep" '
  .system_dependencies[$dep]
' "$registry")

# Find all components that require it
components=$(jq -r --arg dep "$dep" '
  (.scripts[] | select(.dependencies[]? == $dep) | .name),
  (.daemons[] | select(.dependencies[]? == $dep) | .name)
' "$registry")

# Display info and impact analysis
```

**Feasibility:** ✅ HIGH - JSON querying

---

### **Tool 4: `8825 audit conflicts`**

**What it does:**
Finds conflicts in the system

**Example:**
```bash
$ 8825 audit conflicts

=== Conflict Detection ===

Checking for:
  • Duplicate implementations
  • Conflicting exclusion patterns
  • Overlapping touchpoints
  • Orphaned processes

[1/4] Duplicate Implementations...
  ⚠️  Found 1 duplicate:
    • downloads_sync.py
      - Location 1: 8825_core/sync/downloads_sync.py
      - Location 2: users/justin_harmon/jh_assistant/projects/download-wedge/downloads_sync.py
      - Recommendation: Delete duplicate, keep only 8825_core version

[2/4] Exclusion Pattern Conflicts...
  ✅ No conflicts
  All scripts touching Downloads have matching exclusions

[3/4] Overlapping Touchpoints...
  ℹ️  ~/Downloads touched by 9 components
    • 8 scripts (coordinated)
    • 1 daemon (stopped)
    • Risk: LOW (all use same exclusions)

[4/4] Orphaned Processes...
  ✅ No orphaned processes detected
  All running processes are registered

Overall: 1 issue found
Action required: Remove duplicate downloads_sync.py
```

**Implementation:**
```bash
#!/bin/bash
# 8825 audit conflicts

# Find duplicate files
find . -name "*.py" -o -name "*.sh" | 
  awk -F/ '{print $NF}' | 
  sort | uniq -d

# Compare exclusion patterns across scripts
# Check for unregistered running processes
# Identify overlapping touchpoints
```

**Feasibility:** ✅ MEDIUM - Requires file scanning and comparison

---

## Component 2: Impact Analysis

### **Purpose:**
Predict consequences before making changes

---

### **Tool: `8825 impact <change_description>`**

**What it does:**
Analyzes proposed change and predicts impact

**Example 1: Changing exclusion pattern**
```bash
$ 8825 impact "add *.png to IMG_ exclusions"

=== Impact Analysis ===

Change: Add *.png to IMG_ exclusions
Current pattern: IMG_*.HEIC, IMG_*.jpeg
Proposed pattern: IMG_*

Affected components (3):
  1. downloads_sync.py
     • Current: IMG_ (matches .HEIC, .jpeg)
     • Change: Update to IMG_* (all extensions)
     • Impact: Will stop syncing PNG images
     • Line: 34
  
  2. sync_downloads_folders.sh
     • Current: IMG_*.HEIC, IMG_*.jpeg
     • Change: Add IMG_*.png
     • Impact: Auto-cleanup will remove PNG images
     • Line: 36
  
  3. simple_sync_and_process.sh
     • Current: IMG_*.HEIC, IMG_*.jpeg
     • Change: Add IMG_*.png
     • Impact: Won't sync PNG from iCloud
     • Line: 49

Dependencies affected: None

Risk assessment:
  • Risk level: LOW
  • Breaking changes: None
  • Data loss risk: None (files excluded, not deleted)

Execution plan:
  1. Update downloads_sync.py line 34
  2. Update sync_downloads_folders.sh line 36
  3. Update simple_sync_and_process.sh line 49
  4. Test with sample PNG file
  5. Monitor for 24 hours

Estimated time: 10 minutes
Rollback plan: Revert exclusion patterns

Proceed? (y/n)
```

**Example 2: Starting a daemon**
```bash
$ 8825 impact "start downloads_sync daemon"

=== Impact Analysis ===

Change: Start downloads_sync daemon
Current status: STOPPED
Proposed status: RUNNING

What will happen:
  • Daemon watches ~/Downloads and iCloud Downloads
  • Any file change triggers bidirectional sync
  • Runs continuously until killed
  • Logs to 8825_core/sync/logs/downloads_sync.log

Conflicts:
  ✅ No conflicts with running processes
  ✅ Exclusions match other scripts
  ✅ No other daemons touching same paths

Resource usage:
  • CPU: Low (idle until file changes)
  • Memory: ~50MB
  • Disk I/O: High during sync events

Risk assessment:
  • Risk level: MEDIUM
  • Could re-sync files if exclusions incomplete
  • Will run until explicitly stopped
  • May interfere with manual sync scripts

Recommendations:
  • Only start if continuous sync needed
  • Monitor logs for first hour
  • Use manual sync scripts instead if possible

Dependencies:
  • python3 ✅ installed
  • watchdog ✅ installed

Safe to start: YES (with monitoring)

To start:
  cd 8825_core/sync && bash start_all_sync.sh

To monitor:
  tail -f 8825_core/sync/logs/downloads_sync.log

To stop:
  pkill -f downloads_sync.py

Proceed? (y/n)
```

**Example 3: Removing a dependency**
```bash
$ 8825 impact "remove watchdog package"

=== Impact Analysis ===

Change: Remove watchdog package
Current status: INSTALLED
Proposed status: REMOVED

Affected components (2):
  1. downloads_sync.py (daemon)
     • Impact: WILL FAIL
     • Severity: HIGH
     • Workaround: None
  
  2. inbox_sync.py (daemon)
     • Impact: WILL FAIL
     • Severity: HIGH
     • Workaround: None

Risk assessment:
  • Risk level: HIGH
  • Breaking changes: 2 daemons will fail
  • System impact: Sync infrastructure broken

Recommendation:
  ❌ DO NOT REMOVE
  
  This dependency is critical for sync infrastructure.
  Removing it will break bidirectional sync capabilities.

Alternative:
  If you need to update watchdog:
    pip3 install --upgrade watchdog
  
  Then test both daemons before relying on them.

Proceed? (y/n)
```

**Implementation:**
```bash
#!/bin/bash
# 8825 impact

change_description=$1
registry="8825_core/registry/SYSTEM_REGISTRY.json"

# Parse change description (basic heuristics)
# - Look for keywords: "add", "remove", "start", "stop", "change"
# - Extract component names
# - Extract patterns/dependencies

# Query registry for affected components
# Analyze dependencies
# Check for conflicts
# Assess risk level
# Generate execution plan

# Display comprehensive impact report
```

**Advanced Implementation (Future):**
```python
# Use LLM to parse change description
# Semantic analysis of code
# Dependency graph traversal
# Risk scoring algorithm
```

**Feasibility:** 
- ✅ **Basic version:** HIGH - Pattern matching, registry queries
- ⚠️ **Advanced version:** MEDIUM - Requires code analysis

---

## Component 3: Auto-Registration

### **Purpose:**
Keep registry current without manual work

---

### **Approach 1: Scan on Startup (Current)**

**What happens:**
- `8825 start` scans filesystem
- Compares to registry
- Reports new scripts
- **Does NOT auto-add** (Phase 1)

**Pros:**
- Safe (no automatic changes)
- User aware of new scripts

**Cons:**
- Registry stays out of date
- Manual work required

---

### **Approach 2: Auto-Add on Startup (Phase 2)**

**What happens:**
```bash
$ 8825 start

[1/4] Registry Validation
  Scanning for scripts...
  ⚠️  Found 3 new scripts:
    - users/justin_harmon/new_tool.sh
    - 8825_core/new_processor.py
    - INBOX_HUB/new_sync.sh
  
  Analyzing dependencies...
    • new_tool.sh requires: bash, jq
    • new_processor.py requires: python3
    • new_sync.sh requires: bash, rsync
  
  Auto-registering...
    ✅ new_tool.sh added to registry
    ✅ new_processor.py added to registry
    ✅ new_sync.sh added to registry
  
  Registry updated: 7 → 10 scripts
```

**How it works:**
```bash
#!/bin/bash
# auto_register.sh

script_path=$1
script_name=$(basename "$script_path")

# Detect type
if [[ $script_path == *.py ]]; then
    type="python"
elif [[ $script_path == *.sh ]]; then
    type="bash"
fi

# Extract dependencies (heuristics)
deps=()

# Check for common imports/commands
if grep -q "import watchdog" "$script_path"; then
    deps+=("watchdog")
fi

if grep -q "rsync" "$script_path"; then
    deps+=("rsync")
fi

if grep -q "jq" "$script_path"; then
    deps+=("jq")
fi

# Try to detect purpose (keywords in comments/filename)
if [[ $script_name == *sync* ]]; then
    purpose="Sync script"
    category="sync"
elif [[ $script_name == *cleanup* ]]; then
    purpose="Cleanup script"
    category="cleanup"
else
    purpose="Unknown - needs manual review"
    category="unknown"
fi

# Try to detect what it touches (grep for common paths)
touches=()
if grep -q "~/Downloads" "$script_path"; then
    touches+=("~/Downloads")
fi

# Add to registry
jq ".scripts += [{
    \"name\": \"$script_name\",
    \"path\": \"$script_path\",
    \"type\": \"$category\",
    \"purpose\": \"$purpose\",
    \"dependencies\": $(printf '%s\n' "${deps[@]}" | jq -R . | jq -s .),
    \"touches\": $(printf '%s\n' "${touches[@]}" | jq -R . | jq -s .),
    \"auto_registered\": true,
    \"needs_review\": true,
    \"added\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
}]" SYSTEM_REGISTRY.json > tmp.json && mv tmp.json SYSTEM_REGISTRY.json
```

**Pros:**
- Registry stays current automatically
- Dependencies detected
- No manual work

**Cons:**
- Heuristics may be wrong
- Needs manual review/refinement
- Could add noise

**Mitigation:**
- Flag auto-registered items as "needs review"
- Provide `8825 registry review` command
- Allow manual correction

---

### **Approach 3: Git Hook Registration**

**What happens:**
```bash
# On every git commit
# .git/hooks/post-commit

# Scan for new/modified scripts
new_files=$(git diff --name-only HEAD~1 HEAD | grep -E '\.(sh|py)$')

# Auto-register each
for file in $new_files; do
    8825 registry add "$file"
done

# Update registry timestamp
jq '.last_updated = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
    SYSTEM_REGISTRY.json > tmp.json && mv tmp.json SYSTEM_REGISTRY.json
```

**Pros:**
- Catches changes immediately
- Tied to version control
- No manual work

**Cons:**
- Adds to commit time
- May be annoying
- Could miss uncommitted scripts

---

### **Approach 4: File Watcher (Real-time)**

**What happens:**
```python
# Daemon that watches for new scripts
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ScriptWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(('.sh', '.py')):
            print(f"New script detected: {event.src_path}")
            auto_register(event.src_path)

observer = Observer()
observer.schedule(ScriptWatcher(), path='8825_core/', recursive=True)
observer.schedule(ScriptWatcher(), path='INBOX_HUB/', recursive=True)
observer.start()
```

**Pros:**
- Real-time updates
- Catches everything
- No manual work

**Cons:**
- Another daemon to manage
- Resource usage
- Complexity

---

### **Recommended Approach: Hybrid**

**Combine Approach 2 + 3:**

1. **Auto-add on startup** (catches everything eventually)
2. **Git hook** (catches changes immediately for committed code)
3. **Flag for review** (user can refine auto-registered items)

**Workflow:**
```bash
# Developer adds new script
vim new_tool.sh

# Commits it
git add new_tool.sh
git commit -m "Add new tool"
# → Git hook auto-registers it

# Next startup
8825 start
# → Validates registration, checks dependencies

# Review auto-registered items
8825 registry review
# → Shows items needing manual refinement
# → User can update purpose, touchpoints, etc.
```

**Feasibility:** ✅ HIGH - Combines proven patterns

---

## Implementation Plan

### **Step 1: Build Audit Tools (4-6 hours)**

**Deliverables:**
- `8825 audit path <path>` - Show what touches a path
- `8825 audit component <name>` - Show component details
- `8825 audit dependency <dep>` - Show dependency usage
- `8825 audit conflicts` - Find system conflicts

**Files:**
- `8825_core/registry/audit_path.sh`
- `8825_core/registry/audit_component.sh`
- `8825_core/registry/audit_dependency.sh`
- `8825_core/registry/audit_conflicts.sh`
- Update `8825.sh` wrapper with audit subcommands

---

### **Step 2: Build Impact Analysis (4-6 hours)**

**Deliverables:**
- `8825 impact <change>` - Predict consequences
- Basic pattern matching for common changes
- Risk assessment
- Execution plan generation

**Files:**
- `8825_core/registry/impact_analysis.sh`
- Update `8825.sh` wrapper

---

### **Step 3: Build Auto-Registration (3-4 hours)**

**Deliverables:**
- `auto_register.sh` - Register new scripts
- Git hook for automatic registration
- `8825 registry review` - Review auto-registered items
- `8825 registry update <name>` - Manually refine entries

**Files:**
- `8825_core/registry/auto_register.sh` (enhanced)
- `.git/hooks/post-commit`
- `8825_core/registry/registry_review.sh`
- `8825_core/registry/registry_update.sh`
- Update `validate_registry.sh` to auto-register on startup

---

## Total Effort

**Estimated:** 11-16 hours

**Can split into:**
- Session 1: Audit tools (4-6 hours)
- Session 2: Impact analysis (4-6 hours)
- Session 3: Auto-registration (3-4 hours)

---

## Success Criteria

### **Audit Tools:**
- [ ] `8825 audit path ~/Downloads` shows all touchpoints
- [ ] `8825 audit component downloads_sync` shows comprehensive details
- [ ] `8825 audit dependency watchdog` shows all dependents
- [ ] `8825 audit conflicts` finds duplicate downloads_sync.py

### **Impact Analysis:**
- [ ] `8825 impact "add *.png exclusion"` shows affected components
- [ ] `8825 impact "start downloads_sync"` assesses risk correctly
- [ ] `8825 impact "remove watchdog"` warns about breakage
- [ ] Execution plans are actionable

### **Auto-Registration:**
- [ ] New scripts auto-registered on startup
- [ ] Git hook registers on commit
- [ ] Dependencies detected automatically
- [ ] `8825 registry review` shows items needing refinement
- [ ] Registry grows from 7 → 109+ scripts

---

## Risks & Mitigations

### **Risk 1: Auto-registration is inaccurate**
**Impact:** Medium - Wrong dependencies, wrong purpose
**Mitigation:** 
- Flag items as "needs review"
- Provide easy refinement tools
- Start with conservative heuristics

### **Risk 2: Impact analysis misses edge cases**
**Impact:** Medium - User makes change thinking it's safe, breaks something
**Mitigation:**
- Start with "always check manually" disclaimer
- Improve heuristics over time
- Add confidence scores

### **Risk 3: Audit tools are slow**
**Impact:** Low - Annoying but not breaking
**Mitigation:**
- Cache registry queries
- Optimize JSON parsing
- Add progress indicators

### **Risk 4: Too many auto-registered scripts**
**Impact:** Low - Registry becomes noisy
**Mitigation:**
- Filter by directory (only register core paths)
- Exclude test/temp scripts
- Provide bulk review tools

---

## Open Questions

1. **Auto-registration scope:** Register all 109 scripts or just core ones?
   - Recommendation: Start with 8825_core/, INBOX_HUB/, users/justin_harmon/jh_assistant/
   - Exclude: explorations/, poc/, test files

2. **Impact analysis depth:** How deep should analysis go?
   - Recommendation: Start shallow (direct dependencies), enhance over time

3. **Conflict resolution:** What if audit finds conflicts?
   - Recommendation: Report only, don't auto-fix (too risky)

4. **Registry size:** Will 109+ scripts make queries slow?
   - Recommendation: Test with full registry, optimize if needed

5. **Git hook annoyance:** Will auto-registration on commit be annoying?
   - Recommendation: Make it fast (<1 second), add --no-verify option

---

## Alternative Approaches

### **Option A: Audit Tools Only**
- Build audit commands
- Skip impact analysis and auto-registration
- Keep registry manual

**Pros:** Lower risk, simpler
**Cons:** Doesn't solve registry staleness

---

### **Option B: Auto-Registration Only**
- Focus on keeping registry current
- Skip audit and impact tools
- Manual inspection when needed

**Pros:** Registry stays current
**Cons:** Still can't answer "what will break?"

---

### **Option C: Full Phase 2**
- All three components
- Comprehensive visibility and automation

**Pros:** Complete solution
**Cons:** More work, more risk

---

## Recommendation

**Build in order: Audit → Auto-Registration → Impact**

**Rationale:**
1. **Audit tools** give immediate value (visibility)
2. **Auto-registration** keeps registry current (foundation for impact)
3. **Impact analysis** requires accurate registry (build last)

**Start with:** Audit tools (Session 1)
- Quick win
- High value
- Low risk
- Validates registry structure

---

## Next Steps

**If approved:**
1. Review this brainstorm
2. Refine approach based on feedback
3. Finalize execution plan for Audit Tools
4. Build Session 1 (4-6 hours)
5. Test and validate
6. Proceed to Session 2

**If not approved:**
- Discuss concerns
- Adjust approach
- Re-brainstorm as needed

---

**This brainstorm is comprehensive but not final. Ready for your review.**
