# Local Task Cache

This directory contains cached task data from Notion.

## Files

- `tasks.json` - All tasks synced from Notion
- `last_sync.json` - Timestamp and sync metadata

## Purpose

Local cache allows:
- Offline task viewing
- Faster task queries
- Backup of task data
- Conflict detection

## Sync Status

Run `python3 ../notion_sync.py status` to check sync status.

## Do Not Edit

Files in this directory are automatically generated.  
Manual edits will be overwritten on next sync.

Use `task_manager.py` or `notion_sync.py` to make changes.
