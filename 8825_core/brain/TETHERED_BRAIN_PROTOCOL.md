# Tethered Brain Protocol

**Status:** Production Ready  
**Created:** November 11, 2025

---

## Overview

System for keeping active Cascades synchronized with Brain's evolving knowledge.

**Problem Solved:** Previously, Cascades worked in isolation with stale context. Now they stay synchronized with Brain updates.

---

## Architecture

```
🧠 BRAIN (updates every 30s)
    ↓
Brain Update Tracker (monitors changes)
    ↓
Brain Sync Daemon (broadcasts updates)
    ↓
    ├─ Cascade A (checks in every 5 min)
    ├─ Cascade B (checks in every 5 min)
    └─ Cascade C (checks in every 5 min)
```

---

## Components

### 1. **Brain Update Tracker** (`brain_update_tracker.py`)

Monitors Brain knowledge files for changes.

**Tracked Files:**
- `PHILOSOPHY.md` - Principles and learnings
- `decision_matrix.json` - Priority framework
- `learning_principles.md` - Learning protocols
- `prompt_generator.py` - Prompt generation logic

**Functions:**
- `check_for_updates()` - Scan all files for changes
- `get_updates_since(timestamp)` - Get updates after time
- `get_current_snapshot()` - Get current Brain state

**Detection:**
- File hash comparison (SHA-256)
- Specific change detection (new principles, deprecations)
- Timestamp tracking

---

### 2. **Cascade Check-In** (`cascade_check_in.py`)

Allows Cascades to check in with Brain.

**Usage in Cascade:**
```python
from cascade_check_in import CascadeCheckIn

# Initialize
check_in = CascadeCheckIn(
    cascade_id="cascade_automation_1",
    task_type="automation",
    focus_area="inbox_hub"
)

# Periodically check
if check_in.should_check_in():
    updates = check_in.check_in()
    if updates:
        print(check_in.format_updates_for_cascade(updates))
        # Adjust behavior based on updates
```

**Features:**
- Configurable check-in interval (default: 5 min)
- Relevance filtering (only get updates for your task type)
- Formatted update messages
- State tracking per Cascade

---

### 3. **Brain Sync Daemon** (`brain_sync_daemon.py`)

Background daemon that monitors and broadcasts.

**Run as daemon:**
```bash
python3 brain_sync_daemon.py --daemon --interval 30
```

**What it does:**
1. Checks Brain files every 30 seconds
2. Detects updates (new principles, protocol changes)
3. Identifies active Cascades
4. Broadcasts updates to active Cascades
5. Logs all activity

**Status check:**
```bash
python3 brain_sync_daemon.py --status
```

---

### 4. **Cascade Coordinator** (`cascade_check_in.py`)

Manages multiple Cascades.

**Functions:**
- `get_active_cascades()` - List all active Cascades
- `broadcast_update(message)` - Send update to all
- `get_coordination_status()` - Dashboard of all Cascades

---

## Workflows

### Starting a Cascade (with check-in)

```python
from cascade_check_in import CascadeCheckIn
import time

# Initialize check-in
check_in = CascadeCheckIn(
    cascade_id="my_cascade",
    task_type="automation",
    focus_area="inbox_hub",
    check_in_interval_minutes=5
)

# Main work loop
while working:
    # Do work
    do_task()
    
    # Check in with Brain
    if check_in.should_check_in():
        updates = check_in.check_in()
        
        if updates:
            message = check_in.format_updates_for_cascade(updates)
            print(message)
            
            # Adjust approach based on updates
            if 'philosophy' in updates['updates'][0]['updated_files']:
                reload_principles()
    
    time.sleep(60)  # Work cycle
```

---

### Running the Daemon

**Start daemon:**
```bash
# Run in foreground
python3 brain_sync_daemon.py --daemon

# Run in background (macOS/Linux)
nohup python3 brain_sync_daemon.py --daemon > daemon.log 2>&1 &

# Custom interval (60 seconds)
python3 brain_sync_daemon.py --daemon --interval 60
```

**Check status:**
```bash
python3 brain_sync_daemon.py --status
```

**Stop daemon:**
```bash
# Find process
ps aux | grep brain_sync_daemon

# Kill process
kill <PID>
```

---

### Manual Check-In

```python
from cascade_check_in import CascadeCheckIn

check_in = CascadeCheckIn(cascade_id="manual_check")

# Force immediate check-in
updates = check_in.check_in(force=True)

if updates:
    print(f"Received {updates['count']} updates")
    print(check_in.format_updates_for_cascade(updates))
```

---

## Update Types

### Philosophy Updates
- **New principles** - Added to PHILOSOPHY.md
- **Deprecated principles** - Marked as deprecated
- **Status changes** - Active → Promoted → Iron-Clad

**Cascade action:** Review new principles, stop using deprecated ones

### Decision Matrix Updates
- **Priority changes** - What to prioritize
- **New criteria** - How to evaluate tasks

**Cascade action:** Re-evaluate current task priority

