# Update & Publish Workflow

## 🔄 Automated Update Pattern

When you have new user feedback, run this single command to update everything:

```bash
./update_and_publish.sh
```

## 📋 What It Does Automatically:

### **Step 1: Extract Data**
- Scans all user testing sessions
- Extracts quotes and themes
- Groups similar insights
- Counts mentions

### **Step 2: Generate Dashboard**
- Creates standalone HTML with embedded logo
- Updates stats dynamically
- Includes all latest feedback

### **Step 3: Publish**
- Copies to public Joju folder for distribution
- Creates timestamped backup
- Ready to share with team

## 📍 Distribution Location

**Main file (always current):**
```
/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/joju/public/user_engagement_dashboard.html
```

**Backups (timestamped):**
```
/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/joju/public/user_engagement_dashboard_YYYYMMDD_HHMMSS.html
```

## 🚀 Quick Start

### **When New Feedback Arrives:**

1. **Add feedback files** to the appropriate location:
   ```
   ~/Downloads/8825_inbox/processing/lane_b/
   ```

2. **Run update script:**
   ```bash
   cd focuses/joju/user_engagement
   ./update_and_publish.sh
   ```

3. **Share with team:**
   - Email the file from public folder
   - Or share the public folder location
   - Or upload to Slack/Teams

## 📁 File Structure

```
focuses/joju/user_engagement/
├── update_and_publish.sh          # ← Run this to update
├── dashboard.html                  # Development version
├── joju_logo.png                   # Logo file
├── all_user_testing_data.json     # Extracted data
└── joju_user_engagement_dashboard_standalone.html  # Generated

/Users/.../Public/joju/public/
├── user_engagement_dashboard.html              # ← Share this (current)
├── user_engagement_dashboard_20251110_153000.html  # Backup
└── user_engagement_dashboard_20251110_160000.html  # Backup
```

## 🎯 Manual Steps (if needed)

### **Extract Data Only:**
```bash
python3 ../../8825_core/workflows/extract_all_user_testing.py
```

### **Generate Standalone Only:**
```bash
python3 -c "import base64; ..." # (see script)
```

### **Copy to Public Only:**
```bash
cp joju_user_engagement_dashboard_standalone.html \
   "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/joju/public/user_engagement_dashboard.html"
```

## 📊 Versioning Strategy

**Current Version:**
- Always named `user_engagement_dashboard.html`
- Overwrites previous version
- This is what you share with team

**Backups:**
- Timestamped: `user_engagement_dashboard_YYYYMMDD_HHMMSS.html`
- Kept for history/rollback
- Automatically created on each update

## 💡 Best Practices

### **Before Updating:**
- ✅ Ensure all new feedback files are in place
- ✅ Check that extraction script runs without errors
- ✅ Review generated data for accuracy

### **After Updating:**
- ✅ Open the dashboard to verify it looks correct
- ✅ Check stats are updated
- ✅ Test click-to-expand buckets
- ✅ Share with team

### **Sharing:**
- ✅ Use descriptive email subject: "User Feedback Dashboard - Updated Nov 10"
- ✅ Mention what's new: "Added 3 new sessions, 25 new quotes"
- ✅ Include quick stats in email body

## 🔧 Troubleshooting

### **Script fails at Step 1:**
- Check that user testing files exist
- Verify file paths in extraction script

### **Script fails at Step 2:**
- Ensure `joju_logo.png` exists
- Check Python dependencies

### **Script fails at Step 3:**
- Verify public folder path
- Check write permissions

### **Dashboard looks wrong:**
- Clear browser cache
- Re-download file
- Check file size (should be ~700KB)

## 📅 Update Schedule

**Recommended:**
- After each user testing session
- Weekly during active feedback collection
- Monthly during maintenance

**Notify Team:**
- Send update email when dashboard refreshed
- Include summary of new feedback
- Highlight key themes

---

**Created:** November 10, 2025
**Script:** update_and_publish.sh
**Status:** ✅ Automated & Ready
