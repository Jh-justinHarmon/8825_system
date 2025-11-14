# Joju Task Layer - Setup Guide

## 🚀 Quick Setup

### **Step 1: Get Notion API Credentials**

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Name it "8825 Joju Tasks"
4. Select your workspace
5. Copy the "Internal Integration Token"

### **Step 2: Create Notion Database**

1. In Notion, create a new database called "Joju Task Board"
2. Add these properties:
   - Task Name (Title) - default
   - Status (Select): Backlog, To Do, In Progress, In Review, Done
   - Priority (Select): Critical, High, Medium, Low
   - Type (Select): Feature, Bug, Enhancement, Research, Documentation
   - Owner (Person)
   - Due Date (Date)
   - Effort (Number)
   - Source (Select): User Feedback, Team Idea, Bug Report, Survey, Competitive Analysis
   - Tags (Multi-select)
   - Description (Text)

3. Share the database with your integration:
   - Click "Share" in top right
   - Invite your integration
   - Copy the database ID from the URL

### **Step 3: Configure 8825**

```bash
cd focuses/joju/tasks

# Copy example config
cp config.example.json config.json

# Edit config.json
# Add your API key and database ID
```

**config.json:**
```json
{
  "notion": {
    "api_key": "secret_YOUR_KEY_HERE",
    "database_id": "YOUR_DATABASE_ID_HERE",
    "workspace": "Joju"
  }
}
```

### **Step 4: Install Dependencies**

```bash
pip3 install notion-client python-dotenv
```

### **Step 5: Test Connection**

```bash
python3 notion_sync.py test
```

Should output: "✅ Connected to Notion successfully"

---

## 📋 Notion Database ID

**Where to find it:**

Your Notion database URL looks like:
```
https://www.notion.so/YOUR_WORKSPACE/DATABASE_ID?v=VIEW_ID
```

The `DATABASE_ID` is the part between the last `/` and the `?`.

**Example:**
```
https://www.notion.so/myworkspace/a1b2c3d4e5f6?v=123456
                                  ^^^^^^^^^^
                                  This is your database ID
```

---

## 🔐 Security

**Important:**
- Never commit `config.json` to git (already in .gitignore)
- Keep your API key secret
- Only share database with necessary integrations
- Rotate API key if compromised

---

## ✅ Verification Checklist

- [ ] Notion integration created
- [ ] Database created with all properties
- [ ] Database shared with integration
- [ ] config.json created with credentials
- [ ] Dependencies installed
- [ ] Connection test passed
- [ ] First sync completed

---

## 🆘 Troubleshooting

### **"Unauthorized" Error**
- Check API key is correct
- Verify database is shared with integration
- Ensure integration has correct permissions

### **"Database not found"**
- Verify database ID is correct
- Check database is shared with integration
- Try re-sharing the database

### **Import Errors**
- Install dependencies: `pip3 install notion-client`
- Check Python version (3.7+)

---

## 📚 Next Steps

After setup:
1. Run initial sync: `python3 notion_sync.py pull`
2. Create your first task: `python3 task_manager.py create --title "Test task"`
3. Link to user feedback: See README.md for examples

---

**Need Help?**  
See main README.md or check Notion API docs: https://developers.notion.com/
