// 8825 Sticky Importer Plugin
// Imports sticky notes from JSON into FigJam

// Show UI
figma.showUI(__html__, { width: 400, height: 550 });

// Color mapping
const COLORS = {
  'yellow': { r: 1, g: 1, b: 0.6 },
  'pink': { r: 1, g: 0.71, b: 0.76 },
  'blue': { r: 0.68, g: 0.85, b: 0.9 },
  'green': { r: 0.56, g: 0.93, b: 0.56 },
  'orange': { r: 1, g: 0.78, b: 0.49 },
  'purple': { r: 0.85, g: 0.75, b: 0.85 },
  'white': { r: 1, g: 1, b: 1 }
};

// Handle messages from UI
figma.ui.onmessage = async (msg) => {
  if (msg.type === 'import-stickies') {
    try {
      const data = JSON.parse(msg.json);
      
      // Get first result (should only be one)
      const result = data[0];
      
      if (!result || !result.clusters) {
        figma.ui.postMessage({ 
          type: 'error', 
          message: 'Invalid JSON format' 
        });
        return;
      }
      
      let created = 0;
      
      // Create stickies for each cluster
      for (const cluster of result.clusters) {
        for (const stickyData of cluster.stickies) {
          // Create sticky note
          const sticky = figma.createSticky();
          
          // Set position (scale down from photo coordinates)
          const scale = 0.5; // Adjust this to fit your board
          sticky.x = stickyData.position[0] * scale;
          sticky.y = stickyData.position[1] * scale;
          
          // Set size
          sticky.resize(200, 200);
          
          // Set color
          const color = COLORS[stickyData.color] || COLORS['yellow'];
          sticky.fills = [{ type: 'SOLID', color: color }];
          
          // Load the font that's already in the sticky (from Figma docs)
          await figma.loadFontAsync(sticky.text.fontName);
          
          // Set text
          sticky.text.characters = stickyData.text;
          
          created++;
        }
      }
      
      figma.ui.postMessage({ 
        type: 'success', 
        message: `Created ${created} sticky notes!` 
      });
      
      // Zoom to fit
      figma.viewport.scrollAndZoomIntoView(figma.currentPage.children);
      
    } catch (error) {
      figma.ui.postMessage({ 
        type: 'error', 
        message: `Error: ${error.message}` 
      });
    }
  }
  
  if (msg.type === 'cancel') {
    figma.closePlugin();
  }
};
