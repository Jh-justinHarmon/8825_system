# 8825 Inbox Ingestion System

**Intelligent two-lane inbox processing with AI system-wide analysis**

Prevents system drift by forcing AI sweep before behavior-changing patterns are implemented.

---

## Quick Start

### Process Inbox

```bash
cd 8825_core/inbox
python3 ingestion_engine.py process
```

### Check Stats

```bash
python3 ingestion_engine.py stats
```

### Review Teaching Tickets

```bash
python3 ingestion_engine.py tickets list
```

---

## How It Works

### Two-Lane Architecture

**Lane A - Auto-Assimilation (Safe Items)**
- Meeting notes, achievements, personal reminders
- Automatic: validate → dedupe → integrate → done
- No human approval needed

**Lane B - AI Sweep (Behavior Changes)**
- Workflows, protocols, agents, routing changes
- AI searches entire system for touchpoints & conflicts
- Creates teaching ticket for human review
- Only then gets built

---

## File Flow

```
~/Downloads/8825_inbox/pending/
    ↓
Validation & Classification
    ↓
┌─────────────────┬─────────────────┐
│   Lane A        │   Lane B        │
│   (Auto)        │   (AI Sweep)    │
└─────────────────┴─────────────────┘
    ↓                     ↓
completed/        teaching_tickets/
```

---

## Classification

Every inbox item gets 5 dimensions:

1. **content_type** - mining_report, achievement, pattern, note, feature, decision
2. **target_focus** - joju, hcss, team76, jh
3. **scope_intent** - local, focus-wide, system-wide
4. **change_pressure** - low, medium, high
5. **source_channel** - chatgpt, windsurf, manual, external

**Routing Decision:**
- `change_pressure=low` + `scope_intent=local` → Lane A
- `change_pressure=medium/high` → Lane B
- `scope_intent=system-wide` → Lane B

---

## Lane A: Auto-Assimilation

### What Happens

1. **Validate** - Check JSON schema
2. **Classify** - Extract 5 dimensions
3. **Dedupe** - Hash-based duplicate detection
4. **Integrate** - Write to correct focus location
5. **Index** - Update search index
6. **Complete** - Move to completed/

### Integration Targets

- `joju` → `joju_sandbox/libraries/justin_harmon_master_library.json`
- `hcss` → `focuses/hcss/knowledge/`
- `team76` → `focuses/joju/projects/`
- `jh` → `users/justinharmon/personal/`

### Example

```json
{
  "content_type": "note",
  "target_focus": "hcss",
  "content": {
    "title": "Client Call Notes",
    "summary": "Discussed Q1 timeline"
  },
  "metadata": {
    "source": "chatgpt",
    "timestamp": "2025-11-08T16:00:00"
  }
}
```

**Result:** Auto-integrated to `focuses/hcss/knowledge/20251108_note.md`

---

## Lane B: AI System-Wide Sweep

### What Happens

1. **Extract Keywords** - From proposed change
2. **Find Touchpoints** - Grep search across workspace
3. **Find Related Patterns** - Similar in other focuses
4. **Detect Conflicts** - Check critical rules
5. **Calculate Blast Radius** - local / focus-wide / system-wide
6. **Generate Teaching Ticket** - With AI findings

### Teaching Ticket Contains

- **Proposed Change** - What's being suggested
- **Touchpoints** - Files that would be affected (with relevance %)
- **Related Patterns** - Similar solutions elsewhere
- **Conflicts** - Potential issues (with severity)
- **Blast Radius** - Scope of impact
- **Questions** - Smart questions for review
- **Recommendation** - AI's suggestion
- **Required Mode** - teaching_mode or brainstorm_mode

### Example Output

```
Touchpoints: 10 files found
Conflicts: 1 (scope mismatch)
Blast Radius: system-wide
Recommendation: "Consider narrowing scope to specific focus"
Required Mode: teaching_mode
```

---

## Configuration

### Classification Rules

`config/classification_rules.json`

