#!/bin/bash

# 8825 Dropbox Watch Service Startup Script

echo "Starting 8825 Dropbox Watch Service..."
echo ""
echo "This will monitor ~/Dropbox/8825_inbox/ for new files"
echo "and automatically move them to ~/Downloads/8825_inbox/pending/"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Make sure Python script is executable
chmod +x dropbox_watch.py

# Start the watch service
python3 dropbox_watch.py
