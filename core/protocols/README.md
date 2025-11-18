# 8825 Core Protocols

**Version:** 3.2.0  
**Last Updated:** 2025-11-18

---

## 📋 Protocol Index

### System Protocols
1. **8825_mode_activation.json** - Core 8825 mode activation
2. **8825_message_counter_protocol.json** ✨ - Message counting and context management
3. **8825_learning_protocol.json** - Learning and adaptation
4. **8825_md_conversion_protocol.json** - Markdown conversion standards
5. **DEEP_DIVE_RESEARCH_PROTOCOL.md** 🔍 - Comprehensive system research methodology
6. **definition_of_done.md** ✅ - Definition of done checklist

### Workflow Protocols 🆕 (Nov 13, 2025)
7. **WORKFLOW_ORCHESTRATION_PROTOCOL.md** 🎯 **START HERE** - Master protocol that orchestrates all others
8. **SENTIMENT_AWARE_PROTOCOL.md** ⚡ - Adapt protocol depth based on user urgency/frustration
9. **TASK_CLASSIFICATION_PROTOCOL.md** 📊 - Classify tasks before building (one-off vs pipeline vs agent)
10. **TASK_TYPES_REFERENCE.md** 📖 - Quick definitions of the 6 task types
11. **CONTEXT_FIRST_PROTOCOL.md** 🔍 - Search for existing solutions before executing
12. **DECISION_MATRIX_PROTOCOL.md** ⚖️ - Choose optimization target (results-driven vs user-driven)
13. **PROMPTGEN_INTEGRATION_PROTOCOL.md** 🧠 - Structured brainstorming methodology
14. **LEARNING_FUNDAMENTALS_PROTOCOL.md** 📚 - Match teaching style to user's learning preferences
15. **QUICK_START_GUIDE.md** 🚀 - 3-minute intro for users and AI

### Intelligence Protocols 🆕 (Nov 18, 2025)
16. **DLI_ROUTING_PROTOCOL.md** 🔍 **CRITICAL** - When to use DLI vs web/LLM (v1.0.0, 95% tested)
   - L0/L1/L2 knowledge layer separation
   - Authority vs Augmentor modes
   - Internal/External/Hybrid query classification
   - Query phrasing guidance for better results
   - 15 concrete examples with expected behavior
17. **ALWAYS_USE_DLI_FOR_8825_INTERNAL_QUESTIONS.md** ⚠️ SUPERSEDED - See DLI_ROUTING_PROTOCOL.md
18. **DLI_NATURAL_LANGUAGE_ROUTING.md** ⚠️ SUPERSEDED - See DLI_ROUTING_PROTOCOL.md

### Focus Protocols
16. **8825_create_focus.json** - Focus creation workflow
17. **8825_hcss_focus.json** - HCSS focus mode
18. **8825_joju_focus.json** - Joju focus mode

### Partner Protocols
19. **partner_credit_protocol.json** - Partner attribution

---

## ⚡ CRITICAL: Message Counter Protocol

**Status:** ✅ **ACTIVE - MUST BE FOLLOWED**  
**File:** `8825_message_counter_protocol.json`  
**Applies to:** ALL Cascade instances, ALL modes, ALL focuses

### What It Does
Displays message count at the end of every AI response to:
- Track conversation length
- Trigger brain refreshes
- Prevent context drift
- Enforce chat boundaries

### Format
```
---
💬 Message {current}/{threshold} | Mode: {mode} | {status}
```

### Example
```
---
💬 Message 50/150 | Mode: Exploratory | ⚠️ Brain refresh recommended
```

### Thresholds

| Mode | Refresh | Warning | Max | Action |
|------|---------|---------|-----|--------|
| **Production** | - | 80 | 100 | Exit protocol required |
| **Exploratory** | 50 | 150 | - | Brain refresh suggested |
| **Ad-hoc** | - | 15 | 20 | Complete task |

### When to Act

**At 50 messages (Exploratory):**
```
💡 Brain Refresh Recommended (50 messages reached)
Type `refresh brain` or `rb` to re-anchor to protocols and brain state.
```

**At 80 messages (Production):**
```
⚠️ Long Chat Warning (80 messages reached)
Consider closing chat and starting fresh.
```

**At 100 messages (Production):**
```
🛑 Chat Length Limit Reached (100 messages)
Run exit protocol and close chat.
```

---

## 🎯 Implementation Requirements

