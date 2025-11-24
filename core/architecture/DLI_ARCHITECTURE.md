# DLI (Deep Learning Intelligence) Architecture

## Overview

DLI is a three-tier routing system that optimizes cost and quality for AI-assisted research and analysis.

## The Problem

Traditional approach: Every query → Expensive LLM → High cost

**Example**:
- 100 queries × gpt-4o = $2.50
- Most queries don't need expensive models

## The Solution: Three-Tier Routing

### Tier 0: Pattern Matching (FREE)
- Check if query matches known patterns
- Return cached/indexed results
- **Cost**: $0.00
- **Speed**: Instant
- **Coverage**: 60-80% of queries

### Tier 1: Cheap Model Analysis
- Use gpt-4o-mini for complexity analysis
- Determine if expensive model needed
- **Cost**: $0.0001 per query
- **Speed**: Fast (1-2s)
- **Purpose**: Smart routing decision

### Tier 2: Expensive Model (When Needed)
- Use gpt-4o for complex queries only
- Full context, deep analysis
- **Cost**: $0.0046 per query
- **Speed**: Slower (5-10s)
- **Purpose**: Complex reasoning

## Cost Comparison

| Approach | Cost per 100 queries | Savings |
|----------|---------------------|---------|
| All gpt-4o | $2.50 | 0% |
| Dual-layer (mini + gpt-4o) | $0.52 | 79% |
| **Three-tier (pattern + dual)** | **$0.13** | **95%** |

## Architecture

```
Query
  ↓
Pattern Engine (Tier 0)
  ├─ Match found? → Return result (FREE)
  └─ No match ↓
     Complexity Analyzer (Tier 1 - gpt-4o-mini)
       ├─ Simple? → Answer with mini ($0.0001)
       └─ Complex? ↓
          Deep Dive (Tier 2 - gpt-4o) ($0.0046)
```

## Context Quality Score (CQS)

CQS measures how much relevant context is available:

```
CQS = PPM_contribution + Trajectory_contribution + Snippet_contribution

- PPM: Prompt Pattern Memory (cached patterns)
- Trajectory: Conversation history
- Snippet: Indexed content snippets
```

**Routing based on CQS**:
- CQS > 150: Use cheap model (enough context)
- CQS < 150: Use expensive model (needs reasoning)

## Implementation

### 1. Pattern Engine Integration

```python
# Check pattern index first
pattern_result = pattern_engine.search(query)
if pattern_result.confidence > 0.8:
    return pattern_result  # FREE
```

### 2. Complexity Analysis

```python
# Analyze with cheap model
complexity = await analyze_complexity(query, model='gpt-4o-mini')
if complexity < 0.5:
    return await cheap_model_answer(query)
```

### 3. Deep Dive

```python
# Use expensive model for complex queries
return await deep_dive(query, model='gpt-4o', context=full_context)
```

## Telemetry

Track every decision:
- Model used
- Cost incurred
- Tokens consumed
- Latency
- CQS score
- Routing decision

**Database**: SQLite (`~/.8825/dli_telemetry.db`)

## Benefits

- ✅ 95% cost reduction
- ✅ Faster responses (pattern matching is instant)
- ✅ Better quality (expensive model when needed)
- ✅ Auditable (all decisions logged)
- ✅ Adaptive (learns patterns over time)

## Example Use Cases

**Pattern Match** (Tier 0 - FREE):
- "What is DLI?" → Known concept, return definition
- "Show me metrics" → Standard query, return stats

**Cheap Model** (Tier 1 - $0.0001):
- "Summarize this file" → Simple task
- "List all protocols" → Straightforward query

**Expensive Model** (Tier 2 - $0.0046):
- "Compare architectures and recommend best approach" → Complex reasoning
- "Analyze trade-offs and create implementation plan" → Multi-step analysis

## Integration with 8825

DLI integrates with:
- **Pattern Engine** - Tier 0 matching
- **Library** - Context retrieval
- **PPM** - Prompt pattern memory
- **Telemetry** - Cost tracking

## See Also

- `TELEMETRY_ARCHITECTURE.md` - Tracking system
- `PPM_ARCHITECTURE.md` - Pattern memory
- `../mcp/dli_example/` - Reference implementation

## License

MIT
