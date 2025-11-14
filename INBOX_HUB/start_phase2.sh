#!/bin/bash
# Input Hub Phase 2: Start Full Automation
# Launches auto-sync daemon with OCR and smart routing

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Input Hub Phase 2: Full Automation ===${NC}"
echo ""

# Check dependencies
echo "Checking dependencies..."
python3 -c "import watchdog" 2>/dev/null || {
    echo -e "${YELLOW}Installing watchdog...${NC}"
    pip3 install watchdog
}

python3 -c "import pytesseract" 2>/dev/null || {
    echo -e "${YELLOW}Installing pytesseract...${NC}"
    pip3 install pytesseract
}

python3 -c "from PIL import Image" 2>/dev/null || {
    echo -e "${YELLOW}Installing Pillow...${NC}"
    pip3 install Pillow
}

which tesseract > /dev/null || {
    echo -e "${YELLOW}⚠️  Tesseract not found. Install with: brew install tesseract${NC}"
    exit 1
}

echo -e "${GREEN}✓ All dependencies ready${NC}"
echo ""

# Process existing screenshots first
echo "Processing existing screenshots..."
cd "$SCRIPT_DIR"
python3 ocr_engine.py
echo ""

# Route processed screenshots
echo "Routing screenshots to projects..."
python3 smart_router.py --dry-run
echo ""

read -p "Route screenshots now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 smart_router.py
    echo ""
fi

# Start auto-sync daemon
echo -e "${BLUE}Starting auto-sync daemon...${NC}"
echo "This will watch for new files and auto-sync them."
echo "Press Ctrl+C to stop."
echo ""

python3 auto_sync_daemon.py
