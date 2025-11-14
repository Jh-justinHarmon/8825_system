# TGIF Meeting Automation Pipeline

**Status:** Production Ready (Tested pre-v3.0)  
**Priority:** NOW (Quick Win)  
**Effort:** 2-3 hours (configuration)  
**Value:** High (client-facing governance)

---

## 🎯 OBJECTIVE

Transform ad-hoc TGIF meeting capture into a **repeatable, automated weekly workflow** that:
1. Captures all TGIF meetings automatically
2. Extracts decisions, actions, and risks
3. Generates standardized summaries
4. Produces weekly rollup digest (Friday 3pm)
5. Tracks governance and rollout progress

---

## 📊 CURRENT STATE

### **What Works (Tested):**
- ✅ Chat Mining Agent deployed for TGIF
- ✅ Meeting transcription functional
- ✅ Decision capture tested
- ✅ Action item extraction working

### **What's Missing:**
- ❌ Ad-hoc process (not scheduled)
- ❌ No weekly rollup automation
- ❌ Inconsistent template usage
- ❌ Manual trigger required
- ❌ No governance tracking integration

---

## 🏗️ ARCHITECTURE

### **Pipeline Flow:**

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: MEETING DETECTION                              │
│  ─────────────────────────────                          │
│  • Google Calendar: Query TGIF meetings (Mon-Fri)       │
│  • Filter: Project tag = "TGIF"                         │
│  • Detect: New meetings, transcripts, notes             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: CONTENT INGESTION                              │
│  ──────────────────────                                 │
│  • Transcript: Zoom/Teams/Google Meet auto-transcript   │
│  • Notes: Shared doc, email thread, Slack messages      │
│  • Context: Calendar event details, attendees           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: CHAT MINING AGENT                              │
│  ──────────────────────                                 │
│  • Extract: Decisions, actions, risks, blockers         │
│  • Tag: Owner, due date, priority, category             │
│  • Confidence: Score each extraction (0.0-1.0)          │
│  • Dedupe: Avoid duplicate action items                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: STRUCTURED OUTPUT                              │
│  ──────────────────────                                 │
│  • JSON: Normalized meeting summary                     │
│  • Markdown: Human-readable summary                     │
│  • Tags: TGIF project, rollout phase, location          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 5: WEEKLY ROLLUP (Friday 3pm)                     │
│  ────────────────────────────────                       │
│  • Aggregate: All week's meetings                       │
│  • Group: By category (rollout, pricing, operations)    │
│  • Highlight: Red flags, overdue actions                │
│  • Format: Email digest + Notion page                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 6: GOVERNANCE TRACKING                            │
│  ────────────────────────                               │
│  • Update: Rollout governance tracker                   │
│  • Track: Milestones, blockers, decisions               │
│  • Alert: Stakeholders on critical items                │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 DATA SCHEMA

### **Meeting Summary JSON:**

```json
{
  "type": "tgif_meeting_summary",
  "meeting_id": "gcal:abc123",
  "date": "2025-11-09",
  "time": "10:00-11:00 CST",
  "attendees": [
    {"name": "Justin Harmon", "role": "HCSS Lead"},
    {"name": "BH", "role": "Operations"},
    {"name": "Team Member", "role": "Store Manager"}
  ],
  
  "decisions": [
    {
      "id": "DEC-001",
      "text": "Delay Dallas rollout by 5 days due to training gaps",
      "category": "rollout_timing",
      "impact": "high",
      "confidence": 0.92
    }
  ],
  
  "actions": [
    {
      "id": "ACT-001",
      "what": "Complete Toast training for MA stores",
      "who": "BH",
      "due": "2025-11-15",
      "priority": "high",
      "status": "todo",
      "confidence": 0.88
    }
  ],
  
  "risks": [
    {
      "id": "RISK-001",
      "text": "Liquor vendor setup incomplete for new location",
      "severity": "medium",
      "mitigation": "Expedite vendor onboarding",
      "owner": "Operations",
      "confidence": 0.85
    }
  ],
  
  "blockers": [
    {
      "id": "BLOCK-001",
      "text": "NetSuite inventory accounts not configured",
      "impact": "Blocks store opening",
      "resolution_needed_by": "2025-11-12",
      "owner": "IT Team"
    }
  ],
  
  "next_meeting": {
    "date": "2025-11-16",
    "agenda": ["Review Dallas prep", "Pricing system test results"]
  },
  
  "metadata": {
    "processed_at": "2025-11-09T16:30:00Z",
    "agent_version": "chat_mining_v1.2",
    "source": "zoom_transcript",
    "confidence_avg": 0.88
  }
}
```

