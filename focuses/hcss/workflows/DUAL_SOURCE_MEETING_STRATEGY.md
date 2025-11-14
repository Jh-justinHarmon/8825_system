# Dual-Source Meeting Automation Strategy

**Date:** November 11, 2025  
**Philosophy:** More sources = Better information  
**Approach:** Unofficial Otter API (Primary) + Gmail API (Fallback + Validation)

---

## 🎯 CORE PHILOSOPHY

**"The more sources of information, the better"**

Instead of choosing one or the other, use **BOTH**:
1. **Primary:** Unofficial Otter API (faster, direct access)
2. **Fallback:** Gmail API (reliable, official)
3. **Validation:** Cross-check between sources
4. **Resilience:** Automatic failover if primary breaks

---

## 🏗️ DUAL-SOURCE ARCHITECTURE

### **Strategy: Primary + Fallback + Validation**

```
┌─────────────────────────────────────────────────────────┐
│  Meeting Happens → Otter.ai Transcribes                 │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                   ↓
┌──────────────────┐              ┌──────────────────┐
│  Unofficial API  │              │  Gmail API       │
│  (Primary)       │              │  (Fallback)      │
│  - Faster        │              │  - Reliable      │
│  - Direct        │              │  - Official      │
│  - More formats  │              │  - Stable        │
└──────────────────┘              └──────────────────┘
        ↓                                   ↓
        └─────────────────┬─────────────────┘
                          ↓
              ┌───────────────────────┐
              │  Dual-Source Manager  │
              │  - Try primary first  │
              │  - Fall back if fails │
              │  - Cross-validate     │
              │  - Health monitoring  │
              └───────────────────────┘
                          ↓
                  Meeting Processor
```

---

## 🔧 IMPLEMENTATION

### **User Config (Enhanced)**

**Location:** `users/{user_id}/{focus}/meeting_automation/config.json`

```json
{
  "user_id": "justin_harmon",
  "focus": "hcss",
  "enabled": true,
  
  "strategy": {
    "mode": "dual_source",
    "primary": "otter_api",
    "fallback": "gmail",
    "cross_validate": true,
    "prefer_primary": true
  },
  
  "otter_api": {
    "enabled": true,
    "email": "justin@hcss.com",
    "password_keychain_key": "8825_otter_justin_harmon_hcss",
    "poll_interval_minutes": 10,
    "formats": ["txt", "pdf"],
    "note": "Unofficial API - faster but may break"
  },
  
  "gmail": {
    "enabled": true,
    "credentials_path": "users/justin_harmon/hcss/meeting_automation/gmail_credentials.json",
    "token_path": "users/justin_harmon/hcss/meeting_automation/gmail_token.json",
    "search_query": "from:no-reply@otter.ai subject:TGIF is:unread",
    "poll_interval_minutes": 15,
    "note": "Official API - reliable fallback"
  },
  
  "health_monitoring": {
    "enabled": true,
    "check_interval_minutes": 5,
    "failure_threshold": 3,
    "auto_failover": true,
    "alert_on_failover": true
  },
  
  "validation": {
    "cross_check": true,
    "prefer_source": "otter_api",
    "mismatch_action": "log_and_use_primary",
    "mismatch_alert": true
  }
}
```

---

## 🎮 DUAL-SOURCE MANAGER

### **Core Logic**

