# 8825 User Onboarding Philosophy

**Status:** Active Development  
**Version:** 1.0  
**Date:** 2025-11-09  
**Scope:** Cross-project onboarding framework

---

## 🎯 NORTH STAR

**"First automation win in under 5 minutes, then safely graduate to deeper power."**

### **Core Mantra:**
- **Reduce thought/typing**
- **Avoid credential friction**
- **Prove value immediately**
- **Start read-only, escalate on trust**

---

## 🏗️ THREE-LANE PHILOSOPHY

Users arrive with different comfort levels. We meet them where they are:

### **1. Zero-Keys Lane** (No IT Required)
**For:** Non-technical users, no API key comfort  
**Philosophy:** Value without credentials

**Approach:**
- Magic inbound email: `inbox@{workspace}.8825.ai`
- Watched folder via OAuth (Dropbox/Drive)
- ICS-only calendar (read-only subscription)
- Optional Slack DM bot

**Why:** Beginners never touch secrets, still get automation

---

### **2. One-Click OAuth Lane** (Connections Hub)
**For:** Users comfortable with "Sign in with Google"  
**Philosophy:** Progressive permissions with explicit consent

**Approach:**
- Large provider buttons (Google, Microsoft, Dropbox, Notion, Slack)
- Start READ-ONLY by default
- Escalate per capability toggle ("Allow create calendar events")
- Consent Receipt (plain-English PDF)

**Why:** Familiar OAuth flow, granular control, transparent permissions

---

### **3. Concierge Lane** (White-Glove)
**For:** Teams needing hand-holding, enterprise setups  
**Philosophy:** Human-guided setup with documentation

**Approach:**
- 30-min co-browse checklist (no remote control)
- We run setup script, verify flows
- Deliver: Keys & Scopes Map, Consent Receipt, 2-week Health Check
- Org Admin Pack: SSO/SAML notes, pre-approved scopes

**Why:** Support burden becomes revenue opportunity, builds trust

---

## 🎯 FIRST-WIN PATH

**Consistent across all lanes:**

1. **Pick a starter:** "Bills → OCR → Calendar + Drive" or "Inbox → Smart Filing"
2. **Connect one source:** Email OR folder OR Google account
3. **Run test with sample:** Baked-in guaranteed-pass demo
4. **Observe result:** Draft calendar event, Drive PDF, Slack summary
5. **Turn it on:** Toggle from read-only → assisted write → full auto

**Always support UNDO**

---

## 🧩 CORE COMPONENTS

### **Building Blocks:**

| Component | Purpose | User Benefit |
|-----------|---------|--------------|
| **Magic Link Sessions (PKCE)** | Passwordless, device-aware | No password friction |
| **Scope Bundles** | "Safe Read-Only" / "Write Essentials" / "Advanced Admin" | Clear permission levels |
| **Health Monitor** | Connection tiles show last success | Proactive issue detection |
| **Consent Receipts** | Human-readable action log, downloadable PDF | Transparency & trust |
| **Recovery Paths** | Device-code flow, QR handoff | Works in locked-down environments |

---

## 🚫 NO-API-KEY ALTERNATIVES

**Philosophy:** Beginners should never touch secrets

### **Approaches:**

1. **Email-only automation**
   - Plus-address rules: `payables+acme@...`
   - Forward to magic inbox
   - Auto-parse, file, propose calendar holds

2. **Folder rules**
   - Drop into `Bills_2025/11`
   - Auto-process on file arrival
   - No dashboard required

3. **Upload form page**
   - Drag-and-drop interface
   - Receipt + next steps
   - Zero configuration

---

## 🔓 "PRO POWER" (Opt-In)

**Philosophy:** Don't scare beginners, but support power users

### **Advanced Features:**

- **Vault choice:** 8825 encrypted vault OR user-owned encrypted bundle in Dropbox/Drive
- **Service Accounts:** Domain delegation for orgs (admin-approved scopes, auto-rotation)
- **Read-only bank data:** Via aggregator (strictly opt-in, separated connector)

**Rule:** Advanced features hidden until user demonstrates need

---

## 📐 UX PRINCIPLES

### **1. Show Value First**
- Demo before configuration
- Baked-in samples guarantee success
- Explain in plain English

### **2. Start Read-Only**
- Minimal permissions by default
- Escalate on explicit toggle
- Always offer undo

### **3. Progressive Disclosure**
- Keep checklist under 5 steps
- Hide complexity until needed
- Surface power features contextually

### **4. Reflect Trust**
- Consent receipts (downloadable PDF)
- Readable audit logs
- Visible status/health indicators
- 1-click re-auth when needed

### **5. Multiple Entry Points**
- Email (zero setup)
- OAuth (familiar flow)
- Concierge (human support)

---

## 🎓 IMPLEMENTATION PHILOSOPHY

### **MVP Priorities:**

**Ship First:**
1. Connections Hub (Google + Dropbox + Slack; read-only first)
2. Starter Flow: "Bills → OCR → Calendar + Drive" with sample
3. Consent Receipt generator (simple PDF)
4. Health Monitor (green/amber/red + 1-click re-auth)
5. Concierge Script (10-step runbook)

