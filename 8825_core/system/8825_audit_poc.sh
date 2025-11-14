#!/bin/bash
# Convenience wrapper for POC auditor

SYSTEM_ROOT="/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"

cd "$SYSTEM_ROOT"
python3 "$SYSTEM_ROOT/8825_core/system/audit_poc.py" "$@"
