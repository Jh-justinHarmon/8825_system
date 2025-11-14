#!/bin/bash
# 8825 Audit Path
# Shows everything that touches a specific path

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: 8825 audit path <path>"
    echo "Example: 8825 audit path ~/Downloads"
    exit 1
fi

# Normalize path (keep both versions for matching)
path_input="$1"
path_expanded="${path_input/#\~/$HOME}"
path_tilde="$path_input"

# If input doesn't have ~, create tilde version
if [[ "$path_input" == "$HOME"* ]]; then
    path_tilde="~${path_input#$HOME}"
fi

echo ""
echo -e "${BLUE}=== Audit: $path_tilde ===${NC}"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

# Find scripts that touch this path
echo -e "${CYAN}Scripts:${NC}"
script_count=0
while IFS= read -r script_name; do
    if [ -n "$script_name" ]; then
        script_count=$((script_count + 1))
        
        # Get script details
        script_path=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .path' "$REGISTRY")
        script_type=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .type' "$REGISTRY")
        script_purpose=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .purpose' "$REGISTRY")
        script_safe=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .safe_to_run' "$REGISTRY")
        script_modified=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .last_modified' "$REGISTRY")
        
        # Get exclusions if they exist
        exclusions=$(jq -r --arg name "$script_name" '.scripts[] | select(.name == $name) | .excludes[]?' "$REGISTRY" 2>/dev/null | tr '\n' ', ' | sed 's/,$//')
        
        echo ""
        echo -e "  ${GREEN}$script_count. $script_name${NC}"
        echo "     • Type: $script_type"
        echo "     • Purpose: $script_purpose"
        echo "     • Path: $script_path"
        echo "     • Last modified: $script_modified"
        if [ "$script_safe" = "true" ]; then
            echo -e "     • Safe to run: ${GREEN}YES${NC}"
        else
            echo -e "     • Safe to run: ${YELLOW}REVIEW NEEDED${NC}"
        fi
        if [ -n "$exclusions" ]; then
            echo "     • Excludes: $exclusions"
        fi
    fi
done < <(jq -r --arg path "$path_tilde" '.scripts[] | select(.touches[]? | contains($path)) | .name' "$REGISTRY")

if [ $script_count -eq 0 ]; then
    echo "  No scripts touch this path"
fi

# Find daemons that touch this path
echo ""
echo -e "${CYAN}Daemons:${NC}"
daemon_count=0
while IFS= read -r daemon_name; do
    if [ -n "$daemon_name" ]; then
        daemon_count=$((daemon_count + 1))
        
        # Get daemon details
        daemon_path=$(jq -r --arg name "$daemon_name" '.daemons[] | select(.name == $name) | .path' "$REGISTRY")
        daemon_purpose=$(jq -r --arg name "$daemon_name" '.daemons[] | select(.name == $name) | .purpose' "$REGISTRY")
        daemon_should_run=$(jq -r --arg name "$daemon_name" '.daemons[] | select(.name == $name) | .should_be_running' "$REGISTRY")
        
        # Check if actually running
        if ps aux | grep -v grep | grep "$daemon_name" > /dev/null; then
            status="${GREEN}RUNNING${NC}"
        else
            status="${YELLOW}STOPPED${NC}"
        fi
        
        # Get exclusions
        exclusions=$(jq -r --arg name "$daemon_name" '.daemons[] | select(.name == $name) | .excludes[]?' "$REGISTRY" 2>/dev/null | tr '\n' ', ' | sed 's/,$//')
        
        echo ""
        echo -e "  ${GREEN}• $daemon_name${NC}"
        echo -e "    - Status: $status"
        echo "    - Purpose: $daemon_purpose"
        echo "    - Path: $daemon_path"
        if [ "$daemon_should_run" = "true" ]; then
            echo "    - Should be running: YES"
        else
            echo "    - Should be running: NO"
        fi
        if [ -n "$exclusions" ]; then
            echo "    - Excludes: $exclusions"
        fi
    fi
done < <(jq -r --arg path "$path_tilde" '.daemons[] | select(.touches[]? | contains($path)) | .name' "$REGISTRY")

if [ $daemon_count -eq 0 ]; then
    echo "  No daemons touch this path"
fi

# Check for conflicts (different exclusion patterns)
echo ""
echo -e "${CYAN}Conflict Analysis:${NC}"

# Get all unique exclusion patterns for this path
all_exclusions=$(jq -r --arg path "$path_tilde" '
    (.scripts[] | select(.touches[]? | contains($path)) | .excludes[]?),
    (.daemons[] | select(.touches[]? | contains($path)) | .excludes[]?)
' "$REGISTRY" 2>/dev/null | sort -u)

if [ -n "$all_exclusions" ]; then
    # Check if all components have the same exclusions
    script_exclusions=$(jq -r --arg path "$path_tilde" '.scripts[] | select(.touches[]? | contains($path)) | .excludes' "$REGISTRY" 2>/dev/null | sort -u | wc -l)
    daemon_exclusions=$(jq -r --arg path "$path_tilde" '.daemons[] | select(.touches[]? | contains($path)) | .excludes' "$REGISTRY" 2>/dev/null | sort -u | wc -l)
    
    total_patterns=$((script_exclusions + daemon_exclusions))
    
    if [ $total_patterns -le 1 ]; then
        echo -e "  ${GREEN}✅ No conflicts detected${NC}"
        echo "  All components use matching exclusion patterns"
    else
        echo -e "  ${YELLOW}⚠️  Different exclusion patterns detected${NC}"
        echo "  Review components to ensure coordination"
    fi
else
    echo "  No exclusion patterns defined"
fi

# Summary
echo ""
echo -e "${CYAN}Summary:${NC}"
total_touchpoints=$((script_count + daemon_count))
echo "  • Total touchpoints: $total_touchpoints"
echo "  • Scripts: $script_count"
echo "  • Daemons: $daemon_count"

if [ $total_touchpoints -gt 5 ]; then
    echo -e "  • Risk level: ${YELLOW}MEDIUM${NC} (many touchpoints)"
elif [ $daemon_count -gt 0 ]; then
    echo -e "  • Risk level: ${YELLOW}MEDIUM${NC} (daemon involved)"
else
    echo -e "  • Risk level: ${GREEN}LOW${NC}"
fi

echo ""
