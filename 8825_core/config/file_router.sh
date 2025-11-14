#!/bin/bash
# File Router - Shell helper library
# Source this in shell scripts to get consistent file paths

ROUTER_CONFIG="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/config/file_router.json"

# Get root path
get_router_root() {
    jq -r '.root' "$ROUTER_CONFIG"
}

# Get destination for a project
get_router_destination() {
    local project="$1"
    local root=$(jq -r '.root' "$ROUTER_CONFIG")
    local dest=$(jq -r --arg proj "$project" '.destinations[$proj] // .folders.unknown' "$ROUTER_CONFIG")
    echo "$root/$dest"
}

# Get intake folder
get_router_intake() {
    local root=$(jq -r '.root' "$ROUTER_CONFIG")
    local intake=$(jq -r '.folders.intake' "$ROUTER_CONFIG")
    echo "$root/$intake"
}

# Get unknown/misc folder
get_router_unknown() {
    local root=$(jq -r '.root' "$ROUTER_CONFIG")
    local unknown=$(jq -r '.folders.unknown' "$ROUTER_CONFIG")
    echo "$root/$unknown"
}

# Get case convention
get_router_case() {
    local file_type="$1"
    jq -r ".file_conventions.\"$file_type\"" "$ROUTER_CONFIG"
}

# Get shareable root
get_router_shareable() {
    jq -r '.shareable.mirror_root' "$ROUTER_CONFIG"
}

# List all projects
get_router_projects() {
    jq -r '.destinations | keys[]' "$ROUTER_CONFIG"
}
