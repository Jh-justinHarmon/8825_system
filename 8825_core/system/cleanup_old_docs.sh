#!/bin/bash
# Auto-Cleanup Old Documents
# Run weekly to archive old exports and notes

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
DOCS_ROOT="$SYSTEM_ROOT/docs"
MONTH=$(date +%Y-%m)

# Archive old session summaries (>30 days)
if [ -d "$DOCS_ROOT/exports/sessions" ]; then
    find "$DOCS_ROOT/exports/sessions" -name "*.md" -mtime +30 -exec mv {} "$DOCS_ROOT/milestones/$MONTH/" \; 2>/dev/null
fi

# Archive old analyses (>90 days)
if [ -d "$DOCS_ROOT/exports/analyses" ]; then
    find "$DOCS_ROOT/exports/analyses" -name "*.md" -mtime +90 -exec mv {} "$DOCS_ROOT/milestones/$MONTH/" \; 2>/dev/null
fi

# Archive old personal notes (>30 days)
if [ -d "$SYSTEM_ROOT/users/justin_harmon/notes/active" ]; then
    mkdir -p "$SYSTEM_ROOT/users/justin_harmon/notes/archive/$MONTH"
    find "$SYSTEM_ROOT/users/justin_harmon/notes/active" -name "*.md" -mtime +30 -exec mv {} "$SYSTEM_ROOT/users/justin_harmon/notes/archive/$MONTH/" \; 2>/dev/null
fi

echo "✅ Cleanup complete"
