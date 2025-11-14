# 8825 User Guide

**Version:** 3.0.0  
**Last Updated:** 2025-11-10  
**Status:** Living document - update as system evolves

---

## 🎯 What is 8825?

8825 is your **personal AI operating system** - a collection of protocols, workflows, and automations that help you manage work across multiple projects (HCSS, Joju, real estate, personal tasks).

**Think of it as:** Your AI assistant's instruction manual for how to help YOU specifically.

---

## 🚀 Quick Start (5 minutes)

### **1. Understand the Structure**

```
8825_v3.0/
├── 8825_core/          # The system (protocols, agents, workflows)
├── users/              # Your private data
├── focuses/            # Your workspaces (symlinks to users/)
└── 8825_index/         # Fast search
```

**Key concept:** Core is shareable, users/ is private.

---

### **2. Activate 8825 Mode**

In any Cascade chat:

```
User: "Load 8825"
```

Cascade will:
- Load protocols from checkpoint
- Understand your workspace structure
- Know your preferences (direct, code-first, fast decisions)
- Display message counter

**You'll see:**
```
💬 Message 1/150 | Mode: Exploratory | ✅
```

---

### **3. Work in a Focus**

**Focuses are your workspaces:**
- `focuses/hcss/` - HCSS client work
- `focuses/joju/` - Joju library management
- `focuses/jh_assistant/` - Personal tasks

**To work in a focus:**
```bash
cd focuses/hcss
# Now you're in HCSS focus
```

**Or tell Cascade:**
```
User: "Activate HCSS focus"
```

---

## 📋 Core Concepts

### **1. Modes**

**8825 Mode (General):**
- Default mode
- General assistance
- Exploration work
- System maintenance

**Focus Modes:**
- **HCSS Focus:** Client work (email ingestion, meeting summaries, task tracking)
- **Joju Focus:** Library management (contribution tracking, mining)
- **JH Assistant Focus:** Personal tasks (calendar, reminders, automation)

---

### **2. Protocols**

Protocols are rules Cascade follows. Key ones:

**Message Counter Protocol:**
- Shows message count on every response
- Warns at thresholds (50, 80, 100)
- Prevents context loss

**Learning Protocol:**
- Cascade learns from corrections
- Updates brain state
- Adapts to your preferences

**Focus Protocols:**
- Each focus has specific workflows
- Cascade knows what tools are available
- Follows focus-specific rules

---

### **3. Brain State**

Your "brain" is saved context that persists across chats.

**Location:** `~/Downloads/8825_brain/`

**Contains:**
- Active projects
- Recent decisions
- Ongoing tasks
- System state

**Commands:**
- `refresh brain` - Re-load brain state mid-chat
- `save brain` - Save current context
- `check brain` - View current brain state

---

### **4. Explorations**

Explorations are ideas you're testing.

**Location:** `8825_core/explorations/`

**Lifecycle:**
1. **Brainstorm** - Initial idea
2. **Exploration** - Testing feasibility
3. **PoC** - Proof of concept
4. **Production** - Fully working

**Current active:** 6 explorations (see `CURRENT_STATUS.md`)

---

## 🔧 Common Tasks

### **Process Inbox**

```
User: "Process inbox"
```

Cascade will:
1. Check `~/Downloads/8825_inbox/`
2. Process files (JSON, TXT, MD, DOCX)
3. Route to appropriate focus
4. Archive processed files

---

### **Ingest HCSS Email**

```
User: "Activate HCSS focus"
User: "Ingest gmail"
```

Cascade will:
1. Fetch flagged emails
2. Extract key points
3. Update task tracker
4. Save to daily email log

---

### **Mine Otter Transcript**

```
User: "Activate HCSS focus"
User: "Ingest otter"
```

Cascade will:
1. Fetch latest transcript
2. Extract decisions/actions
3. Route to projects (HCSS/RAL/TGIF)
4. Update task tracker

---

### **Update Joju Library**

```
User: "Activate Joju focus"
User: "Add contribution: [details]"
```

Cascade will:
1. Parse contribution details
2. Update master library
3. Generate attribution
4. Save to library JSON

---

### **Search the System**

```bash
# Fast index-based search
python3 8825_core/workflows/search.py "query"
```

Returns results in <1 second (2.3ms average).

---

### **Check System Status**

```
User: "System status"
```

