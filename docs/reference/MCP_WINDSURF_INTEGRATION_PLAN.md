# MCP Windsurf Integration Plan
**Date:** 2025-11-16  
**Status:** Ready for Execution  
**Goal:** Full production integration of all MCP servers into Windsurf with E2E testing

---

## Executive Summary

**Current State:**
- 9 MCP servers centralized in `~/mcp_servers/`
- No Windsurf-specific MCP configuration found
- Servers currently configured for Goose only (`~/.config/goose/profiles.yaml`)
- MCP registry exists but not connected to Windsurf

**Target State:**
- All 9 MCP servers accessible from Windsurf/Cascade
- Windsurf MCP configuration established
- E2E tested and production-ready
- New MCP creation protocol documented

**Timeline:** 3-4 hours total (including testing)

---

## Phase 0: Discovery & Baseline (COMPLETE ✅)

### 0.1 Windsurf MCP Configuration Location
**Status:** DISCOVERED

**Findings:**
- Windsurf uses Cascade MCP system (visible in current session)
- MCP servers available: `8825-pattern-engine`, `dli-router`
- Configuration likely in Windsurf settings or workspace-specific files
- No `.windsurf/` directory in workspace
- Global Windsurf settings at `~/Library/Application Support/Windsurf/User/settings.json` (currently only git settings)

**Next:** Determine how to add MCP servers to Windsurf's configuration

### 0.2 Current MCP Inventory
**Location:** `~/mcp_servers/`

| Server | Entry | Language | Status | Tools |
|--------|-------|----------|--------|-------|
| 8825-core | server.py | Python | ✅ Present | Multiple (8825 system access) |
| hcss-bridge | server.js | Node | ✅ Present | 5 (Gmail, Otter, routing) |
| figma-make-transformer | server.js | Node | ✅ Present | 5 (Figma → Joju) |
| figjam | server.js | Node | ✅ Present | Multiple (FigJam integration) |
| otter-integration | server.py | Python | ✅ Present | Multiple (Otter.ai) |
| fds | server.py | Python | ✅ Present | Multiple (FDS) |
| meeting-automation | server.py | Python | ✅ Present | Multiple (meetings) |
| ral-portal | server.py | Python | ✅ Present | Multiple (RAL) |
| customer-platform | server.js | Node | ✅ Present | Multiple (customers) |

**All 9 servers confirmed present in centralized location.**

### 0.3 MCP Bridge Decision
**Location:** `8825_core/integrations/goose/mcp-bridge/server.py`

**Analysis:**
- 12 tools (process_inbox, check_status, list_tasks, etc.)
- Specifically built for Goose integration
- Aggregates multiple 8825 functions into single interface
- Used by Matthew Galley (MG) via Goose

**Decision:** **KEEP SEPARATE for Goose**
- Rationale: MCP bridge is Goose-specific and serves MG's workflow
- For Windsurf: Use individual MCP servers directly
- Benefits: More granular control, better tool discovery, no Goose assumptions

---

## Phase 1: Windsurf MCP Configuration Setup

### 1.1 Identify Configuration Method
**Gate:** Determine how Windsurf loads MCP servers

**Actions:**
1. Check Windsurf documentation/help for MCP configuration
2. Search for:
   - Workspace settings (`.vscode/settings.json` equivalent)
   - User settings MCP section
   - Extension/plugin system
   - Command palette MCP commands

**Validation:**
- [ ] Configuration location identified
- [ ] Configuration format documented
- [ ] Test adding one MCP server successfully

**Time:** 30 minutes

**Blockers:**
- If no MCP configuration found → Research Windsurf MCP system architecture
- If different from expected → Adjust plan for Windsurf-specific approach

### 1.2 Create Baseline Configuration Template
**Gate:** 1.1 must be complete

**Deliverable:** Template file for Windsurf MCP configuration

