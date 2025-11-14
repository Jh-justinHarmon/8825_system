# Customer Platform: PoC Foundation Design
**Created:** 2025-11-12  
**Purpose:** Practical PoC implementation with trusted test users

---

## PoC vs Production Distinction

### **PoC (Now):**
- Data in JH's Dropbox (simpler)
- Testing with trusted individuals
- Focus: Prove the model works
- Timeline: 2-4 weeks

### **Production (Later):**
- Data in customer's cloud (sovereignty)
- Full customer onboarding
- Focus: Scale and handoff
- Timeline: After PoC validation

**Philosophy analysis was correct - keeping it for production roadmap**

---

## PoC Scope

### **Test User First:**
- Create TEST customer
- Synthetic data
- Validate all workflows
- Refine before real users

### **Then Real Users (Trusted):**
- PS (medical records)
- MES (corporate testing)
- Joju user (professional profile)

**All in JH's Dropbox for PoC simplicity**

---

## PoC Architecture (Simplified)

### **Storage Structure:**

```
~/Hammer Consulting Dropbox/Justin Harmon/Public/8825/
└── 8825_customers/
    ├── TEST/
    │   ├── brain.json
    │   ├── context.db
    │   ├── config.json
    │   └── logs/
    ├── ps_medical/
    │   ├── brain.json
    │   ├── context.db
    │   ├── config.json
    │   └── logs/
    ├── mes_corporate/
    │   └── ...
    └── joju_user_001/
        └── ...
```

**All in JH's Dropbox - simple, fast, testable**

---

## Core Functions (Unchanged)

### **Three Functions:**

```javascript
// lib/core.js

async function ingest(customer_id, data) {
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
  const processed = await LLMRouter.route({
    type: 'extract_data',
    content: data,
    prompt: buildIngestPrompt(brain, data)
  });
  
  const db = openDB(`~/8825_customers/${customer_id}/context.db`);
  db.insert(processed.result);
  
  if (processed.result.learned_something) {
    brain.memory = processed.result.updated_memory;
    saveJSON(`~/8825_customers/${customer_id}/brain.json`, brain);
  }
  
  return processed;
}

async function query(customer_id, question) {
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
  const db = openDB(`~/8825_customers/${customer_id}/context.db`);
  const relevant = db.search(question);
  
  const answer = await LLMRouter.route({
    type: 'customer_response',
    content: question,
    prompt: buildQueryPrompt(brain, relevant, question)
  });
  
  return answer;
}

async function analyze(customer_id) {
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
  const db = openDB(`~/8825_customers/${customer_id}/context.db`);
  const recent = db.query("SELECT * FROM records WHERE date > DATE('now', '-7 days')");
  
  const analysis = await LLMRouter.route({
    type: 'weekly_analysis',
    content: JSON.stringify(recent),
    prompt: buildAnalysisPrompt(brain, recent)
  });
  
  brain.memory = analysis.result.updated_memory;
  brain.state.last_analysis = new Date();
  saveJSON(`~/8825_customers/${customer_id}/brain.json`, brain);
  
  return analysis;
}

module.exports = { ingest, query, analyze };
```

---

## Interface Options for PoC

### **Option 1: Windsurf/Cascade Direct (JH Only)**

**Your workflow:**
```
Windsurf → Cascade → 8825 mode
    ↓
"Ingest this data for TEST customer: [data]"
    ↓
Cascade calls ingest() function
    ↓
Returns result
```

**Pros:**
- ✅ Immediate (no setup)
- ✅ Your natural workflow
- ✅ Full visibility
- ✅ Easy debugging

**Cons:**
- ❌ Only works for you
- ❌ Customers can't use it
- ❌ Not testing customer interface

**Use for:** Initial testing, debugging, validation

---

### **Option 2: Email Gateway (Customer Interface)**

**Customer workflow:**
```
PS forwards email → ps@8825.ai
    ↓
Email webhook receives
    ↓
Routes to ps_medical
    ↓
Calls ingest() or query()
    ↓
Emails response back
```

**Pros:**
- ✅ Tests real customer interface
- ✅ Zero friction for customers
- ✅ Validates full flow
- ✅ Production-like

**Cons:**
- ⚠️ Requires email setup (Mailgun/SendGrid)
- ⚠️ More moving parts
- ⚠️ Harder to debug

**Use for:** Customer-facing testing after Windsurf validation

---

### **Option 3: Simple CLI (Testing Tool)**

**Testing workflow:**
```bash
# Ingest data
./8825-customer ingest TEST "Sample medical record..."

# Query
./8825-customer query TEST "What's the trend?"

# Analyze
./8825-customer analyze TEST
```

**Pros:**
- ✅ Simple testing
- ✅ No email setup needed
- ✅ Easy to script
- ✅ Good for automation

**Cons:**
- ⚠️ Not customer-facing
- ⚠️ Another tool to build

**Use for:** Automated testing, validation scripts

---

## PoC Timeline (2 Weeks)

### **Week 1: Build + Test User**

**Day 1-2: Core Functions**
```javascript
// lib/core.js - ingest, query, analyze
// lib/storage.js - loadBrain, saveBrain, openDB
// lib/llm_router.js - LLM orchestration
```

