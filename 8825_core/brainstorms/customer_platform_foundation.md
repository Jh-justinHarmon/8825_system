# 8825 Customer Platform: Foundation Design
**Created:** 2025-11-12  
**Purpose:** Define minimal viable foundation that supports future evolution

---

## Core Principle: Start Simple, Enable Complex

**Philosophy:**
- Build the simplest thing that works
- Make it easy to extend later
- Don't build features you don't need yet
- But design interfaces that won't break when you add them

---

## The Absolute Minimum (MVP)

### **What You Actually Need Right Now:**

**1. Customer Storage Structure**
```
~/8825_customers/
└── [customer_id]/
    ├── brain.json              # Customer's intelligence
    ├── context.db              # Customer's data (SQLite)
    ├── config.json             # Customer settings
    └── logs/
        └── activity.log        # What happened when
```

**That's it. Four files.**

---

**2. Brain Format (Minimal)**
```json
{
  "customer_id": "ps_medical",
  "customer_name": "Phillip Sheehan",
  "type": "personal_health",
  "created": "2025-11-12",
  
  "purpose": "Track and analyze personal health data",
  
  "workflows": {
    "ingest": "Extract health data from documents",
    "analyze": "Weekly health trend analysis"
  },
  
  "memory": {},
  
  "state": {
    "last_analysis": null,
    "next_scheduled": null
  }
}
```

**Start empty. Let it grow.**

---

**3. Context Database (SQLite)**
```sql
-- Single table to start
CREATE TABLE records (
  id INTEGER PRIMARY KEY,
  date TEXT,
  type TEXT,
  content TEXT,
  metadata TEXT,  -- JSON blob for flexibility
  created_at TEXT
);

-- Simple index
CREATE INDEX idx_date ON records(date);
CREATE INDEX idx_type ON records(type);
```

**Add tables as needed. Don't over-engineer.**

---

**4. Config (Minimal)**
```json
{
  "customer_id": "ps_medical",
  "email": "ps@8825.ai",
  "schedule": "weekly_sunday_10pm",
  "status": "active"
}
```

**That's all you need to start.**

---

## The Three Core Functions

### **Function 1: Ingest**
```javascript
async function ingest(customer_id, data) {
  // 1. Load brain
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
  
  // 2. Process with GPT-4
  const processed = await GPT4.process(brain, data);
  
  // 3. Save to database
  const db = openDB(`~/8825_customers/${customer_id}/context.db`);
  db.insert(processed);
  
  // 4. Update brain if needed
  if (processed.learned_something) {
    brain.memory = processed.updated_memory;
    saveJSON(`~/8825_customers/${customer_id}/brain.json`, brain);
  }
  
  return processed;
}
```

---

### **Function 2: Query**
```javascript
async function query(customer_id, question) {
  // 1. Load brain
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
  
  // 2. Search context
  const db = openDB(`~/8825_customers/${customer_id}/context.db`);
  const relevant = db.search(question);
  
  // 3. Answer with GPT-4
  const answer = await GPT4.answer(brain, relevant, question);
  
  return answer;
}
```

---

### **Function 3: Analyze**
```javascript
async function analyze(customer_id) {
  // 1. Load brain
  const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
  
  // 2. Get recent data
  const db = openDB(`~/8825_customers/${customer_id}/context.db`);
  const recent = db.query("SELECT * FROM records WHERE date > DATE('now', '-7 days')");
  
  // 3. Analyze with GPT-4
  const analysis = await GPT4.analyze(brain, recent);
  
  // 4. Update brain
  brain.memory = analysis.updated_memory;
  brain.state.last_analysis = new Date();
  saveJSON(`~/8825_customers/${customer_id}/brain.json`, brain);
  
  return analysis;
}
```

---

## How to Expose These Functions

### **Option A: Direct MCP (Simplest)**

```javascript
// Single MCP server with three tools
const tools = [
  {
    name: "ingest_data",
    description: "Add data to customer context",
    inputSchema: {
      customer_id: "string",
      data: "string"
    }
  },
  {
    name: "query_customer",
    description: "Ask customer's brain a question",
    inputSchema: {
      customer_id: "string",
      question: "string"
    }
  },
  {
    name: "analyze_customer",
    description: "Run analysis for customer",
    inputSchema: {
      customer_id: "string"
    }
  }
];

// Implementation
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case "ingest_data":
      return await ingest(args.customer_id, args.data);
    case "query_customer":
      return await query(args.customer_id, args.question);
    case "analyze_customer":
      return await analyze(args.customer_id);
  }
});
```

**That's your entire MCP. Three tools. Done.**

---

### **Option B: Email Gateway (For Customers)**

