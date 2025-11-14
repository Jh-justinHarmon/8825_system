# MCP + Brain Architecture: Complete Mental Model
**Created:** 2025-11-12  
**Purpose:** Build complete understanding from first principles

---

## Part 1: What MCP Actually Is

### **The Restaurant Analogy**

**MCP Server = Menu + Waiter**
- Shows you what's available (tools)
- Takes your order (tool calls)
- Brings you food (results)
- Doesn't cook the food
- Doesn't store ingredients

**Your Code = Kitchen**
- Actually does the work
- Stores the data
- Processes requests
- Returns results

**AI Agent (Goose/Claude) = Customer**
- Reads menu (discovers tools)
- Places order (calls tools)
- Gets results
- Doesn't know about kitchen

---

### **MCP in Code**

**MCP Server (server.js):**
```javascript
// This is just the menu + waiter
const server = new Server({
  name: "ps-medical",
  version: "1.0.0"
});

// Tool definition (menu item)
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "query_health_data",
      description: "Search PS's medical records",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" }
        }
      }
    }
  ]
}));

// Tool implementation (waiter takes order to kitchen)
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_health_data") {
    // THIS is where the actual work happens
    const result = await queryHealthData(request.params.arguments.query);
    return { content: [{ type: "text", text: result }] };
  }
});
```

**Actual Implementation (kitchen):**
```javascript
// This is the kitchen - does the real work
async function queryHealthData(query) {
  // Load brain state
  const brain = loadJSON('~/8825_customers/ps_medical/brain_transport.json');
  
  // Load context database
  const db = openDatabase('~/8825_customers/ps_medical/context_index.db');
  
  // Search context
  const results = db.search(query);
  
  // Use brain to interpret
  const analysis = await GPT4.analyze(brain, results, query);
  
  return analysis;
}
```

**Key Insight:**
```
MCP Server ≠ Storage
MCP Server ≠ Processing
MCP Server = Interface

The actual work happens in your code
The actual data lives in files
MCP just exposes it to AI agents
```

---

## Part 2: What Brain Actually Is

### **Brain = State + Logic + Memory**

**NOT a running process (necessarily)**
**IS a JSON file with intelligence encoded**

---

### **Brain Transport Format**

**Think of it like a save game file:**

```json
{
  "meta": {
    "customer_id": "ps_medical",
    "customer_name": "Phillip Sheehan",
    "brain_version": "1.0.0",
    "created": "2025-11-12",
    "last_updated": "2025-11-12T13:35:00Z"
  },
  
  "philosophy": {
    "purpose": "Track and analyze personal health data for PS",
    "core_values": [
      "Privacy first - PS owns all data",
      "Proactive - alert on concerning patterns",
      "Educational - explain medical trends clearly"
    ],
    "constraints": [
      "HIPAA compliant - never share data",
      "Conservative - flag uncertainties",
      "Respectful - use plain language"
    ]
  },
  
  "workflows": {
    "ingest_medical_record": {
      "steps": [
        "Extract structured data (dates, values, medications)",
        "Categorize (lab result, prescription, appointment)",
        "Update context database",
        "Check for concerning patterns",
        "Update brain memory"
      ]
    },
    "weekly_health_analysis": {
      "steps": [
        "Load all data from past week",
        "Compare to historical patterns",
        "Identify trends (improving, stable, concerning)",
        "Generate plain-language summary",
        "Flag items needing attention"
      ]
    }
  },
  
  "memory": {
    "learned_patterns": {
      "blood_pressure": {
        "baseline": "120/80",
        "trend": "stable",
        "last_concerning": "2024-03-15",
        "medication": "Lisinopril 10mg daily"
      },
      "cholesterol": {
        "baseline": "LDL 110, HDL 55",
        "trend": "improving",
        "last_check": "2025-09-15"
      }
    },
    "preferences": {
      "communication_style": "conversational, not clinical",
      "alert_threshold": "conservative",
      "summary_frequency": "weekly_sunday_night"
    },
    "context_summary": {
      "total_records": 47,
      "date_range": "2024-01-15 to 2025-11-10",
      "categories": {
        "lab_results": 23,
        "prescriptions": 12,
        "appointments": 12
      }
    }
  },
  
  "state": {
    "last_analysis_date": "2025-11-10T10:00:00Z",
    "next_scheduled_analysis": "2025-11-17T10:00:00Z",
    "last_email_sent": "2025-11-10T10:05:00Z",
    "pending_alerts": [],
    "processing_queue": []
  }
}
```

