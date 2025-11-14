# Link Goose to Entire v2.1 Workspace

**Goal:** Give Goose full context of your entire project  
**Benefit:** Goose can see and work with all files, not just one directory

---

## ✅ Already Set Up!

The MCP server is already configured to work with the full v2.1 workspace.

---

## How to Use

### Method 1: CLI in Windsurf (Best for Development)

**Quick start script created:**
```bash
./start_goose.sh
```

Or manually:
```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system"
goose session start
```

**What Goose Can See:**
- ✅ All files in v2.1 folder
- ✅ hcss_sandbox/
- ✅ goose_sandbox/
- ✅ protocols/
- ✅ All subdirectories
- ✅ Full project context

---

### Method 2: Desktop App (Best for Exploration)

**Option A: Set Working Directory**
1. Open Goose app
2. Click folder icon (bottom left)
3. Navigate to: `/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system`
4. Select folder
5. Start session

**Option B: Open from Finder**
1. Right-click v2.1 folder in Finder
2. Services → Open with Goose (if available)
3. Or drag folder into Goose app

---

## What Goose Can Do With Full Context

### Code Analysis
```
Analyze the entire HCSS architecture
Show me all the routing logic across all files
Find all places where corrections are applied
Map out the data flow from Gmail to archives
```

### Cross-File Operations
```
Find all references to "routing" across the project
Show me how the protocols connect to the sandbox
List all Python scripts and their purposes
Generate a project structure diagram
```

### Development
```
Review the entire codebase for improvements
Suggest refactoring opportunities
Find duplicate code
Identify missing documentation
```

### HCSS Tools (via MCP)
```
Use check_status
Use list_recent_files
Use get_routing_stats
Use ingest_gmail
Use read_corrections_log
```

---

## Workspace Structure Goose Will See

```
windsurf-project - 8825 8825-system/
├── hcss_sandbox/              ← HCSS workflows
│   ├── 8825_gmail_extractor.py
│   ├── raw/
│   ├── mined/
│   └── archives/
├── goose_sandbox/             ← Goose Focus
│   ├── mcp-servers/
│   │   └── hcss-bridge/      ← MCP server
│   ├── config/
│   └── logs/
├── protocols/                 ← Mode definitions
│   ├── 8825_mode_activation.json
│   ├── 8825_hcss_focus.json
│   └── 8825_goose_focus.json
├── joju_sandbox/             ← Joju workflows
└── start_goose.sh            ← Quick start script
```

---

## Example Commands with Full Context

### Understand the System
```
Explain how the entire 8825 system works, from Gmail ingestion to archiving
```

### Find Things
```
Where is the routing logic defined?
Show me all files that use OpenAI API
Find all correction rules across the project
```

### Analyze
```
Use get_routing_stats and analyze if the routing is working well
Review all the protocols and explain how they relate
Map out the complete data flow
```

### Improve
```
Suggest improvements to the overall architecture
Find opportunities for code reuse
Identify missing error handling
```

---

## CLI vs Desktop with Full Context

### CLI (Windsurf Terminal)
**Best for:**
- Active development
- Code editing
- Running commands
- Deep integration

**Start:**
```bash
cd "/Users/justinharmon/.../windsurf-project - 8825 8825-system"
goose session start
```

### Desktop App
**Best for:**
- Exploration
- Learning
- Planning
- Visual navigation

**Start:**
1. Open Goose app
2. Set working directory to v2.1 folder
3. Start session

---

## MCP Server Already Has Full Access

The MCP server (`hcss-bridge`) is already configured with full paths:

```javascript
const HCSS_SANDBOX = join(__dirname, '../../../hcss_sandbox');
```

This means:
- ✅ MCP tools work from anywhere
- ✅ Full project access
- ✅ No additional config needed

---

## Quick Start

### In Windsurf Terminal
```bash
# Use the quick start script
./start_goose.sh

# Or manually
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/windsurf-project - 8825 8825-system"
goose session start
```

### First Commands to Try
```
> "Explain the structure of this project"
> "Use check_status to see HCSS health"
> "Show me all the protocols and what they do"
> "Analyze the routing accuracy"
```

---

## Benefits of Full Context

### Before (Single Directory)
- Limited file access
- Can't see relationships
- Partial understanding
- Manual navigation

### After (Full v2.1 Workspace)
- ✅ See entire project
- ✅ Understand relationships
- ✅ Cross-file analysis
- ✅ Complete context
- ✅ Better suggestions
- ✅ Smarter assistance

---

## Privacy & Security

**What Goose Can See:**
- All files in v2.1 folder
- File contents when you ask
- Directory structure

**What Goose Can't See:**
- Files outside v2.1 folder
- System files
- Other projects

**What Gets Sent to OpenAI:**
- Only what you explicitly ask about
- Not automatic scanning
- You control what's shared

---

## Testing Full Context

### Test 1: Project Understanding
```
Explain the overall architecture of this project
```

### Test 2: Cross-File Analysis
```
Find all places where routing decisions are made
```

### Test 3: HCSS Tools
```
Use check_status and list_recent_files, then analyze the system health
```

### Test 4: Code Search
```
Show me all Python scripts and what they do
```

---

## Summary

**Status:** ✅ Already configured for full v2.1 access

**CLI:** Use `./start_goose.sh` or `cd` to v2.1 folder  
**Desktop:** Set working directory to v2.1 folder  
**MCP Tools:** Already have full access  

**Goose can now:**
- See entire project structure ✅
- Analyze across all files ✅
- Use HCSS tools ✅
- Provide better assistance ✅

---

## Next Steps

1. **Start Goose** in v2.1 folder
2. **Test context:** "Explain this project"
3. **Use tools:** "Use check_status"
4. **Explore:** Ask about any file or feature

**Full workspace context = Much better AI assistance!** 🎯
