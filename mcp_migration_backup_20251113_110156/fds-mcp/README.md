# File Dispatch System - MCP Server

**Goose-compatible MCP server for FDS control**

---

## What This Provides

Natural language control of File Dispatch System via Goose.

### 7 MCP Tools

1. **fds_status** - Get system status
2. **fds_start** - Start FDS
3. **fds_stop** - Stop FDS
4. **fds_process_file** - Process specific file
5. **fds_get_logs** - View recent logs
6. **fds_get_queue** - See processing queue
7. **fds_clear_queue** - Clear queue

---

## Setup

```bash
./SETUP_GOOSE.sh
```

This will:
1. Check Goose installation
2. Show configuration to add
3. Optionally add to profiles.yaml automatically

---

## Manual Setup

Add to `~/.config/goose/profiles.yaml`:

```yaml
mcpServers:
  file-dispatch-system:
    command: python3
    args:
      - /Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/file_dispatch_system/mcp_server/server.py
    env:
      PYTHONPATH: /Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/file_dispatch_system
```

---

## Usage with Goose

```bash
goose session start
```

### Natural Language Examples

**Status:**
- "What's the status of the file dispatch system?"
- "Is FDS running?"
- "Show me FDS status"

**Control:**
- "Start the file dispatch system"
- "Stop FDS"
- "Start file processing"

**Monitoring:**
- "Show me recent FDS logs"
- "What's in the processing queue?"
- "Show me the last 50 log entries"

**Processing:**
- "Process this file: /Users/justinharmon/Downloads/document.pdf"
- "Clear the FDS queue"

---

## Tool Details

### fds_status
Returns:
- Running status (running/stopped)
- PID if running
- Input/output configuration
- Queue size
- Recent activity

### fds_start
Starts the FDS watcher in background.

### fds_stop
Stops the FDS watcher.

### fds_process_file
Process a specific file immediately.

**Parameters:**
- `file_path` (required): Full path to file

### fds_get_logs
Get recent log entries.

**Parameters:**
- `lines` (optional): Number of lines (default: 20)

### fds_get_queue
Returns list of files in processing queue.

### fds_clear_queue
Clears the processing queue.

---

## Architecture

```
Goose (Natural Language)
    ↓ (stdio/JSON-RPC)
FDS MCP Server
    ↓
Unified Processor
    ↓
├─ Smart Classifier
├─ Ingestion Router
├─ Screenshot Processor
├─ Output Manager
└─ Progressive Router
```

---

## Troubleshooting

### MCP Server Won't Start

```bash
# Check Python path
which python3

# Test server directly
python3 server.py

# Check logs
tail -f ../logs/unified_processor.log
```

### Goose Can't Find Tools

```bash
# Verify configuration
cat ~/.config/goose/profiles.yaml

# Check server is registered
goose session start
> list available tools
```

### Commands Not Working

```bash
# Check FDS is configured
cd ..
./status.sh

# Verify paths in goose_config.yaml
cat goose_config.yaml
```

---

## Integration with Other MCPs

FDS MCP works alongside:
- HCSS MCP (port 8826)
- Joju/Team76 MCP (port 8827)
- JH Assistant MCP (port 8828)

All can be used simultaneously in Goose.

---

**Status:** Production ready  
**Protocol:** MCP 2024-11-05  
**Goose:** Fully compatible