```python
# users/justin_harmon/hcss/meeting_automation/dual_source_manager.py

class DualSourceManager:
    """Manage dual-source meeting transcript retrieval"""
    
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize both sources
        self.otter = OtterAPIClient(self.config['otter_api']) if self.config['otter_api']['enabled'] else None
        self.gmail = GmailClient(self.config['gmail']) if self.config['gmail']['enabled'] else None
        
        # Health tracking
        self.health = {
            'otter_api': {'status': 'unknown', 'failures': 0, 'last_success': None},
            'gmail': {'status': 'unknown', 'failures': 0, 'last_success': None}
        }
        
        self.current_source = self.config['strategy']['primary']
    
    def get_transcripts(self) -> List[Dict]:
        """
        Get transcripts using dual-source strategy
        
        Strategy:
        1. Try primary source (Otter API)
        2. If fails, try fallback (Gmail)
        3. If cross_validate enabled, compare results
        4. Return best result
        """
        
        primary_result = None
        fallback_result = None
        
        # Try primary source
        if self.current_source == 'otter_api' and self.otter:
            try:
                primary_result = self._get_from_otter()
                self._mark_success('otter_api')
                
            except Exception as e:
                self.log(f"Otter API failed: {e}", "WARN")
                self._mark_failure('otter_api')
                
                # Auto-failover if threshold reached
                if self._should_failover('otter_api'):
                    self._failover_to('gmail')
        
        # Try fallback (always, if cross_validate enabled)
        if self.config['validation']['cross_check'] or not primary_result:
            if self.gmail:
                try:
                    fallback_result = self._get_from_gmail()
                    self._mark_success('gmail')
                    
                except Exception as e:
                    self.log(f"Gmail API failed: {e}", "ERROR")
                    self._mark_failure('gmail')
        
        # Return best result
        return self._select_best_result(primary_result, fallback_result)
    
    def _get_from_otter(self) -> List[Dict]:
        """Get transcripts from Otter API"""
        speeches = self.otter.get_speeches()
        
        # Filter for TGIF meetings
        tgif_speeches = [s for s in speeches if 'TGIF' in s.title]
        
        transcripts = []
        for speech in tgif_speeches:
            # Check if already processed
            if self._is_processed(speech.id, 'otter_api'):
                continue
            
            # Download transcript
            transcript = self.otter.download_speech(
                speech.id,
                format='txt'
            )
            
            transcripts.append({
                'source': 'otter_api',
                'id': speech.id,
                'title': speech.title,
                'date': speech.date,
                'transcript': transcript,
                'metadata': {
                    'duration': speech.duration,
                    'participants': speech.participants
                }
            })
        
        return transcripts
    
    def _get_from_gmail(self) -> List[Dict]:
        """Get transcripts from Gmail"""
        query = self.config['gmail']['search_query']
        messages = self.gmail.search(query)
        
        transcripts = []
        for message in messages:
            # Check if already processed
            if self._is_processed(message['id'], 'gmail'):
                continue
            
            # Extract transcript from email
            transcript = self._extract_from_email(message)
            
            transcripts.append({
                'source': 'gmail',
                'id': message['id'],
                'title': self._extract_title(message),
                'date': message['date'],
                'transcript': transcript,
                'metadata': {
                    'email_id': message['id'],
                    'subject': message['subject']
                }
            })
        
        return transcripts
    
    def _select_best_result(self, primary: List[Dict], fallback: List[Dict]) -> List[Dict]:
        """
        Select best result from primary and fallback
        
        Logic:
        1. If only one source has results, use it
        2. If both have results, cross-validate
        3. If mismatch, use preferred source
        4. Log any discrepancies
        """
        
        # Only primary has results
        if primary and not fallback:
            return primary
        
        # Only fallback has results
        if fallback and not primary:
            self.log("Using fallback source (primary failed)", "WARN")
            return fallback
        
        # Both have results - cross-validate
        if primary and fallback:
            if self.config['validation']['cross_check']:
                mismatches = self._cross_validate(primary, fallback)
                
                if mismatches:
                    self.log(f"Cross-validation found {len(mismatches)} mismatches", "WARN")
                    
                    if self.config['validation']['mismatch_alert']:
                        self._send_mismatch_alert(mismatches)
            
            # Use preferred source
            preferred = self.config['validation']['prefer_source']
            if preferred == 'otter_api':
                return primary
            else:
                return fallback
        
        # Neither has results
        return []
    
    def _cross_validate(self, primary: List[Dict], fallback: List[Dict]) -> List[Dict]:
        """
        Cross-validate results from both sources
        
        Returns list of mismatches
        """
        mismatches = []
        
        # Match by title/date
        for p in primary:
            # Find matching fallback
            matches = [f for f in fallback if self._is_same_meeting(p, f)]
            
            if not matches:
                mismatches.append({
                    'type': 'missing_in_fallback',
                    'primary': p,
                    'fallback': None
                })
            elif len(matches) > 1:
                mismatches.append({
                    'type': 'multiple_matches',
                    'primary': p,
                    'fallback': matches
                })
            else:
                # Compare content
                if not self._content_matches(p, matches[0]):
                    mismatches.append({
                        'type': 'content_mismatch',
                        'primary': p,
                        'fallback': matches[0]
                    })
        
        # Check for meetings in fallback not in primary
        for f in fallback:
            matches = [p for p in primary if self._is_same_meeting(f, p)]
            if not matches:
                mismatches.append({
                    'type': 'missing_in_primary',
                    'primary': None,
                    'fallback': f
                })
        
        return mismatches
    
    def _mark_failure(self, source: str):
        """Mark source as failed"""
        self.health[source]['failures'] += 1
        self.health[source]['status'] = 'degraded'
        
        self.log(f"{source} failure count: {self.health[source]['failures']}", "WARN")
    
    def _mark_success(self, source: str):
        """Mark source as successful"""
        self.health[source]['failures'] = 0
        self.health[source]['status'] = 'healthy'
        self.health[source]['last_success'] = datetime.now()
    
    def _should_failover(self, source: str) -> bool:
        """Check if should failover to fallback"""
        if not self.config['health_monitoring']['auto_failover']:
            return False
        
        threshold = self.config['health_monitoring']['failure_threshold']
        failures = self.health[source]['failures']
        
        return failures >= threshold
    
    def _failover_to(self, source: str):
        """Failover to different source"""
        old_source = self.current_source
        self.current_source = source
        
        self.log(f"FAILOVER: {old_source} → {source}", "WARN")
        
        if self.config['health_monitoring']['alert_on_failover']:
            self._send_failover_alert(old_source, source)
    
    def get_health_status(self) -> Dict:
        """Get health status of both sources"""
        return {
            'current_source': self.current_source,
            'otter_api': self.health['otter_api'],
            'gmail': self.health['gmail'],
            'auto_failover_enabled': self.config['health_monitoring']['auto_failover']
        }
```

