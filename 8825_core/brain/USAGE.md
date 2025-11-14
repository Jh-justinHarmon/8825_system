# 8825 Brain Usage Guide

**Quick reference for using the brain system**

---

## 🚀 QUICK START

### **Start Brain:**
```bash
cd 8825_core/brain
./start_brain.sh
```

### **Check Status:**
```bash
8825_core/bin/8825-brain-status
```

### **Stop Brain:**
```bash
cd 8825_core/brain
./stop_brain.sh
```

---

## 📋 COMMANDS

### **1. Status - See System State**

```bash
8825-brain-status
```

**Shows:**
- Component count
- System health
- Active workflows
- Last sync time
- Recommendations

**Example output:**
```
=== Brain Status ===

System Awareness:
  Components: 109
  Health: healthy
  Active workflows: 0
  Last sync: 5s ago

Recommendations:
  ✅ System healthy, no action needed

Brain sync: ✅ Current
```

---

### **2. Predict - Analyze Before Acting**

```bash
8825-brain-predict "restart inbox_daemon"
```

**Shows:**
- Action type and target
- Risk level (low/medium/high/critical)
- Conflicts detected
- Historical success rate
- Recommendation

**Example output:**
```
=== Impact Prediction ===

Action: restart inbox_daemon
Type: restart
Target: inbox_daemon

Risk Level: ⚠️  MEDIUM

Conflicts: ✅ None detected

Historical Data: No previous attempts

Recommendation:
  ⚠️  Proceed with caution - Monitor for issues

✅ Safe to proceed
```

**Use cases:**
- Before restarting daemons
- Before running cleanup scripts
- Before making system changes
- To understand impact

---

### **3. Execute - Run with Coordination**

```bash
8825-brain-execute "restart inbox_daemon"
```

**What happens:**
1. Analyzes impact
2. Shows risk and recommendation
3. Asks confirmation if risky
4. Creates safe workflow
5. Executes with coordination
6. Handles failures automatically
7. Records outcome

**Example output:**
```
🎯 Action: restart inbox_daemon

📊 Analyzing impact...
Risk: MEDIUM
Recommendation: ⚠️  Proceed with caution

Proceed? (y/n): y

🔄 Creating safe workflow...
Workflow: safe_restart_inbox_daemon
Steps: 4

🚀 Executing...

[1/4] stop inbox_daemon...
  ✅ Stopped inbox_daemon

[2/4] wait...
  ✅ Waited 5 seconds

[3/4] start inbox_daemon...
  ✅ Started inbox_daemon

[4/4] verify_health inbox_daemon...
  ✅ inbox_daemon is healthy

✅ Success!
Steps completed: 4
```

**Use cases:**
- Restart daemons safely
- Start/stop components
- Run complex workflows
- Coordinate multiple actions

---

### **4. Heal - Fix Issues Autonomously**

```bash
8825-brain-heal
```

**What it does:**
1. Scans for issues
2. Detects problems automatically
3. Matches to healing strategies
4. Executes healing
5. Reports results

**Example output:**
```
🔍 Running self-healing check...

=== Self-Healing Report ===

Issues found: 2
Issues healed: 2

✅ Healed (2):
  - component_unhealthy: inbox_daemon not responding
  - orphaned_pid_file: Orphaned PID file: brain.pid

✅ All issues healed successfully
```

**Detects:**
- Unhealthy components
- Stale processes
- Low disk space
- Orphaned files

**Heals:**
- Restarts unhealthy components
- Cleans up disk space
- Removes orphaned files
- Kills stale processes

---

## 🎯 COMMON WORKFLOWS

### **Safe Daemon Restart:**
```bash
# Predict first
8825-brain-predict "restart inbox_daemon"

# If safe, execute
8825-brain-execute "restart inbox_daemon"
```

### **System Health Check:**
```bash
# Check status
8825-brain-status

# Run healing
8825-brain-heal
```

### **Before Making Changes:**
```bash
# Always predict first
8825-brain-predict "update sync scripts"

# Review impact
# Then decide whether to proceed
```

---

## 💡 TIPS & BEST PRACTICES

