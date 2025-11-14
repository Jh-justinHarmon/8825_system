#!/bin/bash
# HCSS Calendar Sync - One-command workflow
# Syncs screenshots from Dropbox → OCR → Google Calendar

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INBOX_HUB="$(dirname "$PROJECT_ROOT")/INBOX_HUB"
GOOGLE_INTEGRATION="$PROJECT_ROOT/integrations/google"

echo -e "${BLUE}=== HCSS Calendar Sync ===${NC}"
echo ""

# Step 1: Sync screenshots from Dropbox
echo -e "${YELLOW}Step 1: Syncing screenshots from Dropbox...${NC}"
cd "$INBOX_HUB"
./sync_screenshots.sh

echo ""

# Step 2: Run OCR calendar sync
echo -e "${YELLOW}Step 2: Running OCR calendar sync...${NC}"
cd "$GOOGLE_INTEGRATION"
python3 calendar_screenshot_sync.py

echo ""
echo -e "${GREEN}✓ HCSS Calendar sync complete!${NC}"
echo ""
echo "Next: Verify events in harmon.justin@gmail.com calendar"
