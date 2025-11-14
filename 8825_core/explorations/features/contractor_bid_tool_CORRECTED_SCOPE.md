# Contractor Bid Tool - CORRECTED SCOPE (Bid Builder)

**Date:** 2025-11-09  
**Status:** Exploration  
**Purpose:** Build accurate bids, not compare them

---

## 🎯 THE REAL PROBLEM

**You need to create a bid for a kitchen remodel:**
- Measure the space
- Calculate materials needed
- Apply waste factors
- Price labor + materials
- Generate professional bid document

**Current process:**
- Manual measurements (tape measure, error-prone)
- Spreadsheet calculations (formulas break)
- Guessing waste factors (over/under order)
- Inconsistent bid formats
- Takes hours per bid

---

## 💡 THE SOLUTION

**Bid Builder Tool** that:
1. Captures measurements (low-friction, phone-first)
2. Calculates quantities (with transparent waste/complexity)
3. Applies your rate book (labor + materials)
4. Generates professional bid (PDF, branded)
5. Tracks what you quoted (for change orders)

**Think:** "Magicplan meets rate book meets bid generator"

---

## 🏗️ HOW IT WORKS

### **Step 1: Capture the Space**

**Option A: Quick (CubiCasa + Laser Patches)**
```
1. Get CubiCasa floor plan ($10)
2. Import SVG into app
3. Walk the space with BLE laser
4. Tap wall → laser → paste measurement
5. Mark issues with photos
Result: Accurate measurements in 15 minutes
```

**Option B: Precise (RoomPlan)**
```
1. Open app on iPhone
2. Scan room with LiDAR
3. RoomPlan generates parametric model
4. Review/adjust measurements
Result: Highly accurate, 10 minutes per room
```

**Option C: Import (If client has it)**
```
1. Import Magicplan CSV
2. Import Bluebeam Markups
3. Import existing floor plan PDF
Result: Instant, if available
```

---

### **Step 2: Define the Scope**

**Select trades/scopes:**
```
☑ Tile floor (herringbone)
☑ Tile backsplash (subway)
☑ Countertops (quartz)
☑ Paint (walls + ceiling)
☑ Base trim (wood)
☐ Electrical
☐ Plumbing
```

**For each scope, app calculates:**
- Base quantities (sqft, lf, each)
- Waste factors (pattern-based)
- Complexity adjustments (room shape, site conditions)
- Final quantities to quote

---

### **Step 3: Apply Your Rate Book**

**Your rate book (saved in app):**
```javascript
{
  "tile.floor.herringbone": {
    "labor_rate": 7.50,      // $/sqft
    "material_rate": 4.25,   // $/sqft
    "waste_default": 0.15,   // 15%
    "unit": "sqft"
  },
  "tile.edge.schluter": {
    "labor_rate": 3.50,      // $/lf
    "material_rate": 2.00,   // $/lf
    "unit": "lf"
  },
  "prep.leveling": {
    "labor_rate": 2.00,      // $/sqft
    "material_rate": 0.50,   // $/sqft
    "unit": "sqft"
  }
}
```

**App auto-calculates:**
```
Floor: 327 sqft raw
+ Waste (15%): 49 sqft
+ Complexity (L-shape, 8%): 30 sqft
= 406 sqft to quote

Labor: 406 × $7.50 = $3,045
Materials: 406 × $4.25 = $1,726
Subtotal: $4,771
```

---

### **Step 4: Build the Bid**

**Line items auto-generated:**
```
TILE WORK
─────────────────────────────────────────
Floor Tile Installation (Herringbone)
  327 sqft @ $11.75/sqft              $3,842
  (includes 15% waste, leveling prep)

Schluter Edge Trim
  62 lf @ $5.50/lf                      $341

Waterproofing Membrane
  327 sqft @ $1.25/sqft                 $409

Grout & Seal
  327 sqft @ $0.75/sqft                 $245
                                    ─────────
TILE SUBTOTAL                         $4,837

COUNTERTOPS
─────────────────────────────────────────
Quartz Countertop (3cm)
  38.5 sqft @ $65/sqft                $2,503
  (includes sink cutout, eased edge)

Backsplash (Subway Tile)
  28.5 sqft @ $18/sqft                  $513
                                    ─────────
COUNTERTOP SUBTOTAL                   $3,016

PAINT
─────────────────────────────────────────
Walls (2 coats)
  382 sqft @ $2.50/sqft                 $955

Ceiling (1 coat)
  147 sqft @ $2.00/sqft                 $294
                                    ─────────
PAINT SUBTOTAL                        $1,249

─────────────────────────────────────────
TOTAL                                 $9,102
```

**Adjustments:**
- Markup: 20% → $1,820
- **GRAND TOTAL: $10,922**

---

### **Step 5: Generate Professional Bid**

