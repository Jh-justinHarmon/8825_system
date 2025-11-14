# TGIF Meeting Automation - Otter.ai Integration

**Current Setup:** Otter.ai → Gmail Inbox  
**Goal:** Automate retrieval from Otter.ai (bypass Gmail manual check)

---

## 🎯 YOUR CURRENT WORKFLOW

### **What Works Now:**
1. ✅ Otter.ai joins TGIF meetings automatically
2. ✅ Otter.ai transcribes in real-time
3. ✅ Otter.ai sends transcript to Gmail inbox
4. ✅ You manually check Gmail for new transcripts

### **What We'll Automate:**
1. ✅ Poll Otter.ai API for new transcripts (no Gmail check)
2. ✅ Download transcript automatically
3. ✅ Feed to Chat Mining Agent
4. ✅ Generate summary automatically

---

## 🔧 OTTER.AI API OPTIONS

### **Option 1: Official Zapier Integration** ⭐ RECOMMENDED

**What Otter Provides:**
- Official Zapier integration
- Exports: transcripts, summaries, action items
- Trigger: New recording created
- Max 3 most recent recordings per export

**How It Works:**
```
Otter.ai (new transcript) 
    → Zapier Trigger
    → Webhook to 8825 MCP Server
    → Chat Mining Agent
    → Summary Generated
```

**Setup:**
1. Connect Otter.ai to Zapier
2. Create Zap: "New Recording in Otter" → "Webhook POST"
3. Webhook sends to: `http://localhost:8828/ingest/otter`
4. 8825 MCP receives transcript, processes automatically

**Pros:**
- ✅ Official integration (reliable)
- ✅ No API key management
- ✅ Real-time trigger (instant)
- ✅ Includes summaries + action items from Otter

**Cons:**
- ⚠️ Requires Zapier account
- ⚠️ Limited to 3 most recent recordings

---

### **Option 2: Unofficial Python API**

**What's Available:**
- Unofficial library: `gmchad/otterai-api`
- Login with username/password
- Full API access

**How It Works:**
```python
from otterai import OtterAI

# Login
otter = OtterAI()
otter.login('your_email', 'your_password')

# Get all speeches (transcripts)
speeches = otter.get_speeches()

# Download specific speech
otter.download_speech(
    speech_id='abc123',
    filename='tgif_meeting.txt',
    format='txt'  # or pdf, docx, srt
)
```

**Scheduled Polling:**
```python
# Run every 15 minutes
def check_for_new_transcripts():
    # Get speeches from last 24 hours
    speeches = otter.get_speeches()
    
    for speech in speeches:
        # Check if TGIF meeting
        if 'TGIF' in speech.title:
            # Check if already processed
            if not already_processed(speech.id):
                # Download transcript
                transcript = otter.download_speech(
                    speech.id,
                    format='txt'
                )
                
                # Process with Chat Mining Agent
                process_transcript(transcript)
                
                # Mark as processed
                mark_processed(speech.id)
```

**Pros:**
- ✅ Full control
- ✅ No Zapier needed
- ✅ Can query all speeches
- ✅ Multiple format options

**Cons:**
- ⚠️ Unofficial (could break)
- ⚠️ Need to manage credentials
- ⚠️ Polling (not real-time)

---

### **Option 3: Gmail API** (Your Current Method, Automated)

**Keep Gmail, Automate It:**
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Connect to Gmail
service = build('gmail', 'v1', credentials=creds)

# Search for Otter.ai emails
query = 'from:no-reply@otter.ai subject:TGIF'
results = service.users().messages().list(
    userId='me',
    q=query,
    maxResults=10
).execute()

# Get messages
messages = results.get('messages', [])

for msg in messages:
    # Get full message
    message = service.users().messages().get(
        userId='me',
        id=msg['id']
    ).execute()
    
    # Extract transcript link or attachment
    transcript_url = extract_otter_link(message)
    
    # Download transcript
    transcript = download_from_url(transcript_url)
    
    # Process
    process_transcript(transcript)
```

**Pros:**
- ✅ Uses your existing workflow
- ✅ Gmail API is official/stable
- ✅ Can access email history

**Cons:**
- ⚠️ Indirect (Otter → Gmail → 8825)
- ⚠️ Need to parse emails
- ⚠️ Polling (not real-time)

---

## 🎯 RECOMMENDED APPROACH

### **Phase 1: Quick Win (Gmail API)**
**Why:** Works with your current setup, minimal changes

**Implementation:**
```python
# Check Gmail every 15 minutes
schedule.every(15).minutes.do(check_gmail_for_otter)

