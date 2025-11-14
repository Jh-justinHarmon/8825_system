#!/bin/bash
# Sync Brain Transport to BOTH Downloads locations
# So it's always available everywhere

SOURCE="$HOME/Documents/8825_BRAIN_TRANSPORT.json"
LOCAL_DEST="$HOME/Downloads/0-8825_BRAIN_TRANSPORT.json"
ICLOUD_DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Downloads/0-8825_BRAIN_TRANSPORT.json"

# Copy to both locations
cp "$SOURCE" "$LOCAL_DEST"
cp "$SOURCE" "$ICLOUD_DEST"

echo "✅ BRAIN_TRANSPORT synced to:"
echo "   - Local Downloads"
echo "   - iCloud Downloads"
