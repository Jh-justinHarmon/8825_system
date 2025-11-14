# FDS + HCSS Meeting Automation Integration Design

**Date:** November 11, 2025  
**Status:** Design Phase  
**Architecture:** User-Specific Credentials + System-Wide Processing

---

## 🎯 CORE PRINCIPLE

**All credentials must be user-specific, stored in user directories, never in system-wide code.**

---

## 📊 CURRENT STATE ANALYSIS

### **File Dispatch System (FDS)**
**Location:** `INBOX_HUB/file_dispatch_system/`  
**Purpose:** System-wide file orchestration  
**Scope:** All users, all file types

**Current Classification:**
- JSON/TXT/TXF → Ingestion system
- Screenshots → Screenshot processor
- BRAIN_TRANSPORT → Protected (copy to output)
- Everything else → Progressive router

**Missing:** Meeting transcript handling

---

### **HCSS Meeting Automation**
**Location:** `focuses/hcss/automation/` and `focuses/hcss/workflows/`  
**Purpose:** TGIF meeting summary automation  
**Scope:** HCSS focus only, Justin Harmon user only

**Two Protocols Documented:**
1. **Gmail API** - Poll for Otter.ai emails
2. **Otter.ai Unofficial API** - Direct API access (risky)

**Status:** Documented but never implemented

---

## 🏗️ PROPOSED ARCHITECTURE

### **Layer 1: System-Wide (FDS)**
**What:** File detection and classification  
**Where:** `INBOX_HUB/file_dispatch_system/`  
**Credentials:** None (no API access)

**Responsibilities:**
- Detect meeting transcript files
- Classify by file type and naming pattern
- Route to appropriate user-specific processor
- No API calls, no credentials

---

### **Layer 2: User-Specific (Focus Layer)**
**What:** Meeting processing with credentials  
**Where:** `users/{user_id}/{focus}/meeting_automation/`  
**Credentials:** Stored per-user, per-focus

**Responsibilities:**
- Gmail API access (user-specific OAuth)
- Otter.ai credentials (if using unofficial API)
- Meeting summary generation
- Output to user's knowledge base

---

### **Layer 3: MCP Integration**
**What:** Natural language control  
**Where:** `8825_core/integrations/mcp-servers/meeting-automation-mcp/`  
**Credentials:** Proxies to user-specific credentials

**Responsibilities:**
- Goose-compatible interface
- User authentication
- Route commands to user-specific processors
- Status monitoring

---

## 📁 PROPOSED FILE STRUCTURE

```
8825-system/
│
├── INBOX_HUB/
│   └── file_dispatch_system/
│       ├── smart_classifier.py          # ADD: Meeting transcript detection
│       ├── meeting_router.py            # NEW: Route to user processors
│       └── unified_processor.py         # UPDATE: Add meeting routing
│
├── users/
│   └── {user_id}/                       # e.g., justin_harmon
│       ├── hcss/
│       │   ├── meeting_automation/      # NEW: User-specific automation
│       │   │   ├── config.json          # Gmail OAuth, Otter creds
│       │   │   ├── gmail_client.py      # Gmail API wrapper
│       │   │   ├── meeting_processor.py # Process transcripts
│       │   │   ├── summary_generator.py # Generate summaries
│       │   │   └── logs/                # User-specific logs
│       │   │
│       │   └── knowledge/               # EXISTING: Output location
│       │       └── meetings/
│       │           ├── transcripts/
│       │           ├── summaries/
│       │           └── json/
│       │
│       └── jh_assistant/
│           └── meeting_automation/      # Different user, different config
│               └── config.json
│
└── 8825_core/
    └── integrations/
        └── mcp-servers/
            ├── fds-mcp/                 # EXISTING: File dispatch control
            └── meeting-automation-mcp/  # NEW: Meeting automation control
                ├── server.py
                ├── goose_config.yaml
                └── README.md
```

---

## 🔐 CREDENTIAL MANAGEMENT

### **User-Specific Config Structure**

**Location:** `users/{user_id}/{focus}/meeting_automation/config.json`

