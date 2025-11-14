#!/usr/bin/env node
/**
 * 8825 Customer Platform MCP Server
 * 
 * Control layer with guardrails, validation, routing, and logging
 * Customer interface: Email (simple)
 * Management interface: MCP (powerful)
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import * as core from '../lib/core.js';
import * as storage from '../lib/storage_simple.js';
import dotenv from 'dotenv';

dotenv.config();

// Create MCP server
const server = new Server(
  {
    name: '8825-customer-platform',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions
const tools = [
  {
    name: 'ingest_data',
    description: 'Ingest data into customer context. Extracts structured information and stores in database.',
    inputSchema: {
      type: 'object',
      properties: {
        customer_id: {
          type: 'string',
          description: 'Customer identifier (e.g., TEST, ps_medical, mes_corporate)',
          pattern: '^[a-z_][a-z0-9_]*$'
        },
        data: {
          type: 'string',
          description: 'Raw data to ingest (text, document content, etc.)'
        }
      },
      required: ['customer_id', 'data']
    }
  },
  {
    name: 'query_customer',
    description: 'Query customer context with a question. Returns answer based on stored data and brain knowledge.',
    inputSchema: {
      type: 'object',
      properties: {
        customer_id: {
          type: 'string',
          description: 'Customer identifier',
          pattern: '^[a-z_][a-z0-9_]*$'
        },
        question: {
          type: 'string',
          description: 'Question to answer'
        }
      },
      required: ['customer_id', 'question']
    }
  },
  {
    name: 'analyze_customer',
    description: 'Run analysis on customer data. Generates summary, trends, and recommendations.',
    inputSchema: {
      type: 'object',
      properties: {
        customer_id: {
          type: 'string',
          description: 'Customer identifier',
          pattern: '^[a-z_][a-z0-9_]*$'
        },
        days: {
          type: 'number',
          description: 'Number of days to analyze (default: 7)',
          default: 7,
          minimum: 1,
          maximum: 365
        }
      },
      required: ['customer_id']
    }
  },
  {
    name: 'get_customer_stats',
    description: 'Get statistics for a specific customer',
    inputSchema: {
      type: 'object',
      properties: {
        customer_id: {
          type: 'string',
          description: 'Customer identifier',
          pattern: '^[a-z_][a-z0-9_]*$'
        }
      },
      required: ['customer_id']
    }
  },
  {
    name: 'list_customers',
    description: 'List all customers with their statistics',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }
];

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Call tool handler with guardrails
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    // Guardrail: Validate customer_id format
    if (args.customer_id && !/^[a-z_][a-z0-9_]*$/.test(args.customer_id)) {
      throw new Error('Invalid customer_id format. Must be lowercase letters, numbers, and underscores only.');
    }
    
    // Guardrail: Check customer exists (except for list_customers)
    if (args.customer_id && name !== 'list_customers') {
      if (!storage.customerExists(args.customer_id)) {
        throw new Error(`Customer not found: ${args.customer_id}`);
      }
    }
    
    // Guardrail: Check rate limits (placeholder - implement actual rate limiting)
    // if (isRateLimited(args.customer_id)) {
    //   throw new Error('Rate limit exceeded. Please try again later.');
    // }
    
    // Route to appropriate function
    let result;
    
    switch (name) {
      case 'ingest_data':
        result = await core.ingest(args.customer_id, args.data);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      
      case 'query_customer':
        result = await core.query(args.customer_id, args.question);
        return {
          content: [
            {
              type: 'text',
              text: result.answer
            },
            {
              type: 'text',
              text: `\n\n---\nModel: ${result.model_used} | Cost: $${result.cost.toFixed(4)} | Relevant records: ${result.relevant_records}`
            }
          ]
        };
      
      case 'analyze_customer':
        result = await core.analyze(args.customer_id, { days: args.days || 7 });
        return {
          content: [
            {
              type: 'text',
              text: `# Analysis for ${args.customer_id}\n\n${result.summary}\n\n## Trends\n${result.trends.map(t => `- ${t.name}: ${t.direction} (${t.significance})`).join('\n')}\n\n## Recommendations\n${result.recommendations.map(r => `- ${r}`).join('\n')}`
            },
            {
              type: 'text',
              text: `\n\n---\nModel: ${result.model_used} | Cost: $${result.cost.toFixed(4)} | Records analyzed: ${result.records_analyzed}`
            }
          ]
        };
      
      case 'get_customer_stats':
        result = await core.getStats(args.customer_id);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      
      case 'list_customers':
        result = await core.getAllStats();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    // Log error
    console.error(`Tool execution failed: ${name}`, error);
    
    // Return error to client
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('8825 Customer Platform MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