def check_gmail_for_otter():
    # Search for unread Otter emails with TGIF
    emails = gmail.search(
        query='from:no-reply@otter.ai subject:TGIF is:unread'
    )
    
    for email in emails:
        # Extract transcript
        transcript = extract_transcript_from_email(email)
        
        # Process with Chat Mining Agent
        summary = chat_mining_agent.process(transcript)
        
        # Mark email as read
        gmail.mark_as_read(email.id)
        
        # Save summary
        save_summary(summary)
```

**Effort:** 1-2 hours  
**Benefit:** Immediate automation

---

### **Phase 2: Better Integration (Zapier)**
**Why:** Real-time, official, includes Otter's AI summaries

**Setup:**
1. **Zapier Trigger:** "New Recording in Otter.ai"
2. **Filter:** Only if title contains "TGIF"
3. **Webhook:** POST to `http://localhost:8828/ingest/otter`
4. **Payload:**
```json
{
  "source": "otter_zapier",
  "meeting_id": "{{recording_id}}",
  "title": "{{recording_title}}",
  "date": "{{recording_date}}",
  "transcript": "{{transcript}}",
  "otter_summary": "{{summary}}",
  "otter_action_items": "{{action_items}}"
}
```

**MCP Endpoint:**
```python
@app.route('/ingest/otter', methods=['POST'])
def ingest_otter():
    data = request.json
    
    # Already have Otter's AI summary
    otter_summary = data.get('otter_summary')
    otter_actions = data.get('otter_action_items')
    
    # Run Chat Mining Agent for additional extraction
    our_summary = chat_mining_agent.process(
        data['transcript'],
        context={
            'otter_summary': otter_summary,
            'otter_actions': otter_actions
        }
    )
    
    # Merge Otter's AI + our extraction
    final_summary = merge_summaries(otter_summary, our_summary)
    
    return jsonify({"status": "processed"})
```

**Effort:** 2-3 hours  
**Benefit:** Real-time + Otter's AI insights

---

### **Phase 3: Full Control (Unofficial API)**
**Why:** Maximum flexibility, no dependencies

**Only if:**
- Zapier not an option
- Need to query historical transcripts
- Want full control

---

## 📊 COMPARISON

| Method | Real-Time | Official | Effort | Otter AI Included |
|--------|-----------|----------|--------|-------------------|
| **Gmail API** | No (15min poll) | ✅ Yes | 1-2h | No |
| **Zapier** | ✅ Yes | ✅ Yes | 2-3h | ✅ Yes |
| **Unofficial API** | No (poll) | ❌ No | 3-4h | No |

---

## 🚀 IMPLEMENTATION PLAN

### **Week 1: Gmail Automation (Quick Win)**

**Day 1-2: Setup Gmail API**
```bash
# Install Google API client
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Setup OAuth credentials
python setup_gmail_auth.py
```

**Day 3-4: Build Polling Script**
```python
# gmail_otter_poller.py
import schedule
import time
from gmail_client import GmailClient
from chat_mining_agent import ChatMiningAgent

gmail = GmailClient()
agent = ChatMiningAgent()

def poll_for_transcripts():
    print("Checking Gmail for Otter transcripts...")
    
    # Search for TGIF transcripts
    emails = gmail.search(
        'from:no-reply@otter.ai subject:TGIF is:unread'
    )
    
    print(f"Found {len(emails)} new transcripts")
    
    for email in emails:
        try:
            # Extract transcript
            transcript = extract_transcript(email)
            
            # Process
            summary = agent.process(transcript)
            
            # Save
            save_summary(summary)
            
            # Mark as read
            gmail.mark_as_read(email.id)
            
            print(f"Processed: {email.subject}")
            
        except Exception as e:
            print(f"Error processing {email.id}: {e}")

# Run every 15 minutes
schedule.every(15).minutes.do(poll_for_transcripts)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
```

**Day 5: Test & Deploy**
- Test with recent TGIF meeting
- Verify summary quality
- Deploy as background service

---

### **Week 2: Zapier Integration (Better)**

