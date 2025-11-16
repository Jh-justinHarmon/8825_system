# Current TGIF Meeting Summary Workflow

**Status:** Production Ready  
**Last Updated:** 2025-11-14  
**Automation Level:** 90% automated, 10% manual (edge cases)

---

## 📋 Complete Workflow

### **Step 1: Automatic Processing (Weekly/As Needed)**

```bash
cd /path/to/8825-system/8825_core/workflows/meeting_automation
python3 process_meetings.py
```

**What Happens:**
1. **Polls Gmail** for unread Otter.ai emails
2. **Filters** promotional emails (11 filtered in production)
3. **Detects duplicates** (prevents re-processing)
4. **Extracts transcripts** from email body
5. **Processes with GPT-4 Turbo** using:
   - Brain Transport (system context)
   - TGIF Knowledge Base (people, systems, stores, vendors)
6. **Corrects transcription errors:**
   - "net sweet" → "NetSuite"
   - "edward dawn" → "Edward Don"
   - "crunch time" → "Crunchtime"
   - Store numbers (1887, 1191, etc.)
7. **Extracts structured data:**
   - Decisions (with category, impact, confidence)
   - Action items (who, what, due, priority)
   - Risks (severity, mitigation, owner)
   - Blockers (impact, resolution needed)
   - Issues discussed (status, owner, notes)
8. **Saves outputs:**
   - JSON: `8825_files/HCSS/meetings/[date]_[title].json`
   - Markdown: `8825_files/HCSS/meetings/[date]_[title].md`
9. **Marks emails as read**

**Cost:** ~$0.09 per meeting  
**Time:** ~30 seconds per meeting  
**Accuracy:** High (validated corrections)

---

### **Step 2: Handle Empty Transcripts (If Needed)**

**When:** System shows `⚠️ MEETINGS NEED MANUAL TRANSCRIPTS`

**Manual Workflow:**
```
1. Open Otter.ai link (shown in output)
2. Click "Export" → "Export to text (.txt)"
3. Save to Downloads folder
4. Re-run: python3 process_meetings.py
   → Auto-detects and processes txt file
```

**Automatic Processing:**
- Checks Downloads folder for `*_otter_ai.txt` files
- Validates they're Otter transcripts (timestamp format)
- Processes with same GPT-4 + context
- Moves to `Downloads/processed_transcripts/`

**Why This Happens:**
- Some Otter emails don't include transcript in body
- Only have "View in Otter" link
- Manual export required

**Frequency:** Occasional (not every meeting)

---

### **Step 3: Query/Summarize Meetings**

**Query by Date Range:**
```bash
# Last week
python3 meeting_recall.py --last-week

# Specific range
python3 meeting_recall.py --from 2025-11-12 --to 2025-11-13

# Last N days
python3 meeting_recall.py --last-7-days
```

**Output Format:**
```markdown
# Meeting Summary: 2025-11-12 to 2025-11-13

**Total Meetings:** 4
**Date Range:** 2025-11-12 to 2025-11-13

---

## 📋 Individual Meetings

### 1. TGIF Store Rollout Project Meeting
**Date:** 2025-11-13
**Type:** project_call
**Attendees:** Justin, Tricia, Josh

**Key Topics:**
- Store rollout timeline
- Vendor setup issues
- Inventory management

---

## 🎯 All Decisions (2)
- **Correct Edward Don vendor setup** (technical, high impact)
- **Copy settings from 4169 to new locations** (operational, medium impact)

## ✅ All Action Items (5)

### Josh Matulsky
- Add Edward Don to vendor list (Due: TBD, Priority: critical)
- Validate inventory postings (Due: TBD, Priority: high)

### Tricia McHargue
- Copy location settings from 4169 (Due: TBD, Priority: high)

## ⚠️ All Risks (1)

### MEDIUM
- Potential delay in store openings due to vendor setup
  - Mitigation: Prioritize vendor setup and confirm lists

## 🚫 All Blockers (0)

## 📌 All Issues (2)
- Edward Don vendor setup incomplete
- Location settings need copying
```

