# ** NOTE this should not be so joju specific. **. F

**Created:** 2025-11-17  
**Source:** Assimilated from Windsurf memory

## Origin

This protocol was automatically created from a Windsurf AI session memory.

## Original Memory

```
** NOTE this should not be so joju specific. **. Figma Make → Joju Automation Pipeline - Complete Workflow
#figma_make
#automation
#joju
#transformation
#workflow

Edit
Built: 2025-11-10 (40 minutes total build time)

Purpose: Automate transformation of Figma Make components into Joju-ready React code

Location: ~/Documents/8825/meeting_prep/figma-make-transformer/

Time Savings: 55% reduction (75 min → 34 min per component)

Workflow
Step 1: Collaborative Design (2 min)

Design in Figma Make
Click "Make settings → GitHub → Push"
Creates repo (e.g., Figmamakejojucomponents)
Step 2: Transformation (2 min)

bash
cd ~/Documents/8825/meeting_prep/figma-make-transformer
npm run transform ../repo-name/src
Step 3: Copy to Joju (1 min)

bash
cp -r ../repo-name/src/* "/path/to/joju/src/components/ComponentName/"
Step 4: CAM - Code, Add, Merge (30 min)

Review transformed code
Add backend integration
Add tests
Commit and deploy
What Gets Transformed
Icons: SVG → Lucide React (30+ mappings)
Theme: Hex colors → CSS variables (background, foreground, border, etc.)
Imports: Clean up, add cn utility, remove versions
Components: Default exports → Named exports, add context hooks
Scripts
icon_replacer.js - SVG → Lucide
theme_converter.js - Hex → CSS vars
import_organizer.js - Clean imports
component_wrapper.js - Add context
transform_all.sh - Master script
trigger_integration.js - GitHub Action trigger (requires Joju repo access)
First Test Results
Component: Comments Component from Figma Make Transformations:

6 icons replaced
17 colors converted
49 files organized
2 components wrapped
100% accuracy
Time: 2 minutes for transformation

Key Learnings
Figma Make generates production-ready React code - Not just prototypes
Built-in GitHub push - Native feature, no plugin needed
Transformation patterns are consistent - Same icons, colors, imports every time
Manual copy works when GitHub Action can't - Joju repo not accessible via API
ROI is immediate - First component pays for entire setup
Dependencies
json
{
  "@octokit/rest": "^20.0.0",
  "dotenv": "^16.3.1"
}
Environment Setup
.env file required:

GITHUB_TOKEN=your_token_here
GITHUB_ACTOR=matthew
Future Enhancements
Add more icon mappings as needed
Add more color mappings for different themes
Auto-detect component names
Integrate with Joju repo when accessible via API
Add to MCP bridge for Goose access
```

## Protocol

- ** NOTE this should not be so joju specific. **. Figma Make → Joju Automation Pipeline - Complete Workflow
- Step 1: Collaborative Design (2 min)
- Step 2: Transformation (2 min)
- Step 3: Copy to Joju (1 min)
- Step 4: CAM - Code, Add, Merge (30 min)
- Manual copy works when GitHub Action can't - Joju repo not accessible via API
- Add more color mappings for different themes
- Integrate with Joju repo when accessible via API

## Related Context


**Key Entities:**
Workflow, MCP, 8825, Joju

---

*This protocol was auto-generated. Review and enhance as needed.*
