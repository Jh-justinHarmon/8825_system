# Tutorial System Implementation Plan
**Version:** 1.0  
**Date:** 2025-11-16  
**Status:** Ready for Review

---

## Executive Summary

This plan implements a **Living Tutorial System** for 8825 that solves the "UI vs docs mismatch" problem through interactive capture, validation, and adaptive guidance.

**Core Innovation:** Tutorials are executable objects with screenshot validation, not static documents.

**Key Components:**
1. Interactive Capture Protocol (AI-assisted)
2. Tutorial Hub MCP (central management + validation API)
3. Multi-mode Guidance Protocol (Coach/Co-pilot/Overview)

**Timeline:** 4 phases over 6-8 weeks  
**Risk Level:** Medium (new patterns, CV dependencies)

---

## Technical Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│  (Cascade Chat / Future: Dedicated Tutorial UI)            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  GUIDANCE PROTOCOL LAYER                     │
│  • Coach Mode Handler                                        │
│  • Co-pilot Mode Handler                                     │
│  • Overview Mode Generator                                   │
│  • Screenshot Comparison Router                              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   TUTORIAL HUB MCP                           │
│  • Tutorial CRUD API                                         │
│  • Screenshot Validation Service                             │
│  • Version Management                                        │
│  • OCR Processing Pipeline                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    STORAGE LAYER                             │
│  • Tutorial Objects (JSON) - tutorials/                      │
│  • Screenshots (PNG) - tutorials/screenshots/                │
│  • OCR Cache (JSON) - tutorials/ocr_cache/                  │
│  • User Progress (JSON) - tutorials/user_progress/          │
└──────────────────────────────────────────────────────────────┘
```

### Technology Stack

**MCP Server:**
- **Language:** Python 3.9+
- **Framework:** Flask or FastAPI (FastAPI recommended for async validation)
- **Port:** 8829 (new MCP in the 8825 ecosystem)

**Computer Vision / OCR:**
- **Primary:** Tesseract OCR (local, free, battle-tested)
- **Backup:** Google Vision API (if higher accuracy needed for complex UIs)
- **Image Comparison:** OpenCV + SSIM (Structural Similarity Index)

**Storage:**
- **Format:** JSON for tutorial objects (human-readable, version-controllable)
- **Location:** `8825_core/tutorials/` (shareable across users)
- **Screenshots:** PNG, organized by tutorial ID

**Integration:**
- **With 8825:** New MCP in `start_all_mcps.sh`
- **With Cascade:** New command set: `/tutorial start`, `/tutorial validate`, etc.

---

## Implementation Phases

### Phase 0: Foundation & Validation (Week 1)

**Goal:** Prove the core assumptions with a minimal spike.

#### Gate 0.1: Technology Validation
**Tasks:**
1. Install Tesseract OCR on your Mac
2. Create test script: `test_ocr.py`
   - Takes a Rive screenshot
   - Runs OCR
   - Outputs all detected text + coordinates
3. Create test script: `test_image_compare.py`
   - Compares two screenshots (one with Timeline visible, one without)
   - Outputs similarity score (SSIM)

**Success Criteria:**
- [ ] OCR correctly identifies "Animate", "Timeline", "Duration" from Rive screenshot
- [ ] Image comparison correctly reports <80% similarity when Timeline panel is added
- [ ] Both scripts run in <2 seconds on typical screenshot

**Validation:**
```bash
python test_ocr.py tutorials/test_screenshots/rive_step1.png
# Expected output: Text regions with "Animate" at coords ~(1420, 60)