**PDF output includes:**
```
[Your Company Logo]

BID PROPOSAL

Client: John Smith
Address: 123 Main St, Austin, TX
Date: November 9, 2025
Valid: 30 days

SCOPE OF WORK
─────────────────────────────────────────
Complete kitchen remodel including:
• Tile floor installation (herringbone pattern)
• Quartz countertops with sink cutout
• Tile backsplash (subway pattern)
• Interior paint (walls + ceiling)
• Base trim installation

DETAILED BREAKDOWN
[Line items from above]

EXCLUSIONS
• Electrical work
• Plumbing modifications
• Appliance installation
• Demolition/haul-away

TERMS
• 50% deposit required
• Net 30 payment terms
• Warranty: 1 year workmanship

[Your Signature]
```

---

### **Step 6: Track What You Quoted**

**Saved in app:**
```javascript
{
  "bid_id": "bid_20251109_smith",
  "client": "John Smith",
  "address": "123 Main St",
  "date": "2025-11-09",
  "total": 10922,
  "status": "sent",
  
  "line_items": [
    {
      "scope": "tile.floor.herringbone",
      "qty_quoted": 406,
      "rate_quoted": 11.75,
      "total": 4771
    }
    // ... all items
  ],
  
  "measurements": {
    "floor_sqft": 327,
    "waste_pct": 0.15,
    "complexity": 1.08
  }
}
```

**Why track?**
- Change orders: "You quoted 327 sqft, now it's 350"
- Actual vs estimated: Learn from past bids
- Repeat clients: Pull up old rates

---

## 🎯 USE CASES

### **Use Case 1: Quick Residential Bid**

**Scenario:** Homeowner wants kitchen tile quote

**Steps:**
1. Get CubiCasa floor plan ($10, 24hr)
2. Walk space with laser (15 min)
3. Select scopes: tile floor, backsplash
4. App calculates quantities
5. Apply your rates
6. Generate PDF bid
7. Email to client

**Time:** 30 minutes (vs 2-3 hours manual)

---

### **Use Case 2: Complex Commercial Bid**

**Scenario:** Office buildout, multiple rooms

**Steps:**
1. Import architect's floor plan
2. Scan weird rooms with RoomPlan
3. Mark issues with photos
4. Select scopes per room
5. Apply commercial rates
6. Add mobilization, permits
7. Generate detailed bid

**Time:** 2 hours (vs 8-10 hours manual)

---

### **Use Case 3: Change Order**

**Scenario:** Client wants to upgrade tile pattern

**Steps:**
1. Load original bid
2. Change pattern: straight → herringbone
3. App recalculates:
   - Waste: 10% → 15%
   - Complexity: 1.0x → 1.08x
   - Labor rate: $5.25 → $7.50
4. Show difference: +$736
5. Generate change order PDF

**Time:** 5 minutes

---

### **Use Case 4: Material Order**

**Scenario:** Bid accepted, need to order materials

**Steps:**
1. Load accepted bid
2. App shows material list:
   - Tile: 406 sqft → 21 boxes (20 sqft/box)
   - Grout: 406 sqft → 3 bags (150 sqft/bag)
   - Schluter: 62 lf → 8 pieces (8 lf/piece)
3. Export to supplier
4. Order placed

**Time:** 5 minutes

---

### **Use Case 5: Historical Analysis**

**Scenario:** "Am I pricing tile too low?"

**Steps:**
1. Query all tile bids (last 12 months)
2. App shows:
   - Avg rate: $7.35/sqft
   - Range: $6.50-$9.00
   - Win rate by rate
3. Adjust rate book if needed

**Time:** 2 minutes

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│  CAPTURE LAYER                                          │
│  ─────────────                                          │
│  • CubiCasa import ($10/plan)                          │
│  • BLE laser (Leica DISTO)                             │
│  • RoomPlan (iOS LiDAR)                                │
│  • Photo markup                                         │
│  • Import (Magicplan, Bluebeam, PDF)                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  MEASUREMENT ENGINE                                     │
│  ──────────────────                                     │
│  • Calculate surfaces (floor, walls, ceiling)           │
│  • Calculate runs (countertop, trim, base)              │
│  • Detect openings (doors, windows)                     │
│  • Store measurements                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  QUANTITY CALCULATOR                                    │
│  ───────────────────                                    │
│  • Apply waste factors (pattern-based)                  │
│  • Apply complexity (room shape, site)                  │
│  • Calculate final quantities                           │
│  • Show formulas (transparent)                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  RATE BOOK ENGINE                                       │
│  ────────────────                                       │
│  • Load your rates (labor + materials)                  │
│  • Apply to quantities                                  │
│  • Calculate subtotals                                  │
│  • Add markup/overhead                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  BID GENERATOR                                          │
│  ─────────────                                          │
│  • Format line items                                    │
│  • Add company branding                                 │
│  • Include terms/exclusions                             │
│  • Generate PDF                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  TRACKING & ANALYTICS                                   │
│  ────────────────────                                   │
│  • Save bid history                                     │
│  • Track win/loss                                       │
│  • Analyze pricing                                      │
│  • Material ordering                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 DATA MODEL

