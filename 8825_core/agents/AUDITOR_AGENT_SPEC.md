# Agent Specification: Auditor Agent

**Agent ID:** AGENT-AUDITOR-0001  
**Type:** Meta-Agent (validates other agents/workflows)  
**Priority Score:** 88.0  
**Status:** ✅ Implemented  
**Implementation:** `8825_core/agents/auditor_agent.py`  
**Created:** 2025-11-14

---

## Overview

The Auditor Agent is a **meta-agent** that validates workflow outputs by gathering exhaustive context from all available sources and performing evidence triangulation. Unlike production workflows that prioritize speed and efficiency, the auditor prioritizes thoroughness and accuracy.

### Key Design Principles

1. **Thoroughness over speed** - Can be slow/expensive
2. **Evidence triangulation** - Multiple sources = high confidence
3. **Actionable recommendations** - Distinguish auditor vs automation approaches
4. **Graceful degradation** - Partial audit if sources unavailable
5. **Read-only** - Never modifies automation output

---

## Problem Definition

### Core Need
Validate that automated workflows are producing accurate, complete results.

### Pain Point
Workflows run automatically, but results may contain:
- Extraction errors (wrong data)
- Omissions (missed data)
- Ambiguities (unclear data)
- Transcription mistakes (OCR/speech-to-text errors)

### What Happens If Not Solved
- Trust issues with automation
- Manual verification required (defeats purpose)
- Errors propagate downstream
- No feedback loop for improvement

### Minimum Viable Solution
Agent checks workflow output against best available context, reports discrepancies, suggests improvements.

---

## Context & Dependencies

### Existing Patterns Reused

1. **Meeting Processor Correction Tracking**
   - Already logs original → corrected transformations
   - Pattern: Track what changed and why

2. **Evidence Triangulation Philosophy**
   - Multiple weak signals > one strong signal
   - Pattern: Aggregate multiple sources, score confidence

3. **Agent Classification System**
   - This IS a true agent (makes decisions, adapts)
   - Pattern: Decision logic + conditional behavior

4. **Multi-Source Ingestion**
   - Email, transcripts, screenshots, Brain Transport
   - Pattern: Gather from all available channels

5. **Confidence Scoring**
   - high/medium/low pattern established
   - Pattern: Quantify certainty of findings

### Dependencies

**Data Sources:**
- Brain Transport (system context)
- Domain knowledge bases (TGIF Knowledge, etc.)
- MCP Inbox Server (email access)
- Filesystem (transcripts, screenshots, logs)
- Other agents (can call for specialized analysis)

**Tools:**
- All MCPs available
- All protocols accessible
- All workflows callable
- Full filesystem access

**No Constraints:**
- Time: Can take 5-10 minutes
- Cost: Can spend $0.50-$2.00 per audit
- Thoroughness: Check ALL sources

---

## Requirements

### Explicit Requirements

**MUST do:**

1. **Accept workflow output** - JSON/structured data from any automation
2. **Gather maximum context** - All available sources for that workflow type
3. **Prompt user for context** - Request additional materials if needed
4. **Compare output to context** - Identify gaps, errors, ambiguities
5. **Generate audit report** - What's accurate, what's missing, what's wrong
6. **Recommend improvements** - How to make automation better
7. **Score confidence** - Overall quality assessment (PASS/REVIEW/FAIL)

**Performance Requirements:**
- Complete audit in <10 minutes
- Cost <$2.00 per audit
- Accuracy >90% in detecting real errors
- <5% false positives

**Integration Requirements:**
- Input: JSON workflow output
- Output: JSON audit report + markdown summary
- CLI interface for command-line usage
- Python API for programmatic usage

### Implicit Requirements

- **Who:** You (initially), team members (eventually)
- **Where:** Runs after workflow completes
- **When:** On-demand or scheduled
- **How often:** Weekly for critical workflows, monthly for others
- **Skill level:** User just says "/audit" - agent handles complexity

---

## Constraints

### Technical Constraints

