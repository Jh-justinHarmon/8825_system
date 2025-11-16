# Backend Setup Instructions

**Problem:** HTML can't directly write to filesystem. Need Cascade to run the setup command.

---

## Solution

When user clicks "Save & Activate" in the HTML:

1. **HTML downloads `.env` file** to Downloads folder
2. **HTML copies command to clipboard**
3. **User tells Cascade:** "Run the command in my clipboard"
4. **Cascade runs:** `./set_gemini_key.sh AIzaSy...`
5. **Script creates/updates** `8825_core/.env`
6. **Key is immediately active** (no restart needed)

---

## For Cascade

When user says "set up gemini" or "run the command":

```bash
cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/8825_core

# Run with the API key from clipboard or user provides
./set_gemini_key.sh AIzaSy...user-key-here...
```

**The script will:**
- ✅ Validate key format
- ✅ Backup existing .env
- ✅ Create/update .env file
- ✅ Set environment variable
- ✅ Show confirmation

---

## Verification

After running, check:

```bash
# Check .env file exists
ls -la 8825_core/.env

# Check key is in file
grep GOOGLE_GEMINI_API_KEY 8825_core/.env

# Check environment variable
python3 -c 'import os; print(os.getenv("GOOGLE_GEMINI_API_KEY"))'
```

---

## Status

**Current State:** HTML downloads file, user must manually run script  
**Future:** Build proper backend API that HTML can call  
**For Now:** This works and is secure
