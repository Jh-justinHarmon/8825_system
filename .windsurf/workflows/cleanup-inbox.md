---
description: Clean up Downloads inbox immediately after processing
---

# Cleanup Inbox Protocol

## CRITICAL RULE

**When you say "processed" or "inbox is clean", it MUST be true immediately.**

## The Problem

Files stay in Downloads after being processed, causing:
- Reprocessing the same files
- False "inbox is clean" statements
- User confusion and wasted time

## The Solution

**Move files IMMEDIATELY after processing, not at end of session.**

## Cleanup Steps

### 1. After Processing Any File

```bash
# Create dated archive folder
mkdir -p ~/Downloads/8825_processed/$(date +%Y-%m-%d)

# Move the processed file
mv ~/Downloads/[filename] ~/Downloads/8825_processed/$(date +%Y-%m-%d)/
```

### 2. Verify Cleanup

```bash
# Check that file is gone
ls ~/Downloads/[filename]  # Should error "no such file"

# Verify it's archived
ls ~/Downloads/8825_processed/$(date +%Y-%m-%d)/[filename]  # Should exist
```

### 3. Only Then Say "Processed"

**NEVER say:**
- "Processed" 
- "Inbox is clean"
- "All done"

**UNTIL the file is actually moved.**

## Batch Cleanup

For multiple files:

```bash
# Create archive folder
mkdir -p ~/Downloads/8825_processed/brainstorms_$(date +%Y-%m-%d)

# Move all processed files
mv ~/Downloads/8825_*_brainstorm_*.txt ~/Downloads/8825_processed/brainstorms_$(date +%Y-%m-%d)/

# Verify
ls ~/Downloads/8825_*.txt  # Should error "no matches"
```

## When to Clean

**Immediately after:**
- ✅ Creating exploration from brainstorm
- ✅ Processing bill/receipt
- ✅ OCR'ing sticky notes
- ✅ Mining chat transcripts
- ✅ Any file transformation

**NOT at:**
- ❌ End of session
- ❌ When user asks
- ❌ "Later"

## Archive Structure

```
~/Downloads/8825_processed/
├── 2025-11-09/
│   ├── bill_electric_nov.pdf
│   └── sticky_notes_photo.jpeg
├── brainstorms_2025-11-09/
│   ├── contractor_bid_tool.txt
│   └── low_friction_onboarding.txt
└── receipts_2025-11/
    └── amazon_order_123.pdf
```

## Verification Command

Before saying "inbox is clean":

```bash
find ~/Downloads -maxdepth 1 -type f \
  \( -name "8825_*.txt" \
  -o -name "*bill*.pdf" \
  -o -name "*receipt*.pdf" \
  -o -name "sticky*.jpeg" \
  -o -name "sticky*.png" \) \
  -mtime -7
```

**If this returns ANY files, inbox is NOT clean.**

## Example Workflow

```bash
# 1. Process brainstorm
# ... create exploration file ...

# 2. IMMEDIATELY clean up
mkdir -p ~/Downloads/8825_processed/brainstorms_2025-11-09
mv ~/Downloads/8825_contractor_bid_tool.txt ~/Downloads/8825_processed/brainstorms_2025-11-09/

# 3. Verify
ls ~/Downloads/8825_contractor_bid_tool.txt  # Should error

# 4. ONLY NOW say "Processed"
echo "✅ Contractor Bid Tool brainstorm processed and archived"
```

## Recovery

If you realize you said "clean" but didn't move files:

```bash
# 1. Acknowledge the mistake
echo "⚠️ Files not yet archived. Cleaning up now..."

# 2. Move them immediately
# ... cleanup commands ...

# 3. Confirm
echo "✅ NOW inbox is actually clean"
```

## Integration with Tools

### Bill Processor
After processing, should automatically:
```python
# Move to processed folder
processed_dir = Path.home() / 'Downloads' / '8825_processed' / 'bills'
processed_dir.mkdir(parents=True, exist_ok=True)
shutil.move(image_path, processed_dir / image_path.name)
```

### Sticky Notes
After OCR, should automatically:
```python
# Move to processed folder
processed_dir = Path.home() / 'Downloads' / '8825_processed' / 'stickies'
processed_dir.mkdir(parents=True, exist_ok=True)
shutil.move(image_path, processed_dir / image_path.name)
```

## The Contract

**When I say "inbox is clean", you should be able to run:**

```bash
ls ~/Downloads/8825_*.txt ~/Downloads/*bill*.pdf ~/Downloads/sticky*.{jpeg,png} 2>&1
```

**And see:** `zsh: no matches found`

**If not, I broke the contract.**

---

**Remember: "Processed" means MOVED, not just "read and understood".**
