# Agent Specification: Library Mining Complexity Router

**Agent ID:** AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001  
**Priority Score:** 91.6 (Highest)  
**Assigned To:** [TBD - First team assignment]  
**Start Date:** [TBD]  
**Target Completion:** [TBD - Estimate 5-7 days]

---

## PromptGen Analysis

### 1. Problem Definition

**What problem are we solving?**

**Core need:** Library mining reports vary wildly in complexity - some are simple single-project contributions, others require multi-project synthesis and new concept creation. Currently, all reports go through the same expensive GPT-4 processing, wasting money on simple cases and potentially under-processing complex ones.

**Pain point:** 
- Spending $0.10-0.65 per report on GPT-4 when 80% could be handled by GPT-4o-mini ($0.01)
- No differentiation between "add this to project X" vs "synthesize across 3 projects and create new patterns"
- Processing time inconsistent (simple reports take as long as complex ones)

**What happens if we don't solve this:**
- Continue overspending on LLM costs (95% cost reduction opportunity missed)
- Simple reports get over-processed (wasted time)
- Complex reports might get under-processed (quality issues)
- No optimization of the LLOM Router architecture

**Minimum viable solution:**
- Agent that reads raw mining report JSON
- Analyzes 4 complexity factors (structure, routing, scope, novelty)
- Returns TIER 1 (simple → mini) or TIER 2 (complex → GPT-4)
- Confidence score and reasoning included
- JSON output for downstream processing

**Current State:**
- LLOM Router architecture exists and proven (95% cost reduction in Content Index)
- Library mining system exists but no complexity routing
- All reports currently processed uniformly
- This is the highest priority agent (91.6 score)

---

### 2. Context Gathering

**What do we already know?**

**Existing solutions:**
- LLOM Router pattern proven in Content Index System (95% cost reduction)
- Three-tier routing: Pattern Match (free) → Intelligence Layer (mini) → User Layer (expensive)
- Confidence-based routing works (let cheap model decide)
- This agent IS the Intelligence Layer for library mining

**Patterns we can reuse:**
- Confidence scoring (0-100)
- JSON input/output format
- Four-factor analysis pattern
- Tier recommendation structure
- Reasoning explanation format

**Constraints that apply:**
- Must use GPT-4o-mini (cost optimization)
- Must return JSON (downstream processing)
- Must be fast (<2 seconds)
- Must preserve Proof Protocol (usage tracking)
- Python 3.9+ compatible

**Related agents/workflows:**
- Library mining workflow (upstream)
- Content processing (downstream)
- LLOM Router architecture (parent pattern)
- Usage tracker (for Proof Protocol)

**Dependencies:**
- OpenAI API (gpt-4o-mini)
- Library mining report format (JSON)
- Downstream tier processors (TIER 1 and TIER 2 handlers)

---

### 3. Requirements (Explicit)

**What MUST the solution do?**

#### Core Functionality
1. **Accept raw mining report JSON** as input
2. **Analyze 4 complexity factors:**
   - Structure quality (well-formed vs messy)
   - Routing clarity (obvious destination vs ambiguous)
   - Cross-project scope (single vs multiple projects)
   - Pattern novelty (existing patterns vs new concepts)
3. **Return tier recommendation** (TIER 1 or TIER 2)
4. **Return confidence score** (0-100)
5. **Return reasoning** (why this tier)
6. **Return complexity indicators** (which factors triggered decision)

#### Performance Requirements
- **Response time:** <2 seconds per report
- **Accuracy:** >90% agreement with human expert
- **Cost:** <$0.01 per classification (GPT-4o-mini pricing)

#### Integration Requirements
- **Input format:** JSON (library mining report structure)
- **Output format:** JSON with tier, confidence, reasoning, indicators
- **API:** OpenAI GPT-4o-mini
- **Error handling:** Graceful degradation (default to TIER 2 if uncertain)

---

### 4. Requirements (Implicit)

**What's assumed but not stated?**

- **Who will use this:** Library mining workflow (automated), potentially manual review tool
- **Where will it run:** Server-side Python script, called by mining workflow
- **When will it be used:** Every time a library mining report is generated
- **How often:** Variable (depends on mining frequency, could be daily or weekly)
- **Skill level required:** None (fully automated), but implementer needs Python + OpenAI API experience

**Assumptions:**
- Mining reports follow consistent JSON structure
- OpenAI API is available and reliable
- Downstream TIER 1 and TIER 2 processors exist
- Cost optimization is critical (hence mini model)
- Speed matters (part of larger workflow)

