# 8825 v3.0 - Full Scope Teaching Document

**Date:** 2025-11-09  
**Version:** 3.0.0  
**Status:** Production Ready  
**Purpose:** Complete system overview for understanding the full scope

---

## 🎯 WHAT IS 8825?

**8825** is a **personal knowledge management and automation system** that:
- Ingests data from multiple sources (Gmail, Otter.ai, files)
- Extracts structured information using AI
- Routes content to appropriate projects/focuses
- Tracks decisions, actions, and knowledge
- Automates workflows and reporting

**Think of it as:** Your personal AI-powered project management and knowledge assistant

---

## 📁 SYSTEM ARCHITECTURE

### **High-Level Structure:**

```
8825 v3.0/
├── 8825_core/              # Shareable system (no user data)
├── 8825_index/             # Fast search layer
├── users/                  # Private user data
├── focuses/                # Active workspaces (symlinks)
└── INBOX_HUB/              # Centralized input processing
```

---

## 🏗️ CORE COMPONENTS

### **1. 8825_core/ - The Brain**

**What:** Shareable system code and configuration  
**Contains:**
- **system/** - Core configuration (15 files)
- **protocols/** - 17 protocols (rules and workflows)
- **agents/** - 5 agent types (automation workers)
- **workflows/** - 33 workflows (processes)
- **integrations/** - 62 integration files (APIs, services)
- **mcp/** - 10 MCP server files (ChatGPT integration)
- **explorations/** - 22 exploration files (ideas being tested)
- **philosophy/** - 6 philosophy docs (principles)
- **poc/** - 13 PoC files (proof of concepts)
- **projects/** - 16 project files (active work)

**Key Principle:** No user data here - 100% shareable

---

### **2. 8825_index/ - The Search Engine**

**What:** Fast discovery layer  
**Contains:**
- `master_index.json` - All files indexed
- `concept_index.json` - Cross-focus concepts
- `refs_graph.json` - Knowledge graph

**Performance:** <1 second searches (2.3ms average)

---

### **3. users/ - Your Private Data**

**What:** User-specific data and credentials  
**Structure:**
```
users/justin_harmon/
├── profile.json            # User profile
├── .env                    # Credentials (NOT committed)
├── joju/                   # Joju focus data
├── hcss/                   # HCSS focus data
└── jh_assistant/           # JH assistant data
```

**Key Principle:** Private, never shared

---

### **4. focuses/ - Active Workspaces**

**What:** Symlinked workspaces for active work  
**Structure:**
```
focuses/
├── joju@ → users/justin_harmon/joju/
├── hcss@ → users/justin_harmon/hcss/
└── jh_assistant@ → users/justin_harmon/jh_assistant/
```

**How it works:** Work in `focuses/`, data stored in `users/`

---

### **5. INBOX_HUB/ - Central Input Processing**

**What:** Centralized location for all incoming data  
**Contains:**
- Raw emails
- Otter transcripts
- Attachments
- Processing logs

**Flow:** Input → Process → Route → Archive

---

## 🎭 FOCUSES (Projects)

### **What is a Focus?**
A **focus** is a project-specific workspace with its own:
- Data
- Workflows
- Agents
- Configuration

### **Current Focuses:**

#### **1. Joju Focus** 📚
**Purpose:** Professional library management  
**Location:** `focuses/joju/`  
**What it does:**
- Manages legal research library
- Tracks books, articles, citations
- Generates bibliographies
- 6 workflow variations

**Key Files:**
- `JH_master_library.json` - Master library
- `joju_sandbox/` - Working area

---

#### **2. HCSS Focus** 🏗️
**Purpose:** HCSS project management  
**Location:** `focuses/hcss/`  
**What it does:**
- Manages HCSS, RAL, TGIF projects
- Ingests Gmail and Otter transcripts
- Routes content to appropriate projects
- Tracks governance and rollouts

**Sub-Projects:**
- **HCSS** - Main construction software project
- **RAL** - Release governance
- **TGIF** - Store rollout automation

**Key Workflows:**
- Email/Otter ingestion
- Content mining
- Intelligent routing
- Weekly rollups

---

#### **3. JH Assistant Focus** 🤖
**Purpose:** Personal assistant automation  
**Location:** `focuses/jh_assistant/`  
**What it does:**
- Weekend soccer advisor
- Bill tracking (Phil's Ledger)
- Personal task management
- Automated reminders

---

## 🔄 CORE WORKFLOWS

### **1. Ingestion Workflow**

```
Input Sources (Gmail, Otter, Files)
    ↓
INBOX_HUB (centralized collection)
    ↓
Raw Content Storage
    ↓
Mining (extract structured data)
    ↓
Routing (send to appropriate focus)
    ↓
Archive
```

**Example:**
1. Email arrives about TGIF rollout
2. Saved to INBOX_HUB
3. Mining agent extracts: decisions, actions, risks
4. Router sends to `focuses/hcss/routed/tgif/`
5. Original archived

---

### **2. Mining Workflow**

```
Raw Content (email, transcript, document)
    ↓
Chat Mining Agent (AI extraction)
    ↓
Structured Output (JSON)
    ↓
Contains:
- Key topics
- Decisions made
- Action items
- Risks/blockers
- Participants
- Confidence scores
```

**Example Output:**
```json
{
  "decisions": [
    {
      "decision": "Launch TGIF in Dallas first",
      "confidence": 0.95,
      "context": "Dallas has best infrastructure"
    }
  ],
  "actions": [
    {
      "action": "Schedule Dallas training",
      "owner": "Justin",
      "due_date": "2025-11-15"
    }
  ]
}
```

---

### **3. Routing Workflow**

```
Mined Content
    ↓
Router Agent (keyword scoring)
    ↓
Score against each focus:
- HCSS keywords: construction, software
- RAL keywords: release, governance, bug
- TGIF keywords: rollout, store, pricing
    ↓
Route to highest score (if confidence > 0.8)
    ↓
Flag for review (if confidence < 0.8)
```

---

## 🤖 AGENTS (Automation Workers)

### **What is an Agent?**
An **agent** is an automated worker that performs specific tasks

### **Core Agents:**

#### **1. EmailRouterAgent**
**Purpose:** Route content to correct focus  
**Inputs:** Mined content, routing rules  
**Outputs:** Routed files, confidence scores  
**Algorithm:** Keyword scoring with negative filters

#### **2. ChatMiningAgent**
**Purpose:** Extract structured data from text  
**Inputs:** Raw text (emails, transcripts)  
**Outputs:** JSON with decisions, actions, topics  
**Uses:** AI/LLM for extraction

#### **3. DeduplicationAgent**
**Purpose:** Prevent duplicate processing  
**Inputs:** Content hash, processed tracker  
**Outputs:** Duplicate flag (yes/no)  
**Method:** SHA-256 hashing

#### **4. TaskTrackerAgent**
**Purpose:** Manage action items  
**Inputs:** Actions from mining  
**Outputs:** Task list, overdue alerts  
**Features:** Owner assignment, due dates, status

#### **5. NotificationAgent**
**Purpose:** Send alerts and reports  
**Inputs:** Events, schedules  
**Outputs:** Emails, summaries  
**Triggers:** Overdue tasks, weekly rollups

---

## 📋 PROTOCOLS (Rules & Workflows)

### **What is a Protocol?**
A **protocol** is a documented rule or workflow that defines how something should be done

### **Key Protocols:**

#### **1. Decision-Making Protocol**
**Formula:** `(intent × 0.4) + (stakes × 0.3) + (efficiency × 0.2) + (reversibility × 0.1)`  
**Purpose:** Consistent decision-making  
**Example:** Should we build Feature X now or later?

#### **2. Learning Protocol**
**Flow:** Observe → Adapt → Log → Update  
**Purpose:** Continuous improvement  
**Example:** Email routing accuracy improves over time

#### **3. Mining Protocol**
**Flow:** Two-stage (external LLM generates, Windsurf extracts)  
**Purpose:** Extract structured data from unstructured text  
**Example:** Email → JSON with decisions/actions

#### **4. HCSS Focus Protocol**
**File:** `8825_core/protocols/8825_hcss_focus.json`  
**Purpose:** Define HCSS focus behavior  
**Contains:**
- Activation rules
- Workflows
- Routing logic
- Commands

#### **5. REF → ARCHV Lifecycle**
**Flow:** Reference → Archive  
**Purpose:** Content lifecycle management  
**Example:** Active email → Processed → Archived

---

## 🚀 CURRENT ACTIVE WORK

### **1. TGIF Automation (PoC Phase)**

**Location:** `8825_core/poc/projects/tgif_automation/`  
**Status:** Built, ready for validation  
**Purpose:** Automate TGIF meeting summaries and weekly rollups

**Components:**
- Daily email processing (12pm)
- Weekly rollup generation (Friday 3pm)
- Task tracking
- Stakeholder notifications

**Infrastructure Used:**
- Otter integration (meeting transcripts)
- Gmail integration (flagged emails)
- Task tracking system

**Next:** Validate with real data

---

### **2. Infrastructure Components (PoC Phase)**

**Location:** `8825_core/poc/infrastructure/`  
**Status:** Extracted from TGIF, reusable

**Components:**

#### **A. Otter Integration**
- Otter MCP server
- Gmail fallback
- Health monitoring
- **Reusable by:** Any meeting-based project

#### **B. Task Tracking**
- Task CRUD operations
- Overdue detection
- Owner assignment
- **Reusable by:** Any action-tracking project

#### **C. Gmail Integration** (future)
- OAuth authentication
- Email search/retrieval
- Label filtering
- **Reusable by:** Any email-based project

---

### **3. Explorations (Ideas Being Tested)**

**Location:** `8825_core/explorations/features/`  
**Status:** 6 active explorations

**Current Explorations:**

1. **TV Memory Layer** - Streaming service bookmark system
2. **ChatGPT Mobile MCP** - Mobile MCP access via Dropbox
3. **Joju Dropbox Miner** - File attribution for Joju
4. **Contractor Bid Tool** - Unit-agnostic bid comparison (detailed, ready to build)
5. **Phil's Ledger** - Bill tracking + Monarch API (very detailed, ready to build)
6. **Combined Brainstorms** - 10 brainstorms needing separation

---

## 🔄 LIFECYCLE FLOW

### **Exploration → PoC → Production**

```
EXPLORATION (Ideas)
├── Brainstorm
├── Evaluate
├── Design
└── Decide: Build? Later? Never?
    ↓ (if build)
BUILD PHASE
├── Write code
├── Create components
└── Make it work
    ↓ (when working)
POC (Validation)
├── Test with real data
├── Collect feedback
├── Track issues
├── Document learnings
└── Refine
    ↓ (when validated)
PRODUCTION
├── Move to production folder
├── Full deployment
├── Ongoing maintenance
└── Continuous improvement
```

**Example - TGIF:**
- ✅ Exploration (brainstormed)
- ✅ Built (code written)
- 🟡 PoC (currently validating)
- ⏳ Production (after validation)

**Example - Contractor Bid Tool:**
- ✅ Exploration (detailed design)
- ⏳ Build (not started yet)
- ⏳ PoC (after building)
- ⏳ Production (after validation)

---

## 🎯 KEY PRINCIPLES

### **1. User/System Separation**
- **System:** `8825_core/` (shareable, no user data)
- **User:** `users/` (private, never shared)
- **Benefit:** Can share system without exposing private data

### **2. Zero Code Duplication**
- Single implementation of each component
- Reusable infrastructure (Gmail, Otter, Task Tracking)
- **Benefit:** Easier maintenance, faster development

### **3. Fast Discovery**
- Index-based search (<1 second)
- Knowledge graph
- **Benefit:** Find anything instantly

### **4. Focus Isolation**
- Each focus has its own workspace
- No cross-contamination
- **Benefit:** Clean separation, easier to manage

### **5. Infrastructure Reusability**
- Build once, use everywhere
- Central PoC for validation
- **Benefit:** Faster project development

---

## 📊 CURRENT STATUS

### **System Metrics:**

| Metric | Value | Status |
|--------|-------|--------|
| **Version** | 3.0.0 | ✅ Production |
| **Files Indexed** | 266 | ✅ Complete |
| **Search Speed** | 2.3ms | ✅ 434x faster |
| **MCPs Running** | 3 | ✅ Operational |
| **Test Pass Rate** | 100% | ✅ Validated |
| **User/System Separation** | 100% | ✅ Complete |
| **Code Duplication** | 0 | ✅ Eliminated |

### **Active Work:**

| Project | Status | Phase |
|---------|--------|-------|
| **TGIF Automation** | ✅ Built | PoC (validating) |
| **Phil's Ledger** | 📋 Designed | Exploration (ready to build) |
| **Contractor Bid Tool** | 📋 Designed | Exploration (ready to build) |
| **Infrastructure** | ✅ Extracted | PoC (reusable) |

### **Focuses:**

| Focus | Status | Purpose |
|-------|--------|---------|
| **Joju** | ✅ Active | Library management |
| **HCSS** | ✅ Active | Project management |
| **JH Assistant** | ✅ Active | Personal automation |

---

## 🎓 HOW TO USE THE SYSTEM

### **1. Activate a Focus:**
```bash
# In Cascade/Windsurf
"focus on hcss"
```

### **2. Ingest Content:**
```bash
"ingest gmail"
"ingest otter"
```

### **3. Review Routed Content:**
```bash
"review routed tgif"
```

### **4. Search:**
```bash
python3 8825_core/workflows/search.py "achievement of fact"
```

### **5. Exit Focus:**
```bash
"exit focus"
```

---

## 🚀 FUTURE ROADMAP

### **Short-Term (Next Month):**
1. Validate TGIF automation PoC
2. Build Phil's Ledger
3. Separate combined brainstorms
4. Add Chat Mining Agent to infrastructure

### **Medium-Term (Next Quarter):**
1. Build Contractor Bid Tool
2. Graduate TGIF to production
3. Enhance infrastructure components
4. Add more automation workflows

### **Long-Term (Next Year):**
1. Multi-user support
2. External collaboration
3. Advanced analytics
4. Mobile integration

---

## 📚 KEY DOCUMENTS

### **System Overview:**
- `README.md` - System overview
- `TEST_REPORT_2025-11-09.md` - Validation results
- `V3_ARCHITECTURE_REVISED.md` - Architecture details

### **Core Components:**
- `8825_core/protocols/` - 17 protocols
- `8825_core/agents/` - Agent documentation
- `8825_core/workflows/` - Workflow files

### **Active Work:**
- `8825_core/poc/README.md` - PoC overview
- `8825_core/explorations/CURRENT_STATUS.md` - Exploration status
- `focuses/hcss/workflows/` - HCSS workflows

### **Focuses:**
- `8825_core/protocols/8825_hcss_focus.json` - HCSS focus protocol
- `focuses/joju/` - Joju focus data
- `focuses/hcss/` - HCSS focus data

---

## 🎯 SUMMARY

**8825 v3.0 is:**
- ✅ Production-ready personal knowledge and automation system
- ✅ 100% user/system separation (shareable core)
- ✅ Fast search (<1 second)
- ✅ Zero code duplication
- ✅ Multi-focus support (Joju, HCSS, JH Assistant)
- ✅ Reusable infrastructure (Gmail, Otter, Task Tracking)
- ✅ Active development (TGIF automation, Phil's Ledger, Contractor Bid Tool)

**Key Concepts:**
- **Focuses** - Project workspaces
- **Agents** - Automation workers
- **Protocols** - Rules and workflows
- **Workflows** - Processes (ingest, mine, route)
- **PoC** - Validation before production
- **Explorations** - Ideas being tested

**Current Phase:**
- TGIF automation in PoC validation
- Infrastructure extracted and reusable
- Multiple explorations ready to build
- System fully operational and tested

---

**You now understand the full scope of 8825 v3.0!** ✅
