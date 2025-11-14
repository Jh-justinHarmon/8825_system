# Content-Addressed Index System

## Overview

Replaces broken Lane A/B teaching ticket system with intelligent, self-managing content index.

## Key Features

### 1. **Intelligent Naming (LLM-Powered)**
- Reads file content
- Generates meaningful filenames automatically
- Extracts entities and categories
- Suggests destination folders

**Example:**
```
Input:  "20251111_note_1_2_3_4.md"
LLM reads content about RAL Portal API
Output: "RAL_Portal_API_Authentication_Guide.md"
Destination: "focuses/hcss/knowledge/"
```

### 2. **Content-Addressed Storage**
- Files identified by content hash (SHA256)
- Automatic deduplication
- No duplicate storage

### 3. **Full-Text Search (FTS5)**
- Instant search across all indexed files
- Search by keywords, entities, topics
- Results in < 50ms

### 4. **Confidence-Based Auto-Promotion**
- Confidence ≥ 0.85: Auto-promote to knowledge base
- Confidence ≥ 0.70: Suggest to user
- Confidence < 0.70: Wait for more signals

### 5. **Lifecycle Management**
- Fresh (0-7 days): New files
- Aging (7-30 days): Starting to age
- Stale (30-90 days): Probably not valuable
- Expired (90+ days): Auto-cleanup

### 6. **Usage-Based Learning**
- Tracks where files go
- Learns patterns over time
- Auto-promotes similar files

## Usage

### Ingest a File
```python
from index_engine import ContentIndexEngine

index = ContentIndexEngine()
result = index.ingest(Path('file.md'))

# Result includes:
# - Intelligent filename
# - Category and entities
# - Suggested destination
# - Confidence score
```

### Search
```bash
python search_cli.py "RAL Portal"
```

### Check Promotions
```python
from promotion_engine import PromotionEngine

promotion = PromotionEngine(...)
candidates = promotion.check_promotion_candidates()

# Auto-promote high-confidence files
for c in candidates:
    if c['auto_promote']:
        promotion.promote_file(c['hash'], c['destination'])
```

### Run Cleanup
```python
from cleanup_engine import CleanupEngine

cleanup = CleanupEngine(...)
stats = cleanup.daily_cleanup()

print(f"Deleted: {stats['deleted']}")
print(f"Archived: {stats['archived']}")
```

## Architecture

```
File arrives
    ↓
Intelligent Naming (LLM)
    ↓
Content Index (SQLite + FTS5)
    ↓
Confidence Scoring
    ↓
Auto-Promote (≥0.85) or Suggest (≥0.70)
    ↓
Usage Tracking & Learning
    ↓
Decay Management
    ↓
Auto-Cleanup (90+ days)
```

## Files

- `index_engine.py` - Core indexing with SQLite + FTS5
- `intelligent_naming.py` - LLM-powered filename generation
- `promotion_engine.py` - Confidence-based auto-promotion
- `decay_engine.py` - Lifecycle management
- `cleanup_engine.py` - Auto-archive/delete
- `usage_tracker.py` - Pattern learning
- `search_cli.py` - Interactive search interface
- `migrate.py` - Migration from old system

## Environment Variables

```bash
export OPENAI_API_KEY="your-key-here"
export OPENAI_MODEL="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini
```

## Integration

System is integrated with `ingestion_engine.py`:

```python
# Files in pending/ are automatically:
1. Analyzed by LLM for intelligent naming
2. Indexed with content hash
3. Checked for auto-promotion
4. Promoted or suggested based on confidence
```

## Migration

Migrate existing teaching tickets and Lane B files:

```bash
cd ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/8825_core/content_index
python migrate.py
```

## What This Solves

**Before:**
- 74 teaching tickets piling up
- Manual review required for every file
- Files with garbage names (20251111_note_1_2_3_4.md)
- Wrong attributions (ERD in personal folder)
- Duplicates everywhere

**After:**
- 0 teaching tickets
- Intelligent filenames automatically
- Auto-promotion when confident
- Clean, deduplicated storage
- Self-managing lifecycle
