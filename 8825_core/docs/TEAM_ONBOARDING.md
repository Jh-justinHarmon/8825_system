# 8825 Team Onboarding

**Welcome to the 8825 system development team!**

This guide will get you up and running quickly.

---

## What is 8825?

8825 is an evidence-based system that evolves through actual usage, not manual curation. We call this the **Proof Protocol** - "You don't decide what survives - usage does."

**Core Components:**
- **6 True Agents** - Autonomous decision-makers (2 implemented, 4 to build)
- **4 Pipelines** - Automated sequences
- **8 Workflows** - Manual processes
- **Adaptive Learning System (ALS)** - Natural selection for learnings
- **Brain System** - Auto-sync and coordination

**Your Mission:** Help build the remaining 4 agents using proven methodologies.

---

## Quick Start (30 minutes)

### Step 1: Get Access (5 min)

**You need access to:**
1. **Dropbox Shared Folder**
   - Path: `Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/`
   - Contains all code, docs, and protocols
   - Request access from Justin

2. **iCloud Documents** (Read-only)
   - Path: `~/Library/Mobile Documents/com~apple~CloudDocs/`
   - Files: `8825_BRAIN_TRANSPORT.json`, `8825_SYSTEM_CAPABILITIES.md`
   - Auto-syncs system state

3. **Communication Channel**
   - [Slack/Discord/Email - TBD]
   - For daily standups and questions

---

### Step 2: Read Core Documents (15 min)

**Must Read (in order):**

1. **System Capabilities** (10 min)
   - Location: `~/Library/Mobile Documents/com~apple~CloudDocs/8825_SYSTEM_CAPABILITIES.md`
   - What: Complete overview of all 8825 capabilities
   - Why: Understand what exists and what you're building

2. **Team Execution Protocol** (5 min)
   - Location: `8825_core/protocols/TEAM_EXECUTION_PROTOCOL.md`
   - What: How we work together
   - Why: Understand workflow, roles, and communication

---

### Step 3: Set Up Environment (10 min)

**Requirements:**
- **Python:** 3.9 or higher
- **OS:** macOS (primary), Linux (supported)
- **Tools:** Git (optional), text editor/IDE

**Install Python packages:**
```bash
cd "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
pip3 install -r requirements.txt  # If exists
```

**Verify access:**
```bash
# Check you can read Brain Transport
cat ~/Documents/8825_BRAIN_TRANSPORT.json

# Check you can access system
ls -la 8825_core/
```

---

## System Overview

### Directory Structure

```
8825-system/
├── 8825_core/              # Shareable system
│   ├── agents/             # (Deprecated - see registry)
│   ├── brain/              # Brain sync, ALS, coordination
│   ├── docs/               # Documentation (you are here)
│   ├── integrations/       # Google, Reddit, Dropbox, etc.
│   ├── philosophy/         # Proof Protocol, learning system
│   ├── protocols/          # Team execution, PromptGen, etc.
│   ├── registry/           # Agent/pipeline/workflow registry
│   ├── scripts/            # Utilities
│   └── templates/          # Agent spec, PR, review templates
│
├── team/                   # Team workspace
│   ├── assignments/        # Current work
│   ├── standups/          # Daily updates
│   ├── reviews/           # Code reviews
│   └── learnings/         # Captured learnings
│
├── focuses/               # Project-specific work
│   ├── hcss/             # HCSS client work
│   └── joju/             # Joju product work
│
└── users/                # Private user data
    └── justin_harmon/    # Justin's workspace
```

---

## Key Concepts

### 1. Proof Protocol (Usage-Driven Evolution)

**Philosophy:** "You don't decide what survives - usage does."

**Four Barriers to Survival:**
1. **Trial Barrier** - Does anyone try it?
2. **Success Barrier** - Does it work?
3. **Context Barrier** - Does it work elsewhere?
4. **Time Barrier** - Is it still relevant?

**What This Means for You:**
- Track your protocol usage
- Document what works and what doesn't
- Let evidence guide decisions
- Don't manually curate - let usage determine survival

**Tool:** `./track_protocol.py PROTOCOL_NAME --success --context "What you did"`

---

