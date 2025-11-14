# Script Evolution Analysis - v3.0 Alignment

**Date:** 2025-11-10  
**Context:** Two LaunchAgents had outdated paths + exposed credentials. Analyzing scripts for v3.0 alignment.

---

## Scripts Analyzed

### 1. `simple_sync_and_process.sh` (Inbox Pipeline)
**Current Location:** `INBOX_HUB/simple_sync_and_process.sh`  
**LaunchAgent:** `com.8825.inbox-pipeline.plist` (✅ Fixed, Active)

**What It Does:**
- Syncs iCloud Downloads → Local Downloads
- Processes documents through ingestion engine
- Archives processed files
- Syncs cleanup back to iCloud

**Status:** ✅ **KEEP AS-IS**
- Already in correct location
- LaunchAgent path fixed
- No credentials needed
- Aligns with v3.0 philosophy (minimal, focused)

**Action:** None needed

---

### 2. `8825_gmail_extractor.py` (HCSS Gmail Automation)
**Expected Location:** `focuses/hcss/8825_gmail_extractor.py`  
**LaunchAgent:** `com.hcss.gmail.ingest.plist` (🚫 Disabled)

**What It Was Supposed To Do:**
- Monitor Gmail for TGIF emails
- Extract action items
- Update task tracker

**Status:** ⚠️ **SCRIPT DOESN'T EXIST**
- Was from v2.1 system
- Functionality replaced by newer HCSS automation
- LaunchAgent disabled (had exposed credentials)

**Current Alternative:**
- `focuses/hcss/automation/processors/daily_email_processor.py`
- Part of TGIF Meeting Automation Pipeline
- More comprehensive solution

**Action:** Archive old LaunchAgent, document migration

---

### 3. `hcss-cal-sync` Shell Alias
**Current Definition:** Points to v3.0 path (doesn't exist)

```bash
alias hcss-cal-sync='cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system/8825_core/workflows" && ./sync_hcss_calendar.sh'
```

**What It Does:**
- Syncs HCSS calendar screenshots
- OCR processing
- Creates Google Calendar events

**Status:** ⚠️ **NEEDS PATH UPDATE**

**Action:** Update ~/.zshrc to point to 8825-system

---

## Recommended Actions

### Immediate (Do Now)

1. **Update hcss-cal-sync alias**
   - Fix path in ~/.zshrc
   - Test that script exists at new location

2. **Archive old Gmail LaunchAgent**
   - Already disabled
   - Document why (replaced by better solution)

### Future (When Needed)

3. **Consolidate HCSS automation**
   - Current: Multiple scattered scripts
   - Goal: Single entry point per workflow
   - Aligns with minimal documentation philosophy

---

## V3.0 Philosophy Alignment

### ✅ What's Good

**Inbox Pipeline:**
- Single focused script
- No external dependencies beyond Python
- Clear, linear workflow
- Runs automatically, stays out of the way

### ⚠️ What Needs Work

**HCSS Automation:**
- Multiple entry points (calendar sync, email processing, Otter integration)
- Scattered across different locations
- No single "run HCSS automation" command
- Over-documented, under-unified

### 💡 Recommendation

**Create unified HCSS automation entry point:**
```bash
# Single command for all HCSS automation
hcss-automate [calendar|email|otter|all]
```

**Benefits:**
- One command to remember
- Easier to maintain
- Aligns with minimal documentation (code is the doc)
- Follows inbox pipeline pattern (works well)

---

## Dependencies to Update

### 1. ~/.zshrc
- Line 13: `hcss-cal-sync` alias path

### 2. LaunchAgents (Already Fixed)
- ✅ `com.8825.inbox-pipeline.plist` - Updated
- 🚫 `com.hcss.gmail.ingest.plist` - Disabled (obsolete)
- 🚫 `com.8825.mcp-servers.plist` - Disabled (not needed)

### 3. Memory/Documentation
- ✅ Gmail app password stored in memory
- ✅ OpenAI API key stored in memory
- ⚠️ hcss-cal-sync memory still references v3.0 path

---

## Next Steps

1. Update hcss-cal-sync alias
2. Update hcss-cal-sync memory
3. Test calendar sync workflow
4. (Future) Consider unified HCSS automation command
