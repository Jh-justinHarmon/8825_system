#!/usr/bin/env python3
"""
AI Manifest MCP Server
Provides AI personality manifests and protocol content to any AI client

This server allows any AI (Windsurf, ChatGPT, Gemini, etc.) to query for:
- Its personality manifest
- Priority protocols to follow
- Interaction style guidelines
- Strengths and weaknesses
"""
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from manifest_provider import ManifestProvider
from protocol_loader import ProtocolLoader

# Initialize providers
BASE_DIR = Path(__file__).parent.parent.parent
MANIFESTS_DIR = BASE_DIR / "ai_manifests"
PROTOCOLS_DIR = BASE_DIR / "protocols"

print(f"Initializing AI Manifest MCP Server...", file=sys.stderr)
print(f"Manifests dir: {MANIFESTS_DIR}", file=sys.stderr)
print(f"Protocols dir: {PROTOCOLS_DIR}", file=sys.stderr)

manifest_provider = ManifestProvider(MANIFESTS_DIR)
protocol_loader = ProtocolLoader(PROTOCOLS_DIR)

# Create MCP server
server = Server("ai-manifest-server")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="get_my_manifest",
            description="Get AI personality manifest for current model. Returns behavior rules, interaction style, strengths/weaknesses.",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Model identifier (e.g., 'claude-3.5-sonnet-20240620', 'gpt-o1-mini')"
                    }
                },
                "required": ["model_id"]
            }
        ),
        types.Tool(
            name="list_available_models",
            description="List all AI models with manifests configured in the system",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_priority_protocols",
            description="Get full content of priority protocols that a model should follow",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Model identifier"
                    }
                },
                "required": ["model_id"]
            }
        ),
        types.Tool(
            name="get_interaction_style",
            description="Get recommended interaction style and behavior guidelines for a model",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Model identifier"
                    }
                },
                "required": ["model_id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if name == "get_my_manifest":
        model_id = arguments["model_id"]
        manifest = manifest_provider.get_manifest(model_id)
        
        if not manifest:
            available = manifest_provider.list_models()
            return [types.TextContent(
                type="text",
                text=f"No manifest found for model: {model_id}\n\nAvailable models:\n" + 
                     json.dumps(available, indent=2)
            )]
        
        return [types.TextContent(
            type="text",
            text=json.dumps(manifest, indent=2)
        )]
    
    elif name == "list_available_models":
        models = manifest_provider.list_models()
        return [types.TextContent(
            type="text",
            text=json.dumps(models, indent=2)
        )]
    
    elif name == "get_priority_protocols":
        model_id = arguments["model_id"]
        protocols = protocol_loader.get_priority_protocols(model_id, manifest_provider)
        
        # Format response with protocol contents
        response = f"# Priority Protocols for {model_id}\n\n"
        
        for protocol_name, protocol_data in protocols.items():
            response += f"## {protocol_name}\n\n"
            
            if "error" in protocol_data:
                response += f"❌ {protocol_data['error']}\n"
                if "expected_path" in protocol_data:
                    response += f"Expected at: {protocol_data['expected_path']}\n"
            else:
                response += f"✅ Loaded ({protocol_data.get('length', 0)} chars)\n\n"
                response += "```markdown\n"
                response += protocol_data.get('content', '')
                response += "\n```\n"
            
            response += "\n---\n\n"
        
        return [types.TextContent(type="text", text=response)]
    
    elif name == "get_interaction_style":
        model_id = arguments["model_id"]
        manifest = manifest_provider.get_manifest(model_id)
        
        if not manifest:
            return [types.TextContent(
                type="text",
                text=f"No manifest found for model: {model_id}"
            )]
        
        style = manifest.get("interaction_style", {})
        system_prompt = manifest.get("system_prompt_base", "")
        
        response = f"""# Interaction Style for {manifest.get('name', model_id)}

## Description
{manifest.get('description', 'No description available')}

## System Prompt Base
{system_prompt}

## Interaction Parameters
- **Default Sentiment Mode:** {style.get('default_sentiment_mode', 'N/A')}
- **Decision Confidence Threshold:** {style.get('decision_confidence_threshold', 'N/A')}
- **Ask vs Tell Ratio:** {style.get('ask_vs_tell_ratio', 'N/A')} (lower = more action, less asking)
- **Explanation Style:** {style.get('explanation_style', 'N/A')}

## Strengths
{chr(10).join('- ' + s for s in manifest.get('strengths', []))}

## Weaknesses
{chr(10).join('- ' + w for w in manifest.get('weaknesses', []))}

## Priority Protocols
{chr(10).join('- ' + p for p in manifest.get('priority_protocols', []))}

## Context Loading Strategy
- **Always Load:** {', '.join(manifest.get('context_loading_strategy', {}).get('always_load', []))}
- **On Demand:** {', '.join(manifest.get('context_loading_strategy', {}).get('on_demand', []))}
- **If Requested:** {', '.join(manifest.get('context_loading_strategy', {}).get('if_requested', []))}
"""
        
        return [types.TextContent(type="text", text=response)]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server"""
    print("Starting AI Manifest MCP Server...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
