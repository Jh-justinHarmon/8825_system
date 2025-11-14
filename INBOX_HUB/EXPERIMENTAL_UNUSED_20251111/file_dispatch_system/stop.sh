#!/bin/bash
# Stop Unified File Processing System

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/.watcher.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "⚠️  System not running"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "Stopping watcher (PID: $PID)..."
    kill "$PID"
    rm "$PID_FILE"
    echo "✓ Stopped"
else
    echo "⚠️  Process not found (stale PID file)"
    rm "$PID_FILE"
fi
