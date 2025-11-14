# Input Hub Plan - Calibrated Analysis

## Time Estimates (CALIBRATED)

Using calibration factor: **0.57x for complex tasks, 0.56x for medium tasks**

### Option A: Minimal Viable
**Original Estimate:** 2 hours  
**Calibrated:** ~68 minutes (1.1 hours)

- Create folder structure: 5m (simple, 0.53x) = **3m**
- Manual screenshot workflow: 15m (medium, 0.56x) = **8m**
- Implement "checking sg" command: 30m (complex, 0.57x) = **17m**
- Test with one screenshot: 10m (medium, 0.56x) = **6m**
- Documentation: 20m (medium, 0.56x) = **11m**

**Total: ~45 minutes** (not 2 hours)

### Option B: Semi-Automated
**Original Estimate:** 1 day  
**Calibrated:** ~3.5 hours

- Folder structure: 5m = **3m**
- rsync script + cron: 45m (complex, 0.57x) = **26m**
- Sidecar generation: 30m (complex, 0.57x) = **17m**
- Basic routing: 45m (complex, 0.57x) = **26m**
- Commands ("checking sg" + "estimate"): 60m (complex, 0.57x) = **34m**
- Testing + debugging: 60m (medium, 0.56x) = **34m**
- Documentation: 30m (medium, 0.56x) = **17m**

**Total: ~2.5 hours** (not 8 hours)

### Option C: Full System
**Original Estimate:** 1 week  
**Calibrated:** ~1-2 days

- Everything in Option B: **2.5 hours**
- Watchdog auto-mirror: 90m (complex, 0.57x) = **51m**
- OCR integration: 120m (complex, 0.57x) = **68m**
- Time estimator with learning: 120m (complex, 0.57x) = **68m**
- Integration with focus protocols: 90m (complex, 0.57x) = **51m**
- Testing full system: 120m (medium, 0.56x) = **67m**
- Documentation: 60m (medium, 0.56x) = **34m**

**Total: ~6.5 hours** (not 40 hours)

---

## Critical Assessment

### ✅ Excellent Design Elements

1. **Non-Destructive** - Desktop/Downloads untouched
2. **User-Scoped** - Perfect for v3.0 multi-user
3. **Sidecar Metadata** - SHA256 + provenance + OCR
4. **Alias System** - "checking sg" UX is clean

### ⚠️ Concerns

#### 1. **Complexity vs Value**
- **Issue:** Building full automation for screenshots
- **Question:** How often do you actually take screenshots for 8825?
- **Risk:** Over-engineering a low-frequency workflow

#### 2. **Overlap with Existing Inbox**
- **Already have:** `8825_inbox` system (just built)
- **Already works:** ChatGPT → MCP → inbox → AI sweep
- **Question:** Why separate screenshot system vs extending inbox?

#### 3. **OCR Necessity**
- **Issue:** OCR is slow and error-prone
- **Alternative:** Window title + file metadata (instant)
- **Question:** What info do you need from screenshot content?

#### 4. **Time Estimator Scope Creep**
- **Issue:** Building ML classifier for routing
- **Already have:** Classification system in inbox
- **Question:** Can we reuse existing classifier?

---

## Alternative: Extend Existing Inbox

### Simpler Approach

**Add screenshot support to existing `8825_inbox` system:**

```
8825_inbox/
├── pending/
│   ├── screenshots/     # NEW
│   └── json/
├── processing/
└── completed/
```

**Benefits:**
- Reuse existing validator, classifier, router
- Reuse Lane A/B logic
- Reuse teaching tickets
- One system, not two

**Add to inbox:**
- Screenshot handler (extract metadata)
- Image → JSON converter
- "checking sg" command

**Time:** ~1 hour (calibrated)

---

## Recommended Approach

### Phase 0: Validate Need (15 minutes)

**Questions to answer first:**

1. **Frequency:** How many screenshots/week do you take for 8825?
   - If <5/week → Manual is fine
   - If >20/week → Automation worth it

2. **Content:** What info do you need from screenshots?
   - Window title? (instant)
   - Text content? (OCR needed)
   - Just visual reference? (no processing needed)

3. **Workflow:** What happens after screenshot?
   - Goes to specific project?
   - Needs AI analysis?
   - Just archived?

4. **Integration:** Should this be:
   - Separate system (Input Hub)
   - Extension of inbox
   - Part of focus protocols

### Phase 1: Minimal Test (30 minutes)

**If automation is worth it:**

1. Create `8825_inbox/pending/screenshots/`
2. Add screenshot handler to inbox validator
3. Test with 3 screenshots
4. See if existing classifier works

**If it works → extend inbox**  
**If it doesn't → build Input Hub**

---

## My Recommendation

### Start with Questions, Not Code

**Before building anything:**

1. **Track manually for 1 week:**
   - How many screenshots?
   - What do you do with them?
   - What info do you need extracted?

2. **Then decide:**
   - Extend inbox (if fits existing pattern)
   - Build Input Hub (if fundamentally different)
   - Do nothing (if frequency is low)

**Why:**
- Avoid building unused automation
- Real data > theoretical design
- Can always automate later

---

## If You Want to Build Now

### Option A-Lite: Test Integration (30 min calibrated)

**Extend existing inbox to handle screenshots:**

1. Add screenshot folder (2m)
2. Add image metadata extractor (15m)
3. Test classification (8m)
4. Document (5m)

**Total: 30 minutes**

**Validates:**
- Does existing system work for screenshots?
- Do we need separate Input Hub?
- What's actually needed?

---

## Questions for You

1. **How many screenshots/week** do you take for 8825 work?
2. **What do you need** from screenshot content?
3. **Should this extend inbox** or be separate?
4. **Want to test** with existing inbox first?

**My vote:** Test with inbox extension first (30m), then decide if Input Hub is needed.
