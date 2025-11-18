# Workflow Protocols - Structured Task Execution Fra

**Created:** 2025-11-17  
**Source:** Assimilated from Windsurf memory

## Origin

This protocol was automatically created from a Windsurf AI session memory.

## Original Memory

```
Workflow Protocols - Structured Task Execution Framework
#protocols
#workflow
#task_classification
#context_first
#decision_matrix
#promptgen
#learning_fundamentals
#orchestration
#sentiment_aware
#v3.2.0

Edit
Created: Nov 13, 2025
Purpose: Prevent common pitfalls in LLM-assisted development

The Problem
User insight: "Working with you has fundamentally changed how I interact with LLMs. 8825 has become so powerful and intuitive that I've gotten lazy with prompting. I need reminders and guidance to build disciplined workflows."

Common pitfalls:

Jumping into execution without understanding scope
Reinventing solutions that already exist
Building for wrong optimization target (me vs users)
Missing edge cases in planning
Teaching in wrong format
Declaring "done" prematurely
Frustrating urgent users with too many questions ⚡ NEW
Eight New Protocols
0. SENTIMENT_AWARE_PROTOCOL.md ⚡ NEW (Step 0)
Adapt protocol depth based on user urgency/frustration.

3 Modes:

🟢 Calm: Full protocols (exploratory, detailed, no time pressure)
🟡 Urgent: Streamlined (direct, time-sensitive, 1-2 questions max)
🔴 Frustrated: Minimal (terse, "just do it", execute immediately)
Key insight: "Frustrated user who gets unblocked > Calm user who gets perfect process"

Detection signals:

Green: Exploratory, asks questions, detailed
Yellow: Direct requests, time-sensitive, clear goal
Red: Terse, "just do it", repeated corrections, frustrated language
Adaptation:

Green → Full classification, deep context search (5-10min), PromptGen
Yellow → Quick classify (5s), fast context (30s-2min), 1-2 questions max
Red → Infer from context (0s), skip questions, execute immediately
Default: Start Yellow (streamlined), adapt based on signals

Critical: This is Step 0, happens BEFORE everything else. Invisible to user - don't ask "what's your sentiment?", just detect and adapt.

1. WORKFLOW_ORCHESTRATION_PROTOCOL.md (Master)
Orchestrates when to use each protocol based on task type and sentiment.

Flow:

Sentiment Detection → Classify → Context Search → Decision Mode → PromptGen (if complex) 
→ Execute → Teaching (if needed) → Repeatability Check → DoD
2. TASK_CLASSIFICATION_PROTOCOL.md
Classify before building:

One-Off: Do once, minimal docs
Repeatable Workflow: Manual process, document steps
Pipeline: Automated sequence, error handling
Protocol: Methodology to follow
Pattern: Reusable solution
Agent: Autonomous decision-maker
Key questions:

Will this be done more than once?
Who is the end user?
Does it need edge cases?
Does it make decisions?
Quick reference: TASK_TYPES_REFERENCE.md

3. CONTEXT_FIRST_PROTOCOL.md
Search before executing:

Existing code (code_search, grep)
Documentation (README, protocols)
Memory (past conversations)
Dependencies (what's available)
Time investment (varies by sentiment):

One-off: 30 seconds
Workflow: 2 minutes
Pipeline+: 5-10 minutes
Red mode: 0 seconds (use existing context only)
ROI: 2 min search saves 20 min rework

4. DECISION_MATRIX_PROTOCOL.md
Choose optimization target:

Results-Driven: For you, now (speed over robustness)
User-Driven: For others, later (ease over setup time)
Decision criteria shift:

Setup time, documentation, error messages, edge cases, commands, config, monitoring
Example: Meeting automation started results-driven (prototype), evolved user-driven (production)

5. PROMPTGEN_INTEGRATION_PROTOCOL.md
Structured brainstorming (8-point checklist):

Problem definition
Context gathering
Requirements (explicit)
Requirements (implicit)
Constraints
Edge cases
Success criteria
Failure modes
Use for: Pipelines, Agents, Protocols, Patterns
Skip for: One-offs, simple changes, Red mode (frustrated users)

Value: 5 min planning saves 2 hours rework

6. LEARNING_FUNDAMENTALS_PROTOCOL.md
Match teaching to user's learning style:

Information density (sparse/moderate/dense)
Example preference (concrete/abstract/comparative)
Depth approach (top-down/bottom-up/middle-out)
Interaction style (show/walk-through/let-try/explain-first)
Error tolerance (high/low/medium)
Justin's profile:

Concrete examples from actual work
Top-down (big picture first)
Show and explain combo
High error tolerance
Learns by doing, then understanding
Track sentiment:

Understanding: "Makes sense", deeper questions
Confusion: Silence, repeats question
Boredom: "Yeah yeah", interrupts
Overwhelm: "Wait what?", asks to slow down
7. QUICK_START_GUIDE.md
3-minute intro for users and AI with cheat sheets and examples.

Integration
Works with existing protocols:

Definition of Done (already exists)
Deep Dive Research Protocol
POC Promotion Criteria
Cost model:

Planning: High-end LLM (GPT-4)
Context search: Fast LLM
Execution: Fast LLM
Documentation: Fast LLM
Real Examples
Meeting Automation:

Started: One-off ("process this transcript")
Became: Workflow ("process weekly")
Evolved: Pipeline ("auto from Gmail")
Enhanced: Agent ("handle edge cases")
Lesson: Would save 50% time if classified as Pipeline upfront
Downloads Workflow:

Could have asked about user's workflow in PromptGen
User already had solution ("I export txt")
Skipping PromptGen led to one iteration of rework
API Key Management:

Excellent context search (found LastPass, Keychain patterns)
Perfect solution first try (no rework)
Frustrated User Example (NEW):

User: "Just export the damn file"
AI: [Executes immediately, no questions]
Result: User unblocked, can discuss improvements later when calm
Completion Check Pattern
After completing any task, ask:

"This works for now. Do you want to make this repeatable?"

Options:

No → Done, minimal docs
Yes, manual → Workflow docs
Yes, automated → Pipeline
Yes, for others → Agent/protocol
Skip in Red mode - ask later when user is calm

Location
{USER_HOME}/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/protocols/

Files:

WORKFLOW_ORCHESTRATION_PROTOCOL.md (master, updated with Step 0)
SENTIMENT_AWARE_PROTOCOL.md ⚡ NEW
TASK_CLASSIFICATION_PROTOCOL.md
TASK_TYPES_REFERENCE.md (NEW - quick definitions)
CONTEXT_FIRST_PROTOCOL.md
DECISION_MATRIX_PROTOCOL.md
PROMPTGEN_INTEGRATION_PROTOCOL.md
LEARNING_FUNDAMENTALS_PROTOCOL.md
QUICK_START_GUIDE.md
README.md (updated to v3.2.0)
Total: ~18,000 lines of protocol documentation

Usage
For AI: 0. Detect sentiment (automatic, invisible)

Adapt protocol depth based on sentiment
Use WORKFLOW_ORCHESTRATION as default flow
Default to Yellow (streamlined), not Green (full)
Watch for Red signals: "just do it", corrections, frustration
Re-engage protocols after success in Red mode
For Users: Read WORKFLOW_ORCHESTRATION first, then dive into specific protocols as needed

Status: ✅ Active as of Nov 13, 2025
```

