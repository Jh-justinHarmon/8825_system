# Protocol Tracking System

**Status:** ✅ Production Ready  
**Philosophy:** Proof Protocol (Usage-Driven Evolution)  
**Date:** 2025-11-13

---

## What It Does

Tracks when you consult protocols and applies **Proof Protocol** to determine which protocols are valuable:

- ✨ **Promoted:** 3+ uses with 70%+ success rate
- ✅ **Active:** Used recently with decent success
- ⏳ **Decaying:** Not used in 30+ days
- ❌ **Deprecated:** Not used in 90+ days OR low success rate
- 🆕 **Unused:** Never tracked

**"You don't decide what survives - usage does."**

---

## Quick Start

### Record Protocol Usage

```bash
# Successful use
./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --success --context "Debugging sync"

# Failed use
./track_protocol.py WORKFLOW_ORCHESTRATION --fail --notes "Too complex for this task"
```

### View Reports

```bash
# List all protocols
./track_protocol.py --list

# Show usage report
./track_protocol.py --report

# Show stats for specific protocol
./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --stats

# Filter by status
./track_protocol.py --list --status promoted
```

---

## How Proof Protocol Works

### The Four Barriers

Every protocol must pass through:

1. **Trial Barrier** - Does anyone use it?
2. **Success Barrier** - Does it work?
3. **Context Barrier** - Does it work in multiple contexts?
4. **Time Barrier** - Is it still relevant?

### Status Transitions

```
Created → Unused
    ↓ (first use)
Active (used recently, decent success)
    ↓ (3+ uses, 70%+ success)
Promoted (proven valuable)

OR

Active
    ↓ (not used 30+ days)
Decaying (confidence drops)
    ↓ (not used 90+ days OR low success)
Deprecated (marked for removal)
```

### Confidence Decay

Protocols decay over time if not used:
- **Half-life:** 90 days
- **30 days:** Starts decaying
- **90 days:** Deprecated

**Using a protocol resets its decay.**

---

## Usage Examples

### During Work

When you consult a protocol, immediately track it:

```bash
# Just used Deep Dive Research Protocol successfully
./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --success \
  --context "Downloads sync debugging" \
  --notes "Found Universal Inbox Watch running"

# Tried Workflow Orchestration but it was too complex
./track_protocol.py WORKFLOW_ORCHESTRATION_PROTOCOL --fail \
  --context "Simple automation task" \
  --notes "Overkill for this use case"
```

### Weekly Review

```bash
# See what's being used
./track_protocol.py --report

# Check promoted protocols
./track_protocol.py --list --status promoted

# Check decaying protocols (need attention)
./track_protocol.py --list --status decaying
```

### Monthly Audit

```bash
# Generate full report
./track_protocol.py --report > protocol_audit_$(date +%Y%m).md

# Review deprecated protocols
./track_protocol.py --list --status deprecated

# Consider removing or updating deprecated protocols
```

---

## What Gets Tracked

### Per Protocol

- **Use count** - How many times consulted
- **Successes** - Times it worked
- **Failures** - Times it didn't work
- **Success rate** - Percentage that worked
- **Contexts** - Where it was used
- **Last used** - When last consulted
- **Status** - Current Proof Protocol status
- **Confidence** - Current confidence level (0-1)

### Usage Log

Every use is logged to `state/protocol_usage.jsonl`:

```json
{
  "timestamp": "2025-11-13T18:45:00",
  "protocol_id": "DEEP_DIVE_RESEARCH_PROTOCOL",
  "protocol_name": "Deep Dive Research Protocol",
  "success": true,
  "context": "Debugging Downloads sync",
  "notes": "Found Universal Inbox Watch",
  "success_rate": 0.85
}
```

---

## Integration Points

### Manual Tracking (Current)

Use CLI tool during/after work:
```bash
./track_protocol.py PROTOCOL_NAME --success --context "What you did"
```

### Future: Automatic Tracking

Could integrate with:
- **Brain Sync Daemon** - Auto-detect protocol references in checkpoints
- **Cascade Check-ins** - Track which protocols Cascade consulted
- **Git Commits** - Parse commit messages for protocol mentions
- **IDE Integration** - Track when protocol files are opened

---

## Files & Structure

