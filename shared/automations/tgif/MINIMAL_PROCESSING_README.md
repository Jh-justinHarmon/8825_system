# Minimal Meeting Processing

**Philosophy:** Stop trying to predict what you'll need. Keep raw data, answer when asked.

---

## What Changed (2025-11-13)

### Old Approach ❌
```
Meeting → Otter → Heavy OpenAI summarization → Structured JSON
                   ↓
                   Loses operational details
                   Costs money per meeting
                   User doesn't use the summaries
```

### New Approach ✅
```
Meeting → Otter → Extract minimal metadata → Store full transcript
                   ↓
                   - Date/time (for timesheets)
                   - Duration
                   - Attendees
                   - Title
                   
When user asks → Cascade reads full transcript → Accurate answer
```

---

## What Gets Extracted

**Metadata Only:**
- Date
- Time
- Duration (estimated from transcript length)
- Attendees (parsed from transcript)
- Meeting title

**What Gets Stored:**
- Full raw transcript (nothing lost)
- Minimal metadata JSON

**What Does NOT Happen:**
- ❌ No heavy OpenAI summarization
- ❌ No decisions extraction
- ❌ No action items extraction
- ❌ No risks/blockers extraction
- ❌ No upfront processing cost

---

## File Structure

```
8825_files/HCSS/meetings/
├── transcripts/
│   └── 20251113_tgif_weekly_sync.txt          # Full raw transcript
├── metadata/
│   └── 20251113_tgif_weekly_sync.json         # Minimal metadata
└── post_meeting_notes/
    └── 2025-11-13_status_update.md            # Your actual updates
```

---

## Usage

### Process a Meeting

```bash
# From Otter transcript file
python3 minimal_meeting_processor.py transcript.txt

# Output:
# - transcripts/YYYYMMDD_title.txt
# - metadata/YYYYMMDD_title.json
```

### Query a Meeting

**You don't run anything.** Just ask Cascade:

```
"What happened in the TGIF meeting on Nov 13?"
```

Cascade will:
1. Find the transcript
2. Read the full conversation
3. Answer accurately

### Generate Timesheet Entry

```python
from minimal_meeting_processor import MinimalMeetingProcessor

processor = MinimalMeetingProcessor()
timesheet = processor.generate_timesheet_entry('metadata/20251113_meeting.json')

# Returns:
# {
#   "date": "2025-11-13",
#   "duration_hours": 1.5,
#   "title": "TGIF Weekly Sync",
#   "project": "HCSS/TGIF",
#   "billable": true
# }
```

---

## Why This Works Better

### Problem with Old Approach
**Example from 2025-11-13:**
- Meeting discussed vendor setup
- User's actual update: "Hardware delivered, installer friction resolved, Hollywood support pending"
- AI summary captured: "Discussed vendor setup"
- **Result:** Wrong answer when asked "how are restaurants doing?"

### New Approach
- Full transcript preserved
- User asks question
- Cascade reads actual conversation
- Accurate answer

---

## Integration with Existing System

### What Stays
- ✅ Otter.ai integration
- ✅ Gmail automation
- ✅ Daily/weekly scheduling
- ✅ Post-meeting notes system

### What Changes
- ❌ Remove heavy OpenAI processing
- ✅ Add minimal metadata extraction
- ✅ Store full transcripts
- ✅ Cascade reads on demand

---

## Cost Comparison

### Old System (per meeting)
- OpenAI GPT-4 Turbo: ~$0.10-0.65 per meeting
- 6 meetings/week = ~$3.90/week = ~$200/year
- **Plus:** Lost details, wrong answers

### New System (per meeting)
- Metadata extraction: $0 (local processing)
- Storage: negligible
- Cascade reads when needed: included in your Cascade usage
- **Plus:** Nothing lost, accurate answers

---

## Timesheet Automation

**Still works.** Metadata includes:
```json
{
  "date": "2025-11-13",
  "duration_minutes": 90,
  "duration_hours": 1.5,
  "title": "TGIF Weekly Sync",
  "attendees": ["Justin Harmon", "BH", "Team"],
  "project": "HCSS/TGIF"
}
```

Can be imported directly into timesheet system.

---

## Migration Plan

### Phase 1: Parallel Run (1 week)
- Keep old system running
- Add new minimal processing
- Compare results

### Phase 2: Switch (after validation)
- Disable heavy summarization
- Use minimal processing only
- Monitor for issues

### Phase 3: Cleanup
- Archive old summaries
- Update documentation
- Train on new workflow

---

## When to Use Each Approach

### Minimal Processing (Default)
- Regular meetings
- Status updates
- Operational discussions
- **Use when:** You'll ask Cascade for info later

### Heavy Processing (Rare)
- Critical decision meetings
- Quarterly reviews
- Board meetings
- **Use when:** Need pre-structured data for reports

---

## Quick Start

1. **Meeting happens** → Otter transcribes
2. **Automation runs** → Extracts metadata, stores transcript
3. **You need info** → Ask Cascade
4. **Cascade reads** → Full transcript, accurate answer

**That's it.**

---

## Examples

### Question: "How are the TGIF restaurants doing?"

**Cascade's process:**
1. Check `post_meeting_notes/` for latest status
2. Check `transcripts/` for recent meetings
3. Read full conversations
4. Answer: "Restaurants doing fine. Hardware delivered, minor installer friction resolved, Hollywood support being scheduled."

**Not:** "Discussed vendor setup" (from old AI summary)

### Question: "What were the action items from yesterday's meeting?"

**Cascade's process:**
1. Find yesterday's transcript
2. Read full conversation
3. Extract action items on demand
4. Return accurate list

---

## Philosophy

**Old way:** "Let me predict what you'll need and pre-process everything"
- Result: Loses details, costs money, wrong answers

**New way:** "Keep everything, I'll read it when you ask"
- Result: Nothing lost, accurate answers, lower cost

**Lesson:** Raw data + smart AI on demand > Pre-processed summaries

---

**Created:** 2025-11-13  
**Reason:** AI summaries missing critical details  
**Decision:** Stop pre-processing, preserve raw data, answer on demand
