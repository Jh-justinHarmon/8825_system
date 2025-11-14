# Tethered Brain Protocol - Quick Start

**5-Minute Setup Guide**

---

## What It Does

Keeps all active Cascades synchronized with Brain's evolving knowledge in real-time.

**Before:** Cascades work with stale context  
**After:** Cascades auto-update when Brain learns something new

---

## Quick Test

```bash
cd 8825_core/brain

# Test 1: Check Brain tracking
python3 brain_update_tracker.py

# Test 2: Test Cascade check-in
python3 cascade_check_in.py

# Test 3: Run full demo
python3 demo_tethered_protocol.py
```

---

## Start Using It

### 1. Start the Daemon (Background)

```bash
# In terminal
cd 8825_core/brain
python3 brain_sync_daemon.py --daemon
```

**What it does:** Monitors Brain files every 30s, broadcasts updates to Cascades

---

### 2. Add to Your Cascade Code

```python
from cascade_check_in import CascadeCheckIn

# At start of Cascade
check_in = CascadeCheckIn(
    cascade_id="my_cascade_name",
    task_type="automation",  # or validation, documentation, etc.
    focus_area="inbox_hub"   # or joju, hcss, jh
)

# In your work loop
while working:
    # Do your work
    do_task()
    
    # Check in with Brain
    if check_in.should_check_in():
        updates = check_in.check_in()
        
        if updates:
            print("🔔 Brain updated!")
            print(check_in.format_updates_for_cascade(updates))
            # Adjust your behavior based on updates
```

---

### 3. Test It

**Edit PHILOSOPHY.md:**
```bash
# Add a new principle or update existing one
vim ../../PHILOSOPHY.md
```

**Watch it propagate:**
- Daemon detects change within 30s
- Your Cascade receives update within 5 min
- Update logged in `state/` directory

---

## Check Status

```bash
# See all active Cascades
python3 brain_sync_daemon.py --status

# View logs
tail -f state/update_log.jsonl
tail -f state/check_in_log.jsonl
tail -f state/daemon_log.jsonl
```

---

## Configuration

### Cascade Check-In Frequency

```python
# Default: 5 minutes
check_in = CascadeCheckIn(..., check_in_interval_minutes=5)

# More frequent: 2 minutes
check_in = CascadeCheckIn(..., check_in_interval_minutes=2)
```

### Daemon Monitoring Frequency

```bash
# Default: 30 seconds
python3 brain_sync_daemon.py --daemon

# More frequent: 15 seconds
python3 brain_sync_daemon.py --daemon --interval 15
```

---

## What Gets Tracked

**Brain Files:**
- `PHILOSOPHY.md` - Principles and learnings
- `decision_matrix.json` - Priority framework
- `learning_principles.md` - Learning protocols
- `prompt_generator.py` - Prompt generation

**Changes Detected:**
- New principles added
- Principles deprecated
- Status changes (Active → Promoted)
- Protocol updates

---

## Troubleshooting

### Cascade not receiving updates?

1. Check daemon is running: `ps aux | grep brain_sync_daemon`
2. Check Cascade state exists: `ls state/cascade_*.json`
3. Verify check-in interval passed
4. Check logs: `tail state/daemon_log.jsonl`

### Daemon not detecting changes?

1. Verify files exist and are tracked
2. Check file permissions
3. Restart daemon
4. Check logs for errors

---

## Stop Daemon

```bash
# Find process
ps aux | grep brain_sync_daemon

# Kill it
kill <PID>
```

---

## Next Steps

1. ✅ Test with demo: `python3 demo_tethered_protocol.py`
2. ✅ Start daemon: `python3 brain_sync_daemon.py --daemon`
3. ✅ Add check-in to your Cascade
4. ✅ Edit PHILOSOPHY.md and watch it work
5. 🔄 Set up as LaunchAgent (auto-start on boot)

---

**Full docs:** `TETHERED_BRAIN_PROTOCOL.md`  
**Location:** `8825_core/brain/`
