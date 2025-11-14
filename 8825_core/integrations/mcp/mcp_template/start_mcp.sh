#!/bin/bash
# 8825 v3.0 MCP Startup Script

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment variables
if [ -f "$DIR/.env" ]; then
    export $(cat "$DIR/.env" | grep -v '^#' | xargs)
fi

# Start MCP server
echo "Starting 8825 MCP Server..."
python3 "$DIR/server.py"
