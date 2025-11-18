# Task Types Reference Guide

**Quick definitions for the 6 task types in classification protocol**

---

## 📋 The 6 Task Types

### 1️⃣ **One-Off Task**

**What it is:**  
Something you do once and never need again.

**Key characteristics:**
- Single execution
- No repeatability needed
- Minimal documentation
- Fast and direct

**Examples:**
- "Fix this specific bug"
- "Export this data to CSV"
- "Answer this question"
- "Convert this file format"
- "Look up this information"

**Time:** Minutes to 1 hour  
**Output:** Just the result  
**Approach:** Do it fast, move on

---

### 2️⃣ **Repeatable Workflow**

**What it is:**  
A manual process you'll do again, following documented steps.

**Key characteristics:**
- Human executes each time
- Steps documented
- Checklist or runbook
- Commands saved for reuse

**Examples:**
- "Process weekly meeting notes"
- "Generate monthly report"
- "Onboard new team member"
- "Deploy to staging"
- "Review and merge PRs"

**Time:** 1-2 hours (includes documenting)  
**Output:** Result + "How to do this again" docs  
**Approach:** Do it, document it, make it repeatable

---

### 3️⃣ **Pipeline**

**What it is:**  
An automated sequence of steps that runs without human intervention.

**Key characteristics:**
- Fully automated
- Error handling
- Monitoring/logging
- Scheduled or triggered
- No decision-making (just execution)

**Examples:**
- "Auto-process Otter transcripts from Gmail"
- "Daily data sync between systems"
- "Nightly backup script"
- "CI/CD deployment pipeline"
- "Automated report generation"

**Time:** 4-8 hours (includes edge cases)  
**Output:** Working code + docs + tests  
**Approach:** Build robust, handle failures, monitor

**Key difference from Agent:** Pipeline follows fixed steps. No decisions.

---

### 4️⃣ **Protocol**

**What it is:**  
A standardized methodology or approach that guides how to do something.

**Key characteristics:**
- Defines "how we do X"
- Principles and rules
- Checklists and criteria
- Enforcement mechanisms
- Not code - guidance

**Examples:**
- "POC Promotion Criteria"
- "Definition of Done"
- "Code review standards"
- "Incident response protocol"
- "Security review checklist"

**Time:** 2-4 hours  
**Output:** Protocol doc + examples + checklists  
**Approach:** Define principles, create structure, document patterns

**Key difference from Pattern:** Protocol is prescriptive (must follow). Pattern is descriptive (can adapt).

---

### 5️⃣ **Pattern**

**What it is:**  
A reusable solution to a common problem, abstracted from specific implementations.

**Key characteristics:**
- Abstracted from real examples
- Reusable across contexts
- Principles + implementation guidance
- Adaptable to specific needs
- Documents "what worked"

**Examples:**
- "Downloads workflow pattern" (export → detect → process → archive)
- "Context loading pattern" (search multiple sources with fallback)
- "API key management pattern" (primary → backup → fallback)
- "Self-correcting system pattern"
- "Dual-source strategy pattern"

**Time:** 1-2 hours  
**Output:** Pattern doc + implementation examples  
**Approach:** Abstract from specifics, document principles, show examples

**Key difference from Protocol:** Pattern is flexible guidance. Protocol is strict rules.

---

### 6️⃣ **Agent**

**What it is:**  
An autonomous system that makes decisions and takes actions based on conditions.

**Key characteristics:**
- Makes decisions (if/then logic)
- Autonomous operation
- Self-correcting
- Monitoring and alerts
- Handles unexpected situations

**Examples:**
- "Meeting processor agent" (decides how to handle different email types)
- "Ingestion router agent" (routes files based on content)
- "Auto-triage support tickets"
- "Smart notification system"
- "Adaptive learning system"

**Time:** 1-2 days  
**Output:** Agent code + decision trees + monitoring + comprehensive docs  
**Approach:** Build decision logic, extensive testing, monitoring, self-correction

**Key difference from Pipeline:** Agent makes decisions. Pipeline just executes.

---

## 🔄 Evolution Path

Tasks often evolve through these stages:

```
One-Off Task
    ↓ "I need to do this again"
Repeatable Workflow
    ↓ "This is tedious, automate it"
Pipeline
    ↓ "It needs to handle different cases"
Agent
```

