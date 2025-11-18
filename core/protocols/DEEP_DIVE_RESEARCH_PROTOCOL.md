# Deep Dive Research Protocol

**Purpose:** Ensure comprehensive system analysis that finds ALL components, not just the obvious ones  
**Created:** November 12, 2025  
**Trigger:** User says "deep dive", "fully understand", "why is this happening again", or mentions repeated failures

---

## The Problem This Solves

**What happened:** Downloads sync issue attempted 14 times. Deep dive missed Universal Inbox Watch (PID 9731) running since Saturday because:
- It watched `8825_inbox` subfolders (not raw Downloads)
- Different naming pattern than expected
- Long-running process (not recently started)
- Grep searches focused on "Downloads" and "sync" but missed "8825_inbox"

**Result:** Incomplete analysis → incomplete solution → problem persisted

---

## Deep Dive Checklist

### **Phase 1: Process Discovery (What's Actually Running)**

#### 1.1 Find ALL Processes Related to Topic
```bash
# Don't just search for obvious keywords
ps aux | grep -E "keyword1|keyword2|keyword3" | grep -v grep

# Cast a WIDE net - search for:
# - Direct keywords (downloads, sync)
# - Related keywords (watch, monitor, inbox)
# - System names (8825, universal, daemon)
# - File operations (rsync, fswatch, watchdog)
```

**Critical:** Search for RELATED concepts, not just exact matches.

#### 1.2 Check Process Start Times
```bash
ps aux -o pid,lstart,command | grep keyword
```

**Why:** Long-running processes are easy to miss. They may have started days ago and become "invisible".

#### 1.3 Check LaunchAgents/Daemons
```bash
launchctl list | grep -i keyword
ls ~/Library/LaunchAgents/*.plist
ls /Library/LaunchDaemons/*.plist
```

**Why:** Automated processes may not show up in simple ps searches.

---

### **Phase 2: File System Discovery (What Exists)**

#### 2.1 Find ALL Related Files
```bash
# Search by name
find /path -name "*keyword*" -type f

# Search by content
grep -r "keyword" /path --include="*.py" --include="*.sh"

# Search for BOTH active AND archived
find /path -name "*keyword*" | grep -v ".git"
```

**Critical:** Check ARCHIVED/EXPERIMENTAL folders - they may contain clues or active references.

#### 2.2 Check Multiple Naming Patterns
```bash
# Don't assume one naming convention
find /path -name "*download*"
find /path -name "*sync*"
find /path -name "*watch*"
find /path -name "*inbox*"
find /path -name "*universal*"
```

**Why:** Systems evolve. Old names, new names, variations all exist.

#### 2.3 Check Configuration Files
```bash
# Find all configs that might reference the system
find /path -name "*.json" -o -name "*.yaml" -o -name "*.conf"
grep -r "keyword" /path --include="*.json" --include="*.yaml"
```

---

### **Phase 3: Dependency Discovery (What Calls What)**

#### 3.1 Trace Imports/Calls
```bash
# Python imports
grep -r "from.*keyword" /path --include="*.py"
grep -r "import.*keyword" /path --include="*.py"

# Shell script calls
grep -r "keyword.sh" /path --include="*.sh"
grep -r "python.*keyword" /path --include="*.sh"
```

#### 3.2 Check Cron/LaunchAgent Scripts
```bash
# What do LaunchAgents actually run?
cat ~/Library/LaunchAgents/*.plist | grep -A5 "ProgramArguments"

# What do those scripts call?
grep -r "python3" /path --include="*.sh"
grep -r "nohup" /path --include="*.sh"
```

#### 3.3 Map the Call Chain
```
LaunchAgent → Script → Python → Module → Function
```

**Document each layer** - don't assume you know what's running.

---

### **Phase 4: State Discovery (What's Configured)**

#### 4.1 Check ALL Config Files
```bash
# Don't just read one config
find /path -name "*config*.json"
find /path -name "*.conf"
find /path -name ".env"
```

#### 4.2 Check Environment Variables
```bash
# What's set in shell configs?
grep -r "export.*KEYWORD" ~/.*rc ~/.*profile

# What's set in LaunchAgents?
grep -r "EnvironmentVariables" ~/Library/LaunchAgents/
```

#### 4.3 Check State Files
```bash
# PID files
find /path -name "*.pid"

# Lock files
find /path -name "*.lock"

# State files
find /path -name "*state*" -o -name "*status*"
```

