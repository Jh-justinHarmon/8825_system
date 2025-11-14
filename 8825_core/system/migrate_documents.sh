#!/bin/bash
# Document Migration Script - Phase 3 execution
# Version: 1.0.0
# Created: 2025-11-13

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
DOCS_ROOT="$SYSTEM_ROOT/docs"

echo -e "${BLUE}=== Document Migration ===${NC}"
echo ""

# Create new structure
echo "Creating docs/ structure..."
mkdir -p "$DOCS_ROOT/reference/protocols"
mkdir -p "$DOCS_ROOT/reference/integrations"
mkdir -p "$DOCS_ROOT/reference/mcp"
mkdir -p "$DOCS_ROOT/reference/system"
mkdir -p "$DOCS_ROOT/exports/sessions"
mkdir -p "$DOCS_ROOT/exports/analyses"
mkdir -p "$DOCS_ROOT/exports/reports"
mkdir -p "$DOCS_ROOT/milestones/2025-11"
mkdir -p "$DOCS_ROOT/archive/explorations/2025-11"
mkdir -p "$DOCS_ROOT/archive/personal-notes/2025-11"
mkdir -p "$DOCS_ROOT/templates"

echo -e "${GREEN}✅ Structure created${NC}"
echo ""

# Archive explorations from root
echo "Archiving root explorations..."
cd "$SYSTEM_ROOT"
for file in *COMPLETE*.md *FINAL*.md *SUMMARY*.md *EVALUATION*.md *2025-11-10*.md *2025-11-09*.md; do
    if [ -f "$file" ]; then
        mv "$file" "$DOCS_ROOT/archive/explorations/2025-11/"
        echo "  Archived: $file"
    fi
done

# Archive migrations/2025-11-cleanup
echo "Archiving migration docs..."
if [ -d "$SYSTEM_ROOT/migrations/2025-11-cleanup" ]; then
    mv "$SYSTEM_ROOT/migrations/2025-11-cleanup"/*.md "$DOCS_ROOT/archive/explorations/2025-11/" 2>/dev/null || true
fi

# Archive docs_from_2.1
echo "Archiving old version docs..."
if [ -d "$SYSTEM_ROOT/users/justin_harmon/joju/docs_from_2.1" ]; then
    mv "$SYSTEM_ROOT/users/justin_harmon/joju/docs_from_2.1"/*.md "$DOCS_ROOT/archive/explorations/2025-11/" 2>/dev/null || true
    rmdir "$SYSTEM_ROOT/users/justin_harmon/joju/docs_from_2.1" 2>/dev/null || true
fi

# Archive personal notes
echo "Archiving personal notes..."
if [ -d "$SYSTEM_ROOT/users/justin_harmon/personal" ]; then
    mv "$SYSTEM_ROOT/users/justin_harmon/personal"/*.md "$DOCS_ROOT/archive/personal-notes/2025-11/" 2>/dev/null || true
fi

# Move reference docs from root
echo "Moving reference docs..."
for file in API_REFERENCE.md DEVELOPER_GUIDE.md MCP_*.md PHILOSOPHY.md STARTUP_AUTOMATION.md; do
    if [ -f "$SYSTEM_ROOT/$file" ]; then
        mv "$SYSTEM_ROOT/$file" "$DOCS_ROOT/reference/"
        echo "  Moved: $file"
    fi
done

# Copy QUICK_COMMANDS to docs
if [ -f "$SYSTEM_ROOT/QUICK_COMMANDS.md" ]; then
    cp "$SYSTEM_ROOT/QUICK_COMMANDS.md" "$DOCS_ROOT/reference/"
    echo "  Mirrored: QUICK_COMMANDS.md"
fi

echo ""
echo -e "${GREEN}✅ Migration complete${NC}"
echo ""
echo "Summary:"
echo "  Root files: $(ls -1 "$SYSTEM_ROOT"/*.md 2>/dev/null | wc -l | tr -d ' ')"
echo "  Archived explorations: $(ls -1 "$DOCS_ROOT/archive/explorations/2025-11" | wc -l | tr -d ' ')"
echo "  Archived notes: $(ls -1 "$DOCS_ROOT/archive/personal-notes/2025-11" | wc -l | tr -d ' ')"
echo "  Reference docs: $(ls -1 "$DOCS_ROOT/reference" | wc -l | tr -d ' ')"
