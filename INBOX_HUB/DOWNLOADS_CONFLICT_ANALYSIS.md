# Downloads Sync Conflict - Deep Dive Analysis

**Date:** November 12, 2025  
**Attempts to Fix:** 13+  
**Status:** STILL BROKEN

---

## The Core Problem

**You have TWO input folders but MULTIPLE systems trying to manage them:**

1. **Desktop Downloads** (`~/Downloads`) - Desktop input
2. **iCloud Downloads** (`~/Library/Mobile Documents/com~apple~CloudDocs/Downloads`) - Mobile input

**Both need to be inputs. Neither should sync to the other. But multiple systems are interfering.**

---

## ALL Systems Touching Downloads (Found)

### **1. LaunchAgent: com.8825.inbox-pipeline** ✅ ACTIVE
**Location:** `~/Library/LaunchAgents/com.8825.inbox-pipeline.plist`  
**Runs:** Every hour + when Desktop Downloads changes  
**Script:** `INBOX_HUB/simple_sync_and_process.sh`

**What it does:**
- ✅ Syncs iCloud → Desktop (one-way, lines 40-54)
- ✅ Processes files from Desktop Downloads
- ✅ Archives to `8825_processed`
- ❌ Does NOT sync back to iCloud (disabled, line 162-171)

**PROBLEM:** Still syncing iCloud → Desktop, which means:
- Files added to iCloud get copied to Desktop
- Brain Transport in iCloud gets copied to Desktop
- Creates duplicates

---

### **2. Brain Transport Generator** ✅ ACTIVE
**Location:** `8825_core/brain/brain_transport_generator.py`  
**Runs:** Every 30s via Brain Sync Daemon (when threshold met)

**What it does:**
- Writes to: `INBOX_HUB/users/jh/intake/documents/8825_BRAIN_TRANSPORT.json`
- Writes to: `~/Library/.../iCloud/Downloads/0-8825_BRAIN_TRANSPORT.json`

**PROBLEM:** Writes to iCloud Downloads, then sync script copies it to Desktop Downloads → duplicate

---

### **3. downloads_sync.py** ❌ NOT RUNNING (but exists)
**Location:** `users/justin_harmon/jh_assistant/projects/download-wedge/downloads_sync.py`  
**Status:** Not running (verified with `ps aux`)

**What it would do if running:**
- Bidirectional sync Desktop ⟷ iCloud
- Uses watchdog for real-time sync

**PROBLEM:** Even though not running, it exists and could be started accidentally

---

### **4. downloads_manager.py** ❌ NOT RUNNING (but exists)
**Location:** `users/justin_harmon/jh_assistant/projects/download-wedge/downloads_manager.py`  
**Status:** Not running (verified with `ps aux`)

**What it would do if running:**
- Bidirectional sync Desktop ⟷ iCloud
- Routes files to Documents/8825
- Copies to ingestion
- Deletes after 24 hours

**PROBLEM:** Even though not running, it exists and could be started accidentally

---

### **5. auto_sync_daemon.py** ❌ NOT RUNNING (but exists)
**Location:** `INBOX_HUB/auto_sync_daemon.py`  
**Status:** Not running (verified with `ps aux`)

**What it would do if running:**
- Watches Desktop, Downloads, Screenshots
- Routes by file type

**PROBLEM:** Even though not running, it exists and could be started accidentally

---

## The Conflict Chain

```
1. You save Brain Transport to iCloud Downloads
   ↓
2. LaunchAgent triggers (watches Desktop Downloads)
   ↓
3. simple_sync_and_process.sh runs
   ↓
4. rsync copies iCloud → Desktop (line 40-54)
   ↓
5. Brain Transport now in BOTH locations
   ↓
6. Brain Sync Daemon triggers (change detected)
   ↓
7. Regenerates Brain Transport to iCloud Downloads
   ↓
8. LOOP REPEATS
```

---

## Why Previous Fixes Failed

### **Attempt 1-5:** Bidirectional sync
- **Problem:** Created sync loops, conflicts, duplicates

### **Attempt 6-8:** One-way sync iCloud → Desktop
- **Problem:** Still creates duplicates, Desktop becomes source of truth

### **Attempt 9-10:** One-way sync Desktop → iCloud
- **Problem:** Mobile uploads get overwritten

### **Attempt 11-12:** No sync at all
- **Problem:** Mobile uploads never reach processing

### **Attempt 13 (Today):** Brain Transport to iCloud only
- **Problem:** Sync script STILL copies it to Desktop

---

## The Root Cause

**You cannot have:**
1. Two input folders
2. Sync between them
3. Outputs going to either folder

