# 8825 Roadmap System

**Two-part workflow for managing future work.**

---

## The Two Queues

### 1. Refactor Queue
**File:** `refactor_queue.json`

**What goes here:**
- Incremental improvements to existing code
- Technical debt items
- Performance optimizations
- Code cleanup/consolidation
- Dependency updates
- Documentation improvements

**When to use:**
- ✅ Improving existing code structure
- ✅ Removing duplication
- ✅ Optimizing performance
- ✅ Cleaning up tech debt

### 2. Foundation Sprint Backlog
**File:** `foundation_sprint_backlog.json`

**What goes here:**
- New features/capabilities
- Prototypes to validate
- Architectural experiments
- Greenfield work
- New integrations
- Proof of concepts

**When to use:**
- ✅ Building new feature
- ✅ Prototyping capability
- ✅ Experimenting with architecture
- ✅ Adding new integration

---

## Schema

### Refactor Queue Item
```json
{
  "id": "refactor-001",
  "title": "Short descriptive title",
  "description": "Detailed description",
  "source": "where this came from",
  "source_id": "reference ID",
  "priority": "high|medium|low",
  "effort": "small|medium|large",
  "effort_hours": 4,
  "impact": "high|medium|low",
  "dependencies": ["refactor-002"],
  "tags": ["architecture", "performance"],
  "status": "queued|in_progress|complete",
  "created": "2025-11-08",
  "notes": "Additional context"
}
```

### Foundation Sprint Item
```json
{
  "id": "proto-001",
  "title": "Short descriptive title",
  "description": "Detailed description",
  "source": "where this came from",
  "priority": "high|medium|low",
  "effort": "small|medium|large",
  "effort_hours": 6.5,
  "impact": "high|medium|low",
  "dependencies": ["refactor-001"],
  "tags": ["mcp", "automation"],
  "status": "queued|in_progress|complete",
  "prototype_goals": [
    "Goal 1",
    "Goal 2"
  ],
  "success_criteria": "How we know it works",
  "created": "2025-11-08"
}
```

---

## Priority Levels

### High
- Blocks other work
- High impact + low effort (quick win)
- Critical dependency

### Medium
- Valuable but not blocking
- Medium effort/impact

### Low
- Future consideration
- Low impact or high effort/low impact

---

## Effort Estimates

**Using calibrated time estimates (0.57x for complex, 0.56x for medium):**

- **Small:** < 4 hours
- **Medium:** 4-16 hours (1-2 days)
- **Large:** 16-40 hours (1 week)
- **XLarge:** > 40 hours (multi-week)

---

## Decision Tree

```
New item arrives
    ↓
Is it improving existing code?
    YES → Refactor Queue
    NO → Continue
    ↓
Is it a new capability/feature?
    YES → Foundation Sprint Backlog
    NO → Continue
    ↓
Is it a bug fix?
    YES → Immediate (not roadmap)
    NO → Needs clarification
```

---

## Workflow

### 1. Item Arrives (Inbox or Teaching Ticket)
Process and understand the item.

### 2. Decide: Immediate or Roadmap?
- **Immediate:** Do it now
- **Roadmap:** File for later

### 3. If Roadmap: Which Queue?
- **Refactor:** Improving existing code
- **Foundation:** New capability

### 4. Create Roadmap Item
Fill out schema with all details.

### 5. File to Queue
Add to appropriate JSON file.

### 6. Link Back
Reference roadmap ID in source item.

---

## Viewing and Filtering

### View by Priority
```bash
# High priority refactors
jq '.items[] | select(.priority == "high")' refactor_queue.json

# High priority prototypes
jq '.items[] | select(.priority == "high")' foundation_sprint_backlog.json
```

### View by Effort
```bash
# Quick wins (high impact, small effort)
jq '.items[] | select(.impact == "high" and .effort == "small")' refactor_queue.json
```

### View Ready Items
```bash
# No dependencies (ready to start)
jq '.items[] | select(.dependencies == [])' foundation_sprint_backlog.json
```

### View by Tag
```bash
# All automation items
jq '.items[] | select(.tags[] | contains("automation"))' foundation_sprint_backlog.json
```

---

## Sprint Planning

### 1. Review Queues
```bash
# Total items
jq '.meta.total_items' refactor_queue.json
jq '.meta.total_items' foundation_sprint_backlog.json
```

### 2. Identify Quick Wins
High impact + small effort items.

### 3. Check Dependencies
Ensure prerequisites are complete.

### 4. Estimate Capacity
How many hours available?

### 5. Select Items
Pick items that fit capacity.

### 6. Update Status
Change `status` to `in_progress`.

---

## Archive

When items are complete:
1. Update `status` to `complete`
2. Move to `archive/` folder
3. Update meta counts

---

## Integration with Inbox

### From Inbox Item
```json
{
  "inbox_item": {
    "id": "inbox-2025-11-08-001",
    "title": "Input Hub automation",
    "decision": "roadmap",
    "filed_to": "foundation_sprint_backlog",
    "roadmap_id": "proto-001",
    "status": "filed"
  }
}
```

### From Teaching Ticket
```json
{
  "teaching_ticket": {
    "id": "T-8825-20251108-163055",
    "decision": "refactor",
    "filed_to": "refactor_queue",
    "roadmap_id": "refactor-001",
    "status": "filed"
  }
}
```

---

## Current Items

### Refactor Queue (1 item)
- **refactor-001:** Extract shared ingestion core

### Foundation Sprint Backlog (1 item)
- **proto-001:** MCP Input Hub with context learning

---

## Files

```
Documents/roadmap/
├── refactor_queue.json           # Refactor items
├── foundation_sprint_backlog.json # New features
├── README.md                      # This file
└── archive/                       # Completed items
    ├── refactor_2025-11.json
    └── foundation_sprint_2025-12.json
```

---

**Created:** 2025-11-08  
**Status:** Active  
**Next Review:** 2025-11-15
