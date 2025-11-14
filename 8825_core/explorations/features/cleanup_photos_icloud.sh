#!/bin/bash
# Cleanup script for iCloud Photos folder
# Removes exact duplicates and archives old versions
# All files moved to backup, not deleted

set -e

ROOT="/Users/justinharmon/Library/Mobile Documents/com~apple~CloudDocs/Documents/- PHOTOS -"
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
echo "PHASE 1: EXACT DUPLICATES"
echo "========================================================================"
echo ""

echo "1. Kitchen PSD duplicate (261 MB)"
move_to_backup "$ROOT/Family Photos - 2024/Kitchen_pics/- FINAL -/6 - Karsen, Bob, Kathy - cropped copy.psd" "duplicate PSD"

echo ""
echo "2. Family photo shoot duplicates (280 MB)"
move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A9085.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A9085.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A8881.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A8881.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A8974.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A8974.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A8939.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A8939.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A9022.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A9022.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A8951.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A8951.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A8915.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A8915.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A8919.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A8919.jpg" "duplicate in Family Photos - 2024"

move_to_backup "$ROOT/24 harmon fam photos/share with rents/4J5A9040.jpg" "duplicate in Family Photos - 2024"
move_to_backup "$ROOT/24 harmon fam photos/Harmon Family at Prairie Creek Park 2024/4J5A9040.jpg" "duplicate in Family Photos - 2024"

echo ""
echo "========================================================================"
echo "PHASE 2: OLD VIDEO VERSIONS (OPTIONAL - Review before running)"
echo "========================================================================"
echo ""
echo "Uncomment these lines to archive old video versions (1.3 GB):"
echo ""
echo "# move_to_backup \"$ROOT/VTS_01_1.mov\" \"old version (keep VTS_01_2.mov)\""
echo "# move_to_backup \"$ROOT/VTS_01_2.VOB\" \"old version (keep VTS_01_1.VOB)\""
echo ""

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
echo "  rsync -av \"$BACKUP/\" \"$ROOT/\""
echo ""
echo "To also clean up old video versions, edit this script and uncomment Phase 2"
echo ""
