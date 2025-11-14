# RAL Portal MCP Server

AI-accessible documentation for the RAL Portal system managed by HCSS.

## Overview

This MCP server provides comprehensive technical documentation for the RAL Portal, making it easy for AI assistants to answer questions about:
- REST API endpoints and authentication
- Database schema and relationships
- Stored procedures
- File upload workflows
- System architecture

## Resources

The server exposes 6 documentation resources:

1. **Technical Reference** - System overview, architecture, deployment
2. **REST API Documentation** - Complete API reference (263 pages)
3. **Stored Procedures** - All 47 procedures with parameters
4. **Database Schema** - Complete ERD with 45 tables
5. **File Upload Workflow** - Detailed 5-step process
6. **ERD OCR Data** - Raw schema data (JSON)

## Tools

The server provides 4 tools for common queries:

1. **search_api_endpoints** - Find API endpoints by keyword
2. **search_stored_procedures** - Find stored procedures by purpose
3. **find_table_schema** - Get detailed table schema
4. **get_authentication_flow** - Get OAuth 2.0 flow details

## Installation

### Prerequisites
```bash
pip install mcp
```

### Configuration

Add to your MCP client config (e.g., Claude Desktop, Windsurf):

```json
{
  "mcpServers": {
    "ral-portal": {
      "command": "python3",
      "args": [
        "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/mcp_servers/ral_portal/server.py"
      ]
    }
  }
}
```

## Usage Examples

### With Claude Desktop

**Question:** "How do I authenticate to the RAL Portal API?"

**Response:** Claude will use the `get_authentication_flow` tool or read the `rest-api` resource to provide the OAuth 2.0 flow with client credentials.

---

**Question:** "What stored procedure shows client tax status?"

**Response:** Claude will use `search_stored_procedures` with query "tax status" and find `ClientTaxStatus` procedure with parameters.

---

**Question:** "Show me the ProjectTasks table schema"

**Response:** Claude will use `find_table_schema` with "ProjectTasks" and return the complete table definition with foreign keys.

---

**Question:** "What's the endpoint to upload a file?"

**Response:** Claude will use `search_api_endpoints` with query "upload" and find the `/api/files/uploadStatement` endpoint with full documentation.

## For RAL Team

### Quick Start

1. Install Claude Desktop or Windsurf
2. Add RAL Portal MCP server to config
3. Ask questions naturally:
   - "How do I create a new project?"
   - "What tables are involved in cession tracking?"
   - "Show me the authentication process"
   - "Which stored procedure lists active clients?"

### Common Use Cases

**New Developer Onboarding:**
- "Walk me through the database schema"
- "What are the main API controllers?"
- "How does project-template relationship work?"

**Development:**
- "What's the endpoint to update a client?"
- "Show me the ClientBankAccounts table structure"
- "Which stored procedure do I use for bank status?"

**Troubleshooting:**
- "What fields are required for intakeDocument?"
- "What's the status flow for document processing?"
- "How do I check if a user has access to a client?"

## For HCSS Team

### Deployment Options

**Option 1: Shared Server (Recommended)**
- Host MCP server on HCSS infrastructure
- RAL team connects remotely
- Centralized updates and maintenance

**Option 2: Local Installation**
- Each RAL team member runs locally
- Requires access to knowledge base files
- More setup but fully offline

**Option 3: Cloud Hosted**
- Deploy to AWS/Azure
- Accessible from anywhere
- Scalable for multiple clients

### Maintenance

**Updating Documentation:**
1. Update markdown files in `focuses/hcss/knowledge/`
2. MCP server automatically serves latest content
3. No code changes needed

**Adding New Resources:**
1. Add new markdown file to knowledge base
2. Register in `list_resources()` handler
3. Add URI mapping in `read_resource()` handler

### Extending for Other Clients

This MCP server pattern can be replicated for any client portal:

```
mcp_servers/
├── ral_portal/          # RAL Portal
├── client_x_portal/     # Client X
└── client_y_system/     # Client Y
```

Each gets their own AI-accessible documentation.

## Technical Details

### Architecture

```
RAL Portal MCP Server
├── Resources (Read-only)
│   └── 6 markdown/JSON files from knowledge base
│
└── Tools (Query helpers)
    ├── search_api_endpoints()
    ├── search_stored_procedures()
    ├── find_table_schema()
    └── get_authentication_flow()
```

### Performance

- **Startup:** < 1 second
- **Resource reads:** Direct file I/O (fast)
- **Tool calls:** Simple text search (< 100ms)
- **Memory:** ~10MB (loads files on demand)

### Security

- **Read-only:** Cannot modify portal or database
- **Local files:** No external API calls
- **No credentials:** Documentation only, no secrets
- **Audit trail:** MCP client logs all queries

## Business Value

### For RAL
- **Faster onboarding** - New developers productive immediately
- **Reduced errors** - Accurate API/database info always available
- **24/7 access** - No waiting for HCSS support
- **Self-service** - Answer own questions instantly

### For HCSS
- **Reduced support load** - Fewer "how do I..." questions
- **Consistent answers** - No more outdated documentation
- **Competitive advantage** - "AI-accessible portals"
- **Scalable** - Same pattern for all clients

## Future Enhancements

### Phase 2: Live Data Integration
- Connect to RAL database (read-only)
- Query real-time data
- Generate reports on demand

### Phase 3: Code Generation
- Generate API client code
- Create SQL queries from natural language
- Build sample requests

### Phase 4: Multi-Client Platform
- Single MCP server for all HCSS clients
- Client-specific authentication
- Shared knowledge base with client isolation

## Support

**For RAL Team:**
- Contact: justin.harmon@hammercss.com
- Documentation: This README
- Knowledge Base: `focuses/hcss/knowledge/`

**For HCSS Team:**
- Server Code: `mcp_servers/ral_portal/server.py`
- Configuration: See Installation section above
- Updates: Modify knowledge base files directly

---

**Version:** 1.0.0  
**Created:** 2025-11-11  
**Maintained By:** HCSS (Hammer Consulting & Support Services)