```json
{
  "user_id": "justin_harmon",
  "focus": "hcss",
  "enabled": true,
  
  "gmail": {
    "enabled": true,
    "credentials_path": "users/justin_harmon/hcss/meeting_automation/gmail_credentials.json",
    "token_path": "users/justin_harmon/hcss/meeting_automation/gmail_token.json",
    "search_query": "from:no-reply@otter.ai subject:TGIF is:unread",
    "poll_interval_minutes": 15
  },
  
  "otter": {
    "enabled": false,
    "email": "",
    "password_keychain_key": "8825_otter_justin_harmon_hcss",
    "note": "Unofficial API - not recommended"
  },
  
  "processing": {
    "auto_process": true,
    "mark_as_read": true,
    "archive_transcripts": true,
    "output_formats": ["json", "markdown", "email"]
  },
  
  "output": {
    "knowledge_base": "users/justin_harmon/hcss/knowledge/meetings/",
    "transcripts_dir": "transcripts/",
    "summaries_dir": "summaries/",
    "json_dir": "json/"
  },
  
  "notifications": {
    "email": "justin@hcss.com",
    "slack_webhook": "",
    "on_success": true,
    "on_error": true
  }
}
```

### **Security Principles**

1. **OAuth Tokens:** Stored in user directory, gitignored
2. **API Keys:** Never in code, use keychain or env vars
3. **Passwords:** Keychain only (macOS Keychain, not plaintext)
4. **Config Files:** User-specific, never shared
5. **Logs:** User-specific, contain no credentials

---

## 🔄 INTEGRATION FLOW

### **Step 1: File Detection (FDS)**

```python
# smart_classifier.py - ADD meeting detection

def _is_meeting_transcript(self, file_path: Path) -> bool:
    """Check if file is a meeting transcript"""
    filename = file_path.name.lower()
    
    # Otter.ai patterns
    if 'otter' in filename and ('.txt' in filename or '.pdf' in filename):
        return True
    
    # Meeting keywords
    meeting_keywords = ['tgif', 'meeting', 'transcript', 'otter']
    if any(keyword in filename for keyword in meeting_keywords):
        ext = file_path.suffix.lower()
        if ext in {'.txt', '.pdf', '.docx'}:
            return True
    
    return False

def classify(self, file_path: Path) -> Dict:
    """Classify file and return routing decision"""
    
    # ... existing code ...
    
    # NEW: Route meeting transcripts
    if self._is_meeting_transcript(file_path):
        return {
            'action': 'meeting',
            'destination': None,  # Determined by user config
            'processor': 'meeting_router',
            'reason': 'Meeting transcript → User-specific processor'
        }
```

---

### **Step 2: User Routing (FDS)**

```python
# meeting_router.py - NEW FILE

class MeetingRouter:
    """Route meeting transcripts to user-specific processors"""
    
    def __init__(self):
        self.users_dir = Path(__file__).parent.parent.parent / "users"
    
    def route(self, file_path: Path) -> bool:
        """
        Route meeting transcript to appropriate user processor
        
        Logic:
        1. Detect which user's inbox this came from
        2. Find user's meeting automation config
        3. If enabled, invoke user's processor
        4. If not enabled, skip
        """
        
        # Detect user from file path
        user_id = self._detect_user(file_path)
        if not user_id:
            self.log(f"Could not detect user for: {file_path}")
            return False
        
        # Find user's meeting automation configs
        user_configs = self._find_user_configs(user_id)
        
        if not user_configs:
            self.log(f"No meeting automation configured for user: {user_id}")
            return False
        
        # Process with each enabled config
        success = False
        for config in user_configs:
            if config.get('enabled'):
                processor = self._get_processor(config)
                if processor.process(file_path):
                    success = True
        
        return success
    
    def _detect_user(self, file_path: Path) -> Optional[str]:
        """Detect user from file path or config"""
        # Check if file is in user's Downloads/Screenshots
        # Match against configured input paths
        # Return user_id
        pass
    
    def _find_user_configs(self, user_id: str) -> List[Dict]:
        """Find all meeting automation configs for user"""
        configs = []
        user_dir = self.users_dir / user_id
        
        # Search all focuses for meeting_automation/config.json
        for focus_dir in user_dir.iterdir():
            if focus_dir.is_dir():
                config_path = focus_dir / "meeting_automation/config.json"
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        config['_path'] = config_path
                        config['_focus'] = focus_dir.name
                        configs.append(config)
        
        return configs
```

