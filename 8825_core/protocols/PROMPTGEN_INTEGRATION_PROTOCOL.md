# PromptGen Integration Protocol

**Purpose:** Use PromptGen methodology during brainstorming to create better plans

**Problem:** Brainstorming without structure leads to missed requirements, unclear goals, and suboptimal solutions.

---

## Core Principle

**PromptGen = Structured thinking that forces clarity before execution**

When brainstorming ANY solution (especially pipelines, agents, protocols):
→ Run through PromptGen methodology
→ Generate formal plan
→ Then execute

---

## What is PromptGen?

**PromptGen Philosophy:**
A systematic approach to problem-solving that forces you to:
1. Clearly define the problem
2. Identify all constraints
3. List requirements explicitly
4. Consider edge cases upfront
5. Plan for failure modes
6. Define success criteria

**Not just for prompts** - applies to any planning phase

---

## PromptGen Checklist (Apply During Brainstorming)

### **1. Problem Definition**
```
What problem are we actually solving?
- What's the core need?
- What's the pain point?
- What happens if we don't solve this?
- What's the minimum viable solution?
```

### **2. Context Gathering**
```
What do we already know?
- What existing solutions are there?
- What patterns have we used before?
- What constraints apply?
- What's the current state?
```

### **3. Requirements (Explicit)**
```
What MUST the solution do?
- Core functionality (non-negotiable)
- Performance requirements
- User experience requirements
- Integration requirements
```

### **4. Requirements (Implicit)**
```
What's assumed but not stated?
- Who will use this?
- Where will it run?
- When will it be used?
- How often will it run?
```

### **5. Constraints**
```
What are the limitations?
- Technical constraints (APIs, dependencies)
- Time constraints (deadlines)
- Cost constraints (API costs, compute)
- User constraints (skill level, tools)
```

### **6. Edge Cases**
```
What could go wrong?
- Missing data
- Invalid input
- API failures
- Network issues
- Unexpected formats
```

### **7. Success Criteria**
```
How do we know it works?
- What does "done" look like?
- What metrics matter?
- What's the acceptance test?
- How do we validate?
```

### **8. Failure Modes**
```
How should it fail?
- Graceful degradation
- Error messages
- Recovery procedures
- Data safety
```

---

## When to Apply PromptGen

### **Always Use For:**
- ✅ Pipeline design
- ✅ Agent architecture
- ✅ Protocol creation
- ✅ Pattern documentation
- ✅ Complex workflows
- ✅ Multi-step automations

### **Sometimes Use For:**
- 🟡 Repeatable workflows (if complexity warrants)
- 🟡 Feature additions (if changing architecture)
- 🟡 Bug fixes (if root cause unclear)

### **Skip For:**
- ⚪ One-off tasks
- ⚪ Simple code changes
- ⚪ Documentation updates
- ⚪ Obvious fixes

---

## Integration with Brainstorming Phase

### **Standard Brainstorming (Without PromptGen):**
```
User: "Let's build X"
    ↓
AI: "Here's how we could do it..."
    ↓
Start building
    ↓
Hit edge case / realize missed requirement
    ↓
Rework
```

### **PromptGen-Enhanced Brainstorming:**
```
User: "Let's build X"
    ↓
AI: "Let me run through PromptGen methodology first"
    ↓
Work through 8 checklist items
    ↓
AI: "Based on this analysis, here's the plan..."
    ↓
User: "Looks good" or "Wait, we also need Y"
    ↓
Refine plan with all requirements
    ↓
Execute with confidence
```

---

## Example: Meeting Automation (With PromptGen)

### **1. Problem Definition**
- **Core need:** Process Otter.ai transcripts with GPT-4
- **Pain point:** Manual copy/paste, no transcription corrections
- **If not solved:** Continue wasting 10 min per meeting
- **Minimum viable:** Auto-fetch from Gmail, process with GPT-4, save output

### **2. Context Gathering**
- **Existing solutions:** Unofficial Otter API (risky), Gmail API (stable)
- **Patterns:** Brain Transport context loading
- **Constraints:** Must use official APIs only
- **Current state:** Manual processing via ChatGPT

### **3. Requirements (Explicit)**
- Fetch transcripts from Gmail
- Correct transcription errors (names, systems)
- Extract structured data (decisions, actions, risks)
- Save as JSON + Markdown
- Cost < $0.20 per meeting

### **4. Requirements (Implicit)**
- Will be used after every meeting (daily)
- User won't want to configure anything
- Must handle various meeting formats
- Other team members might use it

### **5. Constraints**
- Official APIs only (no unofficial Otter API)
- Must work on macOS
- API keys already in Keychain
- Budget: ~$5/month

### **6. Edge Cases**
- Promotional emails from Otter
- Duplicate meetings
- Empty transcripts
- API failures
- Malformed emails

### **7. Success Criteria**
- Processes meeting in < 1 minute
- Corrections are accurate (verified by user)
- Structured data complete
- Cost under budget
- User can run with single command

