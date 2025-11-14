#!/bin/bash
# Start Unified File Processing System

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/.watcher.pid"
CONFIG_FILE="$SCRIPT_DIR/../sandbox_target_acquisition/user_config.json"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config not found"
    echo "Run setup first: cd ../sandbox_target_acquisition && ./setup_v3.sh"
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
        rm "$PID_FILE"
    fi
fi

echo "============================================================"
echo "🚀 Starting Unified File Processing System"
echo "============================================================"
echo ""

# Start watcher in background
"$SCRIPT_DIR/watch.sh" &
WATCHER_PID=$!

# Save PID
echo "$WATCHER_PID" > "$PID_FILE"

echo "✓ Watcher started (PID: $WATCHER_PID)"
echo ""

# Show config
DESKTOP_DOWNLOADS=$(jq -r '.inputs.desktop_downloads' "$CONFIG_FILE")
ICLOUD_DOWNLOADS=$(jq -r '.inputs.icloud_downloads' "$CONFIG_FILE")
SCREENSHOTS=$(jq -r '.inputs.screenshots' "$CONFIG_FILE")
OUTPUT_BASE=$(jq -r '.outputs.base' "$CONFIG_FILE")

echo "============================================================"
echo "👀 Watching:"
echo "============================================================"
echo "  📥 Desktop Downloads: $DESKTOP_DOWNLOADS"
echo "  📱 iCloud Downloads: $ICLOUD_DOWNLOADS"
echo "  📸 Screenshots: $SCREENSHOTS"
echo ""
echo "📁 Output: $OUTPUT_BASE"
echo ""
echo "============================================================"
echo "System running in background"
echo ""
echo "Commands:"
echo "  ./status.sh  - View status"
echo "  ./stop.sh    - Stop system"
echo "============================================================"
