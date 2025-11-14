#!/bin/bash
# Stop All MCP Servers

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Stopping All MCP Servers ===${NC}"
echo ""

stopped=0

# Stop specific MCP servers
for server in "hcss-bridge/server.js" "figma-make-transformer/server.js" "8825-core/server.py"; do
    if pgrep -f "$server" > /dev/null; then
        pkill -f "$server"
        echo -e "${GREEN}✓ Stopped $(basename $(dirname $server))${NC}"
        stopped=$((stopped + 1))
    fi
done

if [ $stopped -eq 0 ]; then
    echo "No MCP servers were running"
else
    echo ""
    echo "Stopped $stopped server(s)"
fi

echo ""
echo "Verify with:"
echo "  ps aux | grep mcp"
