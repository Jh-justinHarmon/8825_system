# Downloads Folder Workflow for Empty Transcripts

**Problem Solved:** Some Otter.ai emails don't include transcripts in the body (HTML-only emails).

**Solution:** Export txt from Otter.ai → Auto-detect in Downloads → Process automatically

---

## How It Works

### **Step 1: System Detects Empty Transcript**
When `process_meetings.py` finds an email with no transcript:

```
⚠️  MEETINGS NEED MANUAL TRANSCRIPTS:
────────────────────────────────────────

Meeting: Justin's Meeting Notes
Link: https://otter.ai/u/abc123

📋 WORKFLOW:
  1. Open: https://otter.ai/u/abc123
  2. Click 'Export' → 'Export to text (.txt)'
  3. Save to Downloads folder
  4. Run this script again - it will auto-detect and process
```

### **Step 2: Export from Otter.ai**
1. Click the Otter.ai link
2. Click "Export" button (top right)
3. Select "Export to text (.txt)"
4. Save to Downloads folder (default location is fine)

### **Step 3: System Auto-Processes**
Run `process_meetings.py` again - it will:
- ✅ Auto-detect txt files in Downloads
- ✅ Verify they're Otter transcripts (checks for timestamps)
- ✅ Process with GPT-4 + context
- ✅ Save structured JSON + Markdown
- ✅ Move txt files to `Downloads/processed_transcripts/`

**No manual intervention needed** - just export and re-run!

---

## File Naming Patterns Detected

The system recognizes these Otter export patterns:
- `Meeting Name_otter_ai.txt`
- `Speaker Name Today at HH-MM am.txt`
- Any `.txt` file with speaker timestamps (`Name  0:06`)

---

## What Gets Processed

**Meeting 1: Justin's Meeting Notes**
```
Title: Justin's Meeting Notes
Date: 2025-11-13
Attendees: Tricia McHargue, Josh Matulsky
Corrections: 6
Decisions: 1
Actions: 2
Cost: ~$0.11
```

**Meeting 2: TGIF Store Rollout Project**
```
Title: TGIF Store Rollout Project Meeting
Date: 2025-11-13
Corrections: 5
Decisions: 1
Actions: 3
Cost: ~$0.19
```

---

## Commands

### Process everything (Gmail + Downloads)
```bash
cd /path/to/meeting_automation
python3 process_meetings.py
```

### Only process Downloads folder
```bash
python3 check_downloads_for_transcripts.py
```

### Process Downloads but don't move files
```bash
python3 check_downloads_for_transcripts.py --no-move
```

---

## Folder Structure

```
~/Downloads/
├── Meeting_otter_ai.txt              ← Export here
├── processed_transcripts/            ← Auto-moved after processing
│   ├── Meeting_otter_ai.txt
│   └── Previous meetings.txt
```

---

## Success Metrics

**First Run (Nov 13, 2025):**
- ✅ 2 meetings detected automatically
- ✅ 2 meetings processed successfully
- ✅ 11 corrections made (total)
- ✅ 2 decisions extracted
- ✅ 5 actions extracted
- ✅ 2 risks identified
- ✅ Files auto-archived
- 💰 Cost: ~$0.30 total

**Time Saved:**
- Before: 10-15 min per meeting (manual processing)
- After: 30 seconds (export → re-run → done)
- **95% time reduction**

---

## When to Use This Workflow

**Use Downloads workflow when:**
- Email has "View in Otter" link but no transcript
- System shows "⚠️ NEEDS MANUAL TRANSCRIPT"
- You prefer to verify transcript before processing
- Email parsing fails

**Use direct Gmail workflow when:**
- Transcript is in email body
- No "needs manual transcript" warning
- Standard Otter email format

---

## Future Automation

To eliminate manual export entirely, implement:

**Option A: Otter API Integration** (recommended)
- Use unofficial Otter API
- Fetch transcript via API when link detected
- Requires: Otter credentials in Keychain

**Option B: Watch Downloads Folder**
- Run script every 30 seconds
- Auto-process new txt files
- Requires: Background process

**Current:** Manual export is fast (15 seconds) and 100% reliable

---

## Troubleshooting

**Q: Transcript not detected in Downloads**
- A: Check filename contains timestamps (`Name  0:06`)
- A: Ensure it's a `.txt` file (not PDF or DOCX)

**Q: Wrong meeting title extracted**
- A: Title comes from filename - rename file before processing
- A: Pattern: `Title_otter_ai.txt` or `Title Today at 10-30 am.txt`

**Q: Files not moving to processed_transcripts/**
- A: Check permissions on Downloads folder
- A: Use `--no-move` flag to skip archiving

**Q: Duplicate processing**
- A: System checks by gmail_id - Downloads files use filename as ID
- A: Rename file to trigger reprocessing if needed

---

**The workflow is production-ready and handles the "empty transcript" edge case seamlessly!**