---

## 🎯 BENEFITS OF DUAL-SOURCE

### **1. Resilience**
- ✅ If Otter API breaks, Gmail keeps working
- ✅ Automatic failover
- ✅ No downtime

### **2. Speed**
- ✅ Otter API is faster (10 min polling)
- ✅ Gmail is slower but reliable (15 min polling)
- ✅ Get transcripts faster when primary works

### **3. Validation**
- ✅ Cross-check results
- ✅ Detect discrepancies
- ✅ Alert on mismatches
- ✅ More confidence in data

### **4. Flexibility**
- ✅ More transcript formats (Otter: txt, pdf, docx, srt)
- ✅ More metadata (Otter: duration, participants)
- ✅ Richer data when available

### **5. Learning**
- ✅ Monitor which source is more reliable
- ✅ Track failure patterns
- ✅ Optimize over time

---

## 📊 OPERATIONAL MODES

### **Mode 1: Dual-Source (Recommended)**
```json
{
  "strategy": {
    "mode": "dual_source",
    "primary": "otter_api",
    "fallback": "gmail",
    "cross_validate": true
  }
}
```

**How it works:**
1. Try Otter API first (faster)
2. If fails, use Gmail (reliable)
3. Cross-validate when both work
4. Alert on mismatches

**Best for:** Production use

---

### **Mode 2: Primary Only (Risky)**
```json
{
  "strategy": {
    "mode": "primary_only",
    "primary": "otter_api",
    "fallback": null,
    "cross_validate": false
  }
}
```

**How it works:**
1. Only use Otter API
2. No fallback
3. Fails if API breaks

**Best for:** Testing, when you want speed

---

### **Mode 3: Fallback Only (Safe)**
```json
{
  "strategy": {
    "mode": "fallback_only",
    "primary": "gmail",
    "fallback": null,
    "cross_validate": false
  }
}
```

**How it works:**
1. Only use Gmail API
2. No unofficial API
3. Slower but stable

**Best for:** When Otter API is broken

---

### **Mode 4: Validation Mode (Paranoid)**
```json
{
  "strategy": {
    "mode": "dual_source",
    "primary": "otter_api",
    "fallback": "gmail",
    "cross_validate": true,
    "require_both": true
  }
}
```

**How it works:**
1. Require both sources to agree
2. Alert if any mismatch
3. Don't process if mismatch

**Best for:** Critical meetings, high stakes

---

## 🔄 FAILOVER SCENARIOS

### **Scenario 1: Otter API Breaks**
```
1. Otter API fails 3 times
2. Auto-failover to Gmail
3. Alert sent: "Failover to Gmail"
4. Continue processing with Gmail
5. Retry Otter API every hour
6. Failback when Otter recovers
```

### **Scenario 2: Both Sources Fail**
```
1. Otter API fails
2. Gmail API fails
3. Alert sent: "All sources down"
4. Queue for retry
5. Retry every 15 minutes
6. Resume when any source recovers
```

### **Scenario 3: Cross-Validation Mismatch**
```
1. Otter API returns transcript A
2. Gmail API returns transcript B
3. Content differs
4. Alert sent: "Mismatch detected"
5. Use preferred source (Otter)
6. Log both for manual review
```

