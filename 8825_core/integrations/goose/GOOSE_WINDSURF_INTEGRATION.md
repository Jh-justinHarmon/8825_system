# Goose + Windsurf Integration Plan

**Created:** 2025-11-06  
**Status:** Implementation Ready  
**Purpose:** Bridge Goose AI agent with 8825 HCSS workflows

---

## Overview

Integrate Goose (AI agent) with Windsurf IDE and existing 8825 HCSS workflows through MCP (Model Context Protocol) servers. This allows Goose to orchestrate HCSS tasks while keeping the proven launchd scheduling for background automation.

---

## Architecture

```
Windsurf IDE
    ↓
Goose CLI (in terminal)
    ↓
MCP Server (bridge)
    ↓
8825 HCSS Scripts (existing)
    ↓
Gmail/Otter/Processing
```

---

## Installation Steps

### 1. Install Goose (macOS)

**Desktop UI:**
```bash
brew install --cask block-goose
open -a Goose
```

**CLI (for Windsurf terminal):**
```bash
brew install block-goose-cli
goose --version
```

### 2. Configure Goose

**First run:**
```bash
goose configure
```

**Set OpenAI key (zsh):**
```bash
echo 'export OPENAI_API_KEY=[REDACTED - Use 8825 key vault]' >> ~/.zshrc
source ~/.zshrc
goose configure
```

### 3. Run Goose from Windsurf Terminal

```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system"
goose session
```

Goose now has context of your entire 8825 workspace!

---

## Project Structure

```
goose_sandbox/
├── mcp-servers/           # MCP bridge servers
│   ├── hcss-bridge/       # HCSS integration
│   │   ├── server.js      # Node.js MCP server
│   │   ├── package.json   # Dependencies
│   │   └── tools/         # Tool implementations
│   │       ├── ingest_gmail.js
│   │       ├── ingest_otter.js
│   │       ├── route_content.js
│   │       └── review_routed.js
│   └── README.md          # MCP server docs
│
├── scripts/               # Helper scripts
│   ├── goose_wrapper.sh   # Wrapper for HCSS commands
│   └── status_check.sh    # Check system status
│
└── docs/                  # Usage documentation
    ├── goose_commands.md  # Available commands
    └── examples.md        # Usage examples
```

---

## MCP Bridge Tools

### Tool 1: ingest_gmail
**Purpose:** Trigger Gmail ingestion  
**Command:** Runs `8825_gmail_extractor.py`  
**Returns:** Count of new emails processed

### Tool 2: ingest_otter
**Purpose:** Trigger Otter.ai ingestion  
**Command:** Runs `8825_otter_extractor.py`  
**Returns:** Count of new transcripts processed

### Tool 3: route_content
**Purpose:** Route processed content to projects  
**Command:** Runs routing logic  
**Returns:** Routing summary (TGIF/RAL/LHL/76)

### Tool 4: review_routed
**Purpose:** Review routed content  
**Command:** Lists recent files by project  
**Returns:** File list with metadata

---

## Usage Patterns

### Pattern 1: Day-to-Day Development
**Use:** Windsurf + Goose CLI  
**Benefit:** Repo-aware agent sessions  
**Example:**
```bash
# In Windsurf terminal
goose session
> "Analyze the HCSS routing logic and suggest improvements"
```

### Pattern 2: Interactive Assistance
**Use:** Goose Desktop UI  
**Benefit:** Broader UX, ad-hoc queries  
**Example:** Open Goose app, ask questions about codebase

### Pattern 3: Background Automation
**Use:** launchd (existing)  
**Benefit:** Reliable polling without webhooks  
**Status:** Already running (every 5 minutes)

---

## Integration Benefits

### For Development
- **Context-aware:** Goose sees entire 8825 workspace
- **Code analysis:** Ask Goose to review/refactor code
- **Scaffolding:** Generate new components
- **Documentation:** Auto-generate docs

### For Operations
- **Orchestration:** "Ingest Gmail and summarize new items"
- **Status checks:** "What's the current HCSS status?"
- **Troubleshooting:** "Why did routing fail?"
- **Reporting:** "Generate summary of today's processing"

