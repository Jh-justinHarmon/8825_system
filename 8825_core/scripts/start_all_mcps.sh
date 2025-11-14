#!/bin/bash
# 8825 v3.0 - Start All MCP Servers

echo "========================================"
echo "8825 v3.0 - Starting All MCP Servers"
echo "========================================"
echo ""

# Get base directory
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd ../.. && pwd )"

# Start HCSS MCP
echo "Starting HCSS MCP (port 8826)..."
cd "$BASE_DIR/~/mcp_servers/hcss-bridge" && ./start_mcp.sh &
HCSS_PID=$!
echo "  ✅ HCSS MCP started (PID: $HCSS_PID)"

# Start Team 76 MCP
echo "Starting Team 76 MCP (port 8827)..."
cd "$BASE_DIR/~/mcp_servers/figma-make-transformer" && ./start_mcp.sh &
TEAM76_PID=$!
echo "  ✅ Team 76 MCP started (PID: $TEAM76_PID)"

# Start Personal MCP
echo "Starting Personal MCP (port 8828)..."
cd "$BASE_DIR/focuses/jh_assistant/mcp_server" && ./start_mcp.sh &
JH_PID=$!
echo "  ✅ Personal MCP started (PID: $JH_PID)"

echo ""
echo "========================================"
echo "All MCPs Started!"
echo "========================================"
echo ""
echo "Access URLs:"
echo "  HCSS MCP:    http://localhost:8826"
echo "  Team 76 MCP: http://localhost:8827"
echo "  Personal MCP: http://localhost:8828"
echo ""
echo "Health Checks:"
echo "  curl http://localhost:8826/health"
echo "  curl http://localhost:8827/health"
echo "  curl http://localhost:8828/health"
echo ""
echo "Process IDs:"
echo "  HCSS: $HCSS_PID"
echo "  Team 76: $TEAM76_PID"
echo "  Personal: $JH_PID"
echo ""
