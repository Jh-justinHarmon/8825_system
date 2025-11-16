# Gemini API Setup Process - TESTED & VERIFIED

**Status:** ✅ Fully tested and working  
**Date:** 2025-11-14  
**Test Results:** All steps verified

---

## Complete Process

### **Step 1: User Gets API Key**
1. Open `gemini_integration_setup.html` in browser
2. Click "Open Google AI Studio"
3. Create API key (select "Default Gemini Project")
4. Copy key (starts with `AIzaSy`)

### **Step 2: User Enters Key in HTML**
1. Paste key into input field
2. Click "Save & Activate"
3. HTML downloads `.env` file to Downloads
4. HTML copies command to clipboard

### **Step 3: User Tells Cascade**
User says: **"Set up my Gemini API key"** or **"Run the setup command"**

### **Step 4: Cascade Runs Script**
```bash
cd /path/to/8825_core
./set_gemini_key.sh AIzaSy...user-key...
```

### **Step 5: Script Executes**
- ✅ Validates key format (`AIzaSy` prefix)
- ✅ Backs up existing `.env` (if exists)
- ✅ Creates/updates `8825_core/.env`
- ✅ Sets environment variable
- ✅ Shows confirmation

### **Step 6: Verification**
Cascade can now access the key:
```python
from dotenv import load_dotenv
load_dotenv()
import os
key = os.getenv('GOOGLE_GEMINI_API_KEY')
```

---

## Test Results

### ✅ Test 1: No Arguments
```bash
./set_gemini_key.sh
# Result: ❌ Error: No API key provided ✅ PASS
```

### ✅ Test 2: Invalid Format
```bash
./set_gemini_key.sh "invalid-key"
# Result: ❌ Error: Invalid API key format ✅ PASS
```

### ✅ Test 3: First Time Setup
```bash
./set_gemini_key.sh "AIzaSyTEST_KEY..."
# Result: ✅ Added GOOGLE_GEMINI_API_KEY to .env ✅ PASS
# File created: 8825_core/.env
```

### ✅ Test 4: Update Existing Key
```bash
./set_gemini_key.sh "AIzaSyUPDATED_KEY..."
# Result: 
# - 📦 Backed up to backups/env_backups/.env.backup_TIMESTAMP ✅ PASS
# - ✅ Updated GOOGLE_GEMINI_API_KEY ✅ PASS
```

### ✅ Test 5: Python Can Read
```python
from dotenv import load_dotenv
load_dotenv()
import os
key = os.getenv('GOOGLE_GEMINI_API_KEY')
# Result: ✅ Key loaded: AIzaSyUPDA...3210 ✅ PASS
```

---

## File Locations

```
8825_core/
├── .env                              # Created by script
├── set_gemini_key.sh                 # Setup script
└── backups/
    └── env_backups/
        └── .env.backup_TIMESTAMP     # Auto-created backups
```

---

## Important Notes

### **Environment Variables**
- ⚠️ `export` in script only affects that shell session
- ✅ Python must use `python-dotenv` to load `.env`
- ✅ All 8825 Python scripts should use `load_dotenv()`

### **Security**
- ✅ `.env` file is gitignored
- ✅ Backups are also gitignored
- ✅ Keys never committed to repo
- ✅ Local storage only

### **Backups**
- ✅ Auto-created before any update
- ✅ Timestamped for easy recovery
- ✅ Stored in `backups/env_backups/`

---

## For Cascade

When user says "set up gemini" or similar:

1. **Ask for API key** (if not provided)
2. **Validate format** (starts with `AIzaSy`)
3. **Run script:**
   ```bash
   cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/8825_core
   ./set_gemini_key.sh "AIzaSy..."
   ```
4. **Verify success** (check output for ✅)
5. **Confirm to user** (show key preview)

---

## Troubleshooting

### "Script not found"
```bash
# Make executable
chmod +x set_gemini_key.sh
```

### "sed: command not found"
```bash
# macOS should have sed by default
# If not, install: brew install gnu-sed
```

### "Python can't find key"
```python
# Make sure to load .env first
from dotenv import load_dotenv
load_dotenv()  # ← Must call this!
import os
key = os.getenv('GOOGLE_GEMINI_API_KEY')
```

---

## Success Criteria

✅ **All tests passed**
- Error handling works
- Validation works
- File creation works
- Backup works
- Update works
- Python can read it

**Status:** Ready for production use! 🚀

---

## Next Steps

1. User completes HTML flow
2. User tells Cascade to run setup
3. Cascade runs `set_gemini_key.sh`
4. Key is immediately available
5. User can test connection in HTML
