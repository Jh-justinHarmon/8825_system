#!/bin/bash
# 8825 Impact Analysis
# Predicts consequences of proposed changes

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REGISTRY="$SCRIPT_DIR/SYSTEM_REGISTRY.json"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: 8825 impact <change_description>"
    echo ""
    echo "Examples:"
    echo "  8825 impact \"add *.png to IMG_ exclusions\""
    echo "  8825 impact \"start downloads_sync daemon\""
    echo "  8825 impact \"remove watchdog package\""
    echo "  8825 impact \"modify sync_downloads_folders.sh\""
    exit 1
fi

change_description="$*"

echo ""
echo -e "${BLUE}=== Impact Analysis ===${NC}"
echo ""
echo "Change: $change_description"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

# Parse change description (basic pattern matching)
change_type="unknown"
target=""
risk_level="UNKNOWN"
affected_count=0

# Detect change type
if echo "$change_description" | grep -qi "start.*daemon\|run.*daemon"; then
    change_type="start_daemon"
    target=$(echo "$change_description" | grep -oE "[a-z_]+_sync|[a-z_]+_daemon" | head -1)
elif echo "$change_description" | grep -qi "stop.*daemon\|kill.*daemon"; then
    change_type="stop_daemon"
    target=$(echo "$change_description" | grep -oE "[a-z_]+_sync|[a-z_]+_daemon" | head -1)
elif echo "$change_description" | grep -qi "remove.*package\|uninstall\|delete.*dependency"; then
    change_type="remove_dependency"
    target=$(echo "$change_description" | grep -oE "watchdog|jq|rsync|python3|bash" | head -1)
elif echo "$change_description" | grep -qi "add.*exclusion\|exclude"; then
    change_type="add_exclusion"
    target=$(echo "$change_description" | grep -oE "\*\.[a-z]+|[a-z_]+\*" | head -1)
elif echo "$change_description" | grep -qiE "modify|change|edit|update"; then
    change_type="modify_script"
    target=$(echo "$change_description" | grep -oE "[a-z_]+\.sh|[a-z_]+\.py" | head -1)
    # If no extension found, try just the name
    if [ -z "$target" ]; then
        target=$(echo "$change_description" | grep -oE "[a-z_]+" | tail -1)
        # Try to find it in registry
        found=$(jq -r --arg name "$target" '.scripts[] | select(.name | contains($name)) | .name' "$REGISTRY" | head -1)
        if [ -n "$found" ]; then
            target="$found"
        fi
    fi
fi

echo -e "${CYAN}Change Type:${NC} $change_type"
if [ -n "$target" ]; then
    echo -e "${CYAN}Target:${NC} $target"
fi
echo ""