### **Project:**
```javascript
{
  id: "proj_123",
  client_name: "John Smith",
  address: "123 Main St",
  type: "kitchen_remodel",
  
  // Measurements
  spaces: [
    {
      id: "kitchen",
      floor_sqft: 327,
      wall_sqft: 382,
      ceiling_sqft: 147,
      perimeter_lf: 42.5,
      // ... detailed measurements
    }
  ],
  
  // Selected scopes
  scopes: [
    "tile.floor.herringbone",
    "tile.backsplash.subway",
    "countertop.quartz",
    "paint.walls",
    "paint.ceiling"
  ]
}
```

### **Bid:**
```javascript
{
  bid_id: "bid_20251109_smith",
  project_id: "proj_123",
  date: "2025-11-09",
  valid_until: "2025-12-09",
  status: "sent",  // draft, sent, accepted, rejected
  
  line_items: [
    {
      scope: "tile.floor.herringbone",
      desc: "Floor Tile Installation (Herringbone)",
      qty_raw: 327,
      qty_final: 406,  // with waste/complexity
      unit: "sqft",
      labor_rate: 7.50,
      material_rate: 4.25,
      total: 4771
    }
  ],
  
  subtotal: 9102,
  markup_pct: 0.20,
  markup_amt: 1820,
  total: 10922,
  
  terms: {
    deposit_pct: 0.50,
    payment_terms: "Net 30",
    warranty: "1 year workmanship"
  }
}
```

### **Rate Book:**
```javascript
{
  contractor_id: "justin_harmon",
  region: "austin_tx",
  updated: "2025-11-09",
  
  rates: [
    {
      id: "tile.floor.basic",
      desc: "Basic tile floor (straight lay)",
      labor_rate: 5.25,
      material_rate: 3.50,
      unit: "sqft",
      waste_default: 0.10
    },
    {
      id: "tile.floor.herringbone",
      desc: "Tile floor (herringbone)",
      labor_rate: 7.50,
      material_rate: 4.25,
      unit: "sqft",
      waste_default: 0.15,
      complexity_factor: 1.08
    }
  ]
}
```

---

## 🚀 BUILD PLAN

### **Phase 0: MVP (2 weeks)**

**Goal:** Manual measurements → Professional bid

**Features:**
- Manual measurement entry (form)
- Select scopes from list
- Apply rates (hardcoded)
- Generate PDF bid
- Save bid history

**Tech:**
- React + TailwindCSS
- Python Flask
- SQLite
- ReportLab (PDF)

**Success:**
- Create 1 bid in <30 minutes
- PDF looks professional
- Saved for later reference

---

### **Phase 1: Capture (3 weeks)**

**Goal:** Low-friction measurement capture

**Features:**
- CubiCasa SVG import
- BLE laser integration
- Photo markup
- RoomPlan import

**Success:**
- Capture measurements in <15 minutes
- 90%+ accuracy vs manual
- Photos linked to issues

---

### **Phase 2: Intelligence (3 weeks)**

**Goal:** Smart calculations + rate book

**Features:**
- Waste factor library (pattern-based)
- Complexity calculators (room shape)
- Custom rate book (your prices)
- Material ordering lists

**Success:**
- Quantities within ±5% of actual
- Rate book saves time
- Material orders accurate

---

### **Phase 3: Advanced (3 weeks)**

**Goal:** Production-ready

**Features:**
- Change order generator
- Win/loss tracking
- Pricing analytics
- Client portal (view bids online)

**Success:**
- Change orders in <5 minutes
- Track win rate by pricing
- Clients can accept online

---

## 💰 BUSINESS MODEL

**Target:** You (general contractor) and contractors like you

**Pricing:**
- **Free:** 5 bids/month
- **Pro:** $29/month (unlimited bids)
- **Team:** $99/month (5 users, shared rate book)

**Value Prop:**
- Save 2-3 hours per bid
- More accurate quantities
- Professional presentation
- Track what you quoted

**ROI:**
- 10 bids/month × 2 hours saved = 20 hours
- 20 hours × $50/hour = $1,000/month value
- Cost: $29/month
- **ROI: 34x**

---

## 🎯 KEY DIFFERENCES

### **Bid Builder (This Tool):**
- **Purpose:** Create your bids
- **User:** You (the contractor)
- **Input:** Measurements, your rates
- **Output:** Professional bid PDF
- **Value:** Save time, look professional

### **Bid Comparison (What I thought):**
- **Purpose:** Compare others' bids
- **User:** You (the GC) or homeowner
- **Input:** Multiple bids from subs
- **Output:** Normalized comparison
- **Value:** Choose best bid

---

## 📋 NEXT STEPS

**To Build:**
1. Start Phase 0 MVP (2 weeks)
2. Test with 3 real projects
3. Refine based on feedback
4. Add capture features (Phase 1)

**To Stay Exploration:**
1. Refine use cases
2. Add more scope types
3. Design rate book structure

---

**This is a BID BUILDER, not a bid comparison tool!**

**Status:** Exploration (ready to build when you decide)
