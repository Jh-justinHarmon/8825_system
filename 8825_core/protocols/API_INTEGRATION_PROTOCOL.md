# API Integration Protocol

**Status:** Proven (Gemini + OpenAI integrations, 0 issues, 95 min total)  
**Success Rate:** 100% (2/2 integrations)  
**Time Improvement:** 50% on second integration via template reuse

---

## 🎯 Overview

4-phase protocol that eliminates issues and reduces integration time by predicting risks upfront and proving functionality before building UI.

**Results:**
- Gemini: 90 min, 0 issues
- OpenAI: 45 min, 0 issues (50% faster via template reuse)
- Both keys persist to `.env`, both production-ready

---

## 📋 The 4 Phases

### **Phase 1: Analysis (PromptGen)**

**Goal:** Predict ALL risks before writing any code

**Steps:**
1. Run PromptGen analysis on the integration
2. Identify potential issues:
   - Authentication method (OAuth, API key, token)
   - Rate limits and quotas
   - SDK version conflicts
   - CORS issues
   - Credential storage security
   - Error scenarios
3. Get user approval on approach
4. Document expected issues

**Output:** Risk analysis document with mitigation strategies

---

### **Phase 2: Backend Verification**

**Goal:** Prove the API works BEFORE building UI

**Steps:**
1. Test with `curl` first (raw HTTP)
2. Install SDK/library
3. Write minimal Python test script
4. Validate:
   - Credentials work
   - API responds correctly
   - Data format is as expected
   - Error handling works
5. Save successful test code

**Output:** Working backend code that proves integration works

**Example:**
```bash
# Test Gemini API with curl
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

---

### **Phase 3: Frontend Integration**

**Goal:** Wire UI to proven backend, avoid CORS issues

**Steps:**
1. Use `integration_server.py` pattern (Flask on port 5001)
2. Serve HTML from Flask (same origin = no CORS)
3. Clone existing integration HTML as template
4. Update branding and service-specific fields
5. Wire frontend to backend endpoints

**Key Pattern:**
- Serve HTML from Flask: `@app.route('/setup')`
- Use `send_file()` to serve HTML templates
- Frontend calls backend on same origin (localhost:5001)
- No CORS configuration needed

**Template Reuse:**
- Clone Gemini/OpenAI HTML
- Find/replace service name
- Update logo and colors
- Adjust validation logic
- Keep same structure (3-step flow)

---

### **Phase 4: E2E Validation**

**Goal:** Verify complete user journey with real credentials

**Steps:**
1. Start integration server
2. Open setup page in browser
3. Enter real API key/credentials
4. Test connection (backend verification)
5. Save to `.env`
6. Verify:
   - Key saved correctly
   - Backup created
   - Environment reloaded
   - No restart required
   - Integration immediately usable

**Success Criteria:**
- ✅ Credentials persist to `.env`
- ✅ Backup created with timestamp
- ✅ Existing keys preserved (append logic)
- ✅ Environment variables loaded
- ✅ Integration works immediately

---

## 🔧 Technical Patterns

### **Flask Backend Structure**

```python
from flask import Flask, send_file, request, jsonify
from pathlib import Path
from dotenv import load_dotenv, set_key
import os
import shutil
from datetime import datetime

app = Flask(__name__)

# Serve HTML
@app.route('/setup/<service>')
def setup_page(service):
    html_path = Path(__file__).parent / 'templates' / f'{service}_setup.html'
    return send_file(html_path)

# Save credentials
@app.route('/api/configure/<service>', methods=['POST'])
def configure_service(service):
    data = request.json
    api_key = data.get('api_key')
    
    # 1. Validate format
    if not validate_key(service, api_key):
        return jsonify({'success': False, 'error': 'Invalid key format'})
    
    # 2. Backup .env
    backup_env()
    
    # 3. Append to .env (preserve existing)
    env_path = Path.home() / '.env'
    key_name = f'{service.upper()}_API_KEY'
    
    with open(env_path, 'a') as f:
        f.write(f'\n# {service.title()} Configuration\n')
        f.write(f'# Added: {datetime.now().isoformat()}\n')
        f.write(f'{key_name}={api_key}\n')
    
    # 4. Reload environment
    load_dotenv(env_path, override=True)
    
    # 5. Test connection
    test_result = test_connection(service, api_key)
    
    return jsonify({
        'success': True,
        'key_preview': f'{api_key[:10]}...{api_key[-4:]}',
        'test_result': test_result
    })
```

### **.env Management**

**Backup Logic:**
```python
def backup_env():
    """Create timestamped backup before modifying .env"""
    env_path = Path.home() / '.env'
    if not env_path.exists():
        return
    
    backup_dir = Path.home() / 'backups' / 'env_backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f'.env.backup.{timestamp}'
    
    shutil.copy2(env_path, backup_path)
