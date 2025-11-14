#!/bin/bash
# 8825 System Installation Script
# Version: 3.1.0
# Last Updated: 2025-11-13

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}8825 System Installation${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# ============================================================================
# STEP 1: Check System Requirements
# ============================================================================
echo -e "${YELLOW}[1/7] Checking system requirements...${NC}"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Install Python 3.10+: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}❌ Python 3.10+ required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 $(pip3 --version | cut -d' ' -f2)${NC}"

# ============================================================================
# STEP 2: Create Virtual Environment (Optional but Recommended)
# ============================================================================
echo ""
echo -e "${YELLOW}[2/7] Setting up virtual environment...${NC}"

if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$ROOT_DIR/venv"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source "$ROOT_DIR/venv/bin/activate"

# ============================================================================
# STEP 3: Install Python Dependencies
# ============================================================================
echo ""
echo -e "${YELLOW}[3/7] Installing Python dependencies...${NC}"

if [ -f "$ROOT_DIR/requirements-full.txt" ]; then
    pip3 install --upgrade pip
    pip3 install -r "$ROOT_DIR/requirements-full.txt"
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements-full.txt not found${NC}"
    exit 1
fi

# ============================================================================
# STEP 4: Create Directory Structure
# ============================================================================
echo ""
echo -e "${YELLOW}[4/7] Creating directory structure...${NC}"

# Create user config directory
mkdir -p "$HOME/.8825"
echo -e "${GREEN}✅ Created ~/.8825${NC}"

# Create brain state directory
mkdir -p "$HOME/.8825/brain_state"
echo -e "${GREEN}✅ Created ~/.8825/brain_state${NC}"

# Create accountability loops directory
mkdir -p "$HOME/.8825/accountability_loops.json"
touch "$HOME/.8825/accountability_loops.json"
echo "{}" > "$HOME/.8825/accountability_loops.json"
echo -e "${GREEN}✅ Created accountability loops config${NC}"

# ============================================================================
# STEP 5: Setup Environment Variables
# ============================================================================
echo ""
echo -e "${YELLOW}[5/7] Setting up environment variables...${NC}"

if [ ! -f "$ROOT_DIR/.env" ]; then
    if [ -f "$ROOT_DIR/.env.template" ]; then
        # Copy template
        cp "$ROOT_DIR/.env.template" "$ROOT_DIR/.env"
        
        # Auto-configure paths
        echo "Auto-configuring paths..."
        
        # Detect Dropbox location
        if [ -d "$HOME/Dropbox" ]; then
            DROPBOX_PATH="$HOME/Dropbox"
        elif [ -d "$HOME/Library/CloudStorage/Dropbox" ]; then
            DROPBOX_PATH="$HOME/Library/CloudStorage/Dropbox"
        else
            DROPBOX_PATH="$HOME/Dropbox"  # Default
        fi
        
        # Replace placeholders in .env
        sed -i '' "s|SYSTEM_ROOT=/path/to/8825-system|SYSTEM_ROOT=$ROOT_DIR|g" "$ROOT_DIR/.env"
        sed -i '' "s|DROPBOX_ROOT=/path/to/Dropbox|DROPBOX_ROOT=$DROPBOX_PATH|g" "$ROOT_DIR/.env"
        sed -i '' "s|DOWNLOADS_DIR=/path/to/Downloads|DOWNLOADS_DIR=$HOME/Downloads|g" "$ROOT_DIR/.env"
        sed -i '' "s|USER_NAME=your_username|USER_NAME=$(whoami)|g" "$ROOT_DIR/.env"
        
        echo -e "${GREEN}✅ Created .env from template${NC}"
        echo -e "${GREEN}✅ Auto-configured paths:${NC}"
        echo "   SYSTEM_ROOT=$ROOT_DIR"
        echo "   DROPBOX_ROOT=$DROPBOX_PATH"
        echo "   DOWNLOADS_DIR=$HOME/Downloads"
        echo "   USER_NAME=$(whoami)"
        echo ""
        echo -e "${YELLOW}⚠️  Edit .env and add your OpenAI API key${NC}"
    else
        # Create basic .env with auto-detected paths
        DROPBOX_PATH="$HOME/Dropbox"
        if [ -d "$HOME/Library/CloudStorage/Dropbox" ]; then
            DROPBOX_PATH="$HOME/Library/CloudStorage/Dropbox"
        fi
        
        cat > "$ROOT_DIR/.env" << EOF
