#!/bin/bash
# 8825 Health Check
# Validates system state and detects issues

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "=== 8825 Health Check ==="
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq not installed (needed for health checks)${NC}"
    echo "   Installing jq..."
    brew install jq
fi

# 1. Check Daemon Status
echo "[1/5] Daemon Status..."
daemon_count=$(jq -r '.daemons | length' "$REGISTRY")
for i in $(seq 0 $((daemon_count - 1))); do
    daemon_name=$(jq -r ".daemons[$i].name" "$REGISTRY")
    should_run=$(jq -r ".daemons[$i].should_be_running" "$REGISTRY")
    
    if ps aux | grep -v grep | grep "$daemon_name" > /dev/null; then
        if [ "$should_run" = "true" ]; then
            echo -e "  ${GREEN}✅${NC} $daemon_name: running (expected)"
        else
            echo -e "  ${YELLOW}⚠️${NC}  $daemon_name: running (should be stopped)"
        fi
    else
        if [ "$should_run" = "true" ]; then
            echo -e "  ${YELLOW}⚠️${NC}  $daemon_name: stopped (should be running)"
        else
            echo -e "  ${GREEN}✅${NC} $daemon_name: stopped (expected)"
        fi
    fi
done

# 2. Check Downloads Size
echo ""
echo "[2/5] Downloads Folders..."
downloads_size=$(du -sm ~/Downloads 2>/dev/null | cut -f1)
if [ $downloads_size -gt 100 ]; then
    echo -e "  ${YELLOW}⚠️${NC}  Local Downloads: ${downloads_size}MB (cleanup recommended)"
else
    echo -e "  ${GREEN}✅${NC} Local Downloads: ${downloads_size}MB (healthy)"
fi

icloud_downloads="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Downloads"
if [ -d "$icloud_downloads" ]; then
    icloud_size=$(du -sm "$icloud_downloads" 2>/dev/null | cut -f1)
    if [ $icloud_size -gt 100 ]; then
        echo -e "  ${YELLOW}⚠️${NC}  iCloud Downloads: ${icloud_size}MB (cleanup recommended)"
    else
        echo -e "  ${GREEN}✅${NC} iCloud Downloads: ${icloud_size}MB (healthy)"
    fi
else
    echo -e "  ${YELLOW}⚠️${NC}  iCloud Downloads: not found"
fi

# 3. Check BRAIN_TRANSPORT
echo ""
echo "[3/5] BRAIN_TRANSPORT..."
if [ -f ~/Downloads/0-8825_BRAIN_TRANSPORT.json ]; then
    echo -e "  ${GREEN}✅${NC} Local Downloads: Present"
else
    echo -e "  ${RED}❌${NC} Local Downloads: Missing"
fi

if [ -f "$icloud_downloads/0-8825_BRAIN_TRANSPORT.json" ]; then
    echo -e "  ${GREEN}✅${NC} iCloud Downloads: Present"
else
    echo -e "  ${YELLOW}⚠️${NC}  iCloud Downloads: Missing"
fi

# 4. Check for Junk Files
echo ""
echo "[4/5] Junk Detection..."
junk_found=0

for pattern in "old" "sticky_*" "*brainstorm*" "IMG_*.HEIC" "IMG_*.jpeg"; do
    if ls ~/Downloads/$pattern 2>/dev/null | grep -q .; then
        echo -e "  ${YELLOW}⚠️${NC}  Found: $pattern in Downloads"
        junk_found=1
    fi
done

if [ $junk_found -eq 0 ]; then
    echo -e "  ${GREEN}✅${NC} No junk files detected"
fi

# 5. Check Registry Freshness
echo ""
echo "[5/5] Registry Status..."
last_updated=$(jq -r '.last_updated' "$REGISTRY")
echo -e "  ${GREEN}✅${NC} Last updated: $last_updated"

# Overall Status
echo ""
echo "=== Overall Status ==="
if [ $downloads_size -lt 100 ] && [ $junk_found -eq 0 ]; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${YELLOW}⚠️  NEEDS ATTENTION${NC}"
fi
echo ""
