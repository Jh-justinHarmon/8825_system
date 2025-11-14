# 8825 Customer Onboarding Architecture
**Created:** 2025-11-12  
**Status:** Brainstorm - Packaging Model Design

---

## Core Question
How do we package 8825 to onboard customers when:
- Each entity needs its own context engine (MCP)
- No UI exists (relying on existing software)
- All work done through IDEs (Windsurf)
- Need to sandbox contexts for proof-of-concept

---

## Use Cases Identified

### 1. **PS (Phillip Sheehan) - Medical Records**
- **Type:** Personal health context
- **Data:** Medical records, appointments, prescriptions, health history
- **Access:** PS-only initially, potentially shared with providers
- **Brain:** Weekly health analysis, appointment prep, medication tracking

### 2. **MES (Mary Sheehan) - Corporate Testing**
- **Type:** Professional/corporate context
- **Data:** Testing protocols, results, compliance docs, workflows
- **Access:** MES-only initially, team access later
- **Brain:** Weekly testing summaries, compliance checks, trend analysis

### 3. **Joju Profiles - User Profiles**
- **Type:** Professional library management
- **Data:** Achievements, variations, professional content
- **Access:** User-specific, user-controlled
- **Brain:** Profile optimization, content suggestions, library maintenance

### 4. **Team Versions (RAL + more)**
- **Type:** Team collaboration contexts
- **Data:** Shared workflows, team knowledge, project data
- **Access:** Team-wide with role-based permissions
- **Brain:** Team analytics, workflow optimization, knowledge synthesis

---

## Architectural Model

### **Each Entity = One MCP Server**

```
Customer Entity
    ↓
Dedicated MCP Server (interface)
    ↓
Personal Brain Instance (intelligence)
    ↓
Context Engine (data + workflows)
    ↓
User's Cloud Storage (data sovereignty)
```

### **Access Control Evolution**

**Phase 1 (Proof of Concept):**
- You monitor all MCPs
- User-specific data in separate sandboxes
- Read-only access for you to validate

**Phase 2 (Production):**
- User-controlled MCPs
- You have no access unless invited
- User manages their own brain

---

## Packaging Components

### **1. Core 8825 Shell (Starter Kit)**

**What's Included:**
- `8825_core.json` (sanitized, no personal data)
- `8825_master_brain.json` (generic version)
- Empty focus template
- Create focus protocol
- Standard workflows (mining, dedup, decision-making)
- Agent recipes (mining, decision, learning)
- Setup guide
- Philosophy documentation

**What's NOT Included:**
- Personal data
- Existing project libraries (joju, hcss, etc.)
- User-specific preferences
- API keys or credentials

**Purpose:** Clean slate for new users to build their own context

---

### **2. MCP Server Template**

**Each customer gets:**
```
~/mcp_servers/[customer_name]/
├── server.js                    # MCP interface
├── package.json                 # Dependencies
├── README.md                    # Setup instructions
├── .env.template                # Config template
└── tools/
    ├── ingest.js               # Data ingestion
    ├── query.js                # Context queries
    ├── analyze.js              # Brain analysis
    └── update.js               # Context updates
```

**Tools Provided:**
- `ingest` - Add data to context
- `query` - Search context
- `analyze` - Weekly brain analysis
- `update` - Modify context (user-controlled)
- `status` - Check system health

**Tools NOT Provided:**
- Philosophy modification
- Core structure changes
- Agent capability changes (until protocol defined)

---

### **3. Personal Brain Instance**

**Each entity gets:**
```
~/.8825/[entity_name]/
├── brain_state.json            # Brain memory
├── context_index.db            # Searchable context
├── weekly_analysis/            # Analysis reports
├── logs/                       # Activity logs
└── config/
    ├── philosophy.json         # Read-only (from starter kit)
    ├── workflows.json          # Customizable
    └── preferences.json        # User-controlled
```

**Brain Capabilities:**
- Weekly check-in/analysis
- Context updates via MCP
- Ingestion engine access
- Query and search
- Pattern recognition

**Brain Restrictions:**
- Cannot modify philosophy
- Cannot change core structure
- Cannot access other entities' data
- Cannot modify agent capabilities (until protocol defined)

---

### **4. Focus Sandbox (Context Engine)**

**Each entity gets a dedicated focus:**
```
/[entity_name]_sandbox/
├── raw/                        # Incoming data
├── processed/                  # Analyzed data
├── output/                     # Generated insights
├── archives/                   # Historical data
├── logs/                       # Activity logs
└── README.md                   # Usage guide
```

**Master File:**
```json
{
  "meta": {
    "entity_name": "PS",
    "entity_type": "personal_health",
    "owner": "Phillip Sheehan",
    "created": "2025-11-12",
    "version": "1.0.0"
  },
  "data": {
    // Entity-specific data structure
  },
  "sessions": [],
  "config": {
    "privacy": "private",
    "sharing": "owner_only",
    "brain_frequency": "weekly"
  }
}
```

---

## Onboarding Process

