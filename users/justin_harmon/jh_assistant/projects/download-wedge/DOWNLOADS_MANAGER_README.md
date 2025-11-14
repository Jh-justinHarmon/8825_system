# 📂 Downloads Manager - Enhanced Download Wedge

**Purpose:** Complete download management system with sync, routing, and cleanup  
**Status:** Ready to use  
**Created:** 2025-11-07

---

## 🎯 Complete Workflow

```
File arrives in Downloads
    ↓
1. Sync Desktop ⟷ iCloud
    ↓
2. Copy to Documents/ingestion
    ↓
3. If 8825-created → File to Documents/[Project]/
    ↓
4. After 24 hours → Delete from Downloads
```

---

## ✨ Features

### **1. Bidirectional Sync**
- Desktop/Downloads ⟷ iCloud/Downloads
- Real-time monitoring
- Excludes "- old -" folders

### **2. Universal Ingestion**
- ALL synced files → Documents/ingestion/
- Creates archive of everything that comes through

### **3. Smart Filing (8825 Files Only)**
- Detects 8825-created files
- Routes to appropriate Documents subfolder
- Based on content analysis and project matching

### **4. Automatic Cleanup**
- Filed files deleted after 24 hours
- Removes from BOTH Downloads folders
- Keeps Documents copy permanently

---

## 🔧 8825 File Detection

Files are considered "8825-created" if filename contains:
- `8825`
- `joju`
- `tgif_meeting`
- `_meeting_`
- `problem_statement`
- `project_brief`

---

## 📁 Folder Structure

```
Downloads/
├── Desktop/Downloads/          ← Synced
└── iCloud/Downloads/           ← Synced
    ↓
Documents/
├── ingestion/                  ← ALL files copied here
├── RAL/                        ← Filed by project
├── HCSS/
│   └── TGIF/
├── 76/
│   └── Trustybits/
├── 8825/
├── Jh/
└── Other/
```

---

## 🚀 Quick Start

### Stop Old Sync (if running):
```bash
# Find process
ps aux | grep downloads_sync
kill [PID]
```

### Run Enhanced Manager:
```bash
cd Jh_sandbox/projects/download-wedge
python3 downloads_manager.py
```

---

## 📊 Example Workflow

### Example 1: 8825-Created File
```
JOJU_PROBLEM_STATEMENT_20251107.docx arrives in Desktop/Downloads
    ↓
✅ Synced to iCloud/Downloads
✅ Copied to Documents/ingestion/
✅ Filed to Documents/8825/
    ↓
After 24 hours:
🗑️  Deleted from Desktop/Downloads
🗑️  Deleted from iCloud/Downloads
✅ Remains in Documents/8825/ permanently
```

### Example 2: External File
```
invoice.pdf arrives in iCloud/Downloads
    ↓
✅ Synced to Desktop/Downloads
✅ Copied to Documents/ingestion/
❌ NOT filed (not 8825-created)
    ↓
Stays in Downloads folders indefinitely
```

### Example 3: TGIF Meeting
```
TGIF_Meeting_2025-11-07.docx arrives
    ↓
✅ Synced
✅ Ingested
✅ Filed to Documents/HCSS/TGIF/
    ↓
After 24 hours: Cleaned up from Downloads
```

---

## 🗂️ Filing Logic

### Project Mapping:
- **RAL** → Documents/RAL/
- **HCSS** → Documents/HCSS/
- **TGIF** → Documents/HCSS/TGIF/
- **76** → Documents/76/
- **Trustybits** → Documents/76/Trustybits/
- **8825** → Documents/8825/
- **Jh** → Documents/Jh/
- **Other** → Documents/Other/

### Confidence Levels:
- **90-100%** - High confidence match
- **50-89%** - Medium confidence match
- **0-49%** - Low confidence, filed to "Other"

---

## 📋 Tracking System

### Filed Files Tracked:
```json
{
  "filed_files": [
    {
      "filename": "JOJU_PROBLEM_STATEMENT_20251107.docx",
      "filed_at": "2025-11-07T16:45:00",
      "project": "8825",
      "confidence": 95,
      "desktop_path": "/Users/.../Downloads/...",
      "icloud_path": "/Users/.../Downloads/..."
    }
  ]
}
```

### Tracking File:
`data/filed_files.json`

---

## 🗑️ Cleanup Process

