# DLI MCP Interface

This directory contains the reference implementation for the DLI (Dual-Layer Intelligence) MCP server interface.

## What's Included

- `schema.json` - MCP tool schema definition
- `example_server.py` - Reference implementation showing the interface
- `README.md` - This file

## What You Need to Implement

To build your own DLI system, you need:

1. **Knowledge Base** - Your indexed content (Pattern Engine or similar)
2. **Routing Logic** - When to use which knowledge source
3. **Cost Optimization** - Model selection based on query complexity
4. **Response Formatting** - Structure answers consistently

## Usage

See the [DLI Routing Protocol](../../core/protocols/DLI_ROUTING_PROTOCOL.md) for the complete methodology.

## Integration

Add this to your Windsurf MCP config:

```json
{
  "mcpServers": {
    "dli-router": {
      "command": "python",
      "args": ["/path/to/example_server.py"]
    }
  }
}
```

## License

MIT (see LICENSE in root)
