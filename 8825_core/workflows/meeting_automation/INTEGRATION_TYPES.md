# Integration Types - API Key Input Methods

**Classification for 8825 integration UIs**

---

## Type 1: Paste-Only 📋

**Use when:** API key is simple string, no complex config needed

**UI Elements:**
- ✅ Single text input field
- ✅ Paste instructions
- ❌ No file upload
- ❌ No JSON editor

**Examples:**
- **Gemini API** - Single key: `AIzaSy...`
- **OpenAI API** - Single key: `sk-...`
- **Anthropic API** - Single key: `sk-ant-...`

**Template:**
```html
<input type="text" placeholder="Paste your API key here">
<p>Your key will be stored locally</p>
```

---

## Type 2: File Upload (JSON/ENV) 📄

**Use when:** Multiple credentials or complex configuration

**UI Elements:**
- ✅ Drag & drop file upload
- ✅ File type validation
- ✅ Auto-parse and extract
- ✅ Optional paste fallback

**Examples:**
- **Supabase** - URL + anon key + service key
- **Firebase** - Full config JSON
- **AWS** - Access key + secret + region

**Template:**
```html
<div class="file-upload">
  Drop your config.json here
</div>
<input type="file" accept=".json,.env">
```

---

## Type 3: Hybrid (Paste OR Upload) 🔄

**Use when:** Supporting both simple and advanced users

**UI Elements:**
- ✅ Paste input field
- ✅ "OR" divider
- ✅ File upload option
- ✅ Auto-detect format

**Examples:**
- **Google Cloud** - Service account JSON OR API key
- **Stripe** - Test key OR live key file
- **Twilio** - Account SID + Auth token OR credentials file

**Template:**
```html
<input type="text" placeholder="Paste key">
<div class="divider">OR</div>
<div class="file-upload">Upload .env</div>
```

---

## Type 4: OAuth Flow 🔐

**Use when:** OAuth 2.0 or complex auth required

**UI Elements:**
- ✅ "Connect with [Service]" button
- ✅ Popup/redirect flow
- ✅ Token storage
- ❌ No manual input

**Examples:**
- **GitHub OAuth** - Authorize app
- **Google OAuth** - Sign in with Google
- **Slack OAuth** - Add to Slack

**Template:**
```html
<button onclick="startOAuth()">
  Connect with GitHub
</button>
```

---

## Decision Matrix

| Integration | Type | Reason |
|-------------|------|--------|
| Gemini API | Paste-Only | Single key string |
| OpenAI API | Paste-Only | Single key string |
| Supabase | File Upload | URL + multiple keys |
| Firebase | File Upload | Complex JSON config |
| GitHub | OAuth | Requires authorization |
| Stripe | Hybrid | Test key OR config file |
| AWS | File Upload | Access + secret + region |
| Anthropic | Paste-Only | Single key string |

---

## Implementation Guidelines

### **Paste-Only**
```typescript
interface PasteOnlyConfig {
  keyFormat: RegExp;  // e.g., /^AIzaSy/
  placeholder: string;
  validation: (key: string) => boolean;
}
```

### **File Upload**
```typescript
interface FileUploadConfig {
  acceptedTypes: string[];  // ['.json', '.env']
  parser: (content: string) => Config;
  validator: (config: Config) => boolean;
}
```

### **Hybrid**
```typescript
interface HybridConfig {
  pasteConfig: PasteOnlyConfig;
  fileConfig: FileUploadConfig;
  priority: 'paste' | 'file';  // Which to show first
}
```

---

## UI Consistency Rules

1. **Always show what will be saved**
   - Preview extracted values
   - Show file location
   - Confirm before save

2. **Provide clear feedback**
   - Validation errors
   - Success messages
   - Next steps

3. **Security messaging**
   - "Stored locally"
   - "Never shared"
   - "Encrypted at rest"

4. **Test before save**
   - "Test Connection" button
   - Verify credentials work
   - Show which services are accessible

---

## Current Implementations

### ✅ Gemini API (Paste-Only)
- **File:** `gemini_integration_setup.html`
- **Type:** Paste-Only
- **Status:** Implemented
- **UI:** Single input field, no file upload

### 🔄 Future Integrations

**Planned:**
- OpenAI API (Paste-Only)
- Supabase (File Upload)
- GitHub OAuth (OAuth Flow)

---

## Template Selection Guide

**Ask these questions:**

1. **How many credentials?**
   - 1 → Paste-Only
   - 2-3 → Hybrid
   - 4+ → File Upload

2. **Is it a JSON object?**
   - Yes → File Upload
   - No → Paste-Only

3. **Does it require OAuth?**
   - Yes → OAuth Flow
   - No → Continue

4. **Do users have existing config files?**
   - Yes → Hybrid or File Upload
   - No → Paste-Only

---

**Status:** ✅ Classification system established  
**Date:** 2025-11-14  
**Next:** Apply to all future integrations
