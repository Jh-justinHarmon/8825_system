#!/bin/bash
# 8825 Audit Conflicts
# Finds conflicts in the system

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

echo ""
echo -e "${BLUE}=== Conflict Detection ===${NC}"
echo ""

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq not installed. Run: 8825 deps"
    exit 1
fi

total_issues=0

# 1. Check for duplicate implementations
echo -e "${CYAN}[1/4] Duplicate Implementations...${NC}"

# Find all scripts in workspace
all_scripts=$(find "$WORKSPACE_ROOT/8825_core" "$WORKSPACE_ROOT/INBOX_HUB" "$WORKSPACE_ROOT/users" \
    -type f \( -name "*.sh" -o -name "*.py" \) 2>/dev/null | \
    xargs -I {} basename {})

# Find duplicates
duplicates=$(echo "$all_scripts" | sort | uniq -d)

if [ -n "$duplicates" ]; then
    dup_count=$(echo "$duplicates" | wc -l | tr -d ' ')
    echo -e "  ${YELLOW}⚠️  Found $dup_count duplicate(s):${NC}"
    echo ""
    
    echo "$duplicates" | while read -r dup; do
        if [ -n "$dup" ]; then
            echo -e "  ${YELLOW}• $dup${NC}"
            
            # Find all locations
            locations=$(find "$WORKSPACE_ROOT/8825_core" "$WORKSPACE_ROOT/INBOX_HUB" "$WORKSPACE_ROOT/users" \
                -type f -name "$dup" 2>/dev/null)
            
            loc_num=1
            echo "$locations" | while read -r loc; do
                rel_path=$(echo "$loc" | sed "s|$WORKSPACE_ROOT/||")
                echo "    Location $loc_num: $rel_path"
                loc_num=$((loc_num + 1))
            done
            
            echo "    Recommendation: Keep one, delete others"
            echo ""
            total_issues=$((total_issues + 1))
        fi
    done
else
    echo -e "  ${GREEN}✅ No duplicate implementations found${NC}"
fi

# 2. Check for exclusion pattern conflicts
echo ""
echo -e "${CYAN}[2/4] Exclusion Pattern Conflicts...${NC}"

# Get all critical paths
critical_paths=$(jq -r '.critical_paths | keys[]' "$REGISTRY")

conflict_found=0

echo "$critical_paths" | while read -r path; do
    if [ -n "$path" ]; then
        # Get all components touching this path
        components=$(jq -r --arg path "$path" '
            (.scripts[] | select(.touches[]? | contains($path)) | .name),
            (.daemons[] | select(.touches[]? | contains($path)) | .name)
        ' "$REGISTRY")
        
        if [ -n "$components" ]; then
            # Get unique exclusion patterns
            patterns=$(jq -r --arg path "$path" '
                (.scripts[] | select(.touches[]? | contains($path)) | .excludes),
                (.daemons[] | select(.touches[]? | contains($path)) | .excludes)
            ' "$REGISTRY" 2>/dev/null | jq -s 'unique')
            
            pattern_count=$(echo "$patterns" | jq 'length')
            
            if [ "$pattern_count" -gt 1 ]; then
                echo -e "  ${YELLOW}⚠️  Conflict at: $path${NC}"
                echo "    Different exclusion patterns detected"
                echo "    Components should coordinate exclusions"
                conflict_found=1
            fi
        fi
    fi
done

if [ $conflict_found -eq 0 ]; then
    echo -e "  ${GREEN}✅ No exclusion pattern conflicts${NC}"
fi

# 3. Check for overlapping touchpoints
echo ""
echo -e "${CYAN}[3/4] Overlapping Touchpoints...${NC}"

echo "$critical_paths" | while read -r path; do
    if [ -n "$path" ]; then
        # Count touchpoints
        touchpoint_count=$(jq -r --arg path "$path" '
            [
                (.scripts[] | select(.touches[]? | contains($path)) | .name),
                (.daemons[] | select(.touches[]? | contains($path)) | .name)
            ] | length
        ' "$REGISTRY")
        
        if [ "$touchpoint_count" -gt 5 ]; then
            echo -e "  ${YELLOW}ℹ️  High activity at: $path${NC}"
            echo "    $touchpoint_count components touch this path"
            echo "    Risk: MEDIUM (many touchpoints)"
            echo ""
        fi
    fi
done

# Check if any path has many touchpoints
max_touchpoints=$(echo "$critical_paths" | while read -r path; do
    if [ -n "$path" ]; then
        jq -r --arg path "$path" '
            [
                (.scripts[] | select(.touches[]? | contains($path)) | .name),
                (.daemons[] | select(.touches[]? | contains($path)) | .name)
            ] | length
        ' "$REGISTRY"
    fi
done | sort -n | tail -1)

if [ "$max_touchpoints" -le 5 ]; then
    echo -e "  ${GREEN}✅ No excessive overlapping touchpoints${NC}"
fi

# 4. Check for orphaned processes
echo ""
echo -e "${CYAN}[4/4] Orphaned Processes...${NC}"

# Get all registered daemon names
registered_daemons=$(jq -r '.daemons[].name' "$REGISTRY")

# Check for running Python/bash processes that might be daemons
running_processes=$(ps aux | grep -E "(python|bash)" | grep -v grep | grep -v "8825" | awk '{print $11}')

orphan_found=0

# Look for common daemon patterns
if ps aux | grep -v grep | grep -E "sync.*\.py|watch.*\.py|monitor.*\.py" > /dev/null; then
    potential_orphans=$(ps aux | grep -v grep | grep -E "sync.*\.py|watch.*\.py|monitor.*\.py" | awk '{print $11, $12}')
    
    echo "$potential_orphans" | while read -r proc; do
        proc_name=$(basename "$proc" | awk '{print $1}')
        
        # Check if it's registered
        if ! echo "$registered_daemons" | grep -q "$proc_name"; then
            echo -e "  ${YELLOW}⚠️  Potential orphan: $proc_name${NC}"
            echo "    Not found in registry"
            echo "    PID: $(ps aux | grep "$proc_name" | grep -v grep | awk '{print $2}')"
            orphan_found=1
        fi
    done
fi

if [ $orphan_found -eq 0 ]; then
    echo -e "  ${GREEN}✅ No orphaned processes detected${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo ""

if [ $total_issues -eq 0 ] && [ $conflict_found -eq 0 ] && [ $orphan_found -eq 0 ]; then
    echo -e "${GREEN}✅ No conflicts detected${NC}"
    echo "  System appears healthy"
else
    issue_count=$((total_issues + conflict_found + orphan_found))
    echo -e "${YELLOW}⚠️  $issue_count issue(s) found${NC}"
    echo "  Review warnings above and take action"
fi

echo ""
