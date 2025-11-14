#!/bin/bash
# POC Promotion Helper - Automates POC promotion workflow

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

# Usage
usage() {
    echo "POC Promotion Helper"
    echo ""
    echo "Usage: $0 <source> <destination>"
    echo ""
    echo "Examples:"
    echo "  $0 sandbox/graduated/my-poc shared/automations"
    echo "  $0 sandbox/experimental/feature focuses/hcss/workflows"
    echo ""
    echo "Destinations:"
    echo "  shared/automations  - Cross-focus automations"
    echo "  shared/templates    - Reusable templates"
    echo "  shared/libraries    - Shared code libraries"
    echo "  focuses/{name}/     - Focus-specific code"
    echo "  core/pipelines      - Universal pipelines"
    echo "  core/integrations   - Universal integrations"
    exit 1
}

if [ $# -ne 2 ]; then
    usage
fi

SOURCE="$1"
DEST="$2"

# Validate source
if [ ! -d "$SYSTEM_ROOT/$SOURCE" ]; then
    echo -e "${RED}Error: Source does not exist: $SOURCE${NC}"
    exit 1
fi

# Get POC name
POC_NAME=$(basename "$SOURCE")

# Build full destination path
DEST_PATH="$SYSTEM_ROOT/$DEST/$POC_NAME"

echo -e "${BLUE}=== POC Promotion ===${NC}"
echo "Source: $SOURCE"
echo "Destination: $DEST/$POC_NAME"
echo ""

# Check if destination already exists
if [ -d "$DEST_PATH" ]; then
    echo -e "${RED}Error: Destination already exists: $DEST/$POC_NAME${NC}"
    exit 1
fi

# Confirm promotion
echo -e "${YELLOW}This will:${NC}"
echo "  1. Move $POC_NAME to $DEST/"
echo "  2. Create promotion metadata"
echo "  3. Update references (if any)"
echo ""
echo -e "${YELLOW}Proceed? [y/N]${NC}"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# Move POC
echo -e "${BLUE}[1/3] Moving POC...${NC}"
mv "$SYSTEM_ROOT/$SOURCE" "$DEST_PATH"
echo -e "  ${GREEN}✅${NC} Moved to $DEST/$POC_NAME"

# Create promotion metadata
echo -e "${BLUE}[2/3] Creating promotion metadata...${NC}"
cat > "$DEST_PATH/.PROMOTION" << EOF
Promoted to: $DEST/$POC_NAME
Promoted from: $SOURCE
Promotion date: $(date +%Y-%m-%d)
Promoted by: POC Promotion Helper

History:
- Built in: $(cat "$DEST_PATH/.ORIGIN" 2>/dev/null | grep "Migrated from" || echo "Unknown")
- Migrated to sandbox: $(cat "$DEST_PATH/.ORIGIN" 2>/dev/null | grep "Migration date" || echo "Unknown")
- Promoted to production: $(date +%Y-%m-%d)
EOF
echo -e "  ${GREEN}✅${NC} Promotion metadata created"

# Update references (simple grep and report)
echo -e "${BLUE}[3/3] Checking for references...${NC}"
REF_COUNT=$(grep -r "$SOURCE" \
    --include="*.py" --include="*.sh" --include="*.md" \
    "$SYSTEM_ROOT/focuses" "$SYSTEM_ROOT/shared" "$SYSTEM_ROOT/8825_core" \
    2>/dev/null | wc -l || echo "0")

if [ "$REF_COUNT" -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️${NC}  Found $REF_COUNT references to old path"
    echo "  You may want to update these manually or run:"
    echo "    find . -type f -exec sed -i '' 's|$SOURCE|$DEST/$POC_NAME|g' {} \\;"
else
    echo -e "  ${GREEN}✅${NC} No references found"
fi

echo ""
echo -e "${GREEN}=== Promotion Complete ===${NC}"
echo ""
echo "POC Location: $DEST/$POC_NAME"
echo "Promotion Record: $DEST/$POC_NAME/.PROMOTION"
echo ""
echo "Next steps:"
echo "  1. Update any references to old path (if any)"
echo "  2. Update documentation"
echo "  3. Test that promoted code works"
echo "  4. Commit changes to git"
echo ""
