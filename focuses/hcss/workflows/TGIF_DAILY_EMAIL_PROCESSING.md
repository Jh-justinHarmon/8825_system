# TGIF Daily Email Processing & Task Tracking

**Schedule:** Every day at 12pm (Mon-Fri)  
**Purpose:** Process flagged emails daily, update task tracking, roll up to weekly summary

---

## 🎯 DAILY WORKFLOW

### **Every Day at 12pm:**

```
1. Detect new flagged emails (last 24 hours)
2. Process with Chat Mining Agent
3. Extract action items
4. Update task tracker
5. Flag overdue items
6. Save to knowledge base
```

### **Friday at 3pm:**

```
1. Collect all daily email extracts (Mon-Fri)
2. Collect all meeting summaries (Mon-Fri)
3. Aggregate everything
4. Generate weekly digest
```

---

## 🔧 IMPLEMENTATION

### **Daily Email Processor (Runs at 12pm):**

```python
# daily_email_processor.py

import schedule
from datetime import datetime, timedelta

def process_daily_emails():
    """Run daily at 12pm to process flagged TGIF emails"""
    
    print(f"[{now()}] Starting daily email processing...")
    
    # Get emails from last 24 hours
    yesterday_noon = now() - timedelta(hours=24)
    new_emails = get_new_flagged_emails(since=yesterday_noon)
    
    print(f"Found {len(new_emails)} new flagged emails")
    
    # Process each email
    email_extracts = []
    for email in new_emails:
        extract = process_email(email)
        email_extracts.append(extract)
        
        # Update task tracker immediately
        update_task_tracker(extract)
    
    # Save daily batch
    save_daily_batch(email_extracts)
    
    # Generate daily summary (optional)
    daily_summary = generate_daily_summary(email_extracts)
    
    print(f"Processed {len(email_extracts)} emails")
    print(f"New actions: {count_actions(email_extracts)}")
    print(f"Red flags: {count_red_flags(email_extracts)}")
    
    return daily_summary

def get_new_flagged_emails(since):
    """Get TGIF emails flagged since last run"""
    
    # Format date for Gmail query
    after_date = since.strftime('%Y/%m/%d')
    
    # Search for forwarded emails
    query_forwarded = f'''
        from:justin@hcss.com 
        subject:TGIF 
        after:{after_date}
    '''
    
    # Search for labeled emails
    query_labeled = f'''
        label:TGIF 
        after:{after_date}
    '''
    
    forwarded = gmail.search(query_forwarded)
    labeled = gmail.search(query_labeled)
    
    # Combine and dedupe
    all_emails = dedupe_emails(forwarded + labeled)
    
    return all_emails

def process_email(email):
    """Extract structured data from email"""
    
    # Get full email content
    content = gmail.get_message(email.id)
    
    # Extract with Chat Mining Agent
    extract = chat_mining_agent.process(
        content,
        context={
            'type': 'email',
            'from': email.from_address,
            'subject': email.subject,
            'date': email.date,
            'project': 'TGIF'
        }
    )
    
    # Structure output
    return {
        'type': 'tgif_email_extract',
        'email_id': email.id,
        'date': email.date,
        'from': email.from_address,
        'subject': email.subject,
        'key_points': extract.key_points,
        'actions': extract.actions,
        'risks': extract.risks,
        'decisions': extract.decisions,
        'metadata': {
            'processed_at': now(),
            'source': 'daily_email_processor',
            'confidence_avg': extract.confidence_avg
        }
    }

def update_task_tracker(email_extract):
    """Update task tracking with new actions from email"""
    
    for action in email_extract['actions']:
        # Create task ID
        task_id = f"ACT-{email_extract['date']}-EMAIL-{action['id']}"
        
        # Add to tracker
        task_tracker.add_task({
            'id': task_id,
            'what': action['what'],
            'who': action.get('who', 'TBD'),
            'due': action.get('due'),
            'priority': action.get('priority', 'medium'),
            'status': 'todo',
            'source': 'email',
            'source_id': email_extract['email_id'],
            'created_at': now()
        })
        
        # Check if overdue
        if action.get('due'):
            if parse_date(action['due']) < today():
                task_tracker.flag_overdue(task_id)

def save_daily_batch(email_extracts):
    """Save daily email extracts to knowledge base"""
    
    date_str = today().strftime('%Y-%m-%d')
    
    # Save individual extracts
    for extract in email_extracts:
        filename = f"TGIF_Email_{extract['date']}_{extract['email_id']}.json"
        path = f"focuses/hcss/knowledge/emails/{filename}"
        save_json(path, extract)
    
    # Save daily batch summary
    batch = {
        'date': date_str,
        'emails_count': len(email_extracts),
        'actions_count': sum(len(e['actions']) for e in email_extracts),
        'extracts': email_extracts
    }
    
    batch_path = f"focuses/hcss/knowledge/emails/daily_batches/TGIF_Daily_Batch_{date_str}.json"
    save_json(batch_path, batch)

def generate_daily_summary(email_extracts):
    """Generate optional daily summary"""
    
    if not email_extracts:
        return None
    
    summary = {
        'date': today().strftime('%Y-%m-%d'),
        'emails_processed': len(email_extracts),
        'new_actions': sum(len(e['actions']) for e in email_extracts),
        'red_flags': [],
        'highlights': []
    }
    
    # Extract highlights
    for extract in email_extracts:
        for point in extract['key_points']:
            if point.get('importance') == 'high':
                summary['highlights'].append({
                    'from': extract['from'],
                    'subject': extract['subject'],
                    'point': point['text']
                })
        
        # Check for red flags
        for risk in extract.get('risks', []):
            if risk.get('severity') in ['high', 'critical']:
                summary['red_flags'].append({
                    'from': extract['from'],
                    'subject': extract['subject'],
                    'risk': risk['text']
                })
    
    return summary

# Schedule daily run
schedule.every().day.at("12:00").do(process_daily_emails)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📊 TASK TRACKER

### **Task Tracker Schema:**

```json
{
  "tasks": [
    {
      "id": "ACT-2025-11-09-001",
      "what": "Complete Toast training for MA stores",
      "who": "BH",
      "due": "2025-11-15",
      "priority": "high",
      "status": "todo",
      "source": "meeting",
      "source_id": "gcal:abc123",
      "created_at": "2025-11-09T11:30:00Z",
      "updated_at": "2025-11-09T11:30:00Z",
      "overdue": false
    },
    {
      "id": "ACT-2025-11-08-EMAIL-001",
      "what": "Update Toast menu with new pricing",
      "who": "TBD",
      "due": "2025-11-14",
      "priority": "high",
      "status": "todo",
      "source": "email",
      "source_id": "gmail:xyz789",
      "created_at": "2025-11-08T12:00:00Z",
      "updated_at": "2025-11-08T12:00:00Z",
      "overdue": false
    }
  ],
  "metadata": {
    "last_updated": "2025-11-09T12:00:00Z",
    "total_tasks": 23,
    "overdue_count": 2,
    "by_status": {
      "todo": 15,
      "in_progress": 5,
      "done": 3
    },
    "by_owner": {
      "BH": 8,
      "Operations": 6,
      "TBD": 9
    }
  }
}
```

### **Task Tracker Operations:**

```python
# task_tracker.py

