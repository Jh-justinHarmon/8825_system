#!/bin/bash
# Unified Scan - Process Downloads + Screenshots together
# Syncs screenshots first, then runs progressive router

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 Syncing screenshots from Dropbox..."
"$SCRIPT_DIR/sync_screenshots.sh"

echo ""
echo "📊 Running progressive router (Downloads + Screenshots)..."
python3 "$SCRIPT_DIR/progressive_router.py" scan --screenshots "$@"
