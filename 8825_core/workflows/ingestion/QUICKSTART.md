# 8825 Ingestion Engine - Quick Start

Get the ingestion engine up and running in minutes.

---

## 🚀 Installation

### 1. Navigate to Sandbox
```bash
cd "8825_ingestion_sandbox"
```

### 2. Create Folder Structure
```bash
mkdir -p config scripts/{source_handlers,processors,routers,utils} data logs tests
```

### 3. Install Dependencies
```bash
pip install watchdog python-magic PyPDF2 pytesseract
```

---

## ⚙️ Configuration

### 1. Create Config File
```bash
cat > config/ingestion_config.json << 'EOF'
{
  "sources": {
    "downloads": {
      "enabled": true,
      "path": "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/ingestion",
      "poll_interval": 10
    }
  },
  "processing": {
    "parallel_workers": 2,
    "retry_attempts": 3,
    "timeout_seconds": 60
  },
  "routing": {
    "auto_route_threshold": 70,
    "suggest_threshold": 50
  },
  "destinations": {
    "RAL": "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/RAL",
    "HCSS": "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/HCSS",
    "76": "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/76",
    "8825": "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/8825",
    "Jh": "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/Jh"
  }
}
EOF
```

---

## 🏃 Running

### Start Engine (when built):
```bash
python3 scripts/ingestion_engine.py
```

### Monitor Activity:
```bash
tail -f logs/ingestion.log
```

### Check Queue:
```bash
cat data/ingestion_queue.json
```

---

## 🧪 Testing

### Test with Sample File:
```bash
# Copy a test file to ingestion folder
cp ~/Downloads/test.pdf "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/ingestion/"

# Watch the logs
tail -f logs/ingestion.log
```

---

## 📊 Monitoring

### View Processed Files:
```bash
cat data/processed_files.json | jq '.[] | {file: .filename, project: .project, confidence: .confidence}'
```

### Check Failed Items:
```bash
cat data/failed_items.json
```

### Stats Summary:
```bash
python3 scripts/utils/stats.py
```

---

## 🔧 Common Tasks

### Reprocess Failed Items:
```bash
python3 scripts/ingestion_engine.py --retry-failed
```

### Clear Queue:
```bash
rm data/ingestion_queue.json
```

### Reset Tracking:
```bash
rm data/processed_files.json
```

---

## 🐛 Troubleshooting

### Engine Won't Start:
- Check config file exists
- Verify paths are correct
- Check dependencies installed

### Files Not Processing:
- Check ingestion folder permissions
- Verify Downloads Manager is running
- Check logs for errors

### Low Confidence Scores:
- Review project matching rules
- Add more keywords
- Check content analysis

---

## 📚 Next Steps

1. **Review README.md** - Understand architecture
2. **Check STATUS.md** - See current progress
3. **Build core engine** - Start development
4. **Test with real files** - Validate workflow

---

**Ready to ingest!** 🎯
