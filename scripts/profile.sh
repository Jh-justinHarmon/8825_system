#!/bin/bash
# 8825 Profile Management
# Wrapper for profile_manager.py

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Set SYSTEM_ROOT for path utilities
export SYSTEM_ROOT="$ROOT_DIR"

# Run profile manager
python3 "$ROOT_DIR/8825_core/brain/profile_manager.py" "$@"
