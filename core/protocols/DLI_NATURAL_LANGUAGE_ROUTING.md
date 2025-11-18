# DLI Natural Language Routing Protocol

⚠️ **SUPERSEDED - November 18, 2025**

This protocol has been replaced by the comprehensive **DLI Routing Protocol v1.0.0**.

**See:** `8825_core/protocols/DLI_ROUTING_PROTOCOL.md`

The new protocol is more comprehensive and includes:
- L0/L1/L2 knowledge layer separation (not just internal triggers)
- Authority vs Augmentor modes (for hybrid queries)
- Internal/External/Hybrid query classification
- Query phrasing guidance (improves results quality)
- 15 concrete examples with expected behavior
- Tested with 95% success rate across 9 scenarios

This original protocol was limited to internal triggers only. The new protocol handles external and hybrid queries as well.

---

**ORIGINAL PROTOCOL (for reference only):**

**Purpose:** Enable natural language triggers for DLI deep dives, making context gathering automatic and intuitive.

**Status:** Superseded → See DLI_ROUTING_PROTOCOL.md  
**Version:** 1.0.0  
**Date:** November 17, 2025

---

## Problem Statement

Currently, DLI is underutilized because:
1. Cascade doesn't automatically recognize when DLI should be used
2. Users must explicitly request "use DLI" or know the tool exists
3. Natural research/analysis requests default to basic grep/search

**Example from real session:**
> User: "deep dive on all backend/frontend processes... gather best practices... using cheap fast llm"
> 
> Cascade used: `code_search` + file reads (wrong)
> Should have used: `mcp1_dli_deep_dive` with pattern mode

---

## Solution: Natural Language Trigger System

### Architecture

```
User Request (Natural Language)
    ↓
Cascade Intent Detection
    ↓
Pattern Matching (Keywords/Phrases)
    ↓
┌─────────────────────────────────────────────────────┐
│ If matched → Route to DLI                           │
│ Else → Use standard tools                           │
└─────────────────────────────────────────────────────┘
    ↓
mcp1_dli_deep_dive(
  topic=extracted_topic,
  mode="pattern" or "baseline" or "both"
)
```

---

## Trigger Categories

### 1. Deep Analysis Triggers

**Keywords:**
- "deep dive"
- "analyze all"
- "comprehensive review"
- "research"
- "investigate"
- "explore"
- "study"

**Example Requests:**
```
"Deep dive on our HTML/UI patterns"
→ mcp1_dli_deep_dive(topic="HTML/UI patterns in 8825", mode="pattern")

"Analyze all our onboarding docs"
→ mcp1_dli_deep_dive(topic="onboarding documentation analysis", mode="pattern")

"Research how we handle authentication"
→ mcp1_dli_deep_dive(topic="authentication handling patterns", mode="pattern")
```

---

### 2. Pattern/Best Practice Triggers

**Keywords:**
- "best practices"
- "patterns"
- "common approaches"
- "how do we typically"
- "what's our strategy"
- "summarize our approach"

**Example Requests:**
```
"Gather best practices for frontend-backend wiring"
→ mcp1_dli_deep_dive(topic="frontend-backend wiring best practices", mode="pattern")

"What are the patterns for MCP server setup?"
→ mcp1_dli_deep_dive(topic="MCP server setup patterns", mode="pattern")

"How do we typically handle file routing?"
→ mcp1_dli_deep_dive(topic="file routing patterns and practices", mode="pattern")
```

---

### 3. Comparison Triggers

**Keywords:**
- "compare"
- "difference between"
- "evaluate options"
- "which is better"
- "pros and cons"
- "trade-offs"

**Example Requests:**
```
"Compare Goose vs Cascade for long tasks"
→ mcp1_dli_deep_dive(topic="Goose vs Cascade comparison for task types", mode="both")

"Evaluate options for user onboarding"
→ mcp1_dli_deep_dive(topic="user onboarding options evaluation", mode="pattern")

"What are the trade-offs of different routing strategies?"
→ mcp1_dli_deep_dive(topic="routing strategy trade-offs", mode="pattern")
```

---

### 4. Context Gathering Triggers

**Keywords:**
- "show me everything about"
- "what do we know about"
- "give me context on"
- "background on"
- "history of"
- "tell me about"

