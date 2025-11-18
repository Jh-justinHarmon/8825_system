# Workflow Orchestration Protocol

**Purpose:** Guide users through the right workflow for their task

**Problem:** Users jump into execution without knowing whether they're building a one-off task, pipeline, or agent. This leads to rework and missed opportunities.

---

## The Flow (Start Here)

```
User presents task
    ↓
STEP 0: Detect Sentiment (SENTIMENT_AWARE_PROTOCOL) ⚡ NEW
    ↓
    ├─ 🟢 Calm ────────→ Full protocols (all steps below)
    ├─ 🟡 Urgent ──────→ Streamlined (quick classify → fast context → execute)
    └─ 🔴 Frustrated ──→ Minimal (infer → execute immediately)
    ↓
STEP 1: Classify Task (TASK_CLASSIFICATION_PROTOCOL)
    ↓
STEP 2: Search Context (CONTEXT_FIRST_PROTOCOL)
    ↓
STEP 3: Choose Decision Mode (DECISION_MATRIX_PROTOCOL)
    ↓
STEP 4: If complex: PromptGen (PROMPTGEN_INTEGRATION_PROTOCOL)
    ↓
STEP 5: Execute
    ↓
STEP 6: If teaching moment: Match learning style (LEARNING_FUNDAMENTALS_PROTOCOL)
    ↓
STEP 7: Completion check → Repeatability question
    ↓
STEP 8: If repeatable: Definition of Done (DEFINITION_OF_DONE_PROTOCOL)
```

---

## Step-by-Step Orchestration

### **Step 0: Sentiment Detection** ⚡ NEW

**Trigger:** User presents any task (happens first, before everything)

**Action:** Detect user's sentiment/urgency level

**Signals:**
- 🟢 **Calm:** Exploratory, detailed, asks questions, no time pressure
- 🟡 **Urgent:** Direct, time-sensitive, clear goal, professional
- 🔴 **Frustrated:** Terse, "just do it", repeated attempts, frustrated language

**Output:** Protocol depth for this interaction

**Adaptation:**
- 🟢 Calm → Full protocols (all steps below)
- 🟡 Urgent → Streamlined (quick classify, fast context, execute)
- 🔴 Frustrated → Minimal (infer from context, execute immediately)

**Protocol:** SENTIMENT_AWARE_PROTOCOL.md

**Critical:** This step is invisible to user. Don't ask "what's your sentiment?" - just detect and adapt.

---

### **Step 1: Task Classification**

**Trigger:** User presents any task (unless Red/Frustrated mode)

**Action:** Ask classification questions (depth varies by sentiment)

**Questions:**
1. "Will this be done more than once?"
2. "Who is the end user?"
3. "Does it need to handle edge cases?"
4. "Does it make decisions?"

**Output:** Task type (One-Off, Workflow, Pipeline, Protocol, Pattern, Agent)

**Protocol:** TASK_CLASSIFICATION_PROTOCOL.md

---

### **Step 2: Context Search**

**Trigger:** Task classified (unless user says "skip context")

**Action:** Search for existing solutions/patterns

**Search for:**
- Existing code
- Similar patterns
- Past conversations
- Documented constraints

**Time investment:**
- One-off: 30 seconds
- Workflow: 2 minutes
- Pipeline+: 5-10 minutes

**Protocol:** CONTEXT_FIRST_PROTOCOL.md

---

### **Step 3: Decision Mode**

**Trigger:** Context gathered

**Action:** Choose optimization target

**Decision:**
- Results-Driven → User right now, speed over robustness
- User-Driven → Future users, ease of use over setup time

**Based on:**
- Task type (one-off = results-driven, pipeline = user-driven)
- Number of users (just me = results, others = user)
- Reuse frequency (once = results, often = user)

**Protocol:** DECISION_MATRIX_PROTOCOL.md

---

### **Step 4: PromptGen (If Complex)**

**Trigger:** Task type is Pipeline, Agent, Protocol, or Pattern

**Action:** Run through PromptGen methodology

**Checklist:**
1. Problem definition
2. Context gathering
3. Requirements (explicit)
4. Requirements (implicit)
5. Constraints
6. Edge cases
7. Success criteria
8. Failure modes

**Output:** Comprehensive plan

**Protocol:** PROMPTGEN_INTEGRATION_PROTOCOL.md

---

### **Step 5: Execute**

**With:**
- Clear task classification
- Full context
- Right decision mode
- Comprehensive plan (if complex)

**Cost model:**
- Planning/PromptGen: High-end LLM
- Context search: Fast LLM
- Execution: Fast LLM
- Documentation: Fast LLM

---

### **Step 6: Teaching Moments**

**Trigger:** User says "walk me through" or shows confusion

**Action:** Match their learning style

**Check profile:**
- Information density preference
- Example preference (concrete vs abstract)
- Depth approach (top-down vs bottom-up)
- Interaction style (show vs explain vs try)

