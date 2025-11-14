# 🚀 Quick Start: Joju Image Capture

## 1. Setup (One Time)

```bash
cd joju_sandbox
./setup_image_capture.sh
```

---

## 2. Get Figma Token

1. Go to: https://www.figma.com/settings
2. Scroll to "Personal access tokens"
3. Click "Create new token"
4. Name it: "Joju Image Export"
5. Copy the token

**Save it somewhere safe!** You'll need it for the next step.

---

## 3. Run Automated Capture

```bash
python3 joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --figma-token YOUR_FIGMA_TOKEN_HERE
```

**What happens:**
- ✅ Scans all projects in your Joju JSON
- ✅ Captures screenshots from web URLs
- ✅ Exports images from Figma URLs
- ✅ Saves to `content/media/`
- ✅ Updates JSON with attachments

---

## 4. Review & Curate

```bash
# Open the media folder
open content/media/
```

**Do this:**
- 🗑️ Delete screenshots you don't want
- ➕ Add custom images (CAD renders, photos, etc.)
- ✂️ Crop/edit images if needed
- 📝 Rename files: `project-id-description.png`

---

## 5. Update JSON

```bash
python3 joju_image_capture.py \
  --config output/joju_upload_ready.json \
  --scan-only
```

**What happens:**
- ✅ Scans `content/media/` folder
- ✅ Gets dimensions for all images
- ✅ Updates JSON with attachment entries

---

## 6. Done! 🎉

Your `joju_upload_ready.json` now has proper image attachments!

---

## Common Commands

### Capture everything
```bash
python3 joju_image_capture.py --config output/joju_upload_ready.json --figma-token TOKEN
```

### Just scan existing images
```bash
python3 joju_image_capture.py --config output/joju_upload_ready.json --scan-only
```

### View what images you have
```bash
ls -lh content/media/
```

---

## Troubleshooting

**"playwright: command not found"**
```bash
pip3 install playwright
playwright install chromium
```

**"Figma API error"**
- Check your token is correct
- Make sure files are accessible to your account

**"No images captured"**
- Check project URLs in your JSON
- Make sure URLs are accessible

---

## Need Help?

See full documentation: `IMAGE_CAPTURE_README.md`
