#!/bin/bash
# 8825 Target Acquisition - Status Dashboard

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/user_config.json"
PID_FILE="$SCRIPT_DIR/.watcher.pid"
QUEUE_FILE="$SCRIPT_DIR/processing_queue.txt"
LOG_FILE="$SCRIPT_DIR/processing_log.txt"

echo "============================================================"
echo "8825 INBOX STATUS"
echo "============================================================"
echo ""

# Check if configured
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Not configured"
    echo "Run ./setup_targets.sh first"
    exit 1
fi

# Show watched folders
echo "📁 Watched Folders:"
screenshots_path=$(jq -r '.watch_paths.screenshots' "$CONFIG_FILE")
downloads_path=$(jq -r '.watch_paths.downloads' "$CONFIG_FILE")
mobile_path=$(jq -r '.watch_paths.mobile' "$CONFIG_FILE")

echo "  Screenshots: $screenshots_path"
echo "  Downloads: $downloads_path"
if [ -n "$mobile_path" ] && [ "$mobile_path" != "null" ]; then
    echo "  Mobile: $mobile_path"
fi
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
    echo ""
    echo "  Next 5:"
    head -5 "$QUEUE_FILE" | while read -r file; do
        echo "    • $(basename "$file")"
    done
else
    echo "  Empty"
fi
echo ""

# Show recent activity
echo "📈 Recent Activity (last 10):"
if [ -f "$LOG_FILE" ] && [ -s "$LOG_FILE" ]; then
    tail -10 "$LOG_FILE" | while IFS='|' read -r timestamp action file; do
        timestamp=$(echo "$timestamp" | xargs)
        action=$(echo "$action" | xargs)
        file=$(echo "$file" | xargs)
        basename=$(basename "$file")
        
        case "$action" in
            DETECTED) icon="🔍" ;;
            QUEUED)   icon="📥" ;;
            PROCESS)  icon="⚙️" ;;
            ROUTED)   icon="✓" ;;
            *)        icon="•" ;;
        esac
        
        echo "  $icon $action: $basename"
    done
else
    echo "  No activity yet"
fi
echo ""

echo "============================================================"
