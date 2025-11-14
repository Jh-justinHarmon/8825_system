#!/bin/bash
# Manual cleanup script for Real Estate folder duplicates
# Based on analysis from enhanced_duplicate_check.py
# All files moved to backup, not deleted

set -e

ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/-- daisy --/Real Estate"
BACKUP="$ROOT/---DELETED-BACKUP---/$(date +%Y%m%d_%H%M%S)"

echo "Creating backup directory: $BACKUP"
mkdir -p "$BACKUP"

TOTAL_SAVED=0

# Function to move file to backup
move_to_backup() {
    local file="$1"
    local reason="$2"
    
    if [ -f "$file" ]; then
        local rel_path="${file#$ROOT/}"
        local backup_path="$BACKUP/$rel_path"
        local backup_dir=$(dirname "$backup_path")
        
        mkdir -p "$backup_dir"
        
        local size=$(stat -f%z "$file" 2>/dev/null || echo 0)
        TOTAL_SAVED=$((TOTAL_SAVED + size))
        
        echo "Moving: $rel_path ($reason)"
        mv "$file" "$backup_path"
    else
        echo "Skipping (not found): $file"
    fi
}

echo ""
echo "========================================================================"
echo "CLEANING UP EXACT DUPLICATES"
echo "========================================================================"
echo ""

# Top 10 exact duplicates from report

echo "1. Photo archive duplicate (111 MB)"
move_to_backup "$ROOT/__1.Clients/Jen on Scotia/Photos/7818-scotia-drive-dallas-tx-75248-High-Res.zip" "duplicate in Closing Binder"

echo ""
echo "2. Curbio SOW duplicate (101 MB)"
move_to_backup "$ROOT/Curbio/Curbio SOW - 309 Forest Grove.pptx" "duplicate in client folder"

echo ""
echo "3. Curbio presentation duplicate (97 MB)"
move_to_backup "$ROOT/Curbio/Curbio/Curbio Listing Presentation Slide Template.pptx" "duplicate in parent folder"

echo ""
echo "4. CMA duplicates (29 MB)"
move_to_backup "$ROOT/Wedegwood Homes/7637 El Pensador/Buy Comps Pictures_7342 Alto Caro.pdf" "duplicate CMA"
move_to_backup "$ROOT/Wedegwood Homes/7637 El Pensador/Buy Comps Pictures_7637 El Pensador.pdf" "duplicate CMA"

echo ""
echo "5. Marketing flyer duplicate (27 MB)"
move_to_backup "$ROOT/Wedegwood Homes/7837 El Pastel/Marketing/pdf-7837 El Pastel-with-bleed.pdf" "duplicate in Transaction Desk"

echo ""
echo "6. Just Sold graphics in trash (24 MB)"
move_to_backup "$ROOT/Soozie/JUST SOLD/Trash/2 properties sold - Prestonshire - Forest Cove (20230717)/2 properties sold - Prestonshire - Forest Cove-0.png" "in trash folder"

echo ""
echo "7. Texas guide duplicate (22 MB)"
move_to_backup "$ROOT/Tiffany/dpm_lawson_texas guide_Apr 23_FINAL.pdf" "duplicate in Marketing folder"

echo ""
echo "8. Headshot duplicate folder (18 MB)"
move_to_backup "$ROOT/7. Branding/- REF -/Headshots/laura-harmon-professional-headshots-spring-2022 2/harmon-spring-2022-14.jpg" "duplicate folder"

echo ""
echo "9. MLS listing duplicate (16 MB)"
move_to_backup "$ROOT/__1.Clients/Marshall, Megan & Mike/15627 Golden Creek/15627 Golden Creek/MLS Lisitng_15627 Golden Creek.pdf" "duplicate in SkySlope"

echo ""
echo "10. Mortgage doc duplicate (16 MB)"
move_to_backup "$ROOT/Mortage/Jackson Thomas/What to expect during pre-approval quoting homebuying process with the Thomas Mortgage Team v2022.pdf" "duplicate in parent folder"

echo ""
echo "========================================================================"
echo "CLEANUP COMPLETE"
echo "========================================================================"
echo ""

# Calculate total saved in MB
TOTAL_MB=$((TOTAL_SAVED / 1024 / 1024))
echo "Total space saved: ${TOTAL_MB} MB"
echo "Backup location: $BACKUP"
echo ""
echo "To rollback, run:"
echo "  mv \"$BACKUP\"/* \"$ROOT/\""
echo ""
