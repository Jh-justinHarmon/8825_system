# Dropbox File Reduction Strategy - Brainstorm

**Status:** Draft  
**Created:** 2025-11-09  
**Context:** Piggyback on contributions deduplication scan  
**Goal:** Reduce Dropbox storage by identifying and archiving/removing duplicate files

---

## 📋 Executive Summary

**Opportunity:** While scanning Dropbox for contribution mining, we can simultaneously:
1. **Identify duplicate files** (same content, different paths)
2. **Calculate potential space savings**
3. **Archive or remove duplicates** (with user confirmation)

**Estimated Impact:** 10-20% storage reduction (industry average for creative files)

---

## 🎯 Two-Phase Approach

### Phase 1: Contribution Deduplication
**Purpose:** Merge duplicate contributions across platforms  
**Scope:** 
- Local Dropbox files
- Figma files
- Behance projects
- etc.

**Method:**
- Content hash (MD5)
- Metadata similarity (name, date, size)
- User review & confirmation

### Phase 2: File Storage Reduction (Piggyback)
**Purpose:** Reduce Dropbox storage footprint  
**Scope:** All files in Dropbox scan  
**Method:** Same deduplication algorithm, different action (archive/delete vs merge)

---

## 🔍 Deduplication Algorithm

### Step 1: Content Hashing
```python
import hashlib

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
```

### Step 2: Group by Hash
```python
duplicates = {}
for file in all_files:
    hash_key = calculate_file_hash(file.path)
    if hash_key not in duplicates:
        duplicates[hash_key] = []
    duplicates[hash_key].append(file)

# Filter to only groups with 2+ files
duplicate_groups = {k: v for k, v in duplicates.items() if len(v) > 1}
```

### Step 3: Select Keep vs Archive
```python
for hash_key, files in duplicate_groups.items():
    # Sort by: 1) Most recent, 2) Shortest path, 3) Alphabetical
    sorted_files = sorted(files, key=lambda f: (
        -f.modified_date.timestamp(),  # Newest first
        len(f.path),                   # Shortest path
        f.path                         # Alphabetical
    ))
    
    keep_file = sorted_files[0]
    archive_files = sorted_files[1:]
    
    yield {
        'keep': keep_file,
        'archive': archive_files,
        'size_saved': sum(f.size for f in archive_files)
    }
```

---

## 📊 Space Savings Estimation

### Calculation Method
```python
def estimate_savings(scan_results):
    total_size = sum(f.size for f in scan_results['all_files'])
    duplicate_size = sum(
        f.size 
        for group in scan_results['duplicate_groups'].values() 
        for f in group[1:]  # All but first (keep) file
    )
    
    return {
        'total_files': len(scan_results['all_files']),
        'duplicate_count': sum(len(g)-1 for g in scan_results['duplicate_groups'].values()),
        'total_size_gb': total_size / (1024**3),
        'duplicate_size_gb': duplicate_size / (1024**3),
        'savings_percent': (duplicate_size / total_size) * 100 if total_size > 0 else 0
    }
```

### Expected Results
```
Example Output:
- Total files scanned: 50,000
- Duplicate files found: 5,234 (10.5%)
- Total storage: 487 GB
- Duplicate storage: 73 GB (15%)
- Potential savings: 73 GB
```

---

## 🛡️ Safety Measures

### 1. Never Auto-Delete
- ALWAYS archive first
- NEVER delete without explicit user confirmation
- Keep deleted files in archive for 30 days minimum

### 2. Archive Structure
```
/Dropbox/Archive/Duplicates_YYYY-MM-DD/
  ├── manifest.json (what was archived, where from, hash)
  ├── file1_copy.ai
  ├── file2_duplicate.psd
  └── ...
```

### 3. Manifest File
```json
{
  "archive_date": "2025-01-15",
  "kept_files": [
    {
      "path": "/Public/Design/project.ai",
      "hash": "abc123...",
      "size": 125829120,
      "reason": "Most recent version"
    }
  ],
  "archived_files": [
    {
      "original_path": "/Clients/OldProject/project_copy.ai",
      "archive_path": "/Archive/Duplicates_2025-01-15/project_copy.ai",
      "hash": "abc123...",
      "size": 125829120,
      "reason": "Duplicate of /Public/Design/project.ai"
    }
  ],
  "total_saved_bytes": 125829120
}
```