### **8. Failure Modes**
- Save raw data if GPT-4 fails
- Skip promotional emails (don't error)
- Clear error messages
- Don't lose data

### **Result:**
Comprehensive plan that anticipated edge cases before building

---

## Example: Downloads Workflow (Could Have Used PromptGen)

### **What Happened:**
```
Problem: Empty transcript emails
    ↓
Jumped to solution: Fetch from Otter.ai
    ↓
Hit wall: Unofficial API risky
    ↓
User: "I'll just export txt"
    ↓
Realized: Could have asked about user workflow upfront
```

### **If We'd Used PromptGen:**

**1. Problem Definition:**
- Some emails have no transcript in body

**2. Context:**
- Why are they empty? (HTML-only emails)
- What does user already do? (**Could have asked this**)

**3. Requirements:**
- Still need to process these meetings

**4. Constraints:**
- Can't use unofficial Otter API

**5. Edge Cases:**
- How often does this happen?
- **What's user's current workaround?** (**Key question missed**)

**6. Success Criteria:**
- User can process these meetings easily

**If asked:** "What do you currently do when transcript is empty?"  
**User would have said:** "I export txt from Otter"  
**Direct to solution:** Downloads workflow

**Lesson:** PromptGen forces you to ask about current state/workflow

---

## PromptGen Template (Copy-Paste for Brainstorming)

```markdown
## PromptGen Analysis: [Topic]

### 1. Problem Definition
- Core need:
- Pain point:
- If not solved:
- Minimum viable:

### 2. Context
- Existing solutions:
- Patterns used before:
- Known constraints:
- Current state:

### 3. Requirements (Explicit)
- MUST have:
- SHOULD have:
- NICE to have:

### 4. Requirements (Implicit)
- Who uses this:
- Where it runs:
- When used:
- How often:

### 5. Constraints
- Technical:
- Time:
- Cost:
- User:

### 6. Edge Cases
- Data issues:
- API failures:
- User errors:
- Unexpected inputs:

### 7. Success Criteria
- Definition of done:
- Metrics:
- Acceptance test:
- Validation method:

### 8. Failure Modes
- How to fail gracefully:
- Error handling:
- Recovery:
- Data safety:

---

## Proposed Solution
[Based on above analysis]

## Alternatives Considered
[What we're NOT doing and why]

## Implementation Plan
[Step-by-step based on requirements]
```

---

## Integration with Other Protocols

### **Context-First + PromptGen:**
```
1. Search for context (existing solutions, patterns)
2. Run through PromptGen with gathered context
3. Generate plan
4. Execute
```

### **Task Classification + PromptGen:**
```
1. Classify task type
2. If Pipeline/Agent/Protocol → PromptGen required
3. Work through methodology
4. Plan accordingly
```

### **Decision Matrix + PromptGen:**
```
During PromptGen:
- Requirements #4 (implicit) → Identifies user type
- Constraints → Informs decision mode
- Success criteria → Defines optimization target
```

---

## When NOT to Use PromptGen

**Skip PromptGen if:**
- One-off task with clear scope
- Simple code change
- Obvious solution
- Time-critical bug fix
- Exploratory / prototyping

**But even then, quick mental checklist helps:**
- What's the problem?
- What could go wrong?
- How do I know it works?

---

## PromptGen for Users

**When user presents complex task:**

> "This sounds like a pipeline/agent. Let me work through PromptGen methodology to make sure we cover everything. Give me 3 minutes to analyze this properly."

Then work through checklist and present findings.

**User can override:**
> "Just build it, we'll iterate"

But make PromptGen the default for complex work.

---

## Benefits

### **Time Saved:**
- 30 minutes of planning saves 2 hours of rework
- Edge cases identified upfront, not during testing
- Requirements clear before coding
- Failure modes handled, not discovered

### **Better Solutions:**
- Comprehensive (doesn't miss edge cases)
- Robust (handles failures gracefully)
- User-aligned (considers actual usage)
- Cost-effective (plans for constraints)

### **Clearer Communication:**
- User sees full analysis
- Can spot missed requirements
- Confirms understanding
- Reduces back-and-forth

---

## Evolution Path

### **Current State:**
Use PromptGen manually when remember to

### **Near-term:**
Automatic trigger for pipelines/agents/protocols

### **Long-term:**
AI automatically runs PromptGen analysis, presents findings

---

## Quick Reference

| Task Type | PromptGen? | Depth |
|-----------|------------|-------|
| One-off | No | N/A |
| Workflow | Maybe | Light (3-4 items) |
| Pipeline | Yes | Full (all 8 items) |
| Protocol | Yes | Full + examples |
| Pattern | Yes | Full + abstraction |
| Agent | Yes | Full + decision trees |

**Trigger words:**
- "Build a system"
- "Automate"
- "For users"
- "Production"
- "Repeatable"

**Response:**
> "Let me run through PromptGen methodology first..."

---

## Success Metrics

**Good PromptGen Session:**
- ✅ Identifies requirements user didn't state
- ✅ Catches edge cases before building
- ✅ Defines clear success criteria
- ✅ Results in comprehensive plan
- ✅ User says "yes, that covers it"

**Poor PromptGen Session:**
- ❌ Just restates what user said
- ❌ Misses obvious edge cases
- ❌ Unclear success criteria
- ❌ User has to add requirements later
- ❌ Plan needs major revision

---

**Remember:** 5 minutes of structured thinking beats 2 hours of unstructured building.

**PromptGen isn't overhead - it's insurance against rework.**
