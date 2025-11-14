#!/usr/bin/env node
/**
 * FigJam MCP Server
 * Processes sticky notes and prepares them for FigJam import
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import { readFile } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const WORKSPACE_ROOT = path.resolve(__dirname, '../../../..');

// Create MCP server
const server = new Server(
  {
    name: 'figjam-sticky-processor',
    version: '1.0.0',
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
    name: 'process_stickies_to_figjam',
    description: 'Process sticky note photos with OCR and prepare JSON for FigJam import. Returns instructions and copies JSON to clipboard.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
];

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Call tool handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name } = request.params;

  try {
    switch (name) {
      case 'process_stickies_to_figjam':
        return await processSticksToFigJam();
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error executing ${name}: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function processSticksToFigJam() {
  const scriptPath = path.join(WORKSPACE_ROOT, '8825_core/integrations/figjam/process_and_copy.sh');
  
  try {
    // Run the processing script
    const { stdout, stderr } = await execAsync(`bash "${scriptPath}"`, {
      cwd: path.join(WORKSPACE_ROOT, '8825_core/integrations/figjam'),
    });
    
    // Read the generated JSON
    const jsonPath = path.join(os.homedir(), 'Downloads', 'sticky_notes_vision.json');
    const jsonData = await readFile(jsonPath, 'utf8');
    const data = JSON.parse(jsonData);
    
    // Count total stickies
    const totalStickies = data[0]?.total_stickies || 0;
    
    const instructions = `
✅ Sticky notes processed successfully!

📊 Results:
- Total stickies found: ${totalStickies}
- JSON copied to clipboard
- Ready for FigJam import

📋 Next steps:
1. Open your FigJam board
2. Run the "8825 Sticky Importer" plugin:
   - Right-click on canvas
   - Plugins → Development → 8825 Sticky Importer
3. Press Cmd+V to paste the JSON
4. Click "Import Stickies"

💡 The JSON is already in your clipboard, ready to paste!

Output from processor:
${stdout}
`;
    
    return {
      content: [
        {
          type: 'text',
          text: instructions,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error processing stickies: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('FigJam MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
