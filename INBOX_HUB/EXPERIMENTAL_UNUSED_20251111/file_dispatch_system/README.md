# File Dispatch System (FDS)

**Status:** Production Ready  
**Date:** November 11, 2025  
**MCP Port:** Integrated with Goose

---

## What This Is

**File Dispatch System (FDS)** - The unified file orchestration system that replaces all overlapping file watchers, sync scripts, and processors.

**ONE system** to rule them all.

### What It Does

1. **Watches** 3 input locations (configured by you)
2. **Classifies** files by type and content
3. **Routes** to appropriate processor:
   - JSON/TXT/TXF → Ingestion system
   - Screenshots → Screenshot protocols + archive
   - BRAIN_TRANSPORT → Output folder (protected)
   - Everything else → Progressive router
4. **Outputs** to iCloud Documents/8825/

---

## Quick Start

### First Time Setup (Already Done!)

You already configured this in `sandbox_target_acquisition/`:
- ✅ 3 inputs (Desktop Downloads, iCloud Downloads, Screenshots)
- ✅ 1 output (iCloud Documents/8825/)

### Option 1: Direct Control

```bash
cd file_dispatch_system
./start.sh
```

### Option 2: Goose Control (Recommended)

```bash
# Setup once
cd ../../8825_core/integrations/mcp-servers/fds-mcp
./SETUP_GOOSE.sh

# Then use natural language
goose session start
> Start the file dispatch system
> What's the FDS status?
> Show me recent logs
```

### Check Status

```bash
./status.sh
```

### Stop the System

```bash
./stop.sh
```

---

## Components

### Core Files

- `smart_classifier.py` - Routes files by type
- `ingestion_router.py` - Handles JSON/TXT/TXF
- `screenshot_processor.py` - Handles screenshots
- `output_manager.py` - Manages outputs
- `unified_processor.py` - Orchestrates everything
- `watch.sh` - File watcher (fswatch)

### Control Scripts

- `start.sh` - Start system
- `stop.sh` - Stop system
- `status.sh` - View status

---

## How It Works

```
INPUTS (3 watched)
├── Desktop Downloads
├── iCloud Downloads
└── Screenshots
     ↓
WATCHER (fswatch)
     ↓
CLASSIFIER
├── .json/.txt/.txf → Ingestion
├── Screenshots → Protocols + Archive
├── BRAIN_TRANSPORT → Protected
└── Other → Progressive Router
     ↓
OUTPUTS
├── iCloud/8825/BRAIN/
├── iCloud/8825/DOCS/
├── Documents/ingestion/
└── Various (Calendar, Drive, etc.)
```

---

## File Routing Rules

### JSON/TXT/TXF Files
- **Action:** Copy to `Documents/ingestion/`
- **Processor:** Existing ingestion engine
- **Result:** Processed into projects

### Screenshots
- **Action:** Run through progressive router
- **Processor:** Screenshot protocols (KARSEN, bills, meetings, etc.)
- **Result:** Routed to destination + archived to `-ARCHV-/`

### BRAIN_TRANSPORT Files
- **Action:** Copy to `iCloud/8825/BRAIN/`
- **Processor:** Output manager
- **Result:** Available in output, kept in Downloads

### Other Files
- **Action:** Progressive router
- **Processor:** Trust-based automation
- **Result:** Routed based on protocols

---

## Logs

All logs in `logs/` folder:
- `unified_processor.log` - Main processing log
- `ingestion_router.log` - Ingestion routing
- `screenshot_processor.log` - Screenshot processing
- `output_manager.log` - Output management
- `watcher.log` - File detection

---

## What This Replaces

**Deleted (redundant):**
- downloads_sync.py
- sync_screenshots.sh
- sync_downloads_folders.sh
- Multiple other sync scripts

**Kept (integrated):**
- Ingestion engine (8825_core/workflows/ingestion/)
- Progressive router (INBOX_HUB/progressive_router.py)
- All protocols (exclusion, dedup, etc.)

---

## Troubleshooting

### System Won't Start
```bash
# Check config exists
ls ../sandbox_target_acquisition/user_config.json

# Check fswatch installed
which fswatch

# View logs
tail -f logs/watcher.log
```

### Files Not Being Detected
```bash
# Check status
./status.sh

# Check if watcher is running
ps aux | grep watch.sh

# View recent activity
tail -f logs/unified_processor.log
```

### Files Going to Wrong Place
```bash
# Check classification
python3 smart_classifier.py

# View processing log
tail -f logs/unified_processor.log
```

---

## Integration Points

### With Ingestion System
- JSON/TXT/TXF files copied to `Documents/ingestion/`
- Existing ingestion engine processes them
- No changes to ingestion system needed

### With Progressive Router
- Non-ingestion files routed through it
- All existing protocols work
- Trust progression continues

### With Output Folder
- BRAIN_TRANSPORT files copied to output
- 8825-generated docs copied to output
- Available on mobile via iCloud

---

---

## Goose Natural Language Commands

Once configured with Goose, you can use natural language:

### Status & Monitoring
- "What's the status of the file dispatch system?"
- "Is FDS running?"
- "Show me recent FDS activity"
- "How many files are in the queue?"

### Control
- "Start the file dispatch system"
- "Stop FDS"
- "Clear the processing queue"

### Processing
- "Process this file: /path/to/file.pdf"
- "Show me the last 50 log entries"
- "What's in the processing queue?"

### Troubleshooting
- "Show me FDS logs"
- "Why isn't FDS processing files?"
- "Check FDS configuration"

---

**This is the final system. One unified solution. No more overlaps.**

**Status:** Ready to use  
**Goose:** Fully integrated
