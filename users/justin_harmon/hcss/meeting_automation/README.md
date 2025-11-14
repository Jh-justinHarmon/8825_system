# HCSS Meeting Automation

**User:** justin_harmon  
**Focus:** hcss  
**Strategy:** Dual-source (Otter API + Gmail)

---

## 🚀 SETUP

### **1. Copy Config**
```bash
cp config.example.json config.json
nano config.json
```

### **2. Configure Otter API**
```json
{
  "otter_api": {
    "enabled": true,
    "email": "your_otter_email@example.com"
  }
}
```

Store password in macOS Keychain:
```bash
security add-generic-password \
  -a justin_harmon \
  -s 8825_otter_justin_harmon_hcss \
  -w "your_otter_password"
```

### **3. Configure Gmail API**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project: "8825-meeting-automation"
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `gmail_credentials.json`
6. Place in this directory

### **4. Test**
```bash
cd /path/to/8825-system/users/justin_harmon/hcss/meeting_automation
python3 test_config.py
```

---

## 📁 FILES

```
meeting_automation/
├── config.json              # Your config (gitignored)
├── config.example.json      # Template
├── gmail_credentials.json   # OAuth credentials (gitignored)
├── gmail_token.json         # OAuth token (gitignored)
├── otter_client.py          # Otter API wrapper
├── gmail_client.py          # Gmail API wrapper
├── dual_source_manager.py   # Manages both sources
├── meeting_processor.py     # Processes transcripts
├── summary_generator.py     # Generates summaries
├── poller.py                # Automated polling
└── logs/                    # Processing logs
```

---

## 🎮 USAGE

### **Start Polling**
```bash
python3 poller.py --daemon
```

### **Stop Polling**
```bash
python3 poller.py --stop
```

### **Check Status**
```bash
python3 poller.py --status
```

### **Process Single File**
```bash
python3 meeting_processor.py /path/to/transcript.txt
```

---

## 🔐 SECURITY

- ✅ `config.json` is gitignored
- ✅ `gmail_credentials.json` is gitignored
- ✅ `gmail_token.json` is gitignored
- ✅ Otter password in macOS Keychain
- ✅ All credentials user-specific

---

## 📊 MONITORING

### **Logs**
```bash
tail -f logs/poller.log
tail -f logs/dual_source_manager.log
tail -f logs/meeting_processor.log
```

### **Health Status**
```bash
python3 dual_source_manager.py --health
```

---

## 🎯 OUTPUT

Processed meetings saved to:
```
users/justin_harmon/hcss/knowledge/meetings/
├── transcripts/
│   └── TGIF_Meeting_2025-11-11.txt
├── summaries/
│   └── TGIF_Meeting_2025-11-11.md
└── json/
    └── TGIF_Meeting_2025-11-11.json
```

---

**Status:** Ready for setup  
**Next:** Configure credentials and test
