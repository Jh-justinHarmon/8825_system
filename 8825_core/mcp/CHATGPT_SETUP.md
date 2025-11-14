# ChatGPT Custom GPT Setup for 8825 Inbox

## Step 1: Start the MCP Server

In terminal:
```bash
cd ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 3.0/8825_core/mcp/
./start_inbox_server.sh
```

**Save the API key that's displayed!**

---

## Step 2: Create Custom GPT in ChatGPT

1. Go to ChatGPT
2. Click your profile → "My GPTs"
3. Click "Create a GPT"
4. Name it: **"8825 Inbox"**

---

## Step 3: Add Custom Instructions

In the "Configure" tab, add this to instructions:

```
You are the 8825 Inbox Assistant. When the user says "send to 8825 inbox" or "write to inbox":

1. Extract the conversation content
2. Structure it as JSON following the 8825 inbox protocol
3. Call the write_to_inbox action
4. Confirm success

JSON Structure:
{
  "content_type": "note|mining_report|achievement|pattern|feature|decision",
  "target_focus": "jh|joju|hcss|team76",
  "content": {
    // Structured content based on type
  },
  "metadata": {
    "source": "chatgpt",
    "timestamp": "ISO 8601 format",
    "note": "Brief description"
  }
}

Content Type Structures:

NOTE:
{
  "title": "Note title",
  "content": "Note content",
  "tags": ["tag1", "tag2"]
}

ACHIEVEMENT:
{
  "title": "Achievement title",
  "description": "What was accomplished",
  "impact": "Business/user impact",
  "date": "YYYY-MM-DD"
}

MINING_REPORT:
{
  "patterns": ["Pattern 1", "Pattern 2"],
  "insights": ["Insight 1", "Insight 2"],
  "recommendations": ["Rec 1", "Rec 2"]
}

After successful write, say:
"✅ Sent to 8825 inbox. Tell Windsurf: 'fetch inbox'"
```

---

## Step 4: Add Action

In the "Actions" section:

### **Authentication:**
- Type: **API Key**
- Auth Type: **Custom**
- Custom Header Name: **X-API-Key**
- API Key: **[paste the key from Step 1]**

### **Schema:**

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "8825 Inbox API",
    "description": "Write content to 8825 inbox for Windsurf integration",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "http://localhost:8828"
    }
  ],
  "paths": {
    "/write_to_inbox": {
      "post": {
        "operationId": "writeToInbox",
        "summary": "Write content to 8825 inbox",
        "description": "Sends structured content to the 8825 inbox for processing by Windsurf",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": ["content_type", "target_focus", "content", "metadata"],
                "properties": {
                  "content_type": {
                    "type": "string",
                    "enum": ["mining_report", "achievement", "pattern", "note", "feature", "decision"],
                    "description": "Type of content being sent"
                  },
                  "target_focus": {
                    "type": "string",
                    "enum": ["joju", "hcss", "team76", "jh"],
                    "description": "Target focus area"
                  },
                  "content": {
                    "type": "object",
                    "description": "The actual content (structure varies by type)"
                  },
                  "metadata": {
                    "type": "object",
                    "required": ["source", "timestamp"],
                    "properties": {
                      "source": {
                        "type": "string",
                        "default": "chatgpt"
                      },
                      "timestamp": {
                        "type": "string",
                        "format": "date-time"
                      },
                      "note": {
                        "type": "string",
                        "description": "Optional description"
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successfully written to inbox",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "success": {"type": "boolean"},
                    "filename": {"type": "string"},
                    "message": {"type": "string"}
                  }
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized - invalid API key"
          },
          "400": {
            "description": "Bad request - invalid data"
          }
        }
      }
    },
    "/health": {
      "get": {
        "operationId": "healthCheck",
        "summary": "Check server health",
        "responses": {
          "200": {
            "description": "Server is running"
          }
        }
      }
    }
  }
}
```

---

## Step 5: Test It!

1. In your Custom GPT, say: **"send this to 8825 inbox: Test message"**
2. ChatGPT should call the action and confirm success
3. Check `~/Downloads/8825_inbox/pending/` for the file
4. In Windsurf, say: **"fetch inbox"**

---

## Troubleshooting

### **"Connection refused"**
- Make sure the MCP server is running
- Check it's on port 8828: `lsof -i :8828`

### **"Unauthorized"**
- Check API key matches in both places
- Make sure Custom Header Name is exactly: `X-API-Key`

### **"Invalid content_type"**
- Must be one of: mining_report, achievement, pattern, note, feature, decision

### **File not appearing**
- Check server logs for errors
- Verify inbox path: `~/Downloads/8825_inbox/pending/`

---

## Quick Reference

**Start Server:**
```bash
cd ~/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 3.0/8825_core/mcp/
./start_inbox_server.sh
```

**Check Server:**
```bash
curl http://localhost:8828/health
```

**Test Write:**
```bash
curl -X POST http://localhost:8828/write_to_inbox \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR-API-KEY" \
  -d '{
    "content_type": "note",
    "target_focus": "jh",
    "content": {"title": "Test", "content": "Test message"},
    "metadata": {"source": "test", "timestamp": "2025-11-08T08:00:00Z"}
  }'
```

---

**Status:** Ready for ChatGPT integration! 🚀
