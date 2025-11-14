# HCSS MCP Bridge Server

**Version:** 1.0.0  
**Purpose:** Bridge Goose AI agent with 8825 HCSS workflows  
**Status:** Ready to use

---

## Overview

This MCP server exposes HCSS tools to Goose, allowing the AI agent to:
- Trigger Gmail/Otter ingestion
- Check system status
- List recent files
- Read correction logs
- Get routing statistics

---

## Installation

### 1. Install Dependencies

```bash
cd mcp-servers/hcss-bridge
npm install
```

### 2. Test Server

```bash
node server.js
```

You should see: `HCSS MCP Bridge Server running on stdio`

---

## Configuration

### Add to Goose (Desktop UI)

1. Open Goose
2. Settings → MCP Servers
3. Click "Add Server"
4. Fill in:
   - **Name:** `hcss-bridge`
   - **Command:** `node`
   - **Args:** `["/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system/goose_sandbox/mcp-servers/hcss-bridge/server.js"]`

### Add to Goose (CLI)

Edit `~/.config/goose/config.json`:

```json
{
  "mcpServers": {
    "hcss-bridge": {
      "command": "node",
      "args": ["/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system/goose_sandbox/mcp-servers/hcss-bridge/server.js"]
    }
  }
}
```

---

## Available Tools

### 1. ingest_gmail
**Description:** Trigger Gmail/Otter ingestion  
**Parameters:**
- `days_back` (optional): Number of days to search back (default: 7)

**Example:**
```
> "Use ingest_gmail to check for new emails"
> "Run ingest_gmail with days_back=14"
```

### 2. check_status
**Description:** Check HCSS system status  
**Parameters:** None

**Example:**
```
> "Use check_status to see the system status"
> "What's the current HCSS status?"
```

### 3. list_recent_files
**Description:** List recently processed files  
**Parameters:**
- `project` (optional): Filter by TGIF, RAL, LHL, 76, or all (default: all)
- `limit` (optional): Max files to return (default: 10)

**Example:**
```
> "Use list_recent_files to show the latest files"
> "List recent TGIF files with limit=5"
```

### 4. read_corrections_log
**Description:** Read corrections log  
**Parameters:**
- `lines` (optional): Number of recent lines (default: 50)

**Example:**
```
> "Use read_corrections_log to see recent corrections"
> "Show me the last 100 corrections"
```

### 5. get_routing_stats
**Description:** Get routing statistics  
**Parameters:** None

**Example:**
```
> "Use get_routing_stats to see project distribution"
> "What's the routing breakdown?"
```

---

## Usage Examples

### From Goose CLI

```bash
# Start Goose in Windsurf terminal
cd "/Users/justinharmon/.../windsurf-project - 8825 8825-system"
goose session

# Use tools
> "Check the HCSS status"
> "Ingest new Gmail messages"
> "Show me the latest TGIF files"
> "What corrections have been applied today?"
> "Give me routing statistics"
```

### From Goose Desktop

Open Goose app and ask:
- "Connect to HCSS and check status"
- "Run Gmail ingestion and summarize results"
- "Show me recent files for the RAL project"
- "Analyze the correction patterns"

---

## Troubleshooting

### Server Won't Start

**Error:** `Cannot find module '@modelcontextprotocol/sdk'`  
**Fix:** Run `npm install` in the hcss-bridge directory

**Error:** `ENOENT: no such file or directory`  
**Fix:** Verify paths in server.js point to correct locations

### Goose Can't Connect

**Issue:** Server not showing in Goose  
**Fix:** 
1. Verify full path in Goose config
2. Test server manually: `node server.js`
3. Check Node.js version: `node --version` (need 18+)

### Tools Not Working

**Issue:** Tool execution fails  
**Fix:**
1. Check HCSS sandbox path is correct
2. Verify Python scripts are executable
3. Check logs in `hcss_sandbox/logs/`

---

## Development

### Adding New Tools

1. **Define tool in TOOLS array:**
```javascript
{
  name: 'my_new_tool',
  description: 'What it does',
  inputSchema: {
    type: 'object',
    properties: {
      param1: { type: 'string', description: 'Parameter' }
    }
  }
}
```

2. **Add case in switch statement:**
```javascript
case 'my_new_tool':
  return await myNewTool(args);
```

3. **Implement function:**
```javascript
async function myNewTool(args) {
  // Implementation
  return {
    content: [{ type: 'text', text: 'Result' }]
  };
}
```

### Testing

```bash
# Test server
node server.js

# Test from Goose
goose session
> "Use my_new_tool with param1='test'"
```

---

## Architecture

```
Goose CLI/Desktop
      ↓
MCP Protocol (stdio)
      ↓
server.js (this file)
      ↓
Tool Functions
      ↓
HCSS Python Scripts
      ↓
Gmail/Otter/Files
```

---

## Files

- `server.js` - Main MCP server implementation
- `package.json` - Node.js dependencies
- `README.md` - This file

---

## Dependencies

- `@modelcontextprotocol/sdk` - MCP protocol implementation
- Node.js 18+ - Runtime
- Python 3 - For HCSS scripts

---

## Next Steps

1. Install dependencies: `npm install`
2. Test server: `node server.js`
3. Configure in Goose
4. Try tools from Goose session
5. Add more tools as needed

---

## Support

For issues or questions:
1. Check this README
2. Review ../GOOSE_WINDSURF_INTEGRATION.md
3. Test server manually
4. Check Goose logs: `~/.config/goose/logs/`
