#!/bin/bash
# Quick reference to latest screenshots
# Usage: ./checking_sg.sh [count]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INTAKE_DIR="$SCRIPT_DIR/users/jh/intake/screenshots"

# Number of screenshots to show (default: 1)
COUNT=${1:-1}

# Check if intake directory exists
if [ ! -d "$INTAKE_DIR" ]; then
    echo -e "${YELLOW}No screenshots found. Run ./sync_screenshots.sh first.${NC}"
    exit 1
fi

# Count total screenshots
TOTAL=$(find "$INTAKE_DIR" -type f | wc -l | tr -d ' ')

if [ "$TOTAL" -eq 0 ]; then
    echo -e "${YELLOW}No screenshots in intake. Run ./sync_screenshots.sh to sync.${NC}"
    exit 1
fi

echo -e "${BLUE}=== Latest Screenshot(s) ===${NC}"
echo ""

# Show latest N screenshots
find "$INTAKE_DIR" -type f -print0 | \
    xargs -0 ls -lt | \
    head -n "$COUNT" | \
    while read -r line; do
        # Parse ls output
        perms=$(echo "$line" | awk '{print $1}')
        size=$(echo "$line" | awk '{print $5}')
        month=$(echo "$line" | awk '{print $6}')
        day=$(echo "$line" | awk '{print $7}')
        time=$(echo "$line" | awk '{print $8}')
        filename=$(echo "$line" | awk '{print $9}')
        
        # Get just the basename
        basename=$(basename "$filename")
        
        # Format size
        if [ "$size" -gt 1048576 ]; then
            size_mb=$(echo "scale=1; $size / 1048576" | bc)
            size_display="${size_mb}MB"
        else
            size_kb=$(echo "scale=0; $size / 1024" | bc)
            size_display="${size_kb}KB"
        fi
        
        echo -e "${GREEN}📸 $basename${NC}"
        echo -e "   ${CYAN}Date:${NC} $month $day $time"
        echo -e "   ${CYAN}Size:${NC} $size_display"
        echo -e "   ${CYAN}Path:${NC} $filename"
        echo ""
    done

echo -e "${BLUE}Total screenshots in intake: $TOTAL${NC}"
echo ""

# Show quick commands
if [ "$COUNT" -eq 1 ]; then
    echo -e "${YELLOW}Tip:${NC} Use './checking_sg.sh 5' to see last 5 screenshots"
fi