### For Maintenance
- **Code review:** Automated suggestions
- **Testing:** Generate test cases
- **Refactoring:** Suggest improvements
- **Documentation:** Keep docs updated

---

## Implementation Plan

### Phase 1: Basic MCP Bridge (Now)
- [ ] Create MCP server structure
- [ ] Implement `ingest_gmail` tool
- [ ] Implement `ingest_otter` tool
- [ ] Test from Goose CLI
- [ ] Document usage

### Phase 2: Enhanced Tools (Next)
- [ ] Add `route_content` tool
- [ ] Add `review_routed` tool
- [ ] Add `status_check` tool
- [ ] Add `generate_report` tool

### Phase 3: Advanced Features (Future)
- [ ] Real-time monitoring
- [ ] Automated responses
- [ ] Learning from corrections
- [ ] Predictive routing

---

## MCP Server Configuration

### Node.js Server (Recommended)

**Dependencies:**
```json
{
  "name": "hcss-mcp-bridge",
  "version": "1.0.0",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.1.0",
    "child_process": "^1.0.2"
  }
}
```

**Server Structure:**
```javascript
// server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'hcss-bridge',
  version: '1.0.0'
});

// Register tools
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'ingest_gmail',
      description: 'Ingest new Gmail/Otter emails',
      inputSchema: { type: 'object', properties: {} }
    },
    // ... more tools
  ]
}));

// Tool execution
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'ingest_gmail') {
    // Execute Python script
    const result = await executeScript('../hcss_sandbox/8825_gmail_extractor.py');
    return { content: [{ type: 'text', text: result }] };
  }
  
  // ... more tool handlers
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Goose Configuration

### Add MCP Server to Goose

**Desktop UI:**
1. Open Goose
2. Settings → MCP Servers
3. Add server:
   - Name: `hcss-bridge`
   - Command: `node`
   - Args: `["/path/to/goose_sandbox/mcp-servers/hcss-bridge/server.js"]`

**CLI Configuration:**
```json
// ~/.config/goose/config.json
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

## Example Usage

### From Goose CLI

```bash
# Start Goose session in Windsurf terminal
cd "/Users/justinharmon/.../windsurf-project - 8825 8825-system"
goose session

# Ask Goose to use tools
> "Use ingest_gmail to check for new emails"
> "Summarize the routing decisions from today"
> "Show me the latest TGIF files"
> "Generate a report of this week's processing"
```

### From Goose Desktop

```
Open Goose app
→ "Connect to my 8825 workspace"
→ "Run ingest_gmail and tell me what's new"
→ "Analyze the HCSS routing accuracy"
→ "Suggest improvements to the correction rules"
```

---

## When to Use Each Tool

### Windsurf + Goose CLI
- ✅ Day-to-day development
- ✅ Code review and refactoring
- ✅ Repo-aware analysis
- ✅ Quick queries about codebase

### Goose Desktop
- ✅ Ad-hoc interactive assistance
- ✅ Broader questions
- ✅ Learning about the system
- ✅ Exploratory analysis

### launchd (Existing)
- ✅ Reliable background polling
- ✅ Scheduled automation
- ✅ No manual intervention
- ✅ Production reliability

---

## Next Steps

### Immediate
1. Install Goose CLI: `brew install block-goose-cli`
2. Configure with OpenAI key
3. Test basic session in Windsurf terminal

### Short-term
1. Build MCP server structure
2. Implement basic tools
3. Test integration
4. Document usage

### Long-term
1. Add advanced tools
2. Enhance with learning
3. Build monitoring
4. Optimize workflows

---

## Summary

**Integration Model:**
- Goose = Orchestrator (interactive, context-aware)
- MCP Server = Bridge (exposes HCSS tools)
- 8825 Scripts = Implementation (existing, proven)
- launchd = Automation (background, reliable)

**Benefits:**
- ✅ Best of both worlds
- ✅ No disruption to existing automation
- ✅ Enhanced development experience
- ✅ Context-aware AI assistance

**Ready to implement MCP bridge?**
