# Contractor Bid Builder - Action Plan

**Date:** 2025-11-09  
**Status:** Pre-Build (Data Collection Phase)  
**Owner:** Justin Harmon

---

## 🎯 GOAL

Collect necessary data and test tools before building Phase 0 MVP

---

## 📋 ACTION ITEMS

### **1. Get Test CubiCasa Plan** 🏠 ✅

**What:** Use existing CubiCasa floor plans for testing

**Test Property:** Mary's house (Laura still has access for enhanced measurements testing)

**Steps:**
1. [x] Decide which property to use → Mary's house
2. [ ] Upload existing CubiCasa floor plans to test data folder
3. [ ] Save to: `8825_core/explorations/features/contractor_bid_tool_test_data/cubicasa/`
4. [ ] Schedule visit to Mary's house with Laura for enhanced measurements testing

**Timeline:** This week (upload plans) + schedule visit

**Output:**
- Floor plan SVG (scalable)
- Floor plan PDF (printable)
- Floor plan PNG (image)
- Enhanced measurements test data from Mary's house

---

### **2. Research Enhanced Measurement Options** 🔍

**What:** Evaluate measurement tools for accuracy and integration

**Tools to Research:**

#### **A. BLE Laser Meters**
**Options:**
- Leica DISTO D2 ($200-300)
- Bosch GLM 50 C ($100-150)
- Leica DISTO D510 ($400-500, outdoor)

