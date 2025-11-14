#!/bin/bash
# Process HCSS Meetings - Generate Word docs for last week's meetings

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}=== HCSS Meeting Summary Pipeline ===${NC}"
echo ""

# Check for python-docx
if ! python3 -c "import docx" 2>/dev/null; then
    echo -e "${YELLOW}⚠ Installing python-docx...${NC}"
    pip3 install python-docx
    echo ""
fi

# Run pipeline
echo -e "${BLUE}Processing last week's meetings...${NC}"
echo ""

cd "$SCRIPT_DIR"
python3 meeting_summary_pipeline.py

echo ""
echo -e "${GREEN}✅ Pipeline complete!${NC}"
