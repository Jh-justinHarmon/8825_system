# Philosophy Automation Layer

**Status:** Production Ready  
**Created:** November 11, 2025

---

## Overview

Automated system for philosophy evolution, principle tracking, and decay monitoring.

**Architecture Position:** Tier 3 - Subordinate to Brain, Learning Principles, Decision Matrix, and PromptGen

---

## Components

### 1. **Learning Extractor** (`learning_extractor.py`)
Auto-extracts learnings from session transcripts.

**Functions:**
- Extract learnings from sessions
- Identify patterns across learnings
- Propose new principles
- Validate existing principles

**Usage:**
```python
from learning_extractor import LearningExtractor

extractor = LearningExtractor()
learnings = extractor.extract_from_session(session_data)
report = extractor.generate_report(learnings)
```

---

### 2. **Principle Tracker** (`principle_tracker.py`)
Tracks principle usage in real-time.

**Functions:**
- Record principle usage
- Update use counts and last used dates
- Check for promotion candidates
- Generate usage statistics

**Usage:**
```python
from principle_tracker import PrincipleTracker

tracker = PrincipleTracker()
tracker.record_usage(
    "Friction is a Feature Flag",
    "Deciding on automation approach",
    impact_type="design"
)
```

---

### 3. **Decay Monitor** (`decay_monitor.py`)
Monitors and manages principle decay.

**Functions:**
- Check principles for decay (30+ days)
- Auto-deprecate stale principles (90+ days)
- Flag decaying principles
- Generate decay reports

**Usage:**
```python
from decay_monitor import DecayMonitor

monitor = DecayMonitor()
decay_status = monitor.check_decay()
monitor.auto_deprecate_stale(dry_run=False)
```

---

### 4. **Philosophy Manager** (`philosophy_manager.py`)
Orchestrates all philosophy automation.

**Functions:**
- Process sessions end-to-end
- Record principle usage
- Run weekly maintenance
- Generate health dashboard

**Usage:**
```python
from philosophy_manager import PhilosophyManager

manager = PhilosophyManager()

# Process session
result = manager.process_session(session_data)

# Weekly maintenance
manager.run_weekly_maintenance(auto_deprecate=True)

# Health dashboard
print(manager.get_dashboard())
```

---

## Workflows

### After Each Session

```bash
python3 philosophy_manager.py --process-session session_data.json
```

**What happens:**
1. Extracts learnings from transcript
2. Identifies patterns
3. Proposes new principles
4. Updates use counts for validated principles
5. Generates learning report

**Output:** `reports/learning_report_YYYY-MM-DD.md`

---

### During Decision-Making

```python
# When applying a principle
manager.record_principle_usage(
    "Precision Over Recall in Validation",
    "Choosing confidence threshold for validator",
    impact_type="design"
)
```

**What happens:**
1. Increments use count
2. Updates last used date
3. Logs usage with context
4. Updates PHILOSOPHY.md

---

### Weekly Maintenance

```bash
python3 philosophy_manager.py --weekly-maintenance
```

**What happens:**
1. Generates usage statistics
2. Checks all principles for decay
3. Flags principles not used in 30+ days
4. Auto-deprecates principles not used in 90+ days
5. Generates reports

**Output:**
- `reports/usage_report_YYYY-MM-DD.md`
- `reports/decay_report_YYYY-MM-DD.md`

---

## Thresholds

### Promotion
- **Active → Promoted:** 3+ uses with positive outcomes
- **Promoted → Iron-Clad:** User validation required

### Decay
- **Active → Decaying:** 30+ days no use
- **Decaying → Deprecated:** 90+ days no use

### Protection
- **Iron-Clad principles:** Cannot be auto-deprecated
- **AI can challenge:** With evidence, user approves

---

## File Structure

```
8825_core/philosophy/
├── learning_extractor.py      # Extract learnings from sessions
├── principle_tracker.py       # Track principle usage
├── decay_monitor.py           # Monitor decay and deprecate
├── philosophy_manager.py      # Orchestrate everything
├── logs/                      # Usage and deprecation logs
│   ├── principle_usage.jsonl
│   └── deprecations.jsonl
└── reports/                   # Generated reports
    ├── learning_report_*.md
    ├── usage_report_*.md
    └── decay_report_*.md
```

---

## Integration Points

### With Brain
- Brain routes session data to learning extractor
- Brain decides when to run weekly maintenance

### With Decision Matrix
- Principle usage informs decision prioritization
- High-use principles get more weight

### With PromptGen
- Principles contextualize execution approach
- Usage stats inform prompt generation

---

## Automation Status

✅ **Automated:**
- Learning extraction from sessions
- Principle usage tracking
- Decay detection
- Report generation
- Auto-deprecation (90+ days)

⚠️ **Manual Approval Required:**
- New principle proposals
- Principle promotions
- Iron-clad principle challenges

---

## Example: Full Workflow

```python
from philosophy_manager import PhilosophyManager

manager = PhilosophyManager()

# 1. After session ends
session_data = {
    'date': '2025-11-11',
    'objective': 'Build screenshot processor',
    'transcript': '...',
    'outcomes': [...]
}

result = manager.process_session(session_data)
print(f"Learnings extracted: {len(result['learnings'])}")
print(f"Proposals: {len(result['proposals'])}")

# 2. During development
manager.record_principle_usage(
    "Friction is a Feature Flag",
    "Chose auto-thumbnail over manual selection",
    impact_type="prevented_mistake"
)

# 3. Weekly maintenance
maintenance = manager.run_weekly_maintenance(auto_deprecate=True)
print(f"Deprecated: {len(maintenance['deprecated'])} principles")

# 4. Check health
print(manager.get_dashboard())
```

---

## Next Steps

1. **Integrate with Brain:** Route session data automatically
2. **Add CLI:** Command-line interface for all operations
3. **Add notifications:** Email/Slack when principles decay
4. **Add LLM enhancement:** Better learning extraction with semantic understanding
5. **Add visualization:** Dashboard web UI for philosophy health

---

**Location:** `8825-system/8825_core/philosophy/`  
**Main Entry Point:** `philosophy_manager.py`  
**Philosophy Document:** `../../PHILOSOPHY.md`
