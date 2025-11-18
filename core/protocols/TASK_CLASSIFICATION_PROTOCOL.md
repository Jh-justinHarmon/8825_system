# Task Classification Protocol

**Purpose:** Help users identify what they're actually building before diving in

**Problem:** Users (including experienced ones) often jump into execution without clarifying scope, leading to rework when a "one-off task" needs to become repeatable.

---

## Task Types (Ordered by Complexity)

### 1. **One-Off Task**
**Definition:** Single execution, no need to repeat  
**Examples:** "Fix this bug," "Export this data," "Answer this question"  
**Approach:** Direct execution, minimal documentation  
**Cost Model:** Fast LLM for execution  
**Output:** Result only  
**Time to Complete:** Minutes to hours

### 2. **Repeatable Workflow**
**Definition:** Manual process that will be done again (by human)  
**Examples:** "Process meeting notes," "Generate weekly report"  
**Approach:** Document steps, create checklist, save commands  
**Cost Model:** Fast LLM for execution, document process  
**Output:** Result + instructions for next time  
**Time to Complete:** 1-2 hours (includes documentation)

### 3. **Pipeline**
**Definition:** Automated sequence of steps (programmatic)  
**Examples:** "Auto-process Otter transcripts," "Daily data sync"  
**Approach:** Build scripts, error handling, monitoring  
**Cost Model:** High-end LLM for design, fast LLM for execution  
**Output:** Working code + documentation + tests  
**Time to Complete:** 4-8 hours (includes edge cases)

### 4. **Protocol**
**Definition:** Standardized approach/methodology to be followed  
**Examples:** "POC promotion criteria," "Definition of done"  
**Approach:** Define principles, create checklists, document patterns  
**Cost Model:** High-end LLM for design and validation  
**Output:** Markdown protocols + examples + enforcement mechanisms  
**Time to Complete:** 2-4 hours

### 5. **Pattern**
**Definition:** Reusable solution to a common problem  
**Examples:** "Downloads workflow pattern," "Context loading pattern"  
**Approach:** Abstract from specific implementation, document principles  
**Cost Model:** High-end LLM for abstraction  
**Output:** Pattern documentation + implementation examples  
**Time to Complete:** 1-2 hours

### 6. **Agent**
**Definition:** Autonomous system that makes decisions and acts  
**Examples:** "Meeting processor agent," "Ingestion router agent"  
**Approach:** Build decision logic, monitoring, self-correction  
**Cost Model:** High-end LLM for design, extensive testing  
**Output:** Agent code + decision trees + monitoring + docs  
**Time to Complete:** 1-2 days

---

## Classification Questions (Ask Upfront)

When a user presents a task, ask:

### **Q1: Will this be done more than once?**
- No → One-Off Task
- Yes, manually → Repeatable Workflow
- Yes, automatically → Pipeline or Agent

### **Q2: Who is the end user?**
- Just me, right now → One-Off Task
- Me, in the future → Repeatable Workflow
- Other users → Pipeline/Protocol/Agent

### **Q3: Does it need to handle edge cases?**
- No → One-Off Task or Workflow
- Yes → Pipeline or Agent

### **Q4: Does it make decisions?**
- No → Pipeline
- Yes → Agent

### **Q5: Is this defining how to do something?**
- Yes → Protocol or Pattern
- No → Task/Workflow/Pipeline/Agent

---

## Completion Check (Ask at End)

When a one-off task or workflow is complete, ask:

> **"This works for now. Do you want to make this repeatable?"**

Options:
- **No** → Mark as complete, minimal docs
- **Yes, manual** → Create workflow documentation
- **Yes, automated** → Design pipeline
- **Yes, for others** → Build agent/protocol

---

## Cost Model Decision Tree

```
Planning/Brainstorming
    ↓
High-End LLM (GPT-4, Claude Opus)
    ↓
Deep Context Search
    ↓
Fast LLM (GPT-4 Turbo, Claude Sonnet)
    ↓
Execution
    ↓
Fast LLM (GPT-4 Turbo)
    ↓
Documentation
    ↓
Fast LLM (GPT-4 Turbo)
```

**Exception:** If hitting a wall, return to High-End LLM for redesign

---

## Red Flags (When to Stop and Reclassify)

### 🚩 **"Wait, I need to do this again next week"**
→ Stop. Reclassify as Repeatable Workflow or Pipeline

### 🚩 **"What if the input format changes?"**
→ Stop. Add error handling. Consider Pipeline.

### 🚩 **"Other people will use this"**
→ Stop. Reclassify as Pipeline or Agent. Build proper docs.

### 🚩 **"This keeps breaking"**
→ Stop. Missing edge cases. Upgrade to Pipeline with monitoring.

### 🚩 **"I'm explaining this for the third time"**
→ Stop. Create Protocol or Pattern documentation.

---

## Examples from Recent Work

### **Meeting Automation (Evolved from One-Off to Agent)**

**Started as:** One-off task ("Process this meeting transcript")  
**Became:** Repeatable workflow ("Process meetings weekly")  
**Evolved to:** Pipeline ("Auto-process from Gmail")  
**Enhanced to:** Agent ("Handle edge cases, Downloads workflow")

**Lesson:** Would have saved 50% time if classified as Pipeline upfront

### **Downloads Workflow (Pattern)**

**Started as:** One-off fix ("Process these 2 txt files")  
**Became:** Pattern ("Auto-detect exported transcripts")  
**Result:** Reusable solution for "empty email body" problem

**Lesson:** Recognizing it as a pattern saved future rework

---

## Integration with Existing Protocols

### **POC Promotion Criteria** (Protocol)
Use for validating Pipelines and Agents before production

### **Definition of Done** (Protocol)
Apply to all task types except One-Offs

### **PromptGen** (Pattern)
Use during brainstorming phase for all task types

---

## User Learning Notes

**Justin's Pattern (from recent sessions):**
- Tends to jump into execution
- Realizes classification need when hitting a wall
- Benefits from upfront classification questions
- Prefers iterative approach (one-off → workflow → pipeline)

**Optimization:**
Ask classification questions upfront, even if user jumps straight in

---

## Quick Reference

| Task Type | Repeat? | Users | Decisions | Time | Cost Model |
|-----------|---------|-------|-----------|------|------------|
| One-Off | No | Just me | No | Minutes | Fast LLM |
| Workflow | Manual | Me later | No | 1-2 hrs | Fast LLM + docs |
| Pipeline | Auto | Me/Others | Limited | 4-8 hrs | High-end design + Fast exec |
| Protocol | N/A | Everyone | Guidelines | 2-4 hrs | High-end |
| Pattern | N/A | Developers | Principles | 1-2 hrs | High-end |
| Agent | Auto | Anyone | Yes | 1-2 days | High-end + extensive testing |

---

**Remember:** It's okay to start as One-Off and evolve. But asking the classification questions upfront saves rework.
