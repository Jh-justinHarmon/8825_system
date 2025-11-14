#!/bin/bash
# Get the latest sticky_notes_vision.json file

JSON_FILE="$HOME/Downloads/sticky_notes_vision.json"

if [ -f "$JSON_FILE" ]; then
    cat "$JSON_FILE"
    exit 0
else
    echo "Error: JSON file not found at $JSON_FILE" >&2
    exit 1
fi