**Day 1: Setup Zapier**
1. Create Zapier account (if needed)
2. Connect Otter.ai account
3. Create Zap: "New Recording" trigger

**Day 2: Configure Webhook**
```yaml
# Zapier Webhook Configuration
URL: http://your-server:8828/ingest/otter
Method: POST
Headers:
  X-API-Key: your_8825_api_key
Body:
  meeting_id: {{recording_id}}
  title: {{recording_title}}
  date: {{recording_date}}
  transcript: {{transcript}}
  summary: {{summary}}
  action_items: {{action_items}}
```

**Day 3: Build MCP Endpoint**
```python
# Add to 8825_core/mcp/inbox_server.py

@app.route('/ingest/otter', methods=['POST'])
def ingest_otter():
    # Validate API key
    if not validate_api_key(request.headers.get('X-API-Key')):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    
    # Process transcript
    result = process_otter_transcript(data)
    
    return jsonify(result)

def process_otter_transcript(data):
    # Save raw data
    save_to_inbox({
        "type": "otter_transcript",
        "source": "zapier",
        "data": data
    })
    
    # Run Chat Mining Agent
    summary = chat_mining_agent.process(
        data['transcript'],
        context={
            'otter_summary': data.get('summary'),
            'otter_actions': data.get('action_items')
        }
    )
    
    return summary
```

**Day 4-5: Test & Tune**
- Trigger test meeting
- Verify webhook delivery
- Compare Otter AI vs Chat Mining Agent
- Tune extraction rules

---

## 🎓 TEACHING MOMENT: WHY MULTIPLE OPTIONS?

### **The Principle: Start Simple, Evolve**

**Phase 1 (Gmail):**
- ✅ Works with existing setup
- ✅ Quick to implement
- ✅ Proves the concept
- ⚠️ Not real-time

**Phase 2 (Zapier):**
- ✅ Real-time triggers
- ✅ Official integration
- ✅ Includes Otter's AI
- ⚠️ Adds dependency

**Phase 3 (Direct API):**
- ✅ Full control
- ✅ No dependencies
- ⚠️ Unofficial (risky)
- ⚠️ More maintenance

### **The Pattern: Crawl → Walk → Run**

Don't jump to the "perfect" solution. Build incrementally:
1. **Crawl:** Gmail polling (works today)
2. **Walk:** Zapier (better, still simple)
3. **Run:** Direct API (only if needed)

---

## 📝 UPDATED PIPELINE

### **Step 2: Content Ingestion (Otter.ai)**

```
┌─────────────────────────────────────────────────────────┐
│  OPTION A: Gmail Polling (Phase 1)                      │
│  ──────────────────────────                             │
│  • Gmail API: Search for Otter emails                   │
│  • Filter: from:no-reply@otter.ai + TGIF                │
│  • Extract: Transcript link or text                     │
│  • Schedule: Every 15 minutes                           │
└─────────────────────────────────────────────────────────┘
                          OR
┌─────────────────────────────────────────────────────────┐
│  OPTION B: Zapier Webhook (Phase 2)                     │
│  ────────────────────────                               │
│  • Otter.ai: New recording created                      │
│  • Zapier: Trigger webhook                              │
│  • MCP Server: Receive transcript                       │
│  • Real-time: Instant processing                        │
│  • Bonus: Includes Otter's AI summary                   │
└─────────────────────────────────────────────────────────┘
                          ↓
                  Chat Mining Agent
                          ↓
                  Structured Summary
```

---

## 🎯 RECOMMENDATION

**Start with Gmail API (Phase 1):**
- Works with your current setup
- 1-2 hours to implement
- Proves automation value
- Can upgrade to Zapier later

**Upgrade to Zapier (Phase 2) if:**
- Gmail polling feels slow
- Want real-time processing
- Want Otter's AI summaries included

---

## 📦 DELIVERABLES

**Phase 1 (Gmail):**
- `gmail_otter_poller.py` - Polling script
- `gmail_client.py` - Gmail API wrapper
- `extract_transcript.py` - Email parsing
- Cron job or systemd service

**Phase 2 (Zapier):**
- Zapier Zap configuration
- MCP endpoint `/ingest/otter`
- Webhook validation
- Summary merge logic

---

**Your current Otter.ai → Gmail workflow can be automated. Start with Gmail API, upgrade to Zapier when ready.** ✅
