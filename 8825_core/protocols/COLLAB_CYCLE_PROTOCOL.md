# Collaborative Dev Cycle Protocol

**Purpose:** Structured workflow for ideation → research → planning → execution  
**Created:** November 14, 2025  
**Trigger:** User uses collab phrases or signals new dev cycle intent

---

## Problem This Solves

**Before:** User says "I have an idea" → LLM responds differently each time → inconsistent depth, missed protocols, no pause for model switching, unclear execution steps

**After:** Consistent 6-phase cycle that collects context, pauses for thinking model, provides teach-me explanations, and delivers clear executable plan

---

## Trigger Detection

### **Explicit Triggers:**
- `[collab]`
- `[collab sesh]`
- `[collab session]`
- `[LFG]`
- `[let's make]`

### **Implicit Triggers:**
- "I have an idea to flush out"
- "want to figure something out"
- "thinking about building..."
- "should we create..."
- Any phrase signaling **new dev cycle initiation**

### **Intent Recognition:**
User is signaling: We're about to create or enter into something new that requires structured thinking

---

## The 6-Phase Cycle

### **Phase 1: Breadcrumb Collection** 📋

**Goal:** Gather ALL relevant context before starting

**What to collect:**
1. **Protocols** - Deep Dive, PromptGen, Decision Matrix, Proof Protocol, Workflow Orchestration
2. **Philosophies** - PHILOSOPHY.md principles, Proof Protocol patterns
3. **Patterns** - Existing workflows, team execution protocols
4. **Constraints** - Known limitations, technical requirements
5. **Previous Work** - Related implementations, learnings

**Output:** 
```
## 📋 BREADCRUMB TRAIL COLLECTED

**Protocols Found:**
1. Protocol Name - Brief description
2. ...

**Philosophies:**
- Philosophy principle - How it applies

**Patterns:**
- Pattern name - Relevance

**Constraints:**
- Known limitation - Impact
```

**Time Box:** 2-3 minutes

---

### **Phase 2: Deep Dive Context** 🔍

**Goal:** Pull additional strings if breadcrumbs suggest more exists

**Questions to ask:**
- Are there related protocols we missed?
- Do any breadcrumbs reference other systems?
- Are there archived implementations worth reviewing?
- Do logs show previous attempts?

**Decision Point:**
- 🟢 **Sufficient context** → Move to Phase 3
- 🟡 **Need more** → Pull additional strings
- 🔴 **Missing critical info** → Ask user before proceeding

**Output:**
```
## 🔍 ADDITIONAL CONTEXT

**Pulled strings:**
- String 1 - What we found
- String 2 - Relevance

**Status:** ✅ Complete picture OR ⚠️ Still missing: [what]
```

**Time Box:** 3-5 minutes (or skip if context is sufficient)

---

### **Phase 3: Brainstorm & Analysis** 🎨

**Goal:** Apply structured thinking to generate comprehensive plan

**Apply in order:**

#### **3.1 PromptGen Analysis**

Run through 8-step PromptGen checklist:

1. **Problem Definition**
   - Core need
   - Pain point
   - If not solved
   - Minimum viable

2. **Context Gathering**
   - Existing solutions
   - Patterns used before
   - Known constraints
   - Current state

3. **Requirements (Explicit)**
   - MUST have
   - SHOULD have
   - NICE to have

4. **Requirements (Implicit)**
   - Who uses this
   - Where it runs
   - When used
   - How often

5. **Constraints**
   - Technical
   - Time
   - Cost
   - User

6. **Edge Cases**
   - Data issues
   - API failures
   - User errors
   - Unexpected inputs

7. **Success Criteria**
   - Definition of done
   - Metrics
   - Acceptance test
   - Validation method

8. **Failure Modes**
   - How to fail gracefully
   - Error handling
   - Recovery
   - Data safety

#### **3.2 Decision Matrix**

**Choose optimization mode:**
- **Results-Driven** - Fast iteration, optimize for speed
- **User-Driven** - Long-term use, optimize for ease