**Example Structure (adjust based on 1.1):**
```json
{
  "mcp.servers": {
    "8825-core": {
      "command": "python3",
      "args": ["/Users/justinharmon/mcp_servers/8825-core/server.py"],
      "cwd": "/Users/justinharmon/mcp_servers/8825-core",
      "env": {}
    }
  }
}
```

**Validation:**
- [ ] Template created
- [ ] Syntax validated
- [ ] One test server added successfully

**Time:** 15 minutes

---

## Phase 2: Server-by-Server Integration

### 2.1 Priority Tier 1: Core System Servers (1 hour)

**Servers:** `8825-core`, `hcss-bridge`

**For Each Server:**

#### Step 1: Add to Configuration
```json
{
  "8825-core": {
    "command": "python3",
    "args": ["/Users/justinharmon/mcp_servers/8825-core/server.py"],
    "cwd": "/Users/justinharmon/mcp_servers/8825-core"
  }
}
```

#### Step 2: Verify Dependencies
```bash
cd ~/mcp_servers/8825-core
# Python
ls requirements.txt && pip3 list | grep -f requirements.txt
# Node
ls package.json && npm list --depth=0
```

**Validation:**
- [ ] All dependencies installed
- [ ] No missing modules

#### Step 3: Test Server Launch
**Action:** Restart Windsurf or reload window

**Expected:** Server appears in MCP server list

**Validation:**
- [ ] Server listed in Windsurf
- [ ] No error messages in output
- [ ] Server status shows "connected" or "ready"

#### Step 4: Test Tool Discovery
**Action:** Use Windsurf command palette or MCP tools interface

**Expected:** All server tools visible

**Validation:**
- [ ] Tools listed correctly
- [ ] Tool descriptions visible
- [ ] Input schemas accessible

#### Step 5: Execute Meaningful Tool Call
**8825-core test:**
```
Tool: search_entities
Input: {"query": "joju", "fuzzy": true}
Expected: Returns entities related to Joju project
```

**hcss-bridge test:**
```
Tool: check_status
Input: {}
Expected: Returns HCSS system status
```

**Validation:**
- [ ] Tool executes without error
- [ ] Returns expected data structure
- [ ] Response time < 5 seconds
- [ ] No path/permission errors

**Gate:** Both Tier 1 servers must pass all 5 steps before proceeding

---

### 2.2 Priority Tier 2: Automation Servers (45 minutes)

**Servers:** `figma-make-transformer`, `otter-integration`, `meeting-automation`

**Process:** Same 5-step process as Tier 1

**Test Cases:**

**figma-make-transformer:**
```
Tool: list_icon_mappings
Input: {}
Expected: Returns icon mapping table
```

**otter-integration:**
```
Tool: list_recent_transcripts
Input: {"limit": 5}
Expected: Returns recent Otter transcripts
```

**meeting-automation:**
```
Tool: check_inbox
Input: {}
Expected: Returns pending meeting files
```

**Gate:** All 3 Tier 2 servers must pass before proceeding

---

### 2.3 Priority Tier 3: Specialized Servers (45 minutes)

**Servers:** `figjam`, `fds`, `ral-portal`, `customer-platform`

**Process:** Same 5-step process

**Test Cases:**

**figjam:**
```
Tool: list_boards (or equivalent)
Input: {}
Expected: Returns FigJam boards or status
```

**fds:**
```
Tool: check_connection (or equivalent)
Input: {}
Expected: Returns FDS connection status
```

**ral-portal:**
```
Tool: get_status (or equivalent)
Input: {}
Expected: Returns RAL portal status
```

**customer-platform:**
```
Tool: list_customers (or equivalent)
Input: {}
Expected: Returns customer list or status
```

**Gate:** All 4 Tier 3 servers must pass before proceeding to Phase 3

---

## Phase 3: End-to-End Integration Testing

### 3.1 Cross-Server Workflow Test (30 minutes)