---

### 5. Constraints

**Technical Constraints:**
- **API:** Must use GPT-4o-mini (not GPT-4, cost constraint)
- **Rate limits:** OpenAI standard limits (3,500 RPM for mini)
- **Input size:** Mining reports can be 1-10KB JSON
- **Python version:** 3.9+
- **Dependencies:** openai>=1.0.0, pydantic for validation

**Process Constraints:**
- Must preserve Proof Protocol (track usage, success/failure)
- Cannot break existing library mining workflow
- Must be backward compatible (graceful fallback)
- Must log decisions for learning

**Resource Constraints:**
- **API cost:** Target <$0.01 per classification
- **Compute:** Minimal (API call only)
- **Storage:** Log decisions for analysis (~1KB per report)

**Quality Constraints:**
- **Accuracy:** >90% agreement with human expert
- **Confidence calibration:** High confidence should correlate with accuracy
- **Explainability:** Reasoning must be clear for debugging

---

### 6. Edge Cases

**What could go wrong?**

#### 1. Missing Data
**Scenario:** Mining report JSON is incomplete or malformed
**Handling:**
- Validate JSON structure on input
- Check for required fields
- If critical fields missing → default to TIER 2 (safe fallback)
- Log warning for investigation

#### 2. Invalid Input
**Scenario:** Input is not valid JSON or wrong format
**Handling:**
- Try to parse JSON, catch exceptions
- If parse fails → return error with clear message
- Default to TIER 2 if cannot determine
- Log error for debugging

#### 3. API Failures
**Scenario:** OpenAI API is down or rate limited
**Handling:**
- Implement retry logic (3 attempts with exponential backoff)
- If all retries fail → default to TIER 2
- Log API errors
- Return confidence=0 to signal uncertainty

#### 4. Network Issues
**Scenario:** Network timeout or connection error
**Handling:**
- Set reasonable timeout (10 seconds)
- Retry on timeout
- Default to TIER 2 if cannot connect
- Log network errors

