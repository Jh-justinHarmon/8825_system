#!/bin/bash
# Joju Task Management - Setup Checker
# Run this before using the task system

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 Checking Joju Task Management Setup..."
echo ""

# Check 1: Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 installed"

# Check 2: notion-client
if ! python3 -c "import notion_client" 2>/dev/null; then
    echo -e "${RED}❌ notion-client not installed${NC}"
    echo "   Run: pip3 install notion-client==1.0.0"
    exit 1
fi

# Check version
VERSION=$(python3 -c "import pkg_resources; print(pkg_resources.get_distribution('notion-client').version)" 2>/dev/null || echo "unknown")
if [ "$VERSION" != "1.0.0" ]; then
    echo -e "${YELLOW}⚠️  notion-client version: $VERSION${NC}"
    echo "   Recommended: 1.0.0 (v2.7.0+ has breaking changes)"
    echo "   Run: pip3 uninstall notion-client && pip3 install notion-client==1.0.0"
else
    echo -e "${GREEN}✓${NC} notion-client v1.0.0 installed"
fi

# Check 3: config.json
if [ ! -f "config.json" ]; then
    echo -e "${RED}❌ config.json not found${NC}"
    echo "   Run: cp config.example.json config.json"
    echo "   Then edit with your Notion API key"
    echo ""
    echo "   📍 Credentials location: v2.0 workspace at config/8825_config.json"
    exit 1
fi
echo -e "${GREEN}✓${NC} config.json exists"

# Check 4: Config has real credentials
if grep -q "YOUR_NOTION_API_KEY_HERE" config.json 2>/dev/null; then
    echo -e "${RED}❌ config.json not configured (still has placeholder)${NC}"
    echo "   Edit config.json with your real Notion API key"
    exit 1
fi
echo -e "${GREEN}✓${NC} config.json configured"

# Check 5: Database ID format
DB_ID=$(python3 -c "import json; print(json.load(open('config.json'))['notion']['database_id'])" 2>/dev/null || echo "")
if [[ ! "$DB_ID" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]]; then
    echo -e "${YELLOW}⚠️  Database ID format may be incorrect${NC}"
    echo "   Should have dashes (UUID format): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    echo "   Current: $DB_ID"
else
    echo -e "${GREEN}✓${NC} Database ID format correct"
fi

# Check 6: Test connection
echo ""
echo "Testing Notion connection..."
if python3 notion_sync.py test > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Notion connection successful"
else
    echo -e "${RED}❌ Notion connection failed${NC}"
    echo "   Run: python3 notion_sync.py test"
    echo "   For troubleshooting: see NOTION_SETUP_COMPLETE.md"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All checks passed! Task management is ready to use.${NC}"
echo ""
echo "Quick commands:"
echo "  python3 notion_sync.py pull    # Pull tasks from Notion"
echo "  python3 task_manager.py        # Interactive task management"
echo ""