python test_image_compare.py tutorials/test_screenshots/rive_step1.png tutorials/test_screenshots/rive_step2.png
# Expected output: Similarity: 0.72 (below 0.80 threshold = different state)
```

**Exit Gate:**
- All success criteria met
- Decision: Proceed with Tesseract or pivot to Google Vision API

---

### Phase 1: Tutorial Hub MCP - Core (Weeks 2-3)

**Goal:** Build the central MCP that stores and serves tutorial objects.

#### Gate 1.1: MCP Scaffold + Basic CRUD
**Tasks:**
1. Create directory: `8825_core/tutorials/mcp_server/`
2. Implement basic FastAPI server:
   - `POST /tutorials` - Create new tutorial
   - `GET /tutorials` - List all tutorials
   - `GET /tutorials/{id}` - Get specific tutorial
   - `PUT /tutorials/{id}` - Update tutorial
3. Define Tutorial Object schema (JSON Schema validation)
4. Add to `start_all_mcps.sh` on port 8829

**Schema (v1):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["tutorialId", "tool", "goal", "steps"],
  "properties": {
    "tutorialId": { "type": "string" },
    "tool": { "type": "string" },
    "uiVersion": { "type": "string" },
    "captureDate": { "type": "string", "format": "date-time" },
    "goal": { "type": "string" },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["stepId", "goal", "screenshotId"],
        "properties": {
          "stepId": { "type": "integer" },
          "goal": { "type": "string" },
          "instruction": { "type": "string" },
          "screenshotId": { "type": "string" },
          "actionType": { "enum": ["click", "type", "drag", "wait"] },
          "targetText": { "type": "string" },
          "targetCoords": { "type": "object" },
          "ocrData": { "type": "object" }
        }
      }
    }
  }
}
```

**Success Criteria:**
- [ ] MCP starts successfully on port 8829
- [ ] Can create a tutorial via `POST /tutorials` with test data
- [ ] Can retrieve it via `GET /tutorials/{id}`
- [ ] Schema validation rejects malformed tutorial objects

**Validation Tests:**
```bash
# Start MCP
./start_tutorial_mcp.sh

# Test create
curl -X POST http://localhost:8829/tutorials \
  -H "Content-Type: application/json" \
  -d @test_tutorial.json

# Test list
curl http://localhost:8829/tutorials

# Test get
curl http://localhost:8829/tutorials/test-tutorial-1
```

**Exit Gate:**
- All CRUD operations work
- JSON schema validation active
- MCP integrated into `start_all_mcps.sh`

---

#### Gate 1.2: Screenshot Validation Endpoint
**Tasks:**
1. Implement `POST /tutorials/{id}/validate_step`
   - Accepts: `stepId`, `userScreenshot` (base64 or file upload)
   - Compares user screenshot to stored step screenshot using SSIM
   - Runs OCR on user screenshot, checks for expected `targetText`
   - Returns: `{"valid": true/false, "confidence": 0.0-1.0, "feedback": "string"}`
