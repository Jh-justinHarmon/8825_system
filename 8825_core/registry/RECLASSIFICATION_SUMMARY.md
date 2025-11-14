# Agent Registry Reclassification Summary

**Date:** 2025-11-13  
**Action:** Reorganized misclassified "agents" into correct categories  
**Auditor:** Cascade (using TASK_TYPES_REFERENCE.md definitions)

---

## What Changed

### Before
- **Single registry:** `8825_core/agents/agent_registry.json`
- **18 items** all labeled as "agents"
- **Problem:** Only 6 were actually agents

### After
- **Four registries:**
  - `8825_core/registry/agents.json` (6 true agents)
  - `8825_core/registry/pipelines.json` (4 pipelines)
  - `8825_core/registry/workflows.json` (8 workflows)
  - `8825_core/registry/protocols_registry.json` (2 protocols)

---

## Reclassification Results

| Category | Count | % of Total | Status |
|----------|-------|------------|--------|
| **True Agents** | 6 | 33% | ✅ Correctly classified |
| **Pipelines** | 4 | 22% | 🔧 Reclassified |
| **Workflows** | 8 | 44% | 📋 Reclassified |
| **Protocols** | 2 | 11% | 📖 Reclassified |
| **Total** | 20 | 100% | - |

---

## True Agents (6)

**Definition:** Makes autonomous decisions, handles unexpected situations, adapts based on conditions

### Implemented (2)
1. **Decision Agent** - `8825_core/agents/decision_agent.py`
   - Makes proceed/default/ask decisions
   - Status: ✅ Production ready

2. **Accountability Loop Agent** - `8825_core/agents/accountability_loop_agent.py`
   - Monitors goals, makes status decisions, generates alerts
   - Status: ✅ Production ready

### Not Implemented (4)
3. **Library Mining Complexity Router** (Priority: High, Score: 91.6)
   - Makes routing decisions based on complexity analysis
   - Critical for mining system

4. **Joju Curation Agent** (Priority: High, Score: 88.0)
   - Makes content selection decisions based on target analysis
   - Core to Joju product

5. **Reddit Beta Evaluator** (Priority: Medium, Score: 75.0)
   - Makes fit assessment decisions with 7-factor scoring

6. **Reddit Pre-Qualifier** (Priority: Medium, Score: 70.0)
   - Makes pre-screening decisions with exclusion rules

---

## Pipelines (4)

**Definition:** Automated sequences with no decisions, just transformations

1. **joju_pdf_generator_pipeline**
   - Original: AGENT-JOJU-PORTFOLIO-PDF-GENERATOR-0001
   - Fixed workflow: JSON → HTML → PDF
   - Auto-detection is deterministic, not decision-making

2. **windsurf_notion_sync_pipeline**
   - Original: AGENT-WS-NOTION-0001
   - Webhook → Parse → Map → Upsert
   - No decisions, just transformation

3. **joju_profile_builder_pipeline**
   - Original: AGENT-JOJU-PROFILE-BUILDER-0001
   - Load library → Apply config → Render → Package
   - No decisions, just transformation

4. **rss_polling_pipeline**
   - Original: AGENT-GENERAL-RSS-AUTOMATION-ARCHITECT-0001
   - Poll → Filter → Parse → Score → Integrate
   - Filtering is rule-based, not decision-based

---

## Workflows (8)

**Definition:** Manual processes with documented steps, user provides inputs

1. **joju_problem_definition_workflow**
   - Original: AGENT-JOJU-PROBLEM-DEFINITION-0001
   - User provides inputs, agent follows 5-step process

2. **workshop_roadmap_workflow**
   - Original: AGENT-WORKSHOP-ROADMAP-0001
   - Manual roadmap generation

3. **beta_tester_profiler_workflow**
   - Original: AGENT-GENERAL-BETA-TESTER-PROFILER-0001
   - Manual profiling process (no scoring/routing like the agent version)

4. **discovery_journey_workflow**
   - Original: AGENT-GENERAL-DISCOVERY-JOURNEY-DOCUMENTOR-0001
   - Manual documentation process

5. **hiring_profile_workflow**
   - Original: AGENT-JOJU-THREE-PROFILE-BLUEPRINT-0001
   - Manual profile generation

6. **persona_matrix_workflow**
   - Original: AGENT-JOJU-PERSONA-MATRIX-BUILDER-0001
   - Manual persona mining