**Example Requests:**
```
"Show me everything about our DLI setup"
→ mcp1_dli_deep_dive(topic="DLI Router setup and configuration", mode="pattern")

"What do we know about Pattern Engine?"
→ mcp1_dli_deep_dive(topic="Pattern Engine architecture and usage", mode="pattern")

"Give me context on the learning integration workflow"
→ mcp1_dli_deep_dive(topic="learning integration workflow", mode="pattern")
```

---

### 5. Synthesis Triggers

**Keywords:**
- "summarize"
- "create a report on"
- "what have we learned"
- "key findings"
- "insights about"
- "wrap up"

**Example Requests:**
```
"Summarize our HTML development approach"
→ mcp1_dli_deep_dive(topic="HTML development approach summary", mode="pattern")

"What have we learned about MCP integration?"
→ mcp1_dli_deep_dive(topic="MCP integration learnings", mode="pattern")

"Key findings on user onboarding"
→ mcp1_dli_deep_dive(topic="user onboarding key findings", mode="pattern")
```

---

### 6. Metrics/Status Triggers

**Keywords:**
- "show me metrics"
- "how are we doing"
- "what's the status"
- "performance of"
- "stats on"
- "track record"

**Example Requests:**
```
"Show me metrics on DLI performance"
→ mcp1_dli_deep_dive(topic="DLI Router performance metrics and analysis", mode="pattern")

"How are we doing with cost optimization?"
→ mcp1_dli_deep_dive(topic="cost optimization performance and trends", mode="pattern")

"What's the status of our tracking systems?"
→ mcp1_dli_deep_dive(topic="tracking systems status and health", mode="pattern")
```

---

## Mode Selection Logic

### When to use `mode="pattern"`
- User wants 8825-specific context
- Looking for established patterns/practices
- Cost-sensitive (86% cheaper)
- **Default for most requests**

### When to use `mode="baseline"`
- Need fresh perspective without bias
- Exploring new territory
- Validating existing approaches

### When to use `mode="both"`
- Comparing approaches
- Validating Pattern Engine accuracy
- Important decisions needing multiple perspectives

---

## Implementation for Cascade

### Cascade's Internal Logic

```python
def should_use_dli(user_request: str) -> tuple[bool, str, str]:
    """
    Determine if DLI should be used based on user request.
    
    Returns:
        (should_use, topic, mode)
    """
    request_lower = user_request.lower()
    
    # Deep analysis triggers
    deep_triggers = [
        "deep dive", "analyze all", "comprehensive review",
        "research", "investigate", "explore", "study"
    ]
    
    # Pattern triggers
    pattern_triggers = [
        "best practices", "patterns", "common approaches",
        "how do we typically", "what's our strategy",
        "summarize our approach"
    ]
    
    # Comparison triggers
    comparison_triggers = [
        "compare", "difference between", "evaluate options",
        "which is better", "pros and cons", "trade-offs"
    ]
    
    # Context triggers
    context_triggers = [
        "show me everything", "what do we know",
        "give me context", "background on", "history of",
        "tell me about"
    ]
    
    # Synthesis triggers
    synthesis_triggers = [
        "summarize", "create a report", "what have we learned",
        "key findings", "insights about", "wrap up"
    ]
    
    # Metrics triggers
    metrics_triggers = [
        "show me metrics", "how are we doing", "what's the status",
        "performance of", "stats on", "track record"
    ]
    
    # Check for triggers
    for trigger in deep_triggers + pattern_triggers + context_triggers + synthesis_triggers + metrics_triggers:
        if trigger in request_lower:
            # Extract topic (everything after the trigger)
            topic = user_request.split(trigger, 1)[1].strip()
            mode = "both" if any(t in request_lower for t in comparison_triggers) else "pattern"
            return (True, topic, mode)
    
    return (False, "", "")
```

### Cascade's Response Pattern

**When DLI trigger detected:**
```
I'll use DLI to deep dive on [topic] with Pattern Engine context.

[Call mcp1_dli_deep_dive]

[Present results]
```

**When NOT detected:**
```
[Use standard tools: code_search, grep, read_file, etc.]
```

---

## Aliases for Power Users

### Short Commands

Users can also use explicit aliases:

```
"dli: analyze HTML patterns"
→ Direct DLI call

"pattern: best practices for MCP"
→ DLI with pattern mode

"baseline: fresh take on onboarding"
→ DLI with baseline mode

"compare: Goose vs Cascade"
→ DLI with both mode
```

---

## Examples from Real Session

### Example 1: Metrics Request