```
8825_core/protocols/
├── protocol_tracker.py       # Core tracking engine
├── track_protocol.py          # CLI tool (executable)
├── PROTOCOL_TRACKING_README.md # This file
└── state/                     # Tracking data
    ├── protocol_usage.jsonl   # Usage log
    └── protocol_metadata.json # Current stats
```

---

## Proof Protocol Rules

### Promotion Criteria

- **Minimum uses:** 3
- **Minimum success rate:** 70%
- **Result:** Status → "promoted", Confidence → 0.85-0.95

### Decay Criteria

- **Trigger:** Not used in 30+ days
- **Formula:** `confidence = 0.8 × (0.5 ^ (days_since_use / 90))`
- **Result:** Status → "decaying"

### Deprecation Criteria

Either:
- Not used in 90+ days
- 5+ uses with <40% success rate

**Result:** Status → "deprecated", Confidence → 0.2

---

## Benefits

### 1. Know What Works
See which protocols are actually useful vs. theoretical.

### 2. Identify Dead Weight
Find protocols that are never used or don't work.

### 3. Prioritize Updates
Focus on improving high-use protocols.

### 4. Natural Selection
Protocols prove value through usage, not opinion.

### 5. Context Awareness
See where protocols work vs. where they fail.

---

## Example Report

```
# Protocol Usage Report

**Generated:** 2025-11-13 18:45

---

## Summary

- **Total Protocols:** 32
- **Tracked Protocols:** 12
- **Total Uses:** 47
- **Average Uses:** 3.9

---

## By Status (Proof Protocol)

### ✨ Promoted (3)
*3+ uses with 70%+ success rate*

- **Deep Dive Research Protocol** - 8 uses, 88% success
- **Definition Of Done** - 5 uses, 80% success
- **Context First Protocol** - 4 uses, 75% success

### ✅ Active (5)
*Used recently with decent success*

- **Workflow Orchestration Protocol** - 3 uses, 67% success
- **Task Classification Protocol** - 2 uses, 100% success
- **Learning Fundamentals Protocol** - 2 uses, 50% success

### ⏳ Decaying (2)
*Not used in 30+ days*

- **Sentiment Aware Protocol** - Last used: 45 days ago
- **Partner Credit Protocol** - Last used: 62 days ago

### ❌ Deprecated (2)
*Not used in 90+ days OR low success rate*

- **8825 Mining** - 1 use, 0% success
- **8825 Message Counter Protocol** - Last used: 120 days ago

### 🆕 Unused (20)
*Never tracked*

- 8825 Cascade Hybrid
- 8825 Create Focus
- 8825 Decision Making
- ...
```

---

## Tips & Best Practices

### 1. Track Immediately
Record usage right after consulting a protocol while context is fresh.

### 2. Be Honest About Success
If protocol didn't help, mark it as failure. This data is valuable.

### 3. Add Context
Context helps understand where protocols work vs. don't work.

### 4. Review Weekly
Check report weekly to see patterns.

### 5. Update Decaying Protocols
If a protocol is decaying but still valuable, use it or update it.

### 6. Remove Deprecated
If a protocol is deprecated, consider removing or archiving it.

---

## Future Enhancements

### Automatic Detection
- Parse Cascade checkpoints for protocol mentions
- Track protocol file opens in IDE
- Detect protocol references in commits

### Cross-Protocol Analysis
- Which protocols are used together?
- Which protocols conflict?
- Which protocols are prerequisites?

### Recommendation Engine
- "You're working on X, consider consulting Y protocol"
- "This protocol has 85% success rate for similar tasks"

### Integration with Brain
- Brain Sync Daemon broadcasts protocol updates
- Cascades receive protocol recommendations
- Automatic decay application

---

## Related Documentation

- **Proof Protocol:** `8825_core/philosophy/PROOF_PROTOCOL.md`
- **Learning Evolution:** `8825_core/philosophy/learning_evolution_system.md`
- **Principle Tracking:** `8825_core/philosophy/principle_tracker.py`
- **Usage Tracking:** `8825_core/brain/usage_tracker.py`

---

**Status:** ✅ Ready to use  
**Effort:** 10 seconds per protocol use  
**Value:** Know which protocols actually work
