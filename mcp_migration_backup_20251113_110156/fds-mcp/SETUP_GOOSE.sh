#!/bin/bash
# Setup File Dispatch System MCP for Goose

echo "============================================================"
echo "File Dispatch System (FDS) - Goose Setup"
echo "============================================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOOSE_CONFIG="$SCRIPT_DIR/goose_config.yaml"
GOOSE_PROFILES="$HOME/.config/goose/profiles.yaml"

# Check if Goose is installed
if ! command -v goose &> /dev/null; then
    echo "❌ Goose not installed"
    echo "Install from: https://github.com/block/goose"
    exit 1
fi

echo "✓ Goose installed"
echo ""

# Check if profiles.yaml exists
if [ ! -f "$GOOSE_PROFILES" ]; then
    echo "Creating Goose profiles directory..."
    mkdir -p "$(dirname "$GOOSE_PROFILES")"
    echo "mcpServers: {}" > "$GOOSE_PROFILES"
fi

echo "Goose profiles: $GOOSE_PROFILES"
echo ""

# Show configuration to add
echo "============================================================"
echo "Add this to your Goose profiles.yaml:"
echo "============================================================"
cat "$GOOSE_CONFIG"
echo ""
echo "============================================================"
echo ""

# Offer to add automatically
read -p "Add to profiles.yaml automatically? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup existing
    cp "$GOOSE_PROFILES" "$GOOSE_PROFILES.backup"
    echo "✓ Backed up existing profiles"
    
    # Check if FDS already configured
    if grep -q "file-dispatch-system" "$GOOSE_PROFILES"; then
        echo "⚠️  FDS already configured in profiles.yaml"
        echo "Remove existing configuration first"
        exit 1
    fi
    
    # Append configuration
    echo "" >> "$GOOSE_PROFILES"
    cat "$GOOSE_CONFIG" >> "$GOOSE_PROFILES"
    
    echo "✓ Added FDS to Goose profiles"
else
    echo "Manual setup required"
    echo "Copy the configuration above to: $GOOSE_PROFILES"
fi

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "Test with Goose:"
echo "  goose session start"
echo "  > What's the status of the file dispatch system?"
echo "  > Start the file dispatch system"
echo "  > Show me recent FDS logs"
echo ""
echo "Available commands:"
echo "  - Get FDS status"
echo "  - Start/stop FDS"
echo "  - Process specific file"
echo "  - View logs and queue"
echo "  - Clear queue"
echo ""
