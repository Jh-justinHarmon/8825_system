#!/bin/bash
# 8825 Unified Startup
# One command to validate, check, and prepare the entire system

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

set -e

V3_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     8825 UNIFIED STARTUP PROTOCOL     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"

# Run unified startup
"$V3_ROOT/8825_core/system/8825_unified_startup.sh"
unified_status=$?

# Step 4: System Ready
echo -e "${BLUE}[4/4] System Status${NC}"
echo ""

if [ $unified_status -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║          ✅ SYSTEM READY ✅           ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Available commands:"
    echo "  8825 start          - Run startup protocol"
    echo "  8825 health         - Run health check only"
    echo "  8825 deps           - Check dependencies only"
    echo ""
    exit 0
else
    echo -e "${YELLOW}╔════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║      ⚠️  NEEDS ATTENTION ⚠️          ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Review warnings above and address issues"
    echo ""
    exit 1
fi
