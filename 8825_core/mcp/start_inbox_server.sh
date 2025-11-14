#!/bin/bash

# 8825 Inbox MCP Server Startup Script

# Generate API key if not set
if [ -z "$INBOX_API_KEY" ]; then
    export INBOX_API_KEY="8825-inbox-$(uuidgen)"
    echo "Generated new API key: $INBOX_API_KEY"
    echo ""
    echo "⚠️  SAVE THIS KEY! Add to ChatGPT custom GPT action."
    echo ""
fi

# Change to script directory
cd "$(dirname "$0")"

# Start server
python3 inbox_server.py
