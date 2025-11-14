---
description: Weekly HCSS calendar sync to harmon.justin@gmail.com
---

# HCSS Calendar Sync Workflow

**Purpose:** Sync HCSS meeting placeholders from personal calendar to harmon.justin@gmail.com calendar  
**Frequency:** Weekly (Monday mornings)  
**Owner:** jh-assistant  
**Integration Layer:** All calendar inputs flow through jh-assistant

---

## 📋 WEEKLY REMINDER (Every Monday)

**Trigger:** Monday 8:00 AM CST  
**Action:** Prompt Justin to provide HCSS meeting details for the week

**Reminder Message:**
```
🗓️ HCSS Calendar Sync Reminder

Time to sync HCSS meetings to harmon.justin@gmail.com:

1. Open Microsoft Teams/Outlook calendar (week view)
2. Take screenshot (Cmd+Shift+4) - saves to Dropbox Screenshots
3. Run: cd 8825_core/workflows && ./sync_hcss_calendar.sh
4. Verify events created in harmon.justin@gmail.com

The script will automatically:
- Sync screenshot from Dropbox Screenshots folder
- OCR extract all HCSS meetings
- Create calendar events with correct times
- Add to harmon.justin@gmail.com calendar

Estimated time: 2-3 minutes
```

---

## 🔄 SYNC PROCESS

### **Step 1: Take Calendar Screenshot**
- Open Microsoft Teams/Outlook calendar (week view)
- **Important:** Ensure meeting titles are visible in the calendar
- Take screenshot (Cmd+Shift+4 on Mac) - select area with meetings
- Screenshot auto-saves to Dropbox Screenshots folder
- **Note:** Dropbox Screenshots folder is locked - cannot move it
- **Tip:** Zoom out if needed to show full week with all meeting titles

### **Step 2: Sync Screenshot to Intake Folder**
```bash
cd INBOX_HUB
./sync_screenshots.sh
```

This syncs from Dropbox Screenshots → Intake folder where OCR can access it.

### **Step 3: Run OCR Sync Script**
```bash
cd 8825_core/integrations/google
python3 calendar_screenshot_sync.py
```

The script will:
- Auto-find latest screenshot (checks Intake → Dropbox → Downloads)
- OCR extract meeting details
- Identify HCSS meetings by pattern matching
- Create events in harmon.justin@gmail.com

### **Step 4: Verify Sync**
- Check harmon.justin@gmail.com calendar
- Verify all HCSS meetings created
- Adjust times if OCR missed anything
- Delete any duplicates

---

## 📅 COMMON HCSS MEETINGS

### **Recurring Meetings:**

**JustinBecky Check-in**
- Platform: Microsoft Teams
- Frequency: Weekly (varies)
- Calendar: harmon.justin@gmail.com

**TGIF Internal Touchbase**
- Platform: Microsoft Teams
- Frequency: Weekly
- Calendar: harmon.justin@gmail.com

**TGI Fridays Meetings**
- Crunchtime integration sessions
- Weekly accounting/project calls
- Toast Weekly Sync
- PM Sync Online

**Crunchtime Meetings**
- Toast Readiness Kick Off
- Weekly project calls
- Integration working sessions

**Portal Development Weekly Touchbase**
- Platform: Microsoft Teams
- Frequency: Weekly (Tuesday 1 PM)
- Calendar: harmon.justin@gmail.com
- Project: Portal development for HCSS

---

## 🤖 AUTOMATION OPTIONS

### **Option A: Manual with Templates (Current)**
- **Why:** Microsoft calendar API blocked by IT restrictions
- **How:** Use quick-copy templates from `hcss_calendar_templates.md`
- **Time:** 15-20 min first-time setup, 2-3 min weekly verification
- **Process:**
  1. One-time: Create all recurring events from templates
  2. Weekly: Verify times on Monday morning
  3. As needed: Add one-off meetings

### **Option B: Semi-Automated (Blocked)**
- Requires Microsoft Graph API access
- IT restrictions prevent automation
- Not feasible with current setup

### **Option C: Fully Automated (Future)**
- Would require IT to enable API access
- Or migrate HCSS meetings to Google Calendar
- Not recommended - keep work calendar separate

---

## 🎯 INTEGRATION WITH JH-ASSISTANT

This workflow is designed to integrate with the `jh-assistant` layer:

- **Reminder Trigger:** Monday 8:00 AM CST (to be implemented)
- **Action:** Prompt for HCSS meeting details
- **Current:** Manual trigger via `hcss-cal-sync` command
- **Tracking:** Update `8825_Jh.json` with sync status

### Quick Command

After taking screenshot, run:
```bash
hcss-cal-sync
```

This alias (defined in `~/.zshrc`) runs the complete sync pipeline.

**Future Enhancement:**
- jh-assistant API integration
- Smart conflict detection

---

## 📝 PRODUCTION CHECKLIST

**Every Monday Morning:**
- [ ] Take screenshot of Microsoft calendar (week view)
- [ ] Run: `hcss-cal-sync`
- [ ] Verify 12 events created in harmon.justin@gmail.com
- [ ] Total time: 2-3 minutes

**Setup Complete:**
- ✅ OCR script created and tested
- ✅ Screenshot sync pipeline integrated
- ✅ Shell alias `hcss-cal-sync` configured
- ✅ Google Calendar API authenticated
- ✅ 12 meeting templates configured
- [ ] Verify sync completed
- [ ] Note any issues or conflicts

---

## 🔧 TROUBLESHOOTING

**Issue: Duplicate events**
- Check both calendars for existing events
- Delete duplicates from harmon.justin@gmail.com
- Re-sync from personal calendar

**Issue: Missing meetings**
- Verify meeting is HCSS-related
- Check personal calendar visibility
- Manually create if needed

**Issue: Time zone conflicts**
- All times should be CST
- Verify calendar time zone settings
- Update events if needed

---

## 📊 TRACKING

**Metrics:**
- Weekly sync completion rate
- Number of meetings synced
- Time spent on sync process
- Automation opportunities identified

**Log Location:** `8825_core/projects/8825_Jh.json` → household_tasks or new calendar_sync section

---

**Created:** 2025-11-10  
**Owner:** jh-assistant  
**Status:** Active  
**Next Review:** 2025-11-17