### 4. Rollback Capability
```python
def rollback_archive(manifest_path):
    """Restore all archived files to original locations"""
    manifest = load_json(manifest_path)
    for file in manifest['archived_files']:
        restore_file(file['archive_path'], file['original_path'])
    # Update manifest
    manifest['rollback_date'] = datetime.now()
    save_json(manifest_path, manifest)
```

---

## 👤 User Flows

### Flow 1: Review Before Archive
```
1. Scan completes
2. Show summary: "Found 5,234 duplicates (73 GB)"
3. User clicks "Review duplicates"
4. Show grouped list:
   ├─ project.ai (3 copies, 125 MB each)
   │  ✓ /Public/Design/project.ai (keep - newest)
   │  □ /Clients/Old/project_copy.ai (archive)
   │  □ /Archive/2024/project.ai (archive)
5. User can:
   - Change which to keep
   - Exclude groups from archive
   - Select all → Archive
6. Confirm: "Archive 5,234 files and save 73 GB?"
7. Execute → Show progress
8. Done: "Archived to /Archive/Duplicates_2025-01-15"
```

### Flow 2: Auto-Archive (Aggressive)
```
1. Scan completes
2. User sets policy: "Auto-archive duplicates"
3. System archives automatically
4. Email summary: "Archived 5,234 files, saved 73 GB"
5. User can rollback for 30 days
```

### Flow 3: Report Only (Conservative)
```
1. Scan completes
2. Export report: duplicates_report.csv
3. User manually reviews and deletes
4. No automation
```

---

## 🔗 Integration with Contribution Deduplication

### Shared Scanner
```python
class UnifiedScanner:
    def __init__(self, root_path):
        self.root_path = root_path
        self.files = []
        self.hashes = {}
    
    def scan(self):
        # Single pass through all files
        for file in walk_directory(self.root_path):
            hash_key = calculate_file_hash(file.path)
            
            # Track for file reduction
            if hash_key not in self.hashes:
                self.hashes[hash_key] = []
            self.hashes[hash_key].append(file)
            
            # Track for contribution mining
            if is_design_file(file):
                self.files.append(file)
    
    def get_contributions(self):
        # Return deduplicated contributions
        pass
    
    def get_duplicate_files(self):
        # Return file reduction opportunities
        return {k: v for k, v in self.hashes.items() if len(v) > 1}
```

---

## 📈 Prelim Plan

### MVP (With Contribution Scanner)
**Scope:** Report only
- Calculate hashes during contribution scan
- Generate duplicate files report
- Estimate savings
- NO archiving/deletion

**Timeline:** +2 days to contribution scanner

### Phase 2 (File Reduction Tool)
**Scope:** Archive duplicates
- User review interface
- Archive to designated folder
- Manifest generation
- Rollback capability

**Timeline:** +1 week

### Phase 3 (Advanced)
**Scope:** Smart policies
- Auto-archive rules
- Scheduled scans
- Analytics dashboard
- Integration with Dropbox API (move to cold storage)

**Timeline:** +2 weeks

---

## 🎯 Success Metrics

### Technical
- Scan 50,000+ files in < 30 minutes
- 0 false positives (identical content = duplicate)
- 100% rollback success rate

### Business
- Save 10-20% storage
- Reduce Dropbox costs
- User satisfaction: "Helpful" > 80%

---

## ⚠️ Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Delete wrong file | HIGH | Never auto-delete, archive first, 30-day retention |
| Corrupt during move | MEDIUM | Verify hash after archive, keep original until verified |
| User loses work | HIGH | Manifest tracks all moves, rollback in one click |
| Performance impact | LOW | Run scan during low usage (night), show progress |
| False positives | LOW | Hash-based (MD5) is highly accurate |

---

## 📋 Next Steps

1. **Discuss in Matthew 1:1**
   - Validate approach
   - Decide on MVP scope
   - Assess risk tolerance

2. **Add to contribution scanner** (MVP: Report only)
   - Track hashes
   - Generate report
   - Estimate savings

3. **Run on full Dropbox** (test)
   - Calculate actual savings
   - Validate performance
   - Check for edge cases

4. **Build archive tool** (Phase 2)
   - If savings justify effort
   - User review UI
   - Safety measures

---

## 📚 References

- Contribution deduplication: See joju_contributions_pipeline_brainstorm.md
- Local miner: See local_miner.py
- Related exploration: [Check if dropbox_file_reduction.md exists]
