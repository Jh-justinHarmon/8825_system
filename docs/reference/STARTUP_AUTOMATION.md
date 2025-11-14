# 8825 System Startup & Automation

**Last Updated:** 2025-11-09

## Dependencies ✅

### Auto-Check & Install
All scripts automatically check and install missing dependencies on first run.

**Manual check:**
```bash
./check_dependencies.sh
```

**Manual install all:**
```bash
pip3 install -r requirements.txt
```

### ⚠️ Notion Integration (Joju Tasks) - CRITICAL

**MUST use specific SDK version:**
```bash
pip3 install notion-client==1.0.0
```

**DO NOT use v2.7.0+** - Breaking API changes (no `databases.query()` method)

**Setup Check:**
```bash
cd focuses/joju/tasks
./check_setup.sh
```

**If missing config:**
1. Copy from v2.0: `config/8825_config.json`
2. Create: `cp config.example.json config.json`
3. Test: `python3 notion_sync.py test`

**See:** `focuses/joju/tasks/NOTION_SETUP_COMPLETE.md` for troubleshooting

---

**Required packages:**
- python-docx (document processing)
- watchdog (file monitoring)
- flask (MCP servers)
- flask-cors (MCP servers)
- python-dotenv (MCP servers)
- **notion-client==1.0.0** (Joju task management) ⚠️ **VERSION CRITICAL**
- google-auth, google-auth-oauthlib, google-api-python-client (bill processor)
- pillow, pytesseract, pillow-heif (OCR & image processing)

**System dependencies (macOS):**
```bash
brew install tesseract  # OCR engine
brew install libheif    # HEIC image support
```

---

## Automated Processing ✅

### Inbox Processing Pipeline
**Status:** Auto-runs every hour (LaunchAgent configured)

**Command:** `process inbox` or `run the pipeline` (manual override)
```bash
cd INBOX_HUB
./simple_sync_and_process.sh
```

**What it does:**
1. Syncs iCloud → Local Downloads
2. Updates brain transport (0- prefix)
3. Processes files (TXT, MD, DOCX, JSON)
4. Archives processed files
5. Cleans up Downloads
6. Syncs back to iCloud

**Schedule:** Runs automatically every hour + on login
**Manual:** Can still run `process inbox` anytime for immediate processing

**LaunchAgent:** `~/Library/LaunchAgents/com.8825.inbox-pipeline.plist`

**Logs:**
- Output: `/tmp/8825-inbox-pipeline.log`
- Errors: `/tmp/8825-inbox-pipeline-error.log`

---

### Screenshot Sync
**Command:** Already runs as part of pipeline, or standalone:
```bash
cd INBOX_HUB
./sync_screenshots.sh
```

**What it does:**
- Syncs screenshots from Desktop, Downloads, Dropbox
- Routes to `users/jh/intake/screenshots/`

---

### OCR Latest Screenshot
**Command:** `eval latest screenshot`
```bash
cd INBOX_HUB
./ocr_latest_screenshot.sh
```

**What it does:**
- Copies latest screenshot to `/tmp/latest_screenshot.png`
- Makes it readable for OCR (avoids path space issues)

---

## Cleanup Commands

### Downloads Cleanup
```bash
cd INBOX_HUB
./cleanup_downloads.sh
```

Archives 8825 files from Downloads to `Downloads/8825_processed/`

### 8825_inbox Cleanup
```bash
cd INBOX_HUB
./cleanup_8825_inbox.sh
```

Organizes 8825_inbox into pending/processing/completed/errors structure

---

## Background Services (Auto-Start Configured)

### MCP Servers ℹ️
**Status:** No auto-start needed - Goose manages them

**How MCP Servers Work:**
- MCP servers use **stdio communication** (not HTTP ports)
- Goose starts/stops them automatically when needed
- No background processes or daemons required
- Configured in `~/.config/goose/profiles.yaml`

