# Launch 8825 Mode - Complete Startup

## Quick Start

From any terminal or Cascade chat:
```bash
launch_8825
```

Or use the alias:
```bash
launch-8825
```

## What Gets Started

### ✅ Automatically Checked/Started
1. **Governance System** - Registry, health checks, audit tools
2. **PMCS System** - Pattern mining & context sidecar (v2.0.0)
3. **Master Brain** - Operational brain with 3 engines
4. **Available Focuses** - joju, hcss, jh_assistant
5. **Brain Daemon** - Background intelligence engine
6. **MCP Servers** - All 4 centralized servers checked
7. **Inbox Server** - Auto-started if not running

### 📋 MCP Servers Checked
- `8825-core` - Deep 8825 system access
- `hcss-bridge` - HCSS automation
- `figma-make-transformer` - Figma → Joju code
- `figjam` - FigJam integration

**Note:** MCP servers are stdio-based and launched by MCP clients (Goose, etc.), not standalone daemons.

## Manual Startup (if needed)

```bash
bash ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/8825_core/system/8825_unified_startup.sh
```

## Logs

MCP logs: `~/.8825/mcp_logs/`

## Shell Integration

The launcher is automatically sourced in your `~/.zshrc`:
```bash
source ~/.8825_launch
```

## From Cascade

Just say:
```
launch 8825 mode
```

Cascade will auto-run the startup script.

## Status Check

After launch, check what's running:
```bash
ps aux | grep -E "(mcp|server\.(js|py)|brain_daemon)" | grep -v grep
```

## Troubleshooting

**If MCP servers aren't available:**
```bash
ls -la ~/mcp_servers/
```

**If inbox server fails:**
```bash
cat ~/.8825/mcp_logs/inbox_server.log
```

**If brain daemon isn't running:**
```bash
ps aux | grep brain_daemon
```

## Architecture

```
8825 Mode
├── Governance (registry, health, audit)
├── PMCS (patterns, mining, context)
├── Master Brain (3 engines)
├── Focuses (joju, hcss, jh_assistant)
├── Brain Daemon (background intelligence)
├── MCP Servers (4 centralized)
└── Inbox Server (intake automation)
```

## Next Steps After Launch

- `focus on joju` - Enter Joju sandbox
- `focus on hcss` - Enter HCSS sandbox
- `8825 health` - Run health check
- `8825 registry review` - Review registry

---

**Created:** 2025-11-13  
**Status:** Production-ready  
**One command. Everything starts.**
