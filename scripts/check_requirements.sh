#!/bin/bash
# 8825 System Requirements Checker
# Verifies all dependencies and configuration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}8825 Requirements Check${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# ============================================================================
# CHECK PYTHON
# ============================================================================
echo -e "${YELLOW}Checking Python...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ Python 3.10+ required (found $PYTHON_VERSION)${NC}"
        ((FAIL_COUNT++))
    fi
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    ((FAIL_COUNT++))
fi

# ============================================================================
# CHECK PIP
# ============================================================================
echo -e "${YELLOW}Checking pip...${NC}"

if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ pip $PIP_VERSION${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ pip3 not found${NC}"
    ((FAIL_COUNT++))
fi

# ============================================================================
# CHECK PYTHON PACKAGES
# ============================================================================
echo ""
echo -e "${YELLOW}Checking Python packages...${NC}"

REQUIRED_PACKAGES=(
    "openai"
    "python-dotenv"
    "requests"
    "flask"
    "google-auth"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import ${package//-/_}" 2>/dev/null; then
        VERSION=$(python3 -c "import ${package//-/_}; print(${package//-/_}.__version__)" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✅ $package ($VERSION)${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ $package not installed${NC}"
        ((FAIL_COUNT++))
    fi
done

# ============================================================================
# CHECK OPTIONAL DEPENDENCIES
# ============================================================================
echo ""
echo -e "${YELLOW}Checking optional dependencies...${NC}"

# Tesseract
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Tesseract OCR $TESSERACT_VERSION${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  Tesseract OCR not found (optional)${NC}"
    ((WARN_COUNT++))
fi

# Playwright
if python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo -e "${GREEN}✅ Playwright installed${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  Playwright not installed (optional)${NC}"
    ((WARN_COUNT++))
fi

# Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js $NODE_VERSION${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  Node.js not found (optional, for MCP servers)${NC}"
    ((WARN_COUNT++))
fi

# ============================================================================
# CHECK CONFIGURATION
# ============================================================================
echo ""
echo -e "${YELLOW}Checking configuration...${NC}"

# Check .env file
if [ -f "$ROOT_DIR/.env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
    ((PASS_COUNT++))
    
    # Check for OpenAI API key
    if grep -q "OPENAI_API_KEY=sk-" "$ROOT_DIR/.env"; then
        echo -e "${GREEN}✅ OpenAI API key configured${NC}"
        ((PASS_COUNT++))
    elif grep -q "OPENAI_API_KEY=your_openai_api_key_here" "$ROOT_DIR/.env"; then
        echo -e "${RED}❌ OpenAI API key not set (still using placeholder)${NC}"
        ((FAIL_COUNT++))
    else
        echo -e "${YELLOW}⚠️  OpenAI API key may not be configured${NC}"
        ((WARN_COUNT++))
    fi
else
    echo -e "${RED}❌ .env file not found${NC}"
    ((FAIL_COUNT++))
fi

# Check ~/.8825 directory
if [ -d "$HOME/.8825" ]; then
    echo -e "${GREEN}✅ ~/.8825 directory exists${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ ~/.8825 directory not found${NC}"
    ((FAIL_COUNT++))
fi

# Check brain state
if [ -f "$HOME/.8825/brain_state/state.json" ]; then
    echo -e "${GREEN}✅ Brain state initialized${NC}"
    ((PASS_COUNT++))
else
    echo -e "${YELLOW}⚠️  Brain state not initialized${NC}"
    ((WARN_COUNT++))
fi

# ============================================================================
# CHECK PERMISSIONS
# ============================================================================
echo ""
echo -e "${YELLOW}Checking permissions...${NC}"

if [ -w "$ROOT_DIR" ]; then
    echo -e "${GREEN}✅ Write access to system directory${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ No write access to system directory${NC}"
    ((FAIL_COUNT++))
fi

if [ -w "$HOME/.8825" ]; then
    echo -e "${GREEN}✅ Write access to ~/.8825${NC}"
    ((PASS_COUNT++))
else
    echo -e "${RED}❌ No write access to ~/.8825${NC}"
    ((FAIL_COUNT++))
fi

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo -e "${GREEN}✅ Passed: $PASS_COUNT${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARN_COUNT${NC}"
echo -e "${RED}❌ Failed: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 All required checks passed!${NC}"
    echo ""
    echo -e "${BLUE}You're ready to use 8825!${NC}"
    echo ""
    echo "Start the brain daemon:"
    echo "  ${YELLOW}cd $ROOT_DIR${NC}"
    echo "  ${YELLOW}source venv/bin/activate${NC}"
    echo "  ${YELLOW}python3 8825_core/brain/brain_daemon.py${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some required checks failed${NC}"
    echo ""
    echo "Fix the issues above and run this script again."
    echo ""
    echo "Installation help:"
    echo "  ${YELLOW}./scripts/install.sh${NC}"
    exit 1
fi