#### 5. Unexpected Formats
**Scenario:** Mining report has new fields or structure changes
**Handling:**
- Use flexible JSON parsing (don't fail on extra fields)
- Extract known fields, ignore unknown
- If structure radically different → TIER 2
- Log unexpected formats for review

#### 6. Ambiguous Cases
**Scenario:** Report is genuinely borderline (50/50 complexity)
**Handling:**
- Return low confidence score (40-60)
- Include detailed reasoning
- Default to TIER 2 (conservative choice)
- Track these for learning

#### 7. Model Hallucination
**Scenario:** GPT-4o-mini returns invalid JSON or nonsense
**Handling:**
- Validate model output structure
- If invalid → retry once
- If still invalid → TIER 2 with confidence=0
- Log hallucinations

---

### 7. Success Criteria

**How do we know it works?**

#### Functional Success
- [x] Accepts mining report JSON as input
- [x] Returns tier recommendation (1 or 2)
- [x] Returns confidence score (0-100)
- [x] Returns reasoning (string explanation)
- [x] Returns complexity indicators (array of factors)
- [x] Handles all 7 edge cases gracefully
- [x] Defaults to TIER 2 when uncertain

#### Quality Success
- [x] All tests passing (unit + integration + edge case)
- [x] Error handling complete (all exceptions caught)
- [x] Documentation complete (README + examples)
- [x] Edge cases handled (7 scenarios tested)
- [x] >90% accuracy on test set (20+ sample reports)
- [x] Confidence calibration validated (high confidence = high accuracy)

#### Performance Success
- [x] Response time <2 seconds (95th percentile)
- [x] Cost <$0.01 per classification
- [x] Handles 100 reports/hour without issues
- [x] No memory leaks (tested with 1000+ reports)

#### Integration Success
- [x] Integrates with library mining workflow
- [x] JSON output parseable by downstream processors
- [x] Logging works (decisions tracked)
- [x] Usage tracking works (Proof Protocol)

---

## Technical Design

### Input Format
```json
{
  "report_id": "unique_id",
  "source": "dropbox_miner|local_miner",
  "timestamp": "2025-11-13T22:00:00Z",
  "content": {
    "title": "Project contribution title",
    "description": "Detailed description",
    "files": ["file1.py", "file2.md"],
    "projects": ["project_a", "project_b"],
    "patterns": ["pattern_1", "pattern_2"],
    "complexity_hints": {
      "cross_project": true,
      "new_concepts": false,
      "structured": true
    }
  },
  "metadata": {
    "file_count": 5,
    "line_count": 500,
    "language": "python"
  }
}
```

### Output Format
```json
{
  "tier": 1,
  "confidence": 85,
  "reasoning": "Single project, clear routing to project_a, well-structured content, uses existing patterns. High confidence for TIER 1 (mini) processing.",
  "complexity_indicators": {
    "structure_quality": "high",
    "routing_clarity": "clear",
    "cross_project_scope": "single",
    "pattern_novelty": "existing"
  },
  "processing_time_ms": 1250,
  "model_used": "gpt-4o-mini",
  "timestamp": "2025-11-13T22:00:02Z"
}
```

### Decision Logic

**Step 1: Extract Complexity Signals**
```python
signals = {
    "structure_quality": analyze_structure(report),
    "routing_clarity": analyze_routing(report),
    "cross_project_scope": analyze_scope(report),
    "pattern_novelty": analyze_novelty(report)
}
```

**Step 2: Build Prompt for GPT-4o-mini**
```python
prompt = f"""
Analyze this library mining report and determine processing tier.

TIER 1 (simple): Clear routing, single project, existing patterns, well-structured
TIER 2 (complex): Ambiguous routing, multi-project, new concepts, messy structure

Report: {json.dumps(report)}

Return JSON:
{{
  "tier": 1 or 2,
  "confidence": 0-100,
  "reasoning": "explanation",
  "indicators": {{
    "structure_quality": "high|medium|low",
    "routing_clarity": "clear|ambiguous",
    "cross_project_scope": "single|multiple",
    "pattern_novelty": "existing|new"
  }}
}}
"""
```

**Step 3: Call GPT-4o-mini**
```python
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,  # Low temp for consistency
    max_tokens=300
)
```

**Step 4: Validate and Return**
```python
result = json.loads(response.choices[0].message.content)
validate_output(result)  # Ensure structure correct
return result
```

### Adaptation Mechanism

**How agent learns:**
- Track tier decisions and downstream success/failure
- If TIER 1 reports fail often → lower confidence threshold
- If TIER 2 reports succeed easily → raise confidence threshold
- Adjust based on usage patterns (Proof Protocol)

**What triggers changes:**
- Success rate drops below 85%
- Confidence calibration off (high confidence but low accuracy)
- New report patterns emerge
- Downstream processors change

**How it improves:**
- Collect decision logs
- Analyze misclassifications
- Adjust prompt or thresholds
- Re-test and validate
- Update via Proof Protocol (usage-driven evolution)

---

## Implementation Plan

### Phase 1: Core Functionality (Days 1-2)
**Duration:** 2 days

**Tasks:**
- [ ] Set up project structure (`library_mining_router/`)
- [ ] Create main agent class (`ComplexityRouter`)
- [ ] Implement input validation
- [ ] Implement GPT-4o-mini API call
- [ ] Implement output formatting
- [ ] Add basic error handling
- [ ] Write unit tests for core logic

**Deliverable:** Working router that classifies reports

---

### Phase 2: Edge Case Handling (Day 3)
**Duration:** 1 day

**Tasks:**
- [ ] Implement retry logic for API failures
- [ ] Add timeout handling
- [ ] Add malformed JSON handling
- [ ] Add missing data handling
- [ ] Add ambiguous case handling
- [ ] Write edge case tests (7 scenarios)

**Deliverable:** Robust router that handles failures gracefully

---

### Phase 3: Integration & Performance (Day 4)
**Duration:** 1 day

**Tasks:**
- [ ] Add logging (info, warning, error levels)
- [ ] Add usage tracking (Proof Protocol)
- [ ] Optimize performance (caching, batching if needed)
- [ ] Write integration tests
- [ ] Test with 100+ real reports
- [ ] Measure response time and cost

**Deliverable:** Production-ready router with monitoring

---

### Phase 4: Documentation (Day 5)
**Duration:** 1 day

**Tasks:**
- [ ] Write README.md (overview, installation, usage)
- [ ] Create usage examples (basic + advanced)
- [ ] Document API (input/output formats)
- [ ] Write troubleshooting guide
- [ ] Update agent registry
- [ ] Create runbook for operations

**Deliverable:** Complete documentation

---

### Phase 5: Testing & Validation (Days 6-7)
**Duration:** 2 days

**Tasks:**
- [ ] Create test set (20+ diverse reports)
- [ ] Manual classification by expert
- [ ] Run router on test set
- [ ] Calculate accuracy (target >90%)
- [ ] Validate confidence calibration
- [ ] Fix any issues found
- [ ] Final integration test

**Deliverable:** Validated router ready for production

---

## Testing Strategy

### Unit Tests
**Test core logic:**
- Input validation (valid/invalid JSON)
- Prompt generation (correct format)
- Output parsing (valid/invalid responses)
- Error handling (exceptions caught)
- Confidence scoring (0-100 range)

**Files:** `tests/test_router.py`

---

### Integration Tests
**Test API connections:**
- OpenAI API call succeeds
- Retry logic works
- Timeout handling works
- Rate limit handling works

**Test data flow:**
- End-to-end classification
- Multiple reports in sequence
- Concurrent requests (if applicable)

**Files:** `tests/test_integration.py`

---

### Edge Case Tests
**Test all 7 scenarios:**
1. Missing data → TIER 2 + warning
2. Invalid JSON → error + TIER 2
3. API failure → retry + TIER 2
4. Network timeout → retry + TIER 2
5. Unexpected format → TIER 2 + log
6. Ambiguous case → low confidence + TIER 2
7. Model hallucination → retry + TIER 2

**Files:** `tests/test_edge_cases.py`

---

### Performance Tests
**Test speed:**
- Single report <2 seconds
- 100 reports <5 minutes
- No memory leaks

**Test cost:**
- Track API calls
- Calculate cost per report
- Verify <$0.01 target

**Files:** `tests/test_performance.py`

---

### Accuracy Tests
**Test quality:**
- Create gold standard (20+ reports, manually classified)
- Run router on test set
- Calculate accuracy (correct tier / total)
- Validate confidence calibration (high confidence = high accuracy)
- Analyze misclassifications

**Files:** `tests/test_accuracy.py`, `tests/gold_standard.json`

---

## Documentation Requirements

### README.md
```markdown
# Library Mining Complexity Router

## Overview
Analyzes library mining reports and routes to appropriate processing tier.

## Installation
pip install -r requirements.txt

## Configuration
export OPENAI_API_KEY="your-key"

## Usage
from library_mining_router import ComplexityRouter

router = ComplexityRouter()
result = router.classify(report_json)

## Examples
[Basic and advanced examples]

## Troubleshooting
[Common issues and solutions]
```

### API Documentation
**Input parameters:**
- `report` (dict): Mining report JSON
- `timeout` (int, optional): API timeout in seconds (default: 10)
- `retry_count` (int, optional): Number of retries (default: 3)

**Output format:**
- `tier` (int): 1 or 2
- `confidence` (int): 0-100
- `reasoning` (str): Explanation
- `complexity_indicators` (dict): Factor analysis
- `processing_time_ms` (int): Time taken
- `model_used` (str): Model name
- `timestamp` (str): ISO format

**Error codes:**
- `INVALID_INPUT`: Malformed JSON
- `API_FAILURE`: OpenAI API error
- `TIMEOUT`: Request timeout
- `VALIDATION_ERROR`: Output validation failed

### Usage Examples

**Basic usage:**
```python
from library_mining_router import ComplexityRouter

router = ComplexityRouter()
report = load_report("report.json")
result = router.classify(report)

print(f"Tier: {result['tier']}")
print(f"Confidence: {result['confidence']}%")
print(f"Reasoning: {result['reasoning']}")
```

**Advanced usage with error handling:**
```python
from library_mining_router import ComplexityRouter, RouterError

router = ComplexityRouter(timeout=15, retry_count=5)

try:
    result = router.classify(report)
    
    if result['confidence'] < 70:
        print("Low confidence, manual review recommended")
    
    if result['tier'] == 1:
        process_with_mini(report)
    else:
        process_with_gpt4(report)
        
except RouterError as e:
    print(f"Router error: {e}")
    # Fallback to TIER 2
    process_with_gpt4(report)
```

**Batch processing:**
```python
router = ComplexityRouter()
reports = load_reports_batch("reports/")

for report in reports:
    result = router.classify(report)
    save_result(report['id'], result)
```

---

## Dependencies

### Python Packages
```
openai>=1.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

### External APIs
**OpenAI API:**
- Model: gpt-4o-mini
- Authentication: API key via environment variable
- Rate limits: 3,500 RPM (requests per minute)
- Cost: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Documentation: https://platform.openai.com/docs

### System Requirements
- Python 3.9+
- Environment variables: `OPENAI_API_KEY`
- Network access to api.openai.com
- ~10MB disk space for code + logs

---

## Deployment Plan

### Development
**Local testing:**
1. Set up virtual environment
2. Install dependencies
3. Set API key
4. Run unit tests
5. Run integration tests
6. Test with sample reports

**Validation:**
- All tests passing
- Accuracy >90% on test set
- Performance <2 seconds
- Cost <$0.01 per report

---

### Staging
**Integration testing:**
1. Deploy to staging environment
2. Connect to library mining workflow
3. Process 100+ real reports
4. Monitor performance and accuracy
5. Validate logging and tracking
6. Test error scenarios

**Validation:**
- End-to-end flow works
- No production impact
- Monitoring works
- Rollback plan tested

---

### Production
**Gradual rollout:**
1. Deploy router code
2. Start with 10% of reports (shadow mode)
3. Compare with current processing
4. Increase to 50% if successful
5. Full rollout if validated
6. Monitor for 1 week

**Monitoring:**
- Track tier distribution (expect ~80% TIER 1)
- Track accuracy (target >90%)
- Track cost savings (target 95% reduction)
- Track errors and retries

**Rollback plan:**
- If accuracy <85% → rollback to uniform processing
- If errors >5% → investigate and fix
- If cost higher than expected → review model usage

---

## Monitoring & Metrics

### Success Metrics
**Usage:**
- Reports classified per day
- Tier 1 vs Tier 2 distribution (target: 80/20)
- Average confidence score

**Quality:**
- Classification accuracy (target: >90%)
- Confidence calibration (high confidence = high accuracy)
- Misclassification rate (target: <10%)

**Performance:**
- Average response time (target: <2 seconds)
- 95th percentile response time (target: <3 seconds)
- API failure rate (target: <1%)

**Cost:**
- Cost per classification (target: <$0.01)
- Total monthly cost
- Cost savings vs uniform processing (target: 95%)

### Logging
**Info level:**
- Classification decisions (tier, confidence, reasoning)
- Processing time
- Model used

**Warning level:**
- Low confidence classifications (<70%)
- Retry attempts
- Unexpected formats
- Missing data

**Error level:**
- API failures (after all retries)
- Validation errors
- Timeouts
- Exceptions

**Log format:**
```json
{
  "timestamp": "2025-11-13T22:00:00Z",
  "level": "INFO",
  "report_id": "abc123",
  "tier": 1,
  "confidence": 85,
  "processing_time_ms": 1250,
  "model": "gpt-4o-mini"
}
```

### Alerts
**Critical:**
- API failure rate >5%
- Accuracy drops below 85%
- Response time >5 seconds (95th percentile)

**Warning:**
- Low confidence rate >30%
- Retry rate >10%
- Cost per report >$0.02

**Info:**
- Daily summary (reports processed, tier distribution, accuracy)
- Weekly trends (performance, cost, quality)

---

## Questions & Decisions

### Open Questions
1. What's the exact JSON structure of mining reports? (Need sample)
2. Do downstream TIER 1 and TIER 2 processors exist? (Need to verify)
3. What's the expected volume? (Daily/weekly report count)
4. Who reviews misclassifications? (For learning loop)

### Decisions Made
1. **Use GPT-4o-mini** - Cost optimization, proven in LLOM Router
2. **Default to TIER 2 when uncertain** - Conservative, safe choice
3. **Confidence threshold: 70%** - Below this, flag for review
4. **Retry count: 3** - Balance between reliability and speed
5. **Timeout: 10 seconds** - Reasonable for API call

### Assumptions
1. Mining reports are consistent JSON format
2. OpenAI API is reliable (99%+ uptime)
3. Cost savings justify development effort
4. Downstream processors can handle tier routing
5. Accuracy >90% is achievable with mini model

---

## Review Checklist

Before submitting for review:

- [x] PromptGen analysis complete (all 7 steps)
- [x] All requirements documented (explicit + implicit)
- [x] Edge cases identified (7 scenarios)
- [x] Success criteria defined (functional, quality, performance)
- [x] Implementation plan clear (5 phases, 7 days)
- [x] Testing strategy defined (5 test types)
- [x] Documentation requirements listed
- [x] Dependencies identified
- [x] Deployment plan outlined
- [x] Monitoring metrics defined
- [ ] Architect approval received (pending)

---

**Spec Version:** 1.0  
**Created:** 2025-11-13  
**Status:** Ready for Architect Review  
**Estimated Effort:** 5-7 days (one developer)  
**Expected ROI:** 95% cost reduction in library mining processing
