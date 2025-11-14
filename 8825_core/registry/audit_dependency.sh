#!/bin/bash
# 8825 Audit Dependency
# Shows what requires a specific dependency

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: 8825 audit dependency <name>"
    echo "Example: 8825 audit dependency watchdog"
    exit 1
fi

dep="$1"

echo ""
echo -e "${BLUE}=== Dependency: $dep ===${NC}"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

# Check if dependency exists in registry
dep_info=$(jq -r --arg dep "$dep" '.system_dependencies[$dep]' "$REGISTRY")

if [ "$dep_info" = "null" ]; then
    echo -e "${YELLOW}Dependency not found in registry${NC}"
    echo ""
    echo "Registered dependencies:"
    jq -r '.system_dependencies | keys[]' "$REGISTRY" | sed 's/^/  • /'
    echo ""
    exit 1
fi

# Get dependency details
dep_type=$(echo "$dep_info" | jq -r '.type // "system"')
dep_check=$(echo "$dep_info" | jq -r '.check')
dep_install=$(echo "$dep_info" | jq -r '.install')
dep_version=$(echo "$dep_info" | jq -r '.version // "any"')

echo -e "${CYAN}Type:${NC} $dep_type"

# Check if installed
if eval "$dep_check" > /dev/null 2>&1; then
    echo -e "${CYAN}Status:${NC} ${GREEN}✅ Installed${NC}"
    
    # Try to get version for some common tools
    if command -v "$dep" &> /dev/null; then
        case "$dep" in
            python3)
                version=$($dep --version 2>&1 | head -1)
                echo -e "${CYAN}Version:${NC} $version"
                ;;
            jq)
                version=$($dep --version 2>&1)
                echo -e "${CYAN}Version:${NC} $version"
                ;;
        esac
    fi
else
    echo -e "${CYAN}Status:${NC} ${RED}❌ Not installed${NC}"
fi

if [ "$dep_version" != "any" ]; then
    echo -e "${CYAN}Required version:${NC} $dep_version"
fi

echo ""
echo -e "${CYAN}Installation:${NC}"
echo "  Check: $dep_check"
echo "  Install: $dep_install"

# Find components that require this dependency
echo ""
echo -e "${CYAN}Required by:${NC}"

# Check scripts
script_count=0
while IFS= read -r script_name; do
    if [ -n "$script_name" ]; then
        script_count=$((script_count + 1))
        script_type=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .type' "$REGISTRY")
        script_purpose=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .purpose' "$REGISTRY")
        
        echo ""
        echo -e "  ${GREEN}$script_count. $script_name${NC} (script)"
        echo "     • Type: $script_type"
        echo "     • Purpose: $script_purpose"
    fi
done < <(jq -r --arg dep "$dep" '.scripts[] | select(.dependencies[]? == $dep) | .name' "$REGISTRY")

# Check daemons
daemon_count=0
while IFS= read -r daemon_name; do
    if [ -n "$daemon_name" ]; then
        daemon_count=$((daemon_count + 1))
        daemon_purpose=$(jq -r --arg name "$daemon_name" '.daemons[] | select(.name == $name) | .purpose' "$REGISTRY")
        
        # Check if running
        if ps aux | grep -v grep | grep "$daemon_name" > /dev/null; then
            status="${GREEN}RUNNING${NC}"
        else
            status="${YELLOW}STOPPED${NC}"
        fi
        
        echo ""
        echo -e "  ${GREEN}$((script_count + daemon_count)). $daemon_name${NC} (daemon)"
        echo "     • Purpose: $daemon_purpose"
        echo -e "     • Status: $status"
    fi
done < <(jq -r --arg dep "$dep" '.daemons[] | select(.dependencies[]? == $dep) | .name' "$REGISTRY")

total_count=$((script_count + daemon_count))

if [ $total_count -eq 0 ]; then
    echo "  No components require this dependency"
    echo "  (May be a transitive dependency or unused)"
fi

# Impact analysis
echo ""
echo -e "${CYAN}Impact Analysis:${NC}"

if [ $total_count -eq 0 ]; then
    echo -e "  ${GREEN}LOW${NC} - No registered components depend on this"
elif [ $daemon_count -gt 0 ]; then
    echo -e "  ${RED}HIGH${NC} - $daemon_count daemon(s) will fail if removed"
elif [ $total_count -gt 3 ]; then
    echo -e "  ${YELLOW}MEDIUM${NC} - $total_count scripts depend on this"
else
    echo -e "  ${YELLOW}LOW-MEDIUM${NC} - $total_count script(s) depend on this"
fi

# Recommendations
echo ""
echo -e "${CYAN}Recommendations:${NC}"

if [ $daemon_count -gt 0 ]; then
    echo -e "  ${RED}❌ DO NOT REMOVE${NC}"
    echo "  Critical for daemon infrastructure"
elif [ $total_count -gt 3 ]; then
    echo -e "  ${YELLOW}⚠️  CAUTION${NC}"
    echo "  Many scripts depend on this. Test thoroughly if updating."
elif [ $total_count -gt 0 ]; then
    echo "  Safe to update, but test affected scripts"
else
    echo "  Safe to remove if truly unused"
fi

# Alternative actions
if eval "$dep_check" > /dev/null 2>&1; then
    echo ""
    echo -e "${CYAN}Alternative Actions:${NC}"
    echo "  To update: $dep_install"
    if [ $total_count -gt 0 ]; then
        echo "  Then test: 8825 health"
    fi
fi

echo ""
