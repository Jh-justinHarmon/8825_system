#!/usr/bin/env python3
"""
Example DLI MCP Server

This is a reference implementation showing the DLI interface.
Replace the implementation with your own knowledge base and routing logic.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

server = Server("dli-router")

@server.call_tool()
async def dli_deep_dive(topic: str, mode: str = "pattern") -> dict:
    """
    Run a DLI deep dive.
    
    This is a reference implementation. You need to implement:
    1. Your knowledge base / Pattern Engine
    2. Cost optimization logic
    3. Model selection strategy
    4. Response formatting
    
    Args:
        topic: Question to research
        mode: "baseline" | "pattern" | "both"
    
    Returns:
        {
            "answer": str,
            "sources": list,
            "cost": float,
            "run_id": str
        }
    """
    
    # TODO: Replace with your implementation
    # Example:
    # results = await your_knowledge_base.search(topic)
    # answer = await your_llm.generate(topic, context=results)
    
    return {
        "answer": f"Example answer for: {topic}",
        "sources": ["source1.md", "source2.md"],
        "cost": 0.001,
        "run_id": "example-run-123",
        "note": "This is a reference implementation. Replace with your own logic."
    }

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