**Day 3: TEST Customer Setup**
```bash
# Create TEST customer
mkdir -p ~/8825_customers/TEST/logs

# Initialize brain
cat > ~/8825_customers/TEST/brain.json << EOF
{
  "customer_id": "TEST",
  "customer_name": "Test User",
  "type": "test",
  "purpose": "Validate 8825 customer platform",
  "workflows": {
    "ingest": "Extract and categorize test data",
    "analyze": "Generate test summaries"
  },
  "memory": {},
  "state": {
    "last_analysis": null,
    "next_scheduled": null
  }
}
EOF

# Initialize database
sqlite3 ~/8825_customers/TEST/context.db << EOF
CREATE TABLE records (
  id INTEGER PRIMARY KEY,
  date TEXT,
  type TEXT,
  content TEXT,
  metadata TEXT,
  created_at TEXT
);
CREATE INDEX idx_date ON records(date);
CREATE INDEX idx_type ON records(type);
EOF

# Initialize config
cat > ~/8825_customers/TEST/config.json << EOF
{
  "customer_id": "TEST",
  "email": "test@8825.ai",
  "schedule": "daily",
  "status": "active"
}
EOF
```

**Day 4-5: Test via Windsurf/Cascade**
```
In Windsurf/Cascade/8825 mode:

1. "Ingest this test data for TEST customer: [synthetic medical record]"
   → Validate extraction, categorization, storage

2. "Query TEST customer: What data do we have?"
   → Validate retrieval, brain context, response

3. "Run analysis for TEST customer"
   → Validate analysis, memory updates, summary generation

4. Check logs, costs, quality
```

**Day 6-7: Refine + Document**
- Fix bugs found in testing
- Optimize LLM routing
- Document learnings
- Prepare for real users

---

### **Week 2: Real Users (Trusted)**

**Day 8-9: PS Medical**
```bash
# Create PS customer
mkdir -p ~/8825_customers/ps_medical/logs

# Initialize with medical-specific brain
{
  "customer_id": "ps_medical",
  "customer_name": "Phillip Sheehan",
  "type": "personal_health",
  "purpose": "Track and analyze personal health data for PS",
  "workflows": {
    "ingest": "Extract health data (labs, prescriptions, appointments)",
    "analyze": "Weekly health trend analysis with plain-language summary"
  },
  "memory": {
    "learned_patterns": {},
    "preferences": {
      "communication_style": "conversational, not clinical",
      "alert_threshold": "conservative"
    }
  },
  "state": {
    "last_analysis": null,
    "next_scheduled": "2025-11-17T22:00:00Z"
  }
}

# Test with real medical records (with PS's permission)
```

**Day 10-11: MES Corporate**
```bash
# Create MES customer
mkdir -p ~/8825_customers/mes_corporate/logs

# Initialize with corporate-specific brain
{
  "customer_id": "mes_corporate",
  "customer_name": "Mary Sheehan",
  "type": "corporate_testing",
  "purpose": "Track compliance testing and generate team summaries",
  "workflows": {
    "ingest": "Extract test results, compliance data, team metrics",
    "analyze": "Weekly compliance summary for team distribution"
  },
  "memory": {
    "learned_patterns": {},
    "preferences": {
      "communication_style": "professional, data-driven",
      "summary_format": "executive_summary"
    }
  },
  "state": {
    "last_analysis": null,
    "next_scheduled": "2025-11-17T22:00:00Z"
  }
}

# Test with real testing data (with MES's permission)
```

**Day 12-13: Joju User**
```bash
# Create Joju user
mkdir -p ~/8825_customers/joju_user_001/logs

# Initialize with profile-specific brain
{
  "customer_id": "joju_user_001",
  "customer_name": "Test Joju User",
  "type": "professional_profile",
  "purpose": "Optimize professional profile and suggest improvements",
  "workflows": {
    "ingest": "Extract career data, skills, achievements",
    "analyze": "Weekly profile optimization suggestions"
  },
  "memory": {
    "learned_patterns": {},
    "preferences": {
      "communication_style": "encouraging, actionable",
      "optimization_focus": "career_growth"
    }
  },
  "state": {
    "last_analysis": null,
    "next_scheduled": "2025-11-17T22:00:00Z"
  }
}

# Test with real profile data
```

**Day 14: Review + Next Steps**
- Validate all three use cases
- Compare costs across customers
- Document learnings
- Plan production migration

---

## Testing Checklist

### **For Each Customer:**

**Ingestion:**
- [ ] Can ingest data via Windsurf/Cascade
- [ ] Data extracted correctly
- [ ] Stored in context.db
- [ ] Brain memory updated
- [ ] Logs show activity
- [ ] Costs tracked

**Query:**
- [ ] Can query via Windsurf/Cascade
- [ ] Retrieves relevant context
- [ ] Brain provides intelligent response
- [ ] Response quality is good
- [ ] Costs reasonable

**Analysis:**
- [ ] Can trigger analysis
- [ ] Analyzes recent data
- [ ] Generates useful summary
- [ ] Updates brain memory
- [ ] Quality meets expectations
- [ ] Costs acceptable