class TaskTracker:
    def __init__(self):
        self.tasks_file = "focuses/hcss/knowledge/task_tracker.json"
        self.tasks = self.load_tasks()
    
    def add_task(self, task):
        """Add new task to tracker"""
        self.tasks.append(task)
        self.save_tasks()
    
    def update_task(self, task_id, updates):
        """Update existing task"""
        task = self.get_task(task_id)
        if task:
            task.update(updates)
            task['updated_at'] = now()
            self.save_tasks()
    
    def flag_overdue(self, task_id):
        """Mark task as overdue"""
        self.update_task(task_id, {'overdue': True})
    
    def get_tasks_by_owner(self, owner):
        """Get all tasks for specific owner"""
        return [t for t in self.tasks if t['who'] == owner]
    
    def get_overdue_tasks(self):
        """Get all overdue tasks"""
        return [t for t in self.tasks if t.get('overdue', False)]
    
    def check_overdue(self):
        """Check all tasks for overdue status"""
        today = datetime.now().date()
        
        for task in self.tasks:
            if task.get('due'):
                due_date = parse_date(task['due'])
                if due_date < today and task['status'] != 'done':
                    task['overdue'] = True
        
        self.save_tasks()
    
    def save_tasks(self):
        """Save tasks to file"""
        data = {
            'tasks': self.tasks,
            'metadata': self.calculate_metadata()
        }
        save_json(self.tasks_file, data)
    
    def calculate_metadata(self):
        """Calculate task statistics"""
        return {
            'last_updated': now(),
            'total_tasks': len(self.tasks),
            'overdue_count': len(self.get_overdue_tasks()),
            'by_status': self.group_by_status(),
            'by_owner': self.group_by_owner()
        }
