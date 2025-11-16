---
description: Audit workflow output for accuracy and completeness
---

# Audit Workflow

Validates automation results by gathering exhaustive context and performing evidence triangulation.

## Purpose

The Auditor Agent checks workflow outputs against all available context sources to:
- Verify accuracy of extracted data
- Detect missing information (gaps)
- Generate improvement recommendations
- Build confidence in automation results

## When to Use

- **After critical workflows** - TGIF meetings, important email processing
- **Weekly quality checks** - Validate automation is working correctly
- **Before major decisions** - Ensure data accuracy before acting on it
- **When debugging** - Understand why automation missed something

## Trigger Phrases

You can say:
- `/audit <workflow-type> <output-file>`
- "Audit the TGIF meeting from Friday"
- "Check accuracy of the email processing"
- "Validate the screenshot extraction"

## Usage

### Basic Audit

```bash
/audit meeting_automation data/processed/2025-11-14_tgif.json
```

### With Metadata

```bash
python 8825_core/agents/auditor_agent.py \
  --output-file data/processed/2025-11-14_tgif.json \
  --workflow-type meeting_automation \
  --metadata metadata.json \
  --verbose
```

### Supported Workflow Types

- `meeting_automation` - TGIF meetings, Otter transcripts
- `email_processing` - Email classification, extraction
- `screenshot_processing` - OCR, calendar events

## What It Does

### Phase 1: Context Gathering (2-5 min)
- Checks Brain Transport (system context)
- Queries domain knowledge bases (TGIF Knowledge, etc.)
- Accesses emails via MCP inbox server
- Loads meeting transcripts
- Gathers all available sources

### Phase 2: Evidence Triangulation (1-3 min)
- Compares each output item against ALL context sources
- Counts confirmations (sources that agree)
- Detects contradictions (sources that disagree)
- Calculates confidence scores

### Phase 3: Gap Detection (1-2 min)
- Identifies what's in context but missing from output
- Assesses severity of gaps
- Notes which sources contained the missing data

### Phase 4: Recommendations (1-2 min)
- Analyzes patterns in errors/gaps
- Suggests automation improvements
- Provides efficiency trade-offs:
  - What auditor did (thorough/expensive)
  - What automation should do (efficient/cheap)

### Phase 5: Report Generation (<1 min)
- Creates JSON audit report
- Generates markdown summary
- Assigns verdict: PASS / REVIEW / FAIL

## Output

### Audit Report (JSON)

```json
{
  "overall_assessment": {
    "verdict": "PASS",
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

### Verdict Meanings

- **PASS** - High accuracy (>80%), high completeness (>80%)
- **REVIEW** - Medium accuracy or completeness (60-80%)
- **FAIL** - Low accuracy or completeness (<60%)

## Cost & Time

**Per Audit:**
- Time: 5-10 minutes
- Cost: $0.50-$2.00 (depending on context size)
- Frequency: Weekly or on-demand

**Value:**
- Catches errors before they propagate
- Prevents 5-10 hours/month of rework
- ROI: 20-50x return

## Examples

### Example 1: TGIF Meeting Audit

```bash
# Audit Friday's meeting
python 8825_core/agents/auditor_agent.py \
  --output-file data/processed/2025-11-14_tgif.json \
  --workflow-type meeting_automation \
  --verbose

# Result: PASS (87% accuracy, 92% completeness)
# Found: 2 minor gaps, 1 recommendation
```

### Example 2: Email Processing Audit

```bash
# Audit email classification
python 8825_core/agents/auditor_agent.py \
  --output-file data/processed/email_batch_20251114.json \
  --workflow-type email_processing

# Result: REVIEW (72% accuracy)
# Found: 3 misclassifications, 2 recommendations
```

## Recommendations Format

Each recommendation includes:

1. **Issue Found** - What the auditor discovered
2. **Auditor Approach** - How auditor found it (expensive method)
3. **Automation Options** - Efficient alternatives:
   - Option 1: Fast/cheap approach
   - Option 2: Medium approach
   - Option 3: Thorough approach (if needed)

Example:
```
Issue: Missed 2 action items in meeting
Auditor Approach: Queried full email thread, found context
Automation Options:
  1. Add email_thread_id to metadata (near-zero cost)
  2. Update TGIF Knowledge with pattern (one-time cost)
  3. Add regex for "action:" keywords (minimal cost)
```

## Integration

### From Command Line

// turbo
```bash
python 8825_core/agents/auditor_agent.py \
  --output-file "$OUTPUT_FILE" \
  --workflow-type "$WORKFLOW_TYPE" \
  --report-dir audits/ \
  --verbose
```

### From Python

```python
from agents.auditor_agent import AuditorAgent

auditor = AuditorAgent(verbose=True)
report = auditor.audit_workflow(
    workflow_output=output_data,
    workflow_type="meeting_automation",
    metadata={"workflow_id": "tgif_20251114"}
)

if report['overall_assessment']['verdict'] == 'PASS':
    print("✅ Automation working correctly")
else:
    print("⚠️ Issues found, review recommendations")
```

## Tips

1. **Run weekly** - Catch drift before it becomes a problem
2. **Check critical workflows** - Don't audit everything, focus on high-value
3. **Act on recommendations** - Implement efficiency improvements
4. **Track trends** - Are accuracy scores improving over time?
5. **Use verbose mode** - See what sources are being checked

## Troubleshooting

**"Sources unavailable"**
- Auditor continues with partial audit
- Notes missing sources in report
- Recommendations may be limited

**"Low confidence scores"**
- May indicate automation needs improvement
- Or context sources are insufficient
- Review recommendations for fixes

**"Audit takes too long"**
- Normal for first run (gathering context)
- Subsequent audits faster (cached data)
- Can skip sources with `--skip-sources`

## Next Steps

After audit:
1. Review verdict and scores
2. Check low-confidence findings
3. Implement high-priority recommendations
4. Re-run automation with improvements
5. Audit again to verify improvement

---

**Status:** Production Ready  
**Agent:** AGENT-AUDITOR-0001  
**Implementation:** `8825_core/agents/auditor_agent.py`
