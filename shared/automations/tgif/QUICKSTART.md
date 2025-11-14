# TGIF Automation - Quick Start Guide

**Time to setup:** 15-20 minutes

---

## ✅ CHECKLIST

- [ ] Python 3.8+ installed
- [ ] Otter.ai account credentials
- [ ] Gmail account with API access
- [ ] Google Cloud project with Gmail API enabled

---

## 🚀 SETUP (5 STEPS)

### **Step 1: Install Dependencies (5 min)**

```bash
cd "focuses/hcss/automation"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
pip install git+https://github.com/gmchad/otterai-api.git
```

### **Step 2: Configure Environment (3 min)**

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required settings:**
```bash
OTTER_EMAIL=your_email@otter.ai
OTTER_PASSWORD=your_password

NOTIFICATION_EMAIL=justin@hcss.com
STAKEHOLDER_EMAILS=justin@hcss.com,team@tgif.com
```

### **Step 3: Setup Gmail API (5 min)**

1. Go to https://console.cloud.google.com/
2. Create/select project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to `focuses/hcss/automation/`

### **Step 4: Test Components (2 min)**

```bash
# Test task tracker
python task_tracker/tracker.py

# Test Otter MCP
python otter_mcp/server.py &

# Check health
curl http://localhost:8829/health
```

### **Step 5: Start Services (1 min)**

```bash
# Terminal 1: Otter MCP
python otter_mcp/server.py

# Terminal 2: Daily Email Processor
python processors/daily_email_processor.py

# Terminal 3: Weekly Rollup
python processors/weekly_rollup.py
```

---

## 🎯 VERIFY IT'S WORKING

### **Test 1: Otter MCP Health**

```bash
curl http://localhost:8829/health
```

Expected:
```json
{
  "status": "healthy",
  "source": "otter_api",
  "failure_count": 0
}
```

### **Test 2: Task Tracker**

```python
from task_tracker.tracker import TaskTracker

tracker = TaskTracker()
tracker.add_task({
    'what': 'Test task',
    'who': 'Justin',
    'priority': 'high'
})

print(tracker.get_summary())
```

### **Test 3: Email Processing**

```bash
# Run once immediately
RUN_ON_STARTUP=true python processors/daily_email_processor.py
```

Check output:
```
focuses/hcss/knowledge/emails/daily_batches/
```

---

## 📅 DAILY USAGE

### **Your Actions:**

1. **Forward important TGIF emails to Gmail**
   - Add "TGIF:" to subject
   - OR label with "TGIF"

2. **Meetings happen automatically**
   - Otter.ai joins and transcribes
   - Summaries generated

### **Automated:**

- **12pm daily:** Process emails, update tasks
- **3pm Friday:** Generate weekly digest

---

## 📁 WHERE TO FIND OUTPUTS

```
focuses/hcss/knowledge/
├── meetings/summaries/     # Individual meeting summaries
├── emails/daily_batches/   # Daily email processing
├── task_tracker.json       # All action items
└── rollups/                # Weekly digests
```

---

## 🐛 TROUBLESHOOTING

### **"Otter API failed"**
✅ Normal! It falls back to Gmail automatically.

### **"Gmail authentication failed"**
```bash
rm token.json
python processors/daily_email_processor.py
# Complete OAuth in browser
```

### **"No emails found"**
- Make sure emails have "TGIF" in subject or label
- Check forwarding is working

---

## 🎓 NEXT STEPS

1. **Run for one week** - Let it collect data
2. **Review outputs** - Check summaries and task tracker
3. **Tune as needed** - Adjust schedules, add stakeholders
4. **Integrate Chat Mining Agent** - Better extraction (TODO)

---

## 📞 NEED HELP?

Check:
- README.md (full documentation)
- Logs: `focuses/hcss/automation/logs/`
- Health: `curl http://localhost:8829/health`

---

**Setup complete! Pipeline is running.** ✅
