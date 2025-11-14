#!/bin/bash
# 8825 Registry Review
# Shows auto-registered items that need manual review

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${BLUE}=== Auto-Registered Items Needing Review ===${NC}"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

# Find scripts that need review
needs_review=$(jq -r '.scripts[] | select(.needs_review == true)' "$REGISTRY")

if [ -z "$needs_review" ]; then
    echo -e "${GREEN}✅ No items need review${NC}"
    echo ""
    exit 0
fi

# Count items
review_count=$(echo "$needs_review" | jq -s 'length')

echo "Found $review_count item(s) needing review:"
echo ""

# Display each item
item_num=1
echo "$needs_review" | jq -c '.' | while read -r item; do
    name=$(echo "$item" | jq -r '.name')
    path=$(echo "$item" | jq -r '.path')
    type=$(echo "$item" | jq -r '.type')
    purpose=$(echo "$item" | jq -r '.purpose')
    added=$(echo "$item" | jq -r '.last_modified')
    
    # Get dependencies
    deps=$(echo "$item" | jq -r '.dependencies[]?' 2>/dev/null | tr '\n' ', ' | sed 's/,$//')
    
    # Get touches
    touches=$(echo "$item" | jq -r '.touches[]?' 2>/dev/null | tr '\n' ', ' | sed 's/,$//')
    
    echo -e "${CYAN}$item_num. $name${NC}"
    echo "   Path: $path"
    echo "   Type: $type"
    echo "   Purpose: $purpose"
    if [ -n "$deps" ]; then
        echo "   Dependencies: $deps"
    fi
    if [ -n "$touches" ]; then
        echo "   Touches: $touches"
    fi
    echo "   Added: $added"
    echo ""
    echo "   Actions:"
    echo "   • Update: 8825 registry update $name --purpose \"Better description\""
    echo "   • Mark reviewed: 8825 registry update $name --reviewed"
    echo "   • Remove: 8825 registry remove $name"
    echo ""
    
    item_num=$((item_num + 1))
done

echo -e "${YELLOW}Tip:${NC} Review and refine auto-detected entries for accuracy"
echo ""