**Scenario 1: Meeting Processing Workflow**
```
1. Use hcss-bridge → check_status
2. Use otter-integration → list_recent_transcripts
3. Use meeting-automation → process_transcript
4. Use 8825-core → search_entities (verify ingestion)
```

**Validation:**
- [ ] All 4 tools execute in sequence
- [ ] Data flows between tools correctly
- [ ] No errors or timeouts
- [ ] Final state verifiable in 8825 system

**Scenario 2: Development Workflow**
```
1. Use figma-make-transformer → list_icon_mappings
2. Use figma-make-transformer → transform_component
3. Verify transformed files in target location
```

**Validation:**
- [ ] Transformation completes
- [ ] Files created in correct location
- [ ] No path errors

### 3.2 Error Handling Test (20 minutes)

**Test Cases:**
1. **Invalid input:** Call tool with malformed JSON
2. **Missing dependency:** Temporarily rename a required file
3. **Permission error:** Test with read-only directory
4. **Timeout:** Test with slow/hanging operation

**Validation:**
- [ ] Errors reported clearly
- [ ] No crashes or hangs
- [ ] Error messages actionable
- [ ] System recovers gracefully

### 3.3 Performance Test (15 minutes)

**Test:**
- Call same tool 10 times in rapid succession
- Measure response times
- Monitor resource usage

**Validation:**
- [ ] Response times consistent (< 5s)
- [ ] No memory leaks
- [ ] No file descriptor leaks
- [ ] CPU usage reasonable

**Gate:** All E2E tests must pass before production deployment

---

## Phase 4: Production Deployment

### 4.1 Finalize Configuration (15 minutes)

**Actions:**
1. Review all 9 server configurations
2. Verify all paths are absolute
3. Add descriptive names/comments
4. Set appropriate environment variables (if needed)
5. Save configuration

**Validation:**
- [ ] All 9 servers configured
- [ ] Configuration backed up
- [ ] No placeholder values
- [ ] Restart Windsurf successfully

### 4.2 Update Documentation (30 minutes)

**Files to Create/Update:**

1. **`~/mcp_servers/WINDSURF_INTEGRATION.md`**
   - How Windsurf accesses MCP servers
   - Configuration location
   - How to add new servers
   - Troubleshooting guide

2. **`~/mcp_servers/README.md`** (update)
   - Add Windsurf section
   - Update Quick Start for Windsurf
   - Add example tool calls from Windsurf

3. **`8825_core/system/LAUNCH_8825_MODE.md`** (update)
   - Add MCP server status check for Windsurf
   - Document which MCPs work with Windsurf vs Goose

4. **Update `mcp_registry.json`**
   - Add `windsurf_compatible: true` flag to each server
   - Add last_tested timestamps

**Validation:**
- [ ] All docs created/updated
- [ ] Examples tested and verified
- [ ] Links between docs correct
- [ ] No outdated information

### 4.3 Update 8825 Startup Script (15 minutes)

**File:** `8825_core/system/8825_unified_startup.sh`

**Add:**
- Windsurf MCP server availability check
- Report which servers are configured for Windsurf
- Distinguish between Goose-only vs Windsurf-compatible

**Validation:**
- [ ] `8825 start` shows Windsurf MCP status
- [ ] Output is clear and actionable
- [ ] No errors on startup

### 4.4 Create Health Check Script (20 minutes)

**File:** `~/mcp_servers/health_check.sh`

**Purpose:** Test all 9 MCP servers from command line

**Features:**
- Iterate through all servers
- Attempt connection/handshake
- Report status for each
- Summary at end

**Usage:**
```bash
~/mcp_servers/health_check.sh
# Output:
# ✅ 8825-core: Operational (9 tools)
# ✅ hcss-bridge: Operational (5 tools)
# ...
# Summary: 9/9 servers operational
```

**Validation:**
- [ ] Script runs without errors
- [ ] Accurately detects server status
- [ ] Provides actionable error messages
- [ ] Completes in < 30 seconds

