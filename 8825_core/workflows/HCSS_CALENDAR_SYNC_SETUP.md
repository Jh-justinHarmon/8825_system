# HCSS Calendar Sync - Production Setup

**Status:** ✅ Production Ready  
**Created:** 2025-11-10  
**Last Updated:** 2025-11-10

## Overview

Automated OCR-based calendar sync from Microsoft Teams/Outlook to Google Calendar (harmon.justin@gmail.com). Bypasses Microsoft API restrictions by using screenshot OCR.

## Dependencies

### System Requirements
- **Python:** 3.9+ (currently using 3.9.6)
- **Tesseract OCR:** For text extraction from screenshots
- **Bash:** For sync scripts

### Python Packages
```
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
Pillow
pytesseract
```

### Google API
- **Credentials:** `8825_core/integrations/google/credentials.json`
- **Token:** `8825_core/integrations/google/token.json`
- **Scopes:** 
  - `https://www.googleapis.com/auth/calendar`
  - `https://www.googleapis.com/auth/calendar.events`
- **Target Calendar:** harmon.justin@gmail.com

## File Structure

```
8825_core/
├── workflows/
│   ├── hcss_calendar_sync.md          # Workflow documentation
│   ├── sync_hcss_calendar.sh          # One-command wrapper script
│   └── hcss_calendar_templates.md     # Manual event templates
├── integrations/google/
│   ├── calendar_screenshot_sync.py    # Main OCR sync script
│   ├── credentials.json               # Google API credentials
│   ├── token.json                     # OAuth token
│   └── README.md                      # Integration docs
└── INBOX_HUB/
    ├── sync_screenshots.sh            # Screenshot sync from Dropbox
    └── users/jh/intake/screenshots/   # Intake folder for OCR
```

## Shell Alias

**Command:** `hcss-cal-sync`  
**Location:** `~/.zshrc` (line 13)  
**Definition:**
```bash
alias hcss-cal-sync='cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/workflows" && ./sync_hcss_calendar.sh'
```

## Weekly Workflow

### Every Monday 8:00 AM CST

1. **Take Screenshot**
   - Open Microsoft Teams/Outlook calendar (week view)
   - Screenshot with Cmd+Shift+4
   - Auto-saves to: `~/Hammer Consulting Dropbox/Justin Harmon/Screenshots`

2. **Run Sync**
   ```bash
   hcss-cal-sync
   ```

3. **Verify**
   - Check harmon.justin@gmail.com calendar
   - Verify all 12 HCSS meetings created

**Time:** 2-3 minutes total

## Meeting Templates

The script creates 12 recurring HCSS meeting placeholders:

### Monday
- 12:30 PM - JustinBecky Check-in

### Tuesday
- 12:30 PM - JustinBecky Check-in
- 1:00 PM - Portal Development Weekly Touchbase
- 2:00 PM - TGIF Internal Touchbase

### Wednesday
- 10:00 AM - TGI Fridays | Crunchtime - Weekly Accounting Integration
- 12:30 PM - JustinBecky Check-in
- 1:00 PM - Crunchtime | Toast Readiness Kick Off Call
- 2:00 PM - Crunchtime | TGI Friday's - Weekly Project Call

### Thursday
- 11:00 AM - T.G.I. Friday's+Toast Weekly Sync
- 12:30 PM - JustinBecky Check-in
- 2:00 PM - Crunchtime | TGI Fridays - PM Sync Online

### Friday
- 12:30 PM - JustinBecky Check-in

**All events:**
- Prefixed with "HCSS Meeting -"
- 1-hour duration
- 10-minute reminder
- Created in harmon.justin@gmail.com

## Technical Details

### Screenshot Sync Pipeline

1. **Dropbox Screenshots** (locked location)
   - Path: `~/Hammer Consulting Dropbox/Justin Harmon/Screenshots`
   - Cannot be moved due to Dropbox sync

2. **Sync Script** (`sync_screenshots.sh`)
   - Copies from Dropbox → Intake folder
   - Filters: Last 7 days, Screenshot*.png files
   - Preserves metadata

3. **Intake Folder**
   - Path: `INBOX_HUB/users/jh/intake/screenshots/`
   - OCR script reads from here

### OCR Processing

1. **Auto-find Screenshot**
   - Search order: Intake → Dropbox → Downloads
   - Uses most recent Screenshot*.png

2. **Extract Text**
   - Tesseract OCR on full image
   - Extracts calendar header and time markers

3. **Create Events**
   - Uses hardcoded meeting template (12 meetings)
   - Calculates dates from week header
   - Creates via Google Calendar API

### Why This Approach

- **Microsoft API blocked:** IT restrictions prevent direct calendar access
- **Dropbox locked:** Screenshot folder cannot be moved
- **OCR reliable:** Consistent calendar layout makes OCR viable
- **Template-based:** Known recurring meetings, just need dates

## Troubleshooting

### "No screenshots found"
- Ensure screenshot taken (Cmd+Shift+4)
- Check Dropbox Screenshots folder has recent file
- Run sync manually: `cd INBOX_HUB && ./sync_screenshots.sh`

### "Authentication failed"
- Delete `token.json` and re-authenticate
- Ensure `credentials.json` exists
- Check Google API scopes include calendar access

### "Events not created"
- Verify harmon.justin@gmail.com calendar access
- Check for duplicate events (script skips existing)
- Review script output for specific errors

### Python version warning
- Currently using Python 3.9.6 (past EOL)
- Upgrade to Python 3.10+ recommended
- Does not affect functionality currently

## Integration Points

### Existing Systems
- **INBOX_HUB:** Uses existing screenshot sync infrastructure
- **Google Integration:** Shares auth with bill processor
- **jh-assistant:** Workflow documented for future automation

### Future Enhancements
- [ ] Automated Monday 8 AM reminder
- [ ] File watcher for auto-trigger on new screenshot
- [ ] Dynamic OCR parsing (vs hardcoded templates)
- [ ] Duplicate detection before creation
- [ ] Meeting time adjustments from OCR

## Maintenance

### Weekly
- Run `hcss-cal-sync` every Monday
- Verify events created correctly

### Monthly
- Check for duplicate events in calendar
- Update meeting templates if schedule changes

### As Needed
- Update Python packages: `pip3 install --upgrade google-api-python-client`
- Refresh Google OAuth token if expired
- Update meeting templates in `calendar_screenshot_sync.py` (lines 154-167)

## Success Metrics

- ✅ 12 events created per week
- ✅ Correct dates and times
- ✅ < 3 minutes total workflow time
- ✅ Zero manual calendar entry

## Support

**Documentation:**
- Workflow: `8825_core/workflows/hcss_calendar_sync.md`
- Integration: `8825_core/integrations/google/README.md`
- Templates: `8825_core/workflows/hcss_calendar_templates.md`

**Scripts:**
- Main: `8825_core/integrations/google/calendar_screenshot_sync.py`
- Wrapper: `8825_core/workflows/sync_hcss_calendar.sh`
- Screenshot sync: `INBOX_HUB/sync_screenshots.sh`

**Logs:**
- Script output shows sync progress
- Google Calendar API errors logged to console