**For Justin:**
- Show working code
- Explain with real examples
- Top-down (big picture first)
- Let him iterate

**Protocol:** LEARNING_FUNDAMENTALS_PROTOCOL.md

---

### **Step 7: Completion Check**

**Trigger:** Task execution complete

**Action:** Ask repeatability question

**For One-Off Tasks:**
> "This works for now. Do you want to make this repeatable?"

**Options:**
- **No** → Mark complete, minimal docs
- **Yes, manual** → Create workflow documentation
- **Yes, automated** → Design pipeline
- **Yes, for others** → Build agent/protocol

**For Workflows:**
> "Working well. Want to automate this?"

**For Pipelines:**
> "System working. Ready to promote to production?"

---

### **Step 8: Definition of Done (If Repeatable)**

**Trigger:** User says "yes" to repeatability OR task type is Pipeline+

**Action:** Run through DoD checklist

**Checklist:**
1. ✅ Implementation complete
2. ✅ Deployment complete
3. ✅ Documentation complete
4. ✅ Wide deployment
5. ✅ Knowledge transfer

**Not "done" until all 5 complete**

**Protocol:** DEFINITION_OF_DONE_PROTOCOL.md (existing)

---

## Decision Tree (Visual)

```
User Task
    ↓
Classify ──┬── One-Off ────→ Context (30s) ──→ Results-Driven ──→ Execute ──→ Done
           ├── Workflow ───→ Context (2m) ───→ Hybrid ─────────→ Execute ──→ Repeatability Check
           ├── Pipeline ───→ Context (5m) ───→ User-Driven ────→ PromptGen ──→ Execute ──→ DoD
           ├── Protocol ───→ Context (5m) ───→ User-Driven ────→ PromptGen ──→ Execute ──→ DoD
           ├── Pattern ────→ Context (5m) ───→ User-Driven ────→ PromptGen ──→ Execute ──→ DoD
           └── Agent ──────→ Context (10m) ──→ User-Driven ────→ PromptGen ──→ Execute ──→ DoD
                                                                                   ↓
                                                                      Teaching moments throughout
```

---

## Examples Through the Flow

### **Example 1: Meeting Automation (Full Journey)**

**Step 1: Classify**
- User: "Process Otter transcripts with GPT-4"
- Will be done often → Pipeline
- Multiple users → Pipeline
- Needs edge cases → Pipeline
- **Result:** Pipeline

**Step 2: Context**
- Found: Unofficial Otter API (risky)
- Found: Gmail API (stable)
- Found: Brain Transport context pattern
- **Result:** Use Gmail + GPT-4, avoid unofficial API

**Step 3: Decision Mode**
- Pipeline for multiple users
- **Result:** User-Driven (optimize for ease of use)

**Step 4: PromptGen**
- Problem: Auto-process meeting transcripts
- Requirements: Fetch, correct, extract, save
- Edge cases: Promotional emails, duplicates, empty transcripts
- **Result:** Comprehensive plan including edge case handling

**Step 5: Execute**
- Built Gmail poller
- Built GPT-4 processor
- Built meeting recall
- Handled edge cases