**Example: Meeting Automation**
1. **One-Off:** "Process this transcript with GPT-4"
2. **Workflow:** "Here's how to process transcripts weekly"
3. **Pipeline:** "Auto-fetch from Gmail and process"
4. **Agent:** "Handle promotional emails, duplicates, empty transcripts, different formats"

---

## 🎯 Quick Classification

### Ask yourself:

**"Will I do this again?"**
- No → **One-Off**
- Yes, manually → **Workflow**
- Yes, automatically → **Pipeline** or **Agent**

**"Does it make decisions?"**
- No → **Pipeline**
- Yes → **Agent**

**"Am I defining how to do something?"**
- Yes, strict rules → **Protocol**
- Yes, flexible guidance → **Pattern**
- No → **Task/Workflow/Pipeline/Agent**

---

## 📊 Comparison Table

| Type | Automated? | Decisions? | Repeatable? | Time | Output |
|------|------------|------------|-------------|------|--------|
| **One-Off** | No | No | No | Minutes | Result only |
| **Workflow** | No | No | Yes (manual) | 1-2 hrs | Result + docs |
| **Pipeline** | Yes | No | Yes (auto) | 4-8 hrs | Code + docs |
| **Protocol** | N/A | N/A | N/A | 2-4 hrs | Methodology |
| **Pattern** | N/A | N/A | N/A | 1-2 hrs | Reusable solution |
| **Agent** | Yes | Yes | Yes (auto) | 1-2 days | Smart system |

---

## 💡 Real-World Examples

### One-Off Task
> "Export the meeting summary as a Word doc"
- Do once, done
- Use pandoc, verify, complete
- No need to document

### Repeatable Workflow
> "Process weekly TGIF meetings"
- Manual steps each week
- Document: fetch email → extract → process → save
- Save commands for reuse

### Pipeline
> "Auto-process all Otter transcripts"
- Runs automatically
- Polls Gmail → processes → saves
- Error handling, logging
- No human intervention

### Protocol
> "Definition of Done checklist"
- Defines when something is "done"
- 5 criteria to check
- Must follow for all production work
- Not code - guidance

### Pattern
> "Downloads workflow pattern"
- User exports → system detects → auto-processes → archives
- Reusable across different file types
- Principles documented, adaptable

### Agent
> "Meeting processor with smart routing"
- Detects promotional emails → skips
- Finds duplicates → deduplicates
- Empty transcript → flags for manual export
- Different formats → adapts processing
- Makes decisions autonomously

---

## 🚩 Common Misclassifications

### ❌ "Build a script" ≠ Always a Pipeline
- If you run it manually each time → **Workflow**
- If it runs automatically → **Pipeline**

### ❌ "Automate X" ≠ Always an Agent
- If it follows fixed steps → **Pipeline**
- If it makes decisions → **Agent**

### ❌ "Document how we do X" ≠ Always a Protocol
- If it's strict rules → **Protocol**
- If it's flexible guidance → **Pattern**
- If it's just instructions → **Workflow**

### ❌ "I'll do this weekly" ≠ Always a Workflow
- If you want to automate → **Pipeline**
- If you'll do manually → **Workflow**

---

## 🎓 When in Doubt

**Start smaller, evolve bigger:**
- Unsure? Start as **One-Off**
- After completion, ask: "Make repeatable?"
- Upgrade classification as needs grow

**Better to under-classify than over-engineer:**
- One-Off that becomes Workflow → Easy upgrade
- Pipeline built for One-Off → Wasted effort

**Let the task tell you:**
- If you're writing "if this, then that" → Probably an **Agent**
- If you're writing "step 1, step 2, step 3" → Probably a **Pipeline** or **Workflow**
- If you're writing "always do X when Y" → Probably a **Protocol**
- If you're writing "here's a pattern that works" → Probably a **Pattern**

---

## 📖 Full Details

For comprehensive classification guidance, see:
- `TASK_CLASSIFICATION_PROTOCOL.md` - Full protocol with questions, examples, cost models
- `WORKFLOW_ORCHESTRATION_PROTOCOL.md` - How classification fits into overall workflow

---

**Remember:** Classification isn't about being perfect. It's about understanding scope before diving in.

**30 seconds of classification saves 30 minutes of rework.**
