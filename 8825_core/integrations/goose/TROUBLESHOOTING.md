# Goose Troubleshooting Guide

**Issue:** Model not enabled error  
**Fix:** Updated profiles.yaml with correct model names

---

## Common Issues

### 1. "Model is not enabled" Error

**Cause:** Incorrect model names in profiles.yaml

**Fix:**
```yaml
default:
  provider: openai
  processor: gpt-4-turbo-preview
  accelerator: gpt-3.5-turbo
  moderator: passive
  toolkits:
    - name: developer
```

**Steps:**
1. Edit `~/.config/goose/profiles.yaml`
2. Use standard OpenAI model names
3. Restart Goose app

---

### 2. MCP Server Not Found

**Cause:** Incorrect path in config.json

**Fix:**
```bash
cat ~/.config/goose/config.json
```

Verify full absolute path to server.js

---

### 3. Tools Not Working

**Cause:** MCP server not running or path issues

**Fix:**
```bash
cd goose_sandbox/mcp-servers/hcss-bridge
node server.js
# Should see: "HCSS MCP Bridge Server running on stdio"
```

---

### 4. OpenAI API Key Not Working

**Cause:** Key not in environment

**Fix:**
```bash
echo $OPENAI_API_KEY
# Should show your key

# If not:
source ~/.zshrc
```

---

## Quick Fixes

### Restart Goose Desktop
```bash
killall Goose
open -a Goose
```

### Verify Configuration
```bash
cat ~/.config/goose/profiles.yaml
cat ~/.config/goose/config.json
echo $OPENAI_API_KEY
```

### Test MCP Server
```bash
cd goose_sandbox/mcp-servers/hcss-bridge
node server.js
```

---

## Current Configuration

### profiles.yaml (Fixed)
```yaml
default:
  provider: openai
  processor: gpt-4-turbo-preview
  accelerator: gpt-3.5-turbo
  moderator: passive
  toolkits:
    - name: developer
```

### config.json
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

---

## After Restart

Try again in Goose Desktop:
```
Use check_status to see the HCSS system status
```

Should work now! ✅
