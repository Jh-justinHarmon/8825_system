# 🔍 Rhino Contribution Scanner

Generate portfolio metrics and contribution stats from your Rhino 3D files.

---

## 🎯 What It Does

Scans your archive of `.3dm` files and generates:

- **Total file count** and size
- **Years of experience** (based on file dates)
- **Files per year** breakdown
- **Category analysis** (Eyewear, Watches, Brands, etc.)
- **Timeline visualization** (contribution graph by year)
- **Portfolio metrics** for your profile

---

## 📋 Requirements

### Basic (File System Only):
```bash
# No requirements - uses Python standard library
python3 rhino_contribution_scanner.py /path/to/archive
```

### Advanced (With Rhino Metadata):
```bash
# Install rhino3dm for deeper file analysis
pip install rhino3dm

python3 rhino_contribution_scanner.py /path/to/archive
```

**With rhino3dm you get:**
- Object counts per file
- Rhino version info
- Unit system details

---

## 🚀 Usage

### Basic Scan:
```bash
python3 rhino_contribution_scanner.py "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/Jh-ARCHV"
```

### Output Example:
```
🔍 Scanning: /Users/justinharmon/.../Jh-ARCHV

📁 Found 247 Rhino files

============================================================
📊 RHINO CONTRIBUTION REPORT
============================================================

📈 OVERVIEW
   Total Rhino Files: 247
   Total Size: 1,234.5 MB
   Date Range: 2004-03-15 to 2024-11-07
   Years of Experience: 20.6 years
   Avg Files/Year: 12.0

📂 BY CATEGORY
   Eyewear: 145 files (58.7%)
   Watches: 52 files (21.1%)
   Nike: 28 files (11.3%)
   Prototypes: 15 files (6.1%)
   Other: 7 files (2.8%)

📅 BY YEAR
   2004:  12 files ███
   2005:  18 files ████
   2006:  22 files █████
   ...
   2023:  15 files ████
   2024:   8 files ██

💼 PORTFOLIO METRICS
   ✓ 20.6 years of Rhino 3D experience
   ✓ 247 products/models designed
   ✓ Range of work: Eyewear, Watches, Nike

============================================================

💾 Stats saved to: rhino_contribution_stats.json
```

---

## 📊 Output Files

### `rhino_contribution_stats.json`
Complete JSON with:
```json
{
  "total_files": 247,
  "years_of_experience": 20.6,
  "by_year": {
    "2004": 12,
    "2005": 18,
    ...
  },
  "by_category": {
    "Eyewear": 145,
    "Watches": 52,
    ...
  },
  "file_list": [
    {
      "name": "nike_vision_frame_v3.3dm",
      "path": "Nike/Vision/nike_vision_frame_v3.3dm",
      "modified": "2008-06-15T14:23:45",
      "size_mb": 4.2,
      "category": "Nike",
      "object_count": 127
    },
    ...
  ]
}
```

---

## 🏷️ Category Detection

Auto-categorizes files based on path/filename:

- **Eyewear**: eyewear, glasses, sunglass, optical
- **Watches**: watch, timepiece
- **Brands**: Nike, COSTA, Dragon, Fossil, Marchon, Shinola
- **Prototypes**: prototype, proto
- **Concepts**: concept
- **Other**: Everything else

---

## 💡 Use Cases

### 1. Portfolio Metrics
```
"20+ years of Rhino 3D experience"
"250+ products designed using Rhino"
"Expertise spanning eyewear, watches, and accessories"
```

### 2. Joju Profile
Add to your read.CV profile:
- Years of tool experience
- Volume of work
- Range of categories

### 3. Resume Stats
Quantify your design output:
- "Designed 145+ eyewear styles"
- "Created 52 watch designs"
- "20-year Rhino 3D portfolio"

### 4. Contribution Graph
Generate visual timeline of your work (future feature)

---

## 🔧 Customization

### Add Custom Categories

Edit the `_categorize_file()` method:

```python
def _categorize_file(self, file_path):
    path_str = str(file_path).lower()
    
    # Add your custom categories
    if "jewelry" in path_str:
        return "Jewelry"
    elif "furniture" in path_str:
        return "Furniture"
    # ... existing categories
```

### Filter by Date Range

Add date filtering in `scan()`:

```python
def scan(self, start_year=None, end_year=None):
    # Filter files by year
    if start_year and modified_time.year < start_year:
        continue
    if end_year and modified_time.year > end_year:
        continue
```

---

## 🎨 Future Enhancements

- [ ] Visual contribution graph (like GitHub)
- [ ] Export to HTML/PDF report
- [ ] Compare multiple designers
- [ ] Integration with Joju profile builder
- [ ] Thumbnail generation from .3dm files
- [ ] Time-based heatmap (files per month)

---

## 📝 Notes

- **File dates**: Uses modification date (not creation date)
- **Nested folders**: Recursively scans all subdirectories
- **Large archives**: May take time for 1000+ files
- **Metadata**: Requires `rhino3dm` library for deep analysis

---

## 🚀 Quick Start

```bash
# 1. Navigate to joju_sandbox
cd joju_sandbox

# 2. Run scanner on your archive
python3 rhino_contribution_scanner.py "/path/to/Jh-ARCHV"

# 3. View JSON output
cat rhino_contribution_stats.json

# 4. Use metrics in your profile!
```

---

**Ready to quantify your Rhino work!** 🎯
