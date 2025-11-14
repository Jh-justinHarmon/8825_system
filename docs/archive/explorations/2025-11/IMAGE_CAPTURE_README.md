# 🎨 Joju Image Capture System

Automated screenshot capture and image management for Joju profiles.

## Features

✅ **Automated Screenshot Capture**
- Capture from any URL (portfolio sites, live projects)
- Multiple viewport sizes (desktop, tablet, mobile)
- Full-page or viewport screenshots

✅ **Figma API Integration**
- Export frames/artboards directly from Figma
- Automatic image download and processing
- Supports node-specific exports

✅ **Image Management**
- Auto-scan existing images in `/content/media/`
- Generate proper attachment JSON with dimensions
- Organized file naming conventions

✅ **Hybrid Workflow**
- Phase 1: Automated capture
- Phase 2: Manual review/editing
- Phase 3: Auto-update JSON

---

## Installation

### 1. Install Python Dependencies

```bash
cd joju_sandbox
pip install -r requirements_images.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

---

## Usage

### Quick Start: Capture All Project Images

```bash
python joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --portfolio-url https://favorite-day-425385.framer.app/
```

### With Figma Integration

```bash
python joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --figma-token YOUR_FIGMA_TOKEN \
  --portfolio-url https://favorite-day-425385.framer.app/
```

### Scan Existing Images Only

```bash
python joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --scan-only
```

---

## Getting Your Figma Token

1. Go to https://www.figma.com/settings
2. Scroll to "Personal access tokens"
3. Click "Create new token"
4. Give it a name (e.g., "Joju Image Export")
5. Copy the token (save it securely!)

**Permissions needed:** File content (read-only)

---

## Workflow

### Phase 1: Automated Capture

```bash
# Run the capture script
python joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --figma-token YOUR_TOKEN
```

**What it does:**
- Reads all projects from your `joju_upload_ready.json`
- For each project with a URL:
  - If Figma URL → exports via API
  - If web URL → captures screenshot
- Saves images to `content/media/`
- Updates JSON with attachment entries

### Phase 2: Manual Review

```bash
# Open the media folder
open content/media/
```

**Review and edit:**
- Delete unwanted screenshots
- Add custom images (CAD renders, photos, etc.)
- Crop/edit images in your preferred tool
- Rename files if needed (keep format: `project-id-description.png`)

### Phase 3: Auto-Update JSON

```bash
# Scan folder and update JSON
python joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --scan-only
```

**What it does:**
- Scans `content/media/` folder
- Gets dimensions for all images
- Generates attachment entries
- Updates your JSON file

---

## File Naming Convention

**Format:** `{project-id}-{description}.png`

**Examples:**
```
trustybits-hero.png
trustybits-dashboard.png
trustybits-mobile.png
joju-homepage-desktop.png
joju-homepage-mobile.png
teams-ux-research-findings.png
```

---

## Manual Image Addition

### 1. Add Images to Folder

```bash
# Copy your images to media folder
cp ~/Desktop/my-project-image.png content/media/project-id-hero.png
```

### 2. Update JSON Manually (Optional)

Or let the script scan and auto-generate:

```bash
python joju_image_capture.py --config output/joju_upload_ready.json --scan-only
```

---

## Advanced Usage

### Capture Specific Project

```python
from joju_image_capture import JojuImageCapture

capturer = JojuImageCapture('output/joju_upload_ready.json')

# Capture single project
attachment = capturer.capture_screenshot(
    url='https://favorite-day-425385.framer.app/',
    output_name='portfolio-hero',
    viewport={'width': 1920, 'height': 1080}
)

# Update project
capturer.update_project_attachments('project-id', [attachment])
capturer.save_profile()
```

### Multiple Viewports

```python
# Capture desktop, tablet, mobile
attachments = capturer.capture_multiple_viewports(
    url='https://favorite-day-425385.framer.app/',
    base_name='portfolio-hero'
)
# Creates: portfolio-hero-desktop.png, portfolio-hero-tablet.png, portfolio-hero-mobile.png
```

### Export from Figma

```python
attachment = capturer.export_from_figma(
    figma_url='https://www.figma.com/file/ABC123/Project?node-id=1:2',
    output_name='figma-design',
    figma_token='YOUR_TOKEN'
)
```

---

## Troubleshooting

### Playwright Installation Issues

```bash
# Reinstall Playwright browsers
playwright install --force chromium
```

### Figma API Errors

**401 Unauthorized:**
- Check your token is valid
- Ensure token has file content read permissions

**404 Not Found:**
- Verify Figma URL format
- Check file is accessible with your account

### Image Quality

**Screenshots too small:**
- Increase viewport size in script
- Use `scale: 2` for retina displays

**Figma exports low quality:**
- Increase scale parameter (2x or 3x)
- Export specific frames instead of full file

---

## Next Steps

1. **Run initial capture** to get all project images
2. **Review and curate** in `content/media/`
3. **Add custom images** (CAD, photos, etc.)
4. **Re-scan** to update JSON
5. **Upload to Joju** with complete image attachments

---

## Tips

✅ **Use descriptive filenames** - Makes manual curation easier  
✅ **Keep originals** - Save high-res versions separately  
✅ **Optimize file sizes** - Use PNG for screenshots, JPG for photos  
✅ **Test on mobile** - Capture mobile viewports for responsive projects  
✅ **Update regularly** - Re-run when projects change  

---

## File Structure

```
joju_sandbox/
├── joju_image_capture.py       # Main script
├── requirements_images.txt      # Python dependencies
├── IMAGE_CAPTURE_README.md      # This file
├── output/
│   └── joju_upload_ready.json  # Your profile data
└── content/
    └── media/                   # Image storage
        ├── trustybits-hero.png
        ├── joju-homepage.png
        └── teams-ux-findings.png
```

---

**Ready to capture images!** 📸
