#!/bin/bash
# OCR Latest Screenshot
# Copies latest screenshot to /tmp for easy OCR access (avoids space issues in paths)

SCREENSHOTS_DIR="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Screenshots"
TEMP_PATH="/tmp/latest_screenshot.png"

if [ ! -d "$SCREENSHOTS_DIR" ]; then
    echo "❌ Screenshots directory not found: $SCREENSHOTS_DIR"
    exit 1
fi

# Get latest screenshot
cd "$SCREENSHOTS_DIR"
latest=$(ls -1t *.png 2>/dev/null | head -1)

if [ -z "$latest" ]; then
    echo "❌ No screenshots found"
    exit 1
fi

# Copy to temp location
cp "$latest" "$TEMP_PATH"

echo "✓ Latest screenshot ready for OCR"
echo ""
echo "File: $latest"
echo "Path: $TEMP_PATH"
echo ""
echo "Cascade can now read this file without path issues:"
echo "  read_file /tmp/latest_screenshot.png"
