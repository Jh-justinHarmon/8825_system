#!/bin/bash
# 8825 Target Acquisition Setup v3
# Asks for ALL paths - 3 inputs + 1 output

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/user_config.json"

echo "============================================================"
echo "8825 SETUP v3 - Input/Output Configuration"
echo "============================================================"
echo ""
echo "We'll configure:"
echo "  • 3 INPUT locations (where files come from)"
echo "  • 1 OUTPUT location (where 8825 saves to)"
echo ""
read -p "Press Enter to begin..."
echo ""

# Function to clean up dragged path and resolve symlinks
clean_path() {
    local path="$1"
    # Remove quotes and trailing slashes
    path=$(echo "$path" | sed "s/^['\"]//;s/['\"]$//;s:/$::" | xargs)
    
    # Fix common drag-and-drop issues
    # macOS removes ~ when dragging, so fix paths like "comappleCloudDocs"
    path=$(echo "$path" | sed 's/comappleCloudDocs/com~apple~CloudDocs/g')
    
    # Resolve symlinks (iCloud shows as ~/Documents but is really in Library/Mobile Documents)
    if [ -L "$path" ]; then
        # It's a symlink, resolve it
        path=$(readlink "$path")
    fi
    
    # Expand ~ to full path
    path="${path/#\~/$HOME}"
    
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

# Output: User chooses
while true; do
    echo "📁 OUTPUT: Where should 8825 save files?"
    echo "   Drag folder here (or paste path):"
    echo "   Examples:"
    echo "     - iCloud: ~/Library/Mobile Documents/com~apple~CloudDocs/8825"
    echo "     - Dropbox: ~/Dropbox/8825"
    echo "     - Documents: ~/Documents/8825"
    echo ""
    read -r output_input
    output_base=$(clean_path "$output_input")
    
    # Create if doesn't exist
    if [ ! -d "$output_base" ]; then
        echo "⚠️  Folder doesn't exist. Create it? (y/n)"
        read -r create_choice
        if [ "$create_choice" = "y" ]; then
            mkdir -p "$output_base"
            echo "✓ Created: $output_base"
            break
        else
            echo "Try again..."
            echo ""
            continue
        fi
    else
        echo "✓ Found: $output_base"
        break
    fi
done

# Create output structure
OUTPUT_BRAIN="$output_base/BRAIN"
OUTPUT_DOCS="$output_base/DOCS"

echo ""
echo "Creating output structure..."
mkdir -p "$OUTPUT_BRAIN"
mkdir -p "$OUTPUT_DOCS/sessions"
mkdir -p "$OUTPUT_DOCS/reports"
mkdir -p "$OUTPUT_DOCS/summaries"
mkdir -p "$OUTPUT_DOCS/exports"

echo "✓ Structure created"
echo ""
echo "Opening Finder to output location..."
open "$output_base"
echo "✓ Finder opened"
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
    "base": "$output_base",
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
echo "  📁 $output_base"
echo "     ├── BRAIN/     (Brain snapshots)"
echo "     └── DOCS/      (All 8825 outputs)"
echo ""
echo "Config saved to: $CONFIG_FILE"
echo ""
echo "Next: ./start.sh"
echo "============================================================"
