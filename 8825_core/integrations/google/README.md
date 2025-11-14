# 8825 Bill Processor

**Status:** ✅ Ready to test  
**Created:** 2025-11-09

---

## What It Does

Automatically processes bill images from Downloads:
1. **OCR** - Extracts text from images (jpg, png, heic)
2. **Categorize** - Identifies bills vs reference images
3. **Extract Info** - Vendor, amount, due date, account number
4. **Google Calendar** - Creates event on due date
5. **Google Drive** - Uploads bill to `8825_Bills` folder
6. **Archive** - Moves processed bills to `8825_processed/bills/`

---

## Setup Complete ✅

- ✅ Google Calendar API enabled
- ✅ Google Drive API enabled
- ✅ OAuth credentials configured
- ✅ Dependencies installed
- ✅ Added to MCP bridge

---

## First Run (Authorization)

The first time you run this, it will:
1. Open your browser
2. Ask you to sign in with **harmon.justin@gmail.com**
3. Grant permissions (Calendar + Drive)
4. Save token for future automatic runs

**Run it:**
```bash
cd 8825_core/integrations/google
python3 bill_processor.py
```

---

## How It Works

### Image Detection
Scans `~/Downloads/` for:
- `.jpg`, `.jpeg` - Photos
- `.png` - Screenshots/photos
- `.heic`, `.heif` - iPhone photos

### Bill Identification
Looks for keywords:
- "Amount Due", "Payment Due", "Total Due"
- "Invoice", "Bill", "Account Number"
- "Pay by", "Due Date"
- Dollar amounts with dates

**Confidence threshold:** 40% (adjustable)

### Information Extraction
- **Vendor:** Company name (first few lines)
- **Amount:** Largest dollar amount found
- **Due Date:** First date pattern found
- **Account:** Account/Acct number

### Google Integration
**Calendar Event:**
- Title: "Bill Due: [Vendor] - [Amount]"
- Date: Due date (or 30 days if not found)
- Reminder: 1 day before (email + popup)
- Description: Account number + Drive link

**Drive Upload:**
- Folder: `8825_Bills/`
- Filename: Original name
- Link attached to calendar event

---

## Usage

### Manual Run
```bash
cd 8825_core/integrations/google
python3 bill_processor.py
```

### Via MCP Bridge (Goose/Claude)
```
> "Process bills"
> "Check for new bills and add to calendar"
```

### Automatic (Future)
Add to inbox pipeline for automatic processing

---

## Example Output

```
Processing: ATT_bill.jpg
  ✓ OCR extracted 1247 characters
  → Category: bill (confidence: 0.80)
  → Vendor: AT&T
  → Amount: $125.00
  → Due: 11/15/2025
  ✓ Uploaded to Drive: https://drive.google.com/...
  ✓ Calendar event created: https://calendar.google.com/...
  ✓ Moved to: ~/Downloads/8825_processed/bills/ATT_bill.jpg

==================================================
Processed: 1 images
Bills found: 1
Calendar events created: 1
```

---

## Supported Formats

### Images
- ✅ JPG/JPEG
- ✅ PNG
- ✅ HEIC (iPhone photos)
- ✅ HEIF

### Bill Types
- Utility bills
- Credit card statements
- Invoices
- Service bills
- Any document with amount + due date

---

## Configuration

### Change Confidence Threshold
Edit `bill_processor.py`:
```python
if category == 'bill' and confidence >= 0.4:  # Change 0.4 to desired threshold
```

### Change Calendar
Default: Primary calendar  
To use specific calendar, edit:
```python
calendarId='primary'  # Change to calendar ID
```

### Change Drive Folder
Edit:
```python
folder_name: str = '8825_Bills'  # Change folder name
```

---

## Troubleshooting

### "OCR dependencies not installed"
```bash
pip3 install pillow pytesseract pillow-heif
brew install tesseract  # macOS
```

### "Authentication failed"
Delete token and re-auth:
```bash
rm token.json
python3 bill_processor.py
```

### "No images found"
Check Downloads folder has images:
```bash
ls ~/Downloads/*.{jpg,png,heic}
```

### "Calendar event failed"
Check Calendar API is enabled in Google Cloud Console

### "Drive upload failed"
Check Drive API is enabled in Google Cloud Console

---

## Next Steps

### Phase 2 Enhancements
- [ ] AI-powered categorization (GPT-4 Vision)
- [ ] Better date parsing (relative dates)
- [ ] Multiple bill support in one image
- [ ] Email notifications
- [ ] Recurring bill detection
- [ ] Payment tracking

### Integration
- [ ] Add to inbox pipeline (automatic)
- [ ] Mobile trigger (upload photo → auto-process)
- [ ] Slack notifications
- [ ] Export to accounting software

---

## Files

