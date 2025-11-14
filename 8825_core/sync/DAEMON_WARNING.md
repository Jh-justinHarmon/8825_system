# ⚠️ DAEMON WARNING - READ BEFORE STARTING

**Date:** 2025-11-09  
**Status:** CRITICAL

---

## DO NOT RUN `start_all_sync.sh` WITHOUT READING THIS

The sync daemons (`downloads_sync.py` and `inbox_sync.py`) run continuously in the background and will sync files between Downloads folders.

---

## What Was Fixed (2025-11-09):

### **downloads_sync.py**
- ✅ Added exclusions for junk files (sticky_, brainstorm, IMG_, etc.)
- ✅ Will no longer re-sync cleaned files
- ✅ Safe to run NOW

### **simple_sync_and_process.sh**
- ✅ Added same exclusions to rsync command
- ✅ Won't copy junk from iCloud to Local

---

## Before Starting Daemons:

### **1. Check if already running:**
```bash
ps aux | grep -E "(downloads_sync|inbox_sync)" | grep -v grep
```

### **2. If running, kill them:**
```bash
pkill -f downloads_sync.py
pkill -f inbox_sync.py
```

### **3. Verify Downloads is clean:**
```bash
ls ~/Downloads
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/Downloads
```

### **4. Start with updated code:**
```bash
cd 8825_core/sync
bash start_all_sync.sh
```

---

## What the Daemons Do:

### **downloads_sync.py**
- Watches Local and iCloud Downloads folders
- Bidirectional sync (any change in one → copied to other)
- NOW excludes junk files (as of 2025-11-09)

### **inbox_sync.py**
- Watches 8825_inbox folder
- 3-way sync (Local ↔ iCloud ↔ Dropbox)
- Only syncs inbox, not main Downloads

---

## If Downloads Gets Cluttered Again:

### **Step 1: Check if daemons are running**
```bash
ps aux | grep downloads_sync
```

### **Step 2: Check daemon logs**
```bash
tail -f 8825_core/sync/logs/downloads_sync.log
```

### **Step 3: Kill and restart**
```bash
pkill -f downloads_sync.py
# Clean Downloads manually
# Restart daemon
```

---

## Alternative: Manual Sync Only

**Don't run the daemons at all:**

```bash
# When you need to sync, run manually:
bash INBOX_HUB/sync_downloads_folders.sh
```

**Pros:**
- Full control
- No background processes
- Can't break cleanup

**Cons:**
- Must remember to sync
- Not automatic

---

## The Problem That Was Fixed:

**Before (2025-11-09):**
1. User cleans Downloads
2. Daemon sees "missing" files
3. Daemon copies them back from iCloud
4. Junk returns
5. Repeat 12 times

**After (2025-11-09):**
1. User cleans Downloads
2. Daemon sees "missing" files
3. Daemon checks exclusion list
4. Files match exclusions → ignored
5. Junk stays gone

---

## Verification Test:

After starting daemons:

1. Clean Downloads manually
2. Wait 5 minutes
3. Check if junk returns
4. If yes → daemon still broken, kill it
5. If no → daemon working correctly

---

**The daemons are NOW safe to run, but test first.**
