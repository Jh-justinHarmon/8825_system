#!/bin/bash
# Clean up and organize 8825_inbox folder

set -e

INBOX_DIR="$HOME/Downloads/8825_inbox"

echo "=== Organizing 8825_inbox ==="
echo ""

# Create proper structure
mkdir -p "$INBOX_DIR/pending"
mkdir -p "$INBOX_DIR/processing"
mkdir -p "$INBOX_DIR/completed"
mkdir -p "$INBOX_DIR/errors"
mkdir -p "$INBOX_DIR/archive"

# Move existing folders to archive
echo "Archiving old folders..."
[ -d "$INBOX_DIR/archive_old" ] && mv "$INBOX_DIR/archive_old" "$INBOX_DIR/archive/" 2>/dev/null || true
[ -d "$INBOX_DIR/Chat_Mining_Report_2025-11-08" ] && mv "$INBOX_DIR/Chat_Mining_Report_2025-11-08" "$INBOX_DIR/archive/" 2>/dev/null || true
[ -d "$INBOX_DIR/Screengrabs" ] && mv "$INBOX_DIR/Screengrabs" "$INBOX_DIR/archive/" 2>/dev/null || true

# Move loose files to pending
echo "Moving loose files to pending..."
cd "$INBOX_DIR"
find . -maxdepth 1 -type f \( -name "*.json" -o -name "*.txt" -o -name "*.md" \) -exec sh -c 'mv "$1" pending/ && echo "  ✓ $(basename "$1") → pending/"' _ {} \;

echo ""
echo "=== Cleanup Complete ==="
echo ""
echo "Structure:"
echo "  pending/    - New files (ready to process)"
echo "  processing/ - Currently being processed"
echo "  completed/  - Successfully processed"
echo "  errors/     - Failed validation"
echo "  archive/    - Old folders"
echo ""
echo "Next: Run ./sync_and_process.sh to process pending files"