**Based on:**
- Task type (one-off vs repeatable)
- User count (just me vs others)
- Reuse frequency (once vs often)

💡 **TEACH ME:** Explain WHY this mode was chosen

#### **3.3 Synthesized Analysis**

**Output Format:**
```
## 🎨 BRAINSTORM & ANALYSIS

### PromptGen Summary
[Key findings from 8 steps]

### 🎯 DECISION: [Chosen Approach]
💡 **TEACH ME:** [Why this approach over alternatives]

### Options Considered
1. Option A - Pros/Cons
2. Option B - Pros/Cons
3. **✅ Chosen: Option C** - Why

### Implementation Philosophy
⚙️ **IMPLEMENTATION:** [How the pieces fit together]

### Known Gotchas
⚠️ **GOTCHA:** [Common mistakes to avoid]
```

**Time Box:** 5-10 minutes

---

### **Phase 4: ⏸️ PAUSE for Model Switch**

**Goal:** Stop for user to switch to thinking model for detailed planning

**Output:**
```
## ⏸️ PAUSE - READY FOR DETAILED PLANNING

All context collected. Brainstorm complete.

**Switch to thinking model (o1/o1-mini) for:**
- Detailed step-by-step execution plan
- Edge case handling
- Test plan design
- Rollback procedures

**Resume when ready.**
```

**Action:** Wait for user to say "continue" or "go" after model switch

---

### **Phase 5: Detailed Planning** 📝

**Goal:** Create step-by-step execution plan with teach-me explanations

**Output Format:**
```
## 📝 DETAILED EXECUTION PLAN

### Overview
[High-level summary of what we're building]

### Step-by-Step Implementation

#### Step 1: [Action]
⚙️ **IMPLEMENTATION:** [How this works]
💡 **TEACH ME:** [Why we're doing it this way]

**Files to create/modify:**
- File 1: Purpose
- File 2: Purpose

**Commands:**
```bash
# Command with explanation
```

#### Step 2: [Action]
...

[Repeat for each step]

### Integration Points
🔗 **CONNECTIONS:**
- System A → How it connects
- System B → Data flow

### Verification Steps
✅ **SUCCESS METRICS:**
1. Check 1 - Expected result
2. Check 2 - Expected result
3. Check 3 - Expected result

### Common Issues
⚠️ **GOTCHAS:**
1. Issue - How to avoid/fix
2. Issue - How to avoid/fix

### Rollback Plan
If something goes wrong:
1. Step to undo
2. Step to restore
3. Verification
```

**Time Box:** 10-15 minutes (with thinking model)

---

### **Phase 6: Execution** ⚡

**Goal:** Implement the plan with clear instructions and testing

**Execution Phases:**

#### **6.1 Pre-Flight Check**
```
## ✅ PRE-FLIGHT CHECKLIST

- [ ] All dependencies available
- [ ] Backups created (if modifying existing)
- [ ] Dry-run successful (if applicable)
- [ ] User approved plan
```

#### **6.2 Implementation**

Execute step-by-step from Phase 5 plan.

**Progress reporting:**
```
[1/5] Creating workflow file... ✅
[2/5] Writing protocol documentation... ✅
[3/5] Updating memory... ✅
[4/5] Running tests... ⏳
[5/5] Verifying integration... 
```

#### **6.3 Testing**

**Test depth based on confidence:**

**High Confidence (95%+):**
- Basic smoke tests
- Happy path verification
- Quick manual check

**Medium Confidence (70-94%):**
- Smoke tests
- Edge case testing
- Integration verification
- User acceptance test

**Low Confidence (<70%):**
- Full test suite
- Multiple edge cases
- Stress testing
- User walkthrough required

#### **6.4 Completion Report**

