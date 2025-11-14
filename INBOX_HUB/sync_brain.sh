#!/bin/bash
# Sync Brain Transport Protocol
# Ensures latest brain transport is always in Downloads for easy LLM access

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SOURCE="$HOME/Documents/8825_BRAIN_TRANSPORT.json"
DEST="$HOME/Downloads/8825_BRAIN_TRANSPORT.json"

echo -e "${BLUE}=== Syncing Brain Transport ===${NC}"
echo ""

if [ ! -f "$SOURCE" ]; then
    echo "❌ Source brain transport not found: $SOURCE"
    exit 1
fi

# Copy to Downloads
cp "$SOURCE" "$DEST"

echo -e "${GREEN}✓ Brain transport synced${NC}"
echo ""
echo "Location: $DEST"
echo "Size: $(ls -lh "$DEST" | awk '{print $5}')"
echo ""
echo "Usage:"
echo "  - Upload to ChatGPT for context"
echo "  - Reference in new Cascade sessions"
echo "  - Share with other LLMs"
echo ""
echo "This file contains:"
echo "  - System architecture (v3.0)"
echo "  - Three-mode interaction (Teaching/Brainstorm/Dev)"
echo "  - Inbox protocol"
echo "  - Multi-MCP setup"
echo "  - Critical rules & workflows"