# 8825 System Configuration
# Created: $(date)

# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# System Paths (auto-configured)
SYSTEM_ROOT=$ROOT_DIR
DROPBOX_ROOT=$DROPBOX_PATH
DOWNLOADS_DIR=$HOME/Downloads
USER_NAME=$(whoami)

# Optional: Google API Credentials
# GOOGLE_CREDENTIALS_PATH=\${SYSTEM_ROOT}/8825_core/integrations/google/credentials.json
# GOOGLE_TOKEN_PATH=\${SYSTEM_ROOT}/8825_core/integrations/google/token.json

# Optional: Reddit API
# REDDIT_CLIENT_ID=your_reddit_client_id
# REDDIT_CLIENT_SECRET=your_reddit_client_secret
EOF
        echo -e "${GREEN}✅ Created .env file with auto-configured paths${NC}"
        echo -e "${YELLOW}⚠️  Edit .env and add your OpenAI API key${NC}"
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# ============================================================================
# STEP 6: Install Optional Dependencies
# ============================================================================
echo ""
echo -e "${YELLOW}[6/7] Checking optional dependencies...${NC}"

# Check Tesseract
if command -v tesseract &> /dev/null; then
    echo -e "${GREEN}✅ Tesseract OCR installed${NC}"
else
    echo -e "${YELLOW}⚠️  Tesseract OCR not found (optional, for bill processing)${NC}"
    echo "   Install: brew install tesseract (macOS) or sudo apt install tesseract-ocr (Linux)"
fi

# Check Playwright
echo "Checking Playwright browsers..."
if python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start()" 2>/dev/null; then
    echo -e "${GREEN}✅ Playwright browsers installed${NC}"
else
    echo -e "${YELLOW}⚠️  Playwright browsers not found (optional, for screenshots)${NC}"
    echo "   Install: python3 -m playwright install chromium"
fi

# ============================================================================
# STEP 7: Initialize Brain System
# ============================================================================
echo ""
echo -e "${YELLOW}[7/7] Initializing brain system...${NC}"

# Create initial brain state
if [ ! -f "$HOME/.8825/brain_state/state.json" ]; then
    mkdir -p "$HOME/.8825/brain_state"
    cat > "$HOME/.8825/brain_state/state.json" << EOF
{
  "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "version": "3.1.0",
  "learnings": [],
  "memories": [],
  "last_sync": null
}
EOF
    echo -e "${GREEN}✅ Brain state initialized${NC}"
else
    echo -e "${GREEN}✅ Brain state already exists${NC}"
fi

# ============================================================================
# INSTALLATION COMPLETE
# ============================================================================
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Configure API keys:"
echo "   ${YELLOW}nano $ROOT_DIR/.env${NC}"
echo ""
echo "2. Add your OpenAI API key (REQUIRED):"
echo "   ${YELLOW}OPENAI_API_KEY=sk-...${NC}"
echo ""
echo "3. Test the installation:"
echo "   ${YELLOW}./scripts/check_requirements.sh${NC}"
echo ""
echo "4. Start using 8825:"
echo "   ${YELLOW}cd $ROOT_DIR${NC}"
echo "   ${YELLOW}source venv/bin/activate${NC}"
echo "   ${YELLOW}python3 8825_core/brain/brain_daemon.py${NC}"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   - Quick Start: QUICKSTART.md"
echo "   - System Requirements: SYSTEM_REQUIREMENTS.md"
echo "   - User Guide: docs/USER_GUIDE.md"
echo ""
echo -e "${YELLOW}⚠️  Remember to activate the virtual environment:${NC}"
echo "   ${YELLOW}source $ROOT_DIR/venv/bin/activate${NC}"
echo ""