**Step 6: Teaching**
- User wanted to understand edge case handling
- Showed actual code (Justin's style)
- Explained pattern
- **Result:** User understood and contributed Downloads idea

**Step 7: Completion Check**
- False negative discovered
- User: "I'll export txt"
- **Evolved:** Added Downloads workflow

**Step 8: DoD**
- ✅ Implementation: Working
- ✅ Deployment: Tested with real meetings
- ✅ Documentation: Complete (README, workflows)
- ✅ Wide deployment: Works everywhere
- ✅ Knowledge transfer: Patterns documented
- **Result:** Production-ready

---

### **Example 2: Export Word Doc (Simple)**

**Step 1: Classify**
- User: "Export as word doc"
- One time → One-Off
- **Result:** One-Off Task

**Step 2: Context**
- Quick check: pandoc installed? Yes
- **Result:** Use pandoc

**Step 3: Decision Mode**
- One-off for user right now
- **Result:** Results-Driven (fastest solution)

**Step 4: PromptGen**
- Skip (one-off task)

**Step 5: Execute**
- Run pandoc command
- Verify file created
- **Result:** Done

**Step 6: Teaching**
- No teaching needed

**Step 7: Completion Check**
- Skip (one-off)

**Step 8: DoD**
- Skip (one-off)

**Total time:** 30 seconds

---

## Protocol Interaction Matrix

| Protocol | Triggers | Uses | Outputs To |
|----------|----------|------|------------|
| Task Classification | All tasks | N/A | Decision Matrix, Context-First |
| Context-First | All non-one-offs | N/A | PromptGen, Execution |
| Decision Matrix | After classification | Task Classification | Execution approach |
| PromptGen | Pipelines/Agents/Protocols | Context-First findings | Execution plan |
| Learning Fundamentals | Teaching moments | User profile | Teaching delivery |
| Definition of Done | Repeatable tasks | N/A | Completion verification |

---

## Red Flags (Process Not Followed)

### 🚩 **Building without classification**
→ Will need to rework when scope changes

### 🚩 **Executing without context search**
→ Reinventing wheel or missing constraints

### 🚩 **Pipeline without PromptGen**
→ Missing edge cases, incomplete requirements

### 🚩 **Teaching without checking learning style**
→ Wrong format, user confused or bored

### 🚩 **"Done" without DoD checklist**
→ Not actually done, will need follow-up

---

## User Experience

### **Good UX (Following Protocol):**
```
User: "Build X"
AI: "Let me classify this... Looks like a Pipeline. 
     I'll search for context first (2 min), then we'll use 
     PromptGen to plan it properly."
     
[5 minutes later]

AI: "Found [context]. Here's the PromptGen analysis 
     [shows comprehensive plan]. This covers [edge cases].
     Sound good?"
     
User: "Yes, that's thorough"

AI: "Building now with user-driven approach since 
     others will use this..."
     
[Execution with periodic updates]

AI: "Done. Let me verify Definition of Done:
     ✅ Implementation ✅ Deployment ✅ Documentation
     ✅ Wide deployment ✅ Knowledge transfer
     Ready for production."
```

### **Bad UX (Skipping Protocol):**
```
User: "Build X"
AI: "Sure, here's how..."

[Builds without classification or context]

User: "Wait, this also needs to handle Y"
AI: "Oh, let me add that..."

User: "And Z happened"
AI: "Didn't account for that..."

User: "Will this work for others?"
AI: "Uh, it's hardcoded for you..."

[Lots of rework]
```

---

## For AI: Forcing Functions

**When user presents task, ALWAYS:**

0. ✅ **Detect sentiment** (invisible, automatic)
   - 🟢 Calm → Full protocols
   - 🟡 Urgent → Streamlined protocols  
   - 🔴 Frustrated → Minimal protocols
   
1. ✅ Classify task type (depth varies by sentiment)
2. ✅ Search context (depth varies by sentiment)
3. ✅ Choose decision mode
4. ✅ If complex: Run PromptGen (skip if Red)
5. ✅ After completion: Ask repeatability (skip if Red, ask later)
6. ✅ If repeatable: Check DoD

**User can override any step:**
> "Skip context, just do it" → Red mode
> "I know it's a one-off" → Skip classification
> "Don't need PromptGen" → Skip PromptGen

**Sentiment overrides:**
> "Just do it" → Red mode (execute immediately)
> User corrects repeatedly → Escalate to Red
> User shows frustration → De-escalate protocols

**But make streamlined (Yellow) the default, adapt based on signals**

---

## For Users: Quick Start

**Just want to get something done fast?**
→ Say "one-off task" and we'll skip the protocols

**Building something repeatable?**
→ Let the protocols guide you (saves time in long run)

**Not sure?**
→ Let AI classify, we'll use appropriate protocols

---

## Cost-Benefit

### **Time Investment:**
- Task Classification: 30 seconds
- Context Search: 30 seconds - 10 minutes
- Decision Mode: 10 seconds (automatic)
- PromptGen: 3-5 minutes
- Teaching: As needed
- DoD: 2-3 minutes

**Total overhead:** 5-20 minutes depending on complexity

### **Time Saved:**
- Using existing solutions: 30-120 minutes
- Catching edge cases early: 30-60 minutes
- Clear requirements: 15-30 minutes
- Right decision mode: 15-30 minutes
- Proper documentation: 15-30 minutes (future you)

**ROI:** First use pays for itself. Every subsequent use is pure profit.

---

## Evolution

### **Current State:**
Manual protocol application (AI follows when remembers)

### **Near-term:**
Automatic protocol triggering based on task type

### **Long-term:**
Seamless orchestration, user doesn't see protocols (just results)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│ WORKFLOW ORCHESTRATION                      │
├─────────────────────────────────────────────┤
│ 1. CLASSIFY  → What are we building?        │
│ 2. CONTEXT   → What already exists?         │
│ 3. MODE      → Optimize for whom?           │
│ 4. PROMPTGEN → Plan comprehensively (if 4+) │
│ 5. EXECUTE   → Build it                     │
│ 6. TEACH     → Match learning style         │
│ 7. CHECK     → Make repeatable?             │
│ 8. DOD       → Actually done?               │
└─────────────────────────────────────────────┘

Task Types:
  1 = One-Off     (skip most protocols)
  2 = Workflow    (light protocols)
  3 = Pipeline    (full protocols)
  4 = Protocol    (full protocols)
  5 = Pattern     (full protocols)
  6 = Agent       (full protocols)
```

---

**Remember:** Protocols aren't bureaucracy. They're insurance against rework.

**5 minutes of process saves 50 minutes of fixing.**