---

### **Phase 5: Log Discovery (What's Been Happening)**

#### 5.1 Find ALL Log Files
```bash
# Standard locations
ls /tmp/*keyword*.log
ls /var/log/*keyword*
ls ~/Library/Logs/*keyword*

# Custom locations
find /path -name "*.log"
grep -r "logging" /path --include="*.py" | grep "FileHandler"
```

#### 5.2 Check Log Contents
```bash
# Recent activity
tail -100 /path/to/log

# Errors
grep -i error /path/to/log
grep -i fail /path/to/log

# Timestamps (when did it start?)
head -20 /path/to/log
```

---

### **Phase 6: Integration Discovery (What Else Touches This)**

#### 6.1 Search for References
```bash
# Who mentions this system?
grep -r "system_name" /entire/codebase --include="*.py" --include="*.sh" --include="*.md"

# Check documentation
grep -r "system_name" /path --include="*.md" --include="README*"
```

#### 6.2 Check MCP Servers
```bash
# MCP servers may integrate with the system
find /path -name "*mcp*" -type d
grep -r "system_name" /path/mcp-servers/
```

#### 6.3 Check Workflows
```bash
# Workflows may depend on the system
find /path/workflows -name "*.md"
grep -r "system_name" /path/workflows/
```

---

## Research Documentation Template

When doing a deep dive, create a document with this structure:

```markdown
# Deep Dive: [System Name]

**Date:** [Date]
**Trigger:** [Why we're investigating]
**Attempts:** [How many times we've tried to fix this]

---

## 1. Active Processes

| PID | Command | Started | Status |
|-----|---------|---------|--------|
| ... | ...     | ...     | ...    |

## 2. File System Components

### Active
- [List all active files/scripts]

### Archived
- [List archived/experimental files]

### Configuration
- [List all config files]

## 3. Call Chains

```
Process A → Script B → Module C → Function D
```

## 4. State

- Config values: [...]
- Environment vars: [...]
- State files: [...]

## 5. Logs

- Location: [...]
- Recent activity: [...]
- Errors: [...]

## 6. Integrations

- Called by: [...]
- Calls: [...]
- Depends on: [...]

## 7. The Problem

[Clear description of what's broken]

## 8. Root Cause

[Why it's broken - trace back to architecture]

## 9. Previous Attempts

| Attempt | What We Tried | Why It Failed |
|---------|---------------|---------------|
| 1       | ...           | ...           |
| ...     | ...           | ...           |

## 10. The Solution

[What we're doing differently this time]

## 11. Why This Will Work

[Architectural reasoning]
```

---

## Critical Mistakes to Avoid

### ❌ **Mistake 1: Searching Too Narrowly**
**Bad:** `grep "downloads_sync"`  
**Good:** `grep -E "download|sync|watch|monitor|inbox"`

### ❌ **Mistake 2: Ignoring Long-Running Processes**
**Bad:** Only checking recently started processes  
**Good:** `ps aux -o lstart` to see ALL start times

### ❌ **Mistake 3: Assuming One System**
**Bad:** "Found the sync script, that's it"  
**Good:** "Found sync script, what else touches Downloads?"

### ❌ **Mistake 4: Ignoring Archives**
**Bad:** Only searching active code  
**Good:** Check EXPERIMENTAL, ARCHIVED, OLD folders

### ❌ **Mistake 5: Not Mapping Dependencies**
**Bad:** "This script does X"  
**Good:** "This script calls Y which imports Z which uses config W"

### ❌ **Mistake 6: Trusting Documentation**
**Bad:** "The README says it works like this"  
**Good:** "Let me verify what's actually running"

### ❌ **Mistake 7: Not Checking Logs**
**Bad:** Assuming based on code  
**Good:** Checking logs to see what actually happened

### ❌ **Mistake 8: Single Point of View**
**Bad:** Only checking from one angle (processes OR files OR configs)  
**Good:** Check ALL angles and cross-reference

---

## The "Cast a Wide Net" Principle

**When searching, use MULTIPLE related terms:**

For "Downloads sync issue":
- downloads, download
- sync, syncing, synchronize
- watch, watcher, watching, monitor
- inbox, input, pending
- rsync, fswatch, watchdog
- universal, daemon, agent
- icloud, desktop, mobile
- 8825_inbox, 8825_processed