```json
{
  "change_pressure_keywords": {
    "high": ["workflow", "protocol", "agent", "auto-route"],
    "medium": ["pattern", "feature"],
    "low": ["note", "achievement", "mining"]
  }
}
```

### Integration Targets

`config/integration_targets.json`

```json
{
  "hcss": {
    "type": "folder",
    "path": "focuses/hcss/knowledge",
    "file_naming": "{date}_{content_type}.md"
  }
}
```

### Critical Rules

`config/critical_rules.json`

Protected patterns that trigger high-severity conflicts:
- TGIF Auto-Route
- Joju Achievement Detection
- 3-Mode System
- MCP Inbox Server
- Universal Inbox Watch

---

## CLI Commands

### Process Inbox

```bash
# Process all pending files
python3 ingestion_engine.py process

# Process specific file
python3 ingestion_engine.py process --file pending/myfile.json
```

### View Stats

```bash
python3 ingestion_engine.py stats
```

Output:
```json
{
  "pending": 0,
  "lane_a": 3,
  "lane_b": 12,
  "completed": 8,
  "errors": 0
}
```

### Review Teaching Tickets

```bash
# List all tickets
python3 ingestion_engine.py tickets list

# View specific ticket
python3 ingestion_engine.py tickets view T-8825-20251108-161230

# Approve ticket
python3 ingestion_engine.py tickets approve T-8825-20251108-161230

# Reject ticket
python3 ingestion_engine.py tickets reject T-8825-20251108-161230 --reason "Too broad"
```

---

## Folder Structure

```
8825_core/inbox/
├── ingestion_engine.py          # Main orchestrator
├── validators.py                # Schema validation
├── classifier.py                # 5-dimension classification
├── weighting.py                 # Priority calculation
├── deduplicator.py             # Hash-based dedupe
├── lane_a_processor.py          # Auto-assimilation
├── lane_b_processor.py          # AI sweep orchestrator
├── ai_sweep.py                  # System-wide pattern search
├── teaching_ticket_generator.py # Ticket creation
└── config/
    ├── classification_rules.json
    ├── integration_targets.json
    └── critical_rules.json

~/Downloads/8825_inbox/
├── pending/                     # New files
├── processing/
│   ├── lane_a/                 # Auto-processing
│   ├── lane_b/                 # Awaiting AI sweep
│   └── teaching_tickets/       # Human review needed
├── completed/                   # Successfully processed
└── errors/                      # Validation failures
```

---

## Index

`8825_index/inbox_index.json`

Tracks all processed items for deduplication and search:
- Content hash
- Keywords
- Target location
- Timestamp

---

## Success Metrics

### Lane A
- ✅ 90%+ correct routing
- ✅ Zero duplicates created
- ✅ Files in correct locations
- ✅ Index stays consistent

### Lane B
- ✅ AI finds 80%+ of touchpoints
- ✅ Conflicts are real (not false alarms)
- ✅ Teaching tickets are actionable
- ✅ Questions help decision-making

---

## Troubleshooting

### File Goes to Wrong Lane

Check `config/classification_rules.json` keywords. Adjust thresholds if needed.

### Duplicate Not Detected

Index may be out of sync. Check `8825_index/inbox_index.json`.

### AI Sweep Misses Touchpoints

Keywords may be too narrow. Check `ai_sweep.py` keyword extraction.

### Teaching Ticket Questions Not Helpful

Adjust `teaching_ticket_generator.py` question generation logic.

---

## What's Next

After human reviews teaching ticket:
1. Approve → Move to Brainstorm Mode
2. Design solution with full context
3. Export to Windsurf for Dev Mode
4. Build and test
5. Log as promoted pattern

---

## Philosophy

**Lane A:** Trust but verify (automatic with audit trail)  
**Lane B:** Widen the lens first (AI research before human decision)

**Goal:** Prevent narrow-context solutions from creating system-wide drift.

---

**Status:** Production Ready  
**Version:** 1.0  
**Built:** 2025-11-08