---

## 📅 WEEKLY ROLLUP SCHEMA

### **Friday 3pm Digest:**

```json
{
  "type": "tgif_weekly_rollup",
  "week_start": "2025-11-04",
  "week_end": "2025-11-08",
  "meetings_count": 4,
  
  "summary": {
    "decisions": 12,
    "actions": 23,
    "risks": 5,
    "blockers": 2
  },
  
  "by_category": {
    "rollout_governance": {
      "decisions": 5,
      "actions": 8,
      "key_updates": [
        "Dallas rollout delayed +5 days",
        "MA stores training on track"
      ]
    },
    "pricing_management": {
      "decisions": 3,
      "actions": 6,
      "key_updates": [
        "Happy hour pricing tested in lab",
        "Price levels spreadsheet approved"
      ]
    },
    "store_setup": {
      "decisions": 4,
      "actions": 9,
      "key_updates": [
        "Inventory accounts configured for 3 locations",
        "Vendor setup in progress"
      ]
    }
  },
  
  "red_flags": [
    {
      "type": "overdue_action",
      "item": "ACT-015: Complete vendor setup",
      "owner": "Operations",
      "due": "2025-11-06",
      "days_overdue": 2
    },
    {
      "type": "blocker",
      "item": "BLOCK-001: NetSuite accounts not configured",
      "impact": "Blocks store opening",
      "urgency": "critical"
    }
  ],
  
  "next_week_focus": [
    "Complete Dallas prep checklist",
    "Test pricing system in live environment",
    "Finalize vendor onboarding"
  ]
}
```

---

## 🔧 IMPLEMENTATION

### **Phase 1: Automated Detection (Week 1)**

**Goal:** Automatically detect and ingest TGIF meetings

**Steps:**
1. **Calendar Integration:**
   ```python
   # Query Google Calendar for TGIF meetings
   def detect_tgif_meetings(start_date, end_date):
       events = calendar.query(
           calendar_id="primary",
           q="TGIF",
           timeMin=start_date,
           timeMax=end_date
       )
       return [e for e in events if "TGIF" in e.summary]
   ```

2. **Transcript Detection:**
   ```python
   # Check for Zoom/Teams transcripts
   def get_meeting_transcript(meeting_id):
       # Check Zoom API
       zoom_transcript = zoom.get_transcript(meeting_id)
       if zoom_transcript:
           return zoom_transcript
       
       # Check Teams API
       teams_transcript = teams.get_transcript(meeting_id)
       if teams_transcript:
           return teams_transcript
       
       # Fallback: Check Dropbox for uploaded transcript
       return dropbox.search(f"TGIF_{meeting_id}_transcript")
   ```

3. **Notes Detection:**
   ```python
   # Check for meeting notes in common locations
   def get_meeting_notes(meeting_id, date):
       sources = [
           f"TGIF Meeting Notes {date}",  # Google Doc
           f"tgif-{date}",                 # Slack channel
           f"TGIF_{date}_notes.txt"        # Dropbox
       ]
       return search_all_sources(sources)
   ```

---

### **Phase 2: Chat Mining Integration (Week 1)**

**Goal:** Extract structured data from meeting content

