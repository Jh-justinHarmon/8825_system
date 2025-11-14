# Additive Update Mode ✅

**Status:** Implemented  
**Date:** 2025-11-06  
**Version:** 2.1

---

## Critical Principle

### ⚠️ NEVER REMOVE EXISTING DATA

**Profile Builder is ADDITIVE ONLY**

When updating an existing profile:
- ✅ Add new information
- ✅ Fill empty fields
- ✅ Provide additional context
- ✅ Add verification
- ❌ **NEVER remove existing data**
- ❌ **NEVER overwrite user-provided content**

---

## Use Cases

### Scenario 1: Resume Upload First
```
1. User uploads resume → Library created with:
   - Work history from resume
   - Skills from resume
   - Education from resume
   
2. User runs Profile Builder (UPDATE mode) → Adds:
   - GitHub repos (verification)
   - Stack Overflow reputation (proof)
   - Awards (additional context)
   - Wikipedia bio (context)
   
3. Result: Resume data + Online data
   ✅ All resume data preserved
   ✅ New data added
```

### Scenario 2: Manual Entry First
```
1. User manually enters:
   - Custom bio
   - Specific projects
   - Curated skills
   
2. User runs Profile Builder (UPDATE mode) → Adds:
   - Evidence for skills
   - Additional projects
   - Verification data
   
3. Result: Manual data + Automated data
   ✅ Manual entries preserved
   ✅ Automated data added
```

### Scenario 3: Multiple Updates
```
1. First run: GitHub data
2. Second run (UPDATE): Wikipedia data added
3. Third run (UPDATE): Stack Overflow added
4. Fourth run (UPDATE): Awards added

Result: Cumulative data from all runs
✅ Nothing removed
✅ Everything preserved
```

---

## Modes

### CREATE Mode (Default)
```bash
python profile_builder.py torvalds
```

**Behavior:**
- Creates new library from scratch
- Overwrites existing library if present
- Use for first-time profile creation

### UPDATE Mode (Additive)
```bash
python profile_builder.py --update torvalds
```

**Behavior:**
- Loads existing library
- Merges new data with existing
- Preserves all existing data
- Only adds new information
- Use for enriching existing profiles

---

## Merge Logic

### Dictionary Merging
```python
Existing: {"name": "John Doe", "location": "SF"}
New:      {"location": "San Francisco", "company": "Google"}

Result:   {"name": "John Doe", "location": "SF", "company": "Google"}
          ✅ name preserved
          ✅ location preserved (existing takes priority)
          ✅ company added
```

### List Merging
```python
Existing: ["Python", "JavaScript"]
New:      ["JavaScript", "Ruby"]

Result:   ["Python", "JavaScript", "Ruby"]
          ✅ All items preserved
          ✅ New unique items added
          ✅ No duplicates
```

### Empty Field Filling
```python
Existing: {"bio": "", "company": "Google"}
New:      {"bio": "Developer", "company": "Microsoft"}

Result:   {"bio": "Developer", "company": "Google"}
          ✅ Empty bio filled
          ✅ Existing company preserved
```

---

## Output Examples

### UPDATE Mode Console
```
📂 Loaded existing library for torvalds
   Mode: UPDATE (additive only)

📡 Fetching GitHub data...
   ➕ Added new field: public_gists from github
   ➕ Filled empty field from github

💬 Fetching Stack Overflow data...
   ➕ Added new item from stackoverflow

✅ Profile updated!
   Preserved: 15 existing fields
   Added: 8 new fields
   Updated: 3 empty fields
```

---

## Data Preservation Rules

### Rule 1: Existing Data Wins
```python
if existing_value and new_value:
    return existing_value  # Keep existing
```

### Rule 2: Fill Empty Fields
```python
if not existing_value and new_value:
    return new_value  # Fill empty
```

### Rule 3: Merge Collections
```python
if isinstance(existing, list):
    return existing + unique_new_items  # Append unique
```

### Rule 4: Never Delete
```python
# NEVER do this:
if key not in new_data:
    del existing_data[key]  # ❌ FORBIDDEN
```

---

## Protected Fields

### Always Preserved
- User-entered data
- Resume data
- Manual entries
- Custom descriptions
- Curated lists
- Verified information

