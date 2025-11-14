# TGIF Output & Rollup Architecture

**Your Requirements:**
1. **Standalone summary** for every meeting
2. **Weekly rollup** includes meetings + flagged Outlook emails
3. **Current state:** Outlook → Gmail forwarding (manual flag)
4. **Future state:** Microsoft integration (not available yet)

---

## 🏗️ UPDATED ARCHITECTURE

### **Step 4: Structured Output (Per Meeting)**

```
┌─────────────────────────────────────────────────────────┐
│  INDIVIDUAL MEETING OUTPUT                              │
│  ─────────────────────────                              │
│  Every meeting gets its own standalone summary          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  OUTPUT FORMATS (3 versions)                            │
│  ────────────────────────                               │
│  1. JSON (machine-readable)                             │
│     → For governance tracker, automation                │
│                                                          │
│  2. Markdown (human-readable)                           │
│     → For review, sharing, archiving                    │
│                                                          │
│  3. Email (formatted)                                   │
│     → Sent to stakeholders immediately                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STORAGE LOCATIONS                                      │
│  ─────────────────                                      │
│  • JSON: focuses/hcss/knowledge/meetings/json/          │
│  • Markdown: focuses/hcss/knowledge/meetings/summaries/ │
│  • Notion: TGIF Meetings database                       │
└─────────────────────────────────────────────────────────┘
```

**File Naming:**
```
TGIF_Meeting_2025-11-09_10am.json
TGIF_Meeting_2025-11-09_10am.md
```

---

### **Step 5A: Daily Email Processing (12pm)**

```
┌─────────────────────────────────────────────────────────┐
│  DAILY EMAIL REVIEW (Every day at 12pm)                 │
│  ───────────────────────────────────                    │
│  1. Detect new flagged emails (last 24 hours)           │
│  2. Process with Chat Mining Agent                      │
│  3. Update task tracking                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  EMAIL INGESTION (Current State)                        │
│  ────────────────────────                               │
│  • You forward important Outlook emails to Gmail        │
│  • Subject: "TGIF: [topic]" or label "TGIF"            │
│  • Gmail API detects these flagged emails               │
│  • Chat Mining Agent extracts key points               │
│  • Runs daily at 12pm (not just Friday)                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  TASK TRACKING UPDATE                                   │
│  ─────────────────────                                  │
│  • Add new action items from emails                     │
│  • Update status of existing actions                    │
│  • Flag overdue items                                   │
│  • Calculate daily metrics                              │
└─────────────────────────────────────────────────────────┘

### **Step 5B: Weekly Rollup (Friday 3pm)**

```
┌─────────────────────────────────────────────────────────┐
│  WEEKLY ROLLUP INPUTS (Friday 3pm)                      │
│  ──────────────────────────────                         │
│  1. All TGIF meeting summaries (Mon-Fri)                │
│  2. All email extracts (processed daily at 12pm)        │
│  3. Task tracking data (updated daily)                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  AGGREGATION ENGINE                                     │
│  ──────────────────                                     │
│  • Combine: Meeting summaries + Email extractions       │
│  • Group by: Category (rollout, pricing, operations)    │
│  • Identify: Red flags, blockers, overdue items         │
│  • Track: Action items across all sources               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  WEEKLY DIGEST OUTPUT                                   │
│  ─────────────────────                                  │
│  • Executive Summary (high-level)                       │
│  • Meeting Summaries (individual links)                 │
│  • Email Highlights (key points from flagged emails)    │
│  • Action Items (all sources, grouped by owner)         │
│  • Red Flags (blockers, risks, overdue)                 │
│  • Next Week Focus                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 DATA SCHEMAS

### **Individual Meeting Summary (JSON):**

