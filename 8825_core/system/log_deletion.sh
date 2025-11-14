#!/bin/bash
# Log Deletion Helper
# Adds entry to deleted items log before deleting

LOG_FILE="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/migrations/deleted_items_log.json"

log_deletion() {
    local item_path="$1"
    local reason="$2"
    local confidence="${3:-high}"
    
    # Get git commit if in repo
    local git_commit=$(cd "$(dirname "$item_path")" 2>/dev/null && git rev-parse HEAD 2>/dev/null || echo "not in git")
    
    # Get item type and size
    local item_type="unknown"
    local item_size="0"
    if [ -f "$item_path" ]; then
        item_type="file"
        item_size=$(ls -lh "$item_path" | awk '{print $5}')
    elif [ -d "$item_path" ]; then
        item_type="directory"
        item_size=$(du -sh "$item_path" | awk '{print $1}')
    fi
    
    # Create entry
    local entry=$(cat << EOF
  {
    "deleted_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "path": "$item_path",
    "type": "$item_type",
    "size": "$item_size",
    "reason": "$reason",
    "confidence": "$confidence",
    "git_commit": "$git_commit",
    "recoverable": "yes"
  }
EOF
)
    
    # Add to log (append to entries array)
    # Read current log, add entry, write back
    python3 << PYTHON
import json

with open("$LOG_FILE", "r") as f:
    log = json.load(f)

entry = $entry

log["entries"].append(entry)

with open("$LOG_FILE", "w") as f:
    json.dump(log, f, indent=2)

print(f"✅ Logged deletion: $item_path")
PYTHON
}

# If called directly (not sourced)
if [ "$0" = "${BASH_SOURCE[0]}" ]; then
    if [ $# -lt 2 ]; then
        echo "Usage: log_deletion.sh <path> <reason> [confidence]"
        echo "Example: log_deletion.sh /path/to/file 'Duplicate of X' high"
        exit 1
    fi
    
    log_deletion "$1" "$2" "${3:-high}"
fi
