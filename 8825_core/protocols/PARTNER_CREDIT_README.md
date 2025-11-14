# 8825 Partner Credit System - Phase 1

**Version:** 1.0.0  
**Phase:** Manual Tracking  
**Effective:** 2025-11-08  
**Pilot Duration:** 90 days (until 2025-02-08)

---

## Quick Start

### 1. Create a Work Order
1. Copy `WORK_ORDER_TEMPLATE.md`
2. Fill in all sections
3. Get approval from requester and builder
4. If >100 credits, get steering group approval
5. File in shared location (Notion/Airtable)

### 2. Execute Work
1. Builder completes deliverables
2. Meets acceptance criteria
3. Provides evidence (repo, docs, tests)
4. Requests acceptance review

### 3. Log Credits
1. Requester validates acceptance criteria met
2. Log credits to manual ledger
3. Update work order status to "Completed"
4. Record actual hours for estimator learning

### 4. Quarterly True-Up
1. Calculate credit balance (Smart vs HCSS)
2. If within ±15%, roll over to next quarter
3. If outside ±15%, choose true-up option:
   - Cash settlement at 80% peg
   - Roll over with plan to balance
   - Convert to equity (if applicable)

---

## System Overview

### What Is This?
A non-crypto credit-based barter system for Smart/HCSS work exchange.

### Key Principles
- **1 credit = $100 value**
- **18-month expiry** (with 30-day warning)
- **Skill multipliers** (0.8x - 1.5x)
- **Work order caps** (25-150 credits)
- **Quarterly true-up** (±15% tolerance)

### Phase 1 Scope
- ✅ Protocol defined
- ✅ Work order template
- ✅ Manual ledger tracking
- ✅ Documentation
- ❌ No automation (Phase 2)
- ❌ No 8825 integration (Phase 2)
- ❌ No metrics dashboard (Phase 2)

---

## Credit Rules

### Peg Value
- **1 credit = $100 USD equivalent**
- Simple mental math
- Easy to estimate work value

### Expiry
- **18 months from issuance**
- **30-day warning** before expiry
- Forces use, prevents hoarding

### Balance Tolerance
- **±15% quarterly tolerance**
- True-up if balance exceeds tolerance
- Options: cash (80% peg), roll over, equity

---

## Skill Multipliers

### 1.0x Base Rate
**Examples:**
- Standard engineering
- Basic automation
- Documentation
- Code maintenance

### 1.25x Specialized
**Examples:**
- Data engineering
- Security hardening
- Complex integrations
- 8825 MCP development
- API design

### 1.5x Scarce Skills
**Examples:**
- Real-time systems
- ML/AI implementation
- Novel architecture design
- 8825 core protocol design
- Performance optimization

### 0.8x Advisory
**Examples:**
- Consulting without deliverables
- Code review only
- Architecture review only
- Strategic planning

---

## Work Order Process

### Step 1: Create Work Order
1. Use `WORK_ORDER_TEMPLATE.md`
2. Define clear scope and acceptance criteria
3. Estimate hours and calculate credits
4. Identify dependencies and risks

### Step 2: Get Approval
- **Requester:** Approves scope and estimate
- **Builder:** Accepts work and timeline
- **Steering Group:** Approves if >100 credits

### Step 3: Execute
- Builder completes deliverables
- Meets acceptance criteria
- Provides evidence (code, docs, tests)
- Documents actual hours

### Step 4: Validate & Accept
- Requester validates acceptance criteria
- QA validator reviews (earns 10% credits)
- If accepted, log credits
- If disputed, follow dispute resolution

### Step 5: Log Credits
- Record in manual ledger
- Update work order status
- Feed actual hours to estimator (for Phase 2)

---

## Manual Ledger Setup

### Option 1: Notion Database
**Fields:**
- Work Order ID
- From (Smart/HCSS)
- To (HCSS/Smart)
- Title
- Credits
- Status
- Date Issued
- Date Completed
- Expiry Date

**Views:**
- Active work orders
- Credit balance (Smart vs HCSS)
- Expiring soon (30 days)
- Completed work orders

### Option 2: Airtable
**Same fields as Notion**

**Formulas:**
- Balance = SUM(Smart credits) - SUM(HCSS credits)
- Days to expiry = Expiry Date - Today
- Status indicators

### Option 3: Simple JSON
```json
{
  "ledger": [
    {
      "id": "WO-IT-001",
      "from": "Smart",
      "to": "HCSS",
      "title": "Network security audit",
      "credits": 45,
      "status": "completed",
      "issued": "2025-11-08",
      "completed": "2025-11-15",
      "expiry": "2027-05-08"
    }
  ],
  "balance": {
    "smart_issued": 45,
    "hcss_issued": 0,
    "net_balance": 45,
    "tolerance_exceeded": false
  }
}
```

---

## Priority Levels & SLAs

### P1 Critical (7 days)
- Production down
- Security issue
- Blocking launch

### P2 High (14 days)
- Important feature
- Significant impact
- Time-sensitive

### P3 Normal (30 days)
- Standard work
- Planned improvements

