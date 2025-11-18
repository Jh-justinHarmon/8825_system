# Phase 0: Technology Validation Tests

These tests validate that OCR and image comparison work reliably enough to build the Tutorial System on top of.

## What You Need

1. **Test Screenshots** - Take 2-3 screenshots of Rive (or any app):
   - Screenshot 1: Initial state (e.g., Design mode)
   - Screenshot 2: After a UI change (e.g., switched to Animate mode, Timeline panel visible)
   - Screenshot 3: Same as Screenshot 2 (to test identical image detection)

2. **Save them to:** `tutorials/test_screenshots/`
   - Example names: `rive_design_mode.png`, `rive_animate_mode.png`, `rive_animate_mode_copy.png`

## Running the Tests

### Test 1: OCR Validation

**What it tests:** Can we extract text from UI screenshots accurately?

```bash
cd tutorials/phase0_tests
python3 test_ocr.py ../test_screenshots/rive_design_mode.png
```

**What to look for:**
- ✓ Extracts visible button/menu text (e.g., "Animate", "Design", "Timeline")
- ✓ Provides coordinates for each text region
- ✓ Completes in <2 seconds
- ✗ Misses obvious text or hallucinates text that isn't there

**Pass criteria:**
- Finds at least 80% of visible text
- No major hallucinations
- Processing time <2s

---

### Test 2: Image Comparison Validation

**What it tests:** Can we detect when UI state has changed?

```bash
# Test A: Compare identical images (should be >95% similar)
python3 test_image_compare.py ../test_screenshots/rive_animate_mode.png ../test_screenshots/rive_animate_mode_copy.png

# Test B: Compare different states (should be <80% similar)
python3 test_image_compare.py ../test_screenshots/rive_design_mode.png ../test_screenshots/rive_animate_mode.png
```

**What to look for:**

**Test A (identical):**
- ✓ Similarity >95%
- ✓ Category: "IDENTICAL"

**Test B (different states):**
- ✓ Similarity <80%
- ✓ Category: "DIFFERENT" or "VERY DIFFERENT"
- ✓ Detects difference regions

**Pass criteria:**
- Test A: >95% similarity
- Test B: <80% similarity (proves we can detect UI changes)
- Both complete in <2 seconds

---

## What Happens Next?

### If Both Tests Pass ✓

**We proceed to Phase 1:** Building the Tutorial Hub MCP.

The tests prove:
- OCR is accurate enough to extract UI text
- Image comparison can reliably detect when a user has completed a step
- Performance is acceptable (<2s per validation)

### If OCR Test Fails ✗

**Possible issues:**
1. **Low accuracy (<80%)** → Try Google Vision API instead (requires API key)
2. **Slow (>2s)** → Optimize by downscaling images before OCR
3. **Hallucinations** → Add confidence threshold filtering (already in script)

**Decision:** Adjust approach or pivot to Google Vision API.

### If Image Comparison Test Fails ✗

**Possible issues:**
1. **Can't distinguish identical from different** → Adjust SSIM threshold
2. **Too sensitive (minor changes = different)** → Lower threshold from 80% to 70%
3. **Slow (>2s)** → Downscale images before comparison

**Decision:** Tune thresholds or add preprocessing.

---

## Understanding the Results

### OCR Output Example

```
EXTRACTED TEXT:
------------------------------------------------------------
Animate
Design
Timeline
Duration
Playback Speed
------------------------------------------------------------

TOP 10 TEXT REGIONS (with coordinates):
------------------------------------------------------------
 1. 'Animate' @ (1420, 60) [confidence: 96%]
 2. 'Design' @ (1320, 60) [confidence: 94%]
 3. 'Timeline' @ (40, 580) [confidence: 92%]
...
------------------------------------------------------------
```

**What this tells us:**
- The word "Animate" is at coordinates (1420, 60) on screen
- OCR is 96% confident it's correct
- We can use this to validate if a user's screenshot shows "Animate" in the right place

### Image Comparison Output Example

```
SIMILARITY ANALYSIS:
------------------------------------------------------------
SSIM Score: 0.7234 (72.3%)
Category: DIFFERENT
Interpretation: Significant changes (possibly different state)
Difference regions: 3 significant areas
------------------------------------------------------------
```

**What this tells us:**
- Images are 72% similar (below 80% threshold)
- System correctly identifies this as a "different state"
- 3 regions changed (e.g., new panel appeared, button changed color)
- This is exactly what we want: detecting when a tutorial step changes the UI

---

## Quick Start (Copy-Paste Commands)

```bash
# 1. Take screenshots and save to test_screenshots/
# (Do this manually in Rive or any app)

# 2. Run OCR test
cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/8825-system/tutorials/phase0_tests
python3 test_ocr.py ../test_screenshots/YOUR_SCREENSHOT.png

# 3. Run image comparison test (identical images)
python3 test_image_compare.py ../test_screenshots/IMAGE1.png ../test_screenshots/IMAGE1_COPY.png

# 4. Run image comparison test (different states)
python3 test_image_compare.py ../test_screenshots/BEFORE.png ../test_screenshots/AFTER.png
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytesseract'"
```bash
pip3 install pytesseract opencv-python pillow scikit-image
```

### "tesseract is not installed"
```bash
brew install tesseract
```

### "Could not load image"
- Check file path is correct
- Make sure image is PNG or JPG
- Try opening the image in Preview to verify it's not corrupted

### OCR returns empty results
- Image might be too low resolution
- Try a screenshot with more visible text
- Check if image is mostly graphics (OCR needs text)

---

## Next Steps After Phase 0

Once both tests pass, we'll move to **Phase 1: Tutorial Hub MCP**:
1. Build the FastAPI server
2. Implement CRUD endpoints for tutorial objects
3. Add the validation endpoint that uses these OCR/comparison functions
4. Test the full API

**Estimated time:** 2 weeks for Phase 1.

---

**Status:** Ready for testing  
**Last Updated:** 2025-11-16
