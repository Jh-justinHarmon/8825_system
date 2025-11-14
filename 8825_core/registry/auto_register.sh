#!/bin/bash
# 8825 Auto-Register Script
# Automatically registers a new script in the registry

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

if [ -z "$1" ]; then
    echo "Usage: auto_register.sh <script_path>"
    exit 1
fi

script_path="$1"
script_name=$(basename "$script_path")

# Check if already registered
if jq -e --arg name "$script_name" '.scripts[] | select(.name == $name)' "$REGISTRY" > /dev/null 2>&1; then
    echo "Already registered: $script_name"
    exit 0
fi

# Detect script type
if [[ $script_path == *.py ]]; then
    lang="python"
elif [[ $script_path == *.sh ]]; then
    lang="bash"
else
    lang="unknown"
fi

# Extract dependencies (heuristics)
deps=()

if [ -f "$WORKSPACE_ROOT/$script_path" ]; then
    file_content=$(cat "$WORKSPACE_ROOT/$script_path")
    
    # Python dependencies
    if [[ $lang == "python" ]]; then
        if echo "$file_content" | grep -q "import watchdog"; then
            deps+=("watchdog")
        fi
        if echo "$file_content" | grep -q "import.*google"; then
            deps+=("python3")
        fi
        if ! echo "${deps[@]}" | grep -q "python3"; then
            deps+=("python3")
        fi
    fi
    
    # Bash dependencies
    if [[ $lang == "bash" ]]; then
        deps+=("bash")
        
        if echo "$file_content" | grep -q "rsync"; then
            deps+=("rsync")
        fi
        if echo "$file_content" | grep -q "jq"; then
            deps+=("jq")
        fi
    fi
    
    # Detect purpose from filename and comments
    purpose="Auto-detected"
    category="unknown"
    
    # Category from filename
    if [[ $script_name == *sync* ]]; then
        category="sync"
        purpose="Sync script"
    elif [[ $script_name == *cleanup* ]]; then
        category="cleanup"
        purpose="Cleanup script"
    elif [[ $script_name == *process* ]]; then
        category="processing"
        purpose="Processing script"
    elif [[ $script_name == *audit* ]]; then
        category="audit"
        purpose="Audit tool"
    elif [[ $script_name == *check* ]]; then
        category="health"
        purpose="Health check script"
    elif [[ $script_name == *test* ]]; then
        category="test"
        purpose="Test script"
    elif [[ $script_name == *server* ]]; then
        category="service"
        purpose="Server/service script"
    fi
    
    # Try to extract purpose from first comment
    first_comment=$(echo "$file_content" | grep -m1 "^#" | sed 's/^# *//' | head -c 100)
    if [ -n "$first_comment" ] && [ "$first_comment" != "!/bin/bash" ] && [ "$first_comment" != "!/usr/bin/env python" ]; then
        purpose="$first_comment"
    fi
    
    # Detect what it touches
    touches=()
    if echo "$file_content" | grep -q "~/Downloads"; then
        touches+=("~/Downloads")
    fi
    if echo "$file_content" | grep -q "~/Desktop"; then
        touches+=("~/Desktop")
    fi
    if echo "$file_content" | grep -q "8825_inbox"; then
        touches+=("~/Downloads/8825_inbox")
    fi
    if echo "$file_content" | grep -q "iCloud.*Downloads"; then
        touches+=("~/Library/Mobile Documents/com~apple~CloudDocs/Downloads")
    fi
fi

# Build JSON for new entry
new_entry=$(jq -n \
    --arg name "$script_name" \
    --arg path "$script_path" \
    --arg type "$category" \
    --arg purpose "$purpose" \
    --argjson deps "$(printf '%s\n' "${deps[@]}" | jq -R . | jq -s .)" \
    --argjson touches "$(printf '%s\n' "${touches[@]}" | jq -R . | jq -s .)" \
    --arg added "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{
        name: $name,
        path: $path,
        type: $type,
        purpose: $purpose,
        dependencies: $deps,
        touches: $touches,
        auto_registered: true,
        needs_review: true,
        last_modified: $added,
        safe_to_run: false
    }')

# Add to registry
jq --argjson entry "$new_entry" '.scripts += [$entry]' "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"

# Update last_updated timestamp
jq --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.last_updated = $timestamp' "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"

echo "✅ Registered: $script_name"
echo "   Type: $category"
echo "   Purpose: $purpose"
if [ ${#deps[@]} -gt 0 ]; then
    echo "   Dependencies: ${deps[*]}"
fi
if [ ${#touches[@]} -gt 0 ]; then
    echo "   Touches: ${touches[*]}"
fi
echo "   ⚠️  Needs review - run: 8825 registry review"