**Available Servers:**
- **HCSS MCP** - `~/mcp_servers/hcss-bridge/server.js`
- **Joju/Team76 MCP** - `~/mcp_servers/figma-make-transformer/server.js`
- **8825 Core MCP** - `~/mcp_servers/8825-core/server.py`

**Check Configuration:**
```bash
# View Goose MCP config
cat ~/.config/goose/profiles.yaml

# Test in Goose
goose session start
> List available tools
```

**No LaunchAgent needed** - stdio-based servers are invoked on-demand

---

### Downloads Folder Sync (Bidirectional)
**Location:** `users/justin_harmon/jh_assistant/projects/download-wedge/`

**Script:** `downloads_sync.py`

**What it does:**
- Real-time bidirectional sync between local and iCloud Downloads
- Monitors for new files continuously

**Status:** Not running as background service

**To enable:** See `DOWNLOADS_SYNC_README.md` for LaunchAgent setup

---

## File Type Support

### Ingestion Engine Accepts:
- ✅ `.json` - Structured data
- ✅ `.txt` - Plain text (auto-wrapped)
- ✅ `.md` - Markdown (auto-wrapped)
- ✅ `.docx` - Microsoft Word (text extracted, auto-wrapped)

All non-JSON files are automatically wrapped in proper JSON format for processing.

---

## Folder Structure

### Active Folders
```
~/Downloads/
├── 0-8825_BRAIN_TRANSPORT.json  ← Always at top
├── 8825_processed/              ← Archive
└── 8825_inbox/                  ← Ingestion engine
    ├── pending/
    ├── processing/
    ├── completed/
    └── errors/
```

### INBOX_HUB
```
INBOX_HUB/
├── users/jh/intake/
│   ├── screenshots/
│   ├── documents/
│   └── uploads/
└── users/jh/processed/          ← Archived files
```

---

## Automation Summary

### ✅ Configured & Running

**MCP Servers:**
- Auto-start on login
- 3 servers (HCSS, Joju, JH Assistant)

**Inbox Pipeline:**
- Runs every hour automatically
- Also runs on login
- Can trigger manually with `process inbox`

### 📋 Manual Commands Still Available

All automation can be triggered manually anytime:
- `process inbox` - Run pipeline immediately
- `./start_all_mcps.sh` - Start MCPs manually
- `./stop_all_mcps.sh` - Stop MCPs manually

---

## Quick Reference

| Task | Command |
|------|---------|
| Process inbox | `process inbox` |
| OCR screenshot | `eval latest screenshot` |
| Clean Downloads | `./cleanup_downloads.sh` |
| Sync screenshots | `./sync_screenshots.sh` |
| Start all MCPs | `./start_all_mcps.sh` |
| Stop all MCPs | `./stop_all_mcps.sh` |
| Check MCP status | `ps aux \| grep mcp` |
| View teaching tickets | `cd 8825_core/inbox && python3 ingestion_engine.py tickets list` |
| Check stats | `python3 ingestion_engine.py stats` |

---

## Notes

- **MCP servers auto-start on login** - LaunchAgent configured ✅
- **Inbox pipeline runs hourly** - LaunchAgent configured ✅
- **Pipeline is idempotent** - Safe to run multiple times
- **Files are never deleted** - Only moved to archive folders
- **Teaching tickets require human review** - Check with `tickets list` command

## Manage Auto-Start

### Disable MCP Servers
```bash
launchctl unload ~/Library/LaunchAgents/com.8825.mcp-servers.plist
```

### Disable Inbox Pipeline
```bash
launchctl unload ~/Library/LaunchAgents/com.8825.inbox-pipeline.plist
```

### Re-enable
```bash
launchctl load ~/Library/LaunchAgents/com.8825.mcp-servers.plist
launchctl load ~/Library/LaunchAgents/com.8825.inbox-pipeline.plist
```

### Check Status
```bash
launchctl list | grep 8825
```