### 2. PromptGen Methodology

**Purpose:** Structured thinking before execution

**7-Step Checklist:**
1. Problem Definition - What are we solving?
2. Context Gathering - What do we know?
3. Requirements (Explicit) - What MUST it do?
4. Requirements (Implicit) - What's assumed?
5. Constraints - What are the limitations?
6. Edge Cases - What could go wrong?
7. Success Criteria - How do we know it works?

**When to Use:** Before implementing ANY agent

**Location:** `8825_core/protocols/PROMPTGEN_INTEGRATION_PROTOCOL.md`

---

### 3. Adaptive Learning System (ALS)

**What:** Natural selection for learnings

**How It Works:**
1. Learnings captured with metadata
2. Usage tracked (success/failure)
3. Time-based decay applied (180-day half-life)
4. Competition resolved automatically
5. Survivors promoted, losers deprecated

**Survival Rates:**
- 60% die (never tried or failed)
- 30% stay context-specific
- 10% normalize across contexts

**What This Means for You:**
- Your work will be tracked
- Success/failure recorded
- Best approaches will emerge naturally

---

### 4. Brain System

**What:** Auto-sync and coordination system

**Components:**
- **Brain Sync Daemon** - Monitors changes every 30s
- **Brain Transport** - Complete system snapshot
- **System Health Monitor** - Triggers regeneration
- **Cascade Coordinator** - Manages active sessions

**What This Means for You:**
- System state always current
- Brain Transport has latest info
- Changes broadcast automatically
- No manual sync needed

---

## Your Workflow

### Phase 1: Planning (with team)
1. Architect presents agent from registry
2. Team applies PromptGen together
3. Generate detailed spec
4. You're assigned as owner

**Duration:** 1-2 hours (sync or async)

---

### Phase 2: Implementation (you)
1. Read spec and PromptGen checklist
2. Implement core functionality
3. Write tests
4. Document usage
5. Submit for review

**Duration:** 3-7 days

**Daily:** Post standup update in `team/standups/`

---

### Phase 3: Review (Architect)
1. Architect reviews your work
2. Tests functionality
3. Provides feedback or approves

**Duration:** 1-2 hours

---

### Phase 4: Integration (Integration Specialist)
1. Connect to workflows
2. Deploy to production
3. Monitor usage

**Duration:** 1-2 days

---

### Phase 5: Validation (QA/Operations)
1. Real-world testing
2. Track usage
3. Capture learnings

**Duration:** 1+ week

---

## Daily Routine

### Morning (5 min)
1. Check team channel for updates
2. Read other team members' standups
3. Post your standup in `team/standups/YYYY-MM-DD.md`

**Standup Template:**
```markdown
## [Your Name] - [Date]

### Yesterday
- Completed X
- Resolved blocker Y

### Today
- Working on Z
- Expected completion: [date]

### Blockers
- None / [Describe blocker]
```

---

### During Work
1. Follow implementation checklist
2. Write tests as you go
3. Document as you go
4. Ask questions early
5. Track protocol usage

---

### End of Day (2 min)
1. Commit/save your work
2. Update standup if needed
3. Flag blockers immediately

---

## Communication

### Daily (Async)
- **Standups:** Post in `team/standups/`
- **Questions:** Ask in team channel
- **Blockers:** Flag immediately

### Weekly (Sync - 30 min)
- **Review progress**
- **Discuss blockers**
- **Reprioritize**
- **Plan next week**

### Monthly (Sync - 1 hour)
- **Review metrics**
- **Process improvements**
- **Plan next month**
- **Celebrate wins**

---

## Tools You'll Use

### Protocol Tracker
```bash
# Track successful protocol use
./track_protocol.py PROTOCOL_NAME --success --context "What you did"

# Track failure
./track_protocol.py PROTOCOL_NAME --fail --notes "Why it failed"

# View report
./track_protocol.py --report
```

**Location:** `8825_core/protocols/track_protocol.py`

---

### Agent Registry
```bash
# View all agents
cat 8825_core/registry/agents.json

# Check your assigned agent
grep -A 20 "AGENT-YOUR-AGENT-ID" 8825_core/registry/agents.json
```