### **Phase 1: White Glove Service (Initial Customers)**

**Step 1: Discovery (1 hour)**
- Interview customer
- Understand use case
- Define data types
- Identify workflows
- Set expectations

**Step 2: Setup (2 hours)**
- Create MCP server
- Initialize brain instance
- Set up focus sandbox
- Configure workflows
- Test ingestion

**Step 3: Training (1 hour)**
- Show how to use MCP tools
- Demonstrate weekly analysis
- Explain data sovereignty
- Walk through workflows
- Answer questions

**Step 4: Validation (1 week)**
- Customer uses system
- You monitor (read-only)
- Weekly check-in
- Adjust as needed
- Prove value

**Step 5: Handoff (1 hour)**
- Transfer full control
- Remove your access
- Provide support docs
- Set up support channel
- Celebrate launch

**Total Time:** ~5 hours + 1 week validation

---

### **Phase 2: Self-Service (Scale)**

**Future state (not now):**
- Web-based setup wizard
- Automated MCP generation
- Pre-built templates
- Video tutorials
- Community support

**Not worrying about this yet - focus on white glove to prove model**

---

## Technical Challenges & Solutions

### **Challenge 1: No UI, Only IDE Access**

**Problem:** All work done through Windsurf, customers may not have IDE access

**Solutions:**
1. **MCP via Goose** - Customers use Goose CLI to interact with their MCP
2. **ChatGPT Desktop** - MCP support coming, customers use ChatGPT
3. **Claude Desktop** - Already supports MCP, customers use Claude
4. **Simple CLI** - Provide basic terminal commands for non-technical users

