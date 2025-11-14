# 8825 Sticky Importer - Figma Plugin

Import OCR'd sticky notes from photos directly into FigJam!

---

## Installation (2 minutes)

### Step 1: Open Figma Desktop App
**Important:** Plugins only work in the desktop app, not the browser.

Download: https://www.figma.com/downloads/

### Step 2: Import Plugin

1. Open Figma Desktop App
2. Go to **Menu → Plugins → Development → Import plugin from manifest**
3. Navigate to this folder:
   ```
   8825_core/integrations/figjam/figma-plugin/
   ```
4. Select `manifest.json`
5. Click "Open"

**Plugin is now installed!** ✅

---

## Usage

### Step 1: Process Your Sticky Photo

```bash
cd 8825_core/integrations/figjam
python3 vision_sticky_processor.py
```

**Output:** `~/Downloads/sticky_notes_vision.json`

### Step 2: Open FigJam Board

Open your FigJam board where you want the stickies

### Step 3: Run Plugin

1. Right-click on canvas
2. **Plugins → Development → 8825 Sticky Importer**
3. Copy the contents of `sticky_notes_vision.json`
4. Paste into the plugin window
5. Click **"Import Stickies"**

**Done!** Your handwritten stickies are now digital! 📋✨

---

## What It Does

**Automatically creates:**
- ✅ Sticky notes with OCR'd text
- ✅ Correct colors (yellow, pink, blue, etc.)
- ✅ Preserved layout (relative positions)
- ✅ Proper sizing

**Example:**
```
Photo with 3 stickies
    ↓
OCR processing
    ↓
JSON data
    ↓
Plugin import
    ↓
3 digital stickies in FigJam!
```

---

## Complete Workflow

### 1. Take Photo
- Photo of whiteboard/wall with sticky notes
- Save to Downloads with "sticky" in filename

### 2. Process
```bash
python3 vision_sticky_processor.py
```

### 3. Import
- Open FigJam
- Run plugin
- Paste JSON
- Click Import

### 4. Done!
- Digital stickies created
- Edit, move, organize as needed

---

## Troubleshooting

### "Plugin not showing up"
- Make sure you're using Figma **Desktop App** (not browser)
- Restart Figma after importing plugin

### "Import failed"
- Check JSON is valid (copy entire file contents)
- Make sure you're in a FigJam board (not Figma design file)

### "Colors wrong"
- Color detection is approximate
- Manually adjust colors after import if needed

### "Positions off"
- Adjust `scale` variable in `code.js` line 47
- Default is 0.5, try 0.3 or 0.7

---

## Files

```
figma-plugin/
├── manifest.json    # Plugin metadata
├── code.js         # Main plugin logic
├── ui.html         # User interface
└── README.md       # This file
```

---

## Updating Plugin

After making changes:
1. **Menu → Plugins → Development → Reload plugin**
2. Or restart Figma

---

## Publishing (Optional)

To share with others:
1. Go to **Menu → Plugins → Development → Publish plugin**
2. Follow Figma's publishing process
3. Plugin becomes available in Community

---

## Summary

**Status:** ✅ Ready to use  
**Install time:** 2 minutes  
**Works with:** FigJam boards  
**Requires:** Figma Desktop App  

**Transform photos of sticky notes into digital FigJam boards!** 📸→📋✨
