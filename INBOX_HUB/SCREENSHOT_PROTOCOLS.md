# Screenshot Processing Protocols

## Overview

Screenshots are automatically processed with OCR and routed based on content type.

**Location:** `~/Hammer Consulting Dropbox/Justin Harmon/Screenshots/`

**Workflow:**
1. Screenshot appears in main folder
2. OCR extracts text
3. Content type detected
4. Processed accordingly
5. Moved to `- ARCHV -`

---

## Content Types

### 1. KARSEN Protocol 🎯

**Detection:** "KARSEN" appears at top of image

**Purpose:** Departure time schedule for KARSEN

**Expected Format:**
```
KARSEN
Monday 7:30 AM
Wednesday 8:00 AM
Friday 7:45 AM
```

**Processing:**
- Extract day and time
- Add to Google Calendar
- **Same week as when photo is viewed**
- **AM departure times**
- **No travel time or buffer**
- **Exact time written = departure time**

**Calendar Event:**
- Title: "KARSEN Departure"
- Time: Exact time from paper
- Duration: 15 min (placeholder)

---

### 2. Bills Protocol 💵

**Detection:** Keywords like "invoice", "bill", "payment due", "total", "statement"

**Processing:**
- Route to 3 destinations:
  1. **Calendar** - Add due date
  2. **Drive** - File in Bills folder
  3. **Ledger** - Track payment

**Monitoring:** Watch for errors in routing

---

### 3. Folder Screenshots 📁

**Detection:** Shows Finder window with folder path

**Processing:**
- Launch **Screengrab Swap**
- Prompt: "What are you looking for?"
- Search folder
- Find file
- Take screenshot of file
- Save to Downloads
- Replace original screenshot

---

### 4. Standard Screenshots 📄

**Detection:** Anything else

**Processing:**
- OCR text extracted
- Saved to metadata
- Archived

---

## Usage

### Manual Processing

```bash
cd INBOX_HUB
python3 ocr_processor_v2.py
```

### Auto-Watcher (Daemon)

```bash
cd INBOX_HUB
python3 watch_screenshots.py &
```

Monitors folder and auto-processes new screenshots.

---

## File Structure

```
~/Hammer Consulting Dropbox/Justin Harmon/Screenshots/
├── Screenshot1.png          # Unprocessed (OCR pending)
├── Screenshot2.png          # Unprocessed
└── - ARCHV -/              # Processed files
    ├── Screenshot3.png
    └── Screenshot4.png
```

**Rule:** Only unprocessed files in main folder. After OCR, move to `- ARCHV -`.

---

## Examples

### KARSEN Example

**Input Screenshot:**
```
KARSEN
Monday 7:30 AM
Wednesday 8:00 AM
Friday 7:45 AM
```

**Output:**
- 3 calendar events created
- Monday at 7:30 AM - KARSEN Departure
- Wednesday at 8:00 AM - KARSEN Departure  
- Friday at 7:45 AM - KARSEN Departure
- All in same week as today

### Bill Example

**Input Screenshot:**
```
INVOICE #12345
Amount Due: $150.00
Due Date: Nov 15, 2025
```

**Output:**
- Calendar event: Nov 15 - Pay Invoice #12345
- File saved to Drive: Bills/2025/November/
- Ledger entry created

---

## Troubleshooting

### OCR Not Detecting KARSEN

- Ensure "KARSEN" is clearly visible at top
- Check image quality (not blurry)
- Try re-taking screenshot with better lighting

### Times Not Extracted

- Format should be: "Day HH:MM AM/PM"
- Example: "Monday 7:30 AM"
- Avoid extra text on same line

### Files Not Moving to Archive

- Check permissions on `- ARCHV -` folder
- Ensure no other process is accessing file
- Try manual move first

---

## Future Enhancements

- [ ] Post-it detection → FigJam
- [ ] Receipt detection → Expense tracking
- [ ] Meeting notes → Notion
- [ ] Code snippets → GitHub Gist
- [ ] LLM semantic understanding

---

## Related Scripts

- `ocr_processor_v2.py` - Main OCR processor
- `watch_screenshots.py` - Auto-watcher daemon
- `screengrab_swap.py` - Folder screenshot handler
- `enhanced_routing_rules.py` - Routing logic