**V2 Expansion:**
- Microsoft 365 Graph connectors
- Notion integration
- Device-code flow
- Admin Pack & SSO/SAML playbook
- User-owned encrypted token bundle
- Bank data connector (isolated, optional)

---

## ⚖️ RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| **Users fear over-permission** | Start read-only; human-readable consent receipts; granular toggles |
| **OAuth decay/broken tokens** | Health Monitor + proactive re-auth prompts; fallback email/folder |
| **Demo fails** | Provide guaranteed-pass sample + "replay last run" |
| **Support burden** | Concierge Lane, templated scripts, 2-week check, self-serve fixes |

---

## 📊 SUCCESS METRICS

| Metric | Target |
|--------|--------|
| **Time-to-first-value (TTFV)** | <5 minutes |
| **Starter Flow completion rate** | ≥85% |
| **Scope upgrade acceptance (read → write)** | ≥40% by Day 7 |
| **Re-auth success within 24h** | ≥90% |
| **NPS after first win** | ≥+40 |

---

## 🔑 KEY DECISIONS

### **From Brainstorm:**

1. ✅ **Adopt progressive permissions** with explicit capability toggles
2. ✅ **Always provide a sample** for guaranteed demo run
3. ✅ **Standardize Consent Receipt + Audit Log** for every connection
4. ✅ **Provide three lanes** (Zero-Keys, OAuth Hub, Concierge) to match user comfort

### **Rationale:**

**Why three lanes?**
- Users have different technical comfort levels
- One-size-fits-all creates friction
- Multiple entry points increase conversion

**Why start read-only?**
- Builds trust through transparency
- Reduces permission anxiety
- Demonstrates value before asking for write access

**Why guaranteed samples?**
- First impression is critical
- Failed demo = lost user
- Success breeds confidence to try real data

**Why consent receipts?**
- Transparency builds trust
- Audit trail for compliance
- Reduces support burden ("What did I authorize?")

---

## 🌍 CROSS-PROJECT APPLICATION

### **HCSS:**
- Concierge Lane for enterprise clients
- Admin Pack for IT departments
- SSO/SAML integration

### **Joju:**
- Zero-Keys Lane for individual professionals
- OAuth Hub for Google Workspace users
- Progressive permissions for calendar/drive

### **Team 76:**
- Internal onboarding uses same principles
- Dogfood all three lanes
- Iterate based on team feedback

### **Future Clients:**
- Reusable onboarding framework
- Customizable starter flows
- White-label consent receipts

---

## 📚 GLOSSARY

| Term | Definition |
|------|------------|
| **Progressive permissions** | Start minimal; request additional scopes only when a feature needs them |
| **PKCE** | OAuth extension enabling secure, passwordless magic-link sessions |
| **Device-code flow** | Login path that doesn't require a browser on the device |
| **Consent Receipt** | Human-readable PDF summarizing scopes & purposes |
| **Health Monitor** | Dashboard showing connection status with 1-click fixes |
| **Scope Bundles** | Pre-defined permission sets (Read-Only, Write Essentials, Advanced Admin) |

---

## 🔗 RELATED DOCUMENTATION

- **Source Brainstorm:** `implementations/low_friction_onboarding_brainstorm.md`
- **Tokenization Philosophy:** `../tokenization/principles.md`
- **8825 Architecture:** `../../system/version.json`
- **MCP Integration:** `../../integrations/mcp/`

---

## 🚀 NEXT ACTIONS

### **Immediate:**
1. Spec Connections Hub MVP UI (copy + states + error fixes)
2. Build Bills→OCR Starter Flow with replayable sample
3. Implement PDF Consent Receipt generator
4. Instrument Health Monitor tiles + re-auth CTA
5. Draft Concierge 10-step runbook and Admin Pack outline

### **Short Term:**
1. Test all three lanes with real users
2. Measure TTFV and completion rates
3. Iterate based on feedback
4. Document learnings

### **Long Term:**
1. Expand to Microsoft 365, Notion
2. Build Admin Pack for enterprise
3. Create white-label version
4. Open-source onboarding framework

---

## 🎯 PHILOSOPHY IN ACTION

### **Example: New User Journey**

**User:** Small business owner, not technical

**Lane:** Zero-Keys

**Flow:**
1. **Receives invite:** "Forward your bills to bills@acme.8825.ai"
2. **Forwards first bill:** Utility bill PDF
3. **Gets Slack DM:** "✅ Bill processed: $234.56 due Nov 15. Draft calendar event created."
4. **Clicks link:** Sees calendar event draft + PDF in Drive
5. **Approves:** "Turn on autopilot for future bills"
6. **Result:** Automation running, zero API keys touched

**Time:** 3 minutes  
**Friction:** Zero  
**Value:** Immediate

---

**This philosophy guides all 8825 onboarding implementations. Users should feel empowered, not overwhelmed.**