---

## 📁 Output Structure

```
8825_files/HCSS/meetings/
├── 2025-11-13_tgif_store_rollout_project_meeting.json
├── 2025-11-13_tgif_store_rollout_project_meeting.md
├── 2025-11-14_system_and_vendor_setup_review.json
├── 2025-11-14_system_and_vendor_setup_review.md
└── ...

Downloads/processed_transcripts/
├── Justin's Meeting Notes_otter_ai.txt
└── ...
```

---

## 📊 Individual Meeting Output (Markdown)

Each meeting generates a markdown file with:

### **1. Header**
```markdown
# System and Vendor Setup Review

**Date:** 2025-11-14
**Type:** other
**Attendees:** Tricia McHargue, Josh Matulsky
```

### **2. Transcription Corrections**
```markdown
## 🔧 Transcription Corrections

- **Edward dawn** → **Edward Don** (high confidence)
  - Based on project context, 'Edward Don' is a known vendor
- **1548 i** → **1548** (high confidence)
  - The 'i' appears to be a transcription error
```

### **3. Key Topics**
```markdown
## 📋 Key Topics

- Inventory and vendor setup for new locations
- Edward Don vendor setup and product listing issues
```

### **4. Decisions**
```markdown
## 🎯 Decisions

### To correct the Edward Don vendor setup for California location.
- **Category:** technical
- **Impact:** high
- **Context:** Ensuring all locations have correct vendor lists
```

### **5. Action Items**
```markdown
## ✅ Action Items

| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Add Edward Don to vendor list | Josh Matulsky | TBD | critical |
| Copy location settings from 4169 | Tricia McHargue | TBD | high |
```

### **6. Risks**
```markdown
## ⚠️ Risks

### Potential delay in store openings
- **Severity:** medium
- **Mitigation:** Prioritize vendor setup
- **Owner:** Josh Matulsky
```

### **7. Issues Discussed**
```markdown
## 📌 Issues Discussed

- **Edward Don vendor setup incomplete** (in_progress)
  - Owner: Josh Matulsky
  - Notes: Need to add vendor products
```

### **8. Additional Notes**
```markdown
## 📝 Additional Notes

The meeting focused on operational setup for new locations,
with emphasis on inventory and vendor management.
```

---

## 🔄 Current Gaps & Manual Steps

### **What's Automated (90%)**
- ✅ Gmail polling
- ✅ Email filtering (promotional, duplicates)
- ✅ Transcript extraction
- ✅ GPT-4 processing with context
- ✅ Transcription error correction
- ✅ Structured data extraction
- ✅ File saving (JSON + Markdown)
- ✅ Email marking as read
- ✅ Downloads folder monitoring

### **What's Manual (10%)**
- ⚠️ Empty transcript export (when email lacks transcript)
- ⚠️ Review/edit outputs (if corrections needed)
- ⚠️ Generate consolidated summaries (run meeting_recall.py)

---

## 💡 Improvement Opportunities

### **1. Automatic Summary Generation**
**Current:** Manual - run `meeting_recall.py` when needed  
**Ideal:** Auto-generate weekly summary  
**Implementation:** Cron job or scheduled task

### **2. Distribution**
**Current:** Files saved locally  
**Ideal:** Auto-email summary to team  
**Implementation:** Email integration + template

### **3. Action Item Tracking**
**Current:** Static list in markdown  
**Ideal:** Sync to task management (Notion, etc.)  
**Implementation:** Notion API integration

### **4. Empty Transcript Handling**
**Current:** Manual export from Otter  
**Ideal:** Auto-fetch via Otter API  
**Implementation:** Otter.ai API integration (if available)

### **5. Auditing**
**Current:** Manual review  
**Ideal:** Automatic quality checks  
**Implementation:** ✅ **DONE - Auditor Agent built!**

