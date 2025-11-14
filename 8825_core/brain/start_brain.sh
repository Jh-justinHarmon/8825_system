#!/bin/bash
# Start 8825 Brain Daemon

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$HOME/.8825/brain.pid"
LOG_FILE="$HOME/.8825/brain.log"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "🧠 Brain daemon already running (PID: $PID)"
        exit 0
    else
        echo "⚠️  Stale PID file found, removing..."
        rm "$PID_FILE"
    fi
fi

# Ensure .8825 directory exists
mkdir -p "$HOME/.8825"

# Start daemon in background
echo "🧠 Starting brain daemon..."
nohup python3 "$SCRIPT_DIR/brain_daemon.py" > "$LOG_FILE" 2>&1 &
PID=$!

# Save PID
echo "$PID" > "$PID_FILE"

# Wait a moment for startup
sleep 2

# Check if running
if ps -p "$PID" > /dev/null 2>&1; then
    echo "✅ Brain daemon started (PID: $PID)"
    echo "📋 Log: $LOG_FILE"
    echo "🔌 API: /tmp/8825_brain.sock"
else
    echo "❌ Failed to start brain daemon"
    echo "Check log: $LOG_FILE"
    exit 1
fi
