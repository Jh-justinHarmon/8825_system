#!/usr/bin/env python3
"""
RAL Portal MCP Server
Provides AI-accessible documentation for RAL Portal system
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent


# Path to RAL Portal knowledge base
KNOWLEDGE_BASE = Path(__file__).parent.parent.parent / "focuses/hcss/knowledge"


class RALPortalMCPServer:
    """MCP Server for RAL Portal documentation"""
    
    def __init__(self):
        self.server = Server("ral-portal")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Register MCP handlers"""
        
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List all RAL Portal documentation resources"""
            return [
                Resource(
                    uri="ral://portal/technical-reference",
                    name="RAL Portal Technical Reference",
                    mimeType="text/markdown",
                    description="Complete system overview, architecture, deployment, and support"
                ),
                Resource(
                    uri="ral://portal/rest-api",
                    name="RAL Portal REST API Documentation",
                    mimeType="text/markdown",
                    description="Complete REST API reference (263 pages) - all endpoints, authentication, file upload"
                ),
                Resource(
                    uri="ral://portal/stored-procedures",
                    name="RAL Portal Stored Procedures",
                    mimeType="text/markdown",
                    description="All 47 stored procedures with parameters and table dependencies"
                ),
                Resource(
                    uri="ral://portal/database-schema",
                    name="RAL Portal Database Schema (ERD)",
                    mimeType="text/markdown",
                    description="Complete database schema - 45 tables with relationships (OCR extracted)"
                ),
                Resource(
                    uri="ral://portal/file-upload",
                    name="RAL Portal File Upload Workflow",
                    mimeType="text/markdown",
                    description="Detailed 5-step file upload process with OAuth authentication"
                ),
                Resource(
                    uri="ral://portal/erd-ocr-data",
                    name="RAL Portal ERD OCR Data (JSON)",
                    mimeType="application/json",
                    description="Raw OCR data from all 35 ERD diagrams for detailed schema queries"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read RAL Portal documentation resource"""
            
            resource_map = {
                "ral://portal/technical-reference": "RAL_Portal_Technical_Reference.md",
                "ral://portal/rest-api": "RAL_Portal_REST_API_Complete.md",
                "ral://portal/stored-procedures": "RAL_Portal_Stored_Procedures.md",
                "ral://portal/database-schema": "RAL_Portal_ERD_Database_Schema.md",
                "ral://portal/file-upload": "API_Endpoint_File_Upload_Documentation.md",
                "ral://portal/erd-ocr-data": "RAL_Portal_ERD_OCR_Complete.json"
            }
            
            filename = resource_map.get(uri)
            if not filename:
                raise ValueError(f"Unknown resource URI: {uri}")
            
            file_path = KNOWLEDGE_BASE / filename
            
            if not file_path.exists():
                raise FileNotFoundError(f"Resource file not found: {file_path}")
            
            return file_path.read_text()
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available RAL Portal tools"""
            return [
                Tool(
                    name="search_api_endpoints",
                    description="Search RAL Portal REST API endpoints by keyword or controller",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search term (e.g., 'upload', 'client', 'project')"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="search_stored_procedures",
                    description="Search RAL Portal stored procedures by name or purpose",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search term (e.g., 'tax', 'project', 'client')"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="find_table_schema",
                    description="Get detailed schema for a specific database table",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {
                                "type": "string",
                                "description": "Table name (e.g., 'ProjectTasks', 'Clients')"
                            }
                        },
                        "required": ["table_name"]
                    }
                ),
                Tool(
                    name="get_authentication_flow",
                    description="Get OAuth 2.0 authentication flow for RAL Portal API",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Execute RAL Portal tool"""
            
            if name == "search_api_endpoints":
                return await self._search_api_endpoints(arguments["query"])
            
            elif name == "search_stored_procedures":
                return await self._search_stored_procedures(arguments["query"])
            
            elif name == "find_table_schema":
                return await self._find_table_schema(arguments["table_name"])
            
            elif name == "get_authentication_flow":
                return await self._get_authentication_flow()
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _search_api_endpoints(self, query: str) -> list[TextContent]:
        """Search REST API endpoints"""
        api_doc = KNOWLEDGE_BASE / "RAL_Portal_REST_API_Complete.md"
        content = api_doc.read_text()
        
        # Simple search - find sections containing query
        lines = content.split('\n')
        results = []
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                # Get context (10 lines before and after)
                start = max(0, i - 10)
                end = min(len(lines), i + 10)
                context = '\n'.join(lines[start:end])
                results.append(context)
        
        if results:
            return [TextContent(
                type="text",
                text=f"Found {len(results)} matches for '{query}':\n\n" + "\n\n---\n\n".join(results[:3])
            )]
        else:
            return [TextContent(
                type="text",
                text=f"No API endpoints found matching '{query}'"
            )]
    
    async def _search_stored_procedures(self, query: str) -> list[TextContent]:
        """Search stored procedures"""
        sp_doc = KNOWLEDGE_BASE / "RAL_Portal_Stored_Procedures.md"
        content = sp_doc.read_text()
        
        lines = content.split('\n')
        results = []
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower() and ('Procedure Name' in line or 'Purpose:' in line):
                # Get full procedure section
                start = i
                end = i + 20
                context = '\n'.join(lines[start:end])
                results.append(context)
        
        if results:
            return [TextContent(
                type="text",
                text=f"Found {len(results)} stored procedures matching '{query}':\n\n" + "\n\n---\n\n".join(results[:3])
            )]
        else:
            return [TextContent(
                type="text",
                text=f"No stored procedures found matching '{query}'"
            )]
    
    async def _find_table_schema(self, table_name: str) -> list[TextContent]:
        """Find table schema in ERD"""
        erd_doc = KNOWLEDGE_BASE / "RAL_Portal_ERD_Database_Schema.md"
        content = erd_doc.read_text()
        
        # Search for table name
        if table_name.lower() in content.lower():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if table_name.lower() in line.lower() and '[dbo]' in line:
                    # Get full section
                    start = max(0, i - 5)
                    end = min(len(lines), i + 50)
                    schema = '\n'.join(lines[start:end])
                    
                    return [TextContent(
                        type="text",
                        text=f"Schema for table '{table_name}':\n\n{schema}"
                    )]
        
        return [TextContent(
            type="text",
            text=f"Table '{table_name}' not found in schema. Available tables can be found in the database-schema resource."
        )]
    
    async def _get_authentication_flow(self) -> list[TextContent]:
        """Get OAuth authentication flow"""
        api_doc = KNOWLEDGE_BASE / "RAL_Portal_REST_API_Complete.md"
        content = api_doc.read_text()
        
        # Extract authentication section
        lines = content.split('\n')
        auth_section = []
        in_auth = False
        
        for line in lines:
            if '## Authentication Flow' in line or '### OAuth' in line:
                in_auth = True
            elif in_auth and line.startswith('##') and 'Authentication' not in line:
                break
            
            if in_auth:
                auth_section.append(line)
        
        if auth_section:
            return [TextContent(
                type="text",
                text='\n'.join(auth_section)
            )]
        else:
            return [TextContent(
                type="text",
                text="Authentication flow documentation not found. Check the rest-api resource."
            )]
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = RALPortalMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