```

---

## 📅 DAILY SCHEDULE

### **Monday - Thursday:**

**12:00 PM:**
- Process new flagged emails
- Extract action items
- Update task tracker
- Check for overdue tasks
- Save daily batch

### **Friday:**

**12:00 PM:**
- Process new flagged emails (same as Mon-Thu)
- Update task tracker

**3:00 PM:**
- Collect all daily batches (Mon-Fri)
- Collect all meeting summaries (Mon-Fri)
- Aggregate everything
- Generate weekly digest
- Send to stakeholders

---

## 📊 DAILY SUMMARY (Optional)

### **Daily Email Digest (Sent at 12:15pm):**

```markdown
# TGIF Daily Update - Nov 9, 2025

**Processed:** 3 new emails

---

## 📧 New Emails

1. **Sysco Pricing Update**
   - From: vendor@sysco.com
   - Key: New pricing structure effective Nov 15

2. **Training Completion**
   - From: ops@tgif.com
   - Key: MA stores training complete

3. **Vendor Status**
   - From: vendor@supplies.com
   - Key: Delivery delayed by 2 days

---

## ✅ New Action Items (3)

- [ ] Update Toast menu pricing - Due Nov 14 (TBD)
- [ ] Schedule vendor follow-up - Due Nov 12 (Operations)
- [ ] Review training completion - Due Nov 10 (BH)

---

## 🚨 Red Flags (1)

- **Vendor delivery delayed** - May impact store opening

---

**Task Tracker Updated:** 23 total tasks, 2 overdue
```

---

## 🔄 INTEGRATION WITH WEEKLY ROLLUP

### **How Daily Processing Feeds Weekly:**

```python
# weekly_rollup.py

def generate_weekly_rollup():
    week_start = get_monday()
    week_end = get_friday()
    
    # Collect daily email batches (already processed)
    daily_batches = []
    for day in range(5):  # Mon-Fri
        date = week_start + timedelta(days=day)
        batch_file = f"focuses/hcss/knowledge/emails/daily_batches/TGIF_Daily_Batch_{date}.json"
        
        if file_exists(batch_file):
            batch = load_json(batch_file)
            daily_batches.append(batch)
    
    # Flatten all email extracts
    all_email_extracts = []
    for batch in daily_batches:
        all_email_extracts.extend(batch['extracts'])
    
    # Collect meeting summaries
    meeting_summaries = get_meeting_summaries(week_start, week_end)
    
    # Get current task tracker state
    task_tracker_state = task_tracker.get_state()
    
    # Aggregate everything
    rollup = aggregate_sources(
        meetings=meeting_summaries,
        emails=all_email_extracts,
        tasks=task_tracker_state
    )
    
    return rollup
```

---

## 🎯 BENEFITS OF DAILY PROCESSING

### **1. Continuous Task Tracking**
- ✅ Tasks updated daily (not just Friday)
- ✅ Overdue items flagged immediately
- ✅ Better visibility throughout week

### **2. Reduced Friday Load**
- ✅ Emails already processed (not all at once)
- ✅ Faster weekly rollup generation
- ✅ Less compute time on Friday

### **3. Timely Action**
- ✅ New actions identified within 24 hours
- ✅ Red flags surfaced daily (not weekly)
- ✅ Can respond faster to urgent items

### **4. Better Data Quality**
- ✅ Smaller batches = better accuracy
- ✅ Context fresher when processing
- ✅ Easier to validate extractions

---

## 📁 FILE STRUCTURE

```
focuses/hcss/knowledge/
├── meetings/
│   ├── json/
│   └── summaries/
├── emails/
│   ├── TGIF_Email_2025-11-08_xyz789.json
│   ├── TGIF_Email_2025-11-09_abc123.json
│   └── daily_batches/
│       ├── TGIF_Daily_Batch_2025-11-04.json
│       ├── TGIF_Daily_Batch_2025-11-05.json
│       ├── TGIF_Daily_Batch_2025-11-06.json
│       ├── TGIF_Daily_Batch_2025-11-07.json
│       └── TGIF_Daily_Batch_2025-11-08.json
├── task_tracker.json
└── rollups/
    └── TGIF_Rollup_2025-11-08.json
```

---

## 🚀 IMPLEMENTATION TIMELINE

### **Week 1: Daily Email Processing**
- Day 1-2: Build daily email processor
- Day 3: Integrate with Chat Mining Agent
- Day 4: Build task tracker
- Day 5: Test daily runs

### **Week 2: Task Tracking**
- Day 1-2: Implement task tracker operations
- Day 3: Add overdue detection
- Day 4: Build daily summary (optional)
- Day 5: Test integration

### **Week 3: Weekly Rollup Integration**
- Day 1-2: Update weekly rollup to use daily batches
- Day 3: Test full week cycle
- Day 4: Tune and optimize
- Day 5: Deploy to production

---

**Daily processing at 12pm ensures continuous task tracking and reduces Friday load. Everything rolls up to weekly summary at 3pm.** ✅
