#!/bin/bash
# 8825 Registry Validator
# Checks registry and auto-updates if new components found

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "=== Registry Validation ==="
echo ""

# Check if registry exists
if [ ! -f "$REGISTRY" ]; then
    echo -e "${YELLOW}⚠️  Registry not found${NC}"
    echo "   This should not happen - registry should be created during setup"
    exit 1
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq not installed (needed for registry validation)${NC}"
    echo "   Run dependency check first"
    exit 1
fi

# Get current scripts from filesystem
echo "Scanning for scripts..."
current_scripts=$(find "$WORKSPACE_ROOT/INBOX_HUB" "$WORKSPACE_ROOT/8825_core" "$WORKSPACE_ROOT/users" \
    -type f \( -name "*.sh" -o -name "*.py" \) 2>/dev/null | \
    sed "s|$WORKSPACE_ROOT/||" | sort)

# Get registered scripts
registered_scripts=$(jq -r '.scripts[].path' "$REGISTRY" | sort)

# Find new scripts (in filesystem but not in registry)
new_scripts=$(comm -23 <(echo "$current_scripts") <(echo "$registered_scripts"))

if [ -n "$new_scripts" ]; then
    new_count=$(echo "$new_scripts" | wc -l | tr -d ' ')
    echo -e "${YELLOW}⚠️  Found $new_count new script(s)${NC}"
    echo ""
    
    # Auto-register each new script
    echo "Auto-registering..."
    registered_count=0
    echo "$new_scripts" | while read script; do
        if [ -n "$script" ]; then
            "$SCRIPT_DIR/auto_register.sh" "$script" 2>&1 | sed 's/^/   /'
            registered_count=$((registered_count + 1))
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅${NC} Registry updated with $new_count new script(s)"
    echo "   Run '8825 registry review' to refine auto-detected entries"
else
    echo -e "${GREEN}✅${NC} No new scripts detected"
fi

# Check registry freshness
last_updated=$(jq -r '.last_updated' "$REGISTRY")
echo -e "${GREEN}✅${NC} Registry last updated: $last_updated"

# Count registered components
script_count=$(jq -r '.scripts | length' "$REGISTRY")
daemon_count=$(jq -r '.daemons | length' "$REGISTRY")
path_count=$(jq -r '.critical_paths | keys | length' "$REGISTRY")

echo ""
echo "Registry contains:"
echo "  • $script_count scripts"
echo "  • $daemon_count daemons"
echo "  • $path_count critical paths"
echo ""
