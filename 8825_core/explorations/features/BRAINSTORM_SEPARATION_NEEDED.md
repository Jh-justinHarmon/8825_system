# ⚠️ Brainstorm Separation Needed

**Source File:** `~/Downloads/8825_brainstorm_mining_this_chat.txt`  
**Status:** Needs manual separation into 10 individual explorations  
**Date Identified:** 2025-11-09

---

## 📋 FILE STRUCTURE

This single file contains **10 separate brainstorms** across 5 categories:

### **SECTION A - RAL (2 brainstorms)**
1. **RAL Statement Tagger** (drag-and-drop)
   - Zero-friction text normalization
   - Tags/entities/dates extraction
   - NOW priority (1-3 days)

2. **RAL Batch Statement Collector**
   - Bulk email/doc ingestion
   - Deduplication
   - NEXT priority (3-7 days)

### **SECTION B - TGIF (3 brainstorms)**
3. **TGIF Meeting Summary + Weekly Update**
   - One-click meeting recaps
   - Auto weekly rollup
   - NOW priority (1-3 days)

4. **TGIF Location Launch Prep Pipeline**
   - Store launch checklists
   - Dependency tracking
   - NEXT priority (3-7 days)

5. **TGIF Auto Rollout Adjuster**
   - Rollout plan optimization
   - Readiness signals
   - LATER priority (7-14 days)

### **SECTION C - PERSONAL (2 brainstorms)**
6. **Weekend Soccer Advisor**
   - Travel time + arrival calculation
   - "Leave by" notifications
   - NOW priority (1-3 days)

7. **Personal Time Tracker** (15-min blocks)
   - Gentle timeboxing
   - Calendar integration
   - LATER priority (7-14 days)

### **SECTION D - FILES/STORAGE (1 brainstorm)**
8. **Dropbox File Reduction Manager**
   - Dedupe, compress, archive
   - Undo log
   - LATER priority (7-14 days)

### **SECTION E - REAL ESTATE (2 brainstorms)**
9. **Wedgewood AI Value Calculation Tool**
   - Risk-adjusted offer scoring
   - Expected net to seller
   - NEXT priority (3-7 days)

10. **LHL Re-Listing Pipeline**
    - Photo intake + reordering
    - MLS descriptions in Laura's voice
    - LATER priority (7-14 days)

---

## 🎯 RECOMMENDED SEPARATION

### **Create Individual Files:**

**HCSS Focus:**
```
8825_core/explorations/features/hcss/
├── ral_statement_tagger.md
├── ral_batch_collector.md
├── tgif_meeting_summary.md
├── tgif_location_launch_prep.md
└── tgif_rollout_adjuster.md
```

**Personal:**
```
8825_core/explorations/features/personal/
├── weekend_soccer_advisor.md
├── time_tracker_15min.md
└── dropbox_file_reduction.md
```

**Real Estate:**
```
8825_core/explorations/features/real_estate/
├── wedgewood_offer_calculator.md
└── lhl_relisting_pipeline.md
```

---

## 📊 PRIORITIZATION

**NOW (Quick Wins, 1-3 days):**
1. RAL Statement Tagger
2. TGIF Meeting Summary
3. Weekend Soccer Advisor

**NEXT (3-7 days):**
4. RAL Batch Collector
5. TGIF Location Launch Prep
6. Wedgewood Offer Calculator

**LATER (7-14 days):**
7. TGIF Rollout Adjuster
8. Dropbox File Reduction
9. Personal Time Tracker
10. LHL Re-Listing Pipeline

---

## 🔧 COMMON BUILDING BLOCKS

All 10 brainstorms share these reusable components:
- Calendar Linker (Google Calendar read/write)
- Location & ETA Engine (Maps + travel time)
- Dropbox Delta Watcher (webhooks + dedupe)
- Summarizer (LLM → normalized JSON)
- Tagger (rules + small model)
- Webhook Renewer (resilient subscriptions)
- Timezone Normalizer (UTC internal, user tz display)

---

## 🚀 NEXT ACTIONS

1. **Manual Separation Required:**
   - Extract each brainstorm from source file
   - Create 10 individual exploration files
   - Preserve full specs, schemas, MVP steps

2. **Categorize by Focus:**
   - HCSS: 5 brainstorms (RAL + TGIF)
   - Personal: 3 brainstorms
   - Real Estate: 2 brainstorms

3. **Update Explorations README:**
   - List all 10 separately
   - Note focus area for each
   - Update pipeline count

4. **Prioritize for Implementation:**
   - NOW items → Move to active projects
   - NEXT items → Keep in exploration
   - LATER items → Time-box for review

---

## 📝 NOTES

- **Source file preserved:** `~/Downloads/8825_brainstorm_mining_this_chat.txt`
- **All specs included:** Each brainstorm has full MVP steps, schemas, flows
- **Implementation-ready:** Can be dropped into projects immediately
- **Cross-cutting:** Building blocks should be extracted to core utilities

---

**This file serves as a placeholder until manual separation is complete.**
