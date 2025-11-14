#!/bin/bash
# 8825 Target Acquisition Setup v2
# Inputs: Desktop Downloads, iCloud Downloads, Screenshots
# Output: iCloud Documents/8825

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/user_config.json"

echo "============================================================"
echo "8825 SETUP v2 - Input/Output Configuration"
echo "============================================================"
echo ""
echo "We'll configure:"
echo "  • 3 INPUT locations (where files come from)"
echo "  • 1 OUTPUT location (where 8825 saves to)"
echo ""
read -p "Press Enter to begin..."
echo ""

# Function to clean up dragged path
clean_path() {
    local path="$1"
    # Remove quotes and trailing slashes
    path=$(echo "$path" | sed "s/^['\"]//;s/['\"]$//;s:/$::" | xargs)
    # Fix common drag-and-drop issues
    # macOS removes ~ when dragging, so fix paths like "comappleCloudDocs"
    path=$(echo "$path" | sed 's/comappleCloudDocs/com~apple~CloudDocs/g')
    echo "$path"
}

echo "============================================================"
echo "INPUTS (Where files come from)"
echo "============================================================"
echo ""

# Input 1: Desktop Downloads
while true; do
    echo "📥 INPUT 1: Desktop Downloads"
    echo "   Example: /Users/justinharmon/Downloads"
    echo ""
    read -r downloads_input
    downloads_path=$(clean_path "$downloads_input")
    
    if [ -d "$downloads_path" ]; then
        echo "✓ Found: $downloads_path"
        break
    else
        echo "❌ Not found. Try again (or Ctrl+C to quit)"
        echo ""
    fi
done

echo ""

# Input 2: iCloud Downloads
while true; do
    echo "📱 INPUT 2: iCloud Downloads (mobile downloads)"
    echo "   Example: /Users/justinharmon/Library/Mobile Documents/com~apple~CloudDocs/Downloads"
    echo ""
    read -r icloud_downloads_input
    icloud_downloads_path=$(clean_path "$icloud_downloads_input")
    
    if [ -d "$icloud_downloads_path" ]; then
        echo "✓ Found: $icloud_downloads_path"
        break
    else
        echo "❌ Not found. Try again (or Ctrl+C to quit)"
        echo ""
    fi
done

echo ""

# Input 3: Screenshots
while true; do
    echo "📸 INPUT 3: Screenshots"
    echo "   Example: /Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Screenshots"
    echo ""
    read -r screenshots_input
    screenshots_path=$(clean_path "$screenshots_input")
    
    if [ -d "$screenshots_path" ]; then
        echo "✓ Found: $screenshots_path"
        break
    else
        echo "❌ Not found. Try again (or Ctrl+C to quit)"
        echo ""
    fi
done

echo ""
echo "============================================================"
echo "OUTPUT (Where 8825 saves files)"
echo "============================================================"
echo ""

# Create output structure in iCloud Documents
ICLOUD_DOCS="$HOME/Library/Mobile Documents/com~apple~CloudDocs"

if [ ! -d "$ICLOUD_DOCS" ]; then
    echo "❌ Error: iCloud Documents not found"
    echo "Make sure iCloud Drive is enabled in System Settings"
    exit 1
fi

# Create 8825 output structure
OUTPUT_BASE="$ICLOUD_DOCS/8825"
OUTPUT_BRAIN="$OUTPUT_BASE/BRAIN"
OUTPUT_DOCS="$OUTPUT_BASE/DOCS"

echo "Creating output structure in iCloud Documents..."
mkdir -p "$OUTPUT_BRAIN"
mkdir -p "$OUTPUT_DOCS/sessions"
mkdir -p "$OUTPUT_DOCS/reports"
mkdir -p "$OUTPUT_DOCS/summaries"
mkdir -p "$OUTPUT_DOCS/exports"

echo "✓ Created output structure"
echo ""
echo "📁 OUTPUT LOCATION:"
echo "   $OUTPUT_BASE"
echo ""
echo "Opening Finder to this location..."
open "$OUTPUT_BASE"
echo "✓ Finder opened - you can see the folders"
echo ""

# Save config
cat > "$CONFIG_FILE" <<EOF
{
  "user": "jh",
  "inputs": {
    "desktop_downloads": "$downloads_path",
    "icloud_downloads": "$icloud_downloads_path",
    "screenshots": "$screenshots_path"
  },
  "outputs": {
    "base": "$OUTPUT_BASE",
    "brain": "$OUTPUT_BRAIN",
    "docs": "$OUTPUT_DOCS"
  },
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "============================================================"
echo "✅ SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "INPUTS (watched):"
echo "  📥 Desktop Downloads: $downloads_path"
echo "  📱 iCloud Downloads: $icloud_downloads_path"
echo "  📸 Screenshots: $screenshots_path"
echo ""
echo "OUTPUT (destination):"
echo "  📁 $OUTPUT_BASE"
echo "     ├── BRAIN/     (Brain snapshots)"
echo "     └── DOCS/      (All 8825 outputs)"
echo ""
echo "Finder window opened to output location ✓"
echo ""
echo "Config saved to: $CONFIG_FILE"
echo ""
echo "Next: ./start.sh"
echo "============================================================"
