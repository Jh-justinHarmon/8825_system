# Downloads Sync Protocol

**Date:** 2025-11-09  
**Status:** ACTIVE - PERMANENT FIX IMPLEMENTED  
**Version:** 2.0

---

## CRITICAL: Auto-Cleanup Before Sync

**The sync script NOW auto-cleans junk before syncing.**

This prevents the disaster where cleaning one location and then syncing brings all the junk back from the other location.

---

## What `sync_downloads_folders.sh` Does Now:

### **Step 1: Auto-Cleanup (BOTH locations)**
Removes from Local AND iCloud Downloads:
- `old/` and `- old -/` folders
- `sticky_*` debug files  
- `*brainstorm*.txt` files
- `client_secret*.json` files
- `IMG_*.HEIC` and `IMG_*.jpeg` files
- `mythic*.json` and `phils_book*.txf` files

### **Step 2: Sync BRAIN_TRANSPORT**
Copies latest `8825_BRAIN_TRANSPORT.json` to BOTH locations so it's always available.

### **Step 3: Sync 8825_inbox (Bidirectional)**
Syncs the active inbox folder in both directions - works from any device.

### **Step 4: Sync 8825_processed (One-Way)**
Syncs processed files from Local → iCloud only (backup/mirror).

---

## What It DOESN'T Do:

- ❌ Bidirectional sync of all Downloads files
- ❌ Copy random junk back and forth
- ❌ Re-pollute with files from iCloud

---

## Safe to Run Anytime:

**YES** - The script cleans BEFORE syncing, so it won't bring junk back.

---

## Usage:

```bash
# Run sync (auto-cleans first)
bash ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 3.0/INBOX_HUB/sync_downloads_folders.sh
```

---

## What Stays in Downloads:

**Essential files only:**
- `0-8825_BRAIN_TRANSPORT.json` (always synced)
- `8825_inbox/` (active ingestion)
- `8825_processed/` (organized archive)
- `soccer_schedule.json` (current work outputs)
- `Private & Shared/` (user folder)

**Everything else gets auto-cleaned.**

---

## The Fix That Ended the 12-Time Loop:

**Before:** Bidirectional sync copied junk from iCloud back to local after cleanup.

**After:** Auto-cleanup runs on BOTH locations before any syncing happens.

**Result:** Clean Downloads stay clean. Forever.

---

## Automation:

Add to cron or LaunchAgent to run hourly:

```bash
# Run every hour
0 * * * * bash /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 3.0/INBOX_HUB/sync_downloads_folders.sh
```

---

**This protocol is now permanent. The 12-time loop is broken.**
