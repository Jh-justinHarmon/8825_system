# Progressive Routing System - Complete Documentation

**Built:** 2025-11-11  
**Build Time:** 25 minutes (estimated 6 hours - 14.4x faster)  
**Status:** ✅ Ready for testing

---

## 🎯 What It Does

Automatically routes files from Downloads to their correct destinations, building trust through successful uses. Starts with manual selection, graduates to full automation.

---

## 🏗️ Architecture

### 4-Level Trust Progression (Per Protocol)

**Level 0: Manual Selection** (First time)
- User picks protocol from ranked list
- System learns the pattern

**Level 1: Auto-Suggested** (After 1 success)
- System suggests protocol
- User confirms or changes

**Level 2: Auto-Applied** (After 2 successes)
- System routes automatically
- User confirms after execution

**Level 3: Full Automation** (After 3 successes)
- Routes silently
- Shows in daily summary

**Demotion:** Any correction → Back to Level 0

---

## 📦 Components

### Core System
- `progressive_router.py` - Main routing engine
- `protocol_templates.json` - Available routing protocols
- `protocol_trust.json` - Per-user trust tracking

### Safety Protocols
- `exclusion_protocol.py` - Critical files (BRAIN_TRANSPORT, etc.)
- `deduplication_protocol.py` - Prevents reprocessing
- `auto_unpack_protocol.py` - Extracts archives + checks dupes

### User Interface
- `interactive_selector.py` - Manual protocol selection UI
- `time_tracker.py` - Build efficiency + user savings metrics

### Processing Flow
```
Downloads/
  ↓
Exclusion Filter (skip BRAIN_TRANSPORT, etc.)
  ↓
Auto-Unpack (extract .zip, .tar, etc.)
  ↓
Deduplication Check (skip already processed)
  ↓
8825_processing/ (user-visible staging)
  ↓
Protocol Matching (confidence scoring)
  ↓
Trust-Based Routing (Level 0-3)
  ↓
Final Destination (Calendar, Drive, etc.)
```

---

## 🚀 Usage

### Scan Downloads Folder
```bash
cd INBOX_HUB

# Dry run (preview only)
./progressive_router.py scan --dry-run

# Real run
./progressive_router.py scan

# Include screenshots
./progressive_router.py scan --screenshots

# Unified scan (sync screenshots + process everything)
./unified_scan.sh
./unified_scan.sh --dry-run
```

### Manual Protocol Selection
```bash
# For files needing selection (Level 0)
./interactive_selector.py
```

### Check Status
```bash
# View processing folder
./progressive_router.py status

# View protocol templates
./progressive_router.py templates

# View undo stack
./progressive_router.py undo
```

### Pause/Resume
```bash
# Emergency stop
./progressive_router.py pause

# Resume automation
./progressive_router.py resume
```

### Standalone Tools
```bash
# Check exclusions
./exclusion_protocol.py filter ~/Downloads/

# Check duplicates
./deduplication_protocol.py scan ~/Downloads/8825_processing/

# Unpack archives
./auto_unpack_protocol.py scan ~/Downloads/8825_processing/

# View metrics
cd ../8825_core/metrics/
./time_tracker.py stats
./time_tracker.py savings
```

---

## 📁 File Locations

### User-Visible
- `~/Downloads/` - Original location
- `~/Downloads/8825_processing/` - Staging area (transparent)
- `~/Downloads/8825_processing/_unpacked/` - Extracted archives
- `~/Downloads/8825_processed/` - Archive by date

### System Internal
- `INBOX_HUB/users/jh/protocol_trust.json` - Trust tracking
- `INBOX_HUB/users/jh/protocol_templates.json` - Enabled protocols
- `INBOX_HUB/users/jh/exclusions.json` - Exclusion rules
- `INBOX_HUB/users/jh/deduplication.json` - Processed file hashes
- `INBOX_HUB/users/jh/undo_stack.json` - Last 7 days of actions

---

## 🎨 Visual Status Indicators

Files in processing folder have emoji prefixes:

- `[⏳]` - Scanning (OCR/analysis in progress)
- `[?]` - Awaiting selection (needs user input)
- `[→]` - Suggested (protocol recommended)
- `[⚡]` - Routing (executing)
- `[✓]` - Routed (successfully processed)
- `[❌]` - Error (needs attention)

---

## 🚫 Exclusion Rules

### Critical (Never Touch)
- `*BRAIN_TRANSPORT*.json` - System transport file
- `.DS_Store` - macOS metadata
- `*.tmp`, `*.lock` - Temporary files

### Sticky (Stay in Downloads)
- `sticky_*` - User-defined
- `*_sticky.*` - User-defined

### Custom
- User can add via `exclusion_protocol.py add <pattern>`

---

## 🔄 Undo System

### 3 Levels of Undo

**Level 1: Undo Last Batch** (24 hours)
```bash
./progressive_router.py undo
# Select most recent batch
```

**Level 2: Undo Specific Item** (7 days)
```bash
./progressive_router.py undo
# Select specific item from history
```

**Level 3: Restore from Archive** (30 days)
```bash
# Browse ~/Downloads/8825_processed/YYYY-MM-DD/
# Manually restore any file
```

---

## 📊 Protocol Templates

### Built-In Templates

**KARSEN Schedule** (disabled by default)
- Detects: "KARSEN" keyword
- Routes to: Calendar
- Confidence: 85%
- Type: Screenshot

**Bills & Invoices** (disabled by default)
- Detects: "invoice", "bill", "payment due"
- Routes to: Drive + Calendar
- Confidence: 75%
- Type: Document/Screenshot

