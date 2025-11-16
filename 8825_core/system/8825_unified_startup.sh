#!/bin/bash
# 8825 Unified Startup - Combines governance + PMCS initialization
# Version: 1.0.0
# Created: 2025-11-10

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

V3_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

echo -e "${BLUE}=== 8825 Unified Startup ===${NC}"
echo ""

# 0. Check Cascade Lock (v3.1.0)
echo -e "${BLUE}[0/7] Multi-Cascade Safety Check${NC}"
if [ -f "$V3_ROOT/8825_core/system/cascade_lock.sh" ]; then
    LOCK_STATUS=$("$V3_ROOT/8825_core/system/cascade_lock.sh" check 2>&1)
    if echo "$LOCK_STATUS" | grep -q "Active lock"; then
        echo -e "  ${YELLOW}⚠️  Another Cascade is making system changes${NC}"
        echo "$LOCK_STATUS" | grep -v "^$"
        echo ""
        echo -e "${YELLOW}Recommendation: Wait for the other operation to complete${NC}"
        echo ""
    else
        echo -e "  ${GREEN}✅${NC} No active lock - safe to proceed"
    fi
else
    echo -e "  ${YELLOW}⚠️${NC} Cascade lock not found (pre-v3.1.0 system)"
fi
echo ""

# 1. Governance Health Check
echo -e "${BLUE}[1/7] Governance System${NC}"
GOV_COMMAND="$V3_ROOT/8825"
if [ -x "$GOV_COMMAND" ]; then
    "$GOV_COMMAND" health --quiet
else
    echo -e "  ${YELLOW}⚠️  8825 command not found${NC}"
fi
echo ""

# 2. Load PMCS Core
echo -e "${BLUE}[2/7] PMCS System${NC}"
if [ -f "$V3_ROOT/8825_core/system/8825_core.json" ]; then
    echo -e "  ${GREEN}✅${NC} 8825_core.json loaded"
    
    # Extract version
    VERSION=$(grep -o '"version": "[^"]*"' "$V3_ROOT/8825_core/system/8825_core.json" | head -1 | cut -d'"' -f4)
    echo -e "  ${GREEN}✅${NC} Version: $VERSION"
else
    echo -e "  ${YELLOW}⚠️  8825_core.json not found${NC}"
fi
echo ""

# 3. Load Master Brain
echo -e "${BLUE}[3/7] Master Brain${NC}"
if [ -f "$V3_ROOT/8825_core/system/8825_master_brain.json" ]; then
    echo -e "  ${GREEN}✅${NC} Master brain loaded"
else
    echo -e "  ${YELLOW}⚠️  Master brain not found${NC}"
fi
echo ""

# 4. Scan Available Focuses
echo -e "${BLUE}[4/7] Available Focuses${NC}"
FOCUSES=()

# Check for user directories (v3.0 structure)
if [ -d "$V3_ROOT/users" ]; then
    for user_dir in "$V3_ROOT/users"/*; do
        if [ -d "$user_dir" ]; then
            user_name=$(basename "$user_dir")
            
            # Check for focus directories
            for focus_type in joju hcss goose jh_assistant; do
                if [ -d "$user_dir/$focus_type" ]; then
                    FOCUSES+=("$focus_type")
                    echo -e "  ${GREEN}✅${NC} $focus_type (user: $user_name)"
                fi
            done
        fi
    done
fi

# Fallback: Check for sandbox directories (v2.0 structure)
for sandbox in "$V3_ROOT"/*_sandbox; do
    if [ -d "$sandbox" ]; then
        focus_name=$(basename "$sandbox" | sed 's/_sandbox$//')
        if [[ ! " ${FOCUSES[@]} " =~ " ${focus_name} " ]]; then
            FOCUSES+=("$focus_name")
            echo -e "  ${GREEN}✅${NC} $focus_name (sandbox)"
        fi
    fi
done

if [ ${#FOCUSES[@]} -eq 0 ]; then
    echo -e "  ${YELLOW}⚠️  No focuses found${NC}"
fi
echo ""

# 5. Brain Daemon - Auto-start if not running
echo -e "${BLUE}[5/7] Brain Daemon${NC}"
if [ -f "$V3_ROOT/8825_core/brain/brain_sync_daemon.py" ]; then
    if pgrep -f "brain_sync_daemon.py" > /dev/null; then
        echo -e "  ${GREEN}✅${NC} Brain daemon already running"
    else
        echo -e "  ${YELLOW}⚡${NC} Starting brain daemon..."
        nohup python3 "$V3_ROOT/8825_core/brain/brain_sync_daemon.py" --daemon > /tmp/brain_daemon.log 2>&1 &
        sleep 2
        if pgrep -f "brain_sync_daemon.py" > /dev/null; then
            echo -e "  ${GREEN}✅${NC} Brain daemon started"
        else
            echo -e "  ${YELLOW}✗${NC} Failed to start brain daemon (check /tmp/brain_daemon.log)"
        fi
    fi
else
    echo -e "  ${YELLOW}⚠️  Brain daemon not found${NC}"
fi
echo ""

# 6. Load AI Manifests
echo -e "${BLUE}[6/7] AI Personality Manifests${NC}"
if [ -f "$V3_ROOT/8825_core/brain/manifest_loader.py" ]; then
    python3 "$V3_ROOT/8825_core/brain/manifest_loader.py"
else
    echo -e "  ${YELLOW}⚠️  manifest_loader.py not found${NC}"
fi
echo ""

# 7. Start All MCP Servers
echo -e "${BLUE}[7/7] MCP Servers${NC}"
if [ -f "$V3_ROOT/8825_core/system/start_all_mcps.sh" ]; then
    bash "$V3_ROOT/8825_core/system/start_all_mcps.sh"
else
    echo -e "  ${YELLOW}⚠️${NC} MCP startup script not found"
fi

# Summary
echo -e "${BLUE}=== 8825 Mode Active ===${NC}"
echo ""
echo "System: Persistent Context Memory Sidecar"
echo "Version: 3.1.0"
echo "User: Justin Harmon"
echo "Workspace: $V3_ROOT"
echo ""

if [ ${#FOCUSES[@]} -gt 0 ]; then
    echo "Available Focuses:"
    for focus in "${FOCUSES[@]}"; do
        echo "  - $focus"
    done
    echo ""
fi

echo "Commands:"
echo "  8825 start          - Full startup protocol"
echo "  8825 health         - Health check"
echo "  8825 audit path     - Audit path usage"
echo "  8825 impact         - Impact analysis"
echo "  8825 registry       - Registry management"
echo "  8825-brain-status   - Brain daemon status"
echo ""
echo "v3.1 POC Management:"
echo "  audit-pocs          - Check POC promotion readiness"
echo "  promote-poc         - Promote POC to production"
echo "  check-lock          - Check Cascade lock status"
echo "  8825-version        - Show system version"
echo ""
echo "Focus Commands:"
echo "  focus on [project]  - Enter project sandbox"
echo "  list focuses        - Show all focuses"
echo "  exit 8825 mode      - Deactivate system"
echo ""
