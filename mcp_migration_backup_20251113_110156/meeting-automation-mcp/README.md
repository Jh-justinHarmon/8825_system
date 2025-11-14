# Meeting Automation MCP Server

**Port:** N/A (stdio communication)  
**Purpose:** Control meeting automation via Goose  
**Users:** justin_harmon (hcss focus)

---

## 🎮 GOOSE COMMANDS

### **Status**
```
> What's my HCSS meeting automation status?
> Is meeting automation running?
```

### **Control**
```
> Start HCSS meeting automation
> Stop HCSS meeting automation
```

### **Monitoring**
```
> Check HCSS meeting automation health
> Show recent HCSS meetings
> Show last 5 HCSS meetings
```

---

## 🔧 TOOLS

### **meeting/status**
Get meeting automation status

**Params:**
- `user_id` (optional): Default "justin_harmon"
- `focus` (optional): Default "hcss"

**Returns:**
```json
{
  "status": "enabled",
  "polling": true,
  "strategy": "dual_source",
  "primary_source": "otter_api",
  "otter_enabled": true,
  "gmail_enabled": true
}
```

### **meeting/start**
Start automated polling

### **meeting/stop**
Stop automated polling

### **meeting/health**
Get health status of both sources

### **meeting/recent**
Get recent meeting summaries

**Params:**
- `limit` (optional): Number of meetings (default 10)

---

## 🚀 SETUP

### **1. Add to Goose**
```bash
cd ~/.config/goose
cat >> profiles.yaml << 'EOF'

meeting-automation:
  provider: openai
  processor: gpt-4
  accelerator: gpt-4
  moderator: passive
  toolkits:
    - name: meeting-automation
      requires: {}
EOF
```

### **2. Test**
```bash
goose session start --profile meeting-automation

> What's my HCSS meeting automation status?
```

---

## 📊 ARCHITECTURE

```
Goose (Natural Language)
         ↓
Meeting Automation MCP
         ↓
User-Specific Poller
  (justin_harmon/hcss)
         ↓
Dual-Source Manager
         ↓
    Otter API + Gmail
```

---

**Status:** Ready for use  
**Integration:** Complete
