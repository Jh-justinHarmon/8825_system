#!/bin/bash
# 8825 Onboarding Script
# Interactive setup for new users

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

clear
echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}🎉 Welcome to 8825!${NC}"
echo -e "${CYAN}================================${NC}"
echo ""
echo "This wizard will help you get started."
echo ""

# ============================================================================
# CHECK INSTALLATION
# ============================================================================
echo -e "${YELLOW}Checking installation...${NC}"

if [ ! -f "$ROOT_DIR/.env" ]; then
    echo -e "${RED}❌ Installation not complete${NC}"
    echo ""
    echo "Please run installation first:"
    echo "  ${CYAN}./scripts/install.sh${NC}"
    exit 1
fi

if ! grep -q "sk-" "$ROOT_DIR/.env" 2>/dev/null; then
    echo -e "${RED}❌ OpenAI API key not configured${NC}"
    echo ""
    echo "Please add your API key to .env:"
    echo "  ${CYAN}nano .env${NC}"
    echo ""
    echo "Change:"
    echo "  OPENAI_API_KEY=your_openai_api_key_here"
    echo "To:"
    echo "  OPENAI_API_KEY=sk-proj-..."
    exit 1
fi

echo -e "${GREEN}✅ Installation verified${NC}"
echo ""

# ============================================================================
# WELCOME
# ============================================================================
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}About 8825${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "8825 is your AI-powered personal operating system."
echo ""
echo "Key features:"
echo "  • Brain system - Learns from your work"
echo "  • Accountability loops - Track your goals"
echo "  • Meeting automation - Process transcripts"
echo "  • Workflow protocols - Structured thinking"
echo ""
read -p "Press Enter to continue..."
clear

# ============================================================================
# USER PROFILE
# ============================================================================
echo -e "${YELLOW}[1/5] User Profile${NC}"
echo ""

# Get username from .env or system
USERNAME=$(grep "USER_NAME=" "$ROOT_DIR/.env" | cut -d'=' -f2)
if [ -z "$USERNAME" ]; then
    USERNAME=$(whoami)
fi

echo "Your username: ${GREEN}$USERNAME${NC}"
echo ""

# Ask for display name
read -p "What should we call you? (e.g., Justin): " DISPLAY_NAME
if [ -z "$DISPLAY_NAME" ]; then
    DISPLAY_NAME=$USERNAME
fi

echo ""
echo -e "${GREEN}✅ Profile configured${NC}"
echo "  Username: $USERNAME"
echo "  Display name: $DISPLAY_NAME"
echo ""
read -p "Press Enter to continue..."
clear

# ============================================================================
# FIRST GOAL
# ============================================================================
echo -e "${YELLOW}[2/5] Set Your First Goal${NC}"
echo ""
echo "Let's create an accountability loop to track something important."
echo ""

read -p "What goal do you want to track? (e.g., Daily Exercise): " GOAL_NAME
if [ -z "$GOAL_NAME" ]; then
    GOAL_NAME="Daily Goals"
fi

read -p "Brief description: " GOAL_DESC
if [ -z "$GOAL_DESC" ]; then
    GOAL_DESC="Track daily progress"
fi

read -p "What are you measuring? (e.g., Workouts): " METRIC_NAME
if [ -z "$METRIC_NAME" ]; then
    METRIC_NAME="Tasks"
fi

read -p "Target per week? (e.g., 5): " METRIC_TARGET
if [ -z "$METRIC_TARGET" ]; then
    METRIC_TARGET=5
fi

echo ""
echo "Creating accountability loop..."

# Activate venv and create loop
source "$ROOT_DIR/venv/bin/activate"
python3 "$ROOT_DIR/8825_core/agents/accountability_loop_agent.py" \
    --add "$GOAL_NAME" \
    --description "$GOAL_DESC" \
    --metric-name "$METRIC_NAME" \
    --metric-target "$METRIC_TARGET" \
    --metric-unit "per week" 2>/dev/null || echo "Note: Loop creation skipped"

echo ""
echo -e "${GREEN}✅ Goal created${NC}"
echo "  Goal: $GOAL_NAME"
echo "  Target: $METRIC_TARGET $METRIC_NAME per week"
echo ""
read -p "Press Enter to continue..."
clear

# ============================================================================
# BRAIN INTRODUCTION
# ============================================================================
echo -e "${YELLOW}[3/5] Brain System${NC}"
echo ""
echo "The 8825 Brain learns from your work:"
echo ""
echo "  • Extracts patterns from conversations"
echo "  • Remembers decisions and solutions"
echo "  • Tracks what works and what doesn't"
echo "  • Gets smarter over time"
echo ""
echo "The brain runs in the background and requires no maintenance."
echo ""
read -p "Press Enter to continue..."
clear

# ============================================================================
# QUICK TOUR
# ============================================================================
echo -e "${YELLOW}[4/5] Quick Tour${NC}"
echo ""
echo "Here's what you can do with 8825:"
echo ""
echo -e "${CYAN}1. Check Your Goals${NC}"
echo "   cd $ROOT_DIR/8825_core/agents"
echo "   python3 accountability_loop_agent.py --list"
echo ""
echo -e "${CYAN}2. Process Meeting Transcripts${NC}"
echo "   cd $ROOT_DIR/8825_core/workflows/meeting_automation"
echo "   python3 process_meetings.py"
echo ""
echo -e "${CYAN}3. Export Brain Learnings${NC}"
echo "   cd $ROOT_DIR/8825_core/agents"
echo "   python3 brain_learning_exporter.py --format markdown"
echo ""
echo -e "${CYAN}4. Explore Protocols${NC}"
echo "   cat $ROOT_DIR/8825_core/protocols/README.md"
echo ""
read -p "Press Enter to continue..."
clear

# ============================================================================
# NEXT STEPS
# ============================================================================
echo -e "${YELLOW}[5/5] Next Steps${NC}"
echo ""
echo "You're all set! Here's what to do next:"
echo ""
echo -e "${GREEN}1. Check your goal:${NC}"
echo "   cd $ROOT_DIR/8825_core/agents"
echo "   python3 accountability_loop_agent.py --check $(echo "$GOAL_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')"
echo ""
echo -e "${GREEN}2. Read the quick start:${NC}"
echo "   cat $ROOT_DIR/QUICKSTART.md"
echo ""
echo -e "${GREEN}3. Explore the system:${NC}"
echo "   ls $ROOT_DIR/8825_core/"
echo ""
echo -e "${GREEN}4. Get help:${NC}"
echo "   cat $ROOT_DIR/INSTALLATION.md"
echo ""
read -p "Press Enter to finish..."
clear

# ============================================================================
# COMPLETION
# ============================================================================
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}🎉 Onboarding Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Welcome to 8825, $DISPLAY_NAME!"
echo ""
echo "Your first goal: ${CYAN}$GOAL_NAME${NC}"
echo "Target: ${CYAN}$METRIC_TARGET $METRIC_NAME per week${NC}"
echo ""
echo -e "${YELLOW}Quick Commands:${NC}"
echo ""
echo "  # Activate environment"
echo "  source $ROOT_DIR/venv/bin/activate"
echo ""
echo "  # Check goals"
echo "  python3 8825_core/agents/accountability_loop_agent.py --list"
echo ""
echo "  # Start brain"
echo "  python3 8825_core/brain/brain_daemon.py"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  • QUICKSTART.md - Get started in 5 minutes"
echo "  • INSTALLATION.md - Complete setup guide"
echo "  • 8825_core/protocols/README.md - Workflow protocols"
echo ""
echo -e "${GREEN}Happy building! 🚀${NC}"
echo ""
