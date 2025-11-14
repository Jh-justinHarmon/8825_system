#!/bin/bash
# Easier setup - just paste the paths

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/user_config.json"

echo "============================================================"
echo "8825 SETUP (Easy Mode)"
echo "============================================================"
echo ""
echo "Just copy/paste the full paths (or drag folders)"
echo "Press Ctrl+C anytime to cancel and restart"
echo ""

# Screenshots
while true; do
    echo "📸 Screenshots folder path:"
    echo "   Example: /Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Screenshots"
    echo ""
    read -r screenshots_input
    screenshots_path=$(echo "$screenshots_input" | sed "s/^['\"]//;s/['\"]$//;s:/$::" | xargs)
    
    if [ -d "$screenshots_path" ]; then
        echo "✓ Found: $screenshots_path"
        break
    else
        echo "❌ Not found. Try again (or Ctrl+C to quit)"
        echo ""
    fi
done

echo ""

# Downloads
while true; do
    echo "📥 Downloads folder path:"
    echo "   Example: /Users/justinharmon/Downloads"
    echo ""
    read -r downloads_input
    downloads_path=$(echo "$downloads_input" | sed "s/^['\"]//;s/['\"]$//;s:/$::" | xargs)
    
    if [ -d "$downloads_path" ]; then
        echo "✓ Found: $downloads_path"
        break
    else
        echo "❌ Not found. Try again (or Ctrl+C to quit)"
        echo ""
    fi
done

echo ""

# Mobile (optional)
echo "📱 Mobile folder path (or just press Enter to skip):"
echo "   Example: /Users/justinharmon/Dropbox/Camera Uploads"
echo ""
read -r mobile_input

if [ -z "$mobile_input" ]; then
    mobile_path=""
    echo "⊘ Skipped"
else
    mobile_path=$(echo "$mobile_input" | sed "s/^['\"]//;s/['\"]$//;s:/$::" | xargs)
    if [ -d "$mobile_path" ]; then
        echo "✓ Found: $mobile_path"
    else
        echo "⚠️  Not found, skipping mobile folder"
        mobile_path=""
    fi
fi

# Save config
cat > "$CONFIG_FILE" <<EOF
{
  "user": "jh",
  "watch_paths": {
    "screenshots": "$screenshots_path",
    "downloads": "$downloads_path",
    "mobile": "$mobile_path"
  },
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo ""
echo "============================================================"
echo "✅ SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Watching:"
echo "  📸 $screenshots_path"
echo "  📥 $downloads_path"
[ -n "$mobile_path" ] && echo "  📱 $mobile_path"
echo ""
echo "Next: ./start.sh"
echo "============================================================"