```javascript
// Receive email webhook
async function handleEmail(email) {
  // Route to customer
  const customer_id = routeEmail(email.to); // ps@8825.ai → ps_medical
  
  // Check if it's a query or data
  if (hasAttachment(email)) {
    // Ingest data
    const result = await ingest(customer_id, email.attachment);
    await sendEmail(email.from, `Added: ${result.summary}`);
  } else {
    // Answer query
    const answer = await query(customer_id, email.body);
    await sendEmail(email.from, answer);
  }
}
```

**That's your entire email interface. One function.**

---

### **Option C: Scheduler (For Automation)**

```javascript
// Run every hour
setInterval(async () => {
  const customers = listCustomers();
  
  for (const customer_id of customers) {
    const config = loadJSON(`~/8825_customers/${customer_id}/config.json`);
    const brain = loadJSON(`~/8825_customers/${customer_id}/brain.json`);
    
    // Check if analysis is due
    if (isDue(brain.state.next_scheduled)) {
      const analysis = await analyze(customer_id);
      await sendEmail(config.email, analysis.summary);
    }
  }
}, 3600000); // Every hour
```

**That's your entire scheduler. One loop.**

---

## Future-Proofing: The Extension Points

### **1. Brain Format Can Evolve**

**Start:**
```json
{
  "memory": {}
}
```

**Later:**
```json
{
  "memory": {
    "patterns": {},
    "preferences": {},
    "learned_facts": {}
  }
}
```

**Your code doesn't break because:**
- You always load the whole brain
- GPT-4 interprets whatever's there
- You can add fields without migration

---

### **2. Database Can Grow**

**Start:**
```sql
CREATE TABLE records (
  id INTEGER PRIMARY KEY,
  date TEXT,
  type TEXT,
  content TEXT,
  metadata TEXT,
  created_at TEXT
);
```

**Later:**
```sql
-- Add new tables
CREATE TABLE health_metrics (
  id INTEGER PRIMARY KEY,
  record_id INTEGER,
  metric_name TEXT,
  value REAL,
  unit TEXT
);

-- Add new indexes
CREATE INDEX idx_metric ON health_metrics(metric_name);
```

**Your code doesn't break because:**
- Old queries still work
- New code can use new tables
- SQLite handles schema evolution

---

### **3. Tools Can Expand**

**Start:**
```javascript
const tools = [
  "ingest_data",
  "query_customer",
  "analyze_customer"
];
```

**Later:**
```javascript
const tools = [
  "ingest_data",
  "query_customer",
  "analyze_customer",
  "export_data",        // New
  "share_context",      // New
  "set_preferences",    // New
  "get_insights"        // New
];
```

**Your code doesn't break because:**
- MCP clients discover tools dynamically
- Old tools keep working
- New tools are additive

---

### **4. Workflows Can Be Added**

**Start:**
```json
{
  "workflows": {
    "ingest": "Extract health data",
    "analyze": "Weekly analysis"
  }
}
```

**Later:**
```json
{
  "workflows": {
    "ingest": "Extract health data",
    "analyze": "Weekly analysis",
    "predict": "Forecast health trends",
    "recommend": "Suggest interventions",
    "alert": "Detect concerning patterns"
  }
}
```

**Your code doesn't break because:**
- Brain defines its own workflows
- GPT-4 interprets them
- You can add without changing code

---

## What NOT to Build Yet

### **Don't Build:**

**❌ User authentication system**
- Use email allowlist for now
- Add auth when you have paying customers

**❌ Web UI**
- Email works fine
- Build UI when customers ask for it

**❌ Complex permissions**
- One customer = one brain = full access
- Add permissions when you have teams

**❌ Multi-tenant database**
- Separate SQLite per customer is fine
- Move to Postgres when you have 100+ customers

**❌ Real-time sync**
- Hourly checks are fine
- Add websockets when customers need it

**❌ Advanced analytics**
- Weekly summary is enough
- Add dashboards when customers ask

**❌ Mobile app**
- Email works on mobile
- Build app when you have revenue

**❌ API versioning**
- You're the only user
- Add versions when you have external devs

**❌ Backup system**
- Dropbox already backs up
- Add dedicated backups at scale

**❌ Monitoring/alerting**
- Check logs manually
- Add monitoring when you can't keep up

---

## The Tight Scope: Week 1 Build

### **Day 1-2: Core Functions**
```javascript
// lib/core.js
async function ingest(customer_id, data) { ... }
async function query(customer_id, question) { ... }
async function analyze(customer_id) { ... }

// lib/storage.js
function loadBrain(customer_id) { ... }
function saveBrain(customer_id, brain) { ... }
function openDB(customer_id) { ... }

// lib/gpt.js
async function process(brain, data) { ... }
async function answer(brain, context, question) { ... }
async function analyze(brain, data) { ... }
```