**Then cross-reference findings.**

---

## The "Trust But Verify" Principle

**Never assume:**
- ✅ Check if process is running: `ps aux | grep`
- ✅ Check if LaunchAgent is loaded: `launchctl list`
- ✅ Check if file exists: `ls -la`
- ✅ Check if config is active: `cat config.json`
- ✅ Check logs for actual behavior: `tail -f log`

**Don't trust:**
- ❌ "This should be running"
- ❌ "The documentation says..."
- ❌ "We set this up before"
- ❌ "I remember this working"

---

## The "Complete Picture" Checklist

Before proposing a solution, verify you have:

- [ ] All running processes identified
- [ ] All related files found (active + archived)
- [ ] All configuration files read
- [ ] All call chains mapped
- [ ] All logs checked
- [ ] All integrations identified
- [ ] All previous attempts documented
- [ ] Root cause identified (not just symptoms)
- [ ] Architectural understanding (why it's designed this way)
- [ ] Solution addresses root cause (not just symptoms)

**If you can't check all boxes, you're not done researching.**

---

## Publishing Results

### 1. Create Analysis Document
**Location:** `[SYSTEM]/DEEP_DIVE_ANALYSIS_[DATE].md`

**Include:**
- Complete findings (all 6 phases)
- Root cause analysis
- Previous attempts and why they failed
- Proposed solution
- Why this solution addresses root cause

### 2. Create Solution Document
**Location:** `[SYSTEM]/PERMANENT_SOLUTION_[ISSUE].md`

**Include:**
- Implementation steps
- Verification steps
- Rollback plan
- Success criteria
- Why this won't break again

### 3. Update System Documentation
**Files to update:**
- README.md (add warning/note)
- ARCHITECTURE.md (document actual state)
- TROUBLESHOOTING.md (add this issue)

### 4. Create Memory
**Tags:** `deep_dive`, `root_cause`, `[system_name]`, `critical_fix`

**Content:**
- Problem summary
- Root cause
- Solution
- Files modified
- Verification commands

### 5. Create Status Document
**Location:** `[SYSTEM]/SYSTEM_STATUS.md`

**Include:**
- Current state (what's running)
- Verification commands
- Troubleshooting steps
- Last updated date

---

## Example: Downloads Sync Deep Dive (Nov 12, 2025)

### What We Missed Initially
- Universal Inbox Watch (PID 9731) running since Saturday
- Watching `8825_inbox` subfolders (not raw Downloads)
- Different naming pattern (`universal_inbox_watch` not `downloads_sync`)

### Why We Missed It
- Searched for "downloads" and "sync" but not "inbox" or "universal"
- Didn't check long-running processes (only recent activity)
- Didn't search archived/experimental folders thoroughly

### How We Found It
- Expanded search: `grep -E "downloads|sync|watch|inbox|universal"`
- Checked all processes: `ps aux | grep -E "download|sync|watch"`
- Found reference in MCP server pointing to archived FDS

### What We Did Differently
- Cast wider net with multiple search terms
- Checked process start times (found Saturday start)
- Mapped complete architecture (4 systems, not 2)
- Documented ALL findings before proposing solution
- Created comprehensive solution addressing root cause

---

## Success Metrics

**Before Deep Dive Protocol:**
- 14 attempts to fix Downloads sync
- Incomplete analysis each time
- Solutions addressed symptoms, not root cause
- Problem persisted

**After Deep Dive Protocol:**
- Complete system map (4 systems identified)
- Root cause identified (architectural conflict)
- Solution addresses architecture (no sync, separate outputs)
- Verified working

**Time Investment:**
- Deep dive: 45 minutes
- Implementation: 20 minutes
- **Total:** 65 minutes

**ROI:**
- Previous attempts: 14 × 30 min = 7 hours wasted
- Future prevention: ∞ hours saved
- **Never have this conversation again**

---

## When to Use This Protocol

**Triggers:**
- User says "we've tried this X times"
- User says "here we go again"
- User says "deep dive"
- User says "fully understand"
- User says "why is this still happening"
- You've attempted a fix more than twice
- System behavior doesn't match documentation
- Multiple overlapping systems exist

**Don't skip steps. Incomplete research = incomplete solution.**

---

**This protocol is now part of the 8825 core. Use it. Follow it. Avoid the 14-attempt nightmare.**