```json
{
  "type": "tgif_meeting_summary",
  "meeting_id": "gcal:abc123",
  "date": "2025-11-09",
  "time": "10:00-11:00 CST",
  "title": "TGIF Weekly Sync",
  "attendees": [
    {"name": "Justin Harmon", "role": "HCSS Lead"},
    {"name": "BH", "role": "Operations"}
  ],
  
  "decisions": [
    {
      "id": "DEC-2025-11-09-001",
      "text": "Delay Dallas rollout by 5 days",
      "category": "rollout_timing",
      "impact": "high",
      "confidence": 0.92
    }
  ],
  
  "actions": [
    {
      "id": "ACT-2025-11-09-001",
      "what": "Complete Toast training for MA stores",
      "who": "BH",
      "due": "2025-11-15",
      "priority": "high",
      "status": "todo",
      "source": "meeting",
      "confidence": 0.88
    }
  ],
  
  "risks": [
    {
      "id": "RISK-2025-11-09-001",
      "text": "Liquor vendor setup incomplete",
      "severity": "medium",
      "mitigation": "Expedite vendor onboarding",
      "owner": "Operations"
    }
  ],
  
  "blockers": [
    {
      "id": "BLOCK-2025-11-09-001",
      "text": "NetSuite inventory accounts not configured",
      "impact": "Blocks store opening",
      "resolution_needed_by": "2025-11-12"
    }
  ],
  
  "metadata": {
    "processed_at": "2025-11-09T11:30:00Z",
    "source": "otter_transcript",
    "agent_version": "chat_mining_v1.2",
    "confidence_avg": 0.88
  }
}
```

---

### **Flagged Email (JSON):**

```json
{
  "type": "tgif_email_extract",
  "email_id": "gmail:xyz789",
  "date": "2025-11-08",
  "from": "vendor@sysco.com",
  "subject": "TGIF: Pricing update for Dallas location",
  "forwarded_by": "justin@hcss.com",
  "flagged_at": "2025-11-08T14:30:00Z",
  
  "key_points": [
    {
      "text": "New pricing structure effective Nov 15",
      "category": "pricing_management",
      "importance": "high"
    },
    {
      "text": "Requires menu updates in Toast",
      "category": "store_setup",
      "importance": "medium"
    }
  ],
  
  "actions": [
    {
      "id": "ACT-2025-11-08-EMAIL-001",
      "what": "Update Toast menu with new pricing",
      "who": "TBD",
      "due": "2025-11-14",
      "priority": "high",
      "status": "todo",
      "source": "email"
    }
  ],
  
  "metadata": {
    "processed_at": "2025-11-08T15:00:00Z",
    "source": "gmail_forward",
    "agent_version": "chat_mining_v1.2"
  }
}
```

---

### **Weekly Rollup (JSON):**

```json
{
  "type": "tgif_weekly_rollup",
  "week_start": "2025-11-04",
  "week_end": "2025-11-08",
  "generated_at": "2025-11-08T15:00:00Z",
  
  "summary": {
    "meetings_count": 4,
    "emails_count": 7,
    "total_decisions": 12,
    "total_actions": 23,
    "total_risks": 5,
    "total_blockers": 2
  },
  
  "sources": {
    "meetings": [
      {
        "date": "2025-11-04",
        "title": "TGIF Weekly Sync",
        "summary_link": "focuses/hcss/knowledge/meetings/summaries/TGIF_Meeting_2025-11-04_10am.md"
      },
      {
        "date": "2025-11-06",
        "title": "TGIF Dallas Prep",
        "summary_link": "focuses/hcss/knowledge/meetings/summaries/TGIF_Meeting_2025-11-06_2pm.md"
      }
    ],
    "emails": [
      {
        "date": "2025-11-05",
        "from": "vendor@sysco.com",
        "subject": "TGIF: Pricing update",
        "key_points": ["New pricing structure", "Menu updates needed"]
      },
      {
        "date": "2025-11-07",
        "from": "ops@tgif.com",
        "subject": "TGIF: Training completion",
        "key_points": ["MA stores training complete", "Dallas delayed"]
      }
    ]
  },
  
  "by_category": {
    "rollout_governance": {
      "decisions": 5,
      "actions": 8,
      "key_updates": [
        "Dallas rollout delayed +5 days (Meeting 11/4)",
        "MA stores training complete (Email 11/7)"
      ]
    },
    "pricing_management": {
      "decisions": 3,
      "actions": 6,
      "key_updates": [
        "New pricing structure approved (Email 11/5)",
        "Happy hour pricing tested (Meeting 11/6)"
      ]
    }
  },
  
  "action_items_by_owner": {
    "BH": [
      {
        "id": "ACT-2025-11-04-001",
        "what": "Complete Toast training",
        "due": "2025-11-15",
        "status": "in_progress",
        "source": "meeting_2025-11-04"
      }
    ],
    "TBD": [
      {
        "id": "ACT-2025-11-08-EMAIL-001",
        "what": "Update Toast menu pricing",
        "due": "2025-11-14",
        "status": "todo",
        "source": "email_2025-11-08"
      }
    ]
  },
  
  "red_flags": [
    {
      "type": "blocker",
      "item": "NetSuite accounts not configured",
      "impact": "Blocks store opening",
      "urgency": "critical",
      "source": "meeting_2025-11-09"
    },
    {
      "type": "overdue_action",
      "item": "ACT-2025-11-01-005: Vendor setup",
      "owner": "Operations",
      "due": "2025-11-06",
      "days_overdue": 2,
      "source": "meeting_2025-11-01"
    }
  ],
  
  "next_week_focus": [
    "Complete Dallas prep checklist",
    "Resolve NetSuite blocker",
    "Update Toast menu pricing"
  ]
}
```

