# Goose CLI + Desktop Integration Guide

**Status:** ✅ Both Installed and Linked  
**Configuration:** Shared between both

---

## How They're Integrated

### Shared Configuration Files

Both CLI and Desktop use the **same config directory:**

```
~/.config/goose/
├── config.json          # MCP servers (shared)
├── profiles.yaml        # LLM provider (shared)
└── logs/                # Session logs (shared)
```

**This means:**
- Configure MCP server once → works in both ✅
- Set OpenAI key once → works in both ✅
- Same tools available in both ✅

---

## Current Setup

### ✅ CLI (Windsurf Terminal)
**Installed:** v1.12.1  
**Config:** `~/.config/goose/config.json`  
**MCP Server:** hcss-bridge configured  
**Usage:** `goose session` in terminal

### ✅ Desktop (Goose.app)
**Installed:** v1.12.1  
**Config:** Same `~/.config/goose/config.json`  
**MCP Server:** Already configured (shared)  
**Usage:** Open Goose app

---

## Verification: Check Shared Config

### 1. Check Config File
```bash
cat ~/.config/goose/config.json
```

**Should show:**
```json
{
  "mcpServers": {
    "hcss-bridge": {
      "command": "node",
      "args": ["/full/path/to/server.js"]
    }
  }
}
```

### 2. Check Profile
```bash
cat ~/.config/goose/profiles.yaml
```

**Should show:**
```yaml
default:
  provider: openai
  processor: gpt-4o
  accelerator: gpt-4o-mini
```

### 3. Verify in Desktop UI
1. Open Goose app
2. Click Settings (gear icon)
3. Go to "MCP Servers"
4. Should see: `hcss-bridge` already configured ✅

---

## Using Both Together

### Workflow Pattern

**CLI (Windsurf)** → Development work
```bash
cd "/Users/justinharmon/.../windsurf-project - 8825 8825-system"
goose session
> "Review this code and suggest improvements"
> "Use check_status to see system health"
```

**Desktop** → Planning & exploration
```
Open Goose app
→ "Explain the HCSS architecture"
→ "Generate a weekly summary report"
→ "What should I work on next?"
```

### Seamless Switching

**Scenario 1: Start in CLI, continue in Desktop**
1. Work in CLI: `goose session`
2. Ask complex question
3. Switch to Desktop for better visualization
4. Same context, same tools ✅

**Scenario 2: Start in Desktop, implement in CLI**
1. Plan in Desktop: "How should I improve routing?"
2. Get recommendations
3. Switch to CLI in Windsurf
4. Implement changes with Goose assistance

---

## Desktop UI Features

### What Desktop Adds

**Visual Interface:**
- Chat history (see past conversations)
- File browser (visual navigation)
- Settings UI (easier configuration)
- Session management (multiple sessions)

**Better For:**
- Learning and exploration
- Showing to others
- Non-technical queries
- Report generation

### What CLI Offers

**Terminal Integration:**
- Deep workspace context
- Faster for developers
- Better for coding tasks
- Integrated with Windsurf

**Better For:**
- Active development
- Code review
- Debugging
- Quick commands

---

## Configuration in Desktop UI

### To Verify MCP Server in Desktop:

1. **Open Goose app**
2. **Click Settings** (gear icon, bottom left)
3. **Go to "MCP Servers" tab**
4. **Should see:**
   - Name: `hcss-bridge`
   - Command: `node`
   - Args: `/full/path/to/server.js`
   - Status: ✅ Connected

### To Test Tools in Desktop:

1. **Start new session** (+ button)
2. **Try command:**
   ```
   Use check_status to see the HCSS system status
   ```
3. **Should work!** Same tools as CLI ✅

---

## Shared Features

### Both Have Access To:

**HCSS Tools (via MCP):**
- ✅ check_status
- ✅ ingest_gmail
- ✅ list_recent_files
- ✅ read_corrections_log
- ✅ get_routing_stats

**Workspace Context:**
- ✅ Can read files
- ✅ Can analyze code
- ✅ Can suggest improvements
- ✅ Can generate documentation

**OpenAI Models:**
- ✅ GPT-4o for main processing
- ✅ GPT-4o-mini for acceleration
- ✅ Same API key

---

## Example Workflows

### Workflow 1: Morning Check
**Desktop:**
```
Open Goose app
→ "Use check_status and give me a morning briefing"
→ "Use get_routing_stats and show trends"
→ "Any issues I should address today?"
```

### Workflow 2: Development
**CLI (Windsurf):**
```bash
goose session
> "Review the routing algorithm"
> "Suggest performance improvements"
> "Generate tests for the new feature"
```

### Workflow 3: Analysis
**Desktop:**
```
→ "Use read_corrections_log with lines=500"
→ "Analyze the correction patterns"
→ "What rules should we add?"
→ "Generate a report"
```

### Workflow 4: Troubleshooting
**CLI (Windsurf):**
```bash
goose session
> "Use check_status"
> "Why did routing fail for this email?"
> "Show me the logs"
> "Suggest a fix"
```

---

## Session Continuity

### Sessions Are Independent

**CLI sessions:**
- Stored in `~/.config/goose/logs/`
- Can be resumed with `goose session resume`

**Desktop sessions:**
- Stored in same location
- Visible in Desktop UI sidebar
- Can switch between sessions

**Note:** Sessions don't auto-sync between CLI and Desktop, but they share:
- Configuration ✅
- MCP servers ✅
- Tools ✅
- API keys ✅

---

## Best Practices

### Use CLI When:
- ✅ Actively coding
- ✅ Need terminal integration
- ✅ Quick status checks
- ✅ Code review in progress

### Use Desktop When:
- ✅ Planning features
- ✅ Learning the system
- ✅ Generating reports
- ✅ Showing to others
- ✅ Complex analysis

### Use Both When:
- ✅ Start planning in Desktop
- ✅ Implement in CLI
- ✅ Review results in Desktop
- ✅ Document in Desktop

---

## Troubleshooting

### Desktop Can't Find MCP Server

**Check:**
```bash
cat ~/.config/goose/config.json
```

**Fix:** Ensure full absolute path in config

### Tools Work in CLI but Not Desktop

**Restart Desktop:**
1. Quit Goose app
2. Reopen
3. Check Settings → MCP Servers
4. Should auto-load from config

### Different Behavior Between CLI and Desktop

**Normal!** They use the same backend but:
- CLI has terminal context
- Desktop has visual context
- Both have same tools ✅

---

## Quick Reference

### Start CLI
```bash
cd "/Users/justinharmon/.../windsurf-project - 8825 8825-system"
goose session
```

### Start Desktop
```bash
open -a Goose
```

### Check Config
```bash
cat ~/.config/goose/config.json
cat ~/.config/goose/profiles.yaml
```

### Test Tools (Both)
```
Use check_status
```

---

## Summary

**Integration:** ✅ Complete  
**Shared Config:** ✅ Both use `~/.config/goose/`  
**MCP Server:** ✅ Available in both  
**HCSS Tools:** ✅ Same 5 tools in both  

**You can now:**
- Use CLI for development in Windsurf ✅
- Use Desktop for planning and exploration ✅
- Switch between them seamlessly ✅
- Same tools, same context, same power ✅

---

## Next Steps

1. **Try Desktop:** Open Goose app, test `Use check_status`
2. **Try CLI:** Run `goose session` in Windsurf terminal
3. **Compare:** See which you prefer for different tasks
4. **Use Both:** Leverage strengths of each

**Both are ready to use right now!** 🎉
