#!/bin/bash
# Clean up Downloads folder - move 8825 files to archive

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

DOWNLOADS="$HOME/Downloads"
ARCHIVE="$DOWNLOADS/8825_processed"

mkdir -p "$ARCHIVE"

echo -e "${BLUE}=== Cleaning Downloads Folder ===${NC}"
echo ""

cleaned=0

cd "$DOWNLOADS"

# List of patterns to archive
patterns=(
    "8825*.json"
    "8825*.docx"
    "8825*.md"
    "TOKENIZED*.docx"
    "SYNC*.docx"
    "justinharmon*.json"
    "Profile*.pdf"
    "20251108_*.json"
)

for pattern in "${patterns[@]}"; do
    shopt -s nullglob
    for file in $pattern; do
        if [ -f "$file" ]; then
            mv "$file" "$ARCHIVE/"
            echo -e "  ${GREEN}✓${NC} $file"
            cleaned=$((cleaned + 1))
        fi
    done
    shopt -u nullglob
done

echo ""
if [ $cleaned -eq 0 ]; then
    echo "No files to clean"
else
    echo -e "${GREEN}✓ Moved $cleaned files to Downloads/8825_processed/${NC}"
fi
echo ""
echo "Downloads folder cleaned!"
