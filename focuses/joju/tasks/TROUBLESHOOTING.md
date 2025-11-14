# Joju Task Management - Troubleshooting Guide

**Last Updated:** November 10, 2025

---

## 🚨 Common Issues & Solutions

### 1. "notion-client not installed"

**Error:**
```
❌ notion-client not installed. Run: pip3 install notion-client
```

**Solution:**
```bash
pip3 install notion-client==1.0.0
```

⚠️ **IMPORTANT:** Must use v1.0.0, NOT v2.7.0+

---

### 2. "DatabasesEndpoint has no attribute 'query'"

**Error:**
```
AttributeError: 'DatabasesEndpoint' object has no attribute 'query'
```

**Cause:** Wrong SDK version (v2.7.0+ changed the API)

**Solution:**
```bash
pip3 uninstall notion-client
pip3 install notion-client==1.0.0
```

**Verify version:**
```bash
python3 -c "import pkg_resources; print(pkg_resources.get_distribution('notion-client').version)"
```

Should output: `1.0.0`

---

### 3. "Config file not found"

**Error:**
```
FileNotFoundError: Config file not found: /path/to/config.json
Copy config.example.json to config.json and add your credentials
```

**Solution:**
```bash
cd focuses/joju/tasks
cp config.example.json config.json
# Edit config.json with your Notion API key and database ID
```

**Where to find credentials:**
- Check v2.0 workspace: `8825-system (v2.0 deleted)/config/8825_config.json`
- Or create new integration at: https://www.notion.so/my-integrations

---

### 4. "Invalid request URL"

**Error:**
```
notion_client.errors.APIResponseError: Invalid request URL.
```

**Cause:** Database ID is missing dashes (UUID format)

**Solution:**
Database ID must be in UUID format with dashes:
```
✅ Correct: 2a1fe28f-f8d6-81d7-8e3a-fccd65f2464d
❌ Wrong:   2a1fe28ff8d681d78e3afccd65f2464d
```

**Fix it:**
```bash
python3 << 'EOF'
import json
with open('config.json') as f:
    config = json.load(f)
db_id = config['notion']['database_id']
if '-' not in db_id and len(db_id) == 32:
    formatted = f"{db_id[:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:]}"
    config['notion']['database_id'] = formatted
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ Fixed: {formatted}")
EOF
```

---

### 5. Empty Task Data (All None)

**Symptom:**
```
Task Summary:
By Status: None: 100
By Priority: None: 100
```

**Cause:** Property name mismatch between code and Notion database

**Solution:**
The code has been updated with fallbacks. If you still see this:

1. Check your Notion database property names
2. Update `notion_sync.py` line 159-168 to match your schema

**Common property name differences:**
- `Task name` vs `Task Name`
- `Task Category` vs `Type`
- `Assignee` vs `Owner`
- `Due` vs `Due Date`
- `Sprint Points` vs `Effort`

---

### 6. "Please configure your Notion API key"

**Error:**
```
ValueError: Please configure your Notion API key in config.json
```

**Cause:** config.json still has placeholder value

**Solution:**
Edit `config.json` and replace:
```json
"api_key": "secret_YOUR_NOTION_API_KEY_HERE"
```

With your actual Notion API key from v2.0 or create new at:
https://www.notion.so/my-integrations

---

## 🔍 Diagnostic Commands

### Check Setup
```bash
./check_setup.sh
```

### Test Connection
```bash
python3 notion_sync.py test
```

### Check SDK Version
```bash
python3 -c "import pkg_resources; print(pkg_resources.get_distribution('notion-client').version)"
```

### View Config (without exposing API key)
```bash
python3 -c "import json; c=json.load(open('config.json')); print(f\"Database: {c['notion']['database_id']}\nAPI Key: {c['notion']['api_key'][:10]}...\")"
```

### Test Property Parsing
```bash
python3 << 'EOF'
from notion_client import Client
import json

with open('config.json') as f:
    config = json.load(f)

client = Client(auth=config['notion']['api_key'])
response = client.databases.query(database_id=config['notion']['database_id'])

if response['results']:
    page = response['results'][0]
    print("Available properties:")
    for key in page['properties'].keys():
        print(f"  - {key}")
EOF
```

---

## 📚 Related Documentation

- [NOTION_SETUP_COMPLETE.md](NOTION_SETUP_COMPLETE.md) - Complete setup history
- [README.md](README.md) - Overview
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [SETUP.md](SETUP.md) - Initial setup

---

## 🆘 Still Stuck?

1. **Run the setup checker:**
   ```bash
   ./check_setup.sh
   ```

2. **Check the logs:**
   ```bash
   python3 notion_sync.py pull 2>&1 | tee debug.log
   ```

3. **Verify credentials:**
   - API key starts with `ntn_` or `secret_`
   - Database ID is 32 characters (with or without dashes)
   - Both are from the same Notion workspace

4. **Check Notion permissions:**
   - Integration has access to the database
   - Database is shared with the integration
   - You have edit permissions

---

## 🎓 Learning from This Experience

**What went wrong:**
- SDK version changed between v1.0.0 and v2.7.0
- Property names in Notion database didn't match code expectations
- Database ID format needed dashes
- Config file was gitignored (good for security, but easy to miss)

**What we learned:**
- Always lock SDK versions in requirements.txt
- Document property name mappings
- Add setup checkers before first use
- Keep credentials in version-controlled example files
- Create comprehensive troubleshooting guides

**Time saved next time:** ~25 minutes (vs 30+ minutes of debugging)