---

## Phase 5: New MCP Creation Protocol

### 5.1 Create Template (30 minutes)

**Location:** `~/mcp_servers/_template/`

**Contents:**
- `server.js` (Node template)
- `server.py` (Python template)
- `package.json` / `requirements.txt`
- `README.md` (template)
- `.gitignore`
- `test_server.sh` (basic test script)

**Features:**
- Minimal working MCP server
- Example tool with echo functionality
- Error handling boilerplate
- Logging setup
- Standard project structure

**Validation:**
- [ ] Template servers start successfully
- [ ] Example tools work
- [ ] Templates are well-commented
- [ ] README is comprehensive

### 5.2 Create Protocol Document (45 minutes)

**File:** `~/mcp_servers/NEW_MCP_CREATION_PROTOCOL.md`

**Sections:**

1. **When to Create an MCP Server**
   - Criteria checklist
   - MCP vs standalone script decision tree

2. **Pre-Creation Checklist**
   - Verify not duplicating existing server
   - Check if tool should be added to existing server
   - Review implementation location (8825_core vs project)

3. **Step-by-Step Creation Process**
   - Copy template
   - Implement tools
   - Add to Windsurf configuration
   - Add to Goose configuration
   - Update mcp_registry.json
   - Test in both Windsurf and Goose
   - Document in main README

4. **Testing Requirements**
   - Checklist of 5 tests (same as Phase 2)
   - Performance criteria
   - Error handling requirements

5. **Integration Requirements**
   - Must work in Windsurf ✅
   - Must work in Goose ✅
   - Must be added to health_check.sh ✅
   - Must be documented ✅
   - Must have test cases ✅

6. **Promotion Criteria**
   - When to move from sandbox to production
   - Stability requirements (14 days, tested in both clients)

**Validation:**
- [ ] Protocol is complete
- [ ] Process is repeatable
- [ ] Examples included
- [ ] Linked from main README

### 5.3 Test Protocol with Mock MCP (30 minutes)

**Action:** Create a test MCP server using the new protocol

**Test Server:** `test-echo-server`
- Simple echo tool
- Returns input as output
- Tests all protocol steps

**Validation:**
- [ ] Protocol successfully followed
- [ ] All steps clear and actionable
- [ ] Server works in Windsurf
- [ ] Server works in Goose
- [ ] Time to create < 20 minutes
- [ ] No gaps in process

**Gate:** Protocol must successfully create working server before Phase 6

---

## Phase 6: Final Validation & Sign-Off

### 6.1 Complete System Test (30 minutes)

**Test Matrix:**

| Server | Windsurf | Goose | Health Check | Docs | Status |
|--------|----------|-------|--------------|------|--------|
| 8825-core | ✅ | ✅ | ✅ | ✅ | ✅ |
| hcss-bridge | ✅ | ✅ | ✅ | ✅ | ✅ |
| figma-make-transformer | ✅ | ✅ | ✅ | ✅ | ✅ |
| figjam | ✅ | ✅ | ✅ | ✅ | ✅ |
| otter-integration | ✅ | ✅ | ✅ | ✅ | ✅ |
| fds | ✅ | ✅ | ✅ | ✅ | ✅ |
| meeting-automation | ✅ | ✅ | ✅ | ✅ | ✅ |
| ral-portal | ✅ | ✅ | ✅ | ✅ | ✅ |
| customer-platform | ✅ | ✅ | ✅ | ✅ | ✅ |

**Must verify:**
- All tools accessible from Windsurf
- All tools accessible from Goose
- Health check passes
- Documentation complete

### 6.2 Definition of Done Checklist

**Implementation:**
- [x] Phase 0: Discovery complete
- [ ] Phase 1: Configuration established
- [ ] Phase 2: All 9 servers integrated
- [ ] Phase 3: E2E testing passed
- [ ] Phase 4: Production deployed
- [ ] Phase 5: Protocol documented