### **1. Always Predict First**
Before any risky action, run predict to see impact:
```bash
8825-brain-predict "your action"
```

### **2. Monitor Status Regularly**
Check system health periodically:
```bash
8825-brain-status
```

### **3. Run Healing Proactively**
Don't wait for problems, run healing regularly:
```bash
8825-brain-heal
```

### **4. Trust the Risk Assessment**
- **Low risk** - Safe to proceed
- **Medium risk** - Proceed with caution
- **High risk** - Review carefully
- **Critical risk** - Don't proceed

### **5. Let Brain Coordinate**
Use `execute` instead of manual commands:
- Brain handles conflicts
- Brain waits for dependencies
- Brain rolls back on failure
- Brain records outcomes

---

## 🔧 TROUBLESHOOTING

### **Brain not responding:**
```bash
# Check if running
ps aux | grep brain_daemon

# Check log
tail -f ~/.8825/brain.log

# Restart
cd 8825_core/brain
./stop_brain.sh
./start_brain.sh
```

### **Command shows error:**
```bash
# Check brain is running
8825-brain-status

# If not running, start it
cd 8825_core/brain
./start_brain.sh
```

### **Prediction seems wrong:**
```bash
# Brain learns from outcomes
# Run the action, let brain record result
# Next time prediction will be better
```

### **Healing fails:**
```bash
# Check healing history
cat ~/.8825/healing_history.json

# Some issues need manual intervention
# Brain will escalate these
```

---

## 📊 UNDERSTANDING OUTPUT

### **Risk Levels:**
- ✅ **Low** - No conflicts, good history, safe to proceed
- ⚠️  **Medium** - Some conflicts or unknown, proceed with caution
- 🔴 **High** - Multiple conflicts or poor history, review carefully
- 🛑 **Critical** - High severity conflicts, do not proceed

### **Conflict Types:**
- **active_workflow** - Another workflow is running
- **component_active** - Component is currently running
- **cleanup_running** - Cleanup script is running

### **Resolutions:**
- **wait_for_completion** - Wait for workflow to finish
- **wait_for_cleanup** - Wait for cleanup to finish
- **stop_before_action** - Stop component first

---

## 🎓 ADVANCED USAGE

### **Custom Workflows:**
You can create custom workflows and execute them:

```python
workflow = {
    "id": "custom_workflow",
    "steps": [
        {"action": "stop", "target": "daemon1"},
        {"action": "wait", "duration": 5},
        {"action": "start", "target": "daemon2"},
        {"action": "verify_health", "target": "daemon2"}
    ]
}

# Execute via API
from brain_api import BrainAPI
api = BrainAPI()
result = api.execute_workflow(workflow)
```

### **Add Custom Healing Strategies:**
Create new strategy in `healing_strategies/`:

```python
class MyCustomStrategy:
    def heal(self, issue, brain_state):
        # Your healing logic
        return {"success": True, "message": "Healed"}
```

Register in `self_healing_engine.py`:
```python
self.strategies["my_issue_type"] = MyCustomStrategy()
```

---

## 📝 FILES & LOCATIONS

### **Brain Files:**
- PID: `~/.8825/brain.pid`
- Log: `~/.8825/brain.log`
- Socket: `/tmp/8825_brain.sock`
- State: `~/Downloads/8825_brain/brain_state.json`

### **History Files:**
- Workflow history: `~/.8825/workflow_history.json`
- Healing history: `~/.8825/healing_history.json`
- Change history: `~/.8825/change_history.json`

### **Commands:**
- `8825_core/bin/8825-brain-status`
- `8825_core/bin/8825-brain-predict`
- `8825_core/bin/8825-brain-execute`
- `8825_core/bin/8825-brain-heal`

---

## 🚀 QUICK REFERENCE

```bash
# Start brain
cd 8825_core/brain && ./start_brain.sh

# Check status
8825-brain-status

# Predict action
8825-brain-predict "restart daemon"

# Execute action
8825-brain-execute "restart daemon"

# Run healing
8825-brain-heal

# Stop brain
cd 8825_core/brain && ./stop_brain.sh
```

---

**For detailed technical docs, see `README.md`**  
**For implementation details, see source files**