**Research:**
- [ ] Bluetooth API availability
- [ ] Measurement accuracy (±1/16" or better)
- [ ] Battery life
- [ ] Price point
- [ ] Integration difficulty

**Questions:**
- Can we read measurements via Bluetooth?
- What's the API/SDK situation?
- Real-time vs batch transfer?

---

#### **B. RoomPlan (iOS LiDAR)**
**What:** Apple's native room scanning API

**Research:**
- [ ] Accuracy vs manual (±1-2%)
- [ ] Export formats (JSON, USDZ)
- [ ] Parametric data available (walls, doors, windows)
- [ ] Integration with web app
- [ ] Limitations (iOS only, LiDAR devices only)

**Test:**
- [ ] Scan a room with RoomPlan
- [ ] Export JSON
- [ ] Parse data structure
- [ ] Compare to manual measurements

---

#### **C. Magicplan**
**What:** Existing measurement app with export

**Research:**
- [ ] Export formats (CSV, XLS, PDF)
- [ ] Data structure
- [ ] Pricing ($10/month)
- [ ] Integration feasibility
- [ ] User base (do contractors already use it?)

**Test:**
- [ ] Download Magicplan app
- [ ] Create test floor plan
- [ ] Export data
- [ ] Parse CSV/XLS

---

#### **D. Bluebeam Revu**
**What:** PDF markup tool used by contractors

**Research:**
- [ ] Markups Summary export (CSV)
- [ ] Data structure
- [ ] Pricing ($349/year)
- [ ] Integration feasibility
- [ ] User base (common in construction?)

---

#### **E. Polycam (Optional)**
**What:** 3D scanning app

**Research:**
- [ ] Mesh/point cloud quality
- [ ] Export formats (OBJ, GLTF, USDZ)
- [ ] Use case (QA overlays for weird geometry)
- [ ] Pricing
- [ ] Integration difficulty

---

**Deliverable:**
- Comparison matrix (accuracy, cost, integration)
- Recommended stack for Phase 1
- Test data from each tool

**Timeline:** 1 week

---

### **3. Get Rate Book Data from Bill & Lisa** 📊

**What:** Collect their pricing data to build rate book

#### **A. Lisa's Excel Rate Book**

**Request:**
- [ ] Contact Lisa
- [ ] Request her current rate book (Excel)
- [ ] Ask for:
  - Labor rates by scope (tile, paint, countertop, etc.)
  - Material costs
  - Waste factors she uses
  - Markup percentages
  - Regional adjustments (if any)

**Expected Format:**
```
Scope               | Labor $/unit | Material $/unit | Unit  | Waste %
--------------------|--------------|-----------------|-------|--------
Tile Floor (Basic)  | $5.25        | $3.50           | sqft  | 10%
Tile Floor (Diag)   | $6.25        | $3.50           | sqft  | 13%
Tile Floor (Herring)| $7.50        | $4.25           | sqft  | 15%
Countertop (Quartz) | $45.00       | $20.00          | sqft  | 5%
Paint (Walls)       | $2.00        | $0.50           | sqft  | 0%
```

**Save to:** `8825_core/explorations/features/contractor_bid_tool_test_data/rate_books/lisa_rate_book.xlsx`

---

#### **B. Large Batch of Bids**

**Request:**
- [ ] Contact Bill & Lisa
- [ ] Request 10-20 past bids (PDF or Word)
- [ ] Ask for variety:
  - Residential (kitchens, baths)
  - Commercial (offices, retail)
  - Different scopes (tile, paint, countertops)
  - Won and lost bids
  - With and without change orders

**What to Extract:**
- Bid formats (how they structure bids)
- Line item descriptions
- Pricing patterns
- Terms and conditions
- Exclusions
- Common scopes

**Save to:** `8825_core/explorations/features/contractor_bid_tool_test_data/sample_bids/`

**Analysis:**
- [ ] Parse common line items
- [ ] Identify pricing patterns
- [ ] Extract waste factors used
- [ ] Note bid format preferences
- [ ] Document terms/exclusions

---

**Deliverable:**
- Lisa's rate book (Excel)
- 10-20 sample bids (PDF)
- Analysis document (patterns, formats)
- Normalized rate book (JSON)

**Timeline:** 1 week (depends on Bill/Lisa availability)

---

## 📊 DATA COLLECTION SUMMARY

### **Folder Structure:**
```
8825_core/explorations/features/contractor_bid_tool_test_data/
├── cubicasa/
│   ├── test_property.svg
│   ├── test_property.pdf
│   └── test_property.png
├── measurements/
│   ├── ble_laser_tests/
│   ├── roomplan_tests/
│   ├── magicplan_tests/
│   └── comparison_matrix.md
├── rate_books/
│   ├── lisa_rate_book.xlsx
│   └── normalized_rate_book.json
└── sample_bids/
    ├── bid_001_kitchen.pdf
    ├── bid_002_bath.pdf
    ├── bid_003_commercial.pdf
    └── analysis.md
```

---

## 🎯 NEXT STEPS (After Data Collection)

### **Phase 0: MVP (2 weeks)**

**Prerequisites (Must Complete First):**
- ✅ CubiCasa test plan received
- ✅ Measurement tools researched
- ✅ Lisa's rate book received
- ✅ Sample bids received and analyzed

**Then Build:**
1. Manual measurement entry
2. Scope selection (from Lisa's rate book)
3. Quantity calculator (with waste factors)
4. Rate application (Lisa's rates)
5. PDF bid generator (based on sample bid formats)

**Test With:**
- CubiCasa test property
- Lisa's actual rates
- Generate 3 test bids
- Compare to Bill/Lisa's actual bids

---

## 📋 IMMEDIATE ACTIONS (This Week)

### **Monday-Tuesday:**
- [ ] Order CubiCasa test plan
- [ ] Email Lisa for rate book
- [ ] Email Bill for sample bids

### **Wednesday-Friday:**
- [ ] Research BLE laser meters
- [ ] Test RoomPlan (if iPhone with LiDAR)
- [ ] Download/test Magicplan
- [ ] Create comparison matrix

### **Next Week:**
- [ ] Receive CubiCasa plan
- [ ] Receive Lisa's rate book
- [ ] Receive sample bids
- [ ] Analyze and normalize data
- [ ] Decision: Build Phase 0 or wait?

---

## 🎓 RESEARCH QUESTIONS

### **CubiCasa:**
- [ ] What file formats do they provide?
- [ ] How accurate are measurements?
- [ ] Can we parse SVG geometry?
- [ ] What's the scale/calibration?

### **BLE Laser:**
- [ ] Which model has best API?
- [ ] Can we auto-transfer measurements?
- [ ] Real-time vs batch?
- [ ] Battery life for full-day use?

### **RoomPlan:**
- [ ] Accuracy for construction use?
- [ ] What data is in JSON export?
- [ ] Can we extract wall lengths, openings?
- [ ] Limitations (room size, lighting)?

### **Rate Book:**
- [ ] How does Lisa organize rates?
- [ ] What waste factors does she use?
- [ ] How does she handle complexity?
- [ ] What's her markup strategy?

### **Bid Format:**
- [ ] What's Bill/Lisa's preferred format?
- [ ] How detailed are line items?
- [ ] What terms/exclusions are standard?
- [ ] How do they handle change orders?

---

## 📊 SUCCESS CRITERIA

**Data Collection Complete When:**
- ✅ CubiCasa test plan in hand
- ✅ Measurement tools researched + comparison matrix
- ✅ Lisa's rate book received and normalized
- ✅ 10+ sample bids received and analyzed
- ✅ Test data folder populated
- ✅ Ready to build Phase 0 MVP

**Then:**
- Promote from Exploration to PoC
- Start Phase 0 build (2 weeks)
- Test with real data
- Get Bill/Lisa feedback

---

## 🎯 CONTACTS

**Lisa:**
- Request: Rate book (Excel)
- Timeline: ASAP
- Follow-up: If not received in 3 days

**Bill:**
- Request: 10-20 sample bids (PDF)
- Timeline: ASAP
- Follow-up: If not received in 3 days

**CubiCasa:**
- Order: Test floor plan
- Cost: $10-30
- Timeline: 24hr turnaround

---

## 📝 NOTES

**Why This Order:**
1. CubiCasa first (longest lead time: 24hr)
2. Measurement research (can do while waiting)
3. Rate book + bids (depends on Bill/Lisa availability)
4. Build Phase 0 (after all data collected)

**Risk Mitigation:**
- If CubiCasa delayed: Use manual measurements for testing
- If Lisa's rate book delayed: Use industry averages from research
- If sample bids delayed: Create synthetic bids based on research

**Decision Point:**
- After data collection: Build now or wait?
- If build: Start Phase 0 MVP
- If wait: Keep in exploration, refine design

---

**Status:** Pre-Build (Data Collection Phase)  
**Next Review:** After data collection complete  
**Estimated Timeline:** 2 weeks to collect data, then decide on build
