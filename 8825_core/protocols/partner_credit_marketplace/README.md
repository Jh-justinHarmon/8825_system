# Partner Credit Marketplace

**Version:** 3.0 (Phase 3)  
**Status:** ✅ Production Ready  
**Built:** 2025-11-10

Multi-partner credit exchange system with automation licensing and governance.

---

## Quick Start

```bash
cd 8825_core/protocols/partner_credit_marketplace
./marketplace_cli.py
```

---

## Features

### 📊 Multi-Partner Ledger
- Track credits across all partner pairs
- Skill multipliers (0.8x - 1.5x)
- 18-month expiry with warnings
- Balance monitoring and true-up alerts

### 🤖 Automation Catalog
- Browse automations built by partners
- Internal use (free for partners)
- External licensing with revenue split
- Usage and revenue tracking

### 🗳️ Governance System
- Create proposals for major decisions
- Voting with consensus or majority rules
- Steering group management
- Participation tracking

---

## Components

### `ledger.py`
Multi-partner credit tracking system.

**CLI:**
```bash
./ledger.py add-partner smart "Smart Inc" "contact@smart.com"
./ledger.py record smart hcss 50 WO-001 "API integration" 1.25
./ledger.py balance smart hcss
./ledger.py summary smart
```

### `automation_catalog.py`
Automation licensing and revenue distribution.

**CLI:**
```bash
./automation_catalog.py add "HCSS Calendar Sync" "OCR-based calendar automation" smart automation ocr,calendar
./automation_catalog.py search calendar
./automation_catalog.py license AUTO-0001 team76 internal
./automation_catalog.py stats smart
```

### `governance.py`
Voting and proposal management.

**CLI:**
```bash
./governance.py propose "Adjust skill multipliers" "Increase ML rate to 1.75x" smart policy 7
./governance.py vote PROP-0001 hcss for "Agreed"
./governance.py show PROP-0001
./governance.py open
```

### `marketplace_cli.py`
Unified interactive interface for all systems.

---

## Data Storage

All data stored in `data/` directory:
- `multi_partner_ledger.json` - Credit transactions and balances
- `automation_catalog.json` - Automation listings
- `licenses.json` - License records
- `proposals.json` - Governance proposals
- `votes.json` - Voting records

---

## Integration with Phase 1

Phase 1 protocol: `../partner_credit_protocol.json`

Phase 3 adds:
- ✅ Multi-partner support (beyond Smart/HCSS)
- ✅ Automation marketplace
- ✅ Revenue distribution
- ✅ Governance voting

---

## Example Workflow

### 1. Add Partners
```bash
./ledger.py add-partner smart "Smart Inc" "contact@smart.com"
./ledger.py add-partner hcss "HCSS" "contact@hcss.com"
./ledger.py add-partner team76 "Team76" "contact@team76.com"
```

### 2. Record Work
```bash
./ledger.py record smart hcss 50 WO-001 "API integration" 1.25
# Smart earned 62.5 credits (50 × 1.25) from HCSS
```

### 3. Add Automation
```bash
./automation_catalog.py add "Calendar Sync" "HCSS calendar automation" smart automation ocr
```

### 4. License to Another Partner
```bash
./automation_catalog.py license AUTO-0001 team76 external 25
# Team76 pays 25 credits to license the automation
```

### 5. Create Proposal
```bash
./governance.py propose "Add new partner" "Onboard Team76" smart membership 7
```

### 6. Vote
```bash
./governance.py vote PROP-0001 smart for
./governance.py vote PROP-0001 hcss for
# Proposal approved
```

---

## Revenue Distribution

External licensing revenue splits per Phase 1 protocol:
- **80/20** (builder/requester) - default
- **50/50** (equal split)
- **Custom** per agreement

Calculate distribution:
```bash
./automation_catalog.py revenue AUTO-0001
```

---

## Governance Rules

From Phase 1 protocol:
- **Steering group:** 2 reps per partner
- **Meeting frequency:** Monthly
- **Decision making:** Consensus or majority
- **Work orders >100 credits:** Require approval

---

## Built On

- Phase 1: `partner_credit_protocol.json` (manual tracking)
- Phase 2: Automation & 8825 integration (refactor-003)
- Phase 3: Multi-partner marketplace (this)

---

**Ready for multi-partner credit exchange!**
