# Windsurf Workflows

Quick reference for available workflows.

## Available Workflows

### `/launch-8825`
**Purpose:** Start 8825 unified startup system  
**What it does:** Runs 7-phase startup (governance, brain daemon, MCP servers)  
**When to use:** At start of session to activate 8825 mode

### `/collab`
**Purpose:** Start collaborative dev cycle  
**What it does:** 6-phase structured ideation → research → planning → execution  
**When to use:** When you have an idea to develop or want to figure something out  
**Aliases:** Also recognizes `[collab]`, `[LFG]`, `[let's make]`

### `/cleanup-inbox`
**Purpose:** Clean up Downloads inbox  
**What it does:** Processes and archives files from Downloads  
**When to use:** After processing files, to maintain clean inbox

## Workflow Features

All workflows support:
- **// turbo** annotation - Auto-runs without confirmation when safe
- **Manual override** - Type commands manually if needed
- **Documentation** - Each has full protocol in `8825_core/protocols/`

## Creating New Workflows

1. Create markdown file in `.windsurf/workflows/`
2. Add YAML frontmatter with description
3. Add `// turbo` annotation for auto-run steps
4. Document in `8825_core/protocols/` for full details

Example:
```markdown
---
description: Brief description of workflow
---

# Workflow Name

Description of what it does.

// turbo
1. Execute command
```bash
echo "Command here"
```
```

## Learn More

- **Workflow Protocol:** `8825_core/protocols/WORKFLOW_ORCHESTRATION_PROTOCOL.md`
- **Collab Cycle:** `8825_core/protocols/COLLAB_CYCLE_PROTOCOL.md`
- **Startup Guide:** `8825_core/system/LAUNCH_8825_MODE.md`
