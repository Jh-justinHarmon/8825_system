# Simplified Inbox Architecture

## Problem Statement
Too many folders, bidirectional sync causing conflicts, files not staying clean.

## New Simple Flow

```
Mobile Upload → iCloud Downloads
                      ↓
                Local Downloads (one-way sync)
                      ↓
                Process immediately
                      ↓
                Archive to processed/
```

## Folders

### Active Intake
- `~/Downloads/` - Primary intake folder
  - `0-8825_BRAIN_TRANSPORT.json` - Always at top
  - Unprocessed files only
  - Gets cleaned immediately after processing

### Archives
- `~/Downloads/8825_processed/` - Processed files archive

### Screenshots
- `INBOX_HUB/users/jh/intake/screenshots/` - Current location (unchanged)

## Eliminated
- ❌ `8825_inbox/` folder (was pre-MCP workaround, no longer needed)
- ❌ Bidirectional sync (causes duplication issues)
- ❌ Multiple Downloads syncing (simplified to iCloud → Local only)

## Processing Steps

1. **Sync** - iCloud Downloads → Local Downloads (one-way)
2. **Rename brain** - Ensure `0-` prefix for top position
3. **Process** - Run through ingestion engine on Downloads files directly
4. **Archive** - Move processed files immediately to 8825_processed/
5. **Clean** - Downloads stays clean with only brain + unprocessed files

## Mobile Flow
iPhone → Upload to iCloud Downloads → Auto-sync to Mac Downloads → Process

## Desktop Flow  
Copy/paste directly to LLM (no Downloads needed)

## Result
Clean Downloads folder with:
- `0-8825_BRAIN_TRANSPORT.json` (always visible at top)
- Current unprocessed files (if any)
- Nothing else
