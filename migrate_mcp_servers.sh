#!/bin/bash
# MCP Server Migration Script
# Date: 2025-11-13
# Purpose: Consolidate all MCP servers to ~/mcp_servers/

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
MCP_HOME="$HOME/mcp_servers"

echo -e "${BLUE}=== MCP Server Migration ===${NC}"
echo ""
echo "This script will:"
echo "  1. Move scattered MCP servers to ~/mcp_servers/"
echo "  2. Delete duplicate copies"
echo "  3. Update registry"
echo "  4. Kill ghost processes"
echo ""
echo -e "${YELLOW}Press Enter to continue, Ctrl+C to cancel${NC}"
read

# Create backup
echo -e "${BLUE}[1/5] Creating backup...${NC}"
BACKUP_DIR="$SYSTEM_ROOT/mcp_migration_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "  Backup location: $BACKUP_DIR"
echo ""

# Phase 1: Move scattered servers
echo -e "${BLUE}[2/5] Moving scattered servers to ~/mcp_servers/${NC}"

# Move Otter Integration (consolidate 3 copies)
if [ -d "$SYSTEM_ROOT/8825_core/poc/infrastructure/otter_integration" ]; then
    echo "  Moving otter-integration..."
    cp -r "$SYSTEM_ROOT/8825_core/poc/infrastructure/otter_integration" "$BACKUP_DIR/"
    mv "$SYSTEM_ROOT/8825_core/poc/infrastructure/otter_integration" "$MCP_HOME/otter-integration"
    echo -e "  ${GREEN}✅${NC} otter-integration moved"
else
    echo -e "  ${YELLOW}⚠️${NC} otter_integration not found"
fi

# Move FDS MCP
if [ -d "$SYSTEM_ROOT/8825_core/integrations/mcp-servers/fds-mcp" ]; then
    echo "  Moving fds..."
    cp -r "$SYSTEM_ROOT/8825_core/integrations/mcp-servers/fds-mcp" "$BACKUP_DIR/"
    mv "$SYSTEM_ROOT/8825_core/integrations/mcp-servers/fds-mcp" "$MCP_HOME/fds"
    echo -e "  ${GREEN}✅${NC} fds moved"
else
    echo -e "  ${YELLOW}⚠️${NC} fds-mcp not found"
fi

# Move Meeting Automation
if [ -d "$SYSTEM_ROOT/8825_core/integrations/mcp-servers/meeting-automation-mcp" ]; then
    echo "  Moving meeting-automation..."
    cp -r "$SYSTEM_ROOT/8825_core/integrations/mcp-servers/meeting-automation-mcp" "$BACKUP_DIR/"
    mv "$SYSTEM_ROOT/8825_core/integrations/mcp-servers/meeting-automation-mcp" "$MCP_HOME/meeting-automation"
    echo -e "  ${GREEN}✅${NC} meeting-automation moved"
else
    echo -e "  ${YELLOW}⚠️${NC} meeting-automation-mcp not found"
fi

# Move RAL Portal
if [ -d "$SYSTEM_ROOT/mcp_servers/ral_portal" ]; then
    echo "  Moving ral-portal..."
    cp -r "$SYSTEM_ROOT/mcp_servers/ral_portal" "$BACKUP_DIR/"
    mv "$SYSTEM_ROOT/mcp_servers/ral_portal" "$MCP_HOME/ral-portal"
    echo -e "  ${GREEN}✅${NC} ral-portal moved"
else
    echo -e "  ${YELLOW}⚠️${NC} ral_portal not found"
fi

# Move Customer Platform
if [ -d "$SYSTEM_ROOT/../8825_customers/mcp_server" ]; then
    echo "  Moving customer-platform..."
    cp -r "$SYSTEM_ROOT/../8825_customers/mcp_server" "$BACKUP_DIR/"
    mv "$SYSTEM_ROOT/../8825_customers/mcp_server" "$MCP_HOME/customer-platform"
    echo -e "  ${GREEN}✅${NC} customer-platform moved"
else
    echo -e "  ${YELLOW}⚠️${NC} customer mcp_server not found"
fi

echo ""

# Phase 2: Remove duplicates
echo -e "${BLUE}[3/5] Removing duplicate copies${NC}"

# Remove old FigJam
if [ -d "$SYSTEM_ROOT/8825_core/integrations/figjam/mcp-server" ]; then
    echo "  Removing duplicate figjam..."
    cp -r "$SYSTEM_ROOT/8825_core/integrations/figjam/mcp-server" "$BACKUP_DIR/"
    rm -rf "$SYSTEM_ROOT/8825_core/integrations/figjam/mcp-server"
    echo -e "  ${GREEN}✅${NC} Duplicate figjam removed"
fi

# Remove old HCSS bridge
if [ -d "$SYSTEM_ROOT/8825_core/integrations/goose/mcp-servers/hcss-bridge" ]; then
    echo "  Removing duplicate hcss-bridge..."
    cp -r "$SYSTEM_ROOT/8825_core/integrations/goose/mcp-servers/hcss-bridge" "$BACKUP_DIR/"
    rm -rf "$SYSTEM_ROOT/8825_core/integrations/goose/mcp-servers/hcss-bridge"
    echo -e "  ${GREEN}✅${NC} Duplicate hcss-bridge removed"
fi

# Remove duplicate Otter #1
if [ -d "$SYSTEM_ROOT/focuses/hcss/automation/otter_mcp" ]; then
    echo "  Removing duplicate otter_mcp #1..."
    cp -r "$SYSTEM_ROOT/focuses/hcss/automation/otter_mcp" "$BACKUP_DIR/"
    rm -rf "$SYSTEM_ROOT/focuses/hcss/automation/otter_mcp"
    echo -e "  ${GREEN}✅${NC} Duplicate otter_mcp #1 removed"
