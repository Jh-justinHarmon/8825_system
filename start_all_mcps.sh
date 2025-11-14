#!/bin/bash
# Start All MCP Servers
# Launches all 8825 MCP servers in background

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check dependencies first
echo -e "${BLUE}=== Checking Dependencies ===${NC}"
"$SCRIPT_DIR/check_dependencies.sh" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Installing missing dependencies...${NC}"
    "$SCRIPT_DIR/check_dependencies.sh"
fi

# Check Notion integration for Joju tasks
if [ -f "$SCRIPT_DIR/focuses/joju/tasks/check_setup.sh" ]; then
    echo ""
    echo -e "${BLUE}=== Checking Joju Task Management Setup ===${NC}"
    cd "$SCRIPT_DIR/focuses/joju/tasks"
    if ! ./check_setup.sh > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Joju task management not configured${NC}"
        echo "   Run: cd focuses/joju/tasks && ./check_setup.sh"
        echo "   See: focuses/joju/tasks/NOTION_SETUP_COMPLETE.md"
    else
        echo -e "${GREEN}✓${NC} Joju task management ready"
    fi
    cd "$SCRIPT_DIR"
fi
echo ""

echo -e "${BLUE}=== Starting All MCP Servers ===${NC}"
echo ""

# Array of MCP servers to start (Node.js servers)
declare -a MCPS=(
    "$HOME/mcp_servers/hcss-bridge/server.js:HCSS MCP:node"
    "$HOME/mcp_servers/figma-make-transformer/server.js:Joju/Team76 MCP:node"
    "$HOME/mcp_servers/8825-core/server.py:8825 Core MCP:python3"
)

started=0
failed=0

for mcp_info in "${MCPS[@]}"; do
    IFS=':' read -r server_path mcp_name command <<< "$mcp_info"
    
    if [ ! -f "$server_path" ]; then
        echo -e "${YELLOW}⚠ Skipping $mcp_name - server not found at $server_path${NC}"
        continue
    fi
    
    # Check if already running
    if pgrep -f "$server_path" > /dev/null; then
        echo -e "${YELLOW}⚠ $mcp_name already running${NC}"
        continue
    fi
    
    echo "Starting $mcp_name..."
    
    # Start in background
    nohup $command "$server_path" > /tmp/mcp-$(basename $(dirname "$server_path")).log 2>&1 &
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $mcp_name started${NC}"
        started=$((started + 1))
    else
        echo -e "${YELLOW}✗ Failed to start $mcp_name${NC}"
        failed=$((failed + 1))
    fi
    
    # Brief pause between starts
    sleep 1
done

echo ""
echo -e "${BLUE}=== Startup Complete ===${NC}"
echo ""
echo "Started: $started servers"
[ $failed -gt 0 ] && echo "Failed: $failed servers"
echo ""
echo "To check status:"
echo "  ps aux | grep mcp"
echo ""
echo "To stop all:"
echo "  pkill -f 'mcp.*server'"
