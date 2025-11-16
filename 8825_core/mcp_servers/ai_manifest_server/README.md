# AI Manifest MCP Server

Universal MCP server that provides AI personality manifests and protocol content to any AI client.

## Purpose

Normalizes AI behavior across different models (Claude, GPT, Gemini) by providing:
- Model-specific personality manifests
- Priority protocols to follow
- Interaction style guidelines
- Strengths and weaknesses awareness

## Architecture

```
AI Client (Windsurf/ChatGPT/etc)
    ↓ (queries via MCP)
AI Manifest Server
    ↓ (reads from)
8825_core/ai_manifests/*.json
8825_core/protocols/*.md
```

## Available Tools

### `get_my_manifest(model_id)`
Get full personality manifest for a specific AI model.

**Example:**
```python
get_my_manifest(model_id="claude-3.5-sonnet-20240620")
```

**Returns:**
```json
{
  "model_id": "claude-3.5-sonnet-20240620",
  "name": "Sonnet (The Implementer)",
  "description": "Optimized for speed, directness, and code implementation",
  "system_prompt_base": "You are Cascade...",
  "priority_protocols": [...],
  "interaction_style": {...},
  "strengths": [...],
  "weaknesses": [...]
}
```

### `list_available_models()`
List all AI models with configured manifests.

**Returns:**
```json
[
  {
    "model_id": "claude-3.5-sonnet-20240620",
    "name": "Sonnet (The Implementer)",
    "description": "Optimized for speed..."
  },
  {
    "model_id": "gpt-o1-mini",
    "name": "Omni (The Architect)",
    "description": "Optimized for deep reasoning..."
  }
]
```

### `get_priority_protocols(model_id)`
Get full content of priority protocols that a model should follow.

**Example:**
```python
get_priority_protocols(model_id="claude-3.5-sonnet-20240620")
```

**Returns:** Full markdown content of each priority protocol file.

### `get_interaction_style(model_id)`
Get recommended interaction style and behavior guidelines.

**Returns:** Formatted guide with:
- System prompt base
- Interaction parameters
- Strengths/weaknesses
- Priority protocols list
- Context loading strategy

## Installation

### 1. Install Dependencies
```bash
cd 8825_core/mcp_servers/ai_manifest_server
pip install -r requirements.txt
```

### 2. Configure Windsurf

Add to `.windsurf/mcp_settings.json`:

```json
{
  "mcpServers": {
    "ai-manifest": {
      "command": "python3",
      "args": [
        "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/mcp_servers/ai_manifest_server/server.py"
      ]
    }
  }
}
```

### 3. Restart Windsurf

The server will auto-start when Windsurf launches.

## Usage in Windsurf

Once configured, you (the AI) can call these tools:

```
At session start:
1. Call get_my_manifest(model_id="claude-3.5-sonnet-20240620")
2. Call get_priority_protocols(model_id="claude-3.5-sonnet-20240620")
3. Apply the rules from the manifest
```

## Usage in Other AI Platforms

### ChatGPT (with MCP support)
Same configuration, different model_id:
```python
get_my_manifest(model_id="gpt-o1-mini")
```

### Gemini (with MCP support)
Create a manifest for Gemini and query it:
```python
get_my_manifest(model_id="gemini-1.5-pro")
```

## Testing

### Test Server Locally
```bash
cd 8825_core/mcp_servers/ai_manifest_server
python3 server.py
```

Should start without errors and wait for MCP protocol messages.

### Test in Windsurf
1. Restart Windsurf
2. In chat, try calling the tools
3. Verify you get manifest data back

## File Structure

```
ai_manifest_server/
├── server.py              # Main MCP server
├── manifest_provider.py   # Loads manifests from JSON
├── protocol_loader.py     # Loads protocol files
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Adding New AI Models

1. Create manifest file:
```bash
8825_core/ai_manifests/your_model.json
```

2. Follow the structure:
```json
{
  "model_id": "your-model-id",
  "name": "Model Name",
  "description": "What this model is good at",
  "system_prompt_base": "Base instructions...",
  "priority_protocols": [
    "PROTOCOL1.md",
    "PROTOCOL2.md"
  ],
  "interaction_style": {
    "default_sentiment_mode": "Yellow (Urgent)",
    "decision_confidence_threshold": 0.7,
    "ask_vs_tell_ratio": 0.2,
    "explanation_style": "minimal"
  },
  "strengths": ["list", "of", "strengths"],
  "weaknesses": ["list", "of", "weaknesses"]
}
```

3. Restart the MCP server (or Windsurf)

## Troubleshooting

### Server won't start
- Check Python 3 is installed: `python3 --version`
- Check mcp package installed: `pip list | grep mcp`
- Check file paths in mcp_settings.json are absolute

### Tools not available in Windsurf
- Verify mcp_settings.json is in `.windsurf/` directory
- Check Windsurf console for MCP errors
- Restart Windsurf completely

### Manifest not found
- Check model_id matches exactly (case-sensitive)
- Verify JSON file exists in `8825_core/ai_manifests/`
- Check JSON is valid: `python3 -m json.tool your_manifest.json`

### Protocol file not found
- Check protocol filename in manifest matches actual file
- Verify file exists in `8825_core/protocols/`
- Check file extension (.md)

## Benefits

### For AI Models
- Clear behavior guidelines
- Consistent interaction style
- Awareness of strengths/weaknesses
- Priority protocols to follow

### For Users
- Predictable AI behavior
- Less "dramatic switches" between sessions
- Consistent experience across platforms
- Customizable per model

### For System
- Centralized configuration
- Easy to add new models
- Version controlled manifests
- Auditable behavior rules

## Future Enhancements

- [ ] Auto-detect model from MCP client
- [ ] Dynamic protocol loading based on task
- [ ] Manifest versioning
- [ ] A/B testing different interaction styles
- [ ] Analytics on which protocols are most effective

## Related Files

- `8825_core/ai_manifests/` - Manifest JSON files
- `8825_core/protocols/` - Protocol markdown files
- `8825_core/brain/manifest_loader.py` - Original loader (terminal-based)
- `8825_core/system/8825_unified_startup.sh` - Startup integration

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Created:** 2025-11-14  
**Last Updated:** 2025-11-14
