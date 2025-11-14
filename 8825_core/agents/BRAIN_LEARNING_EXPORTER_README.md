# Brain Learning Exporter

**Status:** ✅ Ready to use  
**Created:** 2025-11-13  
**Repurposed from:** AGENT-LIBRARY-CHAT-MINING-0001

---

## Purpose

Export brain learnings to external formats for:
- Documentation (markdown)
- Sharing with external LLMs (JSON, Cascade format)
- Analysis (mining report format)
- Knowledge transfer

**Key difference from original Chat Mining Agent:**
- Leverages brain's `learning_extractor.py` and `auto_memory_creator.py`
- No reinvention - uses same extraction patterns as internal brain
- Includes modern features: time decay, usage tracking, confidence scoring

---

## Quick Start

### Export brain memories to markdown
```bash
python3 brain_learning_exporter.py --source brain --format markdown --output learnings.md
```

### Extract from checkpoint and export as JSON
```bash
python3 brain_learning_exporter.py --source checkpoint --source-path checkpoint.md --format json
```

### Export high-confidence learnings only
```bash
python3 brain_learning_exporter.py --source brain --format cascade --min-confidence 0.8
```

---

## Features

### Source Types
1. **`brain`** - Load from brain's memory store (`~/.8825/auto_memories.json`)
2. **`checkpoint`** - Extract from checkpoint summary file
3. **`text`** - Extract from arbitrary text file

### Export Formats
1. **`mining_report`** - Original format with patterns/lexicon/agents
2. **`cascade`** - Cascade memory system format (for import)
3. **`markdown`** - Human-readable documentation
4. **`json`** - Structured data for external systems

### Filters
- **`--type`** - Filter by learning type (decision, pattern, policy, solution, mistake)
- **`--tags`** - Filter by tags (space-separated)
- **`--min-confidence`** - Minimum confidence threshold (0.0-1.0)

---

## Modern Features (from Brain)

### 1. Time-Based Decay
- 6-month half-life by default
- `current_confidence = confidence * 0.5^(age_days / half_life_days)`
- Older learnings decay in confidence

### 2. Usage Tracking
- **Tries:** How many times applied
- **Successes:** How many times worked
- **Failures:** How many times failed
- **Success rate:** Calculated automatically

### 3. Multi-Source Provenance
- Tracks all sources where learning appeared
- Tracks all contexts where validated
- Update count for merged learnings

### 4. Learning Types (5)
- **Decision:** Why we chose X over Y
- **Pattern:** Recurring solutions
- **Policy:** Rules established
- **Solution:** What worked
- **Mistake:** What didn't work

### 5. Confidence Scoring
- Initial confidence (0.0-1.0)
- Current confidence (with decay)
- High/medium/low distribution

### 6. Tool Evolution Tracking
- Tracks tools used in learning
- Version information
- Release dates

### 7. Supersession Chains
- Learning A supersedes Learning B
- Status: active, legacy, deprecated, archived

---

## Examples

### Export all brain learnings to markdown
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format markdown \
  --output brain_learnings.md
```

### Export high-confidence decisions only
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format json \
  --type decision \
  --min-confidence 0.8 \
  --output decisions.json
```

### Extract learnings from checkpoint
```bash
python3 brain_learning_exporter.py \
  --source checkpoint \
  --source-path ~/Downloads/checkpoint_14.md \
  --format cascade \
  --output checkpoint_learnings.json
```

### Export learnings with specific tags
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format markdown \
  --tags meeting_automation api_keys \
  --output tagged_learnings.md
```

---

## Output Examples

### Markdown Format
```markdown
# Brain Learnings Export

**Exported:** 2025-11-13T18:50:00
**Total Learnings:** 42

## Decisions (12)

### Use Keychain for API key storage

**Confidence:** 0.90 (current: 0.85)
**Age:** 15 days
**Usage:** 5 tries, 100.0% success rate

Decided to use macOS Keychain over environment variables because...

**Context:** API key management for meeting automation

**Tags:** api_keys, security, keychain