**Recommendation:** Start with Goose (you're familiar) + ChatGPT Desktop (most accessible)

---

### **Challenge 2: Creating Context Outside IDE**

**Problem:** How do customers add data without IDE?

**Solutions:**
1. **Email Ingestion** - Forward emails to special address, auto-ingested
2. **Folder Watch** - Drop files in folder, auto-processed
3. **Web Upload** - Simple web form (future)
4. **API Endpoint** - POST data directly (technical users)

**Recommendation:** Start with folder watch (simplest, no infrastructure)

---

### **Challenge 3: Sandboxing for Proof of Concept**

**Problem:** Need to prove value before full deployment

**Solutions:**
1. **Separate MCP per entity** - Already planned
2. **Read-only monitoring** - You can observe, not modify
3. **Isolated storage** - Each entity in own folder
4. **Clear boundaries** - Document what you can/can't access

**Recommendation:** Use separate MCP + isolated storage + monitoring dashboard

---

### **Challenge 4: Weekly Brain Analysis Without Manual Trigger**

**Problem:** Brain should run weekly automatically

**Solutions:**
1. **Cron Job** - Schedule weekly analysis script
2. **Brain Daemon** - Already built, add weekly trigger
3. **MCP Tool** - Customer triggers manually (fallback)
4. **Email Report** - Send analysis via email automatically

**Recommendation:** Extend brain daemon with weekly scheduler + email reports

---

## Data Sovereignty Model

### **Core Principle: User Controls Their Data**

**What This Means:**
- Data lives in user's cloud storage (Dropbox, iCloud, etc.)
- User can delete everything anytime
- User controls who has access
- User owns the MCP server
- User can export all data

**Your Access:**
- **Phase 1 (PoC):** Read-only monitoring with explicit permission
- **Phase 2 (Production):** No access unless user invites you
- **Support:** User shares specific logs/data when requesting help

**Implementation:**
```
User's Cloud Storage
├── .8825/
│   └── [entity_name]/          # User owns this
│       ├── brain_state.json
│       ├── context_index.db
│       └── logs/
└── mcp_servers/
    └── [entity_name]/          # User owns this
        └── server.js
```

---

## Pricing Model (Future Consideration)

**Not defining now, but thinking ahead:**

### **Option 1: Per-Entity Subscription**
- $X/month per entity
- Includes brain, MCP, storage
- Weekly analysis included

### **Option 2: Usage-Based**
- Free tier (basic features)
- Pay for brain analysis
- Pay for advanced features

### **Option 3: White Label**
- Sell to organizations
- They deploy for their users
- You provide infrastructure

**Recommendation:** Start with white glove service, figure out pricing after proving value

---

## Next Steps

### **Immediate (This Week)**

1. **Create Starter Kit Package**
   - Sanitize 8825_core.json
   - Create generic master_brain.json
   - Write setup guide
   - Document philosophy

2. **Build MCP Template**
   - Generic MCP server structure
   - Standard tools (ingest, query, analyze, update)
   - Configuration template
   - README with setup instructions

3. **Extend Brain Daemon**
   - Add weekly scheduler
   - Add email reporting
   - Add per-entity isolation
   - Test with dummy data

4. **Create Monitoring Dashboard**
   - Simple CLI tool to check all MCPs
   - Status overview
   - Error alerts
   - Usage stats

### **Short Term (Next 2 Weeks)**

5. **Test with First Customer (PS)**
   - Set up medical records focus
   - Configure weekly health analysis
   - Test ingestion workflows
   - Validate privacy controls

6. **Document Onboarding Process**
   - Step-by-step guide
   - Common issues & solutions
   - Support procedures
   - Handoff checklist

7. **Build Second Customer (MES)**
   - Corporate testing focus
   - Different data types
   - Validate template reusability
   - Refine process

### **Medium Term (Next Month)**

8. **Refine Based on Learnings**
   - Update starter kit
   - Improve MCP template
   - Enhance brain capabilities
   - Streamline onboarding

9. **Create Joju Profile Version**
   - User profile management
   - Professional library focus
   - Test with existing Joju users
   - Validate team version

10. **Build Team Version (RAL)**
    - Multi-user access
    - Role-based permissions
    - Shared context
    - Collaboration features

---

## Open Questions

### **Technical**
1. How do we handle MCP updates? (Auto-update vs manual)
2. What's the backup strategy for user data?
3. How do we version control customer configurations?
4. What's the disaster recovery plan?

### **Business**
1. What's the minimum viable feature set for PoC?
2. How do we measure success in validation phase?
3. What's the support model after handoff?
4. When do we start charging?

### **Product**
1. What features are core vs nice-to-have?
2. How customizable should workflows be?
3. What's the balance between flexibility and simplicity?
4. When do we build the UI?

---

## Key Insights

### **What We Know:**
1. **MCP per entity works** - Already proven with existing MCPs
2. **Brain daemon is ready** - Just needs weekly scheduler
3. **Focus system is solid** - Create focus protocol exists
4. **Data sovereignty is critical** - User must own their data

### **What We Need to Figure Out:**
1. **Ingestion without IDE** - Folder watch? Email? API?
2. **Non-technical user access** - CLI? ChatGPT? Web?
3. **Monitoring without intrusion** - Dashboard? Logs? Reports?
4. **Scaling beyond white glove** - Templates? Automation? Self-service?

### **What We're NOT Worrying About Yet:**
1. UI/web interface
2. Pricing model
3. Marketing/sales
4. Scale infrastructure
5. Mobile apps

---

## Success Criteria

### **Phase 1 Success = Prove the Model**

**For PS (Medical Records):**
- ✅ Can ingest medical records without manual work
- ✅ Weekly health analysis provides value
- ✅ PS feels in control of his data
- ✅ System runs reliably for 4 weeks
- ✅ PS would pay for this

**For MES (Corporate Testing):**
- ✅ Can handle different data types
- ✅ Weekly testing summaries are useful
- ✅ Compliance tracking works
- ✅ Template was reusable (not custom build)
- ✅ MES would pay for this

**For Joju Profiles:**
- ✅ User profile management works
- ✅ Library optimization provides value
- ✅ Users adopt the system
- ✅ Team version is feasible
- ✅ Users would pay for this

**If all three succeed → Model is proven → Scale**

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     8825 Customer Platform                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────────────────────┐
                              │                                 │
                    ┌─────────▼─────────┐           ┌──────────▼─────────┐
                    │   PS (Medical)    │           │  MES (Corporate)   │
                    │   MCP Server      │           │   MCP Server       │
                    └─────────┬─────────┘           └──────────┬─────────┘
                              │                                 │
                    ┌─────────▼─────────┐           ┌──────────▼─────────┐
                    │  Personal Brain   │           │  Corporate Brain   │
                    │  (Weekly Health)  │           │  (Weekly Testing)  │
                    └─────────┬─────────┘           └──────────┬─────────┘
                              │                                 │
                    ┌─────────▼─────────┐           ┌──────────▼─────────┐
                    │  PS Sandbox       │           │  MES Sandbox       │
                    │  (Medical Data)   │           │  (Testing Data)    │
                    └─────────┬─────────┘           └──────────┬─────────┘
                              │                                 │
                    ┌─────────▼─────────┐           ┌──────────▼─────────┐
                    │  PS Cloud Storage │           │  MES Cloud Storage │
                    │  (User Owned)     │           │  (User Owned)      │
                    └───────────────────┘           └────────────────────┘

                              │
                    ┌─────────▼─────────┐
                    │  Monitoring       │
                    │  Dashboard        │
                    │  (Your Access)    │
                    └───────────────────┘
```

---

## Bottom Line

**The Model:**
- Each customer entity = dedicated MCP + brain + sandbox
- Data lives in user's cloud storage (sovereignty)
- Brain runs weekly analysis automatically
- You monitor during PoC, then hand off control
- White glove service to start, self-service later

**The Path:**
1. Build starter kit + MCP template + monitoring (this week)
2. Test with PS medical records (2 weeks)
3. Test with MES corporate testing (2 weeks)
4. Test with Joju profiles (2 weeks)
5. Refine and scale

**The Goal:**
Prove that 8825 context engines provide enough value that customers will pay for them.

**The Timeline:**
6-8 weeks to prove model with 3 customers.

---

**Ready to build the starter kit?**
