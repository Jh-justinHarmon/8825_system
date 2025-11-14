# 8825 Configuration: Windsurf Cascade + Claude Sonnet 4.5 (Dev Mode)

**IDE:** Windsurf (Cascade)  
**LLM:** Claude Sonnet 4.5  
**Mode:** Dev Mode (Hyper-Efficient)  
**Created:** 2025-11-08  
**Status:** Production-Tested ✅

---

## 🎯 CORE PHILOSOPHY:

### **Dev Mode = GO MODE**
- **When:** You have a plan and understand it - now execute
- **Approach:** Do, don't discuss
- **Assumption:** Plan is clear, just needs execution
- **Communication:** Terse progress updates only
- **Speed:** Maximum - parallel ops, minimal chat
- **Trust:** You know what you want, I execute precisely

---

## 🧠 ACTIVE MEMORIES (This Session):

### **System Architecture:**
```
MEMORY[3e1011e0-7871-4898-8dbd-b97b12f45640]
Title: 8825 v3.0 Migration Complete - Multi-MCP Architecture
Tags: 8825_system, v3_migration, multi_mcp, architecture, production_ready

Content: Complete v3.0 system with 3-layer separation, Multi-MCP 
architecture (3 servers), 100% user/system separation, 133 files indexed.
Production ready in 1h 20min.
```

### **Focus Modes:**
```
MEMORY[1c888f8b-8fbe-4978-b9f6-89fd177cc45b]
Title: JH Focus Mode
Tags: jh, focus_mode, personal_workspace, 8825_system, sandbox

Content: Personal workspace at Jh_sandbox/ for individual projects,
notes, scripts. Activation: "focus on jh"
```

### **Data Locations:**
```
MEMORY[60d106d6-2f94-477f-88fb-f2cc3b861e7d]
Title: Master Professional Library Location
Tags: joju, master_library, justin_harmon, profile_data, location

Content: justin_harmon_master_library.json in joju_sandbox/libraries/
79 achievements from 9 ingestion sessions.
```

### **Workflows:**
```
MEMORY[4d0946c3-8679-497d-a68d-7be0109d5179]
Title: HCSS Meeting Summary Workflow
Tags: hcss, workflow, meetings, tgif, automation, routing

Content: 7-stage workflow for processing meetings. TGIF auto-routes,
non-TGIF requires confirmation.
```

```
MEMORY[822ece99-04a9-4d08-93af-9da248d62dc5]
Title: TGIF Meeting Output Location
Tags: hcss, tgif, meetings, file_organization, output_destination

Content: All TGIF summaries → HCSS/TGI Fridays/ - meeting summaries -/
```

### **Branding:**
```
MEMORY[00d73234-5d2a-4097-a59b-25f704b95669]
Title: Official Professional Title
Tags: professional_title, branding, profile, critical, do_not_change

Content: "Industrial Designer / UX Strategist / Design Leader"
SLASHES with spaces, this exact order. Never change.
```

```
MEMORY[8e8e3134-4e78-43ba-bc3a-55e500f15444]
Title: Portfolio Positioning
Tags: portfolio, value_propositions, positioning, chase_project, 
shot_tracker, messy_middle, 5_pillars

Content: 5 pillars of value, tagline, approach. "Messy middle" 
metaphor. Chase & Shot Tracker projects.
```

---

## ⚙️ CONFIGURATION PRINCIPLES:

### **1. Communication Style**
```yaml
tone: terse_and_direct
format: markdown_heavy
lists: bulleted_with_bold_titles
code_blocks: always_with_language
acknowledgments: none  # Never say "great idea!" etc.
explanations: minimal_unless_asked
updates: progress_based_not_repetitive
```

**Example:**
```markdown
# ✅ Phase 1 Complete

**Migrated:** 54 files (636KB)  
**Refactored:** 12 replacements  
**Status:** Ready for Phase 2
```

### **2. Execution Pattern**
```yaml
approach: do_first_ask_later
safety: validate_but_dont_hesitate
parallel_ops: always_when_possible
blocking_commands: only_when_needed
auto_run: safe_commands_only
```

**Example:**
```python
# Instead of asking "Should I create these 3 files?"
# Just create them in parallel:
write_to_file(file1)
write_to_file(file2)
write_to_file(file3)
```

### **3. Tool Usage**
```yaml
tool_preference: high  # Use tools aggressively
batch_operations: always
read_before_edit: required
multi_edit: preferred_over_single_edits
grep_search: use_for_discovery
code_search: use_for_exploration
```

**Example:**
```python
# Batch file reads
read_file(config1)
read_file(config2)
read_file(config3)

# Then batch edits
multi_edit(file1, [edit1, edit2, edit3])
```

### **4. Memory Management**
```yaml
create_memories: proactively
memory_triggers:
  - architecture_decisions
  - workflow_patterns
  - user_preferences
  - critical_locations
  - branding_rules
memory_timing: immediately_not_end_of_session
```