### Runs Every Hour:
1. Check all filed files
2. Calculate age since filing
3. If > 24 hours:
   - Delete from Desktop/Downloads
   - Delete from iCloud/Downloads
   - Remove from tracking
4. Keep in Documents permanently

### Manual Cleanup:
```python
from downloads_manager import cleanup_old_filed_files
cleanup_old_filed_files()
```

---

## 📊 Logs

### Log File:
`logs/manager.log`

### View Live:
```bash
tail -f logs/manager.log
```

### Example Log:
```
[2025-11-07 16:45:00] [INFO] 📥 New file: JOJU_PROBLEM_STATEMENT.docx
[2025-11-07 16:45:00] [INFO] ✅ Synced: JOJU_PROBLEM_STATEMENT.docx → iCloud/
[2025-11-07 16:45:00] [INFO] 📥 Ingested: JOJU_PROBLEM_STATEMENT.docx → Documents/ingestion/
[2025-11-07 16:45:00] [INFO] 🔧 8825 file detected: JOJU_PROBLEM_STATEMENT.docx
[2025-11-07 16:45:00] [INFO] 📁 Filed: JOJU_PROBLEM_STATEMENT.docx → Documents/8825/ (95%)
...
[2025-11-08 16:45:00] [INFO] 🗑️  Cleaned up: JOJU_PROBLEM_STATEMENT.docx (filed 1d ago)
```

---

## ⚙️ Configuration

### Add 8825 File Patterns:
Edit `is_8825_created()` in `downloads_manager.py`:

```python
patterns = [
    "8825",
    "joju",
    "tgif_meeting",
    "_meeting_",
    "problem_statement",
    "project_brief",
    # Add your patterns
    "your_pattern"
]
```

### Change Cleanup Time:
Edit cleanup check in `downloads_manager.py`:

```python
if age > timedelta(hours=24):  # Change to hours=48 for 2 days
```

### Add Project Folders:
Edit `project_folders` in `get_project_destination()`:

```python
project_folders = {
    "RAL": "RAL",
    "HCSS": "HCSS",
    # Add new projects
    "NewProject": "NewProject"
}
```

---

## 🔄 Migration from Old Sync

### If downloads_sync.py is running:
1. Stop it: `Ctrl+C` or `kill [PID]`
2. Start new manager: `python3 downloads_manager.py`

### Difference:
- **Old:** Only sync
- **New:** Sync + Ingestion + Filing + Cleanup

---

## 🎯 Use Cases

### Use Case 1: Export from 8825
```
Generate problem statement in 8825
    ↓
Saved to ~/Downloads/
    ↓
Manager: Syncs, ingests, files to Documents/8825/
    ↓
After 24h: Cleaned from Downloads
```

### Use Case 2: TGIF Meeting Summary
```
Create TGIF meeting summary
    ↓
Saved to Downloads
    ↓
Manager: Files to Documents/HCSS/TGIF/
    ↓
After 24h: Cleaned from Downloads
```

### Use Case 3: External Download
```
Download invoice from email
    ↓
Saved to Downloads
    ↓
Manager: Syncs + ingests (NOT filed)
    ↓
Stays in Downloads for manual handling
```

---

## 🚀 Run as Service

### macOS LaunchAgent:
Create: `~/Library/LaunchAgents/com.jh.downloads-manager.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jh.downloads-manager</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system (v2.0 deleted)/Jh_sandbox/projects/download-wedge/downloads_manager.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

### Load:
```bash
launchctl load ~/Library/LaunchAgents/com.jh.downloads-manager.plist
```

---

## 📊 Statistics Dashboard (Future)

Track:
- Files synced per day
- Files ingested per day
- Files filed by project
- Cleanup actions per day
- Average confidence scores

---

## ⚠️ Important Notes

### Safety:
- **Never deletes unfiled files** - Only 8825-created files that have been filed
- **24-hour grace period** - Plenty of time to catch mistakes
- **Permanent Documents copy** - Filed files kept forever
- **Ingestion backup** - ALL files archived in ingestion/

### Performance:
- Cleanup runs every hour
- Minimal CPU usage
- Instant sync for small files

### Exclusions:
- "- old -" folders never touched
- .DS_Store, .tmp, ~$ files ignored

---

**Complete download management for 8825 workflow!** 🎯