**Configuration:**
```yaml
chat_mining_agent:
  project: TGIF
  extraction_rules:
    decisions:
      keywords: ["decided", "agreed", "approved", "go with"]
      confidence_threshold: 0.8
      
    actions:
      keywords: ["will", "need to", "should", "must", "by [date]"]
      extract_fields: [who, what, due_date, priority]
      confidence_threshold: 0.85
      
    risks:
      keywords: ["risk", "concern", "worry", "might", "could fail"]
      severity_levels: [low, medium, high, critical]
      confidence_threshold: 0.8
      
    blockers:
      keywords: ["blocked", "can't proceed", "waiting on", "dependency"]
      urgency: true
      confidence_threshold: 0.9
```

**Execution:**
```python
def process_meeting(meeting_id, transcript, notes):
    # Combine sources
    content = f"{transcript}\n\n{notes}"
    
    # Run Chat Mining Agent
    result = chat_mining_agent.extract(
        content=content,
        project="TGIF",
        context={
            "meeting_id": meeting_id,
            "attendees": get_attendees(meeting_id),
            "date": get_meeting_date(meeting_id)
        }
    )
    
    # Validate and dedupe
    result = validate_extractions(result)
    result = dedupe_actions(result)
    
    return result
```

---

### **Phase 3: Weekly Rollup Automation (Week 2)**

**Goal:** Generate Friday 3pm digest automatically

**Schedule:**
```yaml
schedule:
  trigger: cron
  expression: "0 15 * * 5"  # Every Friday at 3pm
  timezone: "America/Chicago"
```

**Rollup Logic:**
```python
def generate_weekly_rollup():
    # Get week's date range
    week_start = get_monday_of_current_week()
    week_end = get_friday_of_current_week()
    
    # Fetch all TGIF meetings this week
    meetings = get_tgif_meetings(week_start, week_end)
    
    # Aggregate data
    rollup = {
        "meetings_count": len(meetings),
        "decisions": [],
        "actions": [],
        "risks": [],
        "blockers": []
    }
    
    for meeting in meetings:
        summary = get_meeting_summary(meeting.id)
        rollup["decisions"].extend(summary.decisions)
        rollup["actions"].extend(summary.actions)
        rollup["risks"].extend(summary.risks)
        rollup["blockers"].extend(summary.blockers)
    
    # Group by category
    rollup["by_category"] = group_by_category(rollup)
    
    # Identify red flags
    rollup["red_flags"] = identify_red_flags(rollup)
    
    # Generate next week focus
    rollup["next_week_focus"] = generate_focus_areas(rollup)
    
    return rollup
```

**Output Generation:**
```python
def send_weekly_digest(rollup):
    # Generate Markdown
    markdown = format_as_markdown(rollup)
    
    # Generate HTML email
    html = format_as_html(rollup)
    
    # Send email
    send_email(
        to=["justin@hcss.com", "team@tgif.com"],
        subject=f"TGIF Weekly Digest - {rollup.week_end}",
        body=html,
        attachments=[
            {"filename": "rollup.json", "content": json.dumps(rollup)},
            {"filename": "rollup.md", "content": markdown}
        ]
    )
    
    # Post to Notion
    notion.create_page(
        database_id="tgif_weekly_rollups",
        properties={
            "Week": rollup.week_end,
            "Meetings": rollup.meetings_count,
            "Decisions": len(rollup.decisions),
            "Actions": len(rollup.actions)
        },
        content=markdown
    )
```

---

### **Phase 4: Governance Integration (Week 2-3)**

**Goal:** Update rollout governance tracker automatically

**Integration Points:**
```python
def update_governance_tracker(meeting_summary):
    # Extract rollout-related items
    rollout_items = filter_by_category(
        meeting_summary,
        category="rollout_governance"
    )
    
    # Update tracker
    for decision in rollout_items.decisions:
        governance_tracker.add_decision(
            location=extract_location(decision),
            decision=decision.text,
            date=meeting_summary.date,
            impact=decision.impact
        )
    
    for action in rollout_items.actions:
        governance_tracker.add_action(
            location=extract_location(action),
            action=action.what,
            owner=action.who,
            due=action.due,
            status=action.status
        )
    
    for blocker in rollout_items.blockers:
        governance_tracker.add_blocker(
            location=extract_location(blocker),
            blocker=blocker.text,
            impact=blocker.impact,
            resolution_needed_by=blocker.resolution_needed_by
        )
```

