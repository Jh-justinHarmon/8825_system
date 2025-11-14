# Sticky Notes → FigJam Pipeline

**Status:** ✅ Ready to test  
**Created:** 2025-11-09

---

## What It Does

Converts physical sticky notes from photos into digital FigJam sticky notes:

1. **Photo** → Take picture of whiteboard/wall with sticky notes
2. **OCR** → Detect and read each sticky note
3. **Process** → Extract text, color, position
4. **FigJam** → Create digital stickies in same layout

---

## Setup

### 1. Install Dependencies

```bash
cd 8825_core/integrations/figjam
pip3 install -r requirements.txt
```

**System dependencies (macOS):**
```bash
brew install tesseract  # OCR engine
```

### 2. Get Figma Access Token

1. Go to https://www.figma.com/settings
2. Scroll to "Personal access tokens"
3. Click "Generate new token"
4. Copy the token

**Set environment variable:**
```bash
export FIGMA_ACCESS_TOKEN=your_token_here
# Add to ~/.zshrc to persist
echo 'export FIGMA_ACCESS_TOKEN=your_token' >> ~/.zshrc
```

---

## Usage

### Step 1: Process Photo

**Take a photo of your sticky notes:**
- Name it with "sticky" or "whiteboard" in filename
- Save to `~/Downloads/`

**Run processor:**
```bash
cd 8825_core/integrations/figjam
python3 sticky_processor.py
```

**Output:**
- `sticky_notes_processed.json` - Structured data
- `*_debug.png` - Image with detected stickies highlighted

---

### Step 2: Upload to FigJam

**Create a FigJam file:**
1. Go to Figma
2. Create new FigJam board
3. Copy file key from URL: `https://www.figma.com/file/FILE_KEY/...`

**Upload stickies:**
```bash
python3 figjam_api.py YOUR_FILE_KEY
```

---

## Via MCP Bridge (Goose/Claude)

```
> "Process sticky notes from latest photo"
> "Upload stickies to FigJam"
```

---

## Features

### Sticky Detection
- ✅ Automatic region detection
- ✅ Color recognition (yellow, pink, blue, green, orange, purple)
- ✅ OCR text extraction
- ✅ Confidence scoring

### Layout Preservation
- ✅ Maintains spatial relationships
- ✅ Clusters nearby stickies
- ✅ Preserves relative positions

### FigJam Integration
- ✅ Creates digital stickies
- ✅ Matches colors
- ✅ Preserves layout
- ✅ Scales appropriately

---

## Example Workflow

### Physical Board
```
[Photo of whiteboard with 12 sticky notes in 3 groups]
```

### Process
```bash
python3 sticky_processor.py
```

**Output:**
```
Processing: whiteboard_meeting.jpg
  Found 12 sticky notes
  Organized into 3 clusters

Results saved to: sticky_notes_processed.json
```

### Upload
```bash
python3 figjam_api.py abc123def456
```

**Result:**
```
Uploading 12 stickies to FigJam...
✓ Upload complete!
```

### FigJam Board
Digital stickies in same layout as photo! 📋✨

---

## Configuration

### Adjust Detection Sensitivity

Edit `sticky_processor.py`:

```python
# Minimum sticky size (% of image)
if area < img_area * 0.01:  # Change 0.01 to adjust

# Aspect ratio tolerance
if aspect_ratio < 0.5 or aspect_ratio > 2.0:  # Adjust range
```

### Color Mapping

Edit `STICKY_COLORS` dict to add custom colors:

```python
STICKY_COLORS = {
    'yellow': (255, 255, 153),
    'custom_red': (255, 100, 100),  # Add your color
}
```

---

## Troubleshooting

### "No sticky notes found"
- Check image quality (good lighting, clear photo)
- Adjust detection sensitivity
- Try naming file with "sticky" or "whiteboard"

### "OCR not working"
```bash
brew install tesseract
pip3 install pytesseract
```

### "FigJam upload failed"
- Check access token is set
- Verify file key is correct
- Ensure you have edit access to FigJam file

### "Colors not detected correctly"
- Adjust `STICKY_COLORS` RGB values
- Check lighting in photo
- Try with higher resolution image

---

## Advanced Features

### Batch Processing

Process multiple photos:
```bash
for img in ~/Downloads/sticky*.jpg; do
    python3 sticky_processor.py "$img"
done
```

### Custom Clustering

Adjust cluster distance in `sticky_processor.py`:
```python
if dist < 300:  # Change 300 to adjust grouping
```

### Export Formats

Processed data is JSON - can export to:
- FigJam (implemented)
- Miro (add miro_api.py)
- Notion (add notion_api.py)
- CSV/Excel (add export_csv.py)

---

## Integration with 8825

### Auto-Process from Downloads

Add to inbox pipeline:
```bash
# In simple_sync_and_process.sh
python3 8825_core/integrations/figjam/sticky_processor.py
```

### MCP Bridge Tool

Already added as `process_stickies`:
```
> "Process stickies"
```

### Automatic Upload

Set default FigJam file:
```bash
export FIGJAM_DEFAULT_FILE=your_file_key
```

---

## Files

```
8825_core/integrations/figjam/
├── README.md              # This file
├── sticky_processor.py    # OCR and detection
├── figjam_api.py         # FigJam API client
└── requirements.txt       # Dependencies
```

---

## Future Enhancements

### Phase 2
- [ ] Handwriting recognition (better OCR)
- [ ] Arrow/connection detection
- [ ] Auto-categorization by content
- [ ] Priority/tag detection
- [ ] Action item extraction

### Phase 3
- [ ] Real-time processing (watch folder)
- [ ] Mobile app integration
- [ ] Multi-board support
- [ ] Version control (track changes)
- [ ] Collaboration features

---

## Credits

**Design patterns from:** Figma prototyping notes (T-8825-20251109-013718)
- Component variants
- State management
- Semantic naming
- Layout preservation

---

## Summary

**Status:** ✅ Ready to use  
**Dependencies:** tesseract, opencv, PIL  
**API:** Figma access token required  
**MCP:** Integrated  

**Transform your physical sticky notes into digital FigJam boards!** 📸→📋✨