**This brain file contains:**
- ✅ Who the customer is
- ✅ What the brain should do
- ✅ How it should behave
- ✅ What it has learned
- ✅ What it remembers
- ✅ Current state

**This brain file does NOT:**
- ❌ Run continuously
- ❌ Store actual medical records (those are in context_index.db)
- ❌ Process things automatically
- ❌ Send emails itself

---

### **How Brain Gets Used**

**Scenario 1: Weekly Analysis (Scheduled)**

```javascript
// Brain daemon runs this every Sunday 10pm
async function runWeeklyAnalysis(customer_id) {
  // 1. Load brain (the intelligence)
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain_transport.json`);
  
  // 2. Load context (the data)
  const db = openDatabase(`~/8825_customers/${customer_id}/context_index.db`);
  const weekData = db.query("SELECT * FROM records WHERE date > DATE('now', '-7 days')");
  
  // 3. Use brain to analyze
  const prompt = `
    You are ${brain.meta.customer_name}'s health analysis brain.
    
    Your purpose: ${brain.philosophy.purpose}
    Your values: ${brain.philosophy.core_values.join(', ')}
    Your constraints: ${brain.philosophy.constraints.join(', ')}
    
    Historical patterns you've learned:
    ${JSON.stringify(brain.memory.learned_patterns, null, 2)}
    
    This week's data:
    ${JSON.stringify(weekData, null, 2)}
    
    Generate a weekly health summary following the workflow:
    ${JSON.stringify(brain.workflows.weekly_health_analysis, null, 2)}
  `;
  
  const analysis = await GPT4.complete(prompt);
  
  // 4. Update brain memory
  brain.memory.learned_patterns = analysis.updated_patterns;
  brain.state.last_analysis_date = new Date();
  
  // 5. Save updated brain
  saveJSON(`~/8825_customers/${customer_id}/brain_transport.json`, brain);
  
  // 6. Send email
  await sendEmail(brain.meta.customer_email, analysis.summary);
  
  return analysis;
}
```

**Scenario 2: Query via Email (On-Demand)**

```javascript
// Customer emails: "What's my blood pressure trend?"
async function handleEmailQuery(customer_id, query) {
  // 1. Load brain
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain_transport.json`);
  
  // 2. Load relevant context
  const db = openDatabase(`~/8825_customers/${customer_id}/context_index.db`);
  const bpData = db.query("SELECT * FROM records WHERE category = 'blood_pressure'");
  
  // 3. Use brain to answer
  const prompt = `
    You are ${brain.meta.customer_name}'s health assistant.
    
    Communication style: ${brain.memory.preferences.communication_style}
    
    What you know about their blood pressure:
    ${JSON.stringify(brain.memory.learned_patterns.blood_pressure, null, 2)}
    
    All blood pressure records:
    ${JSON.stringify(bpData, null, 2)}
    
    Customer question: "${query}"
    
    Provide a clear, conversational answer.
  `;
  
  const answer = await GPT4.complete(prompt);
  
  // 4. Send email response
  await sendEmail(brain.meta.customer_email, answer);
  
  return answer;
}
```

**Scenario 3: You Query via MCP**

```javascript
// In Goose: "Show me PS's blood pressure trend"
// MCP tool gets called:
async function queryHealthData(args) {
  const customer_id = "ps_medical";
  const query = args.query;
  
  // Same as email scenario, but return to Goose instead of email
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain_transport.json`);
  const db = openDatabase(`~/8825_customers/${customer_id}/context_index.db`);
  const data = db.search(query);
  
  const prompt = `
    Brain context: ${JSON.stringify(brain, null, 2)}
    Data: ${JSON.stringify(data, null, 2)}
    Query: ${query}
    
    Provide analysis.
  `;
  
  const result = await GPT4.complete(prompt);
  
  return result; // Goes back to Goose
}
```

---

## Part 3: How They Work Together

### **The Full Stack**

```
┌─────────────────────────────────────────────────────────┐
│                   AI Agent (Goose)                       │
│  "Show me PS's blood pressure trend"                    │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              MCP Server (Interface)                      │
│  Tool: query_health_data                                │
│  Receives: { query: "blood pressure trend" }            │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│           Implementation (Your Code)                     │
│  1. Load brain_transport.json                           │
│  2. Load context_index.db                               │
│  3. Search for blood pressure data                      │
│  4. Use brain + GPT-4 to analyze                        │
│  5. Return formatted result                             │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              File System (Storage)                       │
│  ~/8825_customers/ps_medical/                           │
│  ├── brain_transport.json    ← Intelligence            │
│  ├── context_index.db         ← Data                   │
│  └── logs/                    ← History                │
└─────────────────────────────────────────────────────────┘
```

---

### **Key Insight: Separation of Concerns**

**MCP Server:**
- Exposes tools to AI
- Routes requests
- Returns results
- **Stateless** (no memory between calls)

**Brain Transport:**
- Stores intelligence
- Remembers patterns
- Defines behavior
- **Portable** (just a JSON file)

**Context Database:**
- Stores actual data
- Searchable/queryable
- Historical records
- **Customer-owned**

**Your Implementation:**
- Loads brain when needed
- Queries data when needed
- Processes with GPT-4
- Saves updated brain
- **Does the actual work**

---

## Part 4: Multi-Customer Architecture

### **How You Manage Multiple Customers**

```
Your Infrastructure:

