#!/bin/bash
# 8825 Target Acquisition Setup
# One-time configuration - user drags folders to define watch paths

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/user_config.json"

echo "============================================================"
echo "8825 ONBOARDING - TARGET SETUP"
echo "============================================================"
echo ""
echo "This will help 8825 learn where YOUR files live."
echo "Just drag folders from Finder into this terminal."
echo ""
read -p "Press Enter to begin..."
echo ""

# Function to clean up dragged path
clean_path() {
    # Remove quotes and trailing slashes
    echo "$1" | sed "s/^['\"]//;s/['\"]$//;s:/$::" | xargs
}

# Step 1: Screenshots
echo "============================================================"
echo "STEP 1: Desktop Screenshots"
echo "============================================================"
echo ""
echo "📸 Where do your desktop screenshots go?"
echo "   (Usually ~/Dropbox/Screenshots or ~/Desktop)"
echo ""
echo "Drag your Screenshots folder here and press Enter:"
read -r screenshots_input
screenshots_path=$(clean_path "$screenshots_input")

if [ ! -d "$screenshots_path" ]; then
    echo "❌ Error: Folder not found: $screenshots_path"
    exit 1
fi

echo "✓ Screenshots: $screenshots_path"
echo ""

# Step 2: Desktop Downloads
echo "============================================================"
echo "STEP 2: Desktop Downloads"
echo "============================================================"
echo ""
echo "📥 Where do desktop downloads go?"
echo "   (Usually ~/Downloads)"
echo ""
echo "Drag your Downloads folder here and press Enter:"
read -r downloads_input
downloads_path=$(clean_path "$downloads_input")

if [ ! -d "$downloads_path" ]; then
    echo "❌ Error: Folder not found: $downloads_path"
    exit 1
fi

echo "✓ Downloads: $downloads_path"
echo ""

# Step 3: Mobile Downloads (Cloud)
echo "============================================================"
echo "STEP 3: Mobile Downloads (Cloud Folder)"
echo "============================================================"
echo ""
echo "📱 Where do mobile downloads/uploads go?"
echo "   (e.g., ~/Dropbox/Camera Uploads or ~/Dropbox/Mobile)"
echo ""
echo "Drag your mobile cloud folder here (or press Enter to skip):"
read -r mobile_input

if [ -z "$mobile_input" ]; then
    mobile_path=""
    echo "⊘ Skipped mobile downloads"
else
    mobile_path=$(clean_path "$mobile_input")
    
    if [ ! -d "$mobile_path" ]; then
        echo "❌ Error: Folder not found: $mobile_path"
        exit 1
    fi
    
    echo "✓ Mobile: $mobile_path"
fi

echo ""

# Create config file
cat > "$CONFIG_FILE" <<EOF
{
  "user": "jh",
  "watch_paths": {
    "screenshots": "$screenshots_path",
    "downloads": "$downloads_path",
    "mobile": "$mobile_path"
  },
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "============================================================"
echo "✅ SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Watching:"
echo "  📸 Screenshots: $screenshots_path"
echo "  📥 Downloads: $downloads_path"
if [ -n "$mobile_path" ]; then
    echo "  📱 Mobile: $mobile_path"
fi
echo ""
echo "Config saved to: $CONFIG_FILE"
echo ""
echo "Next: Run ./start.sh to begin watching"
echo "============================================================"