7. **relationship_outreach_workflow**
   - Original: AGENT-GENERAL-RELATIONSHIP-OUTREACH-0001
   - Manual outreach prep (confidence gate is not autonomous decision-making)

8. **joju_library_mining_workflow**
   - Original: AGENT-JOJU-LIBRARY-FIRST-MINING-0001
   - Manual mining process

---

## Protocols (2)

**Definition:** Methodologies to follow, not systems that run

1. **joju_validation_protocol**
   - Original: AGENT-JOJU-VALIDATION-LOOP-0001
   - Defines methodology for tracking validation

2. **partnership_due_diligence_protocol**
   - Original: AGENT-FORGE-PARTNERSHIP-DUE-DILIGENCE-0001
   - Defines methodology for partnership validation

---

## File Locations

### New Registry Files
```
8825_core/registry/
├── agents.json                    # 6 true agents
├── pipelines.json                 # 4 pipelines
├── workflows.json                 # 8 workflows
├── protocols_registry.json        # 2 protocols
└── RECLASSIFICATION_SUMMARY.md    # This file
```

### Old Registry (Deprecated)
```
8825_core/agents/
├── agent_registry.json            # ⚠️ DEPRECATED - See registry/ folder
├── AGENT_AUDIT_2025-11-13.md     # Audit findings
└── ...
```

---

## Why This Matters

### 1. Clarity
- Know what needs to be **implemented** (agents) vs **documented** (workflows/protocols)
- Understand the **effort** required (agents are complex, pipelines/workflows are simpler)

### 2. Effort Estimation
- **Agents:** Require decision logic, condition handling, adaptation (complex)
- **Pipelines:** Require error handling, retry logic (moderate)
- **Workflows:** Require documentation, templates (simple)
- **Protocols:** Require methodology definition (simple)

### 3. Maintenance
- **Agents:** Need monitoring, testing, decision logic updates
- **Pipelines:** Need error handling, monitoring
- **Workflows:** Need documentation updates
- **Protocols:** Need methodology refinement

### 4. ROI
- Building **6 agents** >> building "18 agents"
- Focus on high-value agents first (Library Router, Joju Curation)

---

## The Real Gap

### Before Reclassification
- **Agents needed:** 18
- **Agents implemented:** 2
- **Gap:** 16 agents (11% complete) 😰

### After Reclassification
- **Agents needed:** 6
- **Agents implemented:** 2
- **Gap:** 4 agents (33% complete) 🎯

**Much better!**

---

## Next Steps

### Immediate
1. ✅ Reclassification complete
2. ⏳ Update references to old agent_registry.json
3. ⏳ Move workflows to 8825_core/workflows/ (if not already there)
4. ⏳ Move protocols to 8825_core/protocols/ (if not already there)

### Short-term
1. **Implement 2 high-priority agents:**
   - Library Mining Complexity Router (score: 91.6)
   - Joju Curation Agent (score: 88.0)

2. **Document workflows:**
   - Create templates/forms for workflow execution
   - Add to workflows/ directory

3. **Document protocols:**
   - Create .md files in protocols/ directory
   - Add usage examples

### Long-term
1. **Implement remaining agents:**
   - Reddit Beta Evaluator (score: 75.0)
   - Reddit Pre-Qualifier (score: 70.0)

2. **Build pipelines:**
   - Joju PDF Generator
   - Profile Builder
   - Windsurf-Notion Sync
   - RSS Polling

---

## Audit Criteria

### True Agent Checklist
- ✅ Makes autonomous decisions
- ✅ Handles unexpected situations
- ✅ Adapts based on conditions
- ✅ Has if/then logic

### Not an Agent
- ❌ **Pipeline:** Automated sequence, no decisions
- ❌ **Workflow:** Manual process, documented steps
- ❌ **Protocol:** Methodology to follow
- ❌ **Pattern:** Reusable solution

---

## References

- **Audit Document:** `8825_core/agents/AGENT_AUDIT_2025-11-13.md`
- **Task Types Reference:** `8825_core/protocols/TASK_TYPES_REFERENCE.md`
- **Old Registry:** `8825_core/agents/agent_registry.json` (deprecated)
- **New Registries:** `8825_core/registry/*.json`

---

**Status:** ✅ Reclassification complete  
**Impact:** Honest, clear, correct expectations  
**Next:** Implement 2 high-priority agents
