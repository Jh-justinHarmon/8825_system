#!/bin/bash
# Install Brain Sync Daemon as LaunchAgent

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$SCRIPT_DIR/com.8825.brain_sync_daemon.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/com.8825.brain_sync_daemon.plist"

echo "========================================="
echo "Brain Sync Daemon - Installation"
echo "========================================="
echo ""

# Check if plist exists
if [ ! -f "$PLIST_FILE" ]; then
    echo "❌ Error: plist file not found at $PLIST_FILE"
    exit 1
fi

# Create LaunchAgents directory if it doesn't exist
if [ ! -d "$LAUNCH_AGENTS_DIR" ]; then
    echo "Creating LaunchAgents directory..."
    mkdir -p "$LAUNCH_AGENTS_DIR"
fi

# Unload existing daemon if running
if launchctl list | grep -q "com.8825.brain_sync_daemon"; then
    echo "Stopping existing daemon..."
    launchctl unload "$INSTALLED_PLIST" 2>/dev/null || true
fi

# Copy plist to LaunchAgents
echo "Installing daemon..."
cp "$PLIST_FILE" "$INSTALLED_PLIST"

# Load the daemon
echo "Starting daemon..."
launchctl load "$INSTALLED_PLIST"

# Verify it's running
sleep 2
if launchctl list | grep -q "com.8825.brain_sync_daemon"; then
    echo ""
    echo "✅ Brain Sync Daemon installed and running!"
    echo ""
    echo "Commands:"
    echo "  Status:    launchctl list | grep brain_sync"
    echo "  Stop:      launchctl unload ~/Library/LaunchAgents/com.8825.brain_sync_daemon.plist"
    echo "  Start:     launchctl load ~/Library/LaunchAgents/com.8825.brain_sync_daemon.plist"
    echo "  Uninstall: rm ~/Library/LaunchAgents/com.8825.brain_sync_daemon.plist"
    echo ""
    echo "Logs:"
    echo "  Daemon:    tail -f $SCRIPT_DIR/state/daemon_log.jsonl"
    echo "  Stdout:    tail -f $SCRIPT_DIR/state/daemon_stdout.log"
    echo "  Stderr:    tail -f $SCRIPT_DIR/state/daemon_stderr.log"
else
    echo ""
    echo "❌ Error: Daemon failed to start"
    echo "Check logs at:"
    echo "  $SCRIPT_DIR/state/daemon_stderr.log"
    exit 1
fi
