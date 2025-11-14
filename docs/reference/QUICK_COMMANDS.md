# Quick Commands for Cascade

## Memory Loading

### Load Full Session Context
```
load MLP chat mode
```

**What it loads:**
- All systems built (6 systems)
- Roadmap status (6 items)
- Time calibration factors
- File locations
- Meeting prep context
- Joju work context

**Files loaded:**
- `Documents/MLP_CHAT_MODE.md`
- `Documents/SESSION_MEMORY_EXPORT_20251108.md`

---

## System Quick Access

### Meeting Prep System
```
cd 8825_core/meeting_prep
python3 meeting_prep_cli.py
```

### Input Hub
```
cd INBOX_HUB
./sync_screenshots.sh
./checking_sg.sh
```

### Roadmap
```
cd Documents/roadmap
cat QUICK_START.md
jq '.items[]' foundation_sprint_backlog.json
```

### Partner Credit
```
cd 8825_core/protocols
cat PARTNER_CREDIT_README.md
```

---

## Common Cascade Requests

### Check Roadmap Status
```
What's in the roadmap?
```

### View Time Calibration
```
What are the time calibration factors?
```

### Get System Location
```
Where is the [system name]?
```

### Load Recent Work
```
What did we build on November 8?
```

---

## File Locations Quick Reference

| System | Location |
|--------|----------|
| Meeting Prep | `8825_core/meeting_prep/` |
| Time Calibration | `8825_core/system/time_calibration.py` |
| Inbox Ingestion | `8825_core/workflows/ingestion/` |
| Input Hub | `INBOX_HUB/` |
| Roadmap | `Documents/roadmap/` |
| Partner Credit | `8825_core/protocols/` |
| Session Exports | `Documents/SESSION_MEMORY_EXPORT_*.md` |
| MLP Chat Mode | `Documents/MLP_CHAT_MODE.md` |

---

## Memory Load Protocol (MLP)

**Trigger:** `load MLP chat mode`

**Purpose:** Restore full context from most recent session

**What happens:**
1. Cascade reads `MLP_CHAT_MODE.md`
2. Cascade loads latest session export
3. Full context restored
4. Ready to continue work

**Manual alternative:**
```
Read Documents/MLP_CHAT_MODE.md and Documents/SESSION_MEMORY_EXPORT_20251108.md
```

---

**Keep this file handy for quick reference in any Cascade window!**
