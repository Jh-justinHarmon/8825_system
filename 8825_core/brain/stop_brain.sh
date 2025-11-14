#!/bin/bash
# Stop 8825 Brain Daemon

PID_FILE="$HOME/.8825/brain.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "🧠 Brain daemon not running (no PID file)"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 Stopping brain daemon (PID: $PID)..."
    kill "$PID"
    
    # Wait for graceful shutdown
    sleep 2
    
    # Force kill if still running
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️  Forcing shutdown..."
        kill -9 "$PID"
    fi
    
    rm "$PID_FILE"
    echo "✅ Brain daemon stopped"
else
    echo "⚠️  Brain daemon not running (stale PID file)"
    rm "$PID_FILE"
fi

# Clean up socket
if [ -S "/tmp/8825_brain.sock" ]; then
    rm "/tmp/8825_brain.sock"
fi
