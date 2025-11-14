# 8825 Quick Start Guide

**Get up and running in 5 minutes**

---

## Prerequisites

- macOS or Linux
- Python 3.10+
- OpenAI API key

---

## Installation (2 minutes)

```bash
# 1. Clone or download 8825
cd ~/Downloads
# (assume you have 8825-system folder)

# 2. Run installation
cd 8825-system
./scripts/install.sh

# 3. Add your OpenAI API key
nano .env
# Change: OPENAI_API_KEY=your_openai_api_key_here
# To: OPENAI_API_KEY=sk-proj-...
# Save: Ctrl+O, Enter, Ctrl+X
```

**That's it!** Paths are auto-configured.

---

## First Run (1 minute)

```bash
# Activate virtual environment
source venv/bin/activate

# Start brain daemon
python3 8825_core/brain/brain_daemon.py
```

**You should see:**
```
✓ Brain daemon started
✓ Monitoring system health
✓ Ready for interactions
```

---

## Your First Task (2 minutes)

### **Option 1: Process a Meeting Transcript**

```bash
# Put Otter.ai transcript in Downloads
# Then run:
cd 8825_core/workflows/meeting_automation
python3 process_meetings.py
```

### **Option 2: Set Up Accountability**

```bash
cd 8825_core/agents
python3 accountability_loop_agent.py --add "Daily Exercise" \
  --description "Track daily workouts" \
  --metric-name "Workouts" \
  --metric-target 5 \
  --metric-unit "per week"

# Check status
python3 accountability_loop_agent.py --check daily_exercise
```

### **Option 3: Export Brain Learnings**

```bash
cd 8825_core/agents
python3 brain_learning_exporter.py --format markdown --output learnings.md
```

---

## Common Commands

```bash
# Check system health
./scripts/check_requirements.sh

# View all accountability loops
python3 8825_core/agents/accountability_loop_agent.py --list

# Process new meetings
python3 8825_core/workflows/meeting_automation/process_meetings.py

# Export brain learnings
python3 8825_core/agents/brain_learning_exporter.py --format cascade
```

---

## What's Next?

### **Learn More:**
- `INSTALLATION.md` - Detailed setup guide
- `SYSTEM_REQUIREMENTS.md` - System requirements
- `8825_core/protocols/README.md` - Workflow protocols
- `8825_core/agents/README.md` - Agent system

### **Configure:**
- Google API (Gmail, Calendar, Drive): `8825_core/integrations/google/README.md`
- Meeting automation: `8825_core/workflows/meeting_automation/README.md`
- Bill processing: `8825_core/integrations/google/bill_processor.py`

### **Explore:**
- Protocols: `8825_core/protocols/`
- Agents: `8825_core/agents/`
- Workflows: `8825_core/workflows/`

---

## Troubleshooting

### **"Python version too old"**
```bash
# macOS
brew install python@3.10

# Linux
sudo apt install python3.10
```

### **"OpenAI API key not working"**
- Check key starts with `sk-proj-` or `sk-`
- Verify no extra spaces in .env
- Test: `echo $OPENAI_API_KEY` (after `source .env`)

### **"Module not found"**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-full.txt
```

### **"Permission denied"**
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

---

## Getting Help

1. Check `FAQ.md` (coming soon)
2. Review `INSTALLATION.md` for detailed setup
3. Check `8825_core/protocols/README.md` for workflows
4. Open an issue (if using GitHub)

---

## Quick Reference

**Installation:**
```bash
./scripts/install.sh
nano .env  # Add API key
source venv/bin/activate
```

**Brain:**
```bash
python3 8825_core/brain/brain_daemon.py
```

**Accountability:**
```bash
python3 8825_core/agents/accountability_loop_agent.py --list
```

**Meetings:**
```bash
python3 8825_core/workflows/meeting_automation/process_meetings.py
```

**Health Check:**
```bash
./scripts/check_requirements.sh
```

---

**You're ready to go! Start with accountability loops or meeting automation.**
