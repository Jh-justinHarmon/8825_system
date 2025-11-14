# Reddit Watcher Setup Guide

Quick setup guide to get the Reddit watcher running.

## Step 1: Install PRAW

```bash
pip3 install praw
```

## Step 2: Get Reddit API Credentials

### Create Reddit App

1. **Go to:** https://www.reddit.com/prefs/apps
2. **Click:** "Create App" or "Create Another App"
3. **Fill in:**
   - Name: `Joju Watcher`
   - App type: **script** (important!)
   - Description: `Monitors r/joju for new activity`
   - About URL: (leave blank)
   - Redirect URI: `http://localhost:8080`
4. **Click:** "Create app"

### Copy Credentials

After creating the app, you'll see:
- **client_id** - The string under "personal use script" (looks like: `abc123XYZ456`)
- **client_secret** - The "secret" field (looks like: `def789ABC123xyz456`)

## Step 3: Configure

Edit `config.json` and replace the placeholders:

```json
{
  "reddit": {
    "client_id": "YOUR_CLIENT_ID_HERE",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "user_agent": "8825:joju-watcher:v1.0 (by /u/YOUR_REDDIT_USERNAME)"
  }
}
```

**Example:**
```json
{
  "reddit": {
    "client_id": "abc123XYZ456",
    "client_secret": "def789ABC123xyz456",
    "user_agent": "8825:joju-watcher:v1.0 (by /u/justinharmon)"
  }
}
```

## Step 4: Test

Run a single check to make sure it works:

```bash
cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/8825_core/integrations/reddit/

python3 reddit_watcher.py --once
```

**Expected output:**
```
✅ Reddit Watcher initialized for r/joju
🔍 Checking r/joju...
✅ No new activity
```

Or if there are posts:
```
✅ Reddit Watcher initialized for r/joju
🔍 Checking r/joju...
📝 Saved post: Welcome to r/joju!...
✅ Found 1 new posts, 0 new comments
```

## Step 5: Set Up Automatic Monitoring (Optional)

To run automatically every 5 minutes:

```bash
# Copy LaunchAgent
cp com.8825.reddit-watcher.plist ~/Library/LaunchAgents/

# Load it
launchctl load ~/Library/LaunchAgents/com.8825.reddit-watcher.plist

# Verify it's running
launchctl list | grep reddit-watcher
```

**To stop automatic monitoring:**
```bash
launchctl unload ~/Library/LaunchAgents/com.8825.reddit-watcher.plist
```

## Step 6: Check Output

Posts and comments are saved to:
```
focuses/joju/reddit_monitoring/
├── posts/           # Individual post files
├── comments/        # Individual comment files
└── daily_summaries/ # Daily rollups
```

**View latest activity:**
```bash
# Latest posts
ls -lt ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/focuses/joju/reddit_monitoring/posts/ | head -5

# Latest comments
ls -lt ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/focuses/joju/reddit_monitoring/comments/ | head -5
```

## Troubleshooting

### "Invalid credentials"
- Double-check your client_id and client_secret
- Make sure you created a **script** type app (not web app)
- Make sure there are no extra spaces in config.json

### "Subreddit not found"
- Check if r/joju actually exists
- Try with a test subreddit first: change `"subreddit": "test"` in config.json

### "ModuleNotFoundError: No module named 'praw'"
```bash
pip3 install praw
```

### Check logs
```bash
# View logs
tail -f /tmp/8825-reddit-watcher.log

# View errors
tail -f /tmp/8825-reddit-watcher-error.log
```

## Quick Commands

```bash
# Test once
python3 reddit_watcher.py --once

# Run continuously (Ctrl+C to stop)
python3 reddit_watcher.py

# Custom interval (10 minutes)
python3 reddit_watcher.py --interval 600

# Start automatic monitoring
launchctl load ~/Library/LaunchAgents/com.8825.reddit-watcher.plist

# Stop automatic monitoring
launchctl unload ~/Library/LaunchAgents/com.8825.reddit-watcher.plist

# Check if running
launchctl list | grep reddit-watcher

# View logs
tail -f /tmp/8825-reddit-watcher.log
```

## Next Steps

Once it's working:
1. Let it run for a day to collect some data
2. Review the JSON files in `focuses/joju/reddit_monitoring/`
3. Decide if you want to integrate with the ingestion engine
4. Set up notifications for important posts (future enhancement)

---

**That's it! You're ready to monitor r/joju.** 🎯
