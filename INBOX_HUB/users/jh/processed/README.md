# 8825 Inbox: ChatGPT → Windsurf Transport Layer

**Purpose:** Transfer information from ChatGPT to 8825 system  
**Status:** Active  
**Created:** 2025-11-08

---

## 📁 Folder Structure:

- **pending/** - New files from ChatGPT waiting to be processed
- **processing/** - Files currently being reviewed
- **completed/** - Successfully integrated files (archived)
- **errors/** - Files with validation errors

---

## 📋 How to Use:

### **In ChatGPT:**

Add this to your ChatGPT custom instructions:

```
When I say "write to 8825 inbox", create a JSON file with this structure:

{
  "content_type": "mining_report|achievement|pattern|note|feature|decision",
  "target_focus": "joju|hcss|team76|jh",
  "content": {
    // Your structured data here
  },
  "metadata": {
    "source": "chatgpt",
    "timestamp": "2025-11-08T07:38:00Z",
    "note": "Optional description"
  }
}

Save as: ~/Downloads/8825_inbox/pending/YYYYMMDD_HHMMSS_{type}_{focus}.json

Then say: "✅ Written to inbox. Tell Windsurf: 'fetch inbox'"
```

### **In Windsurf:**

Just say: **"fetch inbox"**

Windsurf will:
1. Find all pending files
2. Validate format
3. Show summary
4. Wait for approval
5. Integrate to appropriate location
6. Move to completed/

---

## 📝 JSON Format:

### **Required Fields:**
- `content_type` - Type of content (mining_report, achievement, pattern, note, feature, decision)
- `target_focus` - Where it goes (joju, hcss, team76, jh)
- `content` - The actual data (structure varies by type)
- `metadata.source` - Always "chatgpt"
- `metadata.timestamp` - ISO 8601 format

### **Optional Fields:**
- `metadata.note` - Your description/context

---

## 🎯 Integration Targets:

**joju** → `joju_sandbox/libraries/justin_harmon_master_library.json`  
**hcss** → `focuses/hcss/knowledge/`  
**team76** → `focuses/joju/projects/`  
**jh** → `users/justinharmon/personal/`

---

## ✅ Example File:

**Filename:** `20251108_073800_achievement_joju.json`

```json
{
  "content_type": "achievement",
  "target_focus": "joju",
  "content": {
    "title": "Built ChatGPT transport layer",
    "description": "Created inbox system for seamless ChatGPT → Windsurf integration",
    "impact": "Eliminated manual extraction workflow",
    "date": "2025-11-08"
  },
  "metadata": {
    "source": "chatgpt",
    "timestamp": "2025-11-08T07:38:00Z",
    "note": "Mobile conversation about transport architecture"
  }
}
```

---

## 🔍 Validation Rules:

- ✅ Valid JSON format
- ✅ All required fields present
- ✅ content_type is valid enum
- ✅ target_focus is valid focus
- ✅ timestamp is ISO 8601
- ✅ content is not empty

---

## ⚠️ Error Handling:

**Invalid JSON** → Moved to `errors/` with parse error log  
**Missing fields** → Moved to `errors/` with validation error  
**Unknown type** → Moved to `errors/` with type error  
**Already processed** → Skipped with warning  

---

## 🚀 Quick Start:

1. Add instructions to ChatGPT (see above)
2. Have conversation in ChatGPT
3. Say "write to 8825 inbox"
4. Save JSON file to `pending/`
5. In Windsurf: "fetch inbox"
6. Approve integration
7. Done!

---

**Status:** Infrastructure ready ✅  
**Protocol:** Hardwired into Windsurf memory  
**Location:** `~/Downloads/8825_inbox/`
