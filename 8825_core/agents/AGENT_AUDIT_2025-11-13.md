# Agent Registry Audit - Task Type Reclassification

**Date:** 2025-11-13  
**Auditor:** Cascade (using TASK_TYPES_REFERENCE.md definitions)  
**Purpose:** Determine which "agents" are actually agents vs pipelines/workflows/protocols

---

## Audit Criteria

**True Agent (by definition):**
- Makes autonomous decisions
- Handles unexpected situations
- Adapts based on conditions
- Has if/then logic

**Not an Agent:**
- **Pipeline:** Automated sequence, no decisions
- **Workflow:** Manual process, documented steps
- **Protocol:** Methodology to follow
- **Pattern:** Reusable solution

---

## Results Summary

| Category | Count | % of Total |
|----------|-------|------------|
| **True Agents** | 5 | 28% |
| **Pipelines** | 4 | 22% |
| **Workflows** | 7 | 39% |
| **Protocols** | 2 | 11% |
| **Total** | 18 | 100% |

**Verdict:** You need 5 agents, not 18.

---

## ✅ TRUE AGENTS (5)

### 1. AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001 ✅
**Classification:** AGENT  
**Why:** Makes routing decisions based on complexity analysis
- **Decisions:** Tier 1 vs Tier 2 classification
- **Conditions:** Structure, routing clarity, cross-project scope, pattern novelty
- **Adapts:** Routes to appropriate processing based on assessment
- **Status:** Not implemented

---

### 2. AGENT-REDDIT-BETA-0001 ✅
**Classification:** AGENT  
**Why:** Makes scoring decisions with weighted criteria
- **Decisions:** Beta tester fit scoring (0-100)
- **Conditions:** 7 weighted factors (platform alignment, creator mindset, etc.)
- **Adapts:** Generates profiles based on scoring thresholds
- **Status:** Not implemented

---

### 3. AGENT-REDDIT-PREQUAL-0001 ✅
**Classification:** AGENT  
**Why:** Makes pre-screening decisions with exclusion rules
- **Decisions:** Whether deeper evaluation is worthwhile
- **Conditions:** Activity level, spam/NSFW/bot detection, competitor accounts
- **Adapts:** Confidence scoring, handles ambiguous cases
- **Status:** Not implemented

---

### 4. AGENT-JOJU-CURATION-0001 ✅
**Classification:** AGENT  
**Why:** Makes content selection decisions based on target analysis
- **Decisions:** Which achievements to include for specific audience
- **Conditions:** Confidence scores, Achievement of Fact ratings, target requirements
- **Adapts:** Calculates relevance scores, optimizes for different audiences
- **Status:** Not implemented

---

### 5. Decision Agent (existing) ✅
**Classification:** AGENT  
**Why:** Makes proceed/default/ask decisions
- **Decisions:** Whether to proceed, use default, or ask for clarification
- **Conditions:** Intent clarity, stakes, efficiency, reversibility
- **Adapts:** Safety overrides, confidence thresholds
- **Status:** ✅ IMPLEMENTED (production ready)

---

## 🔧 PIPELINES (4)

### 6. AGENT-JOJU-PORTFOLIO-PDF-GENERATOR-0001
**Reclassify as:** PIPELINE  
**Why:** Automated sequence with no decisions
- Fixed workflow: JSON → HTML → PDF
- Auto-detects layout mode (but this is deterministic, not decision-making)
- No conditional logic beyond format detection
- **Should be:** `joju_pdf_generator_pipeline`

---

### 7. AGENT-WS-NOTION-0001
**Reclassify as:** PIPELINE  
**Why:** Automated sync with fixed mapping
- Webhook → Parse → Map → Upsert to Notion
- No decisions, just transformation
- **Should be:** `windsurf_notion_sync_pipeline`

---

### 8. AGENT-JOJU-PROFILE-BUILDER-0001
**Reclassify as:** PIPELINE  
**Why:** Automated rendering with fixed workflow
- Load library → Apply config → Render → Package
- No decisions, just transformation
- **Should be:** `joju_profile_builder_pipeline`

---

### 9. AGENT-GENERAL-RSS-AUTOMATION-ARCHITECT-0001
**Reclassify as:** PIPELINE  
**Why:** Automated RSS polling with filtering
- Poll → Filter → Parse → Score → Integrate
- Filtering is rule-based, not decision-based
- **Should be:** `rss_polling_pipeline`

---

## 📋 WORKFLOWS (7)

### 10. AGENT-JOJU-PROBLEM-DEFINITION-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual process with documented steps
- User provides inputs
- Agent follows 5-step process (Deconstruct, Diagnose, Develop, Deliver, Refine)
- Outputs structured definition
- **Should be:** `joju_problem_definition_workflow`

---

### 11. AGENT-WORKSHOP-ROADMAP-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual roadmap generation
- User provides goal, participants, constraints
- Agent generates phased plan
- No autonomous decisions, just structured output
- **Should be:** `workshop_roadmap_workflow`

---

### 12. AGENT-GENERAL-BETA-TESTER-PROFILER-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual profiling process
- User provides username/feed
- Agent analyzes and generates profile
- No scoring/routing decisions (unlike AGENT-REDDIT-BETA-0001)
- **Should be:** `beta_tester_profiler_workflow`

---

### 13. AGENT-GENERAL-DISCOVERY-JOURNEY-DOCUMENTOR-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual documentation process
- User provides conversation
- Agent structures as phased narrative
- No decisions, just transformation
- **Should be:** `discovery_journey_workflow`