**Deployment:**
- [ ] All servers accessible from Windsurf
- [ ] All servers continue working in Goose
- [ ] Startup script updated
- [ ] Health check script created
- [ ] No errors in daily use

**Documentation:**
- [ ] WINDSURF_INTEGRATION.md complete
- [ ] README.md updated
- [ ] NEW_MCP_CREATION_PROTOCOL.md created
- [ ] LAUNCH_8825_MODE.md updated
- [ ] All examples tested

**Wide Deployment:**
- [ ] Works across all 8825 workspaces
- [ ] No manual setup required after restart
- [ ] Auto-loads with 8825 startup

**Knowledge Transfer:**
- [ ] Pain points documented
- [ ] Learnings captured in memory
- [ ] MCP bridge decision documented
- [ ] Troubleshooting guide complete

### 6.3 Production Sign-Off

**Criteria:**
- [ ] All 9 servers production-ready
- [ ] All tests passing
- [ ] All documentation complete
- [ ] Zero blockers remaining
- [ ] Health check script working
- [ ] New MCP protocol tested

**Sign-Off Statement:**
"All 9 MCP servers are fully integrated into Windsurf with E2E testing complete, comprehensive documentation, and a repeatable protocol for new MCP creation. System is production-ready."

---

## Rollback Plan

**If Issues Encountered:**

1. **Configuration Issues:**
   - Restore backup configuration
   - Revert to Goose-only operation
   - Time to rollback: 5 minutes

2. **Server Failures:**
   - Disable problematic server only
   - Continue with working servers
   - Investigate and fix offline

3. **Performance Issues:**
   - Remove resource-intensive servers
   - Optimize and re-add individually

**Backup Locations:**
- Configuration: `~/mcp_servers/backup/`
- Documentation: Git history
- Server code: Already in version control

---

## Risk Mitigation

**Identified Risks:**

1. **Windsurf MCP system unknown**
   - Mitigation: Phase 0 discovery first, adjust plan as needed
   - Impact: Could delay by 1-2 hours for research

2. **Server dependencies missing**
   - Mitigation: Test each server individually before E2E
   - Impact: 15-30 min per missing dependency

3. **Path or permission errors**
   - Mitigation: Use absolute paths, verify permissions early
   - Impact: 10-15 min per error

4. **Tool calls fail in production**
   - Mitigation: Meaningful test cases in Phase 2
   - Impact: Caught before production deployment

---

## Timeline Summary

**Optimistic (3 hours):**
- Phase 0: Complete ✅
- Phase 1: 45 minutes
- Phase 2: 2 hours (all servers)
- Phase 3: 1 hour 5 minutes
- Phase 4: 1 hour 20 minutes
- Phase 5: 1 hour 45 minutes
- Phase 6: 30 minutes
- **Total: ~7 hours** (with all phases)

**Realistic (4 hours to Phase 4):**
- Account for troubleshooting
- Dependencies installation
- Documentation polish
- Testing iterations
- **Phase 1-4: 3.5-4 hours**
- **Phase 5-6: Additional 2-3 hours if desired**

---

## Success Metrics

**Quantitative:**
- 9/9 servers operational in Windsurf
- 0 configuration errors on startup
- < 5 seconds average tool response time
- 100% test cases passing
- 100% documentation coverage

**Qualitative:**
- Easy to add new MCP servers
- Clear troubleshooting process
- Confident in production stability
- Can find any tool quickly
- New team members can use system

---

## Next Steps

1. **Review this plan** → Approve or request changes
2. **Schedule execution** → Block 4 hours for Phases 1-4
3. **Begin Phase 1** → Identify Windsurf MCP configuration method
4. **Execute systematically** → Follow gates, don't skip validations
5. **Document learnings** → Update plan with actual findings

**Ready to proceed when approved.**