---

### Brain Transport
```bash
# View current system state
cat ~/Documents/8825_BRAIN_TRANSPORT.json

# Or iCloud version
cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/8825_BRAIN_TRANSPORT.json
```

---

## Templates Available

### Agent Spec Template
- **Location:** `8825_core/templates/AGENT_SPEC_TEMPLATE.md`
- **Use:** Create detailed agent specification
- **When:** During planning phase

### Implementation Checklist
- **Location:** `8825_core/templates/AGENT_IMPLEMENTATION_CHECKLIST.md`
- **Use:** Step-by-step implementation guide
- **When:** During implementation phase

### PR Template
- **Location:** `8825_core/templates/AGENT_PR_TEMPLATE.md`
- **Use:** Submit work for review
- **When:** After implementation complete

### Review Checklist
- **Location:** `8825_core/templates/AGENT_REVIEW_CHECKLIST.md`
- **Use:** Review someone else's work
- **When:** When assigned as reviewer

---

## Getting Help

### Questions About...

**System Architecture**
- Read: `8825_SYSTEM_CAPABILITIES.md`
- Ask: Architect (Justin)

**Implementation Details**
- Check: Existing agents in `8825_core/`
- Check: Templates in `8825_core/templates/`
- Ask: Integration Specialist

**Process/Workflow**
- Read: `TEAM_EXECUTION_PROTOCOL.md`
- Ask: Team channel
- Raise: Weekly sync

**Blockers**
- Post: Daily standup
- Tag: Relevant person
- Escalate: Architect if urgent

---

## Common Pitfalls

### ❌ Don't
- Skip PromptGen analysis
- Hardcode credentials
- Skip error handling
- Skip tests
- Skip documentation
- Work in isolation
- Wait to ask questions

### ✅ Do
- Follow the spec
- Handle edge cases
- Write clear code
- Test thoroughly
- Document well
- Post daily standups
- Ask questions early
- Track protocol usage

---

## Success Indicators

### You're on track if:
- ✅ Daily standups posted
- ✅ Tests passing
- ✅ Documentation growing
- ✅ Questions answered
- ✅ On schedule

### Warning signs:
- ⚠️ No progress for 2+ days
- ⚠️ Tests failing
- ⚠️ Unclear requirements
- ⚠️ Scope creeping
- ⚠️ No documentation

**If you see warning signs, raise them immediately!**

---

## First Assignment

### When You're Ready
1. Architect will assign you an agent
2. You'll receive detailed spec
3. Follow implementation checklist
4. Post daily standups
5. Submit for review when done

### Agents Available (Priority Order)
1. **Library Mining Complexity Router** (Score: 91.6)
2. **Joju Curation Agent** (Score: 88.0)
3. **Reddit Beta Evaluator** (Score: 75.0)
4. **Reddit Pre-Qualifier** (Score: 70.0)

---

## Resources

### Documentation
- **System Capabilities:** `~/Library/Mobile Documents/com~apple~CloudDocs/8825_SYSTEM_CAPABILITIES.md`
- **Team Protocol:** `8825_core/protocols/TEAM_EXECUTION_PROTOCOL.md`
- **PromptGen Protocol:** `8825_core/protocols/PROMPTGEN_INTEGRATION_PROTOCOL.md`
- **Proof Protocol:** `8825_core/philosophy/PROOF_PROTOCOL.md`

### Code
- **Agent Registry:** `8825_core/registry/agents.json`
- **Existing Agents:** `8825_core/brain/` (Decision Agent, Accountability Loop)
- **Integrations:** `8825_core/integrations/`

### Templates
- **All Templates:** `8825_core/templates/`

### Team Workspace
- **Assignments:** `team/assignments/`
- **Standups:** `team/standups/`
- **Reviews:** `team/reviews/`
- **Learnings:** `team/learnings/`

---

## Questions?

**Ask in team channel or contact:**
- **Architect:** Justin Harmon
- **Team Channel:** [TBD]

---

**Welcome aboard! Let's build something great together.** 🚀

---

**Onboarding Version:** 1.0  
**Last Updated:** 2025-11-13  
**Next Review:** 2025-12-13
