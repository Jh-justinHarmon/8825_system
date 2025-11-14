# Install Goose + MCP Bridge - Complete Guide

**Goal:** Get Goose working with HCSS in Windsurf  
**Time:** 15 minutes  
**Status:** Step-by-step instructions

---

## Step 1: Install Goose CLI (5 min)

### Install via Homebrew

```bash
brew install block-goose-cli
```

### Verify Installation

```bash
goose --version
```

You should see the version number.

---

## Step 2: Configure Goose (3 min)

### Set OpenAI API Key

```bash
# Add to your shell config
echo 'export OPENAI_API_KEY=[REDACTED - Use 8825 key vault]' >> ~/.zshrc

# Reload shell config
source ~/.zshrc
```

### Run First Configuration

```bash
goose configure
```

Follow the prompts to set your LLM provider (OpenAI).

---

## Step 3: Install MCP Bridge Dependencies (3 min)

### Navigate to MCP Server Directory

```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system/goose_sandbox/mcp-servers/hcss-bridge"
```

### Install Node.js Dependencies

```bash
npm install
```

### Test Server

```bash
node server.js
```

You should see: `HCSS MCP Bridge Server running on stdio`

Press `Ctrl+C` to stop.

---

## Step 4: Configure MCP Server in Goose (4 min)

### Create/Edit Goose Config

```bash
mkdir -p ~/.config/goose
nano ~/.config/goose/config.json
```

### Add MCP Server Configuration

Paste this content:

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

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## Step 5: Test Integration (5 min)

### Start Goose Session in Windsurf Terminal

```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system"
goose session
```

### Test HCSS Tools

Try these commands in Goose:

```
> "Use check_status to see the HCSS system status"
> "Use list_recent_files to show me the latest processed files"
> "Use get_routing_stats to see project distribution"
```

If tools work, you're all set! ✅

---

## Verification Checklist

- [ ] Goose CLI installed (`goose --version` works)
- [ ] OpenAI API key configured
- [ ] MCP server dependencies installed (`npm install` completed)
- [ ] MCP server runs (`node server.js` works)
- [ ] Goose config created (`~/.config/goose/config.json` exists)
- [ ] Goose session starts (`goose session` works)
- [ ] HCSS tools accessible (can use `check_status`)

---

## Troubleshooting

### Issue: `goose: command not found`

**Fix:**
```bash
brew install block-goose-cli
# Restart terminal
```

### Issue: `Cannot find module '@modelcontextprotocol/sdk'`

**Fix:**
```bash
cd goose_sandbox/mcp-servers/hcss-bridge
npm install
```

### Issue: Goose can't find MCP server

**Fix:**
1. Verify path in `~/.config/goose/config.json`
2. Test server manually: `node server.js`
3. Check Node.js version: `node --version` (need 18+)

### Issue: Tools return errors

**Fix:**
1. Check HCSS scheduler is running: `launchctl list | grep hcss`
2. Verify files exist in `hcss_sandbox/raw/`
3. Check logs: `tail -f hcss_sandbox/logs/ingest.log`

---

## Quick Reference

### Start Goose Session
```bash
cd "/Users/justinharmon/.../windsurf-project - 8825 8825-system"
goose session
```

### Available HCSS Tools
- `check_status` - System status
- `ingest_gmail` - Trigger ingestion
- `list_recent_files` - Show recent files
- `read_corrections_log` - View corrections
- `get_routing_stats` - Routing statistics

### Exit Goose
```
> "exit"
```
or press `Ctrl+D`

---

## What's Next?

### Try These Commands

```
> "Analyze the HCSS routing logic and suggest improvements"
> "Review the correction rules and identify patterns"
> "Generate a summary of today's email processing"
> "Check if there are any low-confidence routing decisions"
```

### Explore the Codebase

```
> "Explain how the Gmail extractor works"
> "Show me the routing algorithm"
> "What corrections are most common?"
```

### Automate Tasks

```
> "Run ingestion and summarize new items"
> "Check status and alert if anything is wrong"
> "Generate a weekly processing report"
```

---

## Summary

✅ **Goose CLI** - Installed and configured  
✅ **MCP Bridge** - Running and connected  
✅ **HCSS Tools** - Available in Goose  
✅ **Integration** - Complete

**You can now use Goose as an AI assistant for HCSS development and operations!**

---

## Files Created

- `~/.config/goose/config.json` - Goose configuration
- `goose_sandbox/mcp-servers/hcss-bridge/` - MCP server
- Environment variable in `~/.zshrc` - OpenAI API key

---

## Support

For help:
1. Check `mcp-servers/hcss-bridge/README.md`
2. Review `GOOSE_WINDSURF_INTEGRATION.md`
3. Test components individually
4. Check Goose logs: `~/.config/goose/logs/`
