# Phil's Ledger - Proof of Concept

**Status:** ✅ Working POC  
**Date:** 2025-11-09  
**Owner:** Justin Harmon (Jh)

---

## What's Working

### **Phase 1: Bill Processing** ✅
- Downloads → OCR → Extract info
- Google Calendar event creation
- Google Drive upload
- CSV export to Phil's Ledger

**File:** `bill_processor.py`

### **Phase 2: Phil's Ledger App** ✅
- Single-file HTML app
- Import CSV files
- View/search/filter bills
- Mark as paid
- Export data
- LocalStorage persistence

**File:** `phils_ledger.html`

---

## How to Use

### **1. Process Bills**
```bash
cd 8825_core/integrations/google
python3 bill_processor.py
```

**Output:**
- Calendar event created
- Drive file uploaded
- CSV exported to: `users/justin_harmon/jh_assistant/data/phils_ledger_imports/bills_YYYY-MM.csv`

---

### **2. Open Phil's Ledger**
```bash
open users/justin_harmon/jh_assistant/data/phils_ledger.html
```

Or double-click the file in Finder.

---

### **3. Import Bills**
1. Click "📁 Import CSV"
2. Navigate to `users/justin_harmon/jh_assistant/data/phils_ledger_imports/`
3. Select `bills_2025-11.csv`
4. Bills appear in table with "NEW" badge

---

### **4. Manage Bills**
- **Search:** Type vendor/amount
- **Filter:** All/Unpaid/Paid/New
- **Mark Paid:** Click button
- **View Links:** Click 📁 (Drive) or 📅 (Calendar)
- **Export:** Download as CSV

---

## What's NOT Built Yet

### **Phase 3: Gmail Monitoring** ❌
- Multi-account monitoring (harmon.justin@gmail.com + jkl.7247.ap@gmail.com)
- Email attachment extraction
- Auto-processing

### **Phase 4: Universal Router** ❌
- Config-driven routing
- Focus-based separation
- TrustyBits support

### **Phase 5: Monarch Integration** ❌
- Bank transaction sync
- Auto-reconciliation
- Matching algorithm

### **Phase 6: Auto-Import** ❌
- File watcher for new CSVs
- Automatic import without manual click

---

## Files in This POC

```
phils_ledger_poc/
├── README.md              # This file
├── bill_processor.py      # Bill processing script (with CSV export)
└── phils_ledger.html      # Single-file web app
```

---

## Testing Checklist

- [ ] Put bill image in ~/Downloads
- [ ] Run bill_processor.py
- [ ] Verify Calendar event created
- [ ] Verify Drive upload
- [ ] Verify CSV created in phils_ledger_imports/
- [ ] Open phils_ledger.html
- [ ] Import CSV
- [ ] Verify bill appears with "NEW" badge
- [ ] Test search/filter
- [ ] Mark bill as paid
- [ ] Verify stats update
- [ ] Test Drive/Calendar links
- [ ] Export to CSV
- [ ] Refresh page (verify LocalStorage persistence)

---

## Next Steps (Future)

1. **Gmail Monitoring** (3-4 hours)
   - Add `gmail_monitor.py`
   - Multi-account OAuth setup
   - Attachment extraction

2. **Universal Router** (2-3 hours)
   - Refactor to config-driven
   - Add focus configs
   - Support TrustyBits

3. **Auto-Import** (2 hours)
   - File watcher
   - Automatic CSV detection
   - Background import

4. **Monarch Integration** (4-6 hours)
   - Research API availability
   - Implement matching algorithm
   - Add reconciliation UI

---

## Architecture

```
Bill Image (Downloads or Gmail)
         ↓
    bill_processor.py
         ↓
    ┌────┴────┬─────────┬──────────┐
    ↓         ↓         ↓          ↓
  GCal     GDrive     CSV      Archive
  Event    Upload    Export    Original
                       ↓
              phils_ledger.html
                       ↓
              Import → Manage → Export
```

---

## Full Design Document

See: `phils_ledger_pipeline_brainstorm.md` for complete architecture, Gmail setup, Monarch integration, and future enhancements.

---

**POC Status:** Ready for testing and iteration