**Meeting Screenshots** (disabled by default)
- Detects: "meeting", "zoom", "teams"
- Routes to: Notes
- Confidence: 70%
- Type: Screenshot

**Receipts** (disabled by default)
- Detects: "receipt", "total", "paid"
- Routes to: Expense Tracker
- Confidence: 75%
- Type: Screenshot

**Screenshot Archive** (enabled by default)
- Detects: All files (fallback)
- Routes to: Archive
- Confidence: 50%
- Type: Screenshot/Document

### Enable/Disable Templates
```bash
# Edit: INBOX_HUB/users/jh/protocol_templates.json
# Set "enabled": true/false for each template
```

---

## 📈 Metrics & Time Savings

### Build Efficiency
- Estimated: 6 hours
- Actual: 25 minutes
- Efficiency: 14.4x faster

### User Time Savings (Projected)

**Before Automation:**
- 10 min per scan × 2 scans/day = 20 min/day

**After 1 Week (Level 1-2):**
- 2 min per scan × 2 scans/day = 4 min/day
- **Saves 16 min/day = 8 hours/month**

**After 1 Month (Level 3):**
- 0.5 min per scan × 2 scans/day = 1 min/day
- **Saves 19 min/day = 9.5 hours/month**

**Annual Savings:**
- 114 hours/year (14.25 days)
- User saves ~2 full weeks per year

---

## 🎓 How It Learns

### Pattern Recognition
1. User selects protocol for file type
2. System records: file type + keywords + destination
3. Next similar file: System suggests same protocol
4. After 3 successful uses: Full automation

### Confidence Scoring
- Keyword matching: +50% base
- Trust level: +5% per level
- Historical success: +10% per use
- Decay: -1 level after 30 days unused

### Example Learning Path

**Day 1:** Screenshot with "KARSEN" → User selects Calendar
- Level 0 → Level 1

**Day 2:** Another KARSEN screenshot → System suggests Calendar → User confirms
- Level 1 → Level 2

**Day 3:** Another KARSEN screenshot → System routes to Calendar → User confirms
- Level 2 → Level 3

**Day 4+:** All KARSEN screenshots → Auto-routed to Calendar
- Level 3 (full automation)

---

## 🔧 Troubleshooting

### Files Not Processing
```bash
# Check exclusions
./exclusion_protocol.py check <file>

# Check if duplicate
./deduplication_protocol.py check <file>

# Check processing folder
ls ~/Downloads/8825_processing/
```

### Wrong Routing
```bash
# Undo the batch
./progressive_router.py undo

# Protocol will demote to Level 0
# Next time, select correct protocol
```

### Archive Not Unpacking
```bash
# Check if supported
./auto_unpack_protocol.py check <file>

# Manually unpack
./auto_unpack_protocol.py unpack <file>
```

### System Paused
```bash
# Resume automation
./progressive_router.py resume
```

---

## 🎯 Testing Checklist

### Phase 1: Manual Selection (Current State)
- [ ] Run `progressive_router.py scan` on 14 files
- [ ] Use `interactive_selector.py` to choose protocols
- [ ] Verify files route correctly
- [ ] Check trust levels increment

### Phase 2: Suggested Routing
- [ ] Process similar files again
- [ ] Verify system suggests previous protocols
- [ ] Confirm or adjust suggestions
- [ ] Watch Level 1 → Level 2 promotion

### Phase 3: Auto-Applied
- [ ] Process similar files third time
- [ ] Verify auto-routing with confirmation
- [ ] Test undo functionality
- [ ] Watch Level 2 → Level 3 promotion

### Phase 4: Full Automation
- [ ] Process similar files fourth+ time
- [ ] Verify silent routing
- [ ] Check daily summary
- [ ] Validate 95%+ accuracy

---

## 🚀 Next Steps

1. **Enable Protocol Templates**
   - Edit `users/jh/protocol_templates.json`
   - Enable KARSEN, Bills, etc. as needed

2. **Process Current Files**
   - Run `progressive_router.py scan`
   - Use `interactive_selector.py` for Level 0 files
   - Build initial trust patterns

3. **Monitor & Refine**
   - Watch trust levels build
   - Adjust protocols based on corrections
   - Add custom exclusions as needed

4. **Integrate with Existing Systems**
   - Connect to OCR engine for screenshots
   - Link to calendar API for events
   - Hook into Drive for document filing

5. **Automate Scanning**
   - Set up cron job or LaunchAgent
   - Run every 4-6 hours
   - Email daily summaries

---

## 📝 Philosophy Alignment

### Precipice Principle ✅
- Transparent (processing folder visible)
- Controllable (undo always available)
- Progressive disclosure (Level 0 → 3)
- Manual override (pause button)

### Progressive Onboarding ✅
- Start read-only (dry run mode)
- Build trust through use (4 levels)
- Low friction (smart batch confirmation)
- Safety nets (exclusions, dedup, undo)

### User Experience ✅
- Files never lost (processing folder)
- Clear status (emoji prefixes)
- Obvious undo (7-day stack)
- Fast validation (batch grouping)

---

## 🎉 Success Criteria

### System Accuracy
- [ ] 95%+ routing accuracy in Level 3
- [ ] <5% items need review in Level 2
- [ ] <2% undo rate overall

### User Confidence
- [ ] Justin trusts it enough to use daily
- [ ] Would recommend to customers
- [ ] Feels transparent and controllable
- [ ] Undo system provides safety net

### Production Readiness
- [ ] Onboarding flow tested
- [ ] Documentation complete
- [ ] Error handling robust
- [ ] Support runbook ready

---

**Status:** Ready for real-world testing with 14 files in processing folder.

**Next:** Run `./progressive_router.py scan` and `./interactive_selector.py` to begin.
