---
description: Launch 8825 unified startup system
---

# Launch 8825 Mode

Starts all 8825 services in the correct order:
- Governance system health check
- PMCS system initialization
- Master Brain loading
- Focus area scanning
- Brain daemon (auto-starts if not running)
- AI personality manifests
- MCP servers (HCSS, Joju, 8825 Core)
- Inbox server (auto-starts if not running)

## Usage

From Cascade, just type:
```
/launch-8825
```

Or use natural language:
```
launch 8825 mode
```

## What It Does

// turbo
1. Run the unified startup script
```bash
bash "$HOME/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/system/8825_unified_startup.sh"
```

## Expected Output

You should see:
- ✅ 7 phases complete
- ✅ Brain daemon running
- ✅ MCP servers available
- ✅ Inbox server running
- ✅ System ready message

## Troubleshooting

If startup fails:
1. Check logs: `/tmp/brain_daemon.log`
2. Check MCP logs: `/tmp/mcp-*.log`
3. Check inbox: `/tmp/8825-inbox-pipeline.log`
4. Verify processes: `ps aux | grep -E "(brain_sync|inbox_server)"`

## Manual Alternative

From terminal:
```bash
launch_8825
```

Or:
```bash
8825-launch
```
