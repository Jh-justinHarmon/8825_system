#!/bin/bash
# Unified sync for Input Hub - handles all file types
# Phase 1: Manual sync with intelligent routing

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INTAKE_SCREENSHOTS="$SCRIPT_DIR/users/jh/intake/screenshots"
INTAKE_DOCUMENTS="$SCRIPT_DIR/users/jh/intake/documents"
INTAKE_UPLOADS="$SCRIPT_DIR/users/jh/intake/uploads"

# Source directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/../8825_core/config/file_router.sh"

DESKTOP="$HOME/Desktop"
DOWNLOADS="$HOME/Downloads"
DROPBOX_SCREENSHOTS="$HOME/Hammer Consulting Dropbox/Justin Harmon/Screenshots"
INGESTION_DIR="$(get_router_intake)"

# Ensure intake directories exist
mkdir -p "$INTAKE_SCREENSHOTS"
mkdir -p "$INTAKE_DOCUMENTS"
mkdir -p "$INTAKE_UPLOADS"

echo -e "${BLUE}=== Input Hub Unified Sync ===${NC}"
echo ""

# Function to determine destination based on file type
get_destination() {
    local file="$1"
    local ext="${file##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    
    case "$ext" in
        png|jpg|jpeg|gif|bmp|webp|svg)
            echo "$INTAKE_SCREENSHOTS"
            ;;
        json|md|txt|docx|pdf|doc|rtf)
            echo "$INTAKE_DOCUMENTS"
            ;;
        *)
            echo "$INTAKE_UPLOADS"
            ;;
    esac
}

# Function to sync files from a directory with intelligent routing
sync_from_dir() {
    local source_dir="$1"
    local dir_name="$2"
    local screenshots=0
    local documents=0
    local uploads=0
    
    if [ ! -d "$source_dir" ]; then
        return
    fi
    
    echo -e "${YELLOW}Checking $dir_name...${NC}"
    
    # Find all relevant files modified in last 7 days
    while IFS= read -r -d '' file; do
        filename=$(basename "$file")
        dest_dir=$(get_destination "$file")
        dest="$dest_dir/$filename"
        
        # Skip if already exists
        if [ -f "$dest" ]; then
            continue
        fi
        
        # Copy with metadata preserved
        cp -p "$file" "$dest"
        
        # Count by type
        if [ "$dest_dir" = "$INTAKE_SCREENSHOTS" ]; then
            screenshots=$((screenshots + 1))
            echo -e "  ${GREEN}✓${NC} [IMG] $filename"
        elif [ "$dest_dir" = "$INTAKE_DOCUMENTS" ]; then
            documents=$((documents + 1))
            echo -e "  ${GREEN}✓${NC} [DOC] $filename"
        else
            uploads=$((uploads + 1))
            echo -e "  ${GREEN}✓${NC} [FILE] $filename"
        fi
        
    done < <(find "$source_dir" -maxdepth 1 -type f \
        \( -name "Screenshot*.png" -o \
           -name "Screen Shot*.png" -o \
           -name "CleanShot*.png" -o \
           -name "*.json" -o \
           -name "*.md" -o \
           -name "*.txt" -o \
           -name "*.docx" -o \
           -name "*.pdf" -o \
           -name "*.jpg" -o \
           -name "*.jpeg" -o \
           -name "*.png" \) \
        -mtime -7 \
        -print0 2>/dev/null)
    
    local total=$((screenshots + documents + uploads))
    if [ $total -eq 0 ]; then
        echo "  No new files"
    else
        echo -e "  ${GREEN}Synced: $screenshots images, $documents docs, $uploads other${NC}"
    fi
    echo ""
}

# Sync from Desktop
sync_from_dir "$DESKTOP" "Desktop"

# Sync from Downloads
sync_from_dir "$DOWNLOADS" "Downloads"

# Sync from Dropbox Screenshots
sync_from_dir "$DROPBOX_SCREENSHOTS" "Dropbox Screenshots"

# Sync from 8825 Ingestion
sync_from_dir "$INGESTION_DIR" "8825 Ingestion"

# Summary
screenshots=$(find "$INTAKE_SCREENSHOTS" -type f | wc -l | tr -d ' ')
documents=$(find "$INTAKE_DOCUMENTS" -type f | wc -l | tr -d ' ')
uploads=$(find "$INTAKE_UPLOADS" -type f | wc -l | tr -d ' ')
total=$((screenshots + documents + uploads))

echo -e "${BLUE}=== Summary ===${NC}"
echo "Screenshots: $screenshots"
echo "Documents:   $documents"
echo "Other:       $uploads"
echo "Total:       $total"
echo ""
echo "Locations:"
echo "  Screenshots: $INTAKE_SCREENSHOTS"
echo "  Documents:   $INTAKE_DOCUMENTS"
echo "  Uploads:     $INTAKE_UPLOADS"
echo ""
echo -e "${GREEN}✓ Sync complete${NC}"
echo ""
echo "Use './checking_sg.sh' to view latest screenshot"