### P4 Low (60 days)
- Nice-to-have
- Backlog items

---

## Dispute Resolution

### Level 1: Steering Group (3 days)
- Initial review and mediation
- Most disputes resolved here

### Level 2: Independent Technical Review (7 days)
- External expert evaluation
- Technical assessment

### Level 3: Binding Arbitration (14 days)
- Final resolution
- Cash settlement at 80% peg if needed

### Pause Rule
- Disputed work paused
- Unrelated work continues

### Evidence Required
- Work order specification
- Acceptance criteria
- Delivery artifacts
- Communication trail
- Test results

---

## IP & Licensing

### Default License
**Perpetual, royalty-free for Smart/HCSS internal use**

### Shared Repository
- All deliverables in shared repo
- LICENSE.md file required
- Clear ownership and rights

### Commercialization
**Internal Use:** Free for both partners

**External Licensing:**
- Revenue share options:
  - 80/20 (builder/requester)
  - 50/50 (equal split)
  - Custom per agreement
- Both partners must approve

---

## Governance

### Steering Group
**Composition:** 2 representatives per partner

**Responsibilities:**
- Approve work orders >100 credits
- Resolve disputes
- Adjust multipliers/caps
- Quarterly true-up review

**Meetings:** Monthly

**Decision Making:** Consensus or majority vote

### 90-Day Pilot
**Start:** 2025-11-08  
**Review:** 2025-02-08

**Success Criteria:**
- At least 3 work orders completed per partner
- Balance within ±15% tolerance
- No unresolved disputes
- Mutual satisfaction rating >4/5

---

## Quality Standards

### Acceptance Criteria
- Must be defined before work starts
- Testable and measurable
- Clear pass/fail conditions

### Testing Required
- Unit tests for code
- Integration tests
- Manual validation checklist
- Performance benchmarks

### Documentation Required
- README.md
- Runbook (for automations)
- API documentation (if applicable)
- Architecture diagrams

### Rework Policy
- Free rework if acceptance criteria not met
- Builder responsible for quality

### Quality Tokens
- QA validators earn 10% of work order credits
- Incentivizes thorough review

---

## Quarterly True-Up Process

### Step 1: Calculate Balance
```
Balance = SUM(Smart credits issued) - SUM(HCSS credits issued)
Tolerance = ±15% of total credits exchanged
```

### Step 2: Check Tolerance
- **Within ±15%:** Roll over to next quarter
- **Outside ±15%:** True-up required

### Step 3: Choose True-Up Option
1. **Cash settlement** at 80% peg
2. **Roll over** with plan to balance next quarter
3. **Convert to equity** (if applicable)

### Step 4: Document Decision
- Record in ledger
- Update steering group
- Plan for next quarter

---

## Example Work Orders

### Example 1: Network Security Audit
**ID:** WO-IT-001  
**From:** Smart  
**To:** HCSS  
**Credits:** 45 (30h × 1.5x scarce multiplier)  
**Priority:** P1 Critical  
**SLA:** 7 days

### Example 2: Inbox OCR Triage Pipeline
**ID:** WO-AUTO-001  
**From:** HCSS  
**To:** Smart  
**Credits:** 56 (45h × 1.25x specialized multiplier)  
**Priority:** P2 High  
**SLA:** 14 days

### Example 3: RAL Operations Automation
**ID:** WO-RAL-OPS-001  
**From:** HCSS  
**To:** Smart  
**Credits:** 38 (38h × 1.0x base multiplier)  
**Priority:** P3 Normal  
**SLA:** 30 days

---

## Files & Locations

### Protocol
`8825_core/protocols/partner_credit_protocol.json`

### Work Order Template
`8825_core/protocols/WORK_ORDER_TEMPLATE.md`

### Manual Ledger
Notion/Airtable (set up by team)

### Automation Catalog
`8825_focus_hcss/automations/` (Phase 2)

---

## Phase 2 Preview

**Coming in next refactor (refactor-003):**
- ✅ Auto-log credits to 8825
- ✅ Validation protocol automation
- ✅ Metrics dashboard
- ✅ Automation catalog
- ✅ Integration with 8825 task history
- ✅ Estimator learning from actual hours

**Effort:** 20 hours (calibrated)

---

## Support & Questions

### Steering Group Contacts
**Smart:** [Names]  
**HCSS:** [Names]

### Monthly Meeting
**Schedule:** [TBD]  
**Location:** [Zoom/In-person]

### Pilot Review
**Date:** 2025-02-08  
**Agenda:** Evaluate success criteria, decide on renewal

---

## Quick Reference

| Item | Value |
|------|-------|
| Credit Peg | $100 USD |
| Expiry | 18 months |
| Balance Tolerance | ±15% |
| Work Order Min | 25 credits |
| Work Order Max | 150 credits |
| Base Multiplier | 1.0x |
| Specialized Multiplier | 1.25x |
| Scarce Multiplier | 1.5x |
| Advisory Multiplier | 0.8x |
| QA Validator Bonus | 10% |
| Pilot Duration | 90 days |

---

**Ready to start the 90-day pilot!** 🚀
