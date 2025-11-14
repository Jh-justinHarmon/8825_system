# MCP Server Startup - Clarification

**Date:** 2025-11-10  
**Issue:** Confusion about MCP server startup automation

---

## The Misunderstanding

**What we thought:** MCP servers need to run as background processes (like web servers on ports 8826, 8827, 8828)

**Reality:** MCP servers use **stdio communication** and are started by Goose on-demand

---

## How MCP Servers Actually Work

### Architecture
```
Goose AI Agent
    ↓ (starts process)
MCP Server (stdio)
    ↓ (JSON-RPC over stdin/stdout)
Goose AI Agent
```

### Key Points
1. **No background processes** - Servers start when Goose needs them
2. **No ports** - Communication via stdin/stdout, not HTTP
3. **No LaunchAgent needed** - Goose manages the lifecycle
4. **Configured in Goose** - `~/.config/goose/profiles.yaml`

---

## What Was Wrong

### ❌ Incorrect Setup
- `start_all_mcps.sh` trying to run servers as daemons
- LaunchAgent `com.8825.mcp-servers.plist` auto-starting on login
- Documentation claiming servers run on ports 8826-8828
- Confusion about "starting" and "stopping" servers

### ✅ Correct Setup
- Servers defined in `~/.config/goose/profiles.yaml`
- Goose invokes them when needed: `node ~/mcp_servers/hcss-bridge/server.js`
- No manual startup required
- No background processes to manage

---

## What We Fixed

### 1. Updated Documentation
- `STARTUP_AUTOMATION.md` - Corrected MCP server section
- Removed references to ports and auto-start

### 2. Disabled LaunchAgent
```bash
launchctl unload ~/Library/LaunchAgents/com.8825.mcp-servers.plist
```
- Added `<key>Disabled</key><true/>` to plist
- Added comment explaining why it's disabled

### 3. Updated Scripts
- `start_all_mcps.sh` - Updated to match actual server paths (but not needed)
- `stop_all_mcps.sh` - Updated to target specific servers (but not needed)
- **Note:** These scripts are now obsolete but kept for reference

---

## Current MCP Server Setup

### Available Servers
Located in `~/mcp_servers/`:

1. **hcss-bridge** - HCSS automation tools
2. **figma-make-transformer** - Figma Make component transformer
3. **8825-core** - Deep 8825 system access

### How to Use

**In Goose:**
```
> List available tools
> Check HCSS system status
> Transform Figma component
```

**Check Configuration:**
```bash
cat ~/.config/goose/profiles.yaml
```

**Verify Servers Work:**
```bash
# Test Node.js server
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node ~/mcp_servers/hcss-bridge/server.js

# Test Python server
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 ~/mcp_servers/8825-core/server.py
```

---

## Why This Confusion Happened

1. **Old v2.0 references** - Documentation mentioned "windsurf-project - 8825 8825-system" (doesn't exist)
2. **Port numbers in docs** - Made it seem like HTTP servers
3. **LaunchAgent existed** - Implied background processes were needed
4. **"Start" terminology** - Made it sound like daemon management

---

## Going Forward

### ✅ What to Do
- Use MCP servers through Goose naturally
- Update `~/.config/goose/profiles.yaml` if adding new servers
- Test servers work by using them in Goose

### ❌ What NOT to Do
- Don't try to "start" MCP servers manually
- Don't look for running MCP processes
- Don't create LaunchAgents for MCP servers
- Don't expect to see ports 8826-8828 in use

---

## Related Files

- **MCP Servers:** `~/mcp_servers/`
- **Goose Config:** `~/.config/goose/profiles.yaml`
- **Documentation:** `~/mcp_servers/README.md`
- **This File:** `8825-system/MCP_STARTUP_CLARIFICATION.md`

---

**Bottom Line:** MCP servers are tools that Goose invokes, not services that run in the background. No startup automation needed! ✅
