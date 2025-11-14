# Joju Dropbox Contribution Miner - MVP

**Status:** MVP Ready to Test  
**Created:** 2025-11-09  
**Version:** 0.1.0-mvp

---

## What It Does (MVP)

Scans Dropbox folders for design files and generates a mining report:
- ✅ Finds all .ai, .psd, .pdf, .indd, .sketch, .fig files
- ✅ Extracts basic metadata (path, size, dates, content_hash)
- ✅ Aggregates statistics (file counts, sizes, date ranges)
- ✅ Exports Joju-compatible mining report

---

## What It DOESN'T Do Yet (Full Version)

- ❌ Creator attribution (needs Business account or XMP parsing)
- ❌ Editor attribution (needs revision tracking)
- ❌ Deduplication (renames, copies)
- ❌ XMP metadata parsing
- ❌ Continuous monitoring
- ❌ Auto-import to Joju

**This is a working MVP to validate the approach.**

---

## Setup

### 1. Install Dependencies

```bash
pip3 install dropbox
```

### 2. Get Dropbox Access Token

**Option A: Quick Test (Short-lived token)**
1. Go to: https://www.dropbox.com/developers/apps
2. Click "Create app"
3. Choose:
   - API: Scoped access
   - Access: Full Dropbox
   - Name: "Joju Miner Test"
4. Go to "Permissions" tab
5. Enable:
   - `files.metadata.read`
   - `files.content.read`
6. Go to "Settings" tab
7. Generate access token (valid for 4 hours)
8. Copy token

**Option B: Production (Long-lived token)**
1. Same as above, but implement OAuth flow
2. See: https://www.dropbox.com/developers/documentation/python#tutorial

### 3. Set Environment Variable

```bash
export DROPBOX_ACCESS_TOKEN="your_token_here"
```

Or add to `~/.zshrc`:
```bash
echo 'export DROPBOX_ACCESS_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## Usage

### Basic Scan

```bash
cd 8825_core/integrations/dropbox
python3 dropbox_miner.py --folder "/Team/Design"
```

**Output:**
```
============================================================
Joju Dropbox Contribution Miner - MVP
============================================================

📁 Scanning: /Team/Design
   Recursive: True
✓ Found 127 design files

🔍 Attributing 127 files...
   Progress: 10/127
   Progress: 20/127
   ...
✓ Attribution complete

📊 Aggregating contributions...
✓ Aggregation complete
   Total files: 127
   Total size: 2458.3 MB
   File types: {'.ai': 87, '.psd': 40}

💾 Exporting mining report...
✓ Report exported: .../mining_reports/mining_report_dropbox_20251109_181500.json
   Size: 145.2 KB

============================================================
✅ Mining complete!
============================================================

📄 View report: .../mining_reports/mining_report_dropbox_20251109_181500.json

💡 Next steps:
   1. Review the mining report
   2. Import to Joju library (manual for MVP)
   3. Iterate on attribution logic
```

---

### With Revisions (Slower)

```bash
python3 dropbox_miner.py --folder "/Team/Design" --with-revisions
```

Fetches revision history for each file (adds ~2-3 seconds per file).

---

### Custom Token

```bash
python3 dropbox_miner.py --folder "/Team/Design" --token "YOUR_TOKEN"
```

---

## Output Format

**Location:** `users/justin_harmon/joju/data/mining_reports/`

**Filename:** `mining_report_dropbox_YYYYMMDD_HHMMSS.json`

**Structure:**
```json
{
  "content_type": "mining_report",
  "target_focus": "joju",
  "metadata": {
    "source": "dropbox_contribution_miner",
    "version": "0.1.0-mvp",
    "timestamp": "2025-11-09T18:15:00Z",
    "folder_root": "/Team/Design",
    "scan_type": "mvp",
    "limitations": [
      "Creator attribution requires Business account or XMP parsing",
      "Editor attribution simplified (server_modified only)",
      "No deduplication across copies/renames",
      "No XMP metadata parsing"
    ]
  },
  "files": [
    {
      "file_id": "id:abc123",
      "path": "/Team/Design/Brand/logo.ai",
      "name": "logo.ai",
      "ext": ".ai",
      "size_bytes": 2048576,
      "content_hash": "dbxhash123",
      "server_modified": "2025-11-09T12:00:00Z",
      "client_modified": "2025-11-09T11:58:00Z",
      "creator": {
        "source": "unknown",
        "note": "MVP: Creator attribution requires Business account or XMP parsing"
      },
      "last_editor": {
        "source": "server_modified",
        "timestamp": "2025-11-09T12:00:00Z"
      }
    }
  ],
  "statistics": {
    "total_files": 127,
    "by_extension": {
      ".ai": 87,
      ".psd": 40
    },
    "by_folder": {
      "/Team/Design/Brand": 45,
      "/Team/Design/Client_X": 32
    },
    "total_size_mb": 2458.3,
    "date_range": {
      "earliest": "2020-03-15T10:00:00Z",
      "latest": "2025-11-09T12:00:00Z"
    }
  },
  "contributors": [
    {
      "note": "MVP: Contributor attribution not implemented yet",
      "next_steps": [
        "Add Business account team_log support",
        "Add XMP parsing for .ai/.psd files",
        "Implement deduplication logic",
        "Add revision-based editor tracking"
      ]
    }
  ]
}
```

---

## Testing

### Test 1: Small Folder
```bash
python3 dropbox_miner.py --folder "/Test"
```
Expected: Quick scan, basic report

### Test 2: Large Folder
```bash
python3 dropbox_miner.py --folder "/Team/Design"
```
Expected: Longer scan, comprehensive report

### Test 3: With Revisions
```bash
python3 dropbox_miner.py --folder "/Test" --with-revisions
```
Expected: Slower, includes revision data

---

## Troubleshooting

### "dropbox package not installed"
```bash
pip3 install dropbox
```

### "DROPBOX_ACCESS_TOKEN not set"
```bash
export DROPBOX_ACCESS_TOKEN="your_token_here"
```

### "Failed to connect to Dropbox"
- Check token is valid
- Check token has correct permissions
- Token may have expired (regenerate)

### "No design files found"
- Check folder path is correct
- Check folder contains .ai/.psd/.pdf files
- Check you have access to the folder

---

## Next Steps

### Phase 2: Attribution (3-4 hours)
1. Add Business account team_log support
2. Add XMP parsing (ExifTool)
3. Implement attribution resolution logic

### Phase 3: Deduplication (2-3 hours)
1. Track by file_id (renames)
2. Track by content_hash (copies)
3. Collapse multi-save bursts

### Phase 4: Joju Integration (1-2 hours)
1. Auto-import to Joju library
2. Generate achievement entries
3. Link to actual files

---

## MVP Limitations

**What's Missing:**
- Creator attribution (shows "unknown")
- Editor attribution (only last modified date)
- Deduplication (counts copies as separate files)
- XMP metadata (no app-level authorship)
- Continuous monitoring (one-time scan only)

**Why This Is OK for MVP:**
- Validates Dropbox API works
- Validates file discovery works
- Validates export format works
- Provides baseline data for iteration

**Next version will add full attribution.**

---

## Files

```
8825_core/integrations/dropbox/
├── README.md              # This file
└── dropbox_miner.py       # Main script
```

---

## Summary

**MVP Status:** ✅ Ready to test  
**Time to Build:** ~2 hours  
**Time to Run:** ~1-5 minutes (depending on folder size)  
**Output:** Joju-compatible mining report  

**Test it now to validate the approach, then iterate on attribution.**