---

## 🎯 Recommended Usage Pattern

### **Weekly Routine**

**Monday Morning:**
```bash
# 1. Process last week's meetings
cd /path/to/meeting_automation
python3 process_meetings.py

# 2. Generate weekly summary
python3 meeting_recall.py --last-week > weekly_summary.md

# 3. Review and distribute
# - Open weekly_summary.md
# - Review for accuracy
# - Share with team
```

**As Needed:**
```bash
# Process specific meeting
python3 check_downloads_for_transcripts.py

# Query specific date range
python3 meeting_recall.py --from 2025-11-10 --to 2025-11-15
```

---

## 📈 Production Metrics

### **First Production Run (Nov 13, 2025)**
- Emails found: 15
- Meetings processed: 4
- Promotional filtered: 11
- Duplicates skipped: 0
- Cost: $0.35
- Time: 2 minutes
- Accuracy: High

### **Typical Weekly Run**
- Meetings: 2-4 per week
- Cost: $0.18-0.36 per week
- Time: 1-2 minutes
- Manual intervention: 0-1 times (empty transcripts)

---

## 🔧 Troubleshooting

### **"No meetings found"**
- Check Gmail for unread Otter.ai emails
- Verify emails aren't marked as read
- Check date range in query

### **"Empty transcript"**
- Follow manual export workflow
- Save to Downloads folder
- Re-run process_meetings.py

### **"Transcription errors not corrected"**
- Update TGIF_KNOWLEDGE.json with new terms
- Add to context_hints section
- Re-process if needed

### **"Missing action items"**
- Check if they're in "issues_discussed" instead
- Review JSON file for raw extraction
- Consider updating GPT-4 prompt

---

## 📚 Key Files

### **Processing Scripts**
- `process_meetings.py` - Main automation
- `check_downloads_for_transcripts.py` - Downloads processor
- `meeting_processor.py` - GPT-4 processing logic
- `gmail_otter_poller.py` - Gmail integration

### **Query/Summary**
- `meeting_recall.py` - Query and summarize meetings

### **Context**
- `8825_files/HCSS/TGIF_KNOWLEDGE.json` - Domain knowledge
- `~/Documents/8825_BRAIN_TRANSPORT.json` - System context

### **Output**
- `8825_files/HCSS/meetings/*.json` - Structured data
- `8825_files/HCSS/meetings/*.md` - Human-readable summaries

### **Documentation**
- `README.md` - Quick start guide
- `DEPLOYMENT_SUMMARY.md` - Production validation
- `DOWNLOADS_WORKFLOW.md` - Empty transcript handling

---

## 🎓 What Makes This Work

### **1. Context-Enhanced Processing**
- Brain Transport: System-wide context
- TGIF Knowledge: Project-specific context
- GPT-4 Turbo: High-accuracy model

### **2. Error Correction**
- Common transcription errors pre-defined
- Phonetic similarity detection
- Context-based validation

### **3. Structured Extraction**
- Consistent JSON schema
- Confidence scoring
- Category classification

### **4. Quality Assurance**
- Filters promotional emails
- Detects duplicates
- Saves raw data (no data loss)
- Transparent corrections

---

## 🚀 Next Steps

### **Immediate (This Week)**
1. ✅ Run weekly processing
2. ✅ Generate weekly summary
3. ✅ Review outputs for accuracy

### **Short-term (This Month)**
1. Set up weekly cron job
2. Create email distribution template
3. Integrate with Notion for action items

### **Long-term (This Quarter)**
1. Add Otter.ai API integration
2. Build dashboard for metrics
3. Add predictive analytics (risk patterns, etc.)

---

**Status:** ✅ Production Ready  
**Automation:** 90%  
**Accuracy:** High  
**Cost:** ~$0.09/meeting  
**Time Savings:** ~15 min/meeting (vs manual)
