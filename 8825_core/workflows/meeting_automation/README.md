# Meeting Automation - High-Fidelity Processing

**Status:** Production Ready  
**Model:** GPT-4 Turbo  
**Approach:** Context-Enhanced Extraction

---

## 🎯 What This Does

Automatically processes Otter.ai meeting transcripts with high fidelity:

1. **Polls Gmail** for new Otter.ai emails
2. **Extracts transcripts** from emails
3. **Processes with GPT-4** using Brain Transport + TGIF knowledge for context
4. **Corrects transcription errors** (names, systems, numbers)
5. **Extracts structured data** (decisions, actions, risks, blockers)
6. **Saves to your files** in 8825_files/HCSS/meetings/
7. **Query anytime** by date range

---

## 🚀 Quick Start

### **Setup (One Time)**

1. **Set OpenAI API Key:**
```bash
export OPENAI_API_KEY="your-api-key-here"
# Add to ~/.zshrc to persist
```

2. **Install Dependencies:**
```bash
pip3 install openai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

3. **Authenticate Gmail:**
```bash
cd /path/to/8825-system/8825_core/integrations/google
python3 search_gmail.py "test"
# Follow OAuth flow in browser
```

---

## 📋 Usage

### **Process New Meetings**
```bash
cd /path/to/8825-system/8825_core/workflows/meeting_automation
python3 process_meetings.py
```

This will:
1. Search Gmail for new Otter.ai emails
2. Filter out promotional emails and duplicates
3. Process each meeting with GPT-4
4. Save structured JSON and Markdown files
5. Mark emails as read
6. **NEW:** Check Downloads folder for exported transcripts

**If transcript is missing from email:**
```
⚠️  MEETINGS NEED MANUAL TRANSCRIPTS:

Meeting: Justin's Meeting Notes
Link: https://otter.ai/u/abc123

📋 WORKFLOW:
  1. Open: https://otter.ai/u/abc123
  2. Click 'Export' → 'Export to text (.txt)'
  3. Save to Downloads folder
  4. Run this script again - it will auto-detect and process
```

### Process Downloads Folder Only

```bash
# Process all Otter transcripts in Downloads
python3 check_downloads_for_transcripts.py

# Process but don't move files to archive
python3 check_downloads_for_transcripts.py --no-move
```

### Query Previous Meetings

```bash
# Get meetings for specific date range
python3 meeting_recall.py --from 2025-11-12 --to 2025-11-13

# Get last week's meetings
python3 meeting_recall.py --last-week

# Get last month's meetings
python3 meeting_recall.py --last-month

# Save to file
python3 meeting_recall.py --from 2025-11-12 --output summary.md
```

---

## 📁 File Structure

```
8825_files/HCSS/meetings/
├── 2025-11-12_crunchtime_accounting_integration.json
├── 2025-11-12_crunchtime_accounting_integration.md
├── 2025-11-12_crunchtime_project_call.json
├── 2025-11-12_crunchtime_project_call.md
├── 2025-11-13_justins_meeting_notes.json
└── 2025-11-13_justins_meeting_notes.md
```

**Each JSON contains:**
- Original Gmail data
- Processed data from GPT-4
- Corrections made
- Decisions, actions, risks, blockers
- Processing metadata (tokens, cost)

---

## 🧠 Context Files

### **Brain Transport**
- Location: `~/Documents/8825_BRAIN_TRANSPORT.json`
- Contains: System architecture, projects, workflows
- Used for: Understanding technical references

### **TGIF Knowledge**
- Location: `8825_files/HCSS/TGIF_KNOWLEDGE.json`
- Contains: People, systems, stores, terms, initiatives
- Used for: Correcting names, interpreting context

---

## 🔧 Components

### **1. Gmail Poller** (`gmail_otter_poller.py`)
- Searches Gmail for Otter.ai emails
- Extracts transcript from email body
- Saves raw data
- Marks as read

### **2. Meeting Processor** (`meeting_processor.py`)
- Loads context (Brain + TGIF knowledge)
- Sends to GPT-4 Turbo with context
- Extracts structured data
- Corrects transcription errors
- Saves JSON + Markdown

### **3. Meeting Recall** (`meeting_recall.py`)
- Queries meetings by date range
- Aggregates decisions, actions, risks
- Generates consolidated summaries
- Outputs Markdown or JSON

### **4. Main Workflow** (`process_meetings.py`)
- Orchestrates poll → process → save
- Handles errors gracefully
- Reports summary

---

## 💰 Cost

**Per Meeting (average):**
- ~4,500 tokens (context + transcript + output)
- ~$0.045 per meeting with GPT-4 Turbo

**Per Month (12 meetings):**
- ~$0.54/month

**Worth it for business-critical accuracy.**

---

## 🎯 What Gets Corrected

**Common Transcription Errors:**
- "net sweet" → "NetSuite"
- "crunch time" → "Crunchtime"
- "eighteen eighty-seven" → "1887 (Dover, DE store)"
- "Trisha" → "Tricia (Finance lead)"
- "the seventeenth" → "2025-11-17"

**Context Applied:**
- Names expanded (first → full name + role)
- Systems identified (Toast, NetSuite, Crunchtime)
- Store numbers interpreted (1887, 1191)
- Dates extracted (YYYY-MM-DD format)

---

## 📊 Output Example

**Markdown Summary:**
```markdown
# TGI Fridays | Crunchtime - Weekly Accounting Integration

**Date:** 2025-11-12  
**Type:** accounting_integration  
**Attendees:** Justin Harmon, Patricia McHargue, Finance Team

## 🔧 Transcription Corrections
- **net sweet** → **NetSuite** (high confidence)
- **Trisha** → **Tricia** (medium confidence)

## 🎯 Decisions
### Not using inventory delta for integration
- **Category:** technical
- **Impact:** high
- **Context:** Missing class and business unit details

## ✅ Action Items
| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Process vendor bills | Team | 2025-11-15 | high |
```

---

## 🔄 Automation

### **Option 1: Cron Job**
```bash
# Add to crontab (every 15 min, Mon-Fri, 9am-6pm)
*/15 9-18 * * 1-5 cd /path/to/meeting_automation && python3 process_meetings.py
```

### **Option 2: Manual**
```bash
# Run after meetings
process-meetings
```

---

## 🐛 Troubleshooting

### **Gmail Authentication Error**
```bash
cd /path/to/8825-system/8825_core/integrations/google
rm token.json
python3 search_gmail.py "test"
# Re-authenticate
```

### **OpenAI API Error**
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API
python3 -c "from openai import OpenAI; OpenAI().models.list()"
```

### **No Meetings Found**
- Check if Otter.ai sent emails
- Check Gmail spam folder
- Verify search query: `from:otter.ai is:unread`

---

## 📚 Files

```
meeting_automation/
├── README.md                    # This file
├── gmail_otter_poller.py        # Gmail polling
├── meeting_processor.py         # GPT-4 processing
├── meeting_recall.py            # Query tool
├── process_meetings.py          # Main workflow
└── data/
    ├── raw/                     # Raw Gmail data
    └── processed/               # Processed meetings
```

---

## ✅ Trust Through Transparency

**You can review:**
1. Raw transcript (saved in data/raw/)
2. Corrections made (logged in JSON)
3. Confidence scores (high/medium/low)
4. Final structured data (editable JSON)

**If GPT-4 makes a mistake:**
1. See it in corrections_made
2. Edit the JSON manually
3. Re-process if needed
4. Update TGIF knowledge to improve future

---

**Ready to process your Nov 12-13 meetings? Run:**
```bash
python3 process_meetings.py
```