### Can Be Added To
- Skills lists
- Project lists
- Work history
- Awards
- Publications
- Social links

### Never Overwritten
- Names (unless empty)
- Locations (unless empty)
- Companies (unless empty)
- Bios (unless empty)
- Any non-empty field

---

## Use Cases by Source

### Resume Upload
```
Resume provides:
- Complete work history
- Education
- Skills
- Projects

Profile Builder adds:
- GitHub verification
- Online presence
- Additional projects
- Community reputation
```

### LinkedIn Import
```
LinkedIn provides:
- Current role
- Work history
- Connections

Profile Builder adds:
- GitHub repos
- Stack Overflow
- Awards
- Publications
```

### Manual Entry
```
User provides:
- Custom bio
- Selected projects
- Specific skills

Profile Builder adds:
- Evidence for skills
- Additional context
- Verification
- Completeness score
```

---

## Verification in UPDATE Mode

### Existing Data
```json
{
  "work_history": [
    {
      "company": "Google",
      "source": "resume",
      "verified": true
    }
  ]
}
```

### After UPDATE
```json
{
  "work_history": [
    {
      "company": "Google",
      "source": "resume",
      "verified": true
    },
    {
      "company": "Linux Foundation",
      "source": "github",
      "verified": true
    }
  ]
}
```

**Result:** Resume data preserved, GitHub data added

---

## Conflict Resolution

### Same Data, Different Sources
```python
Existing: {"company": "Google", "source": "resume"}
New:      {"company": "Google", "source": "github"}

Result:   {"company": "Google", "source": "resume"}
          ✅ First source preserved
          ✅ Verification note added
```

### Different Data, Same Field
```python
Existing: {"location": "San Francisco"}
New:      {"location": "SF"}

Result:   {"location": "San Francisco"}
          ✅ Existing preserved
          ⚠️  Warning: "Location mismatch detected"
```

---

## Benefits

### Data Safety
- No accidental deletions
- User data protected
- Resume data preserved
- Manual entries safe

### Incremental Enrichment
- Add data over time
- Multiple sources
- Cumulative improvement
- No data loss

### Verification
- Cross-source validation
- Evidence accumulation
- Confidence building
- Proof collection

---

## Warnings

### Data Conflicts
```
⚠️  Data Conflicts Detected:
   • Location: "San Francisco" (resume) vs "SF" (github)
   • Company: "Google" (linkedin) vs "Alphabet" (github)
   
💡 Existing data preserved. Review conflicts manually.
```

### Missing Data
```
ℹ️  New Data Available:
   • Stack Overflow reputation: 15,000
   • GitHub stars: 5,000+
   • Wikipedia biography found
   
✅ All new data added to profile
```

---

## Command Examples

### First Time (CREATE)
```bash
# Create new profile
python profile_builder.py johndoe
```

### After Resume Upload (UPDATE)
```bash
# Add online data to resume
python profile_builder.py --update johndoe
```

### After Manual Edits (UPDATE)
```bash
# Add verification to manual data
python profile_builder.py --update johndoe
```

### Periodic Refresh (UPDATE)
```bash
# Add new achievements/data
python profile_builder.py --update johndoe
```

---

## Integration with Joju

### Workflow
```
1. User uploads resume to Joju
   → Library created with resume data
   
2. User runs Profile Builder (UPDATE)
   → Online data added
   
3. User manually edits in Joju
   → Custom data added
   
4. User runs Profile Builder (UPDATE) again
   → New online data added, edits preserved
   
5. Result: Resume + Online + Manual
   ✅ All data preserved
   ✅ Fully enriched profile
```

---

## Summary

**Profile Builder is ADDITIVE ONLY:**
- ✅ Preserves all existing data
- ✅ Adds new information
- ✅ Fills empty fields
- ✅ Provides verification
- ✅ Accumulates evidence
- ❌ Never removes data
- ❌ Never overwrites user content

**Use UPDATE mode when:**
- Profile already exists
- Resume was uploaded
- Manual entries made
- Periodic refresh needed

**Use CREATE mode when:**
- First time creation
- Starting from scratch
- No existing data

---

**Data preservation is guaranteed in UPDATE mode!** 🔒
