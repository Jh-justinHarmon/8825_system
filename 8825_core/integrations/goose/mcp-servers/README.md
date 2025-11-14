# MCP Servers for Goose Integration

**Purpose:** Bridge Goose AI agent with 8825 HCSS workflows  
**Protocol:** Model Context Protocol (MCP)  
**Status:** Ready for implementation

---

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI agents to external tools and data sources. It allows Goose to call your HCSS scripts as if they were native commands.

---

## Directory Structure

```
mcp-servers/
├── README.md              # This file
├── hcss-bridge/           # HCSS integration server
│   ├── server.js          # MCP server implementation
│   ├── package.json       # Node.js dependencies
│   ├── tools/             # Tool implementations
│   │   ├── ingest_gmail.js
│   │   ├── ingest_otter.js
│   │   ├── route_content.js
│   │   └── review_routed.js
│   └── README.md          # Server-specific docs
└── templates/             # Templates for new servers
    └── basic_server.js    # Starter template
```

---

## Available Servers

### hcss-bridge
**Status:** Ready to implement  
**Purpose:** Expose HCSS ingestion and routing tools to Goose  
**Tools:**
- `ingest_gmail` - Trigger Gmail ingestion
- `ingest_otter` - Trigger Otter.ai ingestion
- `route_content` - Route processed content
- `review_routed` - Review routed files

---

## Quick Start

### 1. Install Dependencies

```bash
cd mcp-servers/hcss-bridge
npm install
```

### 2. Test Server

```bash
node server.js
```

### 3. Configure in Goose

**Desktop UI:**
- Settings → MCP Servers → Add Server
- Name: `hcss-bridge`
- Command: `node`
- Args: `["/full/path/to/server.js"]`

**CLI:**
Edit `~/.config/goose/config.json`:
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

### 4. Use from Goose

```bash
goose session
> "Use ingest_gmail to check for new emails"
```

---

## Creating New MCP Servers

### 1. Copy Template

```bash
cp templates/basic_server.js my-server/server.js
```

### 2. Define Tools

```javascript
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'my_tool',
      description: 'What this tool does',
      inputSchema: {
        type: 'object',
        properties: {
          param1: { type: 'string', description: 'Parameter description' }
        },
        required: ['param1']
      }
    }
  ]
}));
```

### 3. Implement Tool Logic

```javascript
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'my_tool') {
    // Your implementation
    const result = await doSomething(args.param1);
    return {
      content: [{ type: 'text', text: result }]
    };
  }
});
```

### 4. Test & Deploy

```bash
node server.js  # Test locally
# Add to Goose config
# Use from Goose session
```

---

## Best Practices

### Tool Design
- **Single purpose:** Each tool does one thing well
- **Clear names:** Use verb_noun format (e.g., `ingest_gmail`)
- **Good descriptions:** Help Goose understand when to use the tool
- **Typed inputs:** Define clear input schemas

### Error Handling
- **Catch exceptions:** Don't let tools crash the server
- **Return errors:** Use error content type for failures
- **Log everything:** Help with debugging

### Performance
- **Async operations:** Use async/await for I/O
- **Timeouts:** Set reasonable timeouts
- **Resource limits:** Don't overwhelm the system

### Security
- **Validate inputs:** Check all parameters
- **Sanitize paths:** Prevent directory traversal
- **Limit scope:** Only expose necessary functionality

---

## Troubleshooting

### Server Won't Start
- Check Node.js version (need 18+)
- Verify dependencies installed
- Check for syntax errors

### Goose Can't Find Server
- Verify full path in config
- Check file permissions
- Test server manually first

### Tools Not Working
- Check tool implementation
- Verify script paths
- Check logs for errors

---

## Examples

### Example 1: Simple Tool

```javascript
{
  name: 'hello_world',
  description: 'Returns a greeting',
  inputSchema: {
    type: 'object',
    properties: {
      name: { type: 'string' }
    }
  }
}

// Implementation
if (name === 'hello_world') {
  return {
    content: [{
      type: 'text',
      text: `Hello, ${args.name}!`
    }]
  };
}
```

### Example 2: Script Execution

```javascript
{
  name: 'run_script',
  description: 'Executes a Python script',
  inputSchema: {
    type: 'object',
    properties: {
      script: { type: 'string' }
    }
  }
}

// Implementation
if (name === 'run_script') {
  const { execSync } = require('child_process');
  const result = execSync(`python3 ${args.script}`).toString();
  return {
    content: [{ type: 'text', text: result }]
  };
}
```

### Example 3: File Reading

```javascript
{
  name: 'read_file',
  description: 'Reads a file and returns contents',
  inputSchema: {
    type: 'object',
    properties: {
      path: { type: 'string' }
    }
  }
}

// Implementation
if (name === 'read_file') {
  const fs = require('fs');
  const content = fs.readFileSync(args.path, 'utf8');
  return {
    content: [{ type: 'text', text: content }]
  };
}
```

---

## Resources

### MCP Documentation
- Official docs: https://modelcontextprotocol.io
- SDK: https://github.com/modelcontextprotocol/sdk

### Goose Documentation
- Goose docs: https://block.github.io/goose
- MCP integration: https://block.github.io/goose/docs/mcp

### Examples
- Sample servers: https://github.com/modelcontextprotocol/servers
- Community servers: https://github.com/topics/mcp-server

---

## Next Steps

1. **Implement hcss-bridge server**
2. **Test with Goose CLI**
3. **Add more tools as needed**
4. **Create additional servers for other focuses**

---

## Support

For questions or issues:
1. Check this README
2. Review GOOSE_WINDSURF_INTEGRATION.md
3. Test server manually
4. Check Goose logs
