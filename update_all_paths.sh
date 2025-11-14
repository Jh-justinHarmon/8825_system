#!/bin/bash
# Update all path references to new 8825-system structure
# Created: 2025-11-10

set -e

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

echo "🔧 Updating all path references..."

# Update 8825-system references to 8825-system
find "$SYSTEM_ROOT" -type f \( -name "*.md" -o -name "*.json" -o -name "*.sh" -o -name "*.py" \) -exec sed -i '' 's|windsurf-project - 8825 version 3\.0|8825-system|g' {} \;

# Update version 2.0 references (now deleted)
find "$SYSTEM_ROOT" -type f \( -name "*.md" -o -name "*.json" \) -exec sed -i '' 's|windsurf-project - 8825 version 2\.0|8825-system (v2.0 deleted)|g' {} \;

# Update old MCP paths
find "$SYSTEM_ROOT" -type f \( -name "*.md" -o -name "*.sh" \) -exec sed -i '' 's|~/mcp_servers/8825-core|~/mcp_servers/8825-core|g' {} \;
find "$SYSTEM_ROOT" -type f \( -name "*.md" -o -name "*.sh" \) -exec sed -i '' 's|~/mcp_servers/hcss-bridge|~/mcp_servers/hcss-bridge|g' {} \;
find "$SYSTEM_ROOT" -type f \( -name "*.md" -o -name "*.sh" \) -exec sed -i '' 's|~/mcp_servers/figma-make-transformer|~/mcp_servers/figma-make-transformer|g' {} \;

echo "✅ Path references updated"
echo ""
echo "📊 Summary:"
echo "  - Updated '8825-system' → '8825-system'"
echo "  - Updated 'version 2.0' references (deleted)"
echo "  - Updated MCP server paths to ~/mcp_servers/"
echo ""
echo "🔍 Verify with:"
echo "  grep -r '8825-system' $SYSTEM_ROOT --include='*.md' --include='*.json'"
echo "  grep -r 'version 2.0' $SYSTEM_ROOT --include='*.md' --include='*.json'"
