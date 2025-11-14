#!/bin/bash
# Status of Unified File Processing System

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/.watcher.pid"
CONFIG_FILE="$SCRIPT_DIR/../sandbox_target_acquisition/user_config.json"
QUEUE_FILE="$SCRIPT_DIR/processing_queue.txt"
LOG_FILE="$SCRIPT_DIR/logs/unified_processor.log"

echo "============================================================"
echo "8825 UNIFIED SYSTEM STATUS"
echo "============================================================"
echo ""

# Check if configured
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Not configured"
    echo "Run setup: cd ../sandbox_target_acquisition && ./setup_v3.sh"
    exit 1
fi

# Show watched folders
echo "📁 Watched Folders:"
DESKTOP_DOWNLOADS=$(jq -r '.inputs.desktop_downloads' "$CONFIG_FILE")
ICLOUD_DOWNLOADS=$(jq -r '.inputs.icloud_downloads' "$CONFIG_FILE")
SCREENSHOTS=$(jq -r '.inputs.screenshots' "$CONFIG_FILE")

echo "  Desktop Downloads: $DESKTOP_DOWNLOADS"
echo "  iCloud Downloads: $ICLOUD_DOWNLOADS"
echo "  Screenshots: $SCREENSHOTS"
echo ""

# Show output
echo "📁 Output:"
OUTPUT_BASE=$(jq -r '.outputs.base' "$CONFIG_FILE")
echo "  $OUTPUT_BASE"
echo ""

# Check if running
echo "🔄 System Status:"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "  ✓ Running (PID: $PID)"
    else
        echo "  ❌ Not running (stale PID)"
    fi
else
    echo "  ❌ Not running"
fi
echo ""

# Show queue
echo "⏳ Processing Queue:"
if [ -f "$QUEUE_FILE" ] && [ -s "$QUEUE_FILE" ]; then
    queue_count=$(wc -l < "$QUEUE_FILE")
    echo "  $queue_count file(s) waiting"
else
    echo "  Empty"
fi
echo ""

# Show recent activity
echo "📈 Recent Activity (last 10):"
if [ -f "$LOG_FILE" ] && [ -s "$LOG_FILE" ]; then
    tail -10 "$LOG_FILE"
else
    echo "  No activity yet"
fi
echo ""

echo "============================================================"
