# Joju Dropbox Contribution Miner - Pipeline Design

**Status:** Exploration → Pipeline Design  
**Date:** 2025-11-09  
**Owner:** Justin Harmon (Jh)  
**Related:** `joju_dropbox_contribution_miner.md` (original brainstorm)

---

## 🎯 PROBLEM

**Goal:** Automatically populate Joju library with contributions from Dropbox files

**Challenge:** Attribution is complex
- Who created the file? (Dropbox uploader vs XMP creator)
- Who edited it? (Multiple revisions, multiple people)
- How to avoid double-counting? (Renames, copies, multi-save bursts)
- How to keep it updated? (Continuous monitoring)

**Use Case:** 
> "I've been designing logos in Illustrator for 5 years. All files are in Dropbox. I want Joju to show: 'Created 127 logos, Modified 89 client files' without manually entering each one."

---

## 💡 CORE CONCEPT

**Dropbox as Source of Truth → Joju as Display Layer**

```
Dropbox Files → Mine Metadata → Attribute Contributors → Export to Joju
```

**Key Insight:** Dropbox has the data, we just need to extract and structure it correctly.

---

## 🏗️ ARCHITECTURE

### **Pipeline Stages:**

```
1. DISCOVERY
   Scan Dropbox folder(s) → Find relevant files (.ai, .psd, .pdf, etc.)

2. METADATA EXTRACTION
   For each file:
   ├─ Dropbox API: file_id, path, content_hash, revisions, actors
   └─ XMP Parsing: dc:creator, modify_date, history (via ExifTool)

3. ATTRIBUTION RESOLUTION
   Merge Dropbox + XMP data → Determine creator & editors

4. DEDUPLICATION
   Handle renames, copies, multi-saves → Count each contribution once

5. AGGREGATION
   Roll up per person: files_created, files_modified, total_touches

6. EXPORT
   Generate Joju mining_report.json → Import to library
```

---

## 📊 DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    DROPBOX FOLDERS                           │
│  /Team/Design/Brand/  /Projects/Client_X/  /Archive/        │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  FOLDER SCANNER │
                    │  (Recursive)    │
                    └─────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
┌───────────────────┐                   ┌───────────────────┐
│  DROPBOX API      │                   │  XMP PARSER       │
│  - file_id        │                   │  - dc:creator     │
│  - content_hash   │                   │  - modify_date    │
│  - revisions      │                   │  - history        │
│  - actors         │                   │  (ExifTool)       │
└───────────────────┘                   └───────────────────┘
        ↓                                           ↓
        └─────────────────────┬─────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  ATTRIBUTION    │
                    │  RESOLVER       │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  DEDUPLICATOR   │
                    │  - file_id      │
                    │  - content_hash │
                    │  - revision     │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  AGGREGATOR     │
                    │  Per Person     │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  JOJU EXPORTER  │
                    │  mining_report  │
                    └─────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  JOJU LIBRARY   │
                    │  Auto-import    │
                    └─────────────────┘
```

---

## 🔍 ATTRIBUTION LOGIC

### **Challenge: Multiple Sources of Truth**

**Dropbox API says:**
- File uploaded by: `dbid:A1` (Jh)
- Last modified by: `dbid:B2` (Cam)

**XMP metadata says:**
- Creator: "Justin Harmon"
- Last modified: "Cameron Smith"

**Which to trust?**

---

### **Attribution Rules (Priority Order):**

```python
def resolve_creator(dropbox_data, xmp_data):
    # 1. Dropbox Business team_log (most reliable)
    if dropbox_data.has_team_log:
        return dropbox_data.team_log.creator
    
    # 2. Dropbox file metadata (uploader)
    if dropbox_data.uploader:
        return dropbox_data.uploader
    
    # 3. XMP dc:creator (fallback for old files)
    if xmp_data.dc_creator:
        return xmp_data.dc_creator
    
    # 4. Unknown
    return "Unknown"