**Isolation:**
- [ ] PS's data separate from MES
- [ ] MES's data separate from Joju
- [ ] No cross-contamination
- [ ] Each brain has own memory

**Cost Control:**
- [ ] LLM router working
- [ ] Pattern matching used when possible
- [ ] Cheap model used appropriately
- [ ] Expensive model only when needed
- [ ] Total costs < $1/customer/week

---

## Your Workflow (JH)

### **In Windsurf/Cascade/8825 Mode:**

**Ingest data:**
```
"Ingest this data for ps_medical:
[paste medical record]"

→ Cascade calls ingest('ps_medical', data)
→ Returns: "Extracted lab result from 2025-11-12. Added to context. No concerning patterns."
```

**Query customer:**
```
"Query ps_medical: What's the blood pressure trend over the last 3 months?"

→ Cascade calls query('ps_medical', question)
→ Returns: "Blood pressure has been stable at 120/80 over the last 3 months. Last reading was 2025-11-10."
```

**Run analysis:**
```
"Run weekly analysis for ps_medical"

→ Cascade calls analyze('ps_medical')
→ Returns: "Weekly analysis complete. Summary: [health summary]. Cost: $0.15"
```

**Check status:**
```
"Show me stats for all customers"

→ Cascade calls getStats()
→ Returns:
  TEST: 5 records, last analysis 2025-11-12
  ps_medical: 12 records, last analysis 2025-11-10
  mes_corporate: 8 records, last analysis 2025-11-10
  Total cost this week: $0.45
```

---

## MCP Integration (For MG/76)

**Note:** MCP is for Matthew Galley (MG) integration with 76 and Joju, NOT for JH workflow.

**MG's workflow:**
```
Goose → MCP Server → 8825 Customer Platform
```

**MCP tools for MG:**
- `query_customer(customer_id, question)`
- `run_analysis(customer_id)`
- `list_customers()`
- `get_status(customer_id)`

**JH doesn't use this - JH uses Windsurf/Cascade/8825 mode directly**

---

## Production Migration Path

### **After PoC Validation:**

**What changes for production:**

1. **Data Sovereignty**
   - Move from JH's Dropbox to customer's cloud
   - Implement Dropbox/iCloud API integration
   - Customer grants access, can revoke anytime

2. **Customer Onboarding**
   - Automated setup flow
   - Email authorization
   - Brain initialization
   - Welcome email

3. **Email Gateway**
   - Set up email receiving (Mailgun/SendGrid)
   - Customer forwards to their@8825.ai
   - Automatic processing
   - Email responses

4. **Scheduler**
   - Background daemon
   - Check schedules hourly
   - Run analysis when due
   - Send email summaries

5. **Monitoring**
   - Usage dashboard
   - Cost tracking
   - Quality metrics
   - Alerting

**What stays the same:**
- Core functions (ingest, query, analyze)
- LLM router
- Brain format
- Database schema
- Three-tier intelligence

---

## PoC Success Criteria

### **Technical:**
- ✅ All three functions work (ingest, query, analyze)
- ✅ LLM router selects models correctly
- ✅ Costs < $1/customer/week
- ✅ Quality meets expectations
- ✅ Isolation verified (no cross-contamination)

### **User:**
- ✅ PS finds health summaries useful
- ✅ MES finds compliance reports valuable
- ✅ Joju user finds profile suggestions helpful

### **Business:**
- ✅ Model proven across 3 use cases
- ✅ Costs sustainable
- ✅ Quality consistent
- ✅ Ready to scale

---

## Next Steps

### **Immediate (This Week):**

1. **Build core functions** (Day 1-2)
   - `lib/core.js` - ingest, query, analyze
   - `lib/storage.js` - loadBrain, saveBrain, openDB
   - `lib/llm_router.js` - LLM orchestration

2. **Create TEST customer** (Day 3)
   - Initialize folder structure
   - Create brain.json
   - Create context.db
   - Create config.json

3. **Test via Windsurf/Cascade** (Day 4-5)
   - Ingest synthetic data
   - Query for results
   - Run analysis
   - Validate everything works

4. **Refine** (Day 6-7)
   - Fix bugs
   - Optimize costs
   - Document learnings

### **Next Week:**

5. **Real users** (Day 8-13)
   - PS medical
   - MES corporate
   - Joju user

6. **Review** (Day 14)
   - Validate success criteria
   - Plan production migration

---

## Bottom Line: PoC Foundation

**Simplified for testing:**
- Data in JH's Dropbox (not customer's)
- Testing with trusted users
- Focus on proving the model

**Your workflow:**
- Windsurf/Cascade/8825 mode (NOT Goose)
- Direct function calls
- Full visibility and control

**Timeline:**
- Week 1: Build + TEST customer
- Week 2: Real users (PS, MES, Joju)

**After PoC:**
- Migrate to production architecture
- Implement data sovereignty
- Add email gateway
- Scale to more customers

**Philosophy analysis preserved for production roadmap**

Ready to build Week 1 (core functions + TEST customer)?