---

## 📈 HEALTH MONITORING

### **Dashboard View**
```
Meeting Automation Health
─────────────────────────────────────────
Current Source: otter_api
Status: Healthy

Otter API:
├─ Status: ✅ Healthy
├─ Failures: 0
├─ Last Success: 2 minutes ago
└─ Uptime: 99.8%

Gmail API:
├─ Status: ✅ Healthy
├─ Failures: 0
├─ Last Success: 5 minutes ago
└─ Uptime: 100%

Recent Activity:
├─ 10:30 AM - Transcript retrieved (otter_api)
├─ 10:35 AM - Cross-validation passed
├─ 10:40 AM - Transcript retrieved (otter_api)
└─ 10:45 AM - Cross-validation passed

Failover History:
└─ None (all systems operational)
```

---

## 🎮 MCP COMMANDS

### **Enhanced Commands**

```bash
goose session start

# Status with dual-source info
> What's my HCSS meeting automation status?
{
  "current_source": "otter_api",
  "otter_api": {"status": "healthy", "failures": 0},
  "gmail": {"status": "healthy", "failures": 0},
  "recent_meetings": 5
}

# Force source switch
> Switch HCSS meetings to Gmail source
> Switch HCSS meetings to Otter API source

# Health check
> Check HCSS meeting automation health

# Manual failover
> Failover HCSS meetings to Gmail

# Cross-validation report
> Show HCSS meeting validation mismatches
```

---

## 🎯 UPDATED IMPLEMENTATION

### **Phase 1: FDS Integration (Week 1)**
- Same as before (no changes)

### **Phase 2: User Layer (Week 2)**
- ✅ Build Gmail client
- ✅ Build Otter API client (NEW)
- ✅ Build dual-source manager (NEW)
- ✅ Build meeting processor

### **Phase 3: Dual-Source Polling (Week 3)**
- ✅ Build dual-source poller
- ✅ Add health monitoring (NEW)
- ✅ Add cross-validation (NEW)
- ✅ Add auto-failover (NEW)

### **Phase 4: MCP Integration (Week 4)**
- ✅ Add dual-source status
- ✅ Add source switching
- ✅ Add health monitoring
- ✅ Add validation reports

---

## 🎓 PHILOSOPHY ALIGNMENT

### **"More Sources = Better Information"**

**Traditional Approach:**
- Choose one source
- Hope it doesn't break
- Manual intervention if it fails

**8825 Approach:**
- Use multiple sources
- Automatic failover
- Cross-validation
- Learn from patterns
- Resilient by design

**Benefits:**
1. ✅ **Resilience:** Never goes down
2. ✅ **Speed:** Use fastest when available
3. ✅ **Validation:** Cross-check results
4. ✅ **Learning:** Track what works
5. ✅ **Flexibility:** Switch sources easily

---

## 📊 RISK MITIGATION

### **Otter API Risks (Mitigated)**
- ❌ **Risk:** Unofficial API breaks
- ✅ **Mitigation:** Auto-failover to Gmail
- ✅ **Impact:** Zero downtime

### **Gmail API Risks (Mitigated)**
- ❌ **Risk:** 15 minute delay
- ✅ **Mitigation:** Use Otter API for speed
- ✅ **Impact:** Get transcripts faster

### **Both Sources Fail (Mitigated)**
- ❌ **Risk:** Both APIs down
- ✅ **Mitigation:** Queue and retry
- ✅ **Impact:** Process when recovered

---

## 🎯 SUCCESS CRITERIA (Updated)

### **Must Have:**
- ✅ Dual-source retrieval working
- ✅ Automatic failover
- ✅ Health monitoring
- ✅ Cross-validation
- ✅ User-specific credentials
- ✅ Goose control

### **Nice to Have:**
- ⭐ Validation dashboard
- ⭐ Failure pattern analysis
- ⭐ Auto-recovery testing
- ⭐ Performance metrics

---

## 📝 UPDATED DESIGN SUMMARY

**Old Design:** Choose Gmail OR Otter API  
**New Design:** Use BOTH with intelligent failover

**Key Changes:**
1. ✅ Dual-source manager
2. ✅ Health monitoring
3. ✅ Auto-failover
4. ✅ Cross-validation
5. ✅ Source switching

**Philosophy:** Embrace redundancy for resilience

---

**Status:** Design updated to dual-source strategy  
**Next:** Implement dual-source manager  
**Timeline:** Still 4 weeks (same phases, enhanced features)
