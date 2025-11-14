#!/bin/bash
# 8825 Registry Update
# Manually update a registry entry

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: 8825 registry update <name> [options]"
    echo ""
    echo "Options:"
    echo "  --purpose \"description\"    Update purpose"
    echo "  --type <category>          Update type"
    echo "  --reviewed                 Mark as reviewed"
    echo "  --safe                     Mark as safe to run"
    echo ""
    echo "Examples:"
    echo "  8825 registry update sync_photos.sh --purpose \"Sync photos from iPhone\""
    echo "  8825 registry update sync_photos.sh --type sync"
    echo "  8825 registry update sync_photos.sh --reviewed"
    echo "  8825 registry update sync_photos.sh --safe"
    exit 1
fi

script_name="$1"
shift

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

# Check if script exists in registry
if ! jq -e --arg name "$script_name" '.scripts[] | select(.name == $name)' "$REGISTRY" > /dev/null 2>&1; then
    echo -e "${YELLOW}Script not found in registry: $script_name${NC}"
    exit 1
fi

# Parse options
while [ $# -gt 0 ]; do
    case "$1" in
        --purpose)
            new_purpose="$2"
            jq --arg name "$script_name" --arg purpose "$new_purpose" \
                '(.scripts[] | select(.name == $name) | .purpose) = $purpose' \
                "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
            echo -e "${GREEN}✅${NC} Updated purpose for $script_name"
            shift 2
            ;;
        --type)
            new_type="$2"
            jq --arg name "$script_name" --arg type "$new_type" \
                '(.scripts[] | select(.name == $name) | .type) = $type' \
                "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
            echo -e "${GREEN}✅${NC} Updated type for $script_name"
            shift 2
            ;;
        --reviewed)
            jq --arg name "$script_name" \
                '(.scripts[] | select(.name == $name) | .needs_review) = false' \
                "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
            echo -e "${GREEN}✅${NC} Marked $script_name as reviewed"
            shift
            ;;
        --safe)
            jq --arg name "$script_name" \
                '(.scripts[] | select(.name == $name) | .safe_to_run) = true' \
                "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
            echo -e "${GREEN}✅${NC} Marked $script_name as safe to run"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Update last_updated timestamp
jq --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.last_updated = $timestamp' \
    "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"

echo ""
