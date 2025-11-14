#!/usr/bin/env node
/**
 * HCSS MCP Bridge Server
 * Exposes 8825 HCSS tools to Goose AI agent via Model Context Protocol
 * 
 * Version: 1.0.0
 * Created: 2025-11-06
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { execSync } from 'child_process';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// Get paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const HCSS_SANDBOX = join(__dirname, '../../../hcss_sandbox');
const RAW_DIR = join(HCSS_SANDBOX, 'raw');
const LOGS_DIR = join(HCSS_SANDBOX, 'logs');

// Create server
const server = new Server(
  {
    name: 'hcss-bridge',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions
const TOOLS = [
  {
    name: 'ingest_gmail',
    description: 'Trigger Gmail/Otter ingestion to check for new emails and transcripts. Returns count of new items processed.',
    inputSchema: {
      type: 'object',
      properties: {
        days_back: {
          type: 'number',
          description: 'Number of days to search back (default: 7)',
          default: 7
        }
      }
    }
  },
  {
    name: 'check_status',
    description: 'Check HCSS system status including scheduler, recent processing, and file counts',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'list_recent_files',
    description: 'List recently processed files with optional filtering by project',
    inputSchema: {
      type: 'object',
      properties: {
        project: {
          type: 'string',
          description: 'Filter by project: TGIF, RAL, LHL, 76, or all',
          enum: ['TGIF', 'RAL', 'LHL', '76', 'all'],
          default: 'all'
        },
        limit: {
          type: 'number',
          description: 'Maximum number of files to return',
          default: 10
        }
      }
    }
  },
  {
    name: 'read_corrections_log',
    description: 'Read the corrections log to see what corrections have been applied',
    inputSchema: {
      type: 'object',
      properties: {
        lines: {
          type: 'number',
          description: 'Number of recent lines to return',
          default: 50
        }
      }
    }
  },
  {
    name: 'get_routing_stats',
    description: 'Get statistics about routing decisions and project distribution',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }
];

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

// Tool execution handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'ingest_gmail':
        return await ingestGmail(args);
      
      case 'check_status':
        return await checkStatus();
      
      case 'list_recent_files':
        return await listRecentFiles(args);
      
      case 'read_corrections_log':
        return await readCorrectionsLog(args);
      
      case 'get_routing_stats':
        return await getRoutingStats();
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error executing ${name}: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

// Tool implementations

async function ingestGmail(args) {
  const daysBack = args?.days_back || 7;
  
  try {
    // Execute the Gmail extractor
    const script = join(HCSS_SANDBOX, '8825_gmail_extractor.py');
    const result = execSync(`python3 "${script}"`, {
      cwd: HCSS_SANDBOX,
      encoding: 'utf8',
      timeout: 120000 // 2 minute timeout
    });
    
    // Parse output for statistics
    const lines = result.split('\n');
    const newEmailsLine = lines.find(l => l.includes('new emails'));
    const processedLine = lines.find(l => l.includes('processed'));
    
    let summary = `Gmail ingestion completed.\n\n${result}`;
    
    return {
      content: [
        {
          type: 'text',
          text: summary
        }
      ]
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Gmail ingestion failed: ${error.message}\n\nThis might be normal if no new emails are available.`
        }
      ]
    };
  }
}

async function checkStatus() {
  try {
    // Check scheduler status
    let schedulerStatus = 'Unknown';
    try {
      const launchctlOutput = execSync('launchctl list | grep hcss', { encoding: 'utf8' });
      schedulerStatus = launchctlOutput.includes('hcss') ? '✅ Running' : '❌ Not running';
    } catch {
      schedulerStatus = '❌ Not running';
    }
    
    // Count files in raw/
    let fileCount = 0;
    try {
      const files = readdirSync(RAW_DIR);
      fileCount = files.filter(f => f.endsWith('.json')).length;
    } catch {
      fileCount = 0;
    }
    
    // Check recent processing
    let lastProcessed = 'Unknown';
    try {
      const processedLog = join(LOGS_DIR, 'processed_emails.json');
      const stat = statSync(processedLog);
      lastProcessed = stat.mtime.toLocaleString();
    } catch {
      lastProcessed = 'No log file found';
    }
    
    const status = `
HCSS System Status
==================

Scheduler: ${schedulerStatus}
Processed Files: ${fileCount} files in raw/
Last Processing: ${lastProcessed}

Directories:
- Raw: ${RAW_DIR}
- Logs: ${LOGS_DIR}
- Sandbox: ${HCSS_SANDBOX}
`;
    
    return {
      content: [
        {
          type: 'text',
          text: status
        }
      ]
    };
  } catch (error) {
    throw new Error(`Status check failed: ${error.message}`);
  }
}

async function listRecentFiles(args) {
  const project = args?.project || 'all';
  const limit = args?.limit || 10;
  
  try {
    const files = readdirSync(RAW_DIR)
      .filter(f => f.endsWith('.json'))
      .map(f => {
        const stat = statSync(join(RAW_DIR, f));
        return {
          name: f,
          size: stat.size,
          modified: stat.mtime
        };
      })
      .sort((a, b) => b.modified - a.modified)
      .slice(0, limit);
    
    // Filter by project if specified
    let filteredFiles = files;
    if (project !== 'all') {
      filteredFiles = files.filter(f => 
        f.name.toLowerCase().includes(project.toLowerCase())
      );
    }
    
    const fileList = filteredFiles.map(f => 
      `${f.name} (${(f.size / 1024).toFixed(1)}KB, ${f.modified.toLocaleString()})`
    ).join('\n');
    
    const summary = `
Recent Files (${filteredFiles.length} of ${files.length} total)
${project !== 'all' ? `Filtered by: ${project}` : 'All projects'}
==================

${fileList || 'No files found'}
`;
    
    return {
      content: [
        {
          type: 'text',
          text: summary
        }
      ]
    };
  } catch (error) {
    throw new Error(`Failed to list files: ${error.message}`);
  }
}

async function readCorrectionsLog(args) {
  const lines = args?.lines || 50;
  
  try {
    const logFile = join(LOGS_DIR, 'corrections_applied.txt');
    const content = readFileSync(logFile, 'utf8');
    const logLines = content.split('\n').filter(l => l.trim());
    const recentLines = logLines.slice(-lines);
    
    const summary = `
Recent Corrections (last ${lines} entries)
==================

${recentLines.join('\n')}

Total corrections in log: ${logLines.length}
`;
    
    return {
      content: [
        {
          type: 'text',
          text: summary
        }
      ]
    };
  } catch (error) {
    throw new Error(`Failed to read corrections log: ${error.message}`);
  }
}

async function getRoutingStats() {
  try {
    const files = readdirSync(RAW_DIR).filter(f => f.endsWith('.json'));
    
    // Count by project (based on filename patterns)
    const stats = {
      total: files.length,
      otter: files.filter(f => f.includes('otter')).length,
      forwarded: files.filter(f => !f.includes('otter')).length,
      byProject: {
        TGIF: 0,
        RAL: 0,
        LHL: 0,
        '76': 0,
        other: 0
      }
    };
    
    // Try to determine project from filenames or content
    files.forEach(f => {
      const name = f.toLowerCase();
      if (name.includes('tgif')) stats.byProject.TGIF++;
      else if (name.includes('ral')) stats.byProject.RAL++;
      else if (name.includes('lhl')) stats.byProject.LHL++;
      else if (name.includes('76') || name.includes('joju')) stats.byProject['76']++;
      else stats.byProject.other++;
    });
    
    const summary = `
Routing Statistics
==================

Total Files: ${stats.total}
- Otter Transcripts: ${stats.otter}
- Forwarded Emails: ${stats.forwarded}

By Project:
- TGIF: ${stats.byProject.TGIF}
- RAL: ${stats.byProject.RAL}
- LHL: ${stats.byProject.LHL}
- 76 (Joju): ${stats.byProject['76']}
- Other: ${stats.byProject.other}
`;
    
    return {
      content: [
        {
          type: 'text',
          text: summary
        }
      ]
    };
  } catch (error) {
    throw new Error(`Failed to get routing stats: ${error.message}`);
  }
}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('HCSS MCP Bridge Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
