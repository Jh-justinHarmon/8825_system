#!/bin/bash

# 8825 Universal Inbox Watch Service Startup Script

echo "Starting 8825 Universal Inbox Watch Service..."
echo ""
echo "This will monitor ALL inbox locations:"
echo "  1. ~/Downloads/8825_inbox/"
echo "  2. ~/Library/Mobile Documents/.../Downloads/8825_inbox/ (iCloud)"
echo "  3. ~/Dropbox/8825_inbox/"
echo ""
echo "All files will funnel to: ~/Downloads/8825_inbox/pending/"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Make sure Python script is executable
chmod +x universal_inbox_watch.py

# Start the watch service
python3 universal_inbox_watch.py
