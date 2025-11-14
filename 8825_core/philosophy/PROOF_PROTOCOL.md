# Proof Protocol

**Official Name:** Usage-Driven Evolution (UDE)  
**Common Name:** Proof Protocol  
**Descriptive Name:** Adaptive Learning System (ALS)  
**Status:** Production Ready  
**Date Formalized:** 2025-11-13

---

## What It Is

**"You don't decide what survives - usage does."**

The Proof Protocol is the meta-principle that governs how learnings, principles, and knowledge evolve within the 8825 system. It's natural selection for knowledge: only what proves useful through actual usage survives and promotes.

---

## Core Philosophy

### The Four Barriers to Survival

Every learning must pass through four barriers to normalize:

1. **Trial Barrier** - Does anyone try it?
2. **Success Barrier** - Does it work?
3. **Context Barrier** - Does it work elsewhere?
4. **Time Barrier** - Is it still relevant?

**Only learnings that pass ALL barriers normalize.**

---

## Key Principles

### 1. Merit Through Usage
Learnings prove value through actual use, not manual curation or opinion.

### 2. Natural Selection Over Manual Curation
The system evolves itself based on success rates. No committees, no voting.

### 3. Time-Based Decay
Old/unused knowledge naturally fades using exponential decay (default: 180-day half-life).

### 4. Evidence-Based Promotion
- **Active → Promoted:** 3+ successful uses with positive outcomes
- **Active → Decaying:** Not used in 30+ days or superseded
- **Decaying → Deprecated:** Not used in 90+ days

### 5. Context Preservation
Most learnings (90%) stay context-specific. Only 10% normalize across all contexts.

### 6. Automatic Evolution
Zero manual effort. The system runs continuously via Brain Sync Daemon.

---

## How It Works

### Decay Formula
```
confidence_now = original_confidence × (0.5 ^ (age_days / half_life_days))
```

**Default half-life:** 180 days
- 6 months: 50% confidence
- 12 months: 25% confidence
- 18 months: 12.5% confidence

**Reset:** Using a learning resets its decay clock.

### Status Transitions
```
Active (confidence ≥ 0.5)
    ↓ (not used 30+ days)
Legacy (0.3 ≤ confidence < 0.5)
    ↓ (not used 90+ days)
Deprecated (confidence < 0.3)
    ↓ (superseded or failed)
Archived
```

### Promotion Path
```
Created → Active
    ↓ (3+ successful uses)
Promoted (normalized across contexts)
```

---

## Survival Rates

### By Learning Type
- **Decisions:** 20% normalize (most are context-specific)
- **Patterns:** 40% normalize (can generalize)
- **Policies:** 60% normalize (apply broadly)
- **Solutions:** 30% normalize (usually specific)
- **Mistakes:** 70% normalize (anti-patterns are universal)

### Overall Distribution
```
100 learnings captured
├── 60 die (never tried or failed)
├── 30 stay context-specific
└── 10 normalize (work across contexts)
```

---

## Implementation

### Components

1. **learning_extractor.py** - Captures learnings with evolution metadata
2. **usage_tracker.py** - Records usage and success/failure
3. **decay_engine.py** - Applies time-based decay
4. **tool_evolution_detector.py** - Detects tool replacements
5. **competition_resolver.py** - Determines winners in tool competitions
6. **brain_sync_daemon.py** - Runs everything automatically (30s cycle)

### Usage Tracking
```python
from usage_tracker import UsageTracker

tracker.record_usage(
    learning_id="abc123",
    success=True,
    context="Production deployment"
)
```

### Principle Tracking
```python
from principle_tracker import PrincipleTracker

tracker.record_usage(
    principle_title="Friction is a Feature Flag",
    decision_context="Deciding on screenshot selection UX",
    impact_type="prevented_mistake"
)
```

---

## Real-World Example

### Tool Evolution Scenario

```
Day 1: "Use Graph API for TGIF"
→ Created, confidence 0.9, status: active

Day 30: Used 5 times, 80% success
→ Confidence stays 0.9 (recent use)
→ Status: active

Day 180: Not used in 6 months
→ Confidence decays to 0.45
→ Status: legacy

Day 181: "Migrated from Graph API to SuperAPI"
→ Competition starts
→ Both tracked

Day 190: SuperAPI 10 tries, 90% success
         Graph API 10 tries, 60% success
→ SuperAPI wins (20%+ better)
→ Graph API marked as "superseded"
→ Status: deprecated

Day 365: Graph API confidence < 0.3
→ Status: archived
```

---

## Why It Works

### 1. Most Learnings Should NOT Normalize
**Reality:** Only 10% of learnings work across all contexts.

**Why:** Context matters. "Use Graph API for TGIF" is different from "Use Graph API everywhere."

### 2. Evolution is Natural
Don't fight it - track it. Show the journey:
```
v1: "Use Graph API for TGIF"
v2: "Use Graph API generally" (tried 3 times, 2 succeeded)
v3: "Use Graph API [requires IT]" (constraint added after failure)
```

### 3. Context Drift is Prevented by Evolution
Not by rules - by natural selection.

Bad generalizations fail → Get marked as failed → Die naturally.

### 4. The System Self-Corrects
- Bad learnings die (low success rate)
- Good learnings survive (high success rate)
- Context-specific learnings stay specific
- Universal learnings normalize

---

## Success Metrics

### Capture Rate
- **Goal:** 95%+ of learnings captured automatically
- **Status:** ✅ Achieved

### Survival Rate
- **Goal:** 10% normalize, 30% stay specific, 60% die
- **Status:** 🔄 Measuring after 3 months

### Conflict Rate
- **Goal:** <2% require manual resolution
- **Status:** 🔄 Measuring after 3 months

### Evolution Speed
- **Goal:** Tool replacements detected within 1 week
- **Status:** ✅ Achieved

---

## When to Use Each Name

### "Proof Protocol" (Day-to-Day)
- Code comments
- Team discussions
- Quick references
- "That's Proof Protocol working"

### "Usage-Driven Evolution" (Formal)
- Documentation headers
- Architecture diagrams
- Technical presentations
- Research papers

### "Adaptive Learning System" (Descriptive)
- Explaining to new users
- Marketing materials
- Non-technical stakeholders
- Product descriptions

---

## Integration Points

### Brain System
- Runs automatically via `brain_sync_daemon.py`
- 30-second check cycle
- Broadcasts updates to active Cascades

### Philosophy Layer
- Tracks principle usage via `principle_tracker.py`
- Updates PHILOSOPHY.md metadata
- Generates usage reports

### Content Index
- Applies to file relevance scoring
- Decays old content naturally
- Promotes frequently accessed content

---

## The Beautiful Part

**You don't decide what survives - usage does.**

- Used a lot + high success = survives and normalizes
- Used rarely or fails = dies
- Natural selection, not manual curation

**The system evolves itself.**

---

## Related Documentation

- **Technical Deep Dive:** `8825_core/philosophy/learning_evolution_system.md`
- **Brain Integration:** `8825_core/brain/TETHERED_BRAIN_PROTOCOL.md`
- **Usage Tracking:** `8825_core/brain/usage_tracker.py`
- **Decay Engine:** `8825_core/brain/decay_engine.py`
- **Principle Tracking:** `8825_core/philosophy/principle_tracker.py`

---

**Status:** ✅ Production Ready  
**Effort to Use:** 0 seconds (automatic)  
**Value:** Knowledge stays current, tools evolve naturally, context preserved