---

### **Step 3: User Processing (Focus Layer)**

```python
# users/justin_harmon/hcss/meeting_automation/meeting_processor.py

class MeetingProcessor:
    """User-specific meeting transcript processor"""
    
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.user_id = self.config['user_id']
        self.focus = self.config['focus']
        
        # Initialize Gmail client (user-specific OAuth)
        if self.config['gmail']['enabled']:
            self.gmail = GmailClient(
                credentials_path=self.config['gmail']['credentials_path'],
                token_path=self.config['gmail']['token_path']
            )
        
        # Initialize summary generator
        self.generator = SummaryGenerator(self.config)
    
    def process(self, file_path: Path) -> bool:
        """Process meeting transcript"""
        try:
            # Read transcript
            transcript = self._read_transcript(file_path)
            
            # Generate summary
            summary = self.generator.generate(transcript)
            
            # Save outputs
            self._save_outputs(summary)
            
            # Send notifications
            if self.config['notifications']['on_success']:
                self._send_notification(summary)
            
            # Mark email as read (if from Gmail)
            if self.config['processing']['mark_as_read']:
                self._mark_as_read(file_path)
            
            return True
            
        except Exception as e:
            self.log(f"Error processing {file_path}: {e}")
            if self.config['notifications']['on_error']:
                self._send_error_notification(e)
            return False
    
    def _save_outputs(self, summary: Dict):
        """Save to user's knowledge base"""
        output_dir = Path(self.config['output']['knowledge_base'])
        
        # Save JSON
        json_path = output_dir / self.config['output']['json_dir']
        json_path.mkdir(parents=True, exist_ok=True)
        
        # Save Markdown
        md_path = output_dir / self.config['output']['summaries_dir']
        md_path.mkdir(parents=True, exist_ok=True)
        
        # ... save files ...
```

---

### **Step 4: Gmail Polling (User-Specific)**

```python
# users/justin_harmon/hcss/meeting_automation/gmail_poller.py

class GmailPoller:
    """Poll Gmail for meeting transcripts (user-specific)"""
    
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # User-specific Gmail client
        self.gmail = GmailClient(
            credentials_path=self.config['gmail']['credentials_path'],
            token_path=self.config['gmail']['token_path']
        )
        
        self.processor = MeetingProcessor(config_path)
    
    def poll(self):
        """Poll Gmail for new transcripts"""
        query = self.config['gmail']['search_query']
        
        # Search Gmail
        messages = self.gmail.search(query)
        
        for message in messages:
            # Extract transcript
            transcript = self._extract_transcript(message)
            
            # Save to temp file
            temp_file = self._save_temp(transcript, message)
            
            # Process
            self.processor.process(temp_file)
            
            # Mark as read
            if self.config['processing']['mark_as_read']:
                self.gmail.mark_as_read(message['id'])
    
    def start_polling(self):
        """Start polling loop"""
        interval = self.config['gmail']['poll_interval_minutes']
        
        while True:
            try:
                self.poll()
            except Exception as e:
                self.log(f"Polling error: {e}")
            
            time.sleep(interval * 60)
```

---

## 🎮 MCP INTEGRATION

### **Meeting Automation MCP Server**

**Location:** `8825_core/integrations/mcp-servers/meeting-automation-mcp/`

```python
# server.py

class MeetingAutomationMCP:
    """MCP server for meeting automation control"""
    
    def __init__(self):
        self.users_dir = Path(__file__).parent.parent.parent.parent / "users"
    
    def handle_request(self, method: str, params: dict, user_id: str) -> dict:
        """Handle MCP request (user-authenticated)"""
        
        if method == "meeting/status":
            return self.get_status(user_id, params.get('focus'))
        
        elif method == "meeting/start_polling":
            return self.start_polling(user_id, params.get('focus'))
        
        elif method == "meeting/stop_polling":
            return self.stop_polling(user_id, params.get('focus'))
        
        elif method == "meeting/process_file":
            return self.process_file(user_id, params.get('focus'), params.get('file_path'))
        
        elif method == "meeting/get_recent":
            return self.get_recent_meetings(user_id, params.get('focus'), params.get('limit', 10))
        
        elif method == "meeting/configure":
            return self.configure(user_id, params.get('focus'), params.get('config'))
    
    def get_status(self, user_id: str, focus: str) -> dict:
        """Get meeting automation status for user/focus"""
        config_path = self.users_dir / user_id / focus / "meeting_automation/config.json"
        
        if not config_path.exists():
            return {"status": "not_configured"}
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check if poller is running
        pid_file = config_path.parent / ".poller.pid"
        is_running = pid_file.exists()
        
        return {
            "status": "enabled" if config.get('enabled') else "disabled",
            "polling": is_running,
            "gmail_enabled": config.get('gmail', {}).get('enabled', False),
            "otter_enabled": config.get('otter', {}).get('enabled', False),
            "recent_meetings": self._get_recent_count(user_id, focus)
        }
```

