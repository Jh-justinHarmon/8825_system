#!/bin/bash
# Task Truth Pipeline - Master Execution Script
# Runs all phases of the pipeline in sequence

set -e  # Exit on error

echo ""
echo "================================================================================"
echo "TASK TRUTH PIPELINE"
echo "Finding ground truth between board and code"
echo "================================================================================"
echo ""

# Phase 1: Sync
echo "📥 Phase 1: Syncing with Notion..."
python3 notion_sync.py pull
echo ""

# Phase 2: Validate
echo "🔍 Phase 2: Validating against codebase..."
python3 validate_tasks_against_code.py
echo ""

# Phase 3 & 4: Promote (requires user confirmation)
echo "🚀 Phase 3: Promoting validated tasks..."
echo "   (This will prompt for confirmation)"
python3 bulk_promote_validated_tasks.py
echo ""

# Phase 5: Export
echo "📄 Phase 4: Exporting bug report to Word..."
python3 export_bug_report_to_word.py
echo ""

echo "================================================================================"
echo "✅ TASK TRUTH PIPELINE COMPLETE"
echo "================================================================================"
echo ""
echo "📊 Check PIPELINE_EXECUTION_SUMMARY.md for results"
echo "📄 Bug report: ~/Documents/Joju/Joju_Bug_Report_$(date +%Y-%m-%d).docx"
echo ""