# Analyze based on change type
case "$change_type" in
    start_daemon)
        echo -e "${CYAN}Analysis: Starting Daemon${NC}"
        echo ""
        
        # Find daemon in registry
        daemon_data=$(jq -r --arg name "$target" '.daemons[] | select(.name == $name)' "$REGISTRY")
        
        if [ -n "$daemon_data" ]; then
            purpose=$(echo "$daemon_data" | jq -r '.purpose')
            should_run=$(echo "$daemon_data" | jq -r '.should_be_running')
            
            echo "What will happen:"
            echo "  • Daemon: $target"
            echo "  • Purpose: $purpose"
            echo "  • Runs continuously until killed"
            
            # Check what it touches
            echo ""
            echo "Touches:"
            echo "$daemon_data" | jq -r '.touches[]' | while read -r path; do
                echo "  • $path"
            done
            
            # Check dependencies
            echo ""
            echo "Dependencies:"
            deps_ok=true
            echo "$daemon_data" | jq -r '.dependencies[]' | while read -r dep; do
                check_cmd=$(jq -r --arg dep "$dep" '.system_dependencies[$dep].check' "$REGISTRY")
                if eval "$check_cmd" > /dev/null 2>&1; then
                    echo -e "  • $dep ${GREEN}✅ installed${NC}"
                else
                    echo -e "  • $dep ${RED}❌ missing${NC}"
                    deps_ok=false
                fi
            done
            
            # Check if already running
            echo ""
            if ps aux | grep -v grep | grep "$target" > /dev/null; then
                echo -e "${YELLOW}⚠️  Already running${NC}"
                risk_level="LOW"
            else
                echo -e "${GREEN}✅ Not currently running${NC}"
                risk_level="MEDIUM"
            fi
            
            # Risk assessment
            echo ""
            echo -e "${CYAN}Risk Assessment:${NC}"
            echo -e "  • Risk level: ${YELLOW}$risk_level${NC}"
            echo "  • Could re-sync files if exclusions incomplete"
            echo "  • Will run until explicitly stopped"
            echo "  • May interfere with manual sync scripts"
            
            # Recommendations
            echo ""
            echo -e "${CYAN}Recommendations:${NC}"
            if [ "$should_run" = "true" ]; then
                echo "  • Configured to run by default"
            else
                echo "  • Only start if continuous sync needed"
            fi
            echo "  • Monitor logs for first hour"
            echo "  • Use manual sync scripts if possible"
            
        else
            echo -e "${RED}Daemon not found in registry: $target${NC}"
            risk_level="HIGH"
        fi
        ;;
        
    stop_daemon)
        echo -e "${CYAN}Analysis: Stopping Daemon${NC}"
        echo ""
        
        # Check if running
        if ps aux | grep -v grep | grep "$target" > /dev/null; then
            echo -e "${GREEN}✅ Daemon is running${NC}"
            echo ""
            echo "What will happen:"
            echo "  • Daemon will be killed"
            echo "  • Continuous sync will stop"
            echo "  • Manual sync scripts still work"
            
            risk_level="LOW"
            
            echo ""
            echo -e "${CYAN}Risk Assessment:${NC}"
            echo -e "  • Risk level: ${GREEN}$risk_level${NC}"
            echo "  • Safe to stop"
            echo "  • No data loss"
            
        else
            echo -e "${YELLOW}⚠️  Daemon not running${NC}"
            risk_level="LOW"
        fi
        ;;
        
    remove_dependency)
        echo -e "${CYAN}Analysis: Removing Dependency${NC}"
        echo ""
        
        # Find what requires this dependency
        scripts_count=$(jq -r --arg dep "$target" '[.scripts[] | select(.dependencies[]? == $dep)] | length' "$REGISTRY")
        daemons_count=$(jq -r --arg dep "$target" '[.daemons[] | select(.dependencies[]? == $dep)] | length' "$REGISTRY")
        total_count=$((scripts_count + daemons_count))
        
        echo "Affected components: $total_count"
        echo "  • Scripts: $scripts_count"
        echo "  • Daemons: $daemons_count"
        echo ""
        
        if [ $daemons_count -gt 0 ]; then
            echo "Daemons that will fail:"
            jq -r --arg dep "$target" '.daemons[] | select(.dependencies[]? == $dep) | .name' "$REGISTRY" | while read -r daemon; do
                echo "  • $daemon"
            done
            echo ""
            risk_level="HIGH"
        elif [ $scripts_count -gt 3 ]; then
            risk_level="MEDIUM"
        elif [ $scripts_count -gt 0 ]; then
            risk_level="LOW-MEDIUM"
        else
            risk_level="LOW"
        fi
        
        echo -e "${CYAN}Risk Assessment:${NC}"
        if [ $daemons_count -gt 0 ]; then
            echo -e "  • Risk level: ${RED}$risk_level${NC}"
            echo "  • $daemons_count daemon(s) will fail"
            echo "  • Critical infrastructure affected"
        elif [ $scripts_count -gt 3 ]; then
            echo -e "  • Risk level: ${YELLOW}$risk_level${NC}"
            echo "  • $scripts_count scripts depend on this"
            echo "  • Test thoroughly if updating"
        else
            echo -e "  • Risk level: ${GREEN}$risk_level${NC}"
            echo "  • Limited impact"
        fi
        
        echo ""
        echo -e "${CYAN}Recommendation:${NC}"
        if [ $daemons_count -gt 0 ]; then
            echo -e "  ${RED}❌ DO NOT REMOVE${NC}"
            echo "  Critical for daemon infrastructure"
        elif [ $scripts_count -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  CAUTION${NC}"
            echo "  Test affected scripts after removal"
        else
            echo "  Safe to remove if truly unused"
        fi
        ;;
        
    add_exclusion)
        echo -e "${CYAN}Analysis: Adding Exclusion Pattern${NC}"
        echo ""
        
        # Find scripts that might need updating
        affected=$(jq -r '.scripts[] | select(.excludes != null) | .name' "$REGISTRY" | wc -l)
        
        echo "Pattern: $target"
        echo "Potentially affected: $affected script(s)"
        echo ""
        
        echo "What will happen:"
        echo "  • Files matching pattern will be excluded from sync"
        echo "  • Existing files won't be deleted"
        echo "  • Future files won't be synced"
        echo ""
        
        risk_level="LOW"
        
        echo -e "${CYAN}Risk Assessment:${NC}"
        echo -e "  • Risk level: ${GREEN}$risk_level${NC}"
        echo "  • No breaking changes"
        echo "  • No data loss"
        echo ""
        
        echo -e "${CYAN}Recommendation:${NC}"
        echo "  • Update all sync scripts with same pattern"
        echo "  • Test with sample file"
        echo "  • Monitor for 24 hours"
        ;;
        
    modify_script)
        echo -e "${CYAN}Analysis: Modifying Script${NC}"
        echo ""
        
        # Find script in registry
        script_data=$(jq -r --arg name "$target" '.scripts[] | select(.name == $name)' "$REGISTRY")
        
        if [ -n "$script_data" ]; then
            purpose=$(echo "$script_data" | jq -r '.purpose')
            script_type=$(echo "$script_data" | jq -r '.type')
            
            echo "Script: $target"
            echo "Type: $script_type"
            echo "Purpose: $purpose"
            echo ""
            
            # Check what it touches
            touches=$(echo "$script_data" | jq -r '.touches[]?' 2>/dev/null)
            if [ -n "$touches" ]; then
                echo "Touches:"
                echo "$touches" | while read -r path; do
                    echo "  • $path"
                    
                    # Count other scripts touching same path
                    others=$(jq -r --arg path "$path" --arg name "$target" '
                        [.scripts[] | select(.touches[]? | contains($path)) | select(.name != $name)] | length
                    ' "$REGISTRY")
                    
                    if [ "$others" -gt 0 ]; then
                        echo "    (Also touched by $others other script(s))"
                    fi
                done
                echo ""
            fi
            
            # Check if called by others
            called_by=$(echo "$script_data" | jq -r '.called_by[]?' 2>/dev/null)
            if [ -n "$called_by" ]; then
                echo "Called by:"
                echo "$called_by" | while read -r caller; do
                    echo "  • $caller"
                done
                echo ""
                risk_level="MEDIUM"
            else
                risk_level="LOW"
            fi
            
            echo -e "${CYAN}Risk Assessment:${NC}"
            echo -e "  • Risk level: ${YELLOW}$risk_level${NC}"
            if [ -n "$called_by" ]; then
                echo "  • Changes may affect calling scripts"
            fi
            echo "  • Test after modification"
            
        else
            echo -e "${YELLOW}Script not found in registry: $target${NC}"
            echo "Run: 8825 audit component $target"
            risk_level="UNKNOWN"
        fi
        ;;
        
    *)
        echo -e "${YELLOW}Unable to analyze this change type${NC}"
        echo ""
        echo "Try:"
        echo "  • 8825 audit path <path> - See what touches a path"
        echo "  • 8825 audit component <name> - Understand a component"
        echo "  • 8825 audit dependency <dep> - Check dependency usage"
        risk_level="UNKNOWN"
        ;;
esac

# Summary
echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo ""
echo -e "Change: $change_description"
echo -e "Risk: $risk_level"
echo ""

if [ "$risk_level" = "HIGH" ] || [ "$risk_level" = "MEDIUM" ]; then
    echo -e "${YELLOW}⚠️  Proceed with caution${NC}"
    echo "Review analysis above before making changes"
elif [ "$risk_level" = "LOW" ]; then
    echo -e "${GREEN}✅ Low risk change${NC}"
    echo "Safe to proceed"
fi

echo ""
