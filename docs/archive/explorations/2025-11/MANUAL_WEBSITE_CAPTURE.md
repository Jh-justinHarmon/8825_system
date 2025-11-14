# 📸 Manual Website Screenshot Guide

Automated capture is blocked by the sites. Here's the quick manual method:

---

## Quick Method (5 minutes)

### **1. Open Sites in Browser**
- https://favorite-day-425385.framer.app/
- https://www.justin-harmon.com/
- https://www.justin-harmon.art/

### **2. Take Screenshots**

**macOS:**
```
Cmd + Shift + 4 = Select area
Cmd + Shift + 3 = Full screen
```

**Or use built-in screenshot tool:**
```
Cmd + Shift + 5 = Screenshot toolbar
```

### **3. Save to Media Folder**
Save screenshots to:
```
content/media/
```

**Naming convention:**
```
portfolio-hero.png
portfolio-projects.png
justin-harmon-com-hero.png
justin-harmon-com-work.png
art-portfolio-hero.png
art-portfolio-gallery.png
```

### **4. Run Auto-Scan**
```bash
python3 joju_image_capture.py --config output/joju_upload_ready.json --scan-only
```

This will:
- Find all images in `content/media/`
- Get dimensions automatically
- Generate attachment JSON entries

---

## Alternative: Browser DevTools Method

### **Chrome/Edge:**
1. Open site
2. Press `Cmd + Option + I` (DevTools)
3. Press `Cmd + Shift + M` (Device toolbar)
4. Click `⋮` menu → "Capture screenshot"
5. Save to `content/media/`

### **Safari:**
1. Open site
2. Develop → Show Web Inspector
3. Click camera icon in toolbar
4. Save to `content/media/`

---

## What to Capture

### **Portfolio Main (favorite-day-425385.framer.app)**
- Hero section (tagline + value props)
- Projects section
- Any project detail pages

### **Justin-Harmon.com**
- Homepage hero
- Work/portfolio section
- About section

### **Art Portfolio (justin-harmon.art)**
- Hero/landing
- Gallery view
- Featured artwork

---

## After Capturing

Run the scan to update your JSON:
```bash
cd joju_sandbox
python3 joju_image_capture.py --config output/joju_upload_ready.json --scan-only
```

This will automatically:
- ✅ Find all images
- ✅ Get dimensions
- ✅ Create attachment entries
- ✅ Update your profile JSON

---

**Estimated time:** 5-10 minutes total
