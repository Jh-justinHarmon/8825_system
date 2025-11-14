#!/bin/bash
# Install Competitive Analysis Tool Aliases
# Run this to add global shortcuts to your shell

echo "🔧 Installing Competitive Analysis Tool Aliases..."

# Get the project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Aliases to add
ALIASES="
# Competitive Analysis Tool Aliases (added $(date +%Y-%m-%d))
alias comp-add='python3 \"$PROJECT_DIR/scripts/add_competitor.py\"'
alias comp-list='python3 \"$PROJECT_DIR/scripts/list_competitors.py\"'
alias comp-analyze='python3 \"$PROJECT_DIR/scripts/analyze_basic.py\"'
alias comp-cd='cd \"$PROJECT_DIR\"'
"

# Determine shell config file
if [ -f ~/.zshrc ]; then
    SHELL_CONFIG=~/.zshrc
    SHELL_NAME="zsh"
elif [ -f ~/.bashrc ]; then
    SHELL_CONFIG=~/.bashrc
    SHELL_NAME="bash"
else
    echo "❌ Could not find .zshrc or .bashrc"
    exit 1
fi

echo "📝 Adding aliases to $SHELL_CONFIG..."

# Check if aliases already exist
if grep -q "Competitive Analysis Tool Aliases" "$SHELL_CONFIG"; then
    echo "⚠️  Aliases already exist in $SHELL_CONFIG"
    echo "   Remove them manually if you want to reinstall"
    exit 0
fi

# Add aliases
echo "$ALIASES" >> "$SHELL_CONFIG"

echo "✅ Aliases added to $SHELL_CONFIG"
echo ""
echo "🔄 Reload your shell to use the new commands:"
echo "   source $SHELL_CONFIG"
echo ""
echo "📋 Available commands:"
echo "   comp-add \"URL\" \"Name\"     - Add a competitor"
echo "   comp-list                    - List all competitors"
echo "   comp-analyze \"name\"         - Analyze a competitor"
echo "   comp-cd                      - Navigate to project folder"
echo ""
echo "🎯 Example usage:"
echo "   comp-add \"https://figma.com\" \"Figma\""
echo "   comp-list"
echo "   comp-analyze \"Figma\""
echo ""