┌─────────────────────────────────────────────────────────┐
│         Single MCP Server (Your Interface)              │
│         ~/mcp_servers/8825-customer-manager/            │
│                                                          │
│  Tools:                                                  │
│  - query_customer(customer_id, query)                   │
│  - run_analysis(customer_id)                            │
│  - list_customers()                                     │
│  - get_status(customer_id)                              │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│      Single Brain Daemon (Scheduler + Processor)        │
│                                                          │
│  Runs every hour:                                       │
│  - Check each customer's schedule                       │
│  - Run analysis if due                                  │
│  - Process email queue                                  │
│  - Send notifications                                   │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│           Customer Storage (Isolated)                    │
│                                                          │
│  ~/8825_customers/                                      │
│  ├── ps_medical/                                        │
│  │   ├── brain_transport.json                          │
│  │   ├── context_index.db                              │
│  │   └── config.json                                   │
│  ├── mes_corporate/                                    │
│  │   ├── brain_transport.json                          │
│  │   ├── context_index.db                              │
│  │   └── config.json                                   │
│  └── joju_user_001/                                    │
│      ├── brain_transport.json                          │
│      ├── context_index.db                              │
│      └── config.json                                   │
└─────────────────────────────────────────────────────────┘
```

---

### **How Isolation Works**

**Each customer folder is completely separate:**

```javascript
// Brain daemon processes each customer independently
async function processAllCustomers() {
  const customers = listCustomers(); // ['ps_medical', 'mes_corporate', 'joju_user_001']
  
  for (const customer_id of customers) {
    // Load THIS customer's brain
    const brain = loadJSON(`~/8825_customers/${customer_id}/brain_transport.json`);
    
    // Check if analysis is due
    if (shouldRunAnalysis(brain)) {
      // Load THIS customer's data
      const db = openDatabase(`~/8825_customers/${customer_id}/context_index.db`);
      
      // Run analysis with THIS customer's brain + data
      const analysis = await runAnalysis(brain, db);
      
      // Save updated brain for THIS customer
      saveJSON(`~/8825_customers/${customer_id}/brain_transport.json`, brain);
      
      // Send email to THIS customer
      await sendEmail(brain.meta.customer_email, analysis);
    }
  }
}
```

**No cross-contamination:**
- PS's brain never sees MES's data
- MES's brain never sees Joju user's data
- Each brain has own memory/patterns
- Each database is separate
- Complete isolation

---

## Part 5: Brain Daemon vs On-Demand

### **Two Ways to Use Brain**

**Option 1: Brain Daemon (Scheduled Tasks)**

```javascript
// Runs continuously in background
// Checks for scheduled tasks
// Processes automatically

// Start daemon
node brain_daemon.js

// Daemon loop
setInterval(async () => {
  const customers = listCustomers();
  
  for (const customer_id of customers) {
    const brain = loadBrain(customer_id);
    
    // Check if weekly analysis is due
    if (isAnalysisDue(brain)) {
      await runWeeklyAnalysis(customer_id);
    }
    
    // Check for pending emails
    if (hasPendingEmails(customer_id)) {
      await processEmails(customer_id);
    }
  }
}, 60000); // Every minute
```

**Option 2: On-Demand (Via MCP)**

```javascript
// No daemon running
// Brain loaded when needed
// Triggered by MCP call

