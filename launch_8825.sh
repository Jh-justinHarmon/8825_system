#!/bin/bash
# 8825 Mode Launch Script
# Starts all required services and displays activation message

echo "🚀 Launching 8825 v3.0..."
echo ""

# Change to v3.0 directory
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system"

# Start MCP servers
echo "Starting MCP servers..."
./start_all_mcps.sh > /dev/null 2>&1

# Wait a moment for servers to start
sleep 2

# Check what's running
echo ""
echo "="*60
echo "8825 MODE ACTIVATED"
echo "="*60
echo ""
echo "Version: 3.0.0"
echo "Workspace: 8825-system"
echo ""
echo "Services Running:"
ps aux | grep -E "(mcp.*server|brain_daemon)" | grep -v grep | awk '{print "  ✓", $11}' | sed 's|.*/||'
echo ""
echo "Available Focus Areas:"
echo "  - Joju (professional library management)"
echo "  - HCSS (client automation)"
echo "  - JH Assistant (personal automation)"
echo ""
echo "Commands:"
echo "  - 'focus on [project]' - Enter project sandbox"
echo "  - 'list focuses' - Show all available focus areas"
echo "  - 'exit 8825 mode' - Deactivate system"
echo ""
echo "What would you like to focus on?"
echo ""
