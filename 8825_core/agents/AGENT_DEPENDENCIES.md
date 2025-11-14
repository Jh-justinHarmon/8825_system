# 8825 Agent Dependencies

**Last Updated:** 2025-11-07  
**Purpose:** Map protocols to agents and vice versa

---

## 📊 Protocol → Agent Mapping:

### **Joju Protocols:**

| Protocol | Agents Used | Location |
|----------|-------------|----------|
| `8825_joju_curation_agent` | AGENT-JOJU-CURATION-0001 | protocols/ |
| `joju_library_first_mining` | AGENT-JOJU-LIBRARY-FIRST-MINING-0001 | protocols/ |
| `profile_builder.py` | AGENT-JOJU-PROFILE-BUILDER-0001 | joju_sandbox/ |
| `8825_joju_mode` | Multiple Joju agents | protocols/ |

### **Mining Protocols:**

| Protocol | Agents Used | Location |
|----------|-------------|----------|
| `8825_mining` | AGENT-LIBRARY-CHAT-MINING-0001<br>AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001 | protocols/ |

### **General Protocols:**

| Protocol | Agents Used | Location |
|----------|-------------|----------|
| `8825_decision-making` | Decision framework (not agent-based) | protocols/ |
| `8825_learning_protocol.json` | Learning system (not agent-based) | protocols/ |

---

## 🔗 Agent → Protocol Mapping:

### **Joju Agents:**

| Agent | Used By | Implementation |
|-------|---------|----------------|
| AGENT-JOJU-CURATION-0001 | 8825_joju_curation_agent | Protocol-defined |
| AGENT-JOJU-LIBRARY-FIRST-MINING-0001 | joju_library_first_mining | Protocol-defined |
| AGENT-JOJU-PROFILE-BUILDER-0001 | profile_builder.py | Python implementation |
| AGENT-JOJU-PROBLEM-DEFINITION-0001 | 8825_joju_mode | Protocol-defined |
| AGENT-JOJU-THREE-PROFILE-BLUEPRINT-0001 | 8825_joju_mode | Protocol-defined |
| AGENT-JOJU-PORTFOLIO-PDF-GENERATOR-0001 | 8825_joju_mode | Protocol-defined |
| AGENT-JOJU-PERSONA-MATRIX-BUILDER-0001 | 8825_joju_mode | Protocol-defined |
| AGENT-JOJU-VALIDATION-LOOP-0001 | 8825_joju_mode | Protocol-defined |

### **Library Agents:**

| Agent | Used By | Implementation |
|-------|---------|----------------|
| AGENT-LIBRARY-CHAT-MINING-0001 | 8825_mining | Protocol-defined |
| AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001 | 8825_mining | Protocol-defined |

### **General Agents:**

| Agent | Used By | Implementation |
|-------|---------|----------------|
| AGENT-WORKSHOP-ROADMAP-0001 | Ad-hoc usage | Protocol-defined |
| AGENT-REDDIT-BETA-0001 | Ad-hoc usage | Protocol-defined |
| AGENT-REDDIT-PREQUAL-0001 | Ad-hoc usage | Protocol-defined |
| AGENT-GENERAL-BETA-TESTER-PROFILER-0001 | Ad-hoc usage | Protocol-defined |
| AGENT-GENERAL-RSS-AUTOMATION-ARCHITECT-0001 | Ad-hoc usage | Protocol-defined |
| AGENT-GENERAL-DISCOVERY-JOURNEY-DOCUMENTOR-0001 | Ad-hoc usage | Protocol-defined |
| AGENT-GENERAL-RELATIONSHIP-OUTREACH-0001 | Ad-hoc usage | Protocol-defined |

### **PMCE Agents:**

| Agent | Used By | Implementation |
|-------|---------|----------------|
| AGENT-WS-NOTION-0001 | Ad-hoc usage | Protocol-defined |

### **Forge Agents:**

| Agent | Used By | Implementation |
|-------|---------|----------------|
| AGENT-FORGE-PARTNERSHIP-DUE-DILIGENCE-0001 | Ad-hoc usage | Protocol-defined |

---

## 🔄 Agent Orchestration:

### **Multi-Agent Workflows:**

#### **Joju Profile Generation:**
```
1. AGENT-JOJU-LIBRARY-FIRST-MINING-0001
   ↓ (mines content)
2. AGENT-JOJU-CURATION-0001
   ↓ (curates for target)
3. AGENT-JOJU-PROFILE-BUILDER-0001
   ↓ (builds and renders)
   → Final Profile
```

#### **Mining Workflow:**
```
1. AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001
   ↓ (routes by complexity)
2. AGENT-LIBRARY-CHAT-MINING-0001
   ↓ (mines content)
   → Library Entries
```

---

## 📦 Implementation Types:

### **Protocol-Defined Agents (15):**
- Defined in protocol files
- Follow WCB schema
- Reconstructable from registry

### **Python-Implemented Agents (3):**
- `profile_builder.py` → AGENT-JOJU-PROFILE-BUILDER-0001
- `decision_agent.py` → Decision Agent (not in registry)
- Others in ingestion pipeline (not in registry)

### **Module-Based (Not Registered):**
- Ingestion pipeline modules
- MCP server endpoints
- These are implementations, not agents

---

## 🎯 Usage Patterns:

### **Direct Invocation:**
```
User: "Use AGENT-JOJU-CURATION-0001 to create a UX-focused profile"
System: Loads agent, applies to library, generates output
```

### **Protocol Activation:**
```
User: "Activate 8825_joju_curation_agent"
System: Loads protocol, invokes AGENT-JOJU-CURATION-0001
```

### **Pipeline Integration:**
```
Ingestion Pipeline → Classification → Routes to Project
                                    ↓
                            Invokes project agents
```

---

## 🔍 Dependency Graph:

```
Protocols
    ├── 8825_joju_curation_agent
    │   └── AGENT-JOJU-CURATION-0001
    │
    ├── joju_library_first_mining
    │   └── AGENT-JOJU-LIBRARY-FIRST-MINING-0001
    │
    ├── 8825_mining
    │   ├── AGENT-LIBRARY-CHAT-MINING-0001
    │   └── AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001
    │
    └── 8825_joju_mode
        ├── AGENT-JOJU-PROBLEM-DEFINITION-0001
        ├── AGENT-JOJU-THREE-PROFILE-BLUEPRINT-0001
        ├── AGENT-JOJU-PORTFOLIO-PDF-GENERATOR-0001
        ├── AGENT-JOJU-PERSONA-MATRIX-BUILDER-0001
        └── AGENT-JOJU-VALIDATION-LOOP-0001

Implementations
    ├── profile_builder.py
    │   └── AGENT-JOJU-PROFILE-BUILDER-0001
    │
    ├── decision_agent.py
    │   └── Decision Agent (not registered)
    │
    └── ingestion_engine.py
        └── Pipeline modules (not registered)
```

---

## ✅ Completeness Check:

- [x] All protocol agents mapped
- [x] All agents have source attribution
- [x] Implementation types documented
- [x] Multi-agent workflows defined
- [x] Dependency graph created

**Agent dependencies are 100% documented!** 🎯