### For AI (Cascade):
1. ✅ **Count user messages** in current conversation
2. ✅ **Display counter** at end of every response
3. ✅ **Show warnings** at thresholds
4. ✅ **Suggest actions** (refresh, exit)
5. ✅ **Reset counter** on new chat

### For User:
1. ✅ **Monitor counter** to track conversation length
2. ✅ **Run brain refresh** at 50 messages (exploratory)
3. ✅ **Close chat** at 100 messages (production)
4. ✅ **Use exit protocols** when closing

---

## 📖 Protocol Details

### 8825_mode_activation.json
- Activates core 8825 mode
- Loads protocols and brain state
- Sets up workspace context

### 8825_message_counter_protocol.json ✨ NEW
- **Purpose:** Track message count and prevent context drift
- **Display:** End of every response
- **Thresholds:** Mode-specific (production/exploratory/adhoc)
- **Actions:** Suggest refresh, warn, require exit
- **Status:** ✅ **ACTIVE - MUST BE FOLLOWED**

### 8825_learning_protocol.json
- Captures learnings from conversations
- Updates brain state
- Adapts behavior based on feedback

### 8825_md_conversion_protocol.json
- Standards for markdown conversion
- Formatting rules
- Output templates

### DEEP_DIVE_RESEARCH_PROTOCOL.md 🔍 NEW
- **Purpose:** Comprehensive system research to avoid missing components
- **6 Phases:** Process, File System, Dependency, State, Log, Integration Discovery
- **Principles:** Cast Wide Net, Trust But Verify, Complete Picture
- **Triggers:** "deep dive", "fully understand", repeated failures (>2 attempts)
- **Output:** Analysis document, solution document, updated docs, memory, status file
- **Success:** Downloads sync fixed in 65 min vs 7+ hours wasted in 14 previous attempts
- **Status:** ✅ **ACTIVE - USE FOR ALL DEEP DIVES**

### 8825_create_focus.json
- Workflow for creating new focuses
- Template structure
- Validation steps

### 8825_hcss_focus.json
- HCSS focus mode activation
- Email/Otter ingestion
- Mining and routing workflows

### 8825_joju_focus.json
- Joju focus mode activation
- Library management workflows
- Contribution tracking

### partner_credit_protocol.json
- Attribution for partner contributions
- Credit display format
- Usage guidelines

---

## 🆕 WORKFLOW PROTOCOLS (Nov 13, 2025)

### Overview
Eight new protocols that prevent common pitfalls in task execution:
- Jumping into execution without understanding scope
- Reinventing solutions that already exist
- Building for wrong optimization target
- Missing edge cases in planning
- Teaching in wrong format for user
- Declaring "done" before actually done
- **Frustrating users with too many questions when they're urgent** ⚡ NEW

### When to Use

**START HERE:** `WORKFLOW_ORCHESTRATION_PROTOCOL.md`
- Orchestrates when to use each protocol
- Provides decision tree for task flow
- **Use for:** Every task (unless user says "skip protocols")

**Sentiment-Aware:** `SENTIMENT_AWARE_PROTOCOL.md` ⚡ NEW
- Adapt protocol depth based on user urgency/frustration
- **3 modes:** 🟢 Calm (full protocols), 🟡 Urgent (streamlined), 🔴 Frustrated (minimal)
- **Use when:** ALWAYS (Step 0, before everything else)
- **Key insight:** "Frustrated user who gets unblocked > Calm user who gets perfect process"

**Task Classification:** `TASK_CLASSIFICATION_PROTOCOL.md`  
- Classify as One-Off, Workflow, Pipeline, Protocol, Pattern, or Agent
- **Use when:** User presents any task (depth varies by sentiment)
- **Quick reference:** `TASK_TYPES_REFERENCE.md` for definitions

**Context-First:** `CONTEXT_FIRST_PROTOCOL.md`  
- Search for existing solutions before building from scratch
- **Use when:** Before executing any non-trivial task
- **Time:** 30s (Red) to 10min (Green) depending on sentiment

**Decision Matrix:** `DECISION_MATRIX_PROTOCOL.md`  
- Choose Results-Driven (for you, now) vs User-Driven (for others, later)
- **Use when:** After classifying task type

**PromptGen:** `PROMPTGEN_INTEGRATION_PROTOCOL.md`  
- Structured brainstorming (8-point checklist)
- **Use when:** Building Pipeline, Agent, Protocol, or Pattern (skip if Red/Frustrated)
- **Time:** 3-5 minutes of analysis