**User said:**
> "show me some metrics. how we doing"

**What happened:**
- Cascade used `mcp1_get_cost_stats` (direct MCP call)

**What should have happened:**
```python
mcp1_dli_deep_dive(
    topic="8825 system metrics, performance, and health status",
    mode="pattern"
)
```

**Why better:**
- Gets metrics + context from Pattern Engine
- Synthesizes trends and insights
- Provides recommendations

---

### Example 2: Deep Dive Request

**User said:**
> "deep dive on all backend/frontend processes... gather best practices... using cheap fast llm"

**What happened:**
- Cascade used `code_search` and file reads

**What should have happened:**
```python
mcp1_dli_deep_dive(
    topic="backend/frontend processes, UI development, dashboard patterns, and frontend-backend wiring best practices",
    mode="pattern"  # User explicitly said "cheap fast llm"
)
```

**Why better:**
- Pattern mode is 86% cheaper (user's requirement)
- Synthesizes across multiple files automatically
- Provides structured best practices summary

---

### Example 3: Evaluation Request

**User said:**
> "eval if dli was used at all in the previous interactions"

**What happened:**
- Cascade used `trajectory_search`

**What should have happened:**
```python
mcp1_dli_deep_dive(
    topic="DLI usage analysis in current conversation",
    mode="baseline"  # Fresh analysis without bias
)
```

**Why better:**
- Can analyze conversation patterns
- Identify missed opportunities
- Provide recommendations for future

---

## Benefits

### For Users
✅ **Natural language** - No need to know tool names  
✅ **Automatic routing** - System picks right tool  
✅ **Cost-effective** - Pattern mode by default  
✅ **Consistent** - Same phrases always work  

### For Cascade
✅ **Clear decision logic** - When to use DLI  
✅ **Better context** - Pattern Engine knowledge  
✅ **Fewer mistakes** - Right tool for the job  
✅ **Learning** - Patterns improve over time  

### For 8825 System
✅ **Higher DLI usage** - More telemetry data  
✅ **Better patterns** - More lookups = better PPM  
✅ **Cost tracking** - All deep dives logged  
✅ **Quality metrics** - CQS scores for all analyses  

---

## Implementation Checklist

### Phase 1: Cascade Training
- [ ] Add trigger detection to Cascade's system prompt
- [ ] Create decision tree for DLI routing
- [ ] Test with historical requests

### Phase 2: User Education
- [ ] Document trigger phrases in QUICK_START
- [ ] Add examples to DLI Router README
- [ ] Create cheat sheet of common patterns

### Phase 3: Monitoring
- [ ] Track DLI trigger accuracy
- [ ] Log false positives/negatives
- [ ] Refine trigger list based on usage

### Phase 4: Enhancement
- [ ] Add user feedback loop ("Was DLI helpful?")
- [ ] Expand trigger vocabulary
- [ ] Create domain-specific triggers (e.g., "joju: ..." routes to Joju context)

---

## Success Metrics

**Target:**
- 80% of deep analysis requests automatically route to DLI
- <5% false positive rate (DLI used when shouldn't be)
- User satisfaction with automatic routing

**Tracking:**
- DLI usage rate before/after implementation
- User corrections ("actually, just grep for this")
- Cost savings from pattern mode usage

---

## Future Enhancements

### Smart Mode Selection
```
User: "deep dive on HTML patterns"
System: Detects "patterns" → auto-selects pattern mode

User: "fresh perspective on onboarding"
System: Detects "fresh" → auto-selects baseline mode

User: "compare our approach vs industry standard"
System: Detects "compare" → auto-selects both mode
```

### Context-Aware Routing
```
User: "how does this work?" (while viewing file)
System: Uses file context + DLI for comprehensive answer

User: "what's the pattern here?" (in specific directory)
System: Scopes DLI to directory context
```

### Learning from Corrections
```
User: "deep dive on X"
Cascade: [Uses DLI]
User: "no, just grep for it"
System: Logs correction, adjusts trigger sensitivity
```

---

## Related Documentation

- **DLI Router MCP:** `dli_router_mcp/README.md`
- **Pattern Engine:** `8825_core/testing/ai_comparison_test/pattern_engine/`
- **Cascade Integration:** `.windsurf/settings.json`

---

**Status:** Ready for Implementation  
**Next Step:** Add trigger detection to Cascade system prompt  
**Owner:** Cascade AI / 8825 Team
