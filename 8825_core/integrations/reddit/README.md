# Reddit Watcher for r/joju

Monitors the Joju subreddit for new posts and comments, saves them to JSON files.

## Features

- ✅ Monitors r/joju for new posts
- ✅ Monitors r/joju for new comments
- ✅ Saves each post/comment as individual JSON file
- ✅ Creates daily summaries
- ✅ Tracks seen IDs to avoid duplicates
- ✅ Can run once or continuously
- ✅ Ready for LaunchAgent integration

## Setup

### 1. Install Dependencies

```bash
pip3 install praw
```

### 2. Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name:** Joju Watcher
   - **App type:** Script
   - **Description:** Monitors r/joju for new activity
   - **About URL:** (leave blank)
   - **Redirect URI:** http://localhost:8080
4. Click "Create app"
5. Copy your credentials:
   - **client_id** - the string under "personal use script"
   - **client_secret** - the "secret" field

### 3. Configure

Edit `config.json`:

```json
{
  "subreddit": "joju",
  "reddit": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "user_agent": "8825:joju-watcher:v1.0 (by /u/YOUR_USERNAME)"
  }
}
```

## Usage

### Run Once (Manual Check)

```bash
python3 reddit_watcher.py --once
```

### Run Continuously (Every 5 minutes)

```bash
python3 reddit_watcher.py
```

### Custom Interval (Every 10 minutes)

```bash
python3 reddit_watcher.py --interval 600
```

## Output Structure

```
focuses/joju/reddit_monitoring/
├── posts/                      # Individual post files
│   └── 20251111_173000_abc123.json
├── comments/                   # Individual comment files
│   └── 20251111_173015_def456.json
├── daily_summaries/            # Daily rollups
│   └── 2025-11-11.json
└── seen_ids.json              # Tracking file (don't delete)
```

## Post JSON Format

```json
{
  "id": "abc123",
  "title": "Post title",
  "author": "username",
  "created_utc": 1699999999,
  "created_readable": "2025-11-11T17:30:00",
  "url": "https://reddit.com/r/joju/comments/abc123/...",
  "selftext": "Post content...",
  "score": 5,
  "num_comments": 2,
  "link_flair_text": null,
  "is_self": true,
  "captured_at": "2025-11-11T17:30:00"
}
```

## Comment JSON Format

```json
{
  "id": "def456",
  "author": "username",
  "created_utc": 1699999999,
  "created_readable": "2025-11-11T17:30:15",
  "body": "Comment text...",
  "score": 3,
  "parent_id": "t3_abc123",
  "link_id": "t3_abc123",
  "permalink": "https://reddit.com/r/joju/comments/abc123/.../def456",
  "captured_at": "2025-11-11T17:30:15"
}
```

## LaunchAgent (Automatic Monitoring)

To run automatically every 5 minutes:

```bash
# Copy the plist file
cp com.8825.reddit-watcher.plist ~/Library/LaunchAgents/

# Load it
launchctl load ~/Library/LaunchAgents/com.8825.reddit-watcher.plist

# Check status
launchctl list | grep reddit-watcher
```

## Integration with 8825

### Option 1: Manual Review
- Posts/comments saved to `focuses/joju/reddit_monitoring/`
- Review daily summaries
- Manually process interesting items

### Option 2: Auto-Route to Ingestion
Enable in `config.json`:
```json
{
  "routing": {
    "enabled": true,
    "route_to_ingestion": true
  }
}
```

This will copy new posts/comments to the ingestion folder for automatic processing.

## Monitoring

### Check Logs
```bash
tail -f /tmp/8825-reddit-watcher.log
```

### View Latest Activity
```bash
# Latest posts
ls -lt focuses/joju/reddit_monitoring/posts/ | head -5

# Latest comments
ls -lt focuses/joju/reddit_monitoring/comments/ | head -5

# Today's summary
cat focuses/joju/reddit_monitoring/daily_summaries/$(date +%Y-%m-%d).json
```

## Troubleshooting

### "Invalid credentials"
- Check your client_id and client_secret in config.json
- Make sure you created a "script" type app, not "web app"

### "Subreddit not found"
- Check if r/joju exists
- Try with a test subreddit first (e.g., "test")

### No new posts/comments
- The watcher only captures NEW activity after it starts
- It won't retroactively capture old posts
- Check r/joju to see if there's actually new activity

## Commands

```bash
# Run once (test)
python3 reddit_watcher.py --once

# Run continuously (default 5 min interval)
python3 reddit_watcher.py

# Run with custom interval (10 minutes)
python3 reddit_watcher.py --interval 600

# Use custom config
python3 reddit_watcher.py --config /path/to/config.json
```

## Notes

- The watcher tracks seen IDs in `seen_ids.json` - don't delete this file
- Posts/comments are saved immediately when detected
- Daily summaries are created when new activity is found
- The watcher is read-only - it never posts or comments
- Rate limits: Reddit allows ~60 requests per minute for scripts

## Future Enhancements

- [ ] Sentiment analysis on posts/comments
- [ ] Keyword alerts (email/notification)
- [ ] Auto-respond to specific questions
- [ ] Integration with Joju task system
- [ ] Weekly/monthly trend reports
- [ ] User engagement metrics
