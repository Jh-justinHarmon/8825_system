# OCR Universal Protocol

**Version:** 1.1.0  
**Date:** November 17, 2025  
**Status:** Production

---

## Purpose

Defines the contract for universal OCR processing across all 8825 systems. This protocol ensures consistent OCR output structure regardless of backend (Tesseract, Google Vision, etc.) or input format (HEIC, JPEG, PNG, PDF).

---

## Tool Specification

### Tool: `ocr_file`

**Description:** Extract text from images and PDFs with document classification

**Input Schema:**
```json
{
  "file_path": "/absolute/path/to/file.jpg",
  "backend": "tesseract" | "vision"
}
```

**Output Schema:**
```json
{
  "text": "Full extracted text...",
  "normalized_mime_type": "image/jpeg",
  "pages": [
    {
      "page_number": 1,
      "width_px": 800,
      "height_px": 600,
      "text": "Page 1 text...",
      "lines": [],
      "blocks": []
    }
  ],
  "full_text": "Full extracted text...",
  "confidence": 0.85,
  "metadata": {
    "mime_type": "image/heic",
    "file_size_bytes": 123456,
    "created_at": "2025-11-17T20:00:00Z",
    "pipeline_version": "ocr_mcp_v1.1.0",
    "backend_used": "tesseract",
    "normalization_applied": true
  }
}
```

---

## Supported Formats

### Images
- **JPEG** (`.jpg`, `.jpeg`) - Native support
- **PNG** (`.png`) - Native support
- **HEIC/HEIF** (`.heic`, `.heif`) - Converted to JPEG via pillow-heif or sips

### Documents
- **PDF** (`.pdf`) - Multi-page support, converted to images per page

---

## Format Normalization

### HEIC → JPEG
1. Attempt to open with `pillow-heif` (preferred)
2. Fallback to macOS `sips` command if pillow-heif fails
3. Set `normalized_mime_type` to `image/jpeg`
4. Set `normalization_applied` to `true`

### PDF → Images
1. Convert each page to image using `pdf2image`
2. OCR each page independently
3. Combine results into `pages[]` array
4. Set `normalized_mime_type` to `application/pdf`
5. Set `normalization_applied` to `true`

---

## Output Fields

### Required Fields

#### `text` (string)
- Full extracted text from all pages
- Backward compatibility field
- Same as `full_text`

#### `normalized_mime_type` (string)
- MIME type after normalization
- Examples: `image/jpeg`, `image/png`, `application/pdf`
- HEIC files show `image/jpeg` after conversion

#### `pages[]` (array)
- One entry per page
- Each page contains:
  - `page_number` (integer) - 1-indexed
  - `width_px` (integer) - Image width in pixels
  - `height_px` (integer) - Image height in pixels
  - `text` (string) - Text from this page
  - `lines[]` (array) - Line-level data (future)
  - `blocks[]` (array) - Block-level data (future)

#### `full_text` (string)
- Complete text from all pages
- Pages joined with `\n\n`

#### `confidence` (float)
- Overall confidence score (0.0 to 1.0)
- Averaged across all pages for PDFs
- Estimated from word-level confidence for Tesseract
- From page confidence for Vision API

#### `metadata` (object)
- `mime_type` - Original MIME type before normalization
- `file_size_bytes` - File size in bytes
- `created_at` - ISO 8601 timestamp (UTC)
- `pipeline_version` - OCR engine version
- `backend_used` - `tesseract` or `vision`
- `normalization_applied` - Boolean, true if format converted

---

## Document Type Classification

### Supported Types

#### `bill`
**Indicators:**
- Keywords: "bill", "invoice", "due date", "payment due", "account number"
- Structured format with amounts and dates
- Vendor/company name at top

#### `receipt`
**Indicators:**
- Keywords: "receipt", "total", "subtotal", "tax"
- Line items with prices
- Store name and date

#### `sticky_note`
**Indicators:**
- Short text (< 100 chars)
- Minimal structure
- No formal formatting

#### `note`
**Indicators:**
- Longer text content
- Paragraphs or bullet points
- General text without specific structure