Cascade will show:
- Active focuses
- MCP servers status
- Recent activity
- Pending tasks

---

## 🎓 Advanced Usage

### **Long Chat Management**

**Message counter shows:**
```
💬 Message 50/150 | Mode: Exploratory | ⚠️ Brain refresh recommended
```

**At 50 messages (exploratory):**
- Run `refresh brain` to re-anchor

**At 100 messages (production):**
- Close chat and start fresh
- Run exit protocol first

---

### **Brain Refresh**

When Cascade seems to lose context:

```
User: "refresh brain"
```

Cascade will:
1. Re-read brain state
2. Re-load protocols
3. Confirm current mode/focus
4. Summarize context

---

### **Exit Protocol**

Before closing production chats:

```
User: "exit focus"
```

Cascade will:
1. Summarize session
2. Save brain state
3. Update activity log
4. Provide resume command

---

### **Create New Focus**

```
User: "Create focus: [name]"
```

Cascade will:
1. Create user folder structure
2. Create symlink in focuses/
3. Set up templates
4. Initialize brain state

---

## 📊 Understanding the Dashboard

### **Message Counter**

```
💬 Message 25/150 | Mode: Exploratory | ✅
```

**Format:** `Message [current]/[threshold] | Mode: [mode] | [status]`

**Status indicators:**
- ✅ Normal
- ⚠️ Brain refresh recommended
- 🔴 Consider closing chat
- 🛑 Exit protocol recommended

---

### **Thresholds by Mode**

| Mode | Refresh | Warning | Max |
|------|---------|---------|-----|
| **Production** | - | 80 | 100 |
| **Exploratory** | 50 | 150 | - |
| **Ad-hoc** | - | 15 | 20 |

---

## 🚨 Troubleshooting

### **Cascade doesn't recognize 8825**

**Problem:** Protocol not loaded  
**Solution:** Close chat and start fresh

---

### **Message counter not showing**

**Problem:** Protocol not active  
**Solution:** 
1. Check if 8825 mode loaded
2. Restart chat if needed
3. Verify checkpoint includes protocols

---

### **Context seems lost**

**Problem:** Long chat, no refresh  
**Solution:**
1. Check message count
2. Run `refresh brain`
3. If >100 messages, close and restart

---

### **MCP servers not responding**

**Problem:** Servers not running  
**Solution:**
```bash
# Check status
ps aux | grep mcp

# Restart if needed
launchctl unload ~/Library/LaunchAgents/com.8825.*.plist
launchctl load ~/Library/LaunchAgents/com.8825.*.plist
```

---

### **Inbox not processing**

**Problem:** Automation not running  
**Solution:**
```bash
# Check cron
crontab -l

# Manual process
cd ~/Downloads/8825_inbox
python3 /path/to/8825_core/inbox/process_inbox.py
```

---

## 📖 Key Files to Know

### **System Files**

- `README.md` - System overview
- `8825_core/protocols/` - All protocols
- `8825_core/agents/` - Available agents
- `8825_index/master_index.json` - Search index

---

### **Your Files**

- `users/justin_harmon/profile.json` - Your profile
- `users/justin_harmon/.env` - Your credentials
- `~/Downloads/8825_brain/` - Your brain state
- `~/Downloads/8825_inbox/` - Your inbox

---

### **Focus Files**

**HCSS:**
- `focuses/hcss/task_tracker.json` - Active tasks
- `focuses/hcss/daily_emails/` - Email logs
- `focuses/hcss/meeting_summaries/` - Meeting notes

**Joju:**
- `focuses/joju/JH_master_library.json` - Your library
- `focuses/joju/contributions/` - Contribution logs

---

## 🎯 Best Practices

### **1. Use Focuses**

Don't mix work types in one chat. Activate the right focus:
- HCSS work → HCSS focus
- Library work → Joju focus
- Personal tasks → JH Assistant focus

---

### **2. Monitor Message Count**

Watch the counter. When you see warnings:
- 50 messages → Refresh brain
- 80 messages → Consider closing
- 100 messages → Close and restart

---

### **3. Save Brain State**

Before closing important chats:
```
User: "save brain"
```

This preserves context for next session.

---

### **4. Keep Explorations Moving**

Don't let ideas sit. Every 2 weeks:
- Review `CURRENT_STATUS.md`
- Promote or archive
- Keep pipeline flowing

