# Contractor Bid Tool - Full Scope

**Date:** 2025-11-09  
**Status:** Exploration (Ready to Build)

---

## 🎯 THE PROBLEM

**You're comparing 3 tile bids:**
- Sub A: "$5.25/sqft for 327 sqft"
- Sub B: "$310/day for 2 days"  
- Sub C: "$62/lf for edge trim"

**Can't answer:**
1. Which is cheaper?
2. What's included vs missing?
3. Is pricing fair?
4. What about waste/complexity?

**Why hard:** Different units, missing scope, hidden factors

---

## 💡 THE SOLUTION

**Bid comparison engine** that:
1. Normalizes to "bid atoms" (common units)
2. Shows included vs missing
3. Applies transparent waste/complexity
4. Compares apples-to-apples
5. Outputs in each sub's units

**Not takeoff (measuring) - This is comparison (normalizing)**

---

## 🏗️ HOW IT WORKS

### **1. Capture (Low-Friction)**
- Import CubiCasa SVG (floor plan)
- BLE laser patches (precision)
- Photo markup (issues)
- RoomPlan (weird rooms)

### **2. Normalize to "Bid Atoms"**
```javascript
{
  trade: "tile",
  qty_raw: 327.8 sqft,
  waste_pct: 0.15,        // 15% herringbone
  complexity: 1.08,       // L-shape
  site_factor: 1.05,      // upper floor
  qty_final: 382.7 sqft,  // calculated
  total: $2,870
}
```

### **3. Convert Units**
- Sub sees: "327 sqft @ $7.50"
- You see: Normalized comparison
- Toggle between views

### **4. Compare Bids**
```
Sub A: $3,034 (complete)
Sub B: $3,200 (unclear scope)
Sub C: $2,126 → $2,707 (missing 3 items)
Winner: Sub A ✅
```

### **5. Waste Calculators**
```
Herringbone: 15% waste
L-shape: 1.05x complexity
Upper floor: 1.05x site
Final: 327 × 1.15 × 1.05 × 1.05 = 414 sqft
```

---

## 🎯 USE CASES

### **1. Bid Comparison**
Compare 3 bids, flag missing scope, identify winner

### **2. Change Order Validation**
Prove what was/wasn't in scope, calculate fair price

### **3. Historical Costs**
"Is $7.50/sqft fair?" → Compare to 23 past projects

### **4. Scope Gap Detection**
Flag missing items, calculate cost to add

### **5. Material Optimizer**
Calculate exact order quantities with waste

---

## 🏗️ ARCHITECTURE

```
Capture → Measure → Normalize → Compare → Output
```

**Components:**
- Capture: CubiCasa, laser, photos
- Normalize: Bid atoms, waste factors
- Compare: Apples-to-apples, gaps
- Output: Reports, exports

---

## 🚀 BUILD PLAN

### **Phase 0: MVP (2 weeks)**
- Manual atom entry
- Simple comparison
- CSV export
- **Goal:** Prove concept

### **Phase 1: Capture (3 weeks)**
- CubiCasa import
- Photo markup
- BLE laser
- **Goal:** Low-friction input

### **Phase 2: Intelligence (3 weeks)**
- PDF extraction (AI)
- Scope gaps
- Historical database
- **Goal:** AI-assisted

### **Phase 3: Advanced (3 weeks)**
- RoomPlan
- Sub tracking
- Material optimizer
- **Goal:** Production-ready

---

## 📊 DATA MODEL

**Project:** Spaces, surfaces, runs, openings, issues  
**Bid Atom:** Normalized unit with all factors visible  
**Rate Book:** Historical pricing by trade/region  
**Sub Profile:** Performance tracking, risk scoring

---

## 💰 BUSINESS MODEL

**Target:** General contractors (primary), homeowners (secondary)  
**Pricing:** $50-100/month subscription, or $20/project  
**Market:** $220M TAM, $22M SAM (10% penetration)

---

## 🎯 COMPETITIVE ADVANTAGE

**Competitors focus on takeoff (measuring)**  
**We focus on comparison (normalizing)**

**Unique:**
- Bid comparison engine (not takeoff)
- Transparent waste/complexity
- Sub-friendly output
- Low-friction capture

---

## 📋 NEXT STEPS

**To Build:**
1. Decide: Build now or later?
2. If now: Start Phase 0 MVP
3. Test with real kitchen remodel
4. Validate bid atom model

**To Stay Exploration:**
1. Keep refining design
2. Add more use cases
3. Wait for right timing

---

**Full detailed scope in: `contractor_bid_tool_EVALUATION.md`**

**Status:** Exploration (detailed, ready when you are)
