# Goose Focus - Quick Start Guide

**Version:** 1.0.0  
**Status:** Complete Framework - Ready to Use

---

## Activate Goose Focus

```
focus on goose
```

**Response:**
```
🦢 GOOSE FOCUS ACTIVATED

Sandbox: /goose_sandbox/
Status: Protocol Framework Ready

Protocols are TBD - ready to define workflows, agents, and processes.

Say 'exit focus' when done.
```

---

## File Structure

```
goose_sandbox/
├── 8825_goose_focus.json          # Core protocol
├── README.md                       # Overview
├── STATUS.md                       # Current state
├── GOOSE_FOCUS_FRAMEWORK.md       # Complete documentation
├── QUICKSTART.md                   # This file
├── goose_engine.py                 # Execution engine
│
├── config/
│   ├── workflows_template.json    # Workflow template
│   ├── agents_template.json       # Agent template
│   └── settings_template.json     # Settings template
│
├── raw/                            # Input files
├── processed/                      # Intermediate files
├── output/                         # Final deliverables
├── logs/                           # Activity logs
└── archives/                       # Archived content
```

---

## Quick Setup (3 Steps)

### 1. Define Your Workflow

```bash
cd goose_sandbox/config
cp workflows_template.json workflows.json
nano workflows.json  # Edit to define your workflow
```

### 2. Define Your Agents

```bash
cp agents_template.json agents.json
nano agents.json  # Edit to define your agents
```

### 3. Run the Engine

```bash
cd ..
python3 goose_engine.py
```

---

## Example: Create a Simple Workflow

### Step 1: Create workflows.json

```json
{
  "workflows": {
    "simple_process": {
      "enabled": true,
      "description": "Simple processing workflow",
      "phases": [
        {
          "phase": "1. Input",
          "actions": ["Read files from raw/"],
          "outputs": ["input_data"]
        },
        {
          "phase": "2. Process",
          "actions": ["Transform data"],
          "outputs": ["processed_data"]
        },
        {
          "phase": "3. Output",
          "actions": ["Save to output/"],
          "outputs": ["final_output"]
        }
      ]
    }
  }
}
```

### Step 2: Test the Workflow

```python
from goose_engine import GooseEngine

engine = GooseEngine()
engine.execute_workflow("simple_process")
```

---

## Common Commands

### Check Engine Status
```bash
python3 goose_engine.py
```

### List Available Workflows
```python
from goose_engine import GooseEngine
engine = GooseEngine()
print(engine.list_workflows())
```

### Execute Workflow
```python
engine.execute_workflow("workflow_name")
```

### Execute Agent
```python
engine.execute_agent("agent_name")
```

---

## Next Steps

1. **Define Your Project**
   - What is Goose for?
   - What inputs do you have?
   - What outputs do you need?

2. **Create Workflows**
   - Copy `workflows_template.json` to `workflows.json`
   - Define your phases
   - Set enabled: true

3. **Create Agents**
   - Copy `agents_template.json` to `agents.json`
   - Define your agents
   - Set enabled: true

4. **Test & Iterate**
   - Run workflows manually
   - Check logs in `logs/`
   - Refine as needed

5. **Automate** (Optional)
   - Add scheduling
   - Set up monitoring
   - Integrate with other systems

---

## Documentation

- **README.md** - Overview and activation
- **STATUS.md** - Current state and progress
- **GOOSE_FOCUS_FRAMEWORK.md** - Complete technical documentation
- **QUICKSTART.md** - This file

---

## Support

### Templates Available
- `config/workflows_template.json` - Workflow examples
- `config/agents_template.json` - Agent examples
- `config/settings_template.json` - Settings examples

### Example Patterns
- See HCSS Focus (`/hcss_sandbox/`) for working example
- See Joju Mode (`/joju_sandbox/`) for another pattern

### Getting Help
- Review `GOOSE_FOCUS_FRAMEWORK.md` for detailed documentation
- Check templates for configuration examples
- Test with `goose_engine.py` for validation

---

## Summary

✅ **Framework Complete**  
✅ **Templates Ready**  
✅ **Engine Operational**  
🔲 **Awaiting Your Protocols**

**Ready to define your workflows and start building!**
