# Download Folder Wedge - Quick Start

**Get started in 5 minutes!**

---

## 🚀 Installation

### 1. Install Dependencies
```bash
pip3 install watchdog PyPDF2 python-docx pytesseract Pillow
```

### 2. Install Tesseract (for OCR)
```bash
brew install tesseract
```

### 3. Make Scripts Executable
```bash
cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 2.0/Jh_sandbox/projects/download-wedge
chmod +x scripts/*.py
```

---

## 🎯 Quick Test

### Test Metadata Extraction
```bash
python3 scripts/metadata_extractor.py ~/Downloads/somefile.pdf
```

### Test Content Analysis
```bash
python3 scripts/content_analyzer.py ~/Downloads/somefile.pdf
```

### Test Project Matching
```bash
python3 scripts/project_matcher.py ~/Downloads/somefile.pdf
```

---

## 🏃 Run the Monitor

### Start Monitoring
```bash
python3 scripts/file_monitor.py
```

### What It Does:
1. Watches `~/Downloads/` and iCloud Downloads
2. Analyzes new files automatically
3. Matches to projects
4. Routes or suggests destinations
5. Sends macOS notifications

---

## 📋 How It Works

### Auto-Route (90-100% confidence)
- File is automatically moved to project folder
- Notification confirms action
- No user input needed

### Suggest (50-89% confidence)
- Notification shows suggested destination
- User can approve or move manually
- Reasoning displayed in terminal

### Ask (<50% confidence)
- Shows top 3 project matches
- User must route manually
- Notification alerts to check terminal

---

## 🎯 Example Files to Test

### TGIF Meeting (Should auto-route to HCSS/TGIF)
```bash
touch ~/Downloads/tgif_meeting_2025-11-07.md
```

### Joju Profile (Should suggest 76)
```bash
touch ~/Downloads/joju_profile_test.json
```

### Unknown File (Should ask)
```bash
touch ~/Downloads/random_document.pdf
```

---

## ⚙️ Configuration

### Edit Project Contexts
```bash
nano project_contexts.json
```

### Adjust Confidence Thresholds
```json
{
  "global_settings": {
    "auto_route_threshold": 90,  // Lower for more auto-routing
    "suggest_threshold": 50,     // Lower for more suggestions
    "ask_threshold": 0
  }
}
```

---

## 📊 Monitor Logs

### View Real-Time Logs
```bash
tail -f logs/wedge.log
```

### Check Processing History
```bash
cat logs/wedge.log | grep "✅"
```

---

## 🛑 Stop Monitoring

Press `Ctrl+C` in the terminal running the monitor

---

## 🔧 Troubleshooting

### Dependencies Not Found
```bash
pip3 install --upgrade watchdog PyPDF2 python-docx
```

### OCR Not Working
```bash
brew install tesseract
# Or disable OCR in content_analyzer.py
```

### Notifications Not Showing
```bash
# Check System Preferences > Notifications
# Ensure Terminal/Python has notification permissions
```

---

## 💡 Tips

1. **Test with dry run first** - Check logs before enabling auto-routing
2. **Adjust thresholds** - Start conservative, increase confidence as it learns
3. **Monitor logs** - Watch for patterns to improve matching
4. **Add keywords** - Update project_contexts.json with your specific terms

---

## 🎯 Next Steps

1. Run monitor for a day
2. Review routing accuracy
3. Adjust project contexts
4. Enable auto-routing for high-confidence projects
5. Add more monitored locations

---

**Your intelligent file routing system is ready!** 🚀

**Start monitoring**: `python3 scripts/file_monitor.py`