def resolve_editors(dropbox_data, xmp_data):
    editors = set()
    
    # 1. Dropbox revisions (most reliable)
    for revision in dropbox_data.revisions:
        if revision.modifier:
            editors.add(revision.modifier)
    
    # 2. XMP history (if available)
    if xmp_data.history:
        for entry in xmp_data.history:
            if entry.modifier:
                editors.add(entry.modifier)
    
    # Remove creator from editors (don't double-count)
    creator = resolve_creator(dropbox_data, xmp_data)
    editors.discard(creator)
    
    return list(editors)
```

---

## 🚫 DEDUPLICATION STRATEGY

### **Problem: Same File, Multiple Identities**

**Scenario 1: Rename**
```
/Brand/logo_v1.ai → /Brand/logo_final.ai
```
**Solution:** Track by `file_id` (stays same across renames)

---

**Scenario 2: Copy**
```
/Brand/logo.ai → /Client_X/logo.ai (copied)
```
**Solution:** Track by `content_hash` (same content = same file)

---

**Scenario 3: Multi-Save Burst**
```
User saves file 5 times in 2 minutes
Dropbox creates 5 revisions
```
**Solution:** Collapse by `(file_id, actor, revision)` - count once per revision

---

**Scenario 4: Copy + Edit**
```
/Brand/logo.ai (created by Jh)
  → copied to /Client_X/logo.ai
  → edited by Cam
```
**Solution:** 
- Jh gets credit for 1 file created (original)
- Cam gets credit for 1 file modified (copy)

---

### **Deduplication Algorithm:**

```python
def deduplicate_contributions(files):
    seen_creates = {}  # content_hash → creator
    seen_edits = {}    # (file_id, revision, actor) → bool
    
    contributions = defaultdict(lambda: {
        'files_created': 0,
        'files_modified': 0,
        'total_touches': 0
    })
    
    for file in files:
        creator = file.creator
        content_hash = file.content_hash
        
        # Credit creation (once per content_hash)
        if content_hash not in seen_creates:
            seen_creates[content_hash] = creator
            contributions[creator]['files_created'] += 1
            contributions[creator]['total_touches'] += 1
        
        # Credit edits (once per revision per actor)
        for revision in file.revisions:
            editor = revision.actor
            key = (file.file_id, revision.rev, editor)
            
            if key not in seen_edits and editor != creator:
                seen_edits[key] = True
                contributions[editor]['files_modified'] += 1
                contributions[editor]['total_touches'] += 1
    
    return contributions