```
## ✅ EXECUTION COMPLETE

### What Was Built
1. File/Component - Purpose
2. File/Component - Purpose

### Verification Results
✅ Test 1: Passed
✅ Test 2: Passed
✅ Test 3: Passed

### Next Steps
1. Action user should take
2. Optional improvement
3. Documentation to read

### Success Metrics
How to know it's working:
- Metric 1
- Metric 2
- Metric 3
```

---

## Teaching Mode Markers

### **Emoji Guide:**

💡 **TEACH ME** - Explains WHY  
*Use when:* Explaining reasoning, philosophy, decision rationale

🎯 **DECISION** - Explains WHAT and WHY  
*Use when:* Announcing chosen approach, explaining trade-offs

⚙️ **IMPLEMENTATION** - Explains HOW  
*Use when:* Describing technical details, architecture, mechanisms

⚠️ **GOTCHA** - Warns about pitfalls  
*Use when:* Highlighting common mistakes, edge cases, known issues

✅ **SUCCESS METRIC** - Defines verification  
*Use when:* Explaining how to validate, test, or confirm success

### **Placement Guidelines:**

- **1 teach-me marker per major section** (don't overuse)
- **Place at decision points** (when user needs to understand)
- **Keep explanations SHORT** (2-3 sentences max)
- **Make visually obvious** (emoji at start of line)

---

## Protocol Integration

### **Called Protocols:**

1. **Deep Dive Research Protocol** (Phase 1-2)
   - 6-phase discovery
   - Cast wide net
   - Trust but verify

2. **PromptGen Integration** (Phase 3)
   - 8-step checklist
   - Comprehensive planning
   - Edge case identification

3. **Decision Matrix** (Phase 3)
   - Results vs User-Driven
   - Optimization target selection
   - Trade-off analysis

4. **Workflow Orchestration** (Overall flow)
   - Task classification
   - Context search
   - Mode selection

5. **Proof Protocol** (After completion)
   - Track usage
   - Record success/failure
   - Apply decay rules

6. **Teaching Mode Config** (Explanation style)
   - Plain language
   - Analogies
   - Check understanding

---

## Override Options

### **Skip Phases:**

User can say:
- "Skip breadcrumbs, I know the context"
- "Skip brainstorm, go to planning"
- "Skip pause, use current model"
- "Execute immediately" (jumps to Phase 6)

### **Adjust Depth:**

- 🟢 **Calm mode** - Full protocols, all phases
- 🟡 **Urgent mode** - Streamlined, skip optional steps
- 🔴 **Frustrated mode** - Infer and execute, minimal process

### **Change Model:**

- "Use thinking model for whole cycle" (no pause)
- "Stay with fast model" (skip model switch)
- "Switch now" (pause early)

---

## Success Metrics

### **Good Collab Cycle:**

✅ All relevant context collected  
✅ User understands the approach (teach-me explanations landed)  
✅ Comprehensive plan before execution  
✅ Edge cases identified upfront  
✅ Clear success criteria defined  
✅ Implementation works as planned  
✅ User says "yes, that's exactly what I wanted"

### **Poor Collab Cycle:**

❌ Jumped to execution without context  
❌ User confused by approach  
❌ Hit edge case during implementation  
❌ Unclear what "done" looks like  
❌ Rework needed after initial build  
❌ User says "wait, I meant something different"

---

## Time Investment vs ROI

### **Time Investment:**
- Phase 1: 2-3 minutes (breadcrumbs)
- Phase 2: 3-5 minutes (deep dive)
- Phase 3: 5-10 minutes (brainstorm)
- Phase 4: 0 minutes (user switches model)
- Phase 5: 10-15 minutes (planning)
- Phase 6: Variable (execution)

**Total overhead:** 20-33 minutes of planning

### **Time Saved:**
- Avoiding rework: 60-180 minutes
- Catching edge cases early: 30-60 minutes
- Clear requirements: 15-30 minutes
- Proper testing: 15-30 minutes
- Future reuse: ∞ minutes

**ROI:** Planning pays for itself immediately, prevents "we've tried this X times" scenarios

---

## Example Session Flow

### **User Input:**
```
[collab] I want to build a system that recognizes when I say certain phrases 
and automatically triggers a structured workflow
```

### **Phase 1 - Breadcrumbs:**
```
📋 BREADCRUMB TRAIL COLLECTED

**Protocols Found:**
1. Workflow Orchestration - Structured task flow
2. Deep Dive Research - Systematic discovery
3. PromptGen - Comprehensive planning

**Patterns:**
- Windsurf workflows with // turbo annotations
- Trigger phrase detection
- LLM model switching
```

### **Phase 2 - Deep Dive:**
```
🔍 ADDITIONAL CONTEXT

Found existing `/launch-8825` workflow - pattern to follow
Found teaching mode markers system - can use for explanations
Status: ✅ Complete picture
```

### **Phase 3 - Brainstorm:**
```
🎨 BRAINSTORM & ANALYSIS

**PromptGen Summary:**
- Problem: Inconsistent dev cycle initiation
- Solution: Structured workflow with trigger detection
- Requirements: Works across LLMs, pause for model switch, teach-me markers

🎯 **DECISION:** Create workflow + protocol hybrid
💡 **TEACH ME:** Workflow handles trigger detection, protocol defines the actual process. 
This way the workflow is simple and the protocol is comprehensive.

**Options Considered:**
1. Simple workflow only - Too basic, no guidance
2. Complex agent - Overkill, hard to maintain
3. ✅ **Workflow + Protocol** - Right balance of automation and documentation
```

### **Phase 4 - Pause:**
```
⏸️ PAUSE - READY FOR DETAILED PLANNING
Switch to thinking model for execution plan.
```

### **Phase 5 - Detailed Plan:**
```
📝 DETAILED EXECUTION PLAN

Step 1: Create workflow file
⚙️ **IMPLEMENTATION:** Markdown with YAML frontmatter and // turbo annotation
💡 **TEACH ME:** Windsurf workflows auto-run when you type /command

[...full plan with teach-me markers...]
```

### **Phase 6 - Execution:**
```
⚡ EXECUTION

[1/3] Creating workflow file... ✅
[2/3] Writing protocol... ✅
[3/3] Updating memory... ✅

✅ EXECUTION COMPLETE

Test it by typing: /collab
```

---

## Integration with Other Systems

### **Brain Sync Daemon:**
After successful collab cycle → Update brain with new protocol

### **Proof Protocol:**
Track collab cycle usage → Promote if successful 3+ times

### **Memory System:**
Create memory with trigger phrases and workflow location

### **MCP Servers:**
No direct integration (workflow is IDE-level)

---

## Evolution Path

### **Current (v1.0):**
Manual protocol following, workflow provides structure

### **Near-term (v1.1):**
Auto-detect implicit triggers ("I have an idea...")

### **Long-term (v2.0):**
AI learns your collab patterns, suggests when to use cycle

---

## Quick Reference

```
┌─────────────────────────────────────────────┐
│ COLLABORATIVE DEV CYCLE                     │
├─────────────────────────────────────────────┤
│ 1. BREADCRUMBS  → Collect all context       │
│ 2. DEEP DIVE    → Pull more strings         │
│ 3. BRAINSTORM   → PromptGen + Decision      │
│ 4. ⏸️ PAUSE      → Switch to thinking model  │
│ 5. PLAN         → Detailed steps + markers  │
│ 6. EXECUTE      → Build + test              │
└─────────────────────────────────────────────┘

Teach-Me Markers:
  💡 WHY      🎯 WHAT/WHY    ⚙️ HOW
  ⚠️ GOTCHA   ✅ SUCCESS

Triggers:
  [collab], [LFG], "I have an idea..."
```

---

**Status:** Production Ready ✅  
**Effort to Use:** 0 seconds (just say /collab)  
**Value:** Consistent, comprehensive dev cycles across all LLMs

**Remember:** This protocol is the map. The workflow is the vehicle. Together they ensure you never miss context or skip important steps again.
