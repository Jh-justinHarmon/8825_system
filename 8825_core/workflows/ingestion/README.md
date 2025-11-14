# 8825 Ingestion Engine

**Purpose:** Central ingestion and processing system for all 8825 workflows  
**Status:** Active Development  
**Created:** 2025-11-07

---

## 🎯 Overview

The 8825 Ingestion Engine is the central nervous system for processing, analyzing, and routing all incoming data across the 8825 ecosystem.

---

## 🔄 What It Does

```
Input Sources → Ingestion → Analysis → Classification → Routing → Storage
```

### **Input Sources:**
- Downloads folder (via Downloads Manager)
- Email attachments (via Gmail extractor)
- Manual uploads
- API integrations
- Web scraping
- Archive scanning

### **Processing:**
- Metadata extraction
- Content analysis
- Entity recognition
- Project matching
- Confidence scoring

### **Output:**
- Filed to project folders
- Indexed in master database
- Available for search/retrieval
- Tracked for lifecycle management

---

## 📂 Folder Structure

```
8825_ingestion_sandbox/
├── README.md                    # This file
├── STATUS.md                    # Current status and roadmap
├── QUICKSTART.md               # Getting started guide
├── config/
│   ├── ingestion_config.json   # Main configuration
│   ├── source_mappings.json    # Input source definitions
│   └── routing_rules.json      # Output routing rules
├── scripts/
│   ├── ingestion_engine.py     # Main engine
│   ├── source_handlers/        # Input source handlers
│   │   ├── downloads_handler.py
│   │   ├── email_handler.py
│   │   ├── manual_handler.py
│   │   └── api_handler.py
│   ├── processors/             # Content processors
│   │   ├── metadata_processor.py
│   │   ├── content_processor.py
│   │   ├── entity_extractor.py
│   │   └── classifier.py
│   ├── routers/                # Output routers
│   │   ├── project_router.py
│   │   ├── archive_router.py
│   │   └── database_router.py
│   └── utils/
│       ├── logger.py
│       ├── tracker.py
│       └── validator.py
├── data/
│   ├── ingestion_queue.json    # Processing queue
│   ├── processed_files.json    # Processed file registry
│   └── failed_items.json       # Failed ingestion log
├── logs/
│   └── ingestion.log           # Activity log
└── tests/
    └── test_ingestion.py       # Unit tests
```

---

## 🔌 Input Sources

### **1. Downloads Folder**
- Monitored by Downloads Manager
- Copies to Documents/ingestion/
- Triggers ingestion engine

### **2. Email Attachments**
- Gmail API extraction
- Automatic download
- Metadata from email context

### **3. Manual Uploads**
- Drag-and-drop interface
- CLI upload command
- Batch upload support

### **4. API Integrations**
- Mural boards
- Figma files
- GitHub repos
- Notion pages

### **5. Archive Scanning**
- Jh-ARCHV processing
- Historical data import
- Bulk ingestion

---

## ⚙️ Processing Pipeline

### **Stage 1: Intake**
```python
{
  "source": "downloads",
  "file_path": "/path/to/file.pdf",
  "timestamp": "2025-11-07T16:55:00",
  "metadata": {...}
}
```

### **Stage 2: Analysis**
```python
{
  "file_type": "pdf",
  "size_mb": 2.4,
  "text_content": "...",
  "entities": ["Joju", "Trustybits"],
  "keywords": ["profile", "UX", "design"]
}
```

### **Stage 3: Classification**
```python
{
  "project": "76",
  "confidence": 85,
  "category": "Documentation",
  "tags": ["joju", "profile", "ux"]
}
```

### **Stage 4: Routing**
```python
{
  "destinations": [
    "Documents/76/",
    "Database/profiles/",
    "Archive/2025-11/"
  ],
  "actions": ["file", "index", "archive"]
}
```

---

## 🎯 Project Matching

### **Confidence Levels:**
- **90-100%** - Auto-route with high confidence
- **70-89%** - Auto-route with logging
- **50-69%** - Suggest destination
- **0-49%** - Manual review required

### **Matching Factors:**
1. Filename patterns
2. Content keywords
3. Entity recognition
4. Source context
5. Historical patterns
6. User corrections

---

## 📊 Tracking & Monitoring

### **Ingestion Queue:**
- Pending items
- Processing status
- Priority levels
- Retry attempts

### **Processed Registry:**
- All ingested files
- Processing timestamps
- Destinations
- Confidence scores

### **Failed Items:**
- Error details
- Retry count
- Manual review flag

---

## 🔄 Integration Points

### **Downloads Manager:**
```
Downloads Manager → Documents/ingestion/ → Ingestion Engine
```

### **Gmail Extractor:**
```
Gmail API → Email Handler → Ingestion Engine
```

### **Manual Upload:**
```
CLI/UI → Manual Handler → Ingestion Engine
```

### **Archive Scanner:**
```
Jh-ARCHV → Archive Handler → Ingestion Engine
```

---

## 🚀 Quick Start

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Configure:
```bash
cp config/ingestion_config.example.json config/ingestion_config.json
# Edit configuration
```

### Run Engine:
```bash
python3 scripts/ingestion_engine.py
```

### Monitor:
```bash
tail -f logs/ingestion.log
```

---

## 📋 Configuration

### **ingestion_config.json:**
```json
{
  "sources": {
    "downloads": {
      "enabled": true,
      "path": "/Users/.../Documents/ingestion",
      "poll_interval": 10
    },
    "email": {
      "enabled": false,
      "gmail_api": true
    }
  },
  "processing": {
    "parallel_workers": 4,
    "retry_attempts": 3,
    "timeout_seconds": 60
  },
  "routing": {
    "auto_route_threshold": 70,
    "suggest_threshold": 50
  }
}
```

---

## 🎯 Roadmap

### **Phase 1: Core Engine** (In Progress)
- [x] Folder structure
- [ ] Basic ingestion pipeline
- [ ] Downloads integration
- [ ] Simple routing

### **Phase 2: Enhanced Processing**
- [ ] Content analysis
- [ ] Entity extraction
- [ ] Smart classification
- [ ] Learning system

### **Phase 3: Multi-Source**
- [ ] Email integration
- [ ] API connectors
- [ ] Archive scanner
- [ ] Manual upload UI

### **Phase 4: Intelligence**
- [ ] Pattern learning
- [ ] Auto-tagging
- [ ] Duplicate detection
- [ ] Relationship mapping

---

## 🔧 Development

### Run Tests:
```bash
python3 -m pytest tests/
```

### Debug Mode:
```bash
DEBUG=1 python3 scripts/ingestion_engine.py
```

### Dry Run:
```bash
python3 scripts/ingestion_engine.py --dry-run
```

---

## 📊 Metrics

Track:
- Files ingested per day
- Processing time per file
- Confidence score distribution
- Auto-route success rate
- Failed ingestion rate
- Storage usage

---

## 🔗 Related Systems

- **Downloads Manager** - Feeds files to ingestion
- **Joju** - Consumes profile data
- **HCSS** - Consumes business docs
- **76** - Consumes project files
- **8825** - Consumes system files

---

**Central ingestion for the entire 8825 ecosystem!** 🎯
