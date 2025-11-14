# Complete Downloads Touchpoint Audit

**Date:** 2025-11-09  
**Status:** CRITICAL - Multiple scripts touch Downloads  
**Risk:** High - Cleanup can be undone by any of these

---

## ALL Scripts/Services That Touch Downloads:

### **1. INBOX_HUB/sync_downloads_folders.sh**
- **Status:** ✅ FIXED (auto-cleanup integrated)
- **What it does:** Syncs Local ↔ iCloud Downloads
- **Risk:** LOW (now cleans before syncing)

### **2. INBOX_HUB/simple_sync_and_process.sh**
- **Status:** ⚠️ NEEDS REVIEW
- **What it does:** One-way sync iCloud → Local
- **Line 36:** `rsync -au --exclude="8825_processed" "$ICLOUD_DOWNLOADS/" "$LOCAL_DOWNLOADS/"`
- **Risk:** MEDIUM (could copy junk from iCloud to Local)

### **3. INBOX_HUB/sync_and_process.sh**
- **Status:** ⚠️ NEEDS UPDATE
- **What it does:** Calls sync_downloads_folders.sh (line 23)
- **Risk:** LOW (uses fixed script)

### **4. INBOX_HUB/cleanup_downloads.sh**
- **Status:** ✅ SAFE
- **What it does:** Moves 8825 files to 8825_processed
- **Risk:** NONE (cleanup only, no sync)

### **5. INBOX_HUB/sync_screenshots.sh**
- **Status:** ⚠️ NEEDS REVIEW
- **What it does:** Syncs from Desktop/Downloads to intake folders
- **Risk:** LOW (reads from Downloads, doesn't write)

### **6. 8825_core/sync/downloads_sync.py** ⚠️ CRITICAL
- **Status:** 🔴 RUNNING AS DAEMON
- **What it does:** Bidirectional sync Desktop ↔ iCloud (watchdog)
- **Line 4:** "Keeps Desktop/Downloads and iCloud/Downloads in sync (bidirectional)"
- **Risk:** 🔴 VERY HIGH - Will re-sync junk continuously
- **Started by:** `start_all_sync.sh` (line 27)

### **7. users/justin_harmon/jh_assistant/projects/download-wedge/downloads_sync.py**
- **Status:** ⚠️ DUPLICATE?
- **What it does:** Same as #6 (bidirectional sync)
- **Risk:** HIGH if running

### **8. users/justin_harmon/jh_assistant/projects/download-wedge/downloads_manager.py**
- **Status:** ⚠️ NEEDS REVIEW
- **What it does:** Enhanced download wedge with routing
- **Risk:** MEDIUM (complex logic)

### **9. 8825_core/sync/inbox_sync.py**
- **Status:** ⚠️ NEEDS REVIEW
- **What it does:** 3-way sync for 8825_inbox
- **Risk:** LOW (only syncs inbox folder)

---

## THE SMOKING GUN:

### **downloads_sync.py is a DAEMON**

```python
# From 8825_core/sync/downloads_sync.py
"""
Downloads Folder Sync
Keeps Desktop/Downloads and iCloud/Downloads in sync (bidirectional)
Excludes '- old -' folders and 8825_inbox (handled by inbox_sync.py)
"""
```

**Started by:** `8825_core/sync/start_all_sync.sh`

**What it does:**
- Watches BOTH Downloads folders with watchdog
- Bidirectionally syncs ANY file changes
- Runs continuously in background
- Excludes: "- old -", ".DS_Store", "8825_inbox"

**The Problem:**
- It does NOT exclude sticky files, brainstorms, temp files
- It WILL copy them back and forth
- It runs 24/7 if started

---

## Why Cleanup Keeps Breaking:

1. User cleans Downloads manually
2. `downloads_sync.py` daemon sees difference
3. Daemon syncs "missing" files from iCloud back to Local
4. Junk returns
5. User frustrated

**OR:**

1. Run `sync_downloads_folders.sh` (now fixed)
2. `downloads_sync.py` daemon still running
3. Daemon re-syncs based on old logic
4. Junk returns

---

## Required Fixes:

### **Priority 1: Fix the Daemon**

Update `8825_core/sync/downloads_sync.py`:

```python
# Add to EXCLUDE_PATTERNS
EXCLUDE_PATTERNS = [
    "- old -",
    "old",  # ADD THIS
    ".DS_Store",
    ".tmp",
    "~$",
    "8825_inbox",
    "sticky_",  # ADD THIS
    "brainstorm",  # ADD THIS
    "client_secret",  # ADD THIS
    "mythic",  # ADD THIS
    "phils_book",  # ADD THIS
    "IMG_",  # ADD THIS (for HEIC/jpeg)
]
```

### **Priority 2: Check if Daemon is Running**

```bash
# Check for running sync daemons
ps aux | grep downloads_sync.py
ps aux | grep inbox_sync.py

# Kill if found
kill <PID>
```

### **Priority 3: Update simple_sync_and_process.sh**

Add exclusions to rsync command (line 36):

```bash
rsync -au \
    --exclude="8825_processed" \
    --exclude="old" \
    --exclude="- old -" \
    --exclude="sticky_*" \
    --exclude="*brainstorm*" \
    --exclude="client_secret*" \
    --exclude="IMG_*" \
    "$ICLOUD_DOWNLOADS/" "$LOCAL_DOWNLOADS/"
```

### **Priority 4: Document Daemon Startup**

Add to startup docs that daemons need to be updated before starting.

---

## Verification Checklist:

- [ ] Check if downloads_sync.py is currently running
- [ ] Kill daemon if running
- [ ] Update downloads_sync.py EXCLUDE_PATTERNS
- [ ] Update simple_sync_and_process.sh exclusions
- [ ] Test: Clean Downloads, wait 5 minutes, check if junk returns
- [ ] If daemon needed, restart with new exclusions
- [ ] Document in startup scripts

---

## The Real Fix:

**Option A: Fix the Daemon**
- Update EXCLUDE_PATTERNS
- Restart daemon
- Monitor for 24 hours

**Option B: Stop the Daemon**
- Don't run `start_all_sync.sh`
- Use manual `sync_downloads_folders.sh` only
- Simpler, less risk

**Option C: Hybrid**
- Fix daemon for 8825_inbox only
- Don't sync main Downloads automatically
- Manual sync when needed

---

## Recommendation:

**Stop the daemon entirely until it's fixed.**

```bash
# Check if running
ps aux | grep downloads_sync.py

# Kill it
pkill -f downloads_sync.py

# Don't run start_all_sync.sh until daemon is updated
```

**Use manual sync only:**
```bash
# When you need to sync
bash INBOX_HUB/sync_downloads_folders.sh
```

---

## Why This Wasn't Caught:

1. Daemon runs silently in background
2. No visible indication it's syncing
3. Multiple scripts with similar names
4. No central documentation of all touchpoints
5. Daemon started by startup script, forgotten about

---

**This is why cleanup kept breaking. The daemon was undoing the work.**