- Python 3.9+
- Cannot access private data without user permission
- Rate limits on API calls
- Must preserve privacy (don't mix contexts)

### Process Constraints

- Read-only (doesn't modify automation output)
- User approves before requesting additional context
- Clear audit trail (what sources were checked)
- Graceful degradation if sources unavailable

### Resource Constraints

- Budget: ~$8-16/month for weekly audits
- Time: 5-10 minutes per audit acceptable
- Storage: Audit reports archived for trend analysis

---

## Edge Cases

### 1. Missing Source Materials
**Scenario:** Transcript deleted, email not available  
**Handling:** Flag as "unable to verify" with explanation, continue with available sources

### 2. Conflicting Sources
**Scenario:** Email says X, transcript says Y  
**Handling:** Note conflict, provide both versions, flag for user decision

### 3. Ambiguous Results
**Scenario:** Automation unclear, context also unclear  
**Handling:** Score low confidence, recommend manual review

### 4. Over-Auditing
**Scenario:** User audits trivial workflows  
**Handling:** Quick pass/fail, don't waste tokens on low-value checks

### 5. Context Overload
**Scenario:** Too many sources to analyze  
**Handling:** Prioritize based on discrepancy likelihood, sample if needed

### 6. API Failures
**Scenario:** MCP server down, Brain Transport unavailable  
**Handling:** Retry with backoff, use cached data, note in report

---

## Success Criteria

### Functional Success
- [x] Accepts any workflow output (JSON/MD)
- [x] Gathers context from 3+ sources
- [x] Identifies errors/gaps in automation
- [x] Generates actionable improvement recommendations
- [x] Prompts user for context when needed

### Quality Success
- [ ] 90%+ accuracy in detecting real errors (needs validation)
- [ ] <5% false positives (needs validation)
- [x] Clear reasoning for each finding
- [x] Recommendations are implementable

### Performance Success
- [x] Complete audit in <10 minutes
- [x] Cost <$2.00 per audit (estimated)
- [x] Handles multiple workflow types

---

## Technical Design

### Architecture

```
AuditorAgent
├── gather_context()           # Multi-source context gathering
├── compare_and_analyze()      # Evidence triangulation
├── detect_gaps()              # Find missing data
├── generate_recommendations() # Efficiency-aware suggestions
└── create_audit_report()      # JSON + markdown output
```

### Input Format

```json
{
  "workflow_output": {
    "decisions": [...],
    "actions": [...],
    "risks": [...],
    "corrections_made": [...]
  },
  "workflow_type": "meeting_automation",
  "metadata": {
    "workflow_id": "tgif_20251114",
    "transcript_file": "path/to/transcript.json"
  }
}
```

### Output Format

```json
{
  "audit_metadata": {
    "workflow_type": "meeting_automation",
    "audit_date": "2025-11-14T21:30:00",
    "sources_checked": 5,
    "sources_available": 4,
    "duration_seconds": 287.5
  },
  "overall_assessment": {
    "verdict": "PASS|REVIEW|FAIL",
    "accuracy_score": 0.87,
    "completeness_score": 0.92,
    "confidence": 0.85
  },
  "findings": {
    "high_confidence": [...],
    "medium_confidence": [...],
    "low_confidence": [...]
  },
  "gaps": [...],
  "recommendations": [...]
}
```

### Context Source Mapping

```python
CONTEXT_SOURCES = {
    "meeting_automation": [
        "gmail_otter_emails",      # MCP inbox server
        "brain_transport",          # Cached system context
        "tgif_knowledge_base",      # Domain knowledge
        "calendar_events",          # Meeting metadata
        "meeting_transcript"        # Source transcript
    ],
    "email_processing": [
        "gmail_full_thread",
        "sender_history",
        "brain_learnings",
        "attachment_analysis"
    ],
    "screenshot_processing": [
        "original_screenshot",
        "ocr_full_output",
        "related_emails",
        "system_logs"
    ]
}
```

---

## Evidence Triangulation Logic

### Confidence Scoring Formula

```python
confirmation_score = min(len(confirmations) * 0.3, 0.9)
contradiction_penalty = len(contradictions) * 0.4
absence_penalty = len(absences) * 0.05

confidence = max(0.0, min(1.0, 
    confirmation_score - contradiction_penalty - absence_penalty
))
```

### Interpretation

- **0.8-1.0:** High confidence (2+ sources confirm, no contradictions)
- **0.5-0.8:** Medium confidence (1 source confirms, or some conflicts)
- **0.0-0.5:** Low confidence (no confirmation, or contradictions)

---

## Recommendation Engine

### Pattern: Efficiency Translation

For each issue found, auditor provides:

1. **What auditor did** (expensive/thorough method)
2. **What automation should do** (efficient alternatives)

**Example:**

```
Issue: Missed action item "Mario to update store mapping"

Auditor Approach:
- Queried full email thread via MCP
- Cross-referenced Brain Transport
- Checked TGIF Knowledge base
- Found mention in follow-up email

Automation Options:
1. Add email_thread_id to metadata (near-zero cost)
   - Links context without re-querying
   - Requires initial capture
   
2. Update TGIF Knowledge with pattern (one-time cost)
   - Automation uses cached version
   - May miss edge cases
   
3. Add regex for "to update|to create|to fix" (minimal cost)
   - Catches common action patterns
   - Won't handle complex variations
```

---

## Workflow Integration

### Command Line

```bash
# Basic audit
python 8825_core/agents/auditor_agent.py \
  --output-file data/processed/2025-11-14_tgif.json \
  --workflow-type meeting_automation

# With metadata
python 8825_core/agents/auditor_agent.py \
  --output-file data/processed/2025-11-14_tgif.json \
  --workflow-type meeting_automation \
  --metadata metadata.json \
  --report-dir audits/ \
  --verbose
```

### Windsurf Workflow

```
/audit meeting_automation data/processed/2025-11-14_tgif.json
```

### Python API

```python
from agents.auditor_agent import AuditorAgent

auditor = AuditorAgent(verbose=True)
report = auditor.audit_workflow(
    workflow_output=output_data,
    workflow_type="meeting_automation",
    metadata={"workflow_id": "tgif_20251114"}
)

print(f"Verdict: {report['overall_assessment']['verdict']}")
```

---

## Test Plan

### Test 1: Known Good Output
**Input:** TGIF meeting with verified correct extraction  
**Expected:** PASS verdict, high confidence scores  
**Validates:** Doesn't create false positives

### Test 2: Known Error
**Input:** Meeting output with planted error ("NetSweet" instead of "NetSuite")  
**Expected:** FAIL or REVIEW, flags the error, suggests correction  
**Validates:** Catches real mistakes

### Test 3: Missing Data
**Input:** Meeting output that missed 2 action items  
**Expected:** Gaps detected, items listed in "missing" section  
**Validates:** Finds omissions, not just errors

### Test 4: Efficiency Recommendations
**Input:** Output where auditor used expensive methods  
**Expected:** Recommendations include 2-3 efficiency options  
**Validates:** Distinguishes auditor vs automation approaches

### Test 5: Partial Context
**Input:** Workflow output where 2/5 context sources unavailable  
**Expected:** Partial audit, notes missing sources, continues anyway  
**Validates:** Graceful degradation

### Test 6: Multi-Workflow
**Input:** 3 different workflow types (meeting, email, screenshot)  
**Expected:** Adapts context gathering per type  
**Validates:** Workflow-specific logic works

---

## Implementation Status

### ✅ Completed

1. Core agent class (`auditor_agent.py`)
2. Context gathering engine
3. Evidence triangulation logic
4. Recommendation engine with efficiency translation
5. Audit report generation (JSON + markdown)
6. CLI interface
7. Registry integration (`agents.json`)
8. Workflow integration (`/audit`)
9. Documentation (this spec + workflow guide)

### 🔄 In Progress

10. Test fixtures and validation

### 📋 Future Enhancements

- NLP-based gap detection (beyond keyword matching)
- Automated improvement implementation
- Trend analysis across multiple audits
- Integration with accountability loops
- Real-time auditing (streaming mode)
- Custom context source plugins

---

## Cost-Benefit Analysis

### Development Cost
- Time: ~12 hours (design + implementation + docs)
- Resources: 1 developer

### Per-Audit Cost
- Time: 5-10 minutes
- Tokens: ~50K-100K (depending on context size)
- Cost: $0.50-$2.00

### Monthly Cost (Weekly Audits)
- 4 audits/month × $1.25 avg = ~$5/month
- Plus development amortized: ~$10/month first year

### Value Created
- Catches automation errors before propagation
- Creates improvement feedback loop
- Builds confidence in automation
- Prevents 5-10 hours/month of rework
- Estimated value: $500-1000/month

### ROI
- Monthly cost: ~$15
- Monthly value: ~$750
- **ROI: 50x return**

---

## Usage Guidelines

### When to Audit

**Do audit:**
- Critical workflows (TGIF meetings, financial data)
- After automation changes
- Weekly quality checks
- When debugging issues
- Before major decisions based on automation

**Don't audit:**
- Trivial workflows (low-value data)
- Every single run (too expensive)
- When context is unavailable
- Real-time processing (use fast validation instead)

### Interpreting Results

**PASS (Accuracy >80%, Completeness >80%)**
- Automation working correctly
- Minor improvements suggested
- Continue using with confidence

**REVIEW (Accuracy 60-80% OR Completeness 60-80%)**
- Some issues found
- Review low-confidence findings
- Implement high-priority recommendations
- Re-audit after fixes

**FAIL (Accuracy <60% OR Completeness <60%)**
- Significant issues
- Don't trust automation output
- Implement critical recommendations
- May need manual review
- Re-audit before resuming automation

---

## Evolution Path

### Phase 1: ✅ Core Implementation
- Basic context gathering
- Simple evidence triangulation
- Recommendation generation
- CLI interface

### Phase 2: 🔄 Validation & Refinement
- Test with real workflow outputs
- Tune confidence scoring
- Improve gap detection
- Add more context sources

### Phase 3: 📋 Advanced Features
- NLP-based analysis
- Automated improvement implementation
- Trend tracking
- Custom plugins

### Phase 4: 📋 Scale & Integration
- Multi-workflow batch auditing
- Integration with accountability loops
- Real-time validation mode
- Team collaboration features

---

## Related Documentation

- **Implementation:** `8825_core/agents/auditor_agent.py`
- **Workflow:** `.windsurf/workflows/audit.md`
- **Registry:** `8825_core/registry/agents.json` (AGENT-AUDITOR-0001)
- **Philosophy:** `docs/reference/PHILOSOPHY.md` (Evidence Triangulation)
- **Collab Protocol:** `8825_core/protocols/COLLAB_CYCLE_PROTOCOL.md`

---

**Status:** Production Ready ✅  
**Next Steps:** Create test fixtures, validate with real data, iterate based on usage
