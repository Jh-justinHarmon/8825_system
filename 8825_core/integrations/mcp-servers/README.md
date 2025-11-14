# 8825 MCP Servers

**System-wide MCP servers for multi-user access**

---

## Available MCP Servers

### 1. FDS MCP (File Dispatch System)
**Location:** `fds-mcp/`  
**Purpose:** File processing control  
**Users:** All (system-wide)  
**Tools:** 7 (status, start, stop, process, logs, queue)

### 2. HCSS MCP
**Location:** `../../focuses/hcss/mcp_server/`  
**Port:** 8826  
**Purpose:** HCSS client work  
**Users:** justin_harmon, hcss_team

### 3. Joju/Team76 MCP
**Location:** `../../focuses/joju/mcp_server/`  
**Port:** 8827  
**Purpose:** Joju product development  
**Users:** justin_harmon, matthew_galley, cam_watkins

### 4. JH Assistant MCP
**Location:** (TBD)  
**Port:** 8828  
**Purpose:** Personal assistant  
**Users:** justin_harmon

---

## MCP Organization

### System-Wide MCPs
**Location:** `8825_core/integrations/mcp-servers/`

**Criteria:**
- Used by multiple users
- System-level functionality
- Not focus-specific
- Shared infrastructure

**Examples:**
- FDS MCP (file processing)
- Brain MCP (knowledge access)
- Index MCP (search/discovery)

### Focus-Specific MCPs
**Location:** `focuses/{focus_name}/mcp_server/`

**Criteria:**
- Focus-specific functionality
- User/team access control
- Project-specific tools
- Isolated data

**Examples:**
- HCSS MCP (client work)
- Joju MCP (product dev)
- JH Assistant MCP (personal)

---

## Adding New MCP Servers

### System-Wide MCP

1. Create in `8825_core/integrations/mcp-servers/{name}-mcp/`
2. Follow FDS structure:
   - `server.py` - MCP server
   - `goose_config.yaml` - Goose configuration
   - `SETUP_GOOSE.sh` - Setup script
   - `README.md` - Documentation
3. Update this README
4. Add to Goose profiles

### Focus-Specific MCP

1. Create in `focuses/{focus}/mcp_server/`
2. Follow focus MCP structure
3. Configure access control
4. Document in focus README

---

## Goose Integration

All MCPs can be used simultaneously in Goose:

```bash
goose session start

# Use any MCP
> What's the FDS status?           # FDS MCP
> Show me HCSS tasks               # HCSS MCP
> Create a Joju feature task       # Joju MCP
> Check my calendar                # JH Assistant MCP
```

---

**Status:** FDS MCP complete, others in progress  
**Date:** November 11, 2025