2. Add OCR caching (don't re-OCR the same stored screenshot)
3. Add configurable similarity threshold (default: 0.75)

**Success Criteria:**
- [ ] Endpoint correctly validates matching screenshot (confidence >0.75)
- [ ] Endpoint correctly rejects non-matching screenshot (confidence <0.75)
- [ ] Provides useful feedback: "Expected 'Timeline' panel on right, but not found"
- [ ] Response time <3 seconds for typical screenshot

**Validation Tests:**
```bash
# Test valid screenshot
curl -X POST http://localhost:8829/tutorials/rive-fade-anim/validate_step \
  -F "stepId=2" \
  -F "screenshot=@user_screenshot_correct.png"
# Expected: {"valid": true, "confidence": 0.89, "feedback": "Step complete"}

# Test invalid screenshot  
curl -X POST http://localhost:8829/tutorials/rive-fade-anim/validate_step \
  -F "stepId=2" \
  -F "screenshot=@user_screenshot_wrong.png"
# Expected: {"valid": false, "confidence": 0.62, "feedback": "Timeline panel not visible"}
```

**Exit Gate:**
- Validation endpoint works reliably (95%+ accuracy on test cases)
- OCR cache functional (2nd validation of same screenshot is <500ms)
- Feedback messages are actionable

---

### Phase 2: Capture Protocol (Weeks 3-4)

**Goal:** Enable AI-assisted tutorial creation via Cascade chat.

#### Gate 2.1: Capture Session Management
**Tasks:**
1. Add session state management to Tutorial Hub MCP:
   - `POST /capture/start` - Initiates new capture session, returns sessionId
   - `POST /capture/{sessionId}/add_step` - Adds a step to in-progress capture
   - `POST /capture/{sessionId}/finalize` - Converts session to tutorial object
2. Implement temporary storage for in-progress captures

**Success Criteria:**
- [ ] Can start a capture session via API
- [ ] Can add steps to session
- [ ] Can finalize session into valid tutorial object
- [ ] Sessions auto-expire after 4 hours of inactivity

**Validation Tests:**
```bash
# Start capture
SESSION=$(curl -X POST http://localhost:8829/capture/start \
  -H "Content-Type: application/json" \
  -d '{"tool": "Rive", "goal": "Test capture"}' | jq -r '.sessionId')

# Add step
curl -X POST http://localhost:8829/capture/$SESSION/add_step \
  -F "screenshot=@step1.png" \
  -F "goal=Switch to Animate mode"

# Finalize
curl -X POST http://localhost:8829/capture/$SESSION/finalize
```

**Exit Gate:**
- All session operations functional
- Auto-expiration works (tested with 5-minute timeout for testing)

---

#### Gate 2.2: Cascade Capture Commands
**Tasks:**
1. Add new Cascade commands:
   - `/tutorial capture start <tool> <goal>` - Starts interactive capture
   - `/tutorial capture next` - Prompts for next step screenshot
   - `/tutorial capture done` - Finalizes and saves tutorial
2. Implement capture conversation flow in Cascade:
   - On `start`: Create session, prompt user for first screenshot
   - On screenshot received: Auto-OCR, ask for step description
   - On `next`: Save current step, prompt for next screenshot
   - On `done`: Finalize session, display tutorial ID

**Success Criteria:**
- [ ] Can complete full capture workflow in Cascade chat
- [ ] OCR analysis visible to user for confirmation
- [ ] Final tutorial object created and retrievable

**Validation Test:**
User performs end-to-end capture:
1. `/tutorial capture start Rive "Create fade animation"`
2. [Sends screenshot 1]
3. Cascade responds with OCR analysis, asks for description
4. User: "Switch to Animate mode"
5. `/tutorial capture next`
6. [Sends screenshot 2]
7. Cascade responds with OCR analysis, asks for description
8. User: "Create new animation"
9. `/tutorial capture done`
10. Cascade: "Tutorial saved as `rive-fade-anim-v1`. Try it with `/tutorial coach rive-fade-anim-v1`"

**Exit Gate:**
- Complete capture workflow functional
- Generated tutorial passes schema validation
- Screenshots correctly stored and linked

---

### Phase 3: Guidance Protocols (Weeks 4-5)

**Goal:** Implement Coach, Co-pilot, and Overview modes.

#### Gate 3.1: Coach Mode
**Tasks:**
1. Implement `/tutorial coach <tutorialId>` command
2. Conversation flow:
   - Load tutorial object
   - Present Step 1: goal + instruction + screenshot
   - Wait for user to say "done" or send screenshot
   - If screenshot: validate via MCP endpoint
   - If valid: move to Step 2
   - If invalid: show feedback, ask for retry or clarification
3. Track user progress (which step they're on) in session state

**Success Criteria:**
- [ ] Can guide user through complete tutorial step-by-step
- [ ] Screenshot validation works (detects success/failure)
- [ ] Feedback messages are clear and actionable
- [ ] Can handle "go back" request (return to previous step)

**Validation Test:**
User completes Rive tutorial in Coach mode:
1. `/tutorial coach rive-fade-anim-v1`
2. Cascade shows Step 1/8 with screenshot
3. User clicks button, sends screenshot
4. Cascade validates, says "Step 1 complete" and shows Step 2
5. ... continues through all 8 steps
6. Final message: "Tutorial complete! You've created a fade animation."

**Exit Gate:**
- Coach mode functional for full tutorial
- 90%+ validation accuracy on test screenshots
- User can complete tutorial without getting stuck

---

#### Gate 3.2: Co-pilot Mode
**Tasks:**
1. Implement `/tutorial copilot <tutorialId>` command
2. Different flow:
   - Load tutorial, show brief overview
   - Wait for user to work independently
   - When user sends screenshot + "what's next?", find matching step
   - Respond with current step number + next step preview
3. Implement step-matching algorithm:
   - Compare user screenshot against all step screenshots
   - Return step with highest SSIM match (if >0.7 threshold)

**Success Criteria:**
- [ ] Can identify current step from arbitrary user screenshot
- [ ] 85%+ accuracy on step identification (test with 20 screenshots)
- [ ] Handles "I'm stuck" without requiring step number

**Validation Test:**
1. `/tutorial copilot rive-fade-anim-v1`
2. User works through steps 1-3 on their own
3. User sends screenshot (at step 3) + "what's next?"
4. Cascade: "You're on Step 3: 'Set duration to 3 seconds'. Next is Step 4: 'Set opacity keyframes'."

**Exit Gate:**
- Step matching works reliably
- Co-pilot mode provides useful guidance without being prescriptive

---

#### Gate 3.3: Overview Mode
**Tasks:**
1. Implement `/tutorial overview <tutorialId>` command
2. Generate markdown summary:
   - Goal statement
   - Numbered list of all steps (goal + brief instruction)
   - Embedded thumbnail images (if chat supports)
   - Estimated time
3. Add quick navigation: "To start Step 5 in Coach mode: `/tutorial coach <id> --step 5`"

**Success Criteria:**
- [ ] Generates clear, readable overview
- [ ] All steps listed with thumbnails
- [ ] Links to Coach/Co-pilot modes work

**Validation Test:**
1. `/tutorial overview rive-fade-anim-v1`
2. Cascade displays full tutorial outline
3. User: `/tutorial coach rive-fade-anim-v1 --step 3`
4. Cascade jumps directly to Step 3 in Coach mode

**Exit Gate:**
- Overview mode functional
- Quick navigation to specific steps works

---

### Phase 4: Self-Healing & Production Hardening (Weeks 6-8)

**Goal:** Handle UI version changes and prepare for production use.

#### Gate 4.1: Tutorial Forking (Version Management)
**Tasks:**
1. Implement `POST /tutorials/{id}/fork` endpoint
   - Creates new tutorial with incremented version (v1 → v2)
   - Copies all steps, marks original as "deprecated" (still accessible)
2. Add version detection logic:
   - When validation fails repeatedly (3+ times), suggest forking
   - Cascade: "It looks like the Rive UI has changed. Would you like to update this tutorial? (yes/no)"
   - If yes: Enter mini-capture mode for the failing step only
3. Update guidance protocols to check tutorial version/deprecation status

**Success Criteria:**
- [ ] Can fork tutorial via API
- [ ] Forked tutorial has independent step list
- [ ] Original tutorial marked as deprecated
- [ ] Guidance protocols show deprecation warning if using old version

**Validation Test:**
1. Simulate UI change: Rename button in Rive screenshot for Step 2
2. User attempts Step 2 in Coach mode with old tutorial
3. Validation fails 3 times
4. Cascade: "This tutorial may be outdated. Update it? (yes/no)"
5. User: yes
6. Cascade: "Send screenshot of current Rive UI at this step"
7. User sends updated screenshot
8. Cascade: "Tutorial updated to v2. Continuing from Step 2..."

**Exit Gate:**
- Forking workflow functional
- Old and new versions coexist
- Users can choose which version to use

---

#### Gate 4.2: Error Handling & Edge Cases
**Tasks:**
1. Comprehensive error handling:
   - Screenshot upload failures → clear error message + retry
   - OCR failures (blank/corrupt image) → request re-upload
   - MCP server down → graceful degradation (disable validation, continue with instructions only)
   - Tutorial not found → suggest similar tutorials
2. Add logging:
   - All validation requests logged (for debugging)
   - Failed validations logged with reason (to identify patterns)
3. Add rate limiting (prevent abuse of validation endpoint)

**Success Criteria:**
- [ ] All error scenarios have clear user-facing messages
- [ ] No stack traces visible to user
- [ ] System degrades gracefully if MCP is unavailable
- [ ] Logs are structured and queryable

**Validation Tests:**
- Manually trigger each error scenario
- Verify error message clarity
- Verify system doesn't crash
- Check logs contain sufficient debug info

**Exit Gate:**
- All error scenarios handled
- Logging sufficient for debugging production issues

---

#### Gate 4.3: Performance Optimization
**Tasks:**
1. Profile validation endpoint (identify bottlenecks)
2. Optimizations:
   - Parallel OCR processing (if multiple screenshots)
   - Image downscaling before comparison (if >2MB)
   - Redis caching for OCR results (optional, if needed)
3. Set performance SLAs:
   - Validation response: <3 seconds (p95)
   - Tutorial list: <500ms (p95)
   - Screenshot upload: <5 seconds (p95)
4. Load testing:
   - Simulate 10 concurrent users running tutorials
   - Verify no degradation in response times

**Success Criteria:**
- [ ] All endpoints meet SLA targets
- [ ] System handles 10 concurrent users without issues
- [ ] No memory leaks (test with 100+ validation requests)

**Validation Tests:**
```bash
# Load test validation endpoint
ab -n 100 -c 10 -p test_screenshot.json \
  http://localhost:8829/tutorials/rive-fade-anim/validate_step
# Expected: All requests <3s, no errors
```

**Exit Gate:**
- Performance SLAs met
- Load testing passes
- System is production-ready

---

## Testing & Validation Strategy

### Unit Tests
**Coverage Target:** 80%+

**Key Test Suites:**
1. **Tutorial Object Validation** (`test_tutorial_schema.py`)
   - Valid tutorial objects pass schema validation
   - Invalid objects rejected with clear error messages
   
2. **OCR Processing** (`test_ocr.py`)
   - Correctly extracts text from test screenshots
   - Handles edge cases (rotated text, low contrast, overlapping text)
   
3. **Image Comparison** (`test_image_compare.py`)
   - SSIM correctly identifies matching screenshots (>0.8)
   - SSIM correctly identifies non-matching screenshots (<0.7)
   
4. **Screenshot Validation Logic** (`test_validation.py`)
   - Valid screenshot → `{"valid": true}`
   - Invalid screenshot → `{"valid": false, "feedback": "..."}` with actionable message

**Run with:**
```bash
cd 8825_core/tutorials/mcp_server
pytest tests/ --cov=. --cov-report=html
```

---

### Integration Tests
**Coverage Target:** Critical paths only

**Test Scenarios:**
1. **End-to-End Capture** (`test_e2e_capture.py`)
   - Start capture session
   - Add 3 steps via API
   - Finalize session
   - Verify tutorial object created correctly
   
2. **End-to-End Coach Mode** (`test_e2e_coach.py`)
   - Load tutorial
   - Submit valid screenshot for Step 1 → advance to Step 2
   - Submit invalid screenshot for Step 2 → receive feedback
   - Submit valid screenshot for Step 2 → advance to Step 3
   
3. **Tutorial Forking** (`test_e2e_fork.py`)
   - Fork existing tutorial
   - Verify new version created
   - Verify old version marked deprecated
   - Update one step in new version
   - Verify old version unchanged

**Run with:**
```bash
pytest tests/integration/ --verbose
```

---

### User Acceptance Testing (UAT)
**Owner:** You (Justin)

**Test Case 1: Create a Tutorial**
1. Choose a simple tool (e.g., Apple Notes "Create a checklist")
2. Use `/tutorial capture start` workflow
3. Complete capture of 3-5 steps
4. Verify generated tutorial is accurate

**Success Criteria:**
- [ ] Capture process feels intuitive
- [ ] OCR analysis is accurate (no hallucinated text)
- [ ] Final tutorial steps match what you actually did

---

**Test Case 2: Use a Tutorial (Coach Mode)**
1. Reset Apple Notes (or use a different tool)
2. Use `/tutorial coach` to follow the tutorial you created
3. Submit screenshots at each step
4. Verify validation works correctly

**Success Criteria:**
- [ ] Validation correctly identifies when step is complete
- [ ] Validation correctly rejects incorrect screenshots
- [ ] Feedback messages are helpful (not generic)
- [ ] You can complete the task following the tutorial

---

**Test Case 3: Handle UI Change (Forking)**
1. Manually alter a screenshot in an existing tutorial (simulate UI change)
2. Attempt to use the tutorial in Coach mode
3. Trigger the fork workflow when validation fails
4. Update the failing step
5. Verify new version works

**Success Criteria:**
- [ ] System detects UI mismatch
- [ ] Fork workflow is clear and easy to follow
- [ ] Updated tutorial works correctly
- [ ] Old tutorial still accessible (for users on old UI version)

---

## Definition of Done (DoD)

The Tutorial System is **production-ready** when:

### Functional Requirements
- [ ] **Capture Protocol:** Can create a complete tutorial (5+ steps) via Cascade chat in <15 minutes
- [ ] **Coach Mode:** Can guide a user through a tutorial with screenshot validation, achieving 90%+ step validation accuracy
- [ ] **Co-pilot Mode:** Can identify current step from arbitrary screenshot with 85%+ accuracy
- [ ] **Overview Mode:** Generates clear tutorial summaries with all steps listed
- [ ] **Forking:** Can update a tutorial when UI changes, creating a new version while preserving the old

### Non-Functional Requirements
- [ ] **Performance:** All API endpoints meet SLA targets (validation <3s p95, list <500ms p95)
- [ ] **Reliability:** System handles 10 concurrent users without errors or degradation
- [ ] **Maintainability:** 80%+ unit test coverage, all critical paths integration-tested
- [ ] **Usability:** UAT passed by at least 2 users (you + 1 team member)

### Documentation
- [ ] **API Documentation:** OpenAPI spec for all Tutorial Hub MCP endpoints
- [ ] **User Guide:** Teaching document explains how to capture and use tutorials (see TUTORIAL_SYSTEM_USER_GUIDE.md)
- [ ] **Developer Guide:** README in mcp_server explains architecture and how to add features
- [ ] **Troubleshooting Guide:** Common issues and solutions documented

### Integration
- [ ] **8825 Integration:** Tutorial Hub MCP included in `start_all_mcps.sh`, starts on boot
- [ ] **Cascade Integration:** All tutorial commands functional (`/tutorial capture`, `/tutorial coach`, etc.)
- [ ] **Storage:** Tutorial objects and screenshots stored in `8825_core/tutorials/`, backed up with Dropbox

---

## End-to-End Final Gate

**The "Rive Animation Tutorial" Test**

This is the ultimate validation that the system works end-to-end.

### Setup
1. You (Justin) will create the "Rive fade animation" tutorial using the Capture Protocol
2. Another user (e.g., a team member unfamiliar with Rive) will attempt to complete the tutorial using Coach Mode

### Pass Criteria
- [ ] **Capture:** You complete the capture process in <20 minutes, creating a tutorial with 8 steps
- [ ] **Validation:** At least 7/8 steps validate correctly for the test user's screenshots
- [ ] **Completion:** The test user successfully creates a working fade animation in Rive by following the tutorial
- [ ] **Feedback:** The test user rates the experience 4/5 or higher on clarity and usefulness
- [ ] **Self-Healing:** If Rive's UI has changed since capture, the fork workflow successfully updates the tutorial

### Execution
1. **Day 1:** You capture the Rive tutorial
2. **Day 2:** Test user attempts tutorial in Coach Mode (you observe but don't help)
3. **Day 3:** Review feedback, identify issues, make adjustments
4. **Day 4:** Repeat test with different tool (e.g., Figma or Notion)
5. **Day 5:** If both tests pass, system is production-ready

---

## Risk Management

### High-Risk Areas

1. **OCR Accuracy**
   - **Risk:** OCR fails on complex UIs (dark mode, overlapping text)
   - **Mitigation:** Fallback to Google Vision API if Tesseract confidence <70%
   - **Contingency:** Manual text entry option ("I don't see this text")

2. **Image Comparison False Negatives**
   - **Risk:** SSIM too strict, rejects valid screenshots due to minor differences (window size, OS theme)
   - **Mitigation:** Configurable similarity threshold per tutorial
   - **Contingency:** "Looks close enough?" override button for user

3. **Performance Degradation**
   - **Risk:** Validation takes >3 seconds, feels sluggish
   - **Mitigation:** Image downscaling, OCR caching, async processing
   - **Contingency:** Progress indicator in UI ("Analyzing screenshot...")

4. **Tutorial Quality**
   - **Risk:** User-captured tutorials are poorly structured or confusing
   - **Mitigation:** Built-in quality checks (flag tutorials with <3 steps, no OCR data)
   - **Contingency:** Community review system (future enhancement)

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| **Phase 0: Foundation** | 1 week | OCR and image comparison validated |
| **Phase 1: Tutorial Hub MCP** | 2 weeks | CRUD API + validation endpoint working |
| **Phase 2: Capture Protocol** | 2 weeks | Can create tutorials via Cascade chat |
| **Phase 3: Guidance Protocols** | 2 weeks | Coach, Co-pilot, Overview modes functional |
| **Phase 4: Hardening** | 2-3 weeks | Forking, error handling, performance optimization |
| **Total** | **6-8 weeks** | **Production-ready system** |

---

## Next Steps

**For Review:**
1. Read this implementation plan
2. Review the companion User Guide (TUTORIAL_SYSTEM_USER_GUIDE.md)
3. Approve, request changes, or reject

**If Approved:**
1. I will create the Phase 0 test scripts (OCR + image comparison validation)
2. You will run them on your Mac with Rive screenshots
3. Based on results, we proceed to Phase 1 or adjust approach

**Decision Point:**
Should we proceed with Phase 0 to validate the core technology assumptions?
