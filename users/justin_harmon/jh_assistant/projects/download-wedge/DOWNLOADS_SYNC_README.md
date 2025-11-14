# 📂 Downloads Folder Sync

**Purpose:** Keep Desktop/Downloads and iCloud/Downloads in sync (bidirectional)  
**Status:** Ready to use  
**Created:** 2025-11-07

---

## 🎯 What It Does

Monitors both Downloads folders and automatically syncs files between them:

```
Desktop/Downloads ⟷ iCloud/Downloads
```

### **Features:**
- ✅ **Bidirectional sync** - Works both ways
- ✅ **Real-time monitoring** - Syncs immediately when files arrive
- ✅ **Initial sync** - Syncs existing files on startup
- ✅ **Excludes "- old -" folders** - Leaves archive folders alone
- ✅ **Preserves structure** - Maintains subfolder organization
- ✅ **Avoids duplicates** - Checks file size before copying
- ✅ **Loop prevention** - Won't create infinite sync loops

---

## 🚀 Quick Start

### Run Sync:
```bash
cd Jh_sandbox/projects/download-wedge
python3 downloads_sync.py
```

### What Happens:
1. **Initial sync** - Copies any missing files between folders
2. **Live monitoring** - Watches for new files
3. **Auto-sync** - Copies files immediately when detected

---

## 📁 Monitored Locations

### Desktop Downloads:
```
~/Downloads/
```

### iCloud Downloads:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/
```

---

## 🚫 Exclusions

These are **NOT** synced:

- **Folders containing "- old -"** (your archive folders)
- **.DS_Store** files
- **.tmp** files
- **~$** files (Office temp files)

---

## 📊 Example Output

```
============================================================
📂 DOWNLOADS FOLDER SYNC
============================================================

📁 Desktop Downloads: /Users/justinharmon/Downloads
☁️  iCloud Downloads:  /Users/justinharmon/Library/.../Downloads

🚫 Excluding: - old -, .DS_Store, .tmp, ~$

============================================================

[2025-11-07 16:45:12] [INFO] 🔄 Starting initial sync...
[2025-11-07 16:45:12] [INFO] 📤 Syncing Desktop → iCloud...
[2025-11-07 16:45:13] [INFO] ✅ Synced: invoice.pdf → iCloud/
[2025-11-07 16:45:13] [INFO] ✅ Synced: meeting_notes.txt → iCloud/
[2025-11-07 16:45:14] [INFO] 📥 Syncing iCloud → Desktop...
[2025-11-07 16:45:14] [INFO] ⏭️  File already synced: document.docx
[2025-11-07 16:45:15] [INFO] ✅ Initial sync complete

⏳ Starting live sync... (Press Ctrl+C to stop)

[2025-11-07 16:47:22] [INFO] 📥 New file detected: screenshot.png
[2025-11-07 16:47:22] [INFO] ✅ Synced: screenshot.png → Desktop/
```

---

## 🔧 How It Works

### 1. Initial Sync (On Startup)
```
Desktop → iCloud: Copy missing files
iCloud → Desktop: Copy missing files
```

### 2. Live Monitoring
```
File arrives in Desktop/Downloads
  ↓
Detect new file
  ↓
Copy to iCloud/Downloads
  ↓
Done!
```

### 3. Bidirectional
Works the same in both directions simultaneously.

---

## ⚙️ Configuration

### Change Exclusions:
Edit `EXCLUDE_PATTERNS` in `downloads_sync.py`:

```python
EXCLUDE_PATTERNS = [
    "- old -",
    ".DS_Store",
    ".tmp",
    "~$",
    # Add your patterns here
    "temp",
    "backup"
]
```

### Change Paths:
Edit paths at top of `downloads_sync.py`:

```python
DESKTOP_DOWNLOADS = Path.home() / "Downloads"
ICLOUD_DOWNLOADS = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Downloads"
```

---

## 📋 Use Cases

### Scenario 1: Browser Downloads
```
Browser saves to Desktop/Downloads
  ↓
Sync tool copies to iCloud/Downloads
  ↓
File available on all devices
```

### Scenario 2: Mobile Upload
```
Upload file to iCloud/Downloads from iPhone
  ↓
Sync tool copies to Desktop/Downloads
  ↓
File available on Mac Desktop
```

### Scenario 3: Archive Folders
```
Move old files to "Downloads/- old - 2024/"
  ↓
Sync tool ignores this folder
  ↓
Archive stays local, not synced
```

---

## 🔔 Logging

### Log File Location:
```
Jh_sandbox/projects/download-wedge/logs/sync.log
```

### View Logs:
```bash
tail -f logs/sync.log
```

---

## 🚀 Run as Background Service

### macOS LaunchAgent:

Create: `~/Library/LaunchAgents/com.jh.downloads-sync.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jh.downloads-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system (v2.0 deleted)/Jh_sandbox/projects/download-wedge/downloads_sync.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/downloads-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/downloads-sync-error.log</string>
</dict>
</plist>
```

### Load Service:
```bash
launchctl load ~/Library/LaunchAgents/com.jh.downloads-sync.plist
```

### Unload Service:
```bash
launchctl unload ~/Library/LaunchAgents/com.jh.downloads-sync.plist
```

---

## ⚠️ Important Notes

### Conflict Resolution:
- **Same filename, different size** → Newer file wins
- **Same filename, same size** → Skips (already synced)

### Performance:
- **Instant sync** for small files (<10MB)
- **Brief delay** for large files (waits for write to complete)

### Safety:
- **No deletions** - Only copies files, never deletes
- **No overwrites** - Skips if destination exists with same size
- **Loop prevention** - Tracks files being processed

---

## 🎯 Integration with Download Wedge

Once files are synced, the Download Wedge can route them:

```
File arrives → Sync to both folders → Wedge analyzes → Route to project
```

Run both tools together:

**Terminal 1:**
```bash
python3 downloads_sync.py
```

**Terminal 2:**
```bash
python3 scripts/file_monitor.py
```

---

## 📊 Statistics

Track sync activity:
- Files synced per day
- Sync direction (Desktop→iCloud vs iCloud→Desktop)
- Average file size
- Excluded files count

(Future feature - add stats dashboard)

---

**Keep your Downloads folders in perfect sync!** 🎯