---
```

### JSON Format
```json
{
  "learnings": [
    {
      "type": "decision",
      "title": "Use Keychain for API key storage",
      "content": "Decided to use macOS Keychain...",
      "confidence": 0.9,
      "current_confidence": 0.85,
      "age_days": 15,
      "tries": 5,
      "successes": 5,
      "success_rate": 1.0,
      "tags": ["api_keys", "security"],
      "sources": ["checkpoint_12", "checkpoint_14"]
    }
  ],
  "metadata": {
    "total": 42,
    "by_type": {
      "decision": 12,
      "pattern": 8,
      "solution": 15,
      "mistake": 7
    },
    "confidence_distribution": {
      "high (0.8-1.0)": 25,
      "medium (0.5-0.8)": 12,
      "low (0.0-0.5)": 5
    }
  }
}
```

### Cascade Memory Format
```json
[
  {
    "Title": "Use Keychain for API key storage",
    "Content": "Decided to use macOS Keychain...",
    "Tags": ["api_keys", "security", "keychain"],
    "UserTriggered": false,
    "Metadata": {
      "type": "decision",
      "confidence": 0.9,
      "current_confidence": 0.85,
      "age_days": 15,
      "success_rate": 1.0
    }
  }
]
```

---

## Integration with Brain

### Brain Components Used
1. **`learning_extractor.py`**
   - Extraction patterns (strong/medium signals)
   - Learning classification (5 types)
   - Context validation

2. **`auto_memory_creator.py`**
   - Deduplication (similarity detection)
   - Memory merging
   - Provenance tracking

3. **`Learning` dataclass**
   - All fields preserved
   - Confidence with decay
   - Usage tracking
   - Evolution tracking

### Consistency Guarantee
- Same extraction patterns as brain
- Same confidence scoring
- Same decay calculations
- No divergence between internal/external formats

---

## Use Cases

### 1. Documentation
Export brain learnings to markdown for documentation:
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format markdown \
  --min-confidence 0.7 \
  --output docs/learnings.md
```

### 2. External LLM Training
Export to JSON for training external LLMs:
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format json \
  --output training_data.json
```

### 3. Cascade Memory Import
Export to Cascade format for import into another system:
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format cascade \
  --min-confidence 0.8 \
  --output cascade_import.json
```

### 4. Checkpoint Analysis
Extract learnings from specific checkpoint:
```bash
python3 brain_learning_exporter.py \
  --source checkpoint \
  --source-path checkpoint_14.md \
  --format markdown \
  --output checkpoint_14_learnings.md
```

### 5. Pattern Analysis
Export only patterns for analysis:
```bash
python3 brain_learning_exporter.py \
  --source brain \
  --format json \
  --type pattern \
  --output patterns.json
```

---

## Comparison: Old vs New

### Old Chat Mining Agent
- Manual trigger
- Reinvented extraction logic
- No consistency with brain
- Static output format
- No usage tracking
- No time decay

### New Brain Learning Exporter
- ✅ Leverages brain's extraction patterns
- ✅ Consistent with internal brain format
- ✅ Multiple export formats
- ✅ Includes usage tracking
- ✅ Includes time decay
- ✅ Includes confidence scoring
- ✅ Includes provenance
- ✅ Includes supersession chains

---

## Statistics in Output

Every export includes metadata:
- Total learnings
- Count by type
- Confidence distribution (high/medium/low)
- Date range (earliest/latest)
- Usage stats (tries, successes, success rate)
- Export timestamp

---

## Next Steps

### Potential Enhancements
1. **Date range filtering** - Filter by creation date
2. **Status filtering** - Filter by active/legacy/deprecated
3. **Success rate filtering** - Filter by usage success rate
4. **Tool filtering** - Filter by tools used
5. **Context filtering** - Filter by validation contexts
6. **Supersession filtering** - Show only active (not superseded)

### Integration Opportunities
1. **Automated exports** - Daily/weekly exports to docs
2. **Brain daemon integration** - Export on schedule
3. **Cascade import tool** - Direct import to Cascade
4. **Web dashboard** - View learnings in browser
5. **Search interface** - Full-text search across learnings

---

## File Location

**Script:** `8825_core/agents/brain_learning_exporter.py`  
**Registry:** `8825_core/agents/agent_registry.json` (AGENT-LIBRARY-CHAT-MINING-0001)  
**Brain components:** `8825_core/brain/`

---

## Status

✅ **Ready to use**  
✅ **Leverages brain components**  
✅ **Multiple export formats**  
✅ **Comprehensive filtering**  
✅ **Includes all modern features**

**The Chat Mining Agent is now a proper export tool, not a redundant implementation.**
