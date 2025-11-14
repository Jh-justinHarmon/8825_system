#!/bin/bash
# 8825 Target Acquisition - Start Watching
# Launches file watcher and processor

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/user_config.json"
PID_FILE="$SCRIPT_DIR/.watcher.pid"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Error: No configuration found"
    echo "Run ./setup_targets.sh first"
    exit 1
fi

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  System already running (PID: $OLD_PID)"
        echo "Run ./stop.sh to stop it first"
        exit 1
    else
        # Stale PID file, remove it
        rm "$PID_FILE"
    fi
fi

# Read config
screenshots_path=$(jq -r '.watch_paths.screenshots' "$CONFIG_FILE")
downloads_path=$(jq -r '.watch_paths.downloads' "$CONFIG_FILE")
mobile_path=$(jq -r '.watch_paths.mobile' "$CONFIG_FILE")

echo "============================================================"
echo "🚀 Starting 8825 Inbox System..."
echo "============================================================"
echo ""

# Verify paths exist
if [ ! -d "$screenshots_path" ]; then
    echo "❌ Error: Screenshots folder not found: $screenshots_path"
    exit 1
fi

if [ ! -d "$downloads_path" ]; then
    echo "❌ Error: Downloads folder not found: $downloads_path"
    exit 1
fi

if [ -n "$mobile_path" ] && [ "$mobile_path" != "null" ] && [ ! -d "$mobile_path" ]; then
    echo "⚠️  Warning: Mobile folder not found: $mobile_path"
    echo "Continuing without mobile folder..."
    mobile_path=""
fi

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    echo "❌ Error: fswatch not installed"
    echo "Install with: brew install fswatch"
    exit 1
fi

# Create queue and log files if they don't exist
touch "$SCRIPT_DIR/processing_queue.txt"
touch "$SCRIPT_DIR/processing_log.txt"

# Start watcher in background
echo "Starting file watcher..."

# Build watch paths array
WATCH_PATHS=("$screenshots_path" "$downloads_path")
if [ -n "$mobile_path" ] && [ "$mobile_path" != "null" ]; then
    WATCH_PATHS+=("$mobile_path")
fi

# Start fswatch
(
    fswatch -0 "${WATCH_PATHS[@]}" | while read -d "" file; do
        # Skip hidden files and directories
        basename=$(basename "$file")
        if [[ "$basename" == .* ]] || [ -d "$file" ]; then
            continue
        fi
        
        # Log detection
        echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | DETECTED | $file" >> "$SCRIPT_DIR/processing_log.txt"
        
        # Add to queue (avoid duplicates)
        if ! grep -Fxq "$file" "$SCRIPT_DIR/processing_queue.txt"; then
            echo "$file" >> "$SCRIPT_DIR/processing_queue.txt"
            echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | QUEUED   | $file" >> "$SCRIPT_DIR/processing_log.txt"
        fi
    done
) &

WATCHER_PID=$!
echo "$WATCHER_PID" > "$PID_FILE"

echo "✓ Watcher started (PID: $WATCHER_PID)"
echo ""
echo "============================================================"
echo "👀 Watching:"
echo "============================================================"
echo "  📸 Screenshots: $screenshots_path"
echo "  📥 Downloads: $downloads_path"
if [ -n "$mobile_path" ] && [ "$mobile_path" != "null" ]; then
    echo "  📱 Mobile: $mobile_path"
fi
echo ""
echo "============================================================"
echo "System running in background"
echo ""
echo "Commands:"
echo "  ./status.sh  - View status"
echo "  ./stop.sh    - Stop watching"
echo "============================================================"
