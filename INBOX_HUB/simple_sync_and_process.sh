#!/bin/bash
# Simplified Inbox Pipeline
# One-way sync: iCloud Downloads → Local Downloads
# Process directly from Downloads
# Clean immediately after processing

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source file router
source "$SCRIPT_DIR/../8825_core/config/file_router.sh"

LOCAL_DOWNLOADS="$HOME/Downloads"
ICLOUD_DOWNLOADS="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Downloads"
PROCESSED_ARCHIVE="$LOCAL_DOWNLOADS/8825_processed"
INTAKE_DOCS="$SCRIPT_DIR/users/jh/intake/documents"
BRAIN_SOURCE="$HOME/Documents/8825_BRAIN_TRANSPORT.json"
BRAIN_DEST="$INTAKE_DOCS/0-8825_BRAIN_TRANSPORT.json"
PENDING_DIR="$HOME/Downloads/8825_inbox/pending"
# New modular ingestion engine (v2)
INGESTION_ENGINE="$SCRIPT_DIR/../8825_core/workflows/ingestion/scripts/ingestion_engine.py"

# Check dependencies first
"$SCRIPT_DIR/../check_dependencies.sh" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing missing dependencies...${NC}"
    "$SCRIPT_DIR/../check_dependencies.sh"
    echo ""
fi

echo -e "${BLUE}=== Simplified Inbox Pipeline ===${NC}"
echo ""

# Step 1: NO SYNC - Universal Inbox Watch handles both folders independently
# UPDATED 2025-11-12: Disabled sync to prevent duplicates
# Both Desktop and iCloud Downloads are monitored independently by Universal Inbox Watch
echo -e "${YELLOW}Step 1: Monitoring both Downloads folders independently...${NC}"
echo -e "${GREEN}✓ Desktop Downloads: Monitored by Universal Inbox Watch${NC}"
echo -e "${GREEN}✓ iCloud Downloads: Monitored by Universal Inbox Watch${NC}"
echo -e "${GREEN}✓ No sync = No duplicates${NC}"
echo ""

# Step 2: Ensure brain transport is at top with 0- prefix
echo -e "${YELLOW}Step 2: Updating brain transport...${NC}"
if [ -f "$BRAIN_SOURCE" ]; then
    cp "$BRAIN_SOURCE" "$BRAIN_DEST"
    echo -e "${GREEN}✓ Brain transport updated: 0-8825_BRAIN_TRANSPORT.json${NC}"
else
    echo "⚠ Brain source not found (will use existing if present)"
fi
echo ""

# Step 3: Process files from Downloads
echo -e "${YELLOW}Step 3: Processing files from Downloads...${NC}"

# Use the actual ingestion engine pending folder
ACTUAL_PENDING="$HOME/Downloads/8825_inbox/pending"
mkdir -p "$ACTUAL_PENDING"

# Move processable files to ingestion pending (exclude brain and processed folder)
processed_count=0
cd "$LOCAL_DOWNLOADS"

for ext in json txt md docx pdf; do
    shopt -s nullglob
    for file in *.$ext; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            
            # Skip brain transport and system files
            if [[ "$filename" == "0-8825_BRAIN_TRANSPORT.json" ]] || \
               [[ "$filename" == *.meta.json ]] || \
               [[ "$filename" == T-8825-* ]]; then
                continue
            fi
            
            # Move to ingestion pending
            mv "$file" "$ACTUAL_PENDING/"
            processed_count=$((processed_count + 1))
        fi
    done
    shopt -u nullglob
done

if [ $processed_count -gt 0 ]; then
    echo "Found $processed_count files to process"
    
    # Run new modular ingestion engine (v2)
    python3 "$INGESTION_ENGINE" process
    
    echo ""
    echo -e "${GREEN}✓ Processing complete${NC}"
else
    echo "No files to process"
fi
echo ""

# Step 4: Archive processed files from ingestion completed folder
echo -e "${YELLOW}Step 4: Archiving processed files...${NC}"
mkdir -p "$PROCESSED_ARCHIVE"

COMPLETED_FOLDER="$HOME/Downloads/8825_inbox/completed"
archived=0

if [ -d "$COMPLETED_FOLDER" ]; then
    for file in "$COMPLETED_FOLDER"/*; do
        if [ -f "$file" ]; then
            mv "$file" "$PROCESSED_ARCHIVE/"
            archived=$((archived + 1))
        fi
    done
fi

if [ $archived -gt 0 ]; then
    echo -e "${GREEN}✓ Archived $archived files to Downloads/8825_processed/${NC}"
else
    echo "No files to archive"
fi
echo ""

# Step 5: Final cleanup - remove any stragglers
echo -e "${YELLOW}Step 5: Final cleanup...${NC}"
cd "$LOCAL_DOWNLOADS"

cleanup_count=0
for pattern in "8825_INBOX_*" "TOKENIZED_*" "SYNC_*" "justinharmon*.json" "Profile*.pdf"; do
    shopt -s nullglob
    for file in $pattern; do
        if [ -f "$file" ]; then
            mv "$file" "$PROCESSED_ARCHIVE/"
            cleanup_count=$((cleanup_count + 1))
        fi
    done
    shopt -u nullglob
done

if [ $cleanup_count -gt 0 ]; then
    echo -e "${GREEN}✓ Cleaned up $cleanup_count additional files${NC}"
else
    echo "Downloads folder is clean"
fi
echo ""

# Step 6: Sync Local → iCloud (DISABLED - keeps iCloud clean)
# echo -e "${YELLOW}Step 6: Syncing cleanup back to iCloud...${NC}"
# if [ -d "$ICLOUD_DOWNLOADS" ]; then
#     # Mirror local to iCloud (including deletions via --delete)
#     rsync -au --delete --exclude="8825_processed" --exclude=".DS_Store" "$LOCAL_DOWNLOADS/" "$ICLOUD_DOWNLOADS/"
#     echo -e "${GREEN}✓ iCloud Downloads now matches Local Downloads${NC}"
# else
#     echo "No iCloud Downloads folder (OK if not using mobile)"
# fi
echo -e "${GREEN}✓ iCloud Downloads stays clean (no sync back)${NC}"
echo ""

echo -e "${BLUE}=== Pipeline Complete ===${NC}"
echo ""
echo "iCloud Downloads: Clean (only unprocessed files)"
echo "Local Downloads: Clean + archives in 8825_processed/"
echo ""
echo "Local:  $LOCAL_DOWNLOADS"
echo "iCloud: $ICLOUD_DOWNLOADS"
echo ""
echo "Processed files archived to: $PROCESSED_ARCHIVE"
echo ""
echo "✓ iCloud stays clean, local has full history"
echo ""
echo "Mobile flow: Upload to iCloud → Auto-syncs & processes locally"
echo "Desktop flow: Drop in Downloads → Instant processing"
