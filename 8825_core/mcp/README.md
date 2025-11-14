# 8825 Inbox MCP Server

**Purpose:** Receive content from external LLMs (ChatGPT, Claude, etc.) and write to 8825 inbox.

**Status:** Production Ready ✅

---

## Quick Start

### 1. Start Server
```bash
./start_inbox_server.sh
```

### 2. Save API Key
The server will display an API key - save it!

### 3. Configure ChatGPT
Follow instructions in `CHATGPT_SETUP.md`

### 4. Use It
In ChatGPT: "send to 8825 inbox"  
In Windsurf: "fetch inbox"

---

## Architecture

```
ChatGPT (Mobile/Desktop)
    ↓ POST /write_to_inbox
MCP Server (localhost:8828)
    ↓ Writes JSON file
~/Downloads/8825_inbox/pending/
    ↓ "fetch inbox"
Windsurf integrates
```

---

## Files

- **inbox_server.py** - Flask server
- **start_inbox_server.sh** - Startup script
- **CHATGPT_SETUP.md** - ChatGPT configuration guide
- **README.md** - This file

---

## API Endpoints

### POST /write_to_inbox
Write content to inbox (requires API key)

**Headers:**
```
X-API-Key: your-api-key
Content-Type: application/json
```

**Body:**
```json
{
  "content_type": "note|mining_report|achievement|pattern|feature|decision",
  "target_focus": "jh|joju|hcss|team76",
  "content": {...},
  "metadata": {
    "source": "chatgpt",
    "timestamp": "ISO 8601",
    "note": "Optional"
  }
}
```

### GET /health
Health check (no auth required)

### POST /test
Test endpoint (no auth required)

---

## Security

- **API Key:** Required for all writes
- **Network:** localhost only (127.0.0.1)
- **Validation:** Schema validation on all inputs
- **Audit:** All writes logged with timestamp

---

## Testing

### Test Server Health
```bash
curl http://localhost:8828/health
```

### Test Write
```bash
curl -X POST http://localhost:8828/write_to_inbox \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR-KEY" \
  -d '{
    "content_type": "note",
    "target_focus": "jh",
    "content": {"title": "Test", "content": "Hello"},
    "metadata": {"source": "test", "timestamp": "2025-11-08T08:00:00Z"}
  }'
```

---

## Troubleshooting

**Port already in use:**
```bash
lsof -i :8828
kill -9 [PID]
```

**Permission denied:**
```bash
chmod +x start_inbox_server.sh
```

**Flask not found:**
```bash
pip3 install flask
```

---

## Integration with ChatGPT

See `CHATGPT_SETUP.md` for complete ChatGPT Custom GPT configuration.

---

**Created:** 2025-11-08  
**Version:** 1.0  
**Status:** Production Ready ✅