---

## 📊 TEMPLATE

### **Standard Meeting Summary (Markdown):**

```markdown
# TGIF Meeting Summary - [Date]

**Time:** [Start] - [End] CST  
**Attendees:** [List]  
**Next Meeting:** [Date]

---

## 🎯 Decisions

1. **[Decision Text]**
   - Category: [rollout/pricing/operations]
   - Impact: [high/medium/low]
   - Confidence: [0.0-1.0]

---

## ✅ Action Items

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| ACT-001 | [Action text] | [Name] | [Date] | High | Todo |

---

## ⚠️ Risks

1. **[Risk Text]**
   - Severity: [critical/high/medium/low]
   - Mitigation: [Plan]
   - Owner: [Name]

---

## 🚫 Blockers

1. **[Blocker Text]**
   - Impact: [Description]
   - Resolution Needed By: [Date]
   - Owner: [Name]

---

## 📅 Next Meeting Agenda

- [ ] [Agenda item 1]
- [ ] [Agenda item 2]
```

---

## 🔍 QUALITY CONTROLS

### **Validation Rules:**

1. **Action Items:**
   - Must have: who, what, due date
   - Owner must be valid attendee
   - Due date must be future date
   - Priority must be [high/medium/low]

2. **Decisions:**
   - Must have clear decision statement
   - Category must be valid
   - Impact must be assessed

3. **Confidence Thresholds:**
   - Decisions: ≥0.8
   - Actions: ≥0.85
   - Risks: ≥0.8
   - Blockers: ≥0.9

4. **Deduplication:**
   - Check for similar action items across meetings
   - Flag if same action appears multiple times
   - Merge duplicates with highest confidence

---

## 📈 SUCCESS METRICS

### **Automation Metrics:**
- **Meeting Detection Rate:** ≥95% (auto-detect all TGIF meetings)
- **Extraction Accuracy:** ≥85% (validated against manual review)
- **Weekly Rollup Delivery:** 100% on-time (Friday 3pm)
- **False Positive Rate:** <10% (incorrect extractions)

### **Business Metrics:**
- **Action Item Completion:** Track % completed by due date
- **Red Flag Response Time:** Time from detection to resolution
- **Governance Coverage:** % of rollout decisions tracked
- **Stakeholder Satisfaction:** Weekly digest usefulness rating

---

## 🚀 ROLLOUT PLAN

### **Week 1: Core Pipeline**
- [ ] Configure calendar detection
- [ ] Set up transcript ingestion
- [ ] Test Chat Mining Agent
- [ ] Validate JSON output

### **Week 2: Weekly Automation**
- [ ] Configure Friday 3pm schedule
- [ ] Build rollup aggregation
- [ ] Create email template
- [ ] Test Notion integration

### **Week 3: Governance Integration**
- [ ] Connect to governance tracker
- [ ] Set up red flag alerts
- [ ] Configure stakeholder notifications
- [ ] Full end-to-end test

### **Week 4: Production Launch**
- [ ] Monitor first automated week
- [ ] Gather stakeholder feedback
- [ ] Tune confidence thresholds
- [ ] Document lessons learned

---

## 🔧 MAINTENANCE

### **Weekly:**
- Review extraction accuracy
- Check for missed meetings
- Validate action item tracking

### **Monthly:**
- Tune confidence thresholds
- Update extraction rules
- Review governance integration
- Stakeholder feedback session

### **Quarterly:**
- Full pipeline audit
- Update templates
- Optimize performance
- Document improvements

---

## 📚 REFERENCES

- **TGIF Project:** `8825_core/projects/8825_HCSS-TGIF.json`
- **Chat Mining Agent:** `8825_core/agents/chat_mining_agent.json`
- **Governance Tracker:** `focuses/hcss/governance/rollout_tracker.md`
- **Calendar Integration:** `8825_core/integrations/google/calendar.py`

---

**Pipeline ready for implementation. Tested components + new automation = production workflow.** ✅