---

## 🔧 IMPLEMENTATION

### **Step 4: Individual Meeting Output**

```python
# process_meeting.py

def process_meeting(meeting_id, transcript):
    # Extract structured data
    summary = chat_mining_agent.process(transcript)
    
    # Generate outputs
    outputs = generate_outputs(summary)
    
    # Save all formats
    save_json(outputs['json'])
    save_markdown(outputs['markdown'])
    send_email(outputs['email'])
    post_to_notion(outputs['notion'])
    
    return summary

def generate_outputs(summary):
    date = summary['date']
    time = summary['time'].replace(':', '')
    
    return {
        'json': {
            'path': f'focuses/hcss/knowledge/meetings/json/TGIF_Meeting_{date}_{time}.json',
            'content': json.dumps(summary, indent=2)
        },
        'markdown': {
            'path': f'focuses/hcss/knowledge/meetings/summaries/TGIF_Meeting_{date}_{time}.md',
            'content': format_as_markdown(summary)
        },
        'email': {
            'to': ['justin@hcss.com', 'team@tgif.com'],
            'subject': f'TGIF Meeting Summary - {date}',
            'body': format_as_email(summary)
        },
        'notion': {
            'database': 'tgif_meetings',
            'properties': extract_notion_properties(summary)
        }
    }
```

---

### **Step 5: Weekly Rollup (Meetings + Emails)**

```python
# weekly_rollup.py

def generate_weekly_rollup():
    # Get date range
    week_start = get_monday_of_current_week()
    week_end = get_friday_of_current_week()
    
    # Collect all sources
    meetings = get_meeting_summaries(week_start, week_end)
    emails = get_flagged_emails(week_start, week_end)
    
    # Process emails
    email_extracts = []
    for email in emails:
        extract = process_flagged_email(email)
        email_extracts.append(extract)
    
    # Aggregate everything
    rollup = aggregate_sources(meetings, email_extracts)
    
    # Generate outputs
    save_rollup(rollup)
    send_digest(rollup)
    
    return rollup

def get_flagged_emails(start_date, end_date):
    """Get emails forwarded from Outlook to Gmail"""
    
    # Search Gmail for forwarded TGIF emails
    query = f'''
        from:justin@hcss.com 
        subject:TGIF 
        after:{start_date} 
        before:{end_date}
    '''
    
    emails = gmail.search(query)
    
    # Also check for labeled emails
    labeled = gmail.search(f'label:TGIF after:{start_date}')
    
    return emails + labeled

def process_flagged_email(email):
    """Extract key points from flagged email"""
    
    # Get email content
    content = gmail.get_message(email.id)
    
    # Extract with Chat Mining Agent
    extract = chat_mining_agent.process(
        content,
        context={
            'type': 'email',
            'from': email.from_address,
            'subject': email.subject,
            'date': email.date
        }
    )
    
    return {
        'type': 'tgif_email_extract',
        'email_id': email.id,
        'date': email.date,
        'from': email.from_address,
        'subject': email.subject,
        'key_points': extract.key_points,
        'actions': extract.actions,
        'metadata': {
            'processed_at': now(),
            'source': 'gmail_forward'
        }
    }

def aggregate_sources(meetings, emails):
    """Combine meetings and emails into rollup"""
    
    rollup = {
        'meetings_count': len(meetings),
        'emails_count': len(emails),
        'sources': {
            'meetings': [],
            'emails': []
        },
        'by_category': {},
        'action_items_by_owner': {},
        'red_flags': []
    }
    
    # Add meeting summaries
    for meeting in meetings:
        rollup['sources']['meetings'].append({
            'date': meeting['date'],
            'title': meeting['title'],
            'summary_link': meeting['file_path']
        })
        
        # Aggregate decisions, actions, etc.
        aggregate_meeting_data(rollup, meeting)
    
    # Add email highlights
    for email in emails:
        rollup['sources']['emails'].append({
            'date': email['date'],
            'from': email['from'],
            'subject': email['subject'],
            'key_points': [kp['text'] for kp in email['key_points']]
        })
        
        # Aggregate email actions
        aggregate_email_data(rollup, email)
    
    # Group by category
    rollup['by_category'] = group_by_category(rollup)
    
    # Group actions by owner
    rollup['action_items_by_owner'] = group_by_owner(rollup)
    
    # Identify red flags
    rollup['red_flags'] = identify_red_flags(rollup)
    
    return rollup
```

