# Download Folder Wedge

**Purpose:** Intelligent file monitoring and routing system for 8825 projects  
**Status:** In Development  
**Created:** 2025-11-07

---

## 🎯 Overview

The Download Folder Wedge monitors download locations, analyzes incoming files, matches them against 8825 project context, and routes them to the appropriate project folder.

---

## 🔍 How It Works

```
File arrives → Extract metadata → Analyze content → Match to project → Route/Suggest
```

### Matching Confidence Levels:
- **90-100%**: Auto-route (high confidence)
- **50-89%**: Suggest with preview
- **0-49%**: Ask user for clarification

---

## 📂 Project Folders Monitored

### RAL
- **Keywords**: RAL, design, client, creative
- **Types**: Design files, presentations, contracts

### HCSS
- **Keywords**: HCSS, Hammer Consulting, business
- **Types**: Documents, spreadsheets, reports

### TGIF
- **Keywords**: TGIF, Friday, meeting, weekly
- **Types**: Meeting notes, summaries, action items

### 76
- **Keywords**: Joju, Forge, TrustyBit, contacts, profiles
- **Types**: Project docs, JSON, profiles

### 8825
- **Keywords**: Protocol, workflow, system, agent, automation
- **Types**: JSON, markdown, scripts

### Jh
- **Keywords**: Personal, Justin, scripts, tools, notes
- **Types**: Scripts, personal docs, experiments

---

## 🛠️ Components

### 1. File Monitor (`file_monitor.py`)
- Watches download folders
- Triggers on new files
- Queues files for analysis

### 2. Metadata Extractor (`metadata_extractor.py`)
- Extracts filename patterns
- Reads file metadata
- Identifies file type

### 3. Content Analyzer (`content_analyzer.py`)
- Quick text scan
- PDF text extraction
- OCR for images
- Keyword extraction

### 4. Project Matcher (`project_matcher.py`)
- Scores against project contexts
- Calculates confidence
- Suggests destination

### 5. Router (`router.py`)
- Auto-routes high confidence
- Notifies for suggestions
- Logs all actions

---

## 📊 Matching Algorithm

### Level 1: Filename (Instant)
```python
score = keyword_match(filename, project_keywords)
```

### Level 2: Metadata (Fast)
```python
score += date_match(file_date, project_timeline)
score += type_match(file_type, project_types)
```

### Level 3: Content (Slower)
```python
content = extract_text(file)
score += semantic_match(content, project_context)
```

---

## 🚀 Quick Start

### Install Dependencies
```bash
pip install watchdog pytesseract PyPDF2 python-magic
```

### Configure
```bash
cp config.example.json config.json
# Edit config.json with your paths
```

### Run Monitor
```bash
python file_monitor.py
```

### Run as Service (macOS)
```bash
./install_service.sh
```

---

## ⚙️ Configuration

### Monitor Locations
- `~/Downloads/`
- `~/Library/Mobile Documents/com~apple~CloudDocs/Downloads/`
- `~/Desktop/` (optional)

### Project Mappings
Defined in `project_contexts.json`

### Routing Rules
Defined in `routing_rules.json`

---

## 📋 Usage Examples

### Example 1: TGIF Meeting
```
Input: TGIF_Meeting_2025-11-07.docx
Match: HCSS/TGIF (95%)
Action: Auto-route to HCSS/TGI Fridays/ - meeting summaries -
```

### Example 2: Unknown PDF
```
Input: Document_12345.pdf
Content: "Joju profile achievement"
Match: 76 (78%)
Action: Suggest move to 76 folder
```

### Example 3: Screenshot
```
Input: Screenshot 2025-11-07.png
OCR: "Figma prototype comments"
Match: RAL (65%)
Action: Ask user which project
```

---

## 🔔 Notifications

### macOS Notification
- Shows file name
- Displays confidence score
- Provides action buttons

### Log File
- All actions logged
- Review history
- Track accuracy

---

## 🧠 Learning System

### Track Corrections
- User moves file manually
- System learns from correction
- Updates project patterns

### Improve Over Time
- Builds custom keyword lists
- Refines confidence thresholds
- Adapts to user preferences

---

## 📊 Statistics

### Dashboard
- Files processed
- Auto-routed vs suggested
- Accuracy rate
- Top projects

---

## 🔧 Advanced Features

### Multi-Location Support
Monitor multiple folders simultaneously

### Batch Processing
Process existing files in folder

### Dry Run Mode
Test without moving files

### Whitelist/Blacklist
Exclude certain file types or patterns

---

## 🎯 Roadmap

### Phase 1: Basic Monitor ✅
- File watching
- Filename matching
- Simple routing

### Phase 2: Content Analysis (In Progress)
- PDF extraction
- OCR support
- Semantic matching

### Phase 3: Learning System (Planned)
- Track corrections
- Improve accuracy
- Custom patterns

### Phase 4: Integration (Future)
- Email attachment monitoring
- Browser download hooks
- Cloud storage sync

---

## 📁 Project Structure

```
download-wedge/
├── README.md
├── config.json
├── project_contexts.json
├── routing_rules.json
├── scripts/
│   ├── file_monitor.py
│   ├── metadata_extractor.py
│   ├── content_analyzer.py
│   ├── project_matcher.py
│   └── router.py
├── logs/
│   └── wedge.log
└── data/
    └── learning_data.json
```

---

**Intelligent file routing for 8825 projects!** 🚀