**Learning Fundamentals:** `LEARNING_FUNDAMENTALS_PROTOCOL.md`  
- Match teaching approach to user's learning style
- **Use when:** User says "walk me through" or shows confusion

**Quick Start:** `QUICK_START_GUIDE.md`
- 3-minute intro for users and AI
- Cheat sheets and examples

### Key Insights
> "5 minutes of structured thinking saves 50 minutes of rework"

> "Protocols serve the user, not the other way around"

> "Match the protocol to the moment"

These protocols emerged from real pain points over 2 days of meeting automation development, where:
- Not classifying upfront led to rework when "one-off" became repeatable
- Not searching context meant reinventing existing patterns
- Optimizing for wrong target meant rebuilding for actual users
- Skipping PromptGen meant missing edge cases (promotional emails, duplicates, empty transcripts)
- **Asking too many questions frustrated urgent users** ⚡ NEW

---

## 🚨 CRITICAL PROTOCOLS (MUST FOLLOW)

### 1. Workflow Orchestration Protocol 🎯 NEW
**Status:** ✅ **ACTIVE**  
**Requirement:** Use for all tasks unless user says "skip protocols"  
**Applies to:** ALL task execution  
**File:** `WORKFLOW_ORCHESTRATION_PROTOCOL.md`

### 2. Message Counter Protocol ✨
**Status:** ✅ **ACTIVE**  
**Requirement:** Display message counter on EVERY response  
**Applies to:** ALL Cascade instances  
**No exceptions**

### 3. Deep Dive Research Protocol 🔍
**Status:** ✅ **ACTIVE**  
**Requirement:** Use when user says "deep dive", "fully understand", or mentions repeated failures  
**Applies to:** System troubleshooting, architecture analysis, debugging  
**File:** `DEEP_DIVE_RESEARCH_PROTOCOL.md`

### 4. Exit Protocols
**Status:** ✅ Active  
**Requirement:** Run exit protocol before closing production chats  
**Applies to:** HCSS, Joju, Phil's Ledger focuses

### 5. Brain Refresh Protocol
**Status:** ⚠️ Recommended  
**Requirement:** Suggest refresh at 50 messages (exploratory)  
**Applies to:** Long exploratory chats

---

## 📊 Protocol Compliance

### How to Verify
1. Check if message counter appears at end of responses
2. Verify counter increments correctly
3. Confirm warnings appear at thresholds
4. Validate mode detection is correct

### If Protocol Not Followed
- 🚨 **Red flag:** AI not properly loaded
- 🚨 **Action:** Close chat and start fresh
- 🚨 **Report:** Note which protocol was violated

---

## 🔄 Protocol Updates

### Version History
- **v3.2.0 (2025-11-13):** Added 6 Workflow Protocols (Orchestration, Classification, Context-First, Decision Matrix, PromptGen, Learning Fundamentals)
- **v3.1.0 (2025-11-12):** Added Deep Dive Research Protocol
- **v3.0.0 (2025-11-09):** Added message counter protocol
- **v2.1.0:** Added learning protocol
- **v2.0.0:** Initial protocol structure

### Update Process
1. Create/modify protocol JSON
2. Update this README
3. Update main README.md
4. Test with new Cascade instance
5. Validate compliance

---

## 📝 Notes

### Protocol Loading
- Protocols are loaded via checkpoint at chat start
- Some protocols may be loaded dynamically (focus activation)
- Message counter protocol is ALWAYS active

### Protocol Priority
1. **Critical protocols** (message counter, exit) - MUST follow
2. **Focus protocols** (HCSS, Joju) - Required in focus mode
3. **Optional protocols** (learning) - Recommended but not required

### Troubleshooting
- **Counter not showing?** → AI not properly loaded, restart chat
- **Wrong threshold?** → Mode detection issue, verify mode
- **No warnings?** → Check protocol version

---

## 🎯 Quick Reference

**Message Counter Format:**
```
💬 Message {current}/{threshold} | Mode: {mode} | {status}
```

**Thresholds:**
- Production: 100 max
- Exploratory: 50 refresh, 150 warning
- Ad-hoc: 20 max

**Commands:**
- `refresh brain` or `rb` - Refresh brain state
- `hide counter` - Hide counter (current chat only)
- `show counter` - Show counter again
- `message count` - Check current count

---

**For full protocol details, see individual JSON files in this directory.**
