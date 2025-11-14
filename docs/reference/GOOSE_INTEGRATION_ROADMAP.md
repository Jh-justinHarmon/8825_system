# Goose MCP Integration Roadmap

**Date:** 2025-11-09  
**Current State:** Infrastructure ready, integration needed  
**Goal:** Full Goose orchestration of 8825 workflows

---

## Current State Analysis

### ✅ What We Have

**Infrastructure:**
- ✅ Goose CLI installed (`/opt/homebrew/bin/goose`)
- ✅ 3 MCP servers built (HCSS, Joju, JH Assistant)
- ✅ MCP servers auto-start on login (LaunchAgent)
- ✅ Inbox processing pipeline (automated hourly)
- ✅ Two-lane ingestion engine (Lane A/B)
- ✅ File type support (JSON, TXT, MD, DOCX)
- ✅ Auto-dependency checking

**Workflows:**
- ✅ Downloads sync (iCloud ↔ Local)
- ✅ Screenshot capture & OCR
- ✅ Brain transport sync
- ✅ File processing & archiving
- ✅ Teaching ticket generation

**Documentation:**
- ✅ Integration pattern defined
- ✅ Task spec format documented
- ✅ MCP bridge architecture designed
- ✅ Usage patterns identified

### 🔲 What's Missing

**Goose Integration:**
- ❌ Goose not configured for 8825 workspace
- ❌ MCP servers not exposed to Goose
- ❌ No Goose-compatible tools defined
- ❌ No task spec generator
- ❌ No Goose session templates

**Bridge Layer:**
- ❌ Current MCPs are Flask-based (not MCP SDK)
- ❌ No stdio transport for Goose
- ❌ Tools not registered in MCP format
- ❌ No Goose config file

---

## Gap Analysis

### Problem 1: MCP Server Format Mismatch
**Current:** Flask REST APIs (ports 8826-8828)  
**Needed:** MCP SDK with stdio transport  
**Impact:** Goose can't communicate with current servers

### Problem 2: No Goose Configuration
**Current:** Goose installed but not configured  
**Needed:** `~/.config/goose/config.json` with MCP servers  
**Impact:** Goose doesn't know about 8825 tools

### Problem 3: Missing Task Spec Layer
**Current:** Direct script execution  
**Needed:** JSON task specs for Goose  
**Impact:** Can't orchestrate complex workflows

### Problem 4: No Goose Session Context
**Current:** Goose has no 8825 context  
**Needed:** Session templates with workspace context  
**Impact:** Goose doesn't understand 8825 structure

---

## Integration Path

### Phase 1: Bridge the Gap (Immediate)
**Goal:** Make current MCPs Goose-compatible

**Tasks:**
1. **Convert MCP Servers to SDK Format**
   - Replace Flask with `@modelcontextprotocol/sdk`
   - Add stdio transport
   - Keep existing tool logic

2. **Register Tools in MCP Format**
   - Define tool schemas
   - Implement tool handlers
   - Return structured responses

3. **Configure Goose**
   - Create `~/.config/goose/config.json`
   - Register 3 MCP servers
   - Test basic connection

**Deliverable:** Goose can call existing 8825 tools

---

### Phase 2: Task Orchestration (Short-term)
**Goal:** Enable complex workflow orchestration

**Tasks:**
1. **Build Task Spec Generator**
   - Create templates for common tasks
   - Generate JSON specs from intent
   - Validate before execution

2. **Create Goose Session Templates**
   - 8825 workspace context
   - Available tools reference
   - Common workflow patterns

3. **Implement Core Workflows**
   - Process inbox → Generate task spec → Execute via Goose
   - Review teaching tickets → Generate approval spec → Execute
   - Mine chat logs → Generate integration spec → Execute

**Deliverable:** Goose orchestrates multi-step 8825 workflows

---

### Phase 3: Intelligence Layer (Medium-term)
**Goal:** Goose learns and optimizes 8825 workflows

**Tasks:**
1. **Add Learning Feedback Loop**
   - Track task success/failure
   - Learn from corrections
   - Suggest optimizations

2. **Build Monitoring Dashboard**
   - Real-time workflow status
   - Success metrics
   - Error patterns

3. **Implement Predictive Routing**
   - Learn from routing decisions
   - Suggest improvements
   - Auto-correct common errors

**Deliverable:** Self-improving 8825 system

---

## Recommended Implementation

### Option A: Hybrid Approach (Recommended)
**Keep current MCPs for Windsurf, add Goose bridge**

