# Context-First Protocol

**Purpose:** Prevent "beating our heads against the wall" by gathering context before executing

**Problem:** Jumping straight into execution without searching for existing solutions, patterns, or full context leads to wasted time and suboptimal solutions.

---

## The Pattern (What Happens)

### **Without Context:**
```
User: "Build this thing"
    ↓
AI: "Sure, here's how" (builds from scratch)
    ↓
Hits wall / doesn't work / already exists
    ↓
User: "Let me search for context..."
    ↓
Find existing solution or critical context
    ↓
Realize we could have saved 30 minutes
```

### **With Context:**
```
User: "Build this thing"
    ↓
AI: "Let me search for existing solutions/patterns first"
    ↓
Find related work / patterns / constraints
    ↓
AI: "Found X, Y, Z. Here's the plan using what exists"
    ↓
Execute with full knowledge
    ↓
Success on first try
```

---

## Context Search Checklist (Run Before Executing)

### **1. Search Codebase**
```bash
# Find existing implementations
code_search: "similar functionality"
grep_search: "related functions"
```

**Ask:**
- Has this been done before?
- Are there similar patterns in the codebase?
- What related systems exist?

### **2. Search Documentation**
```bash
# Find protocols, patterns, READMEs
find: "*.md" in relevant folders
read: PROTOCOL files, README files
```

**Ask:**
- Are there documented approaches?
- What are the established patterns?
- What constraints exist?

### **3. Search Memory**
```bash
# Check for related past conversations
trajectory_search: "similar topic"
memory_search: "key terms"
```

**Ask:**
- Have we solved this before?
- What did we learn last time?
- What pitfalls were documented?

### **4. Search Dependencies**
```bash
# Check what's already installed/available
list: package.json, requirements.txt
check: existing integrations
```

**Ask:**
- What tools are already available?
- What's already integrated?
- Can we leverage existing infrastructure?

---

## When to Search (Decision Tree)

```
New task arrives
    ↓
Is it a one-off task? ──Yes──> Quick search (30 sec)
    ↓ No
Is it building on existing work? ──Yes──> Deep search (5 min)
    ↓ No
Is it greenfield (brand new)? ──Yes──> Pattern search (2 min)
    ↓
Proceed with execution
```

---

## Red Flags (Stop and Search)

### 🚩 **"This seems like it should exist already"**
→ Stop. Search codebase and docs.

### 🚩 **"I'm not sure how this integrates"**
→ Stop. Search for integration patterns.

### 🚩 **"This is taking longer than expected"**
→ Stop. Search for existing solutions.

### 🚩 **"I feel like we did this before"**
→ Stop. Search memory and past conversations.

### 🚩 **"I don't know the constraints"**
→ Stop. Search for protocols and requirements.

---

## Context Layers (What to Look For)

### **Layer 1: Existing Code**
- Similar functions/scripts
- Related pipelines
- Shared utilities
- Integration points

### **Layer 2: Documented Patterns**
- Protocols (how we do things)
- Patterns (reusable solutions)
- Workflows (established processes)
- Architecture decisions

### **Layer 3: Historical Context**
- Past conversations on topic
- Previous attempts
- Known pain points
- Lessons learned

### **Layer 4: System Context**
- Brain Transport (system knowledge)
- TGIF Knowledge (project knowledge)
- Dependencies and constraints
- Environment setup

### **Layer 5: User Context**
- Learning preferences
- Working style
- Past decisions
- Current priorities

---

## Context Search by Task Type

### **One-Off Task**
- Quick grep for existing similar code (30 seconds)
- Check if it's been done before

### **Repeatable Workflow**
- Search for existing workflows (2 minutes)
- Look for documented processes
- Check for related scripts

### **Pipeline**
- Deep search for similar pipelines (5 minutes)
- Review integration patterns
- Check dependency compatibility
- Look for edge case handling

### **Protocol/Pattern**
- Search all existing protocols (3 minutes)
- Look for related patterns
- Review past architectural decisions

### **Agent**
- Comprehensive search (10 minutes)
- Review all related systems
- Check for reusable components
- Understand full integration surface

---

## Recent Examples

### **Example 1: Meeting Automation (Good)**
**Context gathered:**
- ✅ Found unofficial Otter API (existing but risky)
- ✅ Found Gmail API integration (existing, stable)
- ✅ Found GPT-4 processing patterns (Brain Transport)
- ✅ Found TGIF knowledge base (project context)

**Result:** Built on solid foundation, avoided unstable API

### **Example 2: Downloads Workflow (Could Have Been Better)**
**What happened:**
- User hit empty transcript issue
- Jumped to "fetch from Otter" solution
- Hit wall with unofficial API