**Pick TWO of the three. You're trying to do all three.**

---

## Permanent Solutions

### **Option 1: Separate Input/Output Completely** ⭐ RECOMMENDED

**Inputs (No Sync):**
- Desktop Downloads - Desktop input only
- iCloud Downloads - Mobile input only
- **Never sync between them**

**Outputs (Separate Location):**
- Brain Transport → `~/Documents/8825_BRAIN_TRANSPORT.json`
- Other outputs → `~/Documents/8825/outputs/`

**Processing:**
- LaunchAgent watches BOTH folders independently
- Processes from each separately
- Archives to separate locations

**Benefits:**
- No sync = no conflicts
- Clear separation of concerns
- Both folders remain inputs
- Outputs go elsewhere

---

### **Option 2: Single Input Folder**

**Pick ONE:**
- Desktop Downloads only (disable iCloud sync)
- iCloud Downloads only (disable Desktop sync)

**Benefits:**
- Simple, no conflicts
- Single source of truth

**Drawbacks:**
- Lose mobile OR desktop input

---

### **Option 3: Sync with Exclusions**

**Keep sync but exclude ALL outputs:**
```bash
rsync -au \
    --exclude="0-8825_BRAIN_TRANSPORT.json" \
    --exclude="8825_processed" \
    --exclude="*.meta.json" \
    --exclude="T-8825-*" \
    "$ICLOUD_DOWNLOADS/" "$LOCAL_DOWNLOADS/"
```

**Benefits:**
- Both folders remain inputs
- Outputs don't sync

**Drawbacks:**
- Still have sync complexity
- Easy to forget exclusions

---

## My Strong Recommendation: Option 1

### **Implementation:**

1. **Stop ALL syncing between Downloads folders**
   - Remove rsync from `simple_sync_and_process.sh`
   - Ensure no other sync scripts running

2. **Change Brain Transport output**
   - From: `~/Library/.../iCloud/Downloads/`
   - To: `~/Documents/8825_BRAIN_TRANSPORT.json`

3. **Update LaunchAgent to watch BOTH folders**
   ```xml
   <key>WatchPaths</key>
   <array>
       <string>/Users/justinharmon/Downloads</string>
       <string>/Users/justinharmon/Library/Mobile Documents/com~apple~CloudDocs/Downloads</string>
   </array>
   ```

4. **Process each folder independently**
   - Desktop Downloads → process → archive to `~/Downloads/8825_processed/`
   - iCloud Downloads → process → archive to `~/Library/.../iCloud/Downloads/8825_processed/`

5. **All outputs go to Documents**
   - Brain Transport: `~/Documents/8825_BRAIN_TRANSPORT.json`
   - Other outputs: `~/Documents/8825/outputs/`
   - Symlink to Desktop if needed for easy access

---

## Files to Modify

### **1. simple_sync_and_process.sh**
- Remove lines 34-58 (iCloud → Desktop sync)
- Add iCloud Downloads processing
- Keep separate archives

### **2. brain_transport_generator.py**
- Change output from iCloud Downloads to Documents

### **3. com.8825.inbox-pipeline.plist**
- Add iCloud Downloads to WatchPaths

### **4. Archive/Delete**
- `downloads_sync.py` → Archive (not needed)
- `downloads_manager.py` → Archive (not needed)
- `auto_sync_daemon.py` → Archive (not needed)

---

## Testing Plan

1. **Stop LaunchAgent**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.8825.inbox-pipeline.plist
   ```

2. **Clear both Downloads folders**
   ```bash
   # Move everything to temp
   mv ~/Downloads/* /tmp/downloads_backup/
   mv ~/Library/.../iCloud/Downloads/* /tmp/icloud_backup/
   ```

3. **Implement changes**

4. **Test Desktop input**
   - Drop file in Desktop Downloads
   - Verify processing
   - Verify NO sync to iCloud

5. **Test Mobile input**
   - Drop file in iCloud Downloads
   - Verify processing
   - Verify NO sync to Desktop

6. **Test Brain Transport**
   - Trigger regeneration
   - Verify goes to Documents only
   - Verify NOT in either Downloads folder

7. **Monitor for 24 hours**

---

## Success Criteria

✅ Desktop Downloads: Input only, no outputs  
✅ iCloud Downloads: Input only, no outputs  
✅ No sync between Downloads folders  
✅ Brain Transport in Documents only  
✅ Both folders process independently  
✅ No duplicates, no conflicts  
✅ No manual monitoring needed  

---

## Next Steps

**I can implement Option 1 right now. It will take:**
- 30 min to modify scripts
- 10 min to test
- 24 hours to verify stability

**Want me to proceed?**