```

---

## 🛠️ IMPLEMENTATION PLAN

### **Phase 1: Basic Scanner (2-3 hours)**

**Goal:** Scan one folder, list files, extract basic metadata

**Tasks:**
1. ✅ Set up Dropbox API credentials
2. ✅ Implement `list_folder` recursive scan
3. ✅ Filter by file extensions (.ai, .psd, .pdf)
4. ✅ Extract basic metadata (file_id, path, size, modified_date)
5. ✅ Export to JSON

**Output:**
```json
{
  "files": [
    {
      "file_id": "id:abc123",
      "path": "/Brand/logo.ai",
      "size": 2048576,
      "modified": "2025-11-09T12:00:00Z"
    }
  ]
}
```

---

### **Phase 2: Dropbox Attribution (3-4 hours)**

**Goal:** Get creator and editor info from Dropbox API

**Tasks:**
1. ✅ Implement `list_revisions` for each file
2. ✅ Extract uploader (creator proxy)
3. ✅ Extract revision modifiers (editors)
4. ✅ Handle Business vs Personal accounts
5. ✅ Map account_id → display name

**Output:**
```json
{
  "file_id": "id:abc123",
  "creator": {"id": "dbid:A1", "name": "Jh"},
  "editors": [
    {"id": "dbid:B2", "name": "Cam", "revision": 5}
  ]
}
```

---

### **Phase 3: XMP Parsing (2-3 hours)**

**Goal:** Extract creator/editor info from file metadata

**Tasks:**
1. ✅ Install ExifTool
2. ✅ Download file temporarily
3. ✅ Parse XMP metadata
4. ✅ Extract dc:creator, modify_date, history
5. ✅ Clean up temp files

**Output:**
```json
{
  "xmp": {
    "dc_creator": ["Justin Harmon"],
    "modify_date": "2025-11-09T12:00:00Z",
    "creator_tool": "Adobe Illustrator 28",
    "history": [
      {"action": "created", "when": "2025-01-15"},
      {"action": "saved", "when": "2025-11-09"}
    ]
  }
}
```

---

### **Phase 4: Attribution Resolution (2 hours)**

**Goal:** Merge Dropbox + XMP data intelligently

**Tasks:**
1. ✅ Implement priority logic (Dropbox > XMP)
2. ✅ Handle name matching (account_id ↔ XMP name)
3. ✅ Resolve conflicts (different sources, same file)
4. ✅ Add confidence scores

**Output:**
```json
{
  "creator": {
    "id": "dbid:A1",
    "name": "Jh",
    "source": "dropbox_api",
    "confidence": 0.95
  }
}
```

---

### **Phase 5: Deduplication (2-3 hours)**

**Goal:** Implement anti-double-count logic

**Tasks:**
1. ✅ Track by file_id (renames)
2. ✅ Track by content_hash (copies)
3. ✅ Collapse multi-save bursts
4. ✅ Handle copy + edit scenarios
5. ✅ Test edge cases

---

### **Phase 6: Aggregation (1-2 hours)**

**Goal:** Roll up contributions per person

**Tasks:**
1. ✅ Group by contributor
2. ✅ Count files_created, files_modified
3. ✅ Calculate total_touches
4. ✅ Sort by contribution score

**Output:**
```json
{
  "contributors": [
    {
      "id": "dbid:A1",
      "name": "Jh",
      "files_created": 127,
      "files_modified": 89,
      "total_touches": 216,
      "score": 343
    }
  ]
}
```

---

### **Phase 7: Joju Export (1-2 hours)**

**Goal:** Generate Joju-compatible mining report

**Tasks:**
1. ✅ Format as mining_report.json
2. ✅ Add metadata (source, timestamp, folder)
3. ✅ Export to Joju inbox
4. ✅ Trigger Joju import (if auto-import enabled)

**Output:**
```json
{
  "content_type": "mining_report",
  "target_focus": "joju",
  "metadata": {
    "source": "dropbox_contribution_miner",
    "timestamp": "2025-11-09T18:00:00Z",
    "folder_root": "/Team/Design/Brand"
  },
  "files": [...],
  "contributors": [...]
}
```

---

### **Phase 8: Continuous Monitoring (3-4 hours)**

**Goal:** Keep contributions updated automatically

**Tasks:**
1. ✅ Implement longpoll for changes
2. ✅ Process only changed files
3. ✅ Update aggregations incrementally
4. ✅ Schedule nightly full re-scan

**Options:**
- **Longpoll:** No server needed, check every N minutes
- **Webhook:** Immediate updates, requires server
- **Scheduled:** Cron job, nightly re-scan

---

## 📋 DATA MODEL

### **File Record:**
```json
{
  "file_id": "id:abc123",
  "path": "/Brand/logo.ai",
  "ext": "ai",
  "content_hash": "dbxhash123",
  "size_bytes": 2048576,
  "created_at": "2025-01-15T10:00:00Z",
  "modified_at": "2025-11-09T12:00:00Z",
  "creator": {
    "id": "dbid:A1",
    "name": "Jh",
    "source": "dropbox_api"
  },
  "revisions": [
    {
      "rev": "5",
      "modified_at": "2025-11-09T12:00:00Z",
      "modifier": {
        "id": "dbid:B2",
        "name": "Cam"
      }
    }
  ],
  "xmp": {
    "dc_creator": ["Justin Harmon"],
    "modify_date": "2025-11-09T12:00:00Z",
    "creator_tool": "Adobe Illustrator 28"
  }
}
```

---

### **Contributor Record:**
```json
{
  "id": "dbid:A1",
  "name": "Jh",
  "email": "harmon.justin@gmail.com",
  "files_created": 127,
  "files_modified": 89,
  "total_touches": 216,
  "contribution_score": 343,
  "file_types": {
    "ai": 87,
    "psd": 40
  },
  "first_contribution": "2020-03-15T00:00:00Z",
  "last_contribution": "2025-11-09T12:00:00Z"
}
```

---

### **Mining Report (Joju Format):**
```json
{
  "content_type": "mining_report",
  "target_focus": "joju",
  "metadata": {
    "source": "dropbox_contribution_miner",
    "version": "1.0.0",
    "timestamp": "2025-11-09T18:00:00Z",
    "folder_root": "/Team/Design/Brand",
    "scan_depth": "recursive",
    "files_scanned": 342,
    "files_attributed": 216
  },
  "files": [...],
  "contributors": [...],
  "summary": {
    "total_contributors": 5,
    "total_files": 216,
    "total_touches": 543,
    "file_types": {
      "ai": 127,
      "psd": 89
    }
  }
}
```

---

## 🧪 TESTING STRATEGY

### **Test 1: Basic Scan**
```bash
python3 dropbox_miner.py --folder "/Brand" --scan-only
```
Expected: Lists all .ai files with basic metadata

---

### **Test 2: Attribution**
```bash
python3 dropbox_miner.py --folder "/Brand" --with-attribution
```
Expected: Shows creator and editors for each file

---

### **Test 3: Deduplication**
```bash
# Create test scenario:
# 1. Upload logo.ai
# 2. Copy to logo_v2.ai
# 3. Edit logo_v2.ai
# 4. Rename logo_v2.ai to logo_final.ai

