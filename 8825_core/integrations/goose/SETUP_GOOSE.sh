#!/bin/bash
# Setup Goose MCP Bridge for 8825
# Run this script to configure Goose

set -e

echo "=================================================="
echo "8825 Goose MCP Bridge - Setup"
echo "=================================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "Workspace: $WORKSPACE_ROOT"
echo ""

# Check if Goose is installed
if ! command -v goose &> /dev/null; then
    echo "❌ Goose not installed"
    echo ""
    echo "Install Goose:"
    echo "  pip install goose-ai"
    echo ""
    exit 1
fi

echo "✅ Goose installed"
echo ""

# Create Goose config directory
GOOSE_CONFIG_DIR="$HOME/.config/goose"
mkdir -p "$GOOSE_CONFIG_DIR"

echo "✅ Config directory: $GOOSE_CONFIG_DIR"
echo ""

# Create config file
CONFIG_FILE="$GOOSE_CONFIG_DIR/config.yaml"

cat > "$CONFIG_FILE" << EOF
# Goose Configuration for 8825 MCP Bridge
# Generated: $(date)

mcpServers:
  8825-bridge:
    command: python3
    args:
      - $WORKSPACE_ROOT/8825_core/integrations/goose/mcp-bridge/server.py
    env:
      LOG_LEVEL: INFO
      PYTHONUNBUFFERED: "1"

settings:
  model: gpt-4
  temperature: 0.7
  max_tokens: 4000
EOF

echo "✅ Config created: $CONFIG_FILE"
echo ""

# Make server executable
chmod +x "$WORKSPACE_ROOT/8825_core/integrations/goose/mcp-bridge/server.py"

echo "✅ Server executable"
echo ""

# Test the server
echo "Testing MCP server..."
echo '{"method":"tools/list","params":{}}' | python3 "$WORKSPACE_ROOT/8825_core/integrations/goose/mcp-bridge/server.py" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Server test passed"
else
    echo "⚠️  Server test failed (may need Notion config)"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Configure Notion (if using tasks):"
echo "   cd $WORKSPACE_ROOT/focuses/joju/tasks"
echo "   cp config.example.json config.json"
echo "   # Edit config.json with Notion credentials"
echo ""
echo "2. Start Goose:"
echo "   cd $WORKSPACE_ROOT"
echo "   goose session start"
echo ""
echo "3. Test tools:"
echo "   > \"List available tools\""
echo "   > \"Check 8825 status\""
echo ""