---

### **5. Trust the System**

8825 learns from you. The more you use it:
- Better it understands your preferences
- Faster it works
- More accurate it becomes

---

## 🚀 Next Steps

### **New User Checklist**

- [ ] Read this guide
- [ ] Test 8825 mode activation
- [ ] Try one focus (HCSS or Joju)
- [ ] Process inbox once
- [ ] Run brain refresh
- [ ] Check system status

---

### **Weekly Maintenance**

- [ ] Review explorations status
- [ ] Check brain state
- [ ] Verify MCP servers running
- [ ] Process inbox backlog
- [ ] Update task tracker

---

### **Monthly Review**

- [ ] Evaluate active explorations
- [ ] Promote or archive items
- [ ] Update protocols if needed
- [ ] Review system metrics
- [ ] Plan next month's focus

---

## 💡 Tips & Tricks

### **Faster Workflows**

Use shortcuts:
- `rb` instead of `refresh brain`
- `ss` instead of `system status`
- `pi` instead of `process inbox`

---

### **Better Context**

Give Cascade context upfront:
```
User: "Working on TGIF rollout. Need to review last week's decisions and update tracker."
```

Better than:
```
User: "What did we decide last week?"
```

---

### **Effective Exploration**

When brainstorming:
1. Start with problem statement
2. Explore 2-3 solutions
3. Pick one and build PoC
4. Don't over-document

---

### **Smart Delegation**

Let Cascade handle:
- ✅ Repetitive tasks (email processing)
- ✅ Data extraction (meeting summaries)
- ✅ Status updates (task tracking)

You handle:
- ⚠️ Strategic decisions
- ⚠️ Client communication
- ⚠️ Creative work

---

## 📚 Additional Resources

### **Documentation**

- `8825_core/protocols/README.md` - Protocol reference
- `TEST_REPORT_2025-11-09.md` - System validation
- `GOOSE_INTEGRATION_ROADMAP.md` - Future plans
- `8825_core/explorations/CURRENT_STATUS.md` - Active work

---

### **Key Protocols**

- `8825_message_counter_protocol.json` - Message counting
- `8825_hcss_focus.json` - HCSS workflows
- `8825_joju_focus.json` - Joju workflows
- `8825_learning_protocol.json` - Learning system

---

## 🎓 Philosophy

### **8825 Principles**

1. **Direct, code-first** - Show, don't tell
2. **Fast decisions** - Sensible defaults, move quickly
3. **Learn and adapt** - System improves with use
4. **Focus on shipping** - Done > perfect
5. **Trust the process** - Let automation handle routine work

---

### **When to Use 8825**

**Good for:**
- ✅ Repetitive workflows
- ✅ Data processing
- ✅ Status tracking
- ✅ Context management
- ✅ Knowledge capture

**Not good for:**
- ❌ Strategic planning (you do this)
- ❌ Client communication (you do this)
- ❌ Creative work (you do this)

---

## 🔄 Version History

**v3.0.0 (2025-11-09):**
- Complete architecture refactor
- User/system separation
- Fast discovery (<1 second)
- Message counter protocol

**v2.1.0 (2025-10):**
- Advanced features
- Multiple focuses
- Learning protocol

**v2.0.0 (2025-09):**
- Unified base
- Core protocols
- Agent system

---

## 📞 Getting Help

### **In Chat**

```
User: "Help with [topic]"
```

Cascade will explain or point to docs.

---

### **Check Status**

```
User: "System status"
User: "Check brain"
User: "List protocols"
```

---

### **Debug Issues**

```
User: "Debug [issue]"
```

Cascade will diagnose and suggest fixes.

---

## ✅ Summary

**8825 is your AI operating system.**

**Key concepts:**
- Modes (8825, HCSS, Joju, JH Assistant)
- Protocols (rules Cascade follows)
- Brain state (persistent context)
- Explorations (ideas in testing)

**Common tasks:**
- Process inbox
- Ingest email/transcripts
- Update libraries
- Search system

**Best practices:**
- Use focuses
- Monitor message count
- Save brain state
- Keep explorations moving

**When in doubt:** `refresh brain` or start fresh chat.

---

**You're ready. Start using 8825.** 🚀

---

**Last updated:** 2025-11-10  
**Next review:** 2025-11-24