fi

# Remove duplicate Otter #2
if [ -d "$SYSTEM_ROOT/focuses/hcss/poc/tgif_automation/otter_mcp" ]; then
    echo "  Removing duplicate otter_mcp #2..."
    cp -r "$SYSTEM_ROOT/focuses/hcss/poc/tgif_automation/otter_mcp" "$BACKUP_DIR/"
    rm -rf "$SYSTEM_ROOT/focuses/hcss/poc/tgif_automation/otter_mcp"
    echo -e "  ${GREEN}✅${NC} Duplicate otter_mcp #2 removed"
fi

# Remove empty mcp-servers directory
if [ -d "$SYSTEM_ROOT/8825_core/integrations/mcp-servers" ]; then
    if [ -z "$(ls -A "$SYSTEM_ROOT/8825_core/integrations/mcp-servers")" ]; then
        echo "  Removing empty mcp-servers directory..."
        rm -rf "$SYSTEM_ROOT/8825_core/integrations/mcp-servers"
        echo -e "  ${GREEN}✅${NC} Empty directory removed"
    fi
fi

# Remove empty mcp_servers directory in 8825-system
if [ -d "$SYSTEM_ROOT/mcp_servers" ]; then
    if [ -z "$(ls -A "$SYSTEM_ROOT/mcp_servers")" ]; then
        echo "  Removing empty mcp_servers directory..."
        rm -rf "$SYSTEM_ROOT/mcp_servers"
        echo -e "  ${GREEN}✅${NC} Empty directory removed"
    fi
fi

echo ""

# Phase 3: Update registry
echo -e "${BLUE}[4/5] Updating registry${NC}"

REGISTRY_FILE="$SYSTEM_ROOT/8825_core/system/mcp_registry.json"

if [ -f "$REGISTRY_FILE" ]; then
    echo "  Backing up registry..."
    cp "$REGISTRY_FILE" "$BACKUP_DIR/mcp_registry.json.backup"
    
    echo "  Creating new registry..."
    cat > "$REGISTRY_FILE" << 'EOF'
{
  "version": "3.0.0",
  "description": "Registry of all available MCP servers",
  "last_updated": "2025-11-13",
  
  "mcp_location": "~/mcp_servers/",
  
  "available_mcps": {
    "8825_core": {
      "location": "~/mcp_servers/8825-core/",
      "type": "stdio",
      "language": "python",
      "description": "Deep access to 8825 ingestion engine"
    },
    "hcss_bridge": {
      "location": "~/mcp_servers/hcss-bridge/",
      "type": "stdio",
      "language": "node",
      "description": "HCSS automation (Gmail, Otter, routing)"
    },
    "figma_make_transformer": {
      "location": "~/mcp_servers/figma-make-transformer/",
      "type": "stdio",
      "language": "node",
      "description": "Transform Figma Make → Joju React code"
    },
    "figjam": {
      "location": "~/mcp_servers/figjam/",
      "type": "stdio",
      "language": "node",
      "description": "FigJam integration and automation"
    },
    "otter_integration": {
      "location": "~/mcp_servers/otter-integration/",
      "type": "stdio",
      "language": "python",
      "description": "Otter.ai meeting transcription integration"
    },
    "fds": {
      "location": "~/mcp_servers/fds/",
      "type": "stdio",
      "language": "python",
      "description": "FDS integration"
    },
    "meeting_automation": {
      "location": "~/mcp_servers/meeting-automation/",
      "type": "stdio",
      "language": "python",
      "description": "Meeting automation workflows"
    },
    "ral_portal": {
      "location": "~/mcp_servers/ral-portal/",
      "type": "stdio",
      "language": "python",
      "description": "RAL portal integration"
    },
    "customer_platform": {
      "location": "~/mcp_servers/customer-platform/",
      "type": "stdio",
      "language": "node",
      "description": "Customer platform MCP"
    }
  },
  
  "orchestration": {
    "start_all_script": "8825_core/system/start_all_mcps.sh",
    "health_check_interval": 60
  }
}
EOF
    
    echo -e "  ${GREEN}✅${NC} Registry updated"
else
    echo -e "  ${YELLOW}⚠️${NC} Registry file not found"
fi

echo ""

# Phase 4: Kill ghost processes
echo -e "${BLUE}[5/5] Killing ghost processes${NC}"

echo "  Looking for processes with '8825-system' in path..."
GHOST_PIDS=$(ps aux | grep "8825-system.*mcp_server" | grep -v grep | awk '{print $2}')

if [ -n "$GHOST_PIDS" ]; then
    echo "  Found ghost processes: $GHOST_PIDS"
    echo "$GHOST_PIDS" | xargs kill
    echo -e "  ${GREEN}✅${NC} Ghost processes killed"
    echo "  Windsurf will restart them automatically with correct paths"
else
    echo -e "  ${GREEN}✅${NC} No ghost processes found"
fi

echo ""

# Summary
echo -e "${GREEN}=== Migration Complete ===${NC}"
echo ""
echo "Summary:"
echo "  ✅ Scattered servers moved to ~/mcp_servers/"
echo "  ✅ Duplicate copies removed"
echo "  ✅ Registry updated"
echo "  ✅ Ghost processes killed"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "  1. Run: ls ~/mcp_servers/"
echo "  2. Test: launch_8825"
echo "  3. Verify MCP servers are accessible in Windsurf"
echo ""
echo -e "${BLUE}All MCP servers now in one location!${NC}"
echo ""