**~200 lines of code**

---

### **Day 3: MCP Server**
```javascript
// mcp_server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { ingest, query, analyze } from './lib/core.js';

const server = new Server({ name: "8825-customer-manager" });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: "ingest_data", ... },
    { name: "query_customer", ... },
    { name: "analyze_customer", ... }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Route to core functions
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

**~100 lines of code**

---

### **Day 4: Email Gateway**
```javascript
// email_gateway.js
import { ingest, query } from './lib/core.js';
import { sendEmail } from './lib/email.js';

export async function handleWebhook(req, res) {
  const email = parseEmail(req.body);
  const customer_id = routeEmail(email.to);
  
  if (hasAttachment(email)) {
    const result = await ingest(customer_id, email.attachment);
    await sendEmail(email.from, `Added: ${result.summary}`);
  } else {
    const answer = await query(customer_id, email.body);
    await sendEmail(email.from, answer);
  }
  
  res.status(200).send('OK');
}
```

**~50 lines of code**

---

### **Day 5: Scheduler**
```javascript
// scheduler.js
import { analyze } from './lib/core.js';
import { sendEmail } from './lib/email.js';

setInterval(async () => {
  const customers = listCustomers();
  
  for (const customer_id of customers) {
    const config = loadConfig(customer_id);
    const brain = loadBrain(customer_id);
    
    if (isDue(brain.state.next_scheduled)) {
      const analysis = await analyze(customer_id);
      await sendEmail(config.email, analysis.summary);
      
      brain.state.last_analysis = new Date();
      brain.state.next_scheduled = getNextSchedule(config.schedule);
      saveBrain(customer_id, brain);
    }
  }
}, 3600000);
```

**~50 lines of code**

---

### **Day 6-7: Test with PS**
```bash
# Create customer
mkdir -p ~/8825_customers/ps_medical/{logs}

# Initialize brain
cat > ~/8825_customers/ps_medical/brain.json << EOF
{
  "customer_id": "ps_medical",
  "customer_name": "Phillip Sheehan",
  "type": "personal_health",
  "purpose": "Track and analyze personal health data",
  "workflows": {
    "ingest": "Extract health data from documents",
    "analyze": "Weekly health trend analysis"
  },
  "memory": {},
  "state": {
    "last_analysis": null,
    "next_scheduled": "2025-11-17T22:00:00Z"
  }
}
EOF

# Initialize database
sqlite3 ~/8825_customers/ps_medical/context.db << EOF
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
cat > ~/8825_customers/ps_medical/config.json << EOF
{
  "customer_id": "ps_medical",
  "email": "ps@8825.ai",
  "schedule": "weekly_sunday_10pm",
  "status": "active"
}
EOF

# Test ingest via MCP
# In Goose: "Ingest this lab result for ps_medical: [data]"

# Test query via MCP
# In Goose: "Query ps_medical: What's my blood pressure trend?"

# Test analysis via scheduler
# Wait for Sunday 10pm or trigger manually
```

---

## Total Code: ~400 Lines

**Breakdown:**
- Core functions: 200 lines
- MCP server: 100 lines
- Email gateway: 50 lines
- Scheduler: 50 lines

**That's it. That's the entire platform.**

---

## Extension Strategy

### **When to Add Features:**

**Add when you have 3+ customers asking for it**
- Not when you think it's cool
- Not when it's "best practice"
- When actual customers need it

**Examples:**

**Customer asks: "Can I export my data?"**
→ Add export tool (1 hour)

**Customer asks: "Can I share with my doctor?"**
→ Add sharing feature (4 hours)

**Customer asks: "Can I see trends over time?"**
→ Add visualization (8 hours)

**Customer asks: "Can I access on my phone?"**
→ Build mobile-friendly web view (2 weeks)

**Customer asks: "Can my team use this?"**
→ Add multi-user support (4 weeks)

---

## The Foundation Checklist

### **Strong Foundation Means:**

**✅ Simple to understand**
- Three core functions
- Four files per customer
- One MCP server
- One scheduler

**✅ Easy to extend**
- Brain format is flexible JSON
- Database can add tables
- MCP can add tools
- Workflows can be added

**✅ Hard to break**
- Each customer isolated
- No shared state
- SQLite is bulletproof
- JSON is human-readable

**✅ Customer-owned**
- Data in their folder
- Brain is portable
- Can export anytime
- Can delete anytime

**✅ You can manage it**
- Single MCP to monitor all
- Logs show what happened
- Can query any customer
- Can trigger analysis manually

**✅ Scales to 100 customers**
- Separate folders scale fine
- SQLite handles it
- Scheduler loops through all
- MCP routes correctly

**✅ Doesn't scale to 10,000 (yet)**
- That's fine
- You'll know what to change by then
- Don't optimize prematurely

---

## Alternative Ideas to Consider

### **Idea 1: Brain as Code Instead of JSON**

**Instead of:**
```json
{
  "workflows": {
    "ingest": "Extract health data"
  }
}
```

**Use:**
```javascript
// ~/8825_customers/ps_medical/brain.js
export const workflows = {
  async ingest(data) {
    // Custom logic for PS
    const extracted = extractHealthData(data);
    return extracted;
  }
};
```

**Pros:**
- More powerful (real code)
- Customer can customize
- Type-safe

**Cons:**
- Security risk (executing customer code)
- Harder to port
- More complex

**Verdict:** Stick with JSON for now, consider later for power users

---

### **Idea 2: Event-Driven Instead of Polling**

**Instead of:**
```javascript
setInterval(() => {
  checkAllCustomers();
}, 3600000);
```

**Use:**
```javascript
// Emit events
eventBus.on('data_ingested', (customer_id) => {
  checkForPatterns(customer_id);
});