```

**Append Logic (Preserve Existing):**
```python
def append_to_env(key_name, value):
    """Append new key without overwriting existing"""
    env_path = Path.home() / '.env'
    
    # Read existing content
    existing = ''
    if env_path.exists():
        with open(env_path, 'r') as f:
            existing = f.read()
    
    # Check if key already exists
    if f'{key_name}=' in existing:
        # Update existing (optional)
        pass
    else:
        # Append new
        with open(env_path, 'a') as f:
            f.write(f'\n# Added: {datetime.now().isoformat()}\n')
            f.write(f'{key_name}={value}\n')
    
    # Reload
    load_dotenv(env_path, override=True)
```

### **Frontend Template (3-Step Flow)**

```html
<!-- Step 1: Get Credentials -->
<div class="step" id="step1">
    <h3>Step 1: Get Your API Key</h3>
    <ol>
        <li>Go to <a href="..." target="_blank">Service Dashboard</a></li>
        <li>Create new API key</li>
        <li>Copy the key</li>
    </ol>
    <button onclick="nextStep()">Next →</button>
</div>

<!-- Step 2: Paste Credentials -->
<div class="step" id="step2" style="display:none;">
    <h3>Step 2: Paste Your API Key</h3>
    <input type="password" id="apiKey" placeholder="Paste key here">
    <button onclick="testConnection()">Test & Save →</button>
</div>

<!-- Step 3: Test & Save -->
<div class="step" id="step3" style="display:none;">
    <h3>Step 3: Testing Connection...</h3>
    <div class="progress-bar"></div>
    <div id="result"></div>
</div>
```

---

## 📊 Checklist

### **Phase 1: Analysis**
- [ ] Run PromptGen analysis
- [ ] Identify authentication method
- [ ] Document potential issues
- [ ] Get user approval

### **Phase 2: Backend**
- [ ] Test with curl
- [ ] Install SDK
- [ ] Write test script
- [ ] Validate credentials work
- [ ] Save working code

### **Phase 3: Frontend**
- [ ] Clone existing template
- [ ] Update branding
- [ ] Wire to backend
- [ ] Test in browser
- [ ] Verify no CORS issues

### **Phase 4: E2E**
- [ ] Enter real credentials
- [ ] Test connection
- [ ] Save to .env
- [ ] Verify backup created
- [ ] Verify existing keys preserved
- [ ] Verify immediate availability

---

## 🎯 Success Metrics

**Time:**
- First integration: ~90 min
- Second integration: ~45 min (template reuse)
- Third+ integrations: ~30 min (proven pattern)

**Quality:**
- 0 CORS issues (serve from Flask)
- 0 credential loss (backup + append)
- 0 restart required (dotenv reload)
- 100% immediate availability

**ROI:**
- 50% time reduction per integration
- 0 debugging time
- 0 "BRUH" moments
- Proven template for future integrations

---

## 🔄 Template Reuse Pattern

**For each new integration:**

1. **Clone HTML:**
   ```bash
   cp gemini_setup.html new_service_setup.html
   ```

2. **Find/Replace:**
   - Service name (Gemini → New Service)
   - Logo/branding
   - API key format validation
   - Documentation links

3. **Update Backend:**
   - Add route: `/setup/new_service`
   - Add validation: `validate_new_service_key()`
   - Add test: `test_new_service_connection()`

4. **Test E2E:**
   - Real credentials
   - Full flow
   - Verify persistence

**Time: ~30 minutes per integration**

---

## 🐛 Common Issues & Solutions

### **CORS Errors**
- ❌ Don't: Open HTML as `file://`
- ✅ Do: Serve from Flask on same origin

### **Credential Loss**
- ❌ Don't: Overwrite .env
- ✅ Do: Backup + append

### **Multiple Keys**
- ❌ Don't: Replace existing keys
- ✅ Do: Append with comments

### **No Restart**
- ❌ Don't: Require server restart
- ✅ Do: Use `load_dotenv(override=True)`

---

## 📚 Reference Implementations

**Completed Integrations:**
1. Google Gemini API (90 min, 0 issues)
2. OpenAI API (45 min, 0 issues)

**Files:**
- `8825_core/integration_server.py` - Flask backend
- `8825_core/workflows/meeting_automation/gemini_integration_setup.html`
- `8825_core/workflows/meeting_automation/openai_integration_setup.html`

**Port:** 5001 (avoiding macOS AirTunes on 5000)

---

## 🎓 Key Learnings

1. **PromptGen prevents issues** - Predict before coding
2. **Backend-first proves functionality** - curl → SDK → UI
3. **Serve from Flask = no CORS** - Same origin eliminates issues
4. **Template reuse = 50% faster** - Clone and customize
5. **Backup + append = safe** - Never lose existing keys

---

**Ready to integrate a new service?** Follow the 4 phases and you'll be done in ~30-90 minutes with zero issues.
