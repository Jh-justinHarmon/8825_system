# 8825 Philosophy

**Last Updated:** November 11, 2025  
**Version:** 2.0

---

## Architecture Position

**Philosophy is Tier 3 in the system hierarchy:**

```
USER REQUEST
    ↓
🧠 BRAIN (Tier 1: Master Controller)
    ↓
├─ Learning Principles (Tier 2: How to learn)
├─ Decision Matrix (Tier 2: What to prioritize)
├─ PromptGen (Tier 2: How to execute)
    ↓
    └─ PHILOSOPHY.md (Tier 3: Contextualization)
         ↓
         └─ Implementation decisions
```

**What This Means:**
- **Brain** routes all requests and orchestrates meta-systems
- **Meta-Systems** (Learning Principles, Decision Matrix, PromptGen) provide strategy
- **Philosophy** provides implementation context and wisdom
- Philosophy does NOT override Brain—it contextualizes Brain's decisions

**Example Flow:**
1. Brain receives: "Build screenshot processor"
2. Decision Matrix: "Quick win, high value, ship it"
3. PromptGen: "Build with low friction automation"
4. Philosophy provides context: "Friction is a Feature Flag" → No manual steps

---

## Table of Contents

1. [Core Principles (Iron-Clad)](#core-principles-iron-clad)
2. [Automation Principles](#automation-principles)
3. [Validation & Trust](#validation--trust)
4. [Documentation](#documentation)
5. [Delivery & Communication](#delivery--communication)
6. [Execution Philosophy](#execution-philosophy)
7. [Learning Loop Integration](#learning-loop-integration)
8. [Principle Evolution & Decay](#principle-evolution--decay)

---

## Iron-Clad Principles

> **Source:** Direct user direction  
> **Status:** Permanent unless explicitly challenged and approved for change  
> **Last Review:** November 11, 2025

### Ship Week Protocol
**Established:** November 10, 2025  
**Principle:** When stuck in planning mode, shift to execution. Focus on shipping lowest-hanging fruit first. Quick wins build momentum.

**Application:**
- Declare "Ship Week" when planning exceeds execution
- Identify 3-5 quick wins
- Ship incrementally, document as you go
- Build momentum through delivery

**Validation:** Session Nov 10-11 shipped 3 major deliverables in one session

---

## Learned Principles

### Automation Principles

> **Source:** Session learnings  
> **Status:** Active - tracked for usefulness  
> **Promotion Criteria:** Used in 3+ sessions with positive outcomes

### 1. Friction is a Feature Flag
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** If automation requires manual intervention mid-flow, treat it as incomplete.

**Test:** Can a user trigger it and walk away? If no, it's not automated—it's assisted. True automation has zero friction points after initiation.

**Example:** Screengrab Swap v1 (manual selection) vs v2 (auto-thumbnail)

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### 2. File Location = Processing State
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** Use physical location to indicate processing status, not just metadata.

**Pattern:** File/folder location should communicate processing state at a glance. Inbox = unprocessed, Archive = processed, Error = failed. User should know state by looking at folder structure, not reading metadata.

**Example:** Screenshots main folder → `- ARCHV -` after OCR

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### 3. Context-Specific Protocols > Generic Rules
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** One detection engine + multiple protocol handlers scales better than one-size-fits-all rules.

**Pattern:** Build systems with: (1) Universal detection layer, (2) Context-specific protocol handlers. Don't force different content types through the same processing logic.

**Structure:**
```
Detect → Route → Protocol-specific handling
```

**Example:** OCR engine detects content type → routes to KARSEN/bill/standard protocol

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### Validation & Trust

> **Source:** Session learnings  
> **Status:** Active - tracked for usefulness

### 1. Precision Over Recall in Validation
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** In systems that affect trust (task boards, data validation), false positives are worse than false negatives.

**Rule:** When validating state (task completion, data accuracy), optimize for precision. Better to flag 4 items you're 90% sure about than 22 you're 60% sure about. False positives damage system trust permanently.

**Example:** Enhanced validator (4 high-confidence) vs basic validator (22 mixed-confidence)

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### 2. Read-Only Validation Builds Trust
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** Validate production systems without modification rights first.

**Pattern:** When working with production code/data, start with read-only operations. Validate, report, get approval, then modify. This builds trust and prevents accidents.

**Application:** Git repos, task boards, and production databases should be read-only until validation proves changes are safe.

**Example:** Joju git repo treated as read-only throughout entire Task Truth Pipeline

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### 3. Evidence Triangulation > Single Source
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** Multiple weak signals > one strong signal in validation.

**Pattern:** Don't rely on single evidence type. Triangulate: git commits + imports + tests + keywords = high confidence. Any one alone = low confidence. Build systems that aggregate multiple evidence sources and score confidence.

**Example:** 6 validation techniques vs keyword matching alone (4.7x improvement)

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### 4. Preview → Confirm → Execute → Report
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** Bulk operations must show intent before execution.

**Pattern:** Never auto-execute bulk changes. Always:
1. Preview what will change
2. Get explicit confirmation
3. Execute with progress
4. Report results

**Rule:** User should see the plan before it runs.

**Example:** 22 task promotions shown in table → user confirms → execute → summary report

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### Documentation

> **Source:** Session learnings  
> **Status:** Active - tracked for usefulness

### Documentation Discoverability ≠ Documentation Existence
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** Creating docs is table stakes. Making them discoverable is the real work.

**Requirements:** Every system needs:
1. Entry point (README)
2. Index (DOCUMENTATION_INDEX.md)
3. Cross-links between related docs
4. Clear structure (numbered sections, ToC)

**Rule:** If user has to search for docs, they don't exist.

**Example:** Created `DOCUMENTATION_INDEX.md` + links in main README

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### Delivery & Communication

> **Source:** Session learnings  
> **Status:** Active - tracked for usefulness

### Markdown for Dev, Word for Stakeholders
**Added:** 2025-11-11  
**Use Count:** 0  
**Last Used:** Never  
**Status:** Active

**Principle:** Format follows audience, not preference.

**Strategy:**
- **Internal docs** = Markdown (version control, diffs, speed)
- **External deliverables** = Word/PDF (formatting, shareability, familiarity)

**Rule:** Don't force stakeholders to read Markdown. Don't force developers to edit Word. Build export pipelines.

**Example:** Bug report in MD → exported to DOCX for team

**Decision Impact:**
- [ ] Used in design decisions
- [ ] Prevented a mistake
- [ ] Improved user experience

---

### Execution Philosophy

> **Source:** Direct user direction + session validation  
> **Status:** Iron-Clad Principles

### Ship Week Protocol (Validated)
**Established:** 2025-11-10  
**Validated:** 2025-11-11  
**Use Count:** 1  
**Last Used:** 2025-11-11  
**Status:** Iron-Clad

**Principle:** Focus on shipping over planning. Execute lowest-hanging fruit first.

**Validation Results:**
- ✅ 3 quick wins shipped in one session
- ✅ All deliverables production-ready
- ✅ Clear next steps identified
- ✅ Momentum built through delivery

**Pattern:**
1. Identify stuck planning mode
2. Declare Ship Week
3. List 3-5 quick wins
4. Ship incrementally
5. Document as you go (not after)

**Decision Impact:**
- [x] Used in design decisions
- [x] Prevented a mistake (over-planning)
- [x] Improved user experience

---

### Learning Loop Integration

> **Source:** Meta-learning from session  
> **Status:** Iron-Clad Principles

### Philosophy Evolution Process
**Added:** 2025-11-11  
**Status:** Iron-Clad

**Principle:** Philosophy should update based on session learnings.

**Process:**
1. After significant sessions, review learnings
2. Ask: "What principle would have prevented this mistake?" or "What principle made this work?"
3. Add to philosophy document with tracking metadata
4. Track usage and impact
5. Promote useful principles, decay unused ones

**Rule:** Philosophy is living, not static.

---

### Principle Evolution & Decay

> **Source:** User direction  
> **Status:** Iron-Clad Principles

### Tracking System

Each learned principle tracks:
- Added Date: When principle was added (YYYY-MM-DD format)
- Use Count: How many times it informed a decision (integer value)
- Last Used: Most recent application (YYYY-MM-DD or Never)
- Decision Impact: What it helped with (checkboxes)
- Status: Active / Promoted / Decaying / Deprecated / Iron-Clad

### Promotion Criteria

**Active → Promoted:**
- Used in 3+ sessions
- Positive outcomes each time
- User validates usefulness
- Becomes "Iron-Clad" candidate

**Active → Decaying:**
- Not used in 30+ days
- Superseded by better principle
- Context changed (no longer relevant)

**Decaying → Deprecated:**
- Not used in 90+ days
- Actively harmful or misleading
- User explicitly removes

### Challenge Protocol

**For Iron-Clad Principles:**
- AI can challenge if principle appears irrelevant
- Must provide: (1) Evidence of irrelevance, (2) Proposed alternative, (3) Impact analysis
- User has final approval
- Requires explicit "approved for change" confirmation

**For Learned Principles:**
- AI can deprecate after 90 days of non-use
- Must document: (1) Why it decayed, (2) What replaced it (if anything)
- User notified of deprecation

### Review Schedule

**Weekly:** Check use counts, update "Last Used" dates  
**Monthly:** Review decaying principles, consider deprecation  
**Quarterly:** Review iron-clad principles for relevance  
**Annually:** Full philosophy audit

---

## Principle Status Summary

### Iron-Clad (User-Directed)
- Ship Week Protocol ✅ Validated

### Active (Tracking for Promotion)
- Friction is a Feature Flag (0 uses)
- File Location = Processing State (0 uses)
- Context-Specific Protocols > Generic Rules (0 uses)
- Precision Over Recall in Validation (0 uses)
- Read-Only Validation Builds Trust (0 uses)
- Evidence Triangulation > Single Source (0 uses)
- Preview → Confirm → Execute → Report (0 uses)
- Documentation Discoverability ≠ Documentation Existence (0 uses)
- Markdown for Dev, Word for Stakeholders (0 uses)

### Decaying
- None

### Deprecated
- None

---

## Usage Notes

**For AI:**
- **IMPORTANT:** Philosophy is Tier 3 - Brain, Learning Principles, Decision Matrix, and PromptGen supersede this
- Reference this document when making **implementation** decisions (not strategic decisions)
- Philosophy provides context for HOW to execute what Brain decides
- Update "Use Count" and "Last Used" when applying a principle
- Check "Decision Impact" boxes when principle helps
- Flag principles for decay after 30 days of non-use
- Challenge iron-clad principles if evidence suggests irrelevance

**For User:**
- Review monthly to see which principles are useful
- Promote principles that consistently deliver results
- Remove principles that become stale
- Add new iron-clad principles as needed
- Remember: Philosophy contextualizes strategy, doesn't create it

---

## Changelog

### Version 2.0 - November 11, 2025
- **Added architecture position clarification** - Philosophy is Tier 3 contextualization layer
- Clarified hierarchy: Brain → Meta-Systems → Philosophy → Implementation
- Added 9 learned principles from Task Truth Pipeline session
- Established principle evolution & decay system
- Added tracking metadata (use count, last used, decision impact)
- Created promotion/decay criteria
- Established challenge protocol for iron-clad principles
- Validated Ship Week Protocol with session results

### Version 1.0 - November 10, 2025
- Established Ship Week Protocol (iron-clad)
- Initial philosophy document created

---

**Philosophy Status:** Living document, actively evolving based on session learnings and usage patterns.

**Architecture Status:** Tier 3 - Subordinate to Brain, Learning Principles, Decision Matrix, and PromptGen.
