#!/bin/bash
# Sync Downloads Folders - FIXED VERSION
# CRITICAL: Only syncs essential items, prevents junk re-pollution
# Auto-cleans before syncing

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/../8825_core/config/file_router.sh"

LOCAL_DOWNLOADS="$HOME/Downloads"
ICLOUD_DOWNLOADS="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Downloads"

echo -e "${BLUE}=== Smart Downloads Sync ===${NC}"
echo ""

# STEP 1: Auto-cleanup junk from BOTH locations BEFORE syncing
cleanup_junk() {
    local location="$1"
    local name="$2"
    
    echo -e "${YELLOW}Cleaning $name...${NC}"
    
    # Remove old folders
    rm -rf "$location/old" "$location/- old -" 2>/dev/null
    
    # Remove temp/debug files
    find "$location" -maxdepth 1 -type f \( \
        -name "sticky_*" \
        -o -name "*brainstorm*.txt" \
        -o -name "client_secret*.json" \
        -o -name "mythic*.json" \
        -o -name "phils_book*.txf" \
        -o -name "IMG_*.HEIC" \
        -o -name "IMG_*.jpeg" \
    \) -delete 2>/dev/null
    
    echo -e "${GREEN}✓ $name cleaned${NC}"
}

# Clean both locations first
cleanup_junk "$LOCAL_DOWNLOADS" "Local Downloads"
[ -d "$ICLOUD_DOWNLOADS" ] && cleanup_junk "$ICLOUD_DOWNLOADS" "iCloud Downloads"

echo ""

# STEP 2: Sync BRAIN_TRANSPORT to both
echo -e "${YELLOW}Syncing BRAIN_TRANSPORT...${NC}"
BRAIN_SOURCE="$HOME/Documents/8825_BRAIN_TRANSPORT.json"
if [ -f "$BRAIN_SOURCE" ]; then
    cp "$BRAIN_SOURCE" "$LOCAL_DOWNLOADS/0-8825_BRAIN_TRANSPORT.json"
    [ -d "$ICLOUD_DOWNLOADS" ] && cp "$BRAIN_SOURCE" "$ICLOUD_DOWNLOADS/0-8825_BRAIN_TRANSPORT.json"
    echo -e "${GREEN}✓ BRAIN_TRANSPORT synced to both locations${NC}"
fi

echo ""

# STEP 3: Sync ONLY 8825_inbox bidirectionally
echo -e "${YELLOW}Syncing 8825_inbox...${NC}"

local_inbox="$LOCAL_DOWNLOADS/8825_inbox"
icloud_inbox="$ICLOUD_DOWNLOADS/8825_inbox"

# Ensure inbox exists in both locations
mkdir -p "$local_inbox"/{pending,processing,completed,errors}
[ -d "$ICLOUD_DOWNLOADS" ] && mkdir -p "$icloud_inbox"/{pending,processing,completed,errors}

# Bidirectional sync ONLY for inbox
if [ -d "$ICLOUD_DOWNLOADS" ]; then
    rsync -au "$local_inbox/" "$icloud_inbox/"
    rsync -au "$icloud_inbox/" "$local_inbox/"
    echo -e "${GREEN}✓ 8825_inbox synced bidirectionally${NC}"
fi

echo ""

# STEP 4: Sync 8825_processed one-way (local → iCloud only)
echo -e "${YELLOW}Syncing 8825_processed (one-way)...${NC}"
if [ -d "$ICLOUD_DOWNLOADS" ]; then
    rsync -au "$LOCAL_DOWNLOADS/8825_processed/" "$ICLOUD_DOWNLOADS/8825_processed/"
    echo -e "${GREEN}✓ 8825_processed synced (local → iCloud)${NC}"
fi

echo ""
echo -e "${BLUE}=== Sync Complete ===${NC}"
echo ""
echo "✅ Both Downloads folders clean and synced"
echo "✅ BRAIN_TRANSPORT available in both locations"
echo "✅ 8825_inbox synced bidirectionally"
echo "✅ Junk auto-removed before sync"
echo ""
echo "Locations:"
echo "  Local:   $LOCAL_DOWNLOADS"
[ -d "$ICLOUD_DOWNLOADS" ] && echo "  iCloud:  $ICLOUD_DOWNLOADS"