### **Goose Natural Language Commands**

```yaml
# goose_config.yaml

mcpServers:
  meeting-automation:
    command: python3
    args:
      - /path/to/8825_core/integrations/mcp-servers/meeting-automation-mcp/server.py
    env:
      USERS_DIR: /path/to/users
```

**Usage:**
```
goose session start

> What's the status of my HCSS meeting automation?
> Start polling for TGIF meetings
> Show me recent meeting summaries
> Process this transcript: /path/to/file.txt
> Configure HCSS meeting automation
```

---

## 🔧 IMPLEMENTATION PHASES

### **Phase 1: FDS Integration (Week 1)**
**Goal:** Detect and route meeting transcripts

**Tasks:**
1. ✅ Update `smart_classifier.py` - Add meeting detection
2. ✅ Create `meeting_router.py` - Route to user processors
3. ✅ Update `unified_processor.py` - Add meeting routing
4. ✅ Test with sample files

**Deliverables:**
- FDS can detect meeting transcripts
- FDS routes to user-specific processors
- No credentials in FDS layer

---

### **Phase 2: User Layer (Week 2)**
**Goal:** User-specific processing with credentials

**Tasks:**
1. ✅ Create user config structure
2. ✅ Build Gmail client wrapper
3. ✅ Build meeting processor
4. ✅ Build summary generator
5. ✅ Test with Justin's HCSS config

**Deliverables:**
- User-specific meeting automation
- Gmail OAuth working
- Summaries generated
- Saved to knowledge base

---

### **Phase 3: Gmail Polling (Week 3)**
**Goal:** Automated Gmail polling

**Tasks:**
1. ✅ Build Gmail poller
2. ✅ Add scheduling (cron or systemd)
3. ✅ Add error handling
4. ✅ Add notifications
5. ✅ Test end-to-end

**Deliverables:**
- Automated polling every 15 minutes
- Transcripts processed automatically
- Notifications sent
- Logs maintained

---

### **Phase 4: MCP Integration (Week 4)**
**Goal:** Goose control

**Tasks:**
1. ✅ Build MCP server
2. ✅ Add user authentication
3. ✅ Add status monitoring
4. ✅ Add control commands
5. ✅ Test with Goose

**Deliverables:**
- Natural language control
- User-specific access
- Status monitoring
- Configuration management

---

## 🎯 KEY DESIGN DECISIONS

### **1. Why User-Specific Credentials?**

**Problem:** Multiple users, multiple focuses, different Gmail accounts

**Solution:** Store credentials per-user, per-focus
- Justin's HCSS → `users/justin_harmon/hcss/meeting_automation/`
- Justin's JH Assistant → `users/justin_harmon/jh_assistant/meeting_automation/`
- Other users → Their own directories

**Benefits:**
- ✅ Secure (credentials isolated)
- ✅ Scalable (add users easily)
- ✅ Flexible (different configs per focus)
- ✅ Maintainable (no credential conflicts)

---

### **2. Why Dual-Source (Otter API + Gmail)?**

**Decision:** Use BOTH sources with intelligent failover

**Philosophy:** "More sources of information = better"

**Strategy:**
- ✅ **Primary:** Unofficial Otter API (faster, 10 min polling)
- ✅ **Fallback:** Gmail API (reliable, 15 min polling)
- ✅ **Cross-Validation:** Compare results when both work
- ✅ **Auto-Failover:** Switch to Gmail if Otter breaks
- ✅ **Health Monitoring:** Track both sources

