#!/bin/bash
# Start ALL MCP Servers for 8825 Mode
# Created: 2025-11-13

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

MCP_DIR="$HOME/mcp_servers"
LOG_DIR="$HOME/.8825/mcp_logs"

# Create log directory
mkdir -p "$LOG_DIR"

echo -e "${BLUE}=== Checking MCP Servers ===${NC}"
echo ""

# Function to check if server is available
check_mcp_available() {
    local name="$1"
    local server_path="$2"
    
    if [ -f "$server_path" ]; then
        echo -e "  ${GREEN}✅${NC} $name available"
        return 0
    else
        echo -e "  ${RED}❌${NC} $name not found"
        return 1
    fi
}

# Check centralized MCP servers (stdio-based, launched by MCP clients)
echo -e "${BLUE}[1/2] Centralized MCP Servers (for Goose/MCP clients)${NC}"

if [ -d "$MCP_DIR" ]; then
    check_mcp_available "8825-core" "$MCP_DIR/8825-core/server.py"
    check_mcp_available "hcss-bridge" "$MCP_DIR/hcss-bridge/server.js"
    check_mcp_available "figma-make-transformer" "$MCP_DIR/figma-make-transformer/server.js"
    check_mcp_available "figjam" "$MCP_DIR/figjam/server.js"
    
    echo -e "  ${BLUE}ℹ${NC}  These are stdio-based, launched by MCP clients (Goose, etc.)"
else
    echo -e "  ${YELLOW}⚠️${NC} MCP directory not found: $MCP_DIR"
fi

echo ""

# Check inbox server
echo -e "${BLUE}[2/2] Inbox Server${NC}"

INBOX_SERVER="$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/mcp/inbox_server.py"

if [ -f "$INBOX_SERVER" ]; then
    if pgrep -f "inbox_server.py" > /dev/null 2>&1; then
        PID=$(pgrep -f "inbox_server.py")
        echo -e "  ${GREEN}✅${NC} inbox_server running (PID: $PID)"
    else
        echo -e "  ${YELLOW}⚠️${NC} inbox_server not running"
        echo -e "  ${BLUE}ℹ${NC}  Starting inbox_server..."
        cd "$(dirname "$INBOX_SERVER")"
        nohup python3 inbox_server.py > "$LOG_DIR/inbox_server.log" 2>&1 &
        sleep 2
        
        if pgrep -f "inbox_server.py" > /dev/null 2>&1; then
            PID=$(pgrep -f "inbox_server.py")
            echo -e "  ${GREEN}✅${NC} inbox_server started (PID: $PID)"
        else
            echo -e "  ${RED}❌${NC} inbox_server failed to start (check $LOG_DIR/inbox_server.log)"
        fi
    fi
else
    echo -e "  ${YELLOW}⚠️${NC} Inbox server not found at: $INBOX_SERVER"
fi

echo ""
echo -e "${GREEN}=== MCP Check Complete ===${NC}"
echo ""
