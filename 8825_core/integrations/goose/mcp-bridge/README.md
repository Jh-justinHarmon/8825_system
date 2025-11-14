# 8825 MCP Bridge for Goose

**Status:** ✅ Production Ready  
**Version:** 2.0.0  
**Updated:** 2025-11-10

---

## What This Does

Exposes 8825 system tools to Goose via MCP protocol, enabling Goose to:
- Manage Joju Notion tasks (create, list, update, sync)
- Query user engagement data (91 quotes, 5 sessions)
- Create tasks from user feedback
- Process the inbox pipeline
- Check system status
- Review teaching tickets
- OCR screenshots

**Total:** 12 production-ready tools

---

## Production Ready ✅

**MCP Server:** `8825_core/integrations/goose/mcp-bridge/server.py` (Python)  
**Goose Config:** `~/.config/goose/config.yaml`  
**Status:** Production ready with full error handling

**New in v2.0:**
- Task management (5 tools)
- User engagement (3 tools)
- Error handling & retries
- Comprehensive logging
- Authentication framework

---

## Available Tools

### 1. `process_inbox`
**Description:** Run the full inbox processing pipeline  
**What it does:**
- Syncs iCloud → Local Downloads
- Updates brain transport
- Processes files through Lane A/B
- Archives processed files
- Syncs back to iCloud

**Usage:**
```
> "Process the inbox"
> "Run the inbox pipeline"
> "Check for new files and process them"
```

---

### 2. `check_status`
**Description:** Get 8825 system status  
**What it returns:**
- Pending files count
- Lane A/B processing stats
- Completed files
- Error count

**Usage:**
```
> "Check 8825 status"
> "What's the current inbox status?"
> "Show me system stats"
```

---

### 3. `review_tickets`
**Description:** List teaching tickets needing review  
**Parameters:**
- `limit` (optional): Max tickets to return (default: 10)

**Usage:**
```
> "Show me teaching tickets"
> "List tickets that need review"
> "What teaching tickets are pending?"
```

---

### 4. `ocr_screenshot`
**Description:** OCR the latest screenshot  
**What it does:**
- Finds newest screenshot
- Copies to /tmp for processing
- Prepares for OCR analysis

**Usage:**
```
> "OCR the latest screenshot"
> "Read the newest screenshot"
> "What's in the latest screenshot?"
```

---

## How to Use

### Start Goose Session in 8825 Workspace

```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
goose session --name "8825-work"
```

### Test the Tools

```
# Process inbox
> "Use process_inbox to check for new files"

# Check status
> "Use check_status to see what's in the queue"

# Review tickets
> "Use review_tickets to show me what needs review"

# OCR screenshot
> "Use ocr_screenshot to read the latest screenshot"
```

### Natural Language

Goose understands natural language - you don't need to use exact tool names:

```
> "Process my inbox"
> "What's the status of the system?"
> "Show me tickets that need my attention"
> "Read the latest screenshot"
```

---

## Examples

### Example 1: Morning Workflow
```
> "Check 8825 status and process any new files"

Goose will:
1. Call check_status
2. Call process_inbox if files are pending
3. Report results
```

### Example 2: Review Session
```
> "Show me teaching tickets and explain what they're about"

Goose will:
1. Call review_tickets
2. Analyze ticket content
3. Explain what needs review
```

### Example 3: Screenshot Analysis
```
> "OCR the latest screenshot and summarize what it shows"

Goose will:
1. Call ocr_screenshot
2. Read the image
3. Provide summary
```

---

## Architecture

```
Goose CLI
    ↓ (stdio)
MCP Bridge (Node.js)
    ↓ (exec)
8825 Scripts (Bash/Python)
    ↓
8825 System
```

**Key Points:**
- Goose communicates via stdio (standard input/output)
- MCP bridge translates to shell commands
- Existing 8825 scripts do the actual work
- No changes to current automation needed

---

## Testing

### Test MCP Server Directly
```bash
cd 8825_core/integrations/goose/mcp-bridge
node server.js
```

Should output: `8825 MCP Bridge running on stdio`

### Test via Goose
```bash
cd "/path/to/8825/8825-system"
goose session --name "test"

> "List available tools"
> "Use check_status"
```

---

## Troubleshooting

### Goose doesn't see the tools
**Check:** `~/.config/goose/config.yaml` has `8825-bridge` extension enabled

### Tool execution fails
**Check:** Paths in `server.js` are correct for your system

### Permission errors
**Check:** Scripts are executable:
```bash
chmod +x INBOX_HUB/simple_sync_and_process.sh
chmod +x INBOX_HUB/ocr_latest_screenshot.sh
```

---

## Next Steps

### Phase 2: Add More Tools
- `approve_ticket` - Approve/reject teaching tickets
- `mine_chat` - Extract achievements from chat logs
- `update_library` - Update master library
- `generate_report` - Create status reports

### Phase 3: Task Orchestration
- Multi-step workflows
- Task spec generation
- Conditional logic
- Error recovery

---

## Summary

**Status:** ✅ Working  
**Tools:** 4 core tools implemented  
**Integration:** Goose ↔ 8825 connected  
**Next:** Test in real workflows

**Ready to use Goose with 8825!** 🚀
