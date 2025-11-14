#!/bin/bash
# Complete workflow: Process photos and copy JSON to clipboard

cd "$(dirname "$0")"

echo "🔍 Processing sticky note photos..."
python3 vision_sticky_processor.py

if [ $? -eq 0 ]; then
    echo ""
    echo "📋 Copying JSON to clipboard..."
    cat "$HOME/Downloads/sticky_notes_vision.json" | pbcopy
    
    echo "✅ Done!"
    echo ""
    echo "Next steps:"
    echo "1. Open your FigJam board"
    echo "2. Run: Plugins → 8825 Sticky Importer"
    echo "3. Press Cmd+V to paste"
    echo "4. Click 'Import Stickies'"
else
    echo "❌ Processing failed"
    exit 1
fi