```
Windsurf (Cascade)
    ↓
Current Flask MCPs (8826-8828)
    ↓
8825 Scripts

Goose CLI
    ↓
New MCP SDK Bridge (stdio)
    ↓
Same 8825 Scripts
```

**Pros:**
- No disruption to current automation
- Goose integration is additive
- Can test incrementally

**Cons:**
- Maintain two MCP implementations
- Some duplication

---

### Option B: Full Migration
**Replace Flask MCPs with MCP SDK**

```
Windsurf (Cascade) + Goose CLI
    ↓
Unified MCP SDK Servers (stdio + HTTP)
    ↓
8825 Scripts
```

**Pros:**
- Single implementation
- Cleaner architecture
- Better long-term

**Cons:**
- Requires migration of current MCPs
- Risk of breaking current automation
- More upfront work

---

## Immediate Next Steps

### 1. Quick Win: Goose Session in 8825 Workspace
```bash
cd "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system"
goose session start
```

**Test:**
- "Analyze the inbox processing pipeline"
- "Explain the two-lane ingestion system"
- "Review the MCP server architecture"

**Benefit:** Goose has full 8825 context immediately

---

### 2. Build Minimal MCP Bridge (2-3 hours)
**Create:** `8825_core/integrations/goose/mcp-bridge/`

**Tools to implement:**
1. `process_inbox` - Trigger pipeline
2. `check_status` - Get system status
3. `review_tickets` - List teaching tickets
4. `ocr_screenshot` - Process latest screenshot

**Config:**
```json
{
  "mcpServers": {
    "8825-bridge": {
      "command": "node",
      "args": ["/path/to/8825_core/integrations/goose/mcp-bridge/server.js"]
    }
  }
}
```

---

### 3. Create Task Spec Templates (1 hour)
**Location:** `8825_core/integrations/goose/task_specs/`

**Templates:**
- `process_inbox.json`
- `review_ticket.json`
- `update_library.json`
- `mine_chat.json`

**Usage:**
```bash
# Generate spec
python3 generate_task_spec.py --template process_inbox --output task.json

# Execute via Goose
goose session
> "Execute the task spec in task.json"
```

---

## Success Metrics

### Phase 1 (Week 1)
- [ ] Goose can list 8825 tools
- [ ] Goose can trigger inbox processing
- [ ] Goose can check system status
- [ ] Goose has 8825 workspace context

### Phase 2 (Week 2-3)
- [ ] Goose orchestrates multi-step workflows
- [ ] Task specs generated automatically
- [ ] Teaching tickets reviewed via Goose
- [ ] Chat mining automated

### Phase 3 (Month 2)
- [ ] Goose learns from corrections
- [ ] Predictive routing implemented
- [ ] Self-optimization active
- [ ] Monitoring dashboard live

---

## Architecture Decision

### Recommendation: **Hybrid Approach (Option A)**

**Why:**
1. **Low risk** - Current automation keeps working
2. **Incremental** - Test Goose without breaking things
3. **Flexible** - Can migrate later if needed
4. **Fast** - Can start using Goose today

**Implementation:**
1. Keep Flask MCPs for Windsurf (already working)
2. Build new MCP SDK bridge for Goose (small, focused)
3. Both call same 8825 scripts (no duplication)
4. Test Goose integration safely

---

## Quick Start Guide

### Today (30 minutes)
```bash
# 1. Test Goose in workspace
cd "/path/to/8825/8825-system"
goose session start

# 2. Ask Goose about 8825
> "Analyze the structure of this 8825 workspace"
> "Explain the inbox processing pipeline"
> "What MCP servers are available?"

# 3. Verify Goose understands context
> "List all the Python scripts in 8825_core/inbox/"
> "Explain what simple_sync_and_process.sh does"
```

### This Week (2-3 hours)
1. Build minimal MCP bridge (4 tools)
2. Configure Goose to use bridge
3. Test basic orchestration
4. Document usage patterns

### Next Week (4-6 hours)
1. Create task spec templates
2. Build spec generator
3. Implement 3-4 key workflows
4. Add session templates

---

## Summary

**Current State:** Infrastructure ready, missing Goose integration layer

**Gap:** MCP format mismatch + no Goose configuration

**Path:** Hybrid approach - add Goose bridge, keep current MCPs

**Timeline:**
- **Today:** Goose has 8825 context
- **Week 1:** Basic tool orchestration
- **Week 2-3:** Complex workflows
- **Month 2:** Self-optimization

**Next Action:** Start Goose session in 8825 workspace and test context awareness

---

**Ready to start with Goose session test?**
