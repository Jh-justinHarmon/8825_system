# Auto Brain Transport System

**Status:** ✅ Production Ready  
**Integration:** Brain Sync Daemon  
**Update Frequency:** Automatic (threshold-based)

---

## Overview

The Brain Transport is now **automatically generated** by the Brain Sync Daemon based on system changes. No manual updates needed!

### **How It Works:**

```
Brain Sync Daemon (runs every 30s)
    ↓
System Health Monitor
    ├─ Checks LaunchAgents
    ├─ Checks integrations
    ├─ Checks workflows
    ├─ Checks configs
    └─ Calculates change score
    ↓
If score >= 10 points:
    ↓
Brain Transport Generator
    ├─ Scans system state
    ├─ Merges manual overrides
    ├─ Generates JSON
    └─ Distributes to locations
```

---

## Change Detection & Scoring

### **Weights:**
- **LaunchAgent change:** 10 points (High)
- **Config file change:** 5 points (High)
- **Integration script:** 3 points (Medium)
- **Workflow update:** 2 points (Medium)
- **Archive activity:** 1 point (Low)

### **Threshold:** 10 points

### **Examples:**

**Scenario 1: New Integration**
```
New reddit_watcher.py (+3)
New com.8825.reddit-watcher.plist (+5)
Total: 8 points → Wait for more changes
```

**Scenario 2: LaunchAgent Change**
```
LaunchAgent stopped (+10)
Total: 10 points → REGENERATE ✅
```

**Scenario 3: Multiple Small Changes**
```
Cycle 1: README updated (+2)
Cycle 2: Another README (+2)
Cycle 3: Integration modified (+3)
Cycle 4: Config changed (+5)
Total: 12 points → REGENERATE ✅
```

---

## What Gets Auto-Detected

### ✅ **Automatically Scanned:**
- Active LaunchAgents (running/stopped)
- Integration scripts (new/modified)
- Workflow status files
- Configuration files (.json, .plist)
- MCP servers
- Archive directories

### 📝 **Manual Overrides:**
- Interaction modes (dev/brainstorm/teaching)
- Communication style preferences
- Critical rules
- Active memories

**Edit:** `8825_core/brain/brain_transport_overrides.json`

---

## Output Locations

### **Primary:**
```
INBOX_HUB/users/jh/intake/documents/8825_BRAIN_TRANSPORT.json
```

### **Downloads (for easy access):**
```
~/Downloads/0-8825_BRAIN_TRANSPORT.json
```
(0- prefix ensures it sorts to top)

### **Archive:**
```
8825_core/brain/state/brain_transport_archive/
brain_transport_YYYYMMDD_HHMMSS.json
```

---

## Manual Commands

### **Force Regenerate Now:**
```bash
cd 8825_core/brain/
python3 brain_sync_daemon.py --regenerate-transport
```

### **Check System Health:**
```bash
python3 brain_sync_daemon.py --check-health
```

**Output:**
```
Accumulated Score: 8/10
Regenerate Needed: False

Changes Detected:
  - New integrations: 2
  - Modified configs: 1
```

### **View Daemon Status:**
```bash
python3 brain_sync_daemon.py --status
```

---

## Integration with Brain Daemon

The system health monitor runs **every 30 seconds** as part of the Brain Sync Daemon cycle:

```python
def _run_cycle(self):
    # 1. Check Brain files (existing)
    updates = self.tracker.check_for_updates()
    
    # 2. Check system health (NEW)
    system_changes = self.health_monitor.check_system_state()
    
    # 3. Auto-regenerate if threshold met (NEW)
    if system_changes['regenerate_brain_transport']:
        self.transport_generator.generate()
```

**No extra overhead** - piggybacks on existing daemon.

---

## Logs

### **Daemon Log:**
```
8825_core/brain/state/daemon_log.jsonl
```