---

## 📅 WORKFLOW

### **Real-Time (After Each Meeting):**

```
1. Otter.ai transcribes meeting
2. MCP detects new transcript
3. Chat Mining Agent processes
4. Generate 3 outputs:
   ├─ JSON (saved to knowledge base)
   ├─ Markdown (saved to summaries)
   └─ Email (sent to stakeholders)
5. Post to Notion
```

### **Daily 12pm (Email Review & Task Update):**

```
1. Detect new flagged emails (since yesterday 12pm)
   ├─ Search: from:justin@hcss.com subject:TGIF
   └─ Search: label:TGIF
2. Process each email with Chat Mining Agent
   ├─ Extract key points
   ├─ Extract action items
   └─ Identify risks/blockers
3. Update task tracking
   ├─ Add new actions to tracker
   ├─ Update existing action status
   └─ Flag overdue items
4. Generate daily update (optional)
   ├─ New emails processed: X
   ├─ New actions identified: Y
   └─ Red flags: Z
5. Save email extracts to knowledge base
```

### **Friday 3pm (Weekly Rollup):**

```
1. Collect all meeting summaries (Mon-Fri)
2. Collect all email extracts (Mon-Fri)
   └─ Already processed daily at 12pm
3. Aggregate meetings + emails
4. Group by category
5. Consolidate action items by owner
6. Identify red flags
7. Generate weekly digest
8. Send to stakeholders
9. Post to Notion
```

---

## 📊 WEEKLY DIGEST TEMPLATE (Markdown)

```markdown
# TGIF Weekly Digest - Week of Nov 4-8, 2025

**Generated:** Friday, Nov 8, 2025 at 3:00 PM CST

---

## 📊 Executive Summary

- **Meetings:** 4 this week
- **Emails:** 7 flagged items
- **Decisions:** 12 total
- **Action Items:** 23 total (5 overdue)
- **Red Flags:** 2 critical blockers

---

## 🎯 Key Updates by Category

### Rollout Governance
- ✅ MA stores training complete (Email 11/7)
- ⚠️ Dallas rollout delayed +5 days due to training gaps (Meeting 11/4)
- 🚫 NetSuite accounts not configured - **BLOCKER** (Meeting 11/9)

### Pricing Management
- ✅ New pricing structure approved (Email 11/5)
- ✅ Happy hour pricing tested in lab (Meeting 11/6)
- ⏳ Toast menu updates needed by Nov 14 (Email 11/8)

### Store Setup
- ✅ Inventory accounts configured for 3 locations (Meeting 11/5)
- ⏳ Vendor setup in progress (Meeting 11/6)
- ⚠️ Liquor vendor incomplete for new location (Meeting 11/9)

---

## 📋 Meeting Summaries

### Monday, Nov 4 - TGIF Weekly Sync
[Full Summary](focuses/hcss/knowledge/meetings/summaries/TGIF_Meeting_2025-11-04_10am.md)

**Key Points:**
- Decided to delay Dallas rollout by 5 days
- BH to complete Toast training by Nov 15
- Discussed pricing system testing

### Wednesday, Nov 6 - TGIF Dallas Prep
[Full Summary](focuses/hcss/knowledge/meetings/summaries/TGIF_Meeting_2025-11-06_2pm.md)

**Key Points:**
- Happy hour pricing tested successfully
- Vendor setup progress reviewed
- Inventory accounts configured

---

## 📧 Email Highlights

### Tuesday, Nov 5 - Sysco Pricing Update
**From:** vendor@sysco.com  
**Key Points:**
- New pricing structure effective Nov 15
- Requires menu updates in Toast
- Action: Update Toast menu by Nov 14

### Thursday, Nov 7 - Training Completion
**From:** ops@tgif.com  
**Key Points:**
- MA stores training complete
- Dallas training delayed
- All staff certified on new POS

---

## ✅ Action Items by Owner

### BH (3 items)
- [ ] **HIGH:** Complete Toast training for MA stores - Due Nov 15 *(Meeting 11/4)*
- [ ] **MEDIUM:** Review vendor setup progress - Due Nov 12 *(Meeting 11/6)*
- [ ] **LOW:** Schedule follow-up with operations - Due Nov 13 *(Email 11/7)*

### Operations (2 items)
- [ ] **CRITICAL:** Configure NetSuite inventory accounts - Due Nov 12 *(Meeting 11/9)*
- [ ] **HIGH:** Complete vendor onboarding - Due Nov 10 *(Meeting 11/6)* **OVERDUE 2 days**

### TBD (1 item)
- [ ] **HIGH:** Update Toast menu with new pricing - Due Nov 14 *(Email 11/8)*

---

## 🚨 Red Flags

### 🔴 CRITICAL
1. **NetSuite accounts not configured**
   - Impact: Blocks store opening
   - Resolution needed by: Nov 12
   - Source: Meeting 11/9

### 🟡 OVERDUE
2. **Vendor setup incomplete**
   - Owner: Operations
   - Due: Nov 6
   - Days overdue: 2
   - Source: Meeting 11/6

---

## 🎯 Next Week Focus

1. **Resolve NetSuite blocker** (critical for store opening)
2. **Complete Dallas prep checklist** (rollout delayed to Nov 14)
3. **Update Toast menu pricing** (new structure effective Nov 15)
4. **Follow up on overdue vendor setup**

---

## 📎 Attachments

- [All Meeting Summaries (JSON)](focuses/hcss/knowledge/meetings/json/)
- [All Meeting Summaries (Markdown)](focuses/hcss/knowledge/meetings/summaries/)
- [Weekly Rollup (JSON)](focuses/hcss/knowledge/rollups/TGIF_Rollup_2025-11-08.json)

---

**Next Digest:** Friday, Nov 15, 2025 at 3:00 PM CST
```