python3 dropbox_miner.py --folder "/Test" --dedupe
```
Expected: 
- 1 file created (original)
- 1 file modified (copy)
- No double-counting

---

### **Test 4: XMP Parsing**
```bash
python3 dropbox_miner.py --folder "/Brand" --with-xmp
```
Expected: XMP metadata extracted and merged

---

### **Test 5: Joju Export**
```bash
python3 dropbox_miner.py --folder "/Brand" --export-joju
```
Expected: mining_report.json created in Joju inbox

---

### **Test 6: Continuous Monitoring**
```bash
python3 dropbox_miner.py --folder "/Brand" --monitor
```
Expected: Detects new files, updates counts

---

## 🎯 SUCCESS METRICS

### **Phase 1 Success:**
- ✅ Scans folder recursively
- ✅ Finds all .ai/.psd files
- ✅ Extracts basic metadata
- ✅ Exports to JSON

### **Phase 2 Success:**
- ✅ Attributes creator correctly (90%+ accuracy)
- ✅ Attributes editors correctly (80%+ accuracy)
- ✅ Handles Business vs Personal accounts

### **Phase 3 Success:**
- ✅ Parses XMP from .ai files
- ✅ Extracts creator and history
- ✅ Handles files without XMP

### **Phase 4 Success:**
- ✅ Merges Dropbox + XMP intelligently
- ✅ Resolves conflicts correctly
- ✅ Confidence scores accurate

### **Phase 5 Success:**
- ✅ Zero double-counting on renames
- ✅ Correct handling of copies
- ✅ Multi-save bursts collapsed
- ✅ Copy + edit scenarios correct

### **Phase 6 Success:**
- ✅ Accurate contribution counts
- ✅ Correct aggregation per person
- ✅ Contribution scores make sense

### **Phase 7 Success:**
- ✅ Joju mining_report.json valid
- ✅ Auto-imports to Joju library
- ✅ Shows in Joju UI correctly

### **Phase 8 Success:**
- ✅ Detects new files within 5 minutes
- ✅ Updates counts automatically
- ✅ Nightly re-scan catches drift

---

## 🚀 QUICK START (MVP)

### **Minimal Working Version (4-6 hours):**

1. **Scan one folder** (1 hour)
   - List all .ai files
   - Get basic metadata

2. **Simple attribution** (2 hours)
   - Use Dropbox uploader as creator
   - Use last revision modifier as editor

3. **Basic aggregation** (1 hour)
   - Count files per person
   - No deduplication yet

4. **Export to JSON** (1 hour)
   - Simple format
   - Manual import to Joju

**Result:** Working end-to-end, rough but functional

---

## 🔮 FUTURE ENHANCEMENTS

### **Phase 9: Advanced Features**

1. **Contribution Scoring**
   ```python
   score = (files_created * 2) + (files_modified * 1)
   ```

2. **File Lineage**
   - Show creator → editor timeline
   - Visualize collaboration patterns

3. **Dashboard**
   - Real-time contribution stats
   - Leaderboards
   - Trend charts

4. **Multi-Folder Support**
   - Scan multiple folders
   - Aggregate across projects
   - Filter by folder/project

5. **Team Analytics**
   - Who collaborates most?
   - What file types per person?
   - Contribution trends over time

6. **Joju Integration**
   - Auto-populate achievements
   - Generate portfolio entries
   - Link to actual files

---

## 📝 OPEN QUESTIONS

### **Q1: Which Dropbox account type?**
**Business:** Full team_log access (best attribution)  
**Personal:** Limited to revisions (good enough)  
**Decision:** Support both, prefer Business

---

### **Q2: Which file types to support?**
**Phase 1:** .ai (Illustrator)  
**Phase 2:** .psd (Photoshop), .pdf  
**Phase 3:** .indd (InDesign), .sketch, .fig  
**Decision:** Start with .ai, expand based on usage

---

### **Q3: How to handle shared folders?**
**Option A:** Treat as separate projects  
**Option B:** Aggregate across all folders  
**Decision:** Configurable per scan

---

### **Q4: What about deleted files?**
**Option A:** Ignore (only count current files)  
**Option B:** Track deletions (full history)  
**Decision:** Start with Option A, add B later

---

### **Q5: How to handle name changes?**
**Scenario:** User changes Dropbox display name  
**Solution:** Track by account_id, update name mapping

---

## 💡 KEY INSIGHTS

1. **Dropbox API is the source of truth** - XMP is supplementary
2. **Deduplication is critical** - Without it, counts are meaningless
3. **Business accounts >> Personal** - Team logs provide better attribution
4. **Content hash is powerful** - Catches copies across folders
5. **Continuous monitoring is valuable** - One-time scan gets stale
6. **Joju integration is the goal** - Mining report format is key

---

## 🎓 COMPARISON TO PHIL'S LEDGER

| Aspect | Phil's Ledger | Dropbox Miner |
|--------|---------------|---------------|
| **Source** | Email/Downloads | Dropbox API |
| **Data Type** | Bills (structured) | Files (semi-structured) |
| **Attribution** | OCR extraction | API + XMP parsing |
| **Deduplication** | Vendor+Amount+Date | file_id + content_hash |
| **Monitoring** | Gmail polling | Dropbox longpoll |
| **Export** | CSV → HTML app | JSON → Joju library |
| **Complexity** | Medium | High |
| **Value** | Immediate (bill tracking) | Long-term (portfolio building) |

**Similarities:**
- Both mine external data sources
- Both need deduplication
- Both export to structured format
- Both benefit from continuous monitoring

**Differences:**
- Phil's Ledger: Real-time utility (pay bills)
- Dropbox Miner: Historical analysis (build portfolio)

---

## 🚀 NEXT STEPS

### **Immediate (This Week):**
1. [ ] Set up Dropbox API credentials
2. [ ] Test basic folder scan
3. [ ] Verify file_id and content_hash extraction
4. [ ] Test on small folder (10-20 files)

### **Short-term (Next Week):**
1. [ ] Implement attribution logic
2. [ ] Add XMP parsing
3. [ ] Test deduplication algorithm
4. [ ] Export first mining report

### **Long-term (Next Month):**
1. [ ] Add continuous monitoring
2. [ ] Integrate with Joju library
3. [ ] Build dashboard
4. [ ] Scale to full Dropbox

---

**This pipeline would automatically populate Joju with years of design work, accurately attributed, without manual data entry.**

**Estimated total time: 15-20 hours for full implementation**  
**MVP time: 4-6 hours for basic working version**

**Ready to build?**