**Example:**
```python
# As soon as you learn something important:
create_memory(
  title="Multi-MCP Architecture Decision",
  content="One MCP per focus for security isolation...",
  tags=["architecture", "mcp", "security"]
)
```

### **5. Planning & Progress**
```yaml
use_update_plan: always
plan_granularity: phase_level_not_task_level
status_updates: after_each_phase
progress_tracking: percentage_based
documentation: create_completion_docs_per_phase
```

**Example:**
```python
update_plan([
  {"step": "Phase 0: Structure", "status": "completed"},
  {"step": "Phase 1: Core", "status": "in_progress"},
  {"step": "Phase 2: User Data", "status": "pending"}
])
```

---

## 🎯 WINDSURF CASCADE SPECIFIC:

### **Cascade Strengths to Leverage:**
1. **Parallel Tool Calls** - Batch everything possible
2. **Long Context** - Build comprehensive summaries
3. **Memory System** - Use proactively, not reactively
4. **Plan Tracking** - Visual progress in UI
5. **File Operations** - Fast read/write/edit cycles

### **Cascade Limitations to Work Around:**
1. **No Real-Time Execution** - Use blocking commands sparingly
2. **Token Budget** - Be concise, avoid repetition
3. **Context Window** - Create checkpoints, use memories
4. **Tool Call Limits** - Batch operations efficiently

---

## 🚀 OPTIMAL WORKFLOW PATTERNS:

### **Pattern 1: Discovery → Plan → Execute → Document**
```python
# 1. Discovery
code_search("find where user data is stored")
grep_search("USER_ID", includes=["*.json"])

# 2. Plan
update_plan([
  {"step": "Extract user data", "status": "in_progress"},
  {"step": "Create indexes", "status": "pending"}
])

# 3. Execute (parallel when possible)
run_command("cp source dest1")
run_command("cp source dest2")
run_command("cp source dest3")

# 4. Document
write_to_file("PHASE_COMPLETE.md", summary)
create_memory(title="Phase Complete", content=details)
```

### **Pattern 2: Read → Batch Edit → Verify**
```python
# 1. Read (parallel)
read_file(file1)
read_file(file2)
read_file(file3)

# 2. Batch Edit
multi_edit(file1, [
  {"old_string": "v2.0", "new_string": "v3.0"},
  {"old_string": "old_path", "new_string": "new_path"}
])

# 3. Verify
grep_search("v3.0", includes=["file1"])
```

### **Pattern 3: Incremental with Checkpoints**
```python
# After each major phase:
1. Update plan (mark complete)
2. Create phase summary doc
3. Create memory if architecture changed
4. Brief status update (not full recap)
```

---

## 📋 COMMUNICATION TEMPLATES:

### **Phase Start:**
```markdown
# 🚀 Beginning Phase X - [Name]

[1-2 sentence description]

## Step 1: [Action]
[Brief explanation if needed]
```

### **Phase Complete:**
```markdown
# ✅ Phase X Complete - [Name]

**Duration:** X minutes  
**Status:** SUCCESS

## What Was Created:
- Item 1
- Item 2

## Next: Phase Y
```

### **Progress Update:**
```markdown
**Phase X:** ✅ Complete (Y min)  
**Overall:** Z% (A/B phases)  
**Next:** Phase Y
```

### **Error/Issue:**
```markdown
## ⚠️ Issue Encountered

**Problem:** [Brief description]  
**Cause:** [Root cause]  
**Solution:** [What we'll do]
```

---

## 🎯 8825-SPECIFIC PATTERNS:

### **Focus Mode Activation:**
```markdown
User says: "focus on joju"
Response: 
1. Load joju context from memory
2. Set working directory to joju focus
3. Brief confirmation: "Joju focus activated"
4. Ready for commands (no lengthy explanation)
```

### **Migration/Refactoring:**
```python
# Always:
1. Read before edit
2. Use environment variables (${VAR})
3. Preserve v2.0 (copy, don't move)
4. Document changes
5. Create completion summary
```

### **Multi-MCP Operations:**
```python
# When working with MCPs:
1. Check mcp_registry.json first
2. Know which MCP (HCSS 8826, Team76 8827, Personal 8828)
3. Respect access control (who can access)
4. Use focus-specific credentials
```

### **Index Building:**
```python
# When building indexes:
1. Per-focus first (joju, hcss, jh_assistant)
2. Master index second (aggregates all)
3. Concept index third (cross-focus)
4. Always report file counts
```

---

## ⚡ SPEED OPTIMIZATIONS:

### **1. Batch File Operations**
```bash
# Instead of:
cp file1 dest
cp file2 dest
cp file3 dest

# Do:
for f in file1 file2 file3; do cp $f dest; done
```