---

## 🚀 IMPLEMENTATION TIMELINE

### **Week 1: Individual Meeting Output**
- Day 1-2: Build meeting processing pipeline
- Day 3: Generate JSON + Markdown outputs
- Day 4: Add email notification
- Day 5: Test with recent meeting

### **Week 2: Email Integration**
- Day 1-2: Build Gmail flagged email detection
- Day 3: Process emails with Chat Mining Agent
- Day 4: Test email extraction
- Day 5: Validate output quality

### **Week 3: Weekly Rollup**
- Day 1-2: Build aggregation engine
- Day 3: Combine meetings + emails
- Day 4: Generate weekly digest
- Day 5: Test full end-to-end

### **Week 4: Production**
- Day 1: Deploy all components
- Day 2-5: Monitor first week
- Tune and adjust

---

## 🎓 KEY INSIGHTS

### **Why Separate Individual + Rollup?**

**Individual Summaries:**
- ✅ Immediate feedback (sent right after meeting)
- ✅ Detailed context preserved
- ✅ Stakeholders can review specific meetings
- ✅ Searchable archive

**Weekly Rollup:**
- ✅ High-level overview (executive summary)
- ✅ Cross-meeting patterns visible
- ✅ Action items consolidated
- ✅ Red flags surfaced

**Together:**
- Individual = Detail
- Rollup = Big picture
- Both = Complete visibility

---

## 📝 FUTURE STATE (Microsoft Integration)

**When Microsoft integration becomes available:**

```python
# Replace Gmail forwarding
def get_flagged_emails(start_date, end_date):
    # Instead of Gmail
    # emails = gmail.search('from:justin subject:TGIF')
    
    # Use Microsoft Graph API
    emails = microsoft_graph.search(
        mailbox='justin@hcss.com',
        folder='TGIF',
        date_range=(start_date, end_date)
    )
    
    return emails
```

**Migration path:**
1. Build with Gmail (works today)
2. Add Microsoft Graph when available
3. Run both in parallel (validation)
4. Switch to Microsoft as primary
5. Keep Gmail as fallback

---

**Architecture updated: Standalone meeting summaries + Weekly rollup (meetings + flagged emails). Current state uses Gmail forwarding, future state will use Microsoft integration.** ✅