**Could have searched:**
- ❌ Existing "export workflow" patterns
- ❌ User's actual workflow preference
- ❌ Similar "missing data" solutions

**What we found when we searched:**
- ✅ User already knew their workflow (export txt)
- ✅ Pattern: "Alert + manual export + auto-process"

**Lesson:** Searching for user's existing workflow would have saved iteration

### **Example 3: API Key Management (Excellent)**
**Context gathered:**
- ✅ Searched existing key storage (found LastPass)
- ✅ Searched macOS patterns (found Keychain)
- ✅ Searched for security protocols
- ✅ Remembered user hates terminal friction

**Result:** Perfect solution on first try (LastPass → Keychain → Vault fallback)

---

## Integration with PromptGen

**When brainstorming, run through PromptGen with gathered context:**

```
1. Search for context (5 min)
    ↓
2. Brainstorm with PromptGen (use gathered context)
    ↓
3. Generate formal plan
    ↓
4. Execute
```

**PromptGen questions to include:**
- What existing solutions did context search reveal?
- What patterns are established in the codebase?
- What constraints were documented?
- What did we learn from past attempts?

---

## Context-First Workflow

### **Step 1: Receive Task**
User describes what they want

### **Step 2: Classify Task**
Use Task Classification Protocol

### **Step 3: STOP - Context Search**
```
Before proposing solution:
1. Search codebase (code_search, grep_search)
2. Search docs (find *.md, read READMEs)
3. Search memory (trajectory_search)
4. Search brain (check Brain Transport, knowledge bases)
```

### **Step 4: Synthesize Findings**
```
Present to user:
- "Found these existing solutions: [X, Y, Z]"
- "Found these patterns: [A, B, C]"
- "Found these constraints: [P, Q, R]"
- "Here's how we can use them: [plan]"
```

### **Step 5: Get Confirmation**
```
Ask user:
- "Should we use existing [X] or build new?"
- "This pattern worked before, use it again?"
- "These constraints apply, adjust plan?"
```

### **Step 6: Execute**
Now proceed with full knowledge

---

## Forcing Function (For AI)

**Before every execution, ask yourself:**

1. ✅ Did I search the codebase?
2. ✅ Did I check for existing patterns?
3. ✅ Did I review related docs?
4. ✅ Did I check past conversations?
5. ✅ Do I know the constraints?

**If any "No" → STOP and search**

---

## Forcing Function (For User)

**When user jumps straight in, gently pause:**

> "Before we start, let me search for existing solutions and patterns. This usually saves time. Give me 2 minutes."

Then search and present findings.

**User can override:**
> "Just do it, I know there's nothing"

But make the pause the default.

---

## Cost-Benefit

### **Time Investment:**
- Quick search: 30 seconds
- Medium search: 2-5 minutes
- Deep search: 10 minutes

### **Time Saved:**
- Using existing code: 30-60 minutes
- Following established pattern: 15-30 minutes
- Avoiding known pitfalls: 15-60 minutes
- Understanding constraints upfront: 30-120 minutes

**ROI:** Even 30 seconds of searching often saves 15+ minutes

---

## Edge Case: Exploratory Work

**When user is explicitly exploring:**
> "I want to try a different approach"
> "Let's experiment with X"
> "I know it exists, but let's build from scratch to learn"

**Then:** Skip context search, dive in

**But still document learnings** for future context

---

## Memory Integration

**After every task, save context learnings:**

```
Create memory:
- What existed that we used
- What existed that we didn't know about
- What patterns emerged
- What constraints were discovered
- What user preferences were revealed
```

**This builds future context layer**

---

## Quick Reference

| Situation | Search Depth | Time | What to Find |
|-----------|--------------|------|--------------|
| One-off task | Quick | 30s | Existing similar code |
| Repeatable workflow | Medium | 2-5min | Workflows, processes |
| Pipeline | Deep | 5-10min | Patterns, integration points |
| Stuck on problem | Deep | 5-10min | Past solutions, alternatives |
| Greenfield project | Medium | 3-5min | Patterns, architectures |
| Exploratory work | Skip | 0s | (document learnings after) |

---

**Golden Rule:** 2 minutes of context search saves 20 minutes of execution

**When in doubt:** Search first, execute second

**User jumping in:** Pause, search, present findings, then proceed

---

## Reminder Triggers

**AI should search when user says:**
- "Build X" (without mentioning existing work)
- "This isn't working" (might be missing context)
- "How do I..." (might have been solved before)
- "Let's try X" (check if X already exists)

**AI should ask before searching:**
- "Exploring new approach?"
- "Should I check for existing solutions first?"
- "2 minute context search or dive right in?"

**Default:** Always search unless user explicitly says "skip context"