---

### 14. AGENT-JOJU-THREE-PROFILE-BLUEPRINT-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual profile generation
- User provides team/role context
- Agent generates 3 profiles
- No decisions, just structured output
- **Should be:** `hiring_profile_workflow`

---

### 15. AGENT-JOJU-PERSONA-MATRIX-BUILDER-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual persona mining
- User provides product context
- Agent generates persona matrix
- No decisions, just structured output
- **Should be:** `persona_matrix_workflow`

---

### 16. AGENT-GENERAL-RELATIONSHIP-OUTREACH-0001
**Reclassify as:** WORKFLOW  
**Why:** Manual outreach prep
- User provides person info
- Agent generates prep brief + message kit
- Confidence gate (asks if <0.7) is not autonomous decision-making
- **Should be:** `relationship_outreach_workflow`

---

## 📖 PROTOCOLS (2)

### 17. AGENT-JOJU-VALIDATION-LOOP-0001
**Reclassify as:** PROTOCOL  
**Why:** Defines methodology for tracking validation
- Not a system that runs
- Defines how to track feedback/referrals/pricing
- **Should be:** `joju_validation_protocol`

---

### 18. AGENT-LIBRARY-CHAT-MINING-0001 ✅ REPURPOSED
**Reclassified as:** TOOL (Brain Learning Exporter)  
**Why:** Now an export tool that leverages brain's learning_extractor
- **Old:** Manual chat mining with reinvented extraction
- **New:** Export brain learnings to external formats
- **Implementation:** `brain_learning_exporter.py`
- **Uses:** Brain's learning_extractor + auto_memory_creator
- **Formats:** mining_report, cascade, markdown, json
- **Modern features:** Time decay, usage tracking, confidence scoring
- **Status:** ✅ Implemented and documented

---

## 🚫 MISSING AGENTS

### AGENT-FORGE-PARTNERSHIP-DUE-DILIGENCE-0001
**Status:** Not in registry (mentioned in index but not in JSON)  
**Would be:** WORKFLOW (manual due diligence process)

---

## Summary by Reclassification

### ✅ Keep as Agents (5):
1. Decision Agent (implemented)
2. Library Mining Complexity Router
3. Reddit Beta Evaluator
4. Reddit Pre-Qualifier
5. Joju Curation Agent

### 🔧 Reclassify as Pipelines (4):
6. Joju Portfolio PDF Generator
7. Windsurf-Notion Sync
8. Joju Profile Builder
9. RSS Automation Architect

### 📋 Reclassify as Workflows (7):
10. Joju Problem Definition
11. Workshop Roadmap Generator
12. Beta Tester Profiler
13. Discovery Journey Documentor
14. Three-Profile Blueprint
15. Persona Matrix Builder
16. Relationship Outreach

### 📖 Reclassify as Protocols (2):
17. Joju Validation Loop
18. Library Chat Mining

---

## Implementation Priority (True Agents Only)

### High Priority:
1. **Library Mining Complexity Router** (score: 91.6/100)
   - Makes routing decisions
   - Critical for mining system
   - Clear decision logic

2. **Joju Curation Agent** (new, high value)
   - Makes content selection decisions
   - Core to Joju product
   - Scoring + relevance calculation

### Medium Priority:
3. **Reddit Beta Evaluator** (scoring system)
   - Makes fit assessment decisions
   - 7-factor weighted scoring
   - Useful for beta recruitment

4. **Reddit Pre-Qualifier** (filtering system)
   - Makes pre-screening decisions
   - Exclusion rules + confidence scoring
   - Reduces manual work

### Low Priority:
5. **Decision Agent** (✅ already implemented)
   - Working in production
   - No action needed

---

## Recommendations

### Immediate Actions:
1. **Rename registry** → `agent_registry.json` should be `capability_registry.json`
2. **Reclassify all 18** using correct task types
3. **Implement 2 agents:**
   - Library Mining Complexity Router (highest score)
   - Joju Curation Agent (highest business value)

### File Structure:
```
8825_core/
├── agents/           # Only true agents (5 total)
├── pipelines/        # Automated sequences (4 total)
├── workflows/        # Manual processes (7 total)
└── protocols/        # Methodologies (2 total)
```

### Registry Updates:
- Split `agent_registry.json` into 4 files:
  - `agents.json` (5 entries)
  - `pipelines.json` (4 entries)
  - `workflows.json` (7 entries)
  - `protocols.json` (2 entries)

---

## Key Insights

### Why This Matters:
1. **Clarity:** Know what needs to be implemented vs documented
2. **Effort:** Agents require decision logic (complex), pipelines/workflows don't
3. **Maintenance:** Agents need monitoring, pipelines need error handling, workflows need docs
4. **ROI:** Building 5 agents >> building 18 "agents"

### The Real Gap:
- **Agents needed:** 5
- **Agents implemented:** 1 (20%)
- **Gap:** 4 agents

**Not 1/18 (6%), but 1/5 (20%). Much better!**

---

## Next Steps

1. **Audit complete** ✅
2. **Review findings** (you're here)
3. **Decide:** Reclassify registry or keep as-is?
4. **If reclassifying:** Update registry + file structure
5. **If keeping:** Implement 2 high-priority agents next

**Recommendation:** Reclassify. It's honest, clear, and sets correct expectations.
