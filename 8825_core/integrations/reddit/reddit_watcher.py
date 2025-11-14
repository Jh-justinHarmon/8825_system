#!/usr/bin/env python3
"""
Reddit Watcher for r/joju
Monitors subreddit for new posts and comments, saves to JSON files
"""

import praw
import json
import os
from datetime import datetime
from pathlib import Path
import time

class RedditWatcher:
    def __init__(self, config_path=None):
        """Initialize Reddit watcher"""
        self.script_dir = Path(__file__).parent
        
        # Load config
        if config_path is None:
            config_path = self.script_dir / "config.json"
        
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Set up output directory
        self.output_dir = Path(self.config["output_dir"]).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "posts").mkdir(exist_ok=True)
        (self.output_dir / "comments").mkdir(exist_ok=True)
        (self.output_dir / "daily_summaries").mkdir(exist_ok=True)
        
        # Track what we've seen
        self.seen_file = self.output_dir / "seen_ids.json"
        self.seen_ids = self._load_seen_ids()
        
        # Initialize Reddit API
        self.reddit = praw.Reddit(
            client_id=self.config["reddit"]["client_id"],
            client_secret=self.config["reddit"]["client_secret"],
            user_agent=self.config["reddit"]["user_agent"]
        )
        
        self.subreddit = self.reddit.subreddit(self.config["subreddit"])
        
        print(f"✅ Reddit Watcher initialized for r/{self.config['subreddit']}")
    
    def _load_seen_ids(self):
        """Load previously seen post/comment IDs"""
        if self.seen_file.exists():
            with open(self.seen_file) as f:
                return set(json.load(f))
        return set()
    
    def _save_seen_ids(self):
        """Save seen IDs to file"""
        with open(self.seen_file, 'w') as f:
            json.dump(list(self.seen_ids), f, indent=2)
    
    def _save_post(self, post):
        """Save post to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{post.id}.json"
        filepath = self.output_dir / "posts" / filename
        
        post_data = {
            "id": post.id,
            "title": post.title,
            "author": str(post.author) if post.author else "[deleted]",
            "created_utc": post.created_utc,
            "created_readable": datetime.fromtimestamp(post.created_utc).isoformat(),
            "url": f"https://reddit.com{post.permalink}",
            "selftext": post.selftext,
            "score": post.score,
            "num_comments": post.num_comments,
            "link_flair_text": post.link_flair_text,
            "is_self": post.is_self,
            "captured_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(post_data, f, indent=2)
        
        print(f"📝 Saved post: {post.title[:50]}...")
        return post_data
    
    def _save_comment(self, comment):
        """Save comment to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{comment.id}.json"
        filepath = self.output_dir / "comments" / filename
        
        comment_data = {
            "id": comment.id,
            "author": str(comment.author) if comment.author else "[deleted]",
            "created_utc": comment.created_utc,
            "created_readable": datetime.fromtimestamp(comment.created_utc).isoformat(),
            "body": comment.body,
            "score": comment.score,
            "parent_id": comment.parent_id,
            "link_id": comment.link_id,
            "permalink": f"https://reddit.com{comment.permalink}",
            "captured_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(comment_data, f, indent=2)
        
        print(f"💬 Saved comment from u/{comment.author}")
        return comment_data
    
    def check_new_posts(self, limit=10):
        """Check for new posts"""
        new_posts = []
        
        for post in self.subreddit.new(limit=limit):
            if post.id not in self.seen_ids:
                post_data = self._save_post(post)
                new_posts.append(post_data)
                self.seen_ids.add(post.id)
        
        return new_posts
    
    def check_new_comments(self, limit=20):
        """Check for new comments"""
        new_comments = []
        
        for comment in self.subreddit.comments(limit=limit):
            if comment.id not in self.seen_ids:
                comment_data = self._save_comment(comment)
                new_comments.append(comment_data)
                self.seen_ids.add(comment.id)
        
        return new_comments
    
    def create_daily_summary(self, posts, comments):
        """Create daily summary file"""
        if not posts and not comments:
            return
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        summary_file = self.output_dir / "daily_summaries" / f"{date_str}.json"
        
        summary = {
            "date": date_str,
            "new_posts": len(posts),
            "new_comments": len(comments),
            "posts": posts,
            "comments": comments,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Daily summary: {len(posts)} posts, {len(comments)} comments")
    
    def run_once(self):
        """Run a single check"""
        print(f"\n🔍 Checking r/{self.config['subreddit']}...")
        
        new_posts = self.check_new_posts()
        new_comments = self.check_new_comments()
        
        # Save seen IDs
        self._save_seen_ids()
        
        # Create summary if we found anything
        if new_posts or new_comments:
            self.create_daily_summary(new_posts, new_comments)
            print(f"✅ Found {len(new_posts)} new posts, {len(new_comments)} new comments")
        else:
            print("✅ No new activity")
        
        return {
            "posts": new_posts,
            "comments": new_comments
        }
    
    def run_continuous(self, interval=300):
        """Run continuous monitoring"""
        print(f"🔄 Starting continuous monitoring (checking every {interval}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_once()
                print(f"⏳ Waiting {interval} seconds...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Stopping watcher...")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Reddit Watcher for r/joju')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds (default: 300)')
    parser.add_argument('--config', help='Path to config file')
    
    args = parser.parse_args()
    
    watcher = RedditWatcher(config_path=args.config)
    
    if args.once:
        watcher.run_once()
    else:
        watcher.run_continuous(interval=args.interval)


if __name__ == "__main__":
    main()
