# Google Vision API Setup

## Enable Vision API

**Click this link:**
```
https://console.developers.google.com/apis/api/vision.googleapis.com/overview?project=400905002666
```

**Then click "Enable"**

---

## Test It

```bash
cd 8825_core/integrations/figjam
python3 vision_sticky_processor.py
```

**Should process all sticky images in Downloads with superior OCR!**

---

## Cost

**Pricing:** $1.50 per 1,000 images  
**Your usage:** ~$0.0015 per image  
**Free tier:** 1,000 images/month free

**For your use case:** Essentially free (unless you process 1000+ stickies/month)

---

## What's Better

**Tesseract (free):**
- ❌ Poor handwriting recognition
- ❌ Needs perfect conditions

**Google Vision:**
- ✅ Excellent handwriting OCR
- ✅ Works in varied lighting
- ✅ Handles complex backgrounds
- ✅ 99%+ accuracy

---

## Ready!

Once you enable the API, run:
```bash
python3 vision_sticky_processor.py
```

And watch it perfectly OCR your handwritten stickies! 📸✨
