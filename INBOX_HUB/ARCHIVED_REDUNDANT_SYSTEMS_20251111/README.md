# 8825 Target Acquisition - Phase 1 (Setup + Watch)

**Status:** Sandbox - Testing Only  
**Phase:** 1 of 3 (Setup + Start, no automation yet)

---

## What This Does

**Phase 1:** Setup and watch configured folders in real-time
- ✅ User configures paths (drag and drop)
- ✅ System watches for new files (fswatch)
- ✅ Files added to queue
- ❌ No processing yet (waiting for rules)

---

## Quick Start

### 1. Setup (One-time)
```bash
cd sandbox_target_acquisition
./setup_targets.sh
```

**What it asks:**
1. Drag Screenshots folder
2. Drag Downloads folder  
3. Drag Mobile cloud folder (optional)

**Creates:** `user_config.json`

### 2. Start Watching
```bash
./start.sh
```

**What it does:**
- Starts fswatch on configured folders
- Detects new files in real-time
- Adds to `processing_queue.txt`
- Logs to `processing_log.txt`

### 3. Check Status
```bash
./status.sh
```

**Shows:**
- Watched folders
- System status (running/stopped)
- Queue depth
- Recent activity

### 4. Stop
```bash
./stop.sh
```

---

## Files Created

```
sandbox_target_acquisition/
├── setup_targets.sh          # One-time setup
├── start.sh                  # Start watching
├── stop.sh                   # Stop watching
├── status.sh                 # View status
├── user_config.json          # Your paths (created by setup)
├── processing_queue.txt      # Detected files (auto-managed)
├── processing_log.txt        # Activity log (auto-managed)
└── .watcher.pid              # Process ID (auto-managed)
```

---

## What's Next

**Phase 2:** Define processing rules
- Screenshot archiving rules
- File type routing
- Trust progression thresholds
- Exclusion patterns

**Phase 3:** Add processor
- Read from queue
- Apply rules
- Route files
- Update trust levels

---

## Testing

### Test 1: Screenshot Detection
1. Run `./start.sh`
2. Take a screenshot
3. Run `./status.sh`
4. Verify screenshot in queue

### Test 2: Download Detection
1. Download any file
2. Run `./status.sh`
3. Verify file in queue

### Test 3: Mobile Upload
1. Upload file from phone to cloud folder
2. Run `./status.sh`
3. Verify file in queue

---

## Current Limitations

- ✅ Detects files
- ✅ Queues files
- ❌ Does NOT process files (waiting for rules)
- ❌ Does NOT move files
- ❌ Does NOT route files

**This is intentional - waiting for rule definition before automation.**

---

## Logs

### View Queue
```bash
cat processing_queue.txt
```

### View Activity
```bash
tail -f processing_log.txt
```

### View Config
```bash
cat user_config.json | jq
```

---

**Ready to test!**
