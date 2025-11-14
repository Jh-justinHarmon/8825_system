#!/bin/bash
# Auto-import sticky notes to FigJam
# This script copies the JSON to clipboard so you can paste it

JSON_FILE="$HOME/Downloads/sticky_notes_vision.json"

if [ ! -f "$JSON_FILE" ]; then
    echo "❌ Error: $JSON_FILE not found"
    echo "Run: python3 vision_sticky_processor.py first"
    exit 1
fi

echo "📋 Copying JSON to clipboard..."
cat "$JSON_FILE" | pbcopy

echo "✅ JSON copied to clipboard!"
echo ""
echo "Now in Figma:"
echo "1. Run the 8825 Sticky Importer plugin"
echo "2. Press Cmd+V to paste"
echo "3. Click 'Import Stickies'"
echo ""
echo "Or just use the 'Load File' button in the plugin!"
