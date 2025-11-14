#!/bin/bash
# Unified File Watcher
# Watches configured input locations and processes files

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONFIG_FILE="$SCRIPT_DIR/../sandbox_target_acquisition/user_config.json"
PROCESSOR="$SCRIPT_DIR/unified_processor.py"
QUEUE_FILE="$SCRIPT_DIR/processing_queue.txt"
LOG_FILE="$SCRIPT_DIR/logs/watcher.log"

# Ensure directories exist
mkdir -p "$SCRIPT_DIR/logs"
touch "$QUEUE_FILE"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    log "❌ Config not found: $CONFIG_FILE"
    log "Run setup first: cd ../sandbox_target_acquisition && ./setup_v3.sh"
    exit 1
fi

# Read paths from config
DESKTOP_DOWNLOADS=$(jq -r '.inputs.desktop_downloads' "$CONFIG_FILE")
ICLOUD_DOWNLOADS=$(jq -r '.inputs.icloud_downloads' "$CONFIG_FILE")
SCREENSHOTS=$(jq -r '.inputs.screenshots' "$CONFIG_FILE")

log "============================================================"
log "🚀 Starting Unified File Watcher"
log "============================================================"
log ""
log "Watching:"
log "  📥 Desktop Downloads: $DESKTOP_DOWNLOADS"
log "  📱 iCloud Downloads: $ICLOUD_DOWNLOADS"
log "  📸 Screenshots: $SCREENSHOTS"
log ""

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    log "❌ fswatch not installed"
    log "Install with: brew install fswatch"
    exit 1
fi

# Start watching
fswatch -0 "$DESKTOP_DOWNLOADS" "$ICLOUD_DOWNLOADS" "$SCREENSHOTS" | while read -d "" file; do
    # Skip hidden files and directories
    basename=$(basename "$file")
    if [[ "$basename" == .* ]] || [ -d "$file" ]; then
        continue
    fi
    
    # Skip if already in queue
    if grep -Fxq "$file" "$QUEUE_FILE" 2>/dev/null; then
        continue
    fi
    
    # Add to queue
    echo "$file" >> "$QUEUE_FILE"
    log "📥 Detected: $basename"
    
    # Process immediately
    python3 "$PROCESSOR" "$file" &
done
