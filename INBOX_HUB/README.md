# Input Hub - Phase 2: Full Automation

**Status:** ✅ Production Ready  
**Version:** 2.0 (Phase 2 Complete)  
**Built:** 2025-11-10

---

## What This Is

**Fully automated intake system with OCR and smart routing.**

- ✅ Auto-syncs from 4 sources (Desktop, Downloads, Dropbox, 8825 Ingestion)
- ✅ Routes by file type (images → screenshots, docs → documents, other → uploads)
- ✅ OCR extraction from screenshots
- ✅ Smart routing to project folders based on content
- ✅ Learning from corrections to improve accuracy
- ✅ Real-time file watching with watchdog

---

## Folder Structure

```
INBOX_HUB/
└── users/
    └── jh/
        ├── intake/
        │   ├── screenshots/    # PNG, JPG, JPEG, GIF, etc.
        │   ├── documents/      # JSON, MD, TXT, DOCX, PDF
        │   └── uploads/        # Everything else
        ├── normalized/         # (Phase 2: with metadata)
        └── processed/          # (Phase 2: routed to projects)
```

## Source Locations

**Syncs from 4 locations:**
1. `~/Desktop`
2. `~/Downloads`
3. `~/Hammer Consulting Dropbox/Justin Harmon/Screenshots`
4. `~/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/ingestion`

---

## Quick Start

### Phase 2: Full Automation
```bash
cd INBOX_HUB
./start_phase2.sh
```

**What it does:**
1. Processes existing screenshots with OCR
2. Routes screenshots to correct project folders
3. Starts auto-sync daemon (watches for new files)

### Phase 1: Manual Sync (still available)
```bash
./sync_screenshots.sh  # Manual sync
./checking_sg.sh       # View latest screenshot
```

---

## Commands

### `sync_screenshots.sh`
Unified sync that handles all file types from 4 sources with intelligent routing.

**Usage:**
```bash
./sync_screenshots.sh
```

**What it does:**
- Scans 4 source locations (Desktop, Downloads, Dropbox Screenshots, 8825 Ingestion)
- Routes by file type:
  - Images (png, jpg, jpeg, gif, etc.) → `screenshots/`
  - Documents (json, md, txt, docx, pdf) → `documents/`
  - Other files → `uploads/`
- Preserves timestamps
- Skips duplicates
- Shows counts by type

### `checking_sg.sh`
Shows the most recent screenshot.

**Usage:**
```bash
./checking_sg.sh           # Latest screenshot
./checking_sg.sh 5         # Last 5 screenshots
```

**Output:**
- Filename
- Timestamp
- File size
- Location

---

## Phase 1 vs Phase 2

### Phase 1 (Complete)
✅ Folder structure  
✅ Manual sync script  
✅ Quick reference command  
✅ Basic metadata  

### Phase 2 (Complete)
✅ Auto-sync (watchdog)  
✅ OCR integration (pytesseract)  
✅ Context extraction (project detection)  
✅ Smart routing (confidence-based)  
✅ Learning system (tracks corrections)  
⏳ MCP integration (future)

**Phase 2 Status:** ✅ Shipped 2025-11-10

---

## Usage Tips

### Daily Workflow
1. Work as usual (screenshots, save files to Desktop/Downloads)
2. Drop files in `8825/Documents/ingestion/` from ChatGPT/other sources
3. Run `./sync_screenshots.sh` to sync everything
4. Use `./checking_sg.sh` to reference latest screenshot
5. Check `intake/documents/` for JSON/DOCX/PDF files

### Finding Files
```bash
# Latest screenshot
./checking_sg.sh

# Last 10 screenshots
./checking_sg.sh 10

# Recent documents
ls -lt users/jh/intake/documents/ | head -20

# Find specific file
find users/jh/intake/ -name "*token*"

# By date
ls -lt users/jh/intake/documents/ | grep "Nov  8"

# By type
find users/jh/intake/documents/ -name "*.json"
```

---

## Integration

### With Inbox System
Phase 2 will integrate with existing `8825_inbox`:
- Shared ingestion core
- Unified classification
- Common routing logic

### With Focus Protocols
Screenshots can be manually moved to focus folders:
```bash
cp users/jh/intake/screenshots/screenshot.png \
   ../focuses/jh/screenshots/
```

---

## Next Steps

**Phase 1 Complete:**
- ✅ Structure created
- ✅ Sync script ready
- ✅ Reference command ready

**Phase 2 Planning:**
- See `roadmap/foundation_sprint_backlog.json`
- Item ID: `proto-003`
- Depends on: Shared ingestion core refactor

---

**Built:** 2025-11-08  
**Time:** 30 minutes (calibrated)  
**Next:** Roadmap system for Phase 2 planning
