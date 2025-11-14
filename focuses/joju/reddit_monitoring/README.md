# Joju Reddit Monitoring

This directory contains all activity captured from r/joju.

## Structure

```
reddit_monitoring/
├── posts/              # Individual post files (JSON)
├── comments/           # Individual comment files (JSON)
├── daily_summaries/    # Daily rollup summaries (JSON)
└── seen_ids.json       # Tracking file (don't delete)
```

## Files

### Posts
Each post is saved as: `YYYYMMDD_HHMMSS_postid.json`

Example: `20251111_173000_abc123.json`

### Comments
Each comment is saved as: `YYYYMMDD_HHMMSS_commentid.json`

Example: `20251111_173015_def456.json`

### Daily Summaries
One file per day: `YYYY-MM-DD.json`

Contains all posts and comments captured that day.

## Usage

### View Latest Activity
```bash
# Latest posts
ls -lt posts/ | head -5

# Latest comments
ls -lt comments/ | head -5

# Today's summary
cat daily_summaries/$(date +%Y-%m-%d).json | jq
```

### Search for Keywords
```bash
# Find posts mentioning "bug"
grep -l "bug" posts/*.json

# Find comments from specific user
grep -l "username" comments/*.json
```

### Count Activity
```bash
# Total posts captured
ls posts/*.json 2>/dev/null | wc -l

# Total comments captured
ls comments/*.json 2>/dev/null | wc -l

# Activity today
ls posts/$(date +%Y%m%d)*.json 2>/dev/null | wc -l
```

## Integration

This data can be:
1. Manually reviewed for user feedback
2. Routed to ingestion engine for processing
3. Analyzed for trends and sentiment
4. Used to create tasks in Joju system

## Monitoring

The Reddit watcher runs automatically every 5 minutes via LaunchAgent.

**Check status:**
```bash
launchctl list | grep reddit-watcher
```

**View logs:**
```bash
tail -f /tmp/8825-reddit-watcher.log
```

---

**Watcher script:** `8825_core/integrations/reddit/reddit_watcher.py`