eventBus.on('schedule_due', (customer_id) => {
  runAnalysis(customer_id);
});
```

**Pros:**
- More responsive
- More efficient
- More scalable

**Cons:**
- More complex
- Harder to debug
- Overkill for 10 customers

**Verdict:** Stick with polling for now, add events at 50+ customers

---

### **Idea 3: Streaming Instead of Batch**

**Instead of:**
```javascript
const analysis = await analyze(customer_id);
sendEmail(config.email, analysis.summary);
```

**Use:**
```javascript
const stream = analyzeStream(customer_id);
for await (const chunk of stream) {
  sendEmailChunk(config.email, chunk);
}
```

**Pros:**
- Faster perceived response
- Better UX for long analysis
- More modern

**Cons:**
- More complex
- Email doesn't support streaming well
- Overkill for weekly summaries

**Verdict:** Stick with batch for now, add streaming if building web UI

---

### **Idea 4: Multi-Model Instead of GPT-4 Only**

**Instead of:**
```javascript
const result = await GPT4.process(brain, data);
```

**Use:**
```javascript
const result = await ModelRouter.process(brain, data, {
  simple_extraction: 'gpt-4o-mini',
  complex_analysis: 'gpt-4',
  medical_specific: 'claude-3-opus'
});
```

**Pros:**
- Cost optimization
- Best model for each task
- Redundancy

**Cons:**
- More complex
- More API keys
- Harder to debug

**Verdict:** Stick with GPT-4 for now, add routing when cost matters

---

### **Idea 5: Blockchain for Data Integrity**

**Just kidding. Never do this.**

---

## The Decision Framework

### **For Every Feature Idea, Ask:**

**1. Does it solve a real customer problem?**
- Not "might be useful"
- Actual customer said "I need this"

**2. Can I build it in < 1 week?**
- If yes, consider it
- If no, break it down or defer

**3. Does it make the foundation more complex?**
- If yes, defer unless critical
- If no, consider it

**4. Can I remove it later if it doesn't work?**
- If yes, safer to try
- If no, be very careful

**5. Will it break existing customers?**
- If yes, don't do it
- If no, safe to add

---

## The Foundation You're Building

```
Week 1: Core Platform
├── Three functions (ingest, query, analyze)
├── Four files per customer (brain, context, config, logs)
├── One MCP server (your interface)
├── One scheduler (automation)
└── One email gateway (customer interface)

Week 2: First Customer (PS)
├── Test ingestion
├── Test queries
├── Test analysis
├── Validate isolation
└── Prove value

Week 3-4: Second Customer (MES)
├── Reuse platform
├── Different data type
├── Validate template
└── Refine process

Week 5-6: Third Customer (Joju)
├── Reuse platform
├── Different use case
├── Validate scalability
└── Prove model

Week 7-8: Refinement
├── Fix bugs
├── Improve UX
├── Add requested features
└── Prepare for scale
```

---

## Bottom Line

**Start with:**
- 400 lines of code
- Three core functions
- Four files per customer
- One week of building

**Enables:**
- Unlimited customers (up to ~100)
- Unlimited data per customer
- Unlimited customization (via brain)
- Unlimited extension (via tools)

**Prevents:**
- Over-engineering
- Premature optimization
- Feature creep
- Complexity debt

**Foundation is strong when:**
- You can explain it in 5 minutes
- New customer setup takes 5 minutes
- Adding features doesn't break existing
- Customers own their data completely

---

**This is the foundation. Simple, extensible, customer-owned.**

Ready to build it?
