#!/bin/bash
# Unified Sync + Process Pipeline
# Syncs files from all sources, then processes through ingestion engine

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INTAKE_DOCS="$SCRIPT_DIR/users/jh/intake/documents"
PENDING_DIR="$HOME/Downloads/8825_inbox/pending"
INGESTION_ENGINE="$SCRIPT_DIR/../8825_core/inbox/ingestion_engine.py"

echo -e "${BLUE}=== Unified Sync + Process Pipeline ===${NC}"
echo ""

# Step 0: Sync Downloads folders (local ↔ iCloud)
echo -e "${YELLOW}Step 0: Syncing Downloads folders...${NC}"
./sync_downloads_folders.sh
echo ""

# Step 1: Sync brain transport to Downloads
echo -e "${YELLOW}Step 1: Syncing brain transport...${NC}"
./sync_brain.sh
echo ""

# Step 2: Sync from all sources
echo -e "${YELLOW}Step 2: Syncing from all sources...${NC}"
./sync_screenshots.sh
echo ""

# Step 3: Ensure pending directory exists
echo -e "${YELLOW}Step 3: Preparing ingestion folder...${NC}"
mkdir -p "$PENDING_DIR"
echo "✓ Pending folder ready: $PENDING_DIR"
echo ""

# Step 4: Copy new documents to pending
echo -e "${YELLOW}Step 4: Copying documents to ingestion pending...${NC}"
copied=0
if [ -d "$INTAKE_DOCS" ]; then
    for file in "$INTAKE_DOCS"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            dest="$PENDING_DIR/$filename"
            
            # Only copy if not already in pending
            if [ ! -f "$dest" ]; then
                cp "$file" "$dest"
                copied=$((copied + 1))
                echo -e "  ${GREEN}✓${NC} $filename"
            fi
        fi
    done
    
    if [ $copied -eq 0 ]; then
        echo "  No new documents to copy (already in pending)"
    else
        echo -e "  ${GREEN}Copied $copied documents${NC}"
    fi
else
    echo "  No documents folder found"
fi
echo ""

# Step 4: Run ingestion engine
echo -e "${YELLOW}Step 4: Processing through ingestion engine...${NC}"
if [ -f "$INGESTION_ENGINE" ]; then
    cd "$(dirname "$INGESTION_ENGINE")"
    python3 ingestion_engine.py process
else
    echo -e "${YELLOW}⚠ Ingestion engine not found at: $INGESTION_ENGINE${NC}"
    echo "  Files are in pending folder, ready for manual processing"
fi
echo ""

# Step 5: Cleanup processed files
echo -e "${YELLOW}Step 5: Cleaning up processed files...${NC}"
cd "$SCRIPT_DIR"

# Archive processed documents from intake
ARCHIVE_DIR="$SCRIPT_DIR/users/jh/processed"
mkdir -p "$ARCHIVE_DIR"

archived=0
if [ -d "$INTAKE_DOCS" ]; then
    for file in "$INTAKE_DOCS"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            
            # Move to processed archive
            mv "$file" "$ARCHIVE_DIR/"
            archived=$((archived + 1))
        fi
    done
    
    if [ $archived -eq 0 ]; then
        echo "  No documents to archive"
    else
        echo -e "  ${GREEN}✓ Archived $archived documents${NC}"
    fi
fi

# Clean up screenshots older than 30 days
INTAKE_SCREENSHOTS="$SCRIPT_DIR/users/jh/intake/screenshots"
if [ -d "$INTAKE_SCREENSHOTS" ]; then
    old_screenshots=$(find "$INTAKE_SCREENSHOTS" -type f -mtime +30 | wc -l | tr -d ' ')
    if [ $old_screenshots -gt 0 ]; then
        find "$INTAKE_SCREENSHOTS" -type f -mtime +30 -delete
        echo -e "  ${GREEN}✓ Deleted $old_screenshots old screenshots (>30 days)${NC}"
    else
        echo "  No old screenshots to delete"
    fi
fi

# Clean up Downloads folder
echo ""
echo -e "${YELLOW}Step 6: Cleaning up Downloads folder...${NC}"
cd "$SCRIPT_DIR"
./cleanup_downloads.sh

echo ""

echo -e "${BLUE}=== Pipeline Complete ===${NC}"
echo ""
echo "Summary:"
echo "  Synced: Downloads folders + 4 sources"
echo "  Copied: $copied documents to pending"
echo "  Processed: Check ingestion engine output above"
echo "  Archived: $archived documents"
echo "  Downloads: Cleaned (see cleanup output above)"
echo ""
echo "Locations:"
echo "  Processed archive: $ARCHIVE_DIR"
echo "  Screenshots: $INTAKE_SCREENSHOTS (old ones auto-deleted)"
echo "  Downloads archive: $HOME/Downloads/8825_processed"
echo ""
echo "Next steps:"
echo "  - Review teaching tickets: cd 8825_core/inbox && python3 ingestion_engine.py tickets list"
echo "  - Check stats: python3 ingestion_engine.py stats"
