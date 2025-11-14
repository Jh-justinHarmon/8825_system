#!/bin/bash
# Export Document Command - AI session export to project folders
# Version: 2.0.0 - File Router Integration
# Created: 2025-11-13

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

# Source file router
source "$SYSTEM_ROOT/8825_core/config/file_router.sh"

# Usage
usage() {
    echo "Export Document Command"
    echo ""
    echo "Usage: $0 <project> <title>"
    echo ""
    echo "Projects:"
    get_router_projects | while read proj; do
        echo "  $proj"
    done
    echo ""
    echo "Examples:"
    echo "  $0 8825 \"architecture refactor session\""
    echo "  $0 HCSS \"client planning discussion\""
    echo ""
    echo "Note: AI exports use lowercase naming to distinguish from ingestion files (ALL_CAPS)"
    exit 1
}


# Parse arguments
if [ $# -ne 2 ]; then
    usage
fi

PROJECT="$1"
TITLE="$2"

# Get destination from file router
DEST_DIR=$(get_router_destination "$PROJECT")

# Generate filename (lowercase per convention)
DATE=$(date +%Y-%m-%d)
FILENAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | sed 's/[^a-z0-9_-]//g')
DEST_FILE="$DEST_DIR/${DATE}_${FILENAME}.md"

# Create directory if needed
mkdir -p "$DEST_DIR"

# Check if file exists
if [ -f "$DEST_FILE" ]; then
    echo -e "${YELLOW}⚠️  File already exists: $DEST_FILE${NC}"
    echo -e "${YELLOW}Overwrite? [y/N]${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi
fi

# Create file with header
cat > "$DEST_FILE" << EOF
# $TITLE

**Date:** $(date +%Y-%m-%d)  
**Project:** $PROJECT  
**Type:** AI Export

---

[Content goes here]

EOF

echo -e "${GREEN}✅ AI export created${NC}"
echo ""
echo "Location: $DEST_FILE"
echo "Project: $PROJECT"
echo "Convention: lowercase (AI export)"
echo ""

# Store last export for make-shareable
echo "$DEST_FILE" > "$SYSTEM_ROOT/.last_export"
