#!/bin/bash
# 8825 Audit Component
# Shows detailed information about a specific component

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: 8825 audit component <name>"
    echo "Example: 8825 audit component downloads_sync"
    exit 1
fi

component="$1"

echo ""
echo -e "${BLUE}=== Component: $component ===${NC}"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

# Check if it's a daemon
daemon_data=$(jq -r --arg name "$component" '.daemons[] | select(.name == $name)' "$REGISTRY")

if [ -n "$daemon_data" ]; then
    # It's a daemon
    echo -e "${CYAN}Type:${NC} Daemon"
    
    # Get details
    path=$(echo "$daemon_data" | jq -r '.path')
    purpose=$(echo "$daemon_data" | jq -r '.purpose')
    should_run=$(echo "$daemon_data" | jq -r '.should_be_running')
    log_file=$(echo "$daemon_data" | jq -r '.log_file')
    started_by=$(echo "$daemon_data" | jq -r '.started_by')
    
    # Check if running
    if ps aux | grep -v grep | grep "$component" > /dev/null; then
        echo -e "${CYAN}Status:${NC} ${GREEN}RUNNING${NC}"
        pid=$(ps aux | grep -v grep | grep "$component" | awk '{print $2}')
        echo -e "${CYAN}PID:${NC} $pid"
    else
        echo -e "${CYAN}Status:${NC} ${YELLOW}STOPPED${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}Purpose:${NC}"
    echo "  $purpose"
    
    echo ""
    echo -e "${CYAN}Location:${NC}"
    echo "  $path"
    
    # What it touches
    echo ""
    echo -e "${CYAN}What it touches:${NC}"
    echo "$daemon_data" | jq -r '.touches[]' | while read -r touch; do
        echo "  • $touch"
    done
    
    # Exclusions
    exclusions=$(echo "$daemon_data" | jq -r '.excludes[]?' 2>/dev/null)
    if [ -n "$exclusions" ]; then
        echo ""
        echo -e "${CYAN}Exclusions:${NC}"
        echo "$exclusions" | tr '\n' ', ' | sed 's/,$//' | fold -w 70 -s | sed 's/^/  /'
    fi
    
    # Dependencies
    echo ""
    echo -e "${CYAN}Dependencies:${NC}"
    echo "$daemon_data" | jq -r '.dependencies[]' | while read -r dep; do
        # Check if installed
        check_cmd=$(jq -r --arg dep "$dep" '.system_dependencies[$dep].check' "$REGISTRY")
        if eval "$check_cmd" > /dev/null 2>&1; then
            echo -e "  • $dep ${GREEN}✅ installed${NC}"
        else
            echo -e "  • $dep ${YELLOW}⚠️  missing${NC}"
        fi
    done
    
    # How to control it
    echo ""
    echo -e "${CYAN}Control:${NC}"
    echo "  Started by: $started_by"
    if [ -n "$log_file" ]; then
        echo "  Log file: $log_file"
    fi
    
    echo ""
    echo -e "${CYAN}Commands:${NC}"
    if [ -n "$started_by" ]; then
        echo "  To start: cd $(dirname $started_by) && bash $(basename $started_by)"
    fi
    echo "  To stop: pkill -f $component"
    if [ -n "$log_file" ]; then
        echo "  To monitor: tail -f $log_file"
    fi
    
    # Safety check
    echo ""
    echo -e "${CYAN}Safe to start:${NC}"
    if [ "$should_run" = "true" ]; then
        echo -e "  ${GREEN}YES${NC} (configured to run)"
    else
        echo -e "  ${YELLOW}REVIEW${NC} (not configured to run by default)"
    fi
    
elif [ -n "$(jq -r --arg name "$component" '.scripts[] | select(.name == $name)' "$REGISTRY")" ]; then
    # It's a script
    script_data=$(jq -r --arg name "$component" '.scripts[] | select(.name == $name)' "$REGISTRY")
    
    echo -e "${CYAN}Type:${NC} Script"
    
    # Get details
    path=$(echo "$script_data" | jq -r '.path')
    purpose=$(echo "$script_data" | jq -r '.purpose')
    script_type=$(echo "$script_data" | jq -r '.type')
    safe=$(echo "$script_data" | jq -r '.safe_to_run')
    modified=$(echo "$script_data" | jq -r '.last_modified')
    
    if [ "$safe" = "true" ]; then
        echo -e "${CYAN}Status:${NC} ${GREEN}Safe to run${NC}"
    else
        echo -e "${CYAN}Status:${NC} ${YELLOW}Review needed${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}Purpose:${NC}"
    echo "  $purpose"
    
    echo ""
    echo -e "${CYAN}Location:${NC}"
    echo "  $path"
    
    echo ""
    echo -e "${CYAN}Category:${NC} $script_type"
    echo -e "${CYAN}Last modified:${NC} $modified"
    
    # What it touches
    touches=$(echo "$script_data" | jq -r '.touches[]?' 2>/dev/null)
    if [ -n "$touches" ]; then
        echo ""
        echo -e "${CYAN}What it touches:${NC}"
        echo "$touches" | while read -r touch; do
            echo "  • $touch"
        done
    fi
    
    # Exclusions
    exclusions=$(echo "$script_data" | jq -r '.excludes[]?' 2>/dev/null)
    if [ -n "$exclusions" ]; then
        echo ""
        echo -e "${CYAN}Exclusions:${NC}"
        echo "$exclusions" | tr '\n' ', ' | sed 's/,$//' | fold -w 70 -s | sed 's/^/  /'
    fi
    
    # Dependencies
    deps=$(echo "$script_data" | jq -r '.dependencies[]?' 2>/dev/null)
    if [ -n "$deps" ]; then
        echo ""
        echo -e "${CYAN}Dependencies:${NC}"
        echo "$deps" | while read -r dep; do
            # Check if installed
            check_cmd=$(jq -r --arg dep "$dep" '.system_dependencies[$dep].check' "$REGISTRY" 2>/dev/null)
            if [ -n "$check_cmd" ] && [ "$check_cmd" != "null" ]; then
                if eval "$check_cmd" > /dev/null 2>&1; then
                    echo -e "  • $dep ${GREEN}✅ installed${NC}"
                else
                    echo -e "  • $dep ${YELLOW}⚠️  missing${NC}"
                fi
            else
                echo "  • $dep"
            fi
        done
    fi
    
    # Called by
    called_by=$(echo "$script_data" | jq -r '.called_by[]?' 2>/dev/null)
    if [ -n "$called_by" ]; then
        echo ""
        echo -e "${CYAN}Called by:${NC}"
        echo "$called_by" | while read -r caller; do
            echo "  • $caller"
        done
    fi
    
    # How to run
    echo ""
    echo -e "${CYAN}To run:${NC}"
    echo "  bash $path"
    
else
    echo -e "${YELLOW}Component not found in registry${NC}"
    echo ""
    echo "Available components:"
    echo ""
    echo "Daemons:"
    jq -r '.daemons[].name' "$REGISTRY" | sed 's/^/  • /'
    echo ""
    echo "Scripts:"
    jq -r '.scripts[].name' "$REGISTRY" | sed 's/^/  • /'
    exit 1
fi

echo ""
