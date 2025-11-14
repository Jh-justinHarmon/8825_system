# Teaching Tickets Filed to Roadmap

**Date:** 2025-11-08

---

## Summary

Both teaching tickets from inbox ingestion have been reviewed and filed to appropriate roadmap queues based on user direction.

---

## Filed Items

### 1. TV Memory Layer → Foundation Sprint
**Ticket:** T-8825-20251108-163055  
**Filed to:** Foundation Sprint Backlog  
**Roadmap ID:** proto-002  
**Priority:** HIGH  
**Effort:** 20 hours (large)

**What it is:**
- TV Memory Layer thought experiment
- Bookmark model + Siri-first interface
- Passive memory capture and retrieval

**AI Analysis:**
- 11 touchpoints
- 1 high-severity conflict (achievement_detection.json)
- System-wide blast radius
- Recommendation: Refactor existing patterns

**Questions to answer:**
- System-wide or Team76-specific?
- Integrate with existing achievement detection?
- How does it fit with Joju mining patterns?

**Status:** Queued for foundation sprint

---

### 2. 8825+Goose Integration → Next Release
**Ticket:** T-8825-20251108-163843  
**Filed to:** Refactor Queue  
**Roadmap ID:** refactor-002  
**Priority:** MEDIUM  
**Effort:** 16 hours (large)

**What it is:**
- Two-layer automation pattern
- 8825 = brain/context layer
- Goose = execution layer via MCP

**AI Analysis:**
- 14 touchpoints
- 1 high-severity conflict (4 critical patterns)
- System-wide blast radius
- Recommendation: Refactor existing patterns

**Affected Critical Patterns:**
- TGIF auto-route
- Achievement detection
- MCP inbox server
- Universal inbox watch

**Use Cases:**
- Scanned letter → OCR → 8825 → Goose calendar events
- Achievement detection → 8825 context → Goose mining
- TGIF notes → 8825 routing → Goose distribution

**Status:** Queued for next release (after foundation sprint)

---

## Roadmap Status

### Foundation Sprint Backlog (2 items)
1. **proto-001:** MCP Input Hub (6.5h) - depends on refactor-001
2. **proto-002:** TV Memory Layer (20h) - no dependencies

**Total effort:** 26.5 hours (~3-4 days)

### Refactor Queue (2 items)
1. **refactor-001:** Extract shared ingestion core (4h) - no dependencies
2. **refactor-002:** 8825+Goose integration (16h) - no dependencies

**Total effort:** 20 hours (~2.5 days)

---

## Recommended Sequence

### Foundation Sprint (Current)
1. Build refactor-001 (4h) - enables proto-001
2. Build proto-002 (20h) - TV Memory Layer
3. Build proto-001 (6.5h) - Input Hub Phase 2

**Total:** 30.5 hours (~4 days)

### Next Release
1. Build refactor-002 (16h) - 8825+Goose integration

**Total:** 16 hours (~2 days)

---

## Teaching Ticket Status

Both tickets updated:
- `status`: "filed_to_roadmap"
- `roadmap_id`: proto-002 / refactor-002
- `roadmap_queue`: foundation_sprint_backlog / refactor_queue

**Location:** `~/Downloads/8825_inbox/processing/teaching_tickets/`

---

## Next Steps

1. **Review foundation sprint items** - Prioritize proto-002 vs proto-001
2. **Clarify TV Memory Layer scope** - System-wide or Team76?
3. **Plan integration approach** - How to refactor achievement detection?
4. **Schedule sprint** - When to start foundation sprint?

---

**All teaching tickets filed and tracked in roadmap system.**
