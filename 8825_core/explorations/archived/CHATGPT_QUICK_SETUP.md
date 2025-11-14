# ChatGPT Custom GPT Quick Setup

**MCP Server is Running!** ✅

**API Key:** `8825-inbox-5183002D-6410-417A-BF70-4F4828CCC0B0`

---

## Step 1: Create Custom GPT

1. Go to ChatGPT on your phone or computer
2. Tap/click your profile → **"My GPTs"**
3. Tap/click **"Create a GPT"**
4. Name it: **"8825 Inbox"**

---

## Step 2: Add Instructions

In the **"Configure"** tab, paste this:

```
You are the 8825 Inbox Assistant. When I say "send to 8825 inbox":

1. Extract the conversation content
2. Structure it as JSON with these fields:
   - content_type: "note" (or mining_report, achievement, pattern, feature, decision)
   - target_focus: "jh" (or joju, hcss, team76)
   - content: {structured content}
   - metadata: {source: "chatgpt", timestamp: ISO 8601, note: "description"}

3. Call the write_to_inbox action
4. Confirm: "✅ Sent to 8825 inbox. Tell Windsurf: 'fetch inbox'"
```

---

## Step 3: Add Action

In the **"Actions"** section:

### **Authentication:**
- Type: **API Key**
- Auth Type: **Custom**
- Custom Header Name: **X-API-Key**
- API Key: **8825-inbox-5183002D-6410-417A-BF70-4F4828CCC0B0**

### **Schema:**

Paste this entire JSON:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "8825 Inbox API",
    "description": "Write content to 8825 inbox",
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
                    "enum": ["mining_report", "achievement", "pattern", "note", "feature", "decision"]
                  },
                  "target_focus": {
                    "type": "string",
                    "enum": ["joju", "hcss", "team76", "jh"]
                  },
                  "content": {
                    "type": "object"
                  },
                  "metadata": {
                    "type": "object",
                    "required": ["source", "timestamp"],
                    "properties": {
                      "source": {"type": "string"},
                      "timestamp": {"type": "string"},
                      "note": {"type": "string"}
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Success"
          }
        }
      }
    }
  }
}
```

---

## Step 4: Save & Test

1. Save the Custom GPT
2. In ChatGPT, say: **"send this to 8825 inbox: Test message"**
3. ChatGPT should call the API automatically
4. Come back to Windsurf and say: **"fetch inbox"**

---

## Important Notes:

⚠️ **Server must be running** for this to work  
⚠️ **Only works on same computer** (localhost)  
⚠️ **Mobile ChatGPT** won't work with localhost (use desktop ChatGPT)

---

## If It Doesn't Work:

**Problem:** "Connection refused"  
**Solution:** Make sure server is running (check Windsurf terminal)

**Problem:** "Unauthorized"  
**Solution:** Check API key is exactly: `8825-inbox-5183002D-6410-417A-BF70-4F4828CCC0B0`

**Problem:** Mobile not working  
**Solution:** Use desktop ChatGPT (localhost doesn't work from mobile)

---

**Server Status:** Running on http://127.0.0.1:8828 ✅  
**API Key:** 8825-inbox-5183002D-6410-417A-BF70-4F4828CCC0B0  
**Ready to configure!** 🚀
