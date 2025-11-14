# 8825 Agent Index

**Last Updated:** 2025-11-07  
**Total Agents:** 18  
**Registry:** `projects/8825_00-agents.json`

---

## 📊 Quick Stats:

- **Joju Agents:** 8
- **General Agents:** 7
- **Library Agents:** 2
- **PMCE Agents:** 1
- **Forge Agents:** 1

---

## 🎯 By Category:

### **Joju Agents (8 agents)**

| Agent ID | Purpose | Source |
|----------|---------|--------|
| AGENT-JOJU-PROBLEM-DEFINITION-0001 | Clarifies Joju product problems | Protocol |
| AGENT-JOJU-THREE-PROFILE-BLUEPRINT-0001 | Creates three-profile blueprint | Protocol |
| AGENT-JOJU-PORTFOLIO-PDF-GENERATOR-0001 | Generates portfolio PDFs | Protocol |
| AGENT-JOJU-PERSONA-MATRIX-BUILDER-0001 | Builds persona matrices | Protocol |
| AGENT-JOJU-VALIDATION-LOOP-0001 | Validates Joju content | Protocol |
| AGENT-JOJU-CURATION-0001 ✨ | Curates library for target audiences | 8825_joju_curation_agent |
| AGENT-JOJU-LIBRARY-FIRST-MINING-0001 ✨ | Mines content library-first | joju_library_first_mining |
| AGENT-JOJU-PROFILE-BUILDER-0001 ✨ | Builds profiles with variations | profile_builder.py |

✨ = Added 2025-11-07

---

### **General Agents (7 agents)**

| Agent ID | Purpose | Source |
|----------|---------|--------|
| AGENT-WORKSHOP-ROADMAP-0001 | Generates workshop roadmaps | Protocol |
| AGENT-REDDIT-BETA-0001 | Evaluates Reddit users as beta testers | Protocol |
| AGENT-REDDIT-PREQUAL-0001 | Pre-qualifies Reddit beta testers | Protocol |
| AGENT-GENERAL-BETA-TESTER-PROFILER-0001 | Profiles beta testers | Protocol |
| AGENT-GENERAL-RSS-AUTOMATION-ARCHITECT-0001 | Architects RSS automation | Protocol |
| AGENT-GENERAL-DISCOVERY-JOURNEY-DOCUMENTOR-0001 | Documents discovery journeys | Protocol |
| AGENT-GENERAL-RELATIONSHIP-OUTREACH-0001 | Manages relationship outreach | Protocol |

---

### **Library Agents (2 agents)**

| Agent ID | Purpose | Source |
|----------|---------|--------|
| AGENT-LIBRARY-CHAT-MINING-0001 | Mines chat conversations | Protocol |
| AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001 | Routes mining by complexity | Protocol |

---

### **PMCE Agents (1 agent)**

| Agent ID | Purpose | Source |
|----------|---------|--------|
| AGENT-WS-NOTION-0001 | Syncs Windsurf to Notion | Protocol |

---

### **Forge Agents (1 agent)**

| Agent ID | Purpose | Source |
|----------|---------|--------|
| AGENT-FORGE-PARTNERSHIP-DUE-DILIGENCE-0001 | Partnership due diligence | Protocol |

---

## 🔗 By Protocol:

### **Joju Protocols:**
- `8825_joju_curation_agent` → AGENT-JOJU-CURATION-0001
- `joju_library_first_mining` → AGENT-JOJU-LIBRARY-FIRST-MINING-0001
- `profile_builder.py` → AGENT-JOJU-PROFILE-BUILDER-0001

### **General Protocols:**
- Various general protocols → 7 general agents

### **Library Protocols:**
- `8825_mining` → AGENT-LIBRARY-CHAT-MINING-0001, AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001

---

## 📋 WCB Schema:

All agents follow the 6-element WCB schema:
1. **system_role** - What the agent does
2. **inputs_required** - What it needs
3. **outputs** - What it produces
4. **workflow** - How it works
5. **constraints** - What it must follow
6. **provenance** - Where it came from (routing, created_at, source_report)

---

## 🔍 Finding Agents:

### **By Purpose:**
- **Profile Building:** AGENT-JOJU-PROFILE-BUILDER-0001
- **Content Curation:** AGENT-JOJU-CURATION-0001
- **Content Mining:** AGENT-JOJU-LIBRARY-FIRST-MINING-0001, AGENT-LIBRARY-CHAT-MINING-0001
- **Beta Testing:** AGENT-REDDIT-BETA-0001, AGENT-GENERAL-BETA-TESTER-PROFILER-0001
- **Automation:** AGENT-GENERAL-RSS-AUTOMATION-ARCHITECT-0001, AGENT-WS-NOTION-0001

### **By Project:**
- **Joju:** 8 agents
- **General/Cross-project:** 7 agents
- **Library/Mining:** 2 agents
- **PMCE:** 1 agent
- **Forge:** 1 agent

---

## 📖 Usage:

### **To Use an Agent:**
1. Find agent ID in this index
2. Look up full definition in `projects/8825_00-agents.json`
3. Reconstruct WCB using: `recreate WCB for <agent_id>`

### **To Add an Agent:**
1. Create WCB schema (6 elements)
2. Add to `projects/8825_00-agents.json`
3. Update routing_index
4. Update stats
5. Update this index

---

## ✅ Registry Status:

- **Total Agents:** 18
- **All Registered:** ✅
- **All Indexed:** ✅
- **All Documented:** ✅

**The agent registry is 100% complete!** 🎯
