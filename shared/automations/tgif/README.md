# TGIF Meeting Automation Pipeline

**Status:** Ready for Setup  
**Version:** 1.0.0

Automated pipeline for processing TGIF meetings and emails with task tracking and weekly rollups.

---

## 🎯 WHAT IT DOES

### **Real-Time (After Each Meeting):**
- Detects new Otter.ai transcripts
- Generates standalone summary (JSON + Markdown + Email)
- Sends to stakeholders immediately

### **Daily at 12pm:**
- Processes flagged TGIF emails from Gmail
- Extracts action items
- Updates task tracker
- Flags overdue tasks

### **Friday at 3pm:**
- Aggregates all meetings + emails from the week
- Generates weekly digest
- Sends to stakeholders

---

## 📁 STRUCTURE

```
focuses/hcss/automation/
├── otter_mcp/
│   └── server.py              # Otter MCP with Gmail fallback
├── processors/
│   ├── daily_email_processor.py   # Daily 12pm email processing
│   └── weekly_rollup.py           # Friday 3pm rollup (TODO)
├── task_tracker/
│   └── tracker.py             # Task tracking system
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

---

## 🚀 SETUP

### **1. Install Dependencies**

```bash
cd focuses/hcss/automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Otter.ai unofficial API
pip install git+https://github.com/gmchad/otterai-api.git
```

### **2. Configure Environment**

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required settings:**
```bash
# Otter.ai credentials
OTTER_EMAIL=your_email@example.com
OTTER_PASSWORD=your_otter_password

# Gmail API (download credentials.json from Google Cloud Console)
GMAIL_CREDENTIALS_PATH=credentials.json

# Notification email
NOTIFICATION_EMAIL=justin@hcss.com
STAKEHOLDER_EMAILS=justin@hcss.com,team@tgif.com
```

### **3. Setup Gmail API**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to `focuses/hcss/automation/`

### **4. Test Components**

```bash
# Test task tracker
python task_tracker/tracker.py

# Test Otter MCP (in separate terminal)
python otter_mcp/server.py

# Test daily email processor (run once)
RUN_ON_STARTUP=true python processors/daily_email_processor.py
```

---

## 🏃 RUNNING

### **Option 1: Run Components Separately**

```bash
# Terminal 1: Otter MCP Server
python otter_mcp/server.py

# Terminal 2: Daily Email Processor
python processors/daily_email_processor.py
```

### **Option 2: Run with systemd (Linux/Mac)**

Create service files:

```bash
# /etc/systemd/system/tgif-otter-mcp.service
[Unit]
Description=TGIF Otter MCP Server
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/focuses/hcss/automation
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python otter_mcp/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# /etc/systemd/system/tgif-email-processor.service
[Unit]
Description=TGIF Daily Email Processor
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/focuses/hcss/automation
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python processors/daily_email_processor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable tgif-otter-mcp
sudo systemctl enable tgif-email-processor
sudo systemctl start tgif-otter-mcp
sudo systemctl start tgif-email-processor
```

### **Option 3: Run with Docker (TODO)**

---

## 📊 MONITORING

### **Check Otter MCP Health:**

```bash
curl http://localhost:8829/health
```

Response:
```json
{
  "status": "healthy",
  "source": "otter_api",
  "failure_count": 0,
  "last_success": "2025-11-09T12:00:00"
}
```

### **Check Task Tracker:**

```python
from task_tracker.tracker import TaskTracker

tracker = TaskTracker()
print(tracker.get_summary())
```

### **View Logs:**

```bash
tail -f focuses/hcss/automation/logs/tgif_automation.log
```

---

## 📋 DAILY WORKFLOW

### **Your Actions:**

1. **Forward important TGIF emails to Gmail**
   - Add "TGIF:" to subject line
   - OR label with "TGIF" in Gmail

2. **Meetings happen automatically**
   - Otter.ai joins and transcribes
   - Summaries generated automatically

3. **Review outputs**
   - Individual meeting summaries in `knowledge/meetings/summaries/`
   - Daily email batches in `knowledge/emails/daily_batches/`
   - Task tracker in `knowledge/task_tracker.json`
   - Weekly digest (Friday 3pm)

### **Automated Actions:**

**Daily at 12pm:**
- Process flagged emails
- Update task tracker
- Check for overdue tasks

**Friday at 3pm:**
- Generate weekly rollup
- Send digest to stakeholders

---

## 🔧 CONFIGURATION

### **Schedule Times:**

Edit `.env`:
```bash
DAILY_EMAIL_TIME=12:00      # Daily email processing
WEEKLY_ROLLUP_TIME=15:00    # Weekly rollup (3pm)
WEEKLY_ROLLUP_DAY=friday    # Day for weekly rollup
```

### **Notification Recipients:**

```bash
STAKEHOLDER_EMAILS=justin@hcss.com,team@tgif.com,ops@tgif.com
```

### **Storage Paths:**

```bash
KNOWLEDGE_BASE_PATH=focuses/hcss/knowledge
TASK_TRACKER_PATH=focuses/hcss/knowledge/task_tracker.json
```

---

## 🐛 TROUBLESHOOTING

### **Otter API Not Working:**

Check MCP health:
```bash
curl http://localhost:8829/health
```

If status is "degraded", it's using Gmail fallback (this is normal).

### **Gmail Authentication Failed:**

1. Delete `token.json`
2. Run processor again
3. Complete OAuth flow in browser

### **No Emails Being Processed:**

Check query:
```bash
# Make sure emails have "TGIF" in subject or label
```

### **Task Tracker Not Updating:**

Check file permissions:
```bash
ls -la focuses/hcss/knowledge/task_tracker.json
```

---

## 📚 FILE OUTPUTS

### **Meeting Summaries:**
```
focuses/hcss/knowledge/meetings/
├── json/
│   └── TGIF_Meeting_2025-11-09_10am.json
└── summaries/
    └── TGIF_Meeting_2025-11-09_10am.md
```

### **Email Extracts:**
```
focuses/hcss/knowledge/emails/
├── TGIF_Email_2025-11-09_abc123.json
└── daily_batches/
    └── TGIF_Daily_Batch_2025-11-09.json
```

### **Task Tracker:**
```
focuses/hcss/knowledge/task_tracker.json
```

### **Weekly Rollups:**
```
focuses/hcss/knowledge/rollups/
└── TGIF_Rollup_2025-11-08.json
```

---

## 🚧 TODO

- [ ] Integrate Chat Mining Agent for better extraction
- [ ] Build weekly rollup generator
- [ ] Add Notion integration
- [ ] Add email notification system
- [ ] Add Slack notifications
- [ ] Build web dashboard
- [ ] Add meeting transcript processor
- [ ] Implement Microsoft Graph API integration (future)

---

## 📞 SUPPORT

Issues? Check:
1. Logs: `focuses/hcss/automation/logs/`
2. Health endpoints: `http://localhost:8829/health`
3. Task tracker: `task_tracker.json`

---

**Pipeline ready for setup. Follow steps above to get started.** ✅