// MCP tool
async function runAnalysisNow(args) {
  const customer_id = args.customer_id;
  
  // Load brain on-demand
  const brain = loadBrain(customer_id);
  const db = loadContext(customer_id);
  
  // Run analysis
  const result = await runAnalysis(brain, db);
  
  // Save updated brain
  saveBrain(customer_id, brain);
  
  return result;
}
```

**Hybrid Approach (Recommended):**
- Daemon handles scheduled tasks (weekly analysis)
- MCP handles on-demand queries (you asking questions)
- Email gateway handles customer queries (they ask questions)

---

## Part 6: Practical Example End-to-End

### **Scenario: PS Gets Lab Results**

**Step 1: PS Forwards Email**
```
From: ps@gmail.com
To: ps@8825.ai
Subject: Lab Results
Attachment: lab_results_2025-11-12.pdf

Here are my latest lab results.
```

**Step 2: Email Gateway Receives**
```javascript
// Email webhook triggered
async function handleIncomingEmail(email) {
  // Identify customer from recipient
  const customer_id = "ps_medical"; // ps@8825.ai → ps_medical
  
  // Extract attachment
  const pdf = email.attachments[0];
  
  // Save to raw folder
  saveFile(`~/8825_customers/ps_medical/raw/lab_results_2025-11-12.pdf`, pdf);
  
  // Trigger processing
  await processNewDocument(customer_id, 'lab_results_2025-11-12.pdf');
}
```

**Step 3: Brain Processes Document**
```javascript
async function processNewDocument(customer_id, filename) {
  // Load brain
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain_transport.json`);
  
  // Load document
  const pdf = readFile(`~/8825_customers/${customer_id}/raw/${filename}`);
  
  // Extract data using brain's workflow
  const prompt = `
    You are processing a medical document for ${brain.meta.customer_name}.
    
    Follow this workflow:
    ${JSON.stringify(brain.workflows.ingest_medical_record, null, 2)}
    
    Document content:
    ${pdf.text}
    
    Extract structured data.
  `;
  
  const extracted = await GPT4.complete(prompt);
  
  // Save to context database
  const db = openDatabase(`~/8825_customers/${customer_id}/context_index.db`);
  db.insert({
    date: extracted.date,
    type: 'lab_result',
    values: extracted.values,
    source: filename
  });
  
  // Check for concerning patterns
  if (extracted.concerning) {
    brain.state.pending_alerts.push(extracted.alert);
  }
  
  // Update brain memory
  brain.memory.context_summary.total_records += 1;
  brain.state.last_updated = new Date();
  
  // Save updated brain
  saveJSON(`~/8825_customers/${customer_id}/brain_transport.json`, brain);
  
  // Send confirmation email
  await sendEmail(brain.meta.customer_email, 
    `Added lab results from ${extracted.date}. ${extracted.concerning ? 'Alert: ' + extracted.alert : 'Everything looks normal.'}`
  );
}
```

**Step 4: Sunday Night Analysis**
```javascript
// Brain daemon runs weekly analysis
async function runWeeklyAnalysis(customer_id) {
  const brain = loadBrain(customer_id);
  const db = loadContext(customer_id);
  
  // Get week's data
  const weekData = db.query("date > DATE('now', '-7 days')");
  
  // Analyze using brain
  const analysis = await GPT4.analyze(brain, weekData);
  
  // Update brain
  brain.memory.learned_patterns = analysis.patterns;
  saveBrain(customer_id, brain);
  
  // Email summary
  await sendEmail(brain.meta.customer_email, `
    Weekly Health Summary - Nov 10-17, 2025
    
    New this week:
    - Lab results from Nov 12 (cholesterol improved!)
    
    Trends:
    - Blood pressure: Stable at 120/80
    - Cholesterol: LDL down to 105 (was 110)
    
    Recommendations:
    - Continue current medications
    - Next checkup in 3 months
  `);
}
```

**Step 5: You Monitor via MCP**
```javascript
// In Goose: "Show me PS's latest analysis"

// MCP tool called
async function getLatestAnalysis(args) {
  const brain = loadBrain('ps_medical');
  const analysis = readFile(`~/8825_customers/ps_medical/processed/weekly_2025-11-17.json`);
  
  return `
    PS's Latest Analysis (Nov 17, 2025):
    
    Status: ${analysis.overall_status}
    New Records: ${analysis.new_records_count}
    Alerts: ${analysis.alerts.length}
    
    Key Findings:
    ${analysis.summary}
  `;
}
```

---

## Part 7: Key Takeaways

### **MCP:**
- ✅ Interface/API for AI agents
- ✅ Exposes tools
- ✅ Routes requests
- ❌ NOT storage
- ❌ NOT processing
- ❌ NOT continuous

### **Brain Transport:**
- ✅ JSON file with intelligence
- ✅ Stores patterns/memory/state
- ✅ Defines behavior/workflows
- ✅ Portable (customer can take it)
- ❌ NOT a running process
- ❌ NOT the data itself

### **Brain Daemon:**
- ✅ Scheduler for automated tasks
- ✅ Loads brains on-demand
- ✅ Processes emails/analysis
- ✅ Saves updated brains
- ❌ NOT required for MCP access
- ❌ NOT storing brain state

### **Customer Storage:**
- ✅ Isolated folders per customer
- ✅ Brain + context + config
- ✅ Customer owns the data
- ✅ Portable/exportable
- ✅ Complete separation

---

## Part 8: Mental Model Summary

**Think of it like this:**

**Customer = Person with their own assistant**
- Brain = The assistant's knowledge/personality
- Context = The assistant's filing cabinet
- Config = The assistant's instructions

**You = Manager of many assistants**
- MCP = Your phone system (talk to any assistant)
- Brain Daemon = Your scheduler (tells assistants when to work)
- Customer folders = Each assistant's office

**AI Agent (Goose) = You calling in**
- MCP shows you which assistants are available
- You ask to talk to PS's assistant
- Assistant loads their brain (knowledge)
- Assistant checks their files (context)
- Assistant gives you answer
- Assistant updates their notes (brain state)

**Customer (PS) = Emailing their assistant**
- Sends email to ps@8825.ai
- Email gateway routes to PS's assistant
- Assistant loads brain + context
- Assistant processes request
- Assistant emails back
- Assistant updates brain

**Each assistant is completely separate:**
- PS's assistant knows about health
- MES's assistant knows about testing
- Joju user's assistant knows about career
- They never talk to each other
- They never see each other's files

---

## Part 9: What You Build

### **Immediate (Week 1):**

**1. Customer Manager MCP**
```
~/mcp_servers/8825-customer-manager/
├── server.js
├── package.json
└── tools/
    ├── query_customer.js
    ├── run_analysis.js
    ├── list_customers.js
    └── get_status.js
```

**2. Brain Daemon**
```
~/8825_brain_daemon/
├── daemon.js              # Main scheduler
├── email_processor.js     # Handle incoming emails
├── analysis_runner.js     # Run weekly analysis
└── brain_loader.js        # Load/save brain transport
```

**3. Customer Template**
```
~/8825_customers/TEMPLATE/
├── brain_transport.json   # Empty brain template
├── context_index.db       # Empty database
├── config.json            # Default config
└── README.md              # Setup instructions
```

### **Test (Week 2):**

**Create PS's instance:**
```bash
cp -r ~/8825_customers/TEMPLATE ~/8825_customers/ps_medical
# Edit brain_transport.json with PS's info
# Configure email routing
# Test with sample medical record
```

**Validate:**
- ✅ Can ingest document via email
- ✅ Brain processes correctly
- ✅ Context database updates
- ✅ Confirmation email sent
- ✅ Weekly analysis runs
- ✅ You can query via MCP

---

## Bottom Line

**MCP = Interface (menu + waiter)**
**Brain = Intelligence (recipe + chef's knowledge)**  
**Context = Data (ingredients)**
**Daemon = Scheduler (kitchen timer)**
**Storage = Files (pantry)**

**You manage multiple kitchens (customers)**
**Each kitchen has own chef (brain) and pantry (context)**
**MCP lets you talk to any kitchen**
**Daemon makes sure kitchens run on schedule**
**Customers order via email, you monitor via MCP**

**Everything is isolated, portable, customer-owned.**

---

Does this mental model click?