## Protocol

- #task_classification
- 0. SENTIMENT_AWARE_PROTOCOL.md ⚡ NEW (Step 0)
- Green → Full classification, deep context search (5-10min), PromptGen
- Yellow → Quick classify (5s), fast context (30s-2min), 1-2 questions max
- Critical: This is Step 0, happens BEFORE everything else. Invisible to user - don't ask "what's your sentiment?", just detect and adapt.
- Orchestrates when to use each protocol based on task type and sentiment.
- Sentiment Detection → Classify → Context Search → Decision Mode → PromptGen (if complex)
- → Execute → Teaching (if needed) → Repeatability Check → DoD
- 2. TASK_CLASSIFICATION_PROTOCOL.md
- Classify before building:
- Repeatable Workflow: Manual process, document steps
- Decision criteria shift:
- Lesson: Would save 50% time if classified as Pipeline upfront
- Result: User unblocked, can discuss improvements later when calm
- Skip in Red mode - ask later when user is calm
- WORKFLOW_ORCHESTRATION_PROTOCOL.md (master, updated with Step 0)
- TASK_CLASSIFICATION_PROTOCOL.md
- For Users: Read WORKFLOW_ORCHESTRATION first, then dive into specific protocols as needed

## Related Context


**Key Entities:**
DLI, Protocol, Workflow, 8825, PromptGen

---

*This protocol was auto-generated. Review and enhance as needed.*