**Example entries:**
```json
{"timestamp": "2025-11-12T06:00:00", "level": "HEALTH", "message": "System changes detected (score: 12)"}
{"timestamp": "2025-11-12T06:00:01", "level": "TRANSPORT", "message": "Regenerating Brain Transport..."}
{"timestamp": "2025-11-12T06:00:02", "level": "TRANSPORT", "message": "Brain Transport regenerated successfully"}
```

### **View Recent Logs:**
```bash
tail -20 8825_core/brain/state/daemon_log.jsonl | jq
```

---

## State Files

### **System State:**
```
8825_core/brain/state/system_state.json
```

Tracks:
- LaunchAgent status
- Integration file hashes
- Workflow file hashes
- Config file hashes
- Archive directories
- Accumulated change score

### **Brain State:**
```
8825_core/brain/state/brain_state.json
```

Tracks:
- Philosophy.md changes
- Decision matrix changes
- Learning principles changes
- Prompt generator changes

---

## Customization

### **Adjust Thresholds:**

Edit `system_health_monitor.py`:

```python
class SystemHealthMonitor:
    WEIGHTS = {
        'launchagent_change': 10,    # Adjust these
        'config_change': 5,
        'integration_change': 3,
        'workflow_change': 2,
        'archive_activity': 1
    }
    
    REGENERATION_THRESHOLD = 10  # Adjust this
```

### **Add Manual Overrides:**

Edit `brain_transport_overrides.json`:

```json
{
  "interaction_modes": { ... },
  "communication_style": { ... },
  "critical_rules": { ... },
  "active_memories": {
    "your_custom_memory": "value"
  }
}
```

---

## Benefits

### **1. Always Accurate**
- Reflects current system state
- No manual updates needed
- Catches new capabilities automatically

### **2. Smart Thresholds**
- Doesn't regenerate on every tiny change
- Accumulates changes until threshold
- Prioritizes high-impact changes

### **3. Zero Overhead**
- Piggybacks on existing 30s daemon cycle
- No new processes
- No new LaunchAgents

### **4. Logged & Auditable**
- All changes logged
- Can review what triggered regeneration
- Change history tracked

### **5. Manual Override Available**
- Force regenerate anytime
- Check health anytime
- Adjust thresholds easily

---

## Troubleshooting

### **Brain Transport not updating?**

Check accumulated score:
```bash
python3 brain_sync_daemon.py --check-health
```

If score < 10, not enough changes yet.

### **Want to force update?**

```bash
python3 brain_sync_daemon.py --regenerate-transport
```

### **Daemon not running?**

Check if Brain Sync Daemon is active:
```bash
ps aux | grep brain_sync_daemon
```

Start it:
```bash
python3 brain_sync_daemon.py --daemon
```

### **Check logs:**

```bash
tail -f 8825_core/brain/state/daemon_log.jsonl
```

---

## Architecture

```
8825_core/brain/
├── brain_sync_daemon.py              # Main daemon (enhanced)
├── brain_update_tracker.py           # Tracks Brain file changes
├── system_health_monitor.py          # NEW: Monitors system changes
├── brain_transport_generator.py      # NEW: Generates transport JSON
├── brain_transport_overrides.json    # NEW: Manual overrides
└── state/
    ├── daemon_log.jsonl              # Daemon activity log
    ├── system_state.json             # System state tracking
    ├── brain_state.json              # Brain file state
    └── brain_transport_archive/      # Previous versions
```

---

## Quick Reference

```bash
# Check system health
python3 brain_sync_daemon.py --check-health

# Force regenerate
python3 brain_sync_daemon.py --regenerate-transport

# View daemon status
python3 brain_sync_daemon.py --status

# View logs
tail -f 8825_core/brain/state/daemon_log.jsonl

# View latest transport
cat ~/Downloads/0-8825_BRAIN_TRANSPORT.json | jq

# View generation history
ls -lt 8825_core/brain/state/brain_transport_archive/
```

---

**System is now self-maintaining!** 🎯

The Brain Transport will automatically stay up-to-date as you make changes to the system.