**Benefits:**
- ✅ Speed when Otter works
- ✅ Reliability when Otter breaks
- ✅ Validation for confidence
- ✅ Zero downtime
- ✅ Learn from patterns

**See:** `DUAL_SOURCE_MEETING_STRATEGY.md` for complete design

---

### **3. Why Layer Separation?**

**FDS Layer:** System-wide, no credentials
**User Layer:** User-specific, has credentials
**MCP Layer:** Natural language control

**Benefits:**
- ✅ Clear separation of concerns
- ✅ FDS remains credential-free
- ✅ Users can have different configs
- ✅ Easy to add new users
- ✅ Easy to add new focuses

---

### **4. Why Not Consolidate with Existing Ingestion?**

**Existing Ingestion:** `8825_core/workflows/ingestion/`
- Processes JSON/TXT/TXF files
- Routes to projects
- Updates Brain

**Meeting Automation:** Different workflow
- Polls Gmail for transcripts
- Generates summaries
- Saves to knowledge base
- User-specific credentials

**Decision:** Keep separate, different purposes

---

## 📊 COMPARISON: OLD vs NEW

### **Old Approach (Documented but Not Built)**
```
Otter.ai → Gmail → Manual Check → Manual Processing
```
- ❌ Manual intervention required
- ❌ No automation
- ❌ No integration with 8825

---

### **New Approach (Proposed)**
```
Otter.ai → Gmail → FDS Detection → User Processor → Knowledge Base
                                        ↓
                                   MCP Control (Goose)
```
- ✅ Fully automated
- ✅ User-specific credentials
- ✅ Integrated with 8825
- ✅ Natural language control
- ✅ Scalable to multiple users

---

## 🚀 GETTING STARTED

### **For Justin (HCSS)**

**Step 1: Setup Gmail OAuth**
```bash
cd users/justin_harmon/hcss/meeting_automation
python3 setup_gmail.py
# Follow OAuth flow in browser
```

**Step 2: Configure**
```bash
cp config.example.json config.json
nano config.json
# Set search_query, output paths, notifications
```

**Step 3: Test**
```bash
python3 meeting_processor.py --test
```

**Step 4: Start Polling**
```bash
python3 gmail_poller.py --daemon
```

**Step 5: Control with Goose**
```bash
goose session start
> What's my HCSS meeting automation status?
> Start polling for TGIF meetings
```

---

## 🎓 ARCHITECTURE PRINCIPLES

### **1. Credential Isolation**
- Never in system-wide code
- Always in user directories
- Gitignored by default
- Keychain for passwords

### **2. User Scalability**
- Easy to add new users
- Easy to add new focuses
- No conflicts between users
- Independent configurations

### **3. Focus Separation**
- HCSS meetings → HCSS knowledge base
- JH Assistant meetings → JH Assistant knowledge base
- No cross-contamination

### **4. System Integration**
- FDS detects and routes
- User layer processes
- MCP provides control
- All layers work together

---

## 📝 NEXT STEPS

### **Immediate (This Week)**
1. ✅ Review this design
2. ✅ Approve architecture
3. ✅ Create user directory structure
4. ✅ Build Phase 1 (FDS integration)

### **Short Term (Next 2 Weeks)**
1. ✅ Build Phase 2 (User layer)
2. ✅ Setup Gmail OAuth for Justin
3. ✅ Test with real TGIF meetings
4. ✅ Build Phase 3 (Gmail polling)

### **Medium Term (Month 2)**
1. ✅ Build Phase 4 (MCP integration)
2. ✅ Add other users (if needed)
3. ✅ Add other focuses (if needed)
4. ✅ Production deployment

---

## 🎯 SUCCESS CRITERIA

### **Must Have:**
- ✅ FDS detects meeting transcripts
- ✅ User-specific credential storage
- ✅ Gmail OAuth working
- ✅ Automated polling
- ✅ Summaries generated
- ✅ Saved to knowledge base
- ✅ Goose control

### **Nice to Have:**
- ⭐ Multiple users supported
- ⭐ Multiple focuses per user
- ⭐ Slack notifications
- ⭐ Web dashboard
- ⭐ Historical analysis

---

**Status:** Ready for review and approval  
**Next:** Implement Phase 1 (FDS integration)  
**Timeline:** 4 weeks to production