```
8825_core/integrations/google/
├── README.md              # This file
├── bill_processor.py      # Main processor
├── credentials.json       # OAuth credentials (DO NOT COMMIT)
├── token.json            # Auth token (DO NOT COMMIT)
└── requirements.txt       # Python dependencies
```

---

## Security Notes

**DO NOT commit to git:**
- `credentials.json` - OAuth client secret
- `token.json` - User access token

**Add to .gitignore:**
```
8825_core/integrations/google/credentials.json
8825_core/integrations/google/token.json
```

---

## Summary

**Status:** Ready to test  
**First run:** Will open browser for auth  
**After auth:** Fully automatic  
**MCP tool:** `process_bills`  

**Ready to process your first bill!** 📄→📅

---

# HCSS Calendar Screenshot Sync

**Status:** ✅ Ready to use  
**Created:** 2025-11-10

## What It Does

Syncs HCSS meetings from Microsoft calendar to Google Calendar via OCR:
1. **Screenshot** - Take screenshot of Microsoft Teams/Outlook calendar
2. **OCR** - Extract meeting details from image
3. **Parse** - Identify HCSS meetings and times
4. **Create** - Add events to harmon.justin@gmail.com calendar

## Usage

### Quick Sync
```bash
# 1. Take screenshot of calendar (Cmd+Shift+4)
# 2. Run sync
cd 8825_core/integrations/google
python3 calendar_screenshot_sync.py
```

### Specify Screenshot
```bash
python3 calendar_screenshot_sync.py ~/Downloads/Screenshot.png
```

### Different Target Calendar
```bash
python3 calendar_screenshot_sync.py --target other@gmail.com
```

## How It Works

1. **Find Screenshot** - Looks for latest Screenshot*.png in Downloads
2. **OCR Extract** - Uses Tesseract to extract text
3. **Parse Week** - Identifies week dates (Mon 10, Tue 11, etc.)
4. **Find HCSS Meetings** - Matches patterns: JustinBecky, TGIF, Crunchtime, Toast, etc.
5. **Extract Times** - Parses times (10 AM, 1 PM, etc.)
6. **Create Events** - Adds to Google Calendar with 10-min reminders

## Example Output

```
📸 Processing calendar screenshot: Screenshot 2025-11-10.png

Running OCR...
✓ Extracted 1247 characters

Week: 11/10 - 11/16

Extracting HCSS meetings...
  → Found: Portal Development Weekly Touchbase on Tue 11/11 at 13:00
  → Found: TGIF Internal Touchbase on Tue 11/11 at 14:00
  → Found: TGI Fridays | Crunchtime on Wed 11/12 at 10:00
  → Found: Crunchtime | Toast Readiness on Wed 11/12 at 13:00

✓ Found 4 HCSS meetings

Creating events in harmon.justin@gmail.com...
  ✓ Created: Portal Development Weekly Touchbase
  ✓ Created: TGIF Internal Touchbase
  ✓ Created: TGI Fridays | Crunchtime
  ✓ Created: Crunchtime | Toast Readiness

==================================================
Sync complete!
Created: 4/4
==================================================
```

## Weekly Workflow

**Every Monday:**
1. Open Microsoft Teams/Outlook calendar (week view)
2. Take screenshot (Cmd+Shift+4) - saves to Dropbox Screenshots
3. Run one-command sync: `cd ../../workflows && ./sync_hcss_calendar.sh`
4. Verify events in harmon.justin@gmail.com

**Or manual steps:**
1. Sync screenshot: `cd ../../../INBOX_HUB && ./sync_screenshots.sh`
2. Run OCR: `cd ../8825_core/integrations/google && python3 calendar_screenshot_sync.py`

**Time:** 2-3 minutes

**Note:** Screenshot saves to Dropbox Screenshots folder (locked location). The sync script copies it to the intake folder where OCR can access it.

## Troubleshooting

**"No screenshots found"**
- Take screenshot first (Cmd+Shift+4)
- Or specify path: `python3 calendar_screenshot_sync.py ~/path/to/screenshot.png`

**"No HCSS meetings found"**
- Check screenshot includes meeting titles
- Verify meetings contain HCSS keywords (JustinBecky, TGIF, Crunchtime, Toast)
- Try higher resolution screenshot

**"OCR extracted 0 characters"**
- Install Tesseract: `brew install tesseract`
- Check screenshot is readable

**"Wrong times extracted"**
- OCR may misread times - verify and adjust manually
- Future: Add time validation/correction

## Integration

- **jh-assistant:** Runs through jh-assistant integration layer
- **Workflow:** `8825_core/workflows/hcss_calendar_sync.md`
- **Monday Reminder:** Automated via workflow
- **Auth:** Uses same Google credentials as bill processor

---

**Ready to sync your calendar!** 📸→📅