#### `document`
**Indicators:**
- Formal document structure
- Headers, sections
- Professional formatting

#### `unknown`
**Fallback when no clear indicators**

---

## Error Handling

### File Not Found
```json
{
  "error": "FileNotFoundError",
  "message": "File not found: /path/to/file.jpg"
}
```

### Unsupported Format
```json
{
  "error": "ValueError",
  "message": "Unsupported file type: .bmp. Supported: .png, .jpg, .jpeg, .heic, .heif, .pdf"
}
```

### File Too Large
```json
{
  "error": "ValueError",
  "message": "File too large: 52428800 bytes (max 50MB)"
}
```

### OCR Failure
```json
{
  "error": "RuntimeError",
  "message": "Failed to extract text: [backend error]"
}
```

---

## Backend Comparison

### Tesseract (Local)
**Pros:**
- Free, no API costs
- Works offline
- Fast for simple documents

**Cons:**
- Lower accuracy on complex layouts
- No native HEIC support (requires conversion)
- Confidence estimation approximate

**Speed:** 2-5 seconds per image

### Google Vision (Cloud)
**Pros:**
- Higher accuracy
- Better layout detection
- Native confidence scores

**Cons:**
- Requires API key
- Costs per request
- Requires internet

**Speed:** 1-2 seconds per image

---

## Usage Examples

### Basic OCR
```python
from ocr_engine import OCREngine

engine = OCREngine(backend='tesseract')
result = engine.ocr_file('/path/to/image.jpg')

print(result['full_text'])
print(f"Confidence: {result['confidence']}")
```

### HEIC File
```python
# HEIC automatically converted to JPEG
result = engine.ocr_file('/path/to/photo.heic')

assert result['normalized_mime_type'] == 'image/jpeg'
assert result['metadata']['normalization_applied'] == True
```

### Multi-Page PDF
```python
result = engine.ocr_file('/path/to/document.pdf')

for page in result['pages']:
    print(f"Page {page['page_number']}: {len(page['text'])} chars")
```

### With Classification
```python
from doc_classifier import DocumentClassifier

engine = OCREngine()
classifier = DocumentClassifier()

result = engine.ocr_file('/path/to/bill.jpg')
classification = classifier.classify(result['full_text'])

print(f"Type: {classification['doc_type_guess']}")
print(f"Confidence: {classification['confidence']}")
```

---

## Future Enhancements

### Line-Level Data
```json
{
  "lines": [
    {
      "text": "Line text",
      "bbox": {"x": 10, "y": 20, "width": 100, "height": 15},
      "confidence": 0.95
    }
  ]
}
```

### Block-Level Data
```json
{
  "blocks": [
    {
      "block_id": "block_1",
      "bbox": {"x": 10, "y": 20, "width": 200, "height": 100},
      "lines_index": [0, 1, 2]
    }
  ]
}
```

### Color Detection
For sticky notes, detect background colors to enable color-based grouping.

---

## Dependencies

### Required
- `Pillow` - Image processing
- `pytesseract` - Tesseract wrapper (for tesseract backend)
- `pillow-heif` - HEIC support

### Optional
- `google-cloud-vision` - Vision API backend
- `pdf2image` - PDF support
- `poppler` - PDF rendering (system dependency)

### System (macOS)
- `tesseract` - OCR engine (`brew install tesseract`)
- `libheif` - HEIC library (`brew install libheif`)

---

## Version History

### v1.1.0 (Nov 17, 2025)
- Added `normalized_mime_type` field
- Added `full_text` field
- Enhanced `pages[]` with dimensions and structure
- Added `lines[]` and `blocks[]` placeholders

### v1.0.0 (Nov 17, 2025)
- Initial protocol
- Basic OCR with Tesseract/Vision
- Document classification
- HEIC support

---

## See Also

- `OCR_ROUTING_RULES_SPEC.md` - Routing rules specification
- `OCR_MCP_SYSTEM_COMPLETE.md` - Complete system documentation
- `DEVICE_TOPOLOGIES_OCR.md` - Multi-device scenarios