### Learning Principles Updates
- **New protocols** - How to learn from sessions
- **Updated workflows** - Better ways to extract learnings

**Cascade action:** Apply new learning protocols

### PromptGen Updates
- **Generation logic** - How to create prompts
- **Template changes** - New prompt structures

**Cascade action:** Regenerate prompts with new logic

---

## State Files

All state stored in `8825_core/brain/state/`:

```
state/
├── brain_state.json           # Current Brain state
├── update_log.jsonl           # All updates logged
├── cascade_*.json             # Per-Cascade state
├── check_in_log.jsonl         # All check-ins logged
├── broadcasts.jsonl           # All broadcasts logged
└── daemon_log.jsonl           # Daemon activity log
```

---

## Relevance Filtering

Cascades only receive updates relevant to their task:

```python
check_in = CascadeCheckIn(
    cascade_id="joju_automation",
    task_type="automation",      # Filter by task type
    focus_area="joju"            # Filter by focus
)

# Only receives updates about:
# - Automation-related principles
# - Joju-specific protocols
# - General system updates
```

---

## Integration with Brain Reload

**Brain reloads every 30 seconds:**
1. Brain checkpoint updates with new memories
2. Brain Sync Daemon detects file changes
3. Daemon broadcasts to active Cascades
4. Cascades check in and receive updates
5. Cascades adjust behavior

**Timeline:**
```
00:00 - Brain reloads, new principle added
00:30 - Daemon detects update
00:30 - Daemon broadcasts to Cascades
05:00 - Cascade A checks in, receives update
05:00 - Cascade A adjusts approach
```

---

## Benefits

### Before Tethered Protocol
❌ Cascades work with stale context  
❌ Manual user intervention required  
❌ Inconsistent behavior across Cascades  
❌ No awareness of Brain updates  

### After Tethered Protocol
✅ Cascades stay synchronized  
✅ Automatic update propagation  
✅ Consistent behavior system-wide  
✅ Real-time awareness of changes  

---

## Example: Full System in Action

**Scenario:** User adds new principle to PHILOSOPHY.md

1. **00:00** - User edits PHILOSOPHY.md, adds "Always validate before modifying"
2. **00:30** - Brain Sync Daemon detects change
3. **00:30** - Daemon logs: "Philosophy updated: 1 new principle"
4. **00:30** - Daemon broadcasts to 3 active Cascades
5. **05:00** - Cascade A (automation) checks in
6. **05:00** - Cascade A receives: "New principle: Always validate before modifying"
7. **05:00** - Cascade A adjusts: Adds validation step before file modification
8. **10:00** - Cascade B (documentation) checks in
9. **10:00** - Cascade B receives same update
10. **10:00** - Cascade B adjusts: Adds validation to doc generation

**Result:** All Cascades now follow new principle within 10 minutes

---

## Monitoring

### Check Daemon Status
```bash
python3 brain_sync_daemon.py --status
```

### View Update Log
```bash
tail -f 8825_core/brain/state/update_log.jsonl
```

### View Check-In Log
```bash
tail -f 8825_core/brain/state/check_in_log.jsonl
```

### View Broadcasts
```bash
tail -f 8825_core/brain/state/broadcasts.jsonl
```

---

## Configuration

### Check-In Interval
```python
# Default: 5 minutes
check_in = CascadeCheckIn(cascade_id="...", check_in_interval_minutes=5)

# More frequent: 2 minutes
check_in = CascadeCheckIn(cascade_id="...", check_in_interval_minutes=2)

# Less frequent: 10 minutes
check_in = CascadeCheckIn(cascade_id="...", check_in_interval_minutes=10)
```

### Daemon Interval
```bash
# Default: 30 seconds
python3 brain_sync_daemon.py --daemon

# More frequent: 15 seconds
python3 brain_sync_daemon.py --daemon --interval 15

# Less frequent: 60 seconds
python3 brain_sync_daemon.py --daemon --interval 60
```

---

## Next Enhancements

1. **Push notifications** - Alert Cascade windows directly
2. **Priority updates** - Critical updates interrupt immediately
3. **Update acknowledgment** - Cascades confirm receipt
4. **Rollback support** - Revert to previous Brain state
5. **Web dashboard** - Visual monitoring of all Cascades
6. **Slack integration** - Notify team of major updates

---

## Troubleshooting

### Cascade not receiving updates
1. Check if daemon is running: `ps aux | grep brain_sync_daemon`
2. Check Cascade state file exists: `ls 8825_core/brain/state/cascade_*.json`
3. Verify check-in interval hasn't elapsed
4. Check daemon log: `tail 8825_core/brain/state/daemon_log.jsonl`

### Daemon not detecting updates
1. Verify tracked files exist
2. Check file permissions
3. Review daemon log for errors
4. Restart daemon

### Too many updates
1. Increase daemon interval: `--interval 60`
2. Increase Cascade check-in interval
3. Add more specific relevance filtering

---

**The Brain now has a nervous system. All Cascades stay synchronized.** 🧠⚡
