#!/bin/bash

# 8825 Unified Sync & MCP Startup Script
# Starts all sync services and MCP production services

echo "============================================================"
echo "🚀 8825 UNIFIED STARTUP"
echo "============================================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_DIR="$(dirname "$SCRIPT_DIR")/mcp"

# Check if watchdog is installed (required for sync services)
if ! python3 -c "import watchdog" 2>/dev/null; then
    echo "⚠️  watchdog not installed. Installing..."
    pip3 install watchdog
fi

echo "📂 Starting Sync Services..."
echo ""

# Start downloads sync (Desktop ⟷ iCloud, excludes 8825_inbox)
echo "1️⃣  Starting downloads_sync.py..."
cd "$SCRIPT_DIR"
nohup python3 downloads_sync.py > logs/downloads_sync.log 2>&1 &
DOWNLOADS_SYNC_PID=$!
echo "   ✅ downloads_sync.py running (PID: $DOWNLOADS_SYNC_PID)"

# Wait a moment
sleep 2

# Start inbox sync (3-way: Desktop ⟷ iCloud ⟷ Dropbox)
echo "2️⃣  Starting inbox_sync.py..."
nohup python3 inbox_sync.py > logs/inbox_sync.log 2>&1 &
INBOX_SYNC_PID=$!
echo "   ✅ inbox_sync.py running (PID: $INBOX_SYNC_PID)"

# Wait a moment
sleep 2

echo ""
echo "📡 Starting MCP Services..."
echo ""

# Start MCP inbox server (localhost:8828)
echo "3️⃣  Starting MCP inbox server..."
cd "$MCP_DIR"
nohup ./start_inbox_server.sh > /tmp/mcp_inbox_server.log 2>&1 &
MCP_SERVER_PID=$!
echo "   ✅ MCP inbox server running (PID: $MCP_SERVER_PID)"

# Wait a moment
sleep 2

# Start universal inbox watch
echo "4️⃣  Starting universal inbox watch..."
nohup ./start_universal_watch.sh > /tmp/universal_inbox_watch.log 2>&1 &
UNIVERSAL_WATCH_PID=$!
echo "   ✅ Universal inbox watch running (PID: $UNIVERSAL_WATCH_PID)"

echo ""
echo "============================================================"
echo "✅ ALL SERVICES STARTED"
echo "============================================================"
echo ""
echo "📊 Service Status:"
echo "   • downloads_sync:       PID $DOWNLOADS_SYNC_PID"
echo "   • inbox_sync:           PID $INBOX_SYNC_PID"
echo "   • MCP inbox server:     PID $MCP_SERVER_PID"
echo "   • Universal watch:      PID $UNIVERSAL_WATCH_PID"
echo ""
echo "📋 Logs:"
echo "   • downloads_sync:       $SCRIPT_DIR/logs/downloads_sync.log"
echo "   • inbox_sync:           $SCRIPT_DIR/logs/inbox_sync.log"
echo "   • MCP inbox server:     /tmp/mcp_inbox_server.log"
echo "   • Universal watch:      /tmp/universal_inbox_watch.log"
echo ""
echo "⏹️  To stop all services:"
echo "   kill $DOWNLOADS_SYNC_PID $INBOX_SYNC_PID $MCP_SERVER_PID $UNIVERSAL_WATCH_PID"
echo ""
echo "============================================================"
echo ""
echo "🎯 System Ready!"
echo ""
echo "   • Save files anywhere → Auto-synced"
echo "   • ChatGPT → MCP → Inbox"
echo "   • Say 'fetch inbox' in Windsurf"
echo ""
echo "============================================================"