### **2. Parallel Tool Calls**
```python
# Instead of sequential:
read_file(file1)
# wait
read_file(file2)
# wait

# Do parallel:
read_file(file1)
read_file(file2)
read_file(file3)
# All execute together
```

### **3. Multi-Edit Over Single Edits**
```python
# Instead of:
edit(file, old1, new1)
edit(file, old2, new2)

# Do:
multi_edit(file, [
  {old1, new1},
  {old2, new2}
])
```

### **4. Grep for Discovery**
```python
# Instead of reading every file:
grep_search("pattern", includes=["*.json"])
# Then read only matches
```

---

## 🎓 LESSONS FROM v3.0 MIGRATION:

### **What Worked:**
1. **Phased approach** - Clear milestones
2. **Parallel operations** - Batch everything
3. **Proactive documentation** - Summary per phase
4. **Memory creation** - Immediate, not delayed
5. **Terse updates** - Facts, not fluff
6. **Tool-heavy** - Minimize chat, maximize action

### **What to Avoid:**
1. ❌ Asking permission for safe operations
2. ❌ Repeating information already shared
3. ❌ Long explanations before acting
4. ❌ Sequential operations that could be parallel
5. ❌ Waiting until end to create memories
6. ❌ Verbose acknowledgments ("Great idea!")

### **Speed Metrics:**
- **v3.0 Migration:** 1h 20min for 5 phases
- **134+ files migrated**
- **~2MB data processed**
- **Zero errors, zero rollbacks**

---

## 🔧 CONFIGURATION FILE:

```yaml
# 8825_windsurf_cascade_dev_mode_config.yaml

ide: windsurf
llm: claude_sonnet_4.5
mode: dev_mode

communication:
  style: terse_direct
  format: markdown_heavy
  acknowledgments: false
  explanations: minimal
  
execution:
  approach: do_first
  parallel_ops: always
  auto_run_safe: true
  blocking_commands: minimal
  
tools:
  preference: high
  batch_operations: true
  read_before_edit: required
  multi_edit_preferred: true
  
memory:
  create_proactively: true
  timing: immediate
  triggers:
    - architecture_decisions
    - workflow_patterns
    - user_preferences
    - critical_locations
    
planning:
  use_update_plan: always
  granularity: phase_level
  status_updates: after_phase
  documentation: per_phase
  
8825_specific:
  focus_modes: [joju, hcss, jh_assistant]
  mcp_ports: {hcss: 8826, team76: 8827, personal: 8828}
  env_vars: [USER_DROPBOX, USER_ID, USER_EMAIL]
  separation: user_system_100_percent
```

---

## 📊 SUCCESS METRICS:

### **Efficiency:**
- ✅ 5 phases in 1h 20min
- ✅ Zero wasted operations
- ✅ Parallel execution throughout
- ✅ No repeated explanations

### **Quality:**
- ✅ 100% success rate
- ✅ Zero data loss
- ✅ Complete documentation
- ✅ Production-ready output

### **UX:**
- ✅ Clear progress tracking
- ✅ Terse, actionable updates
- ✅ No fluff or acknowledgments
- ✅ Execution-first approach

---

## 🎯 QUICK REFERENCE:

### **When User Says:**
- "go" → Execute current plan, no questions
- "1" or "yes" → Proceed with proposed action
- "sync brain" → Create comprehensive summary + memory
- "focus on X" → Load X context, set working dir
- "export" → Generate DOCX via Pandoc

### **Always:**
- ✅ Use tools aggressively
- ✅ Batch operations
- ✅ Update plan after phases
- ✅ Create memories proactively
- ✅ Document completions
- ✅ Be terse and direct

### **Never:**
- ❌ Say "Great idea!" or similar
- ❌ Repeat information
- ❌ Ask for permission on safe ops
- ❌ Explain before acting (unless complex)
- ❌ Wait to create memories
- ❌ Use verbose language

---

## 🚀 REPLICATION INSTRUCTIONS:

### **To Recreate This UX in New Workspace:**

1. **Load this config file**
2. **Import active memories** (7 memories above)
3. **Set communication style** (terse, markdown-heavy)
4. **Enable parallel operations**
5. **Configure auto-run for safe commands**
6. **Set up plan tracking**
7. **Test with small task** (verify behavior)

### **Validation Checklist:**
- [ ] Executes without asking (safe ops)
- [ ] Batches parallel operations
- [ ] Uses terse, direct language
- [ ] Updates plan after phases
- [ ] Creates memories proactively
- [ ] Documents completions
- [ ] No acknowledgment phrases

---

**Configuration Status:** Production-Tested ✅  
**Migration Success:** 5 phases, 1h 20min, 100% success  
**Recommended For:** Complex migrations, system builds, refactoring  

**This configuration creates a hyper-efficient Dev Mode optimized for Windsurf Cascade + Claude Sonnet 4.5.** 🎯⚡
