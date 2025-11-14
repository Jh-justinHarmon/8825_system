# Explorations - Current Status

**Date:** 2025-11-10  
**Total Active:** 8 explorations  
**Recently Added:** 2 (TGIF Issue Tracker, AI UX Precipice Principle)  
**Recently Promoted:** 3 (TGIF Automation, Universal Inbox, MCP Setup)  
**In PoC:** 1 (Weekend Soccer Advisor - 🟡 Near Completion)

---

## 🎯 ACTIVE EXPLORATIONS (8)

### **1. TV Memory Layer** 📺
**File:** `features/tv_memory_layer.md`  
**Status:** Exploration  
**Problem:** Can't remember which streaming service has which show  
**Idea:** Bookmark/journal model with Siri Shortcuts + browser extensions  
**Next:** Time-box for validation (2 weeks)

---

### **2. ChatGPT Mobile MCP** 📱
**File:** `features/chatgpt_mobile_mcp.md`  
**Status:** Awaiting Testing  
**Problem:** ChatGPT mobile can't access MCP servers  
**Idea:** Dropbox-based solution for mobile access  
**Next:** Test when ChatGPT mobile MCP becomes available

---

### **3. Joju Dropbox Contribution Miner** 📚
**File:** `features/joju_dropbox_contribution_miner.md`  
**Status:** Brainstorm  
**Problem:** Need to attribute Dropbox file contributions to Joju  
**Idea:** Mine file metadata, dedupe, produce Joju-ready summaries  
**Next:** Review for potential promotion

---

### **4. Contractor Bid Tool** 🏗️
**File:** `features/contractor_bid_tool.md`  
**Status:** Brainstorm  
**Problem:** Need unit-agnostic takeoff and rate-book system  
**Idea:** Low-friction capture, normalize quantities, apply waste logic  
**Next:** Review for potential promotion

---

### **5. Phil's Ledger (Combined)** 💰 ⭐ **READY**
**Files:** 
- `features/phils_book_brainstorm.md` (7KB - HTML prototype)
- `features/phils_ledger_pipeline_brainstorm.md` (52KB - Full pipeline)

**Status:** Detailed Brainstorm  
**Problem:** Bill tracking, payment management, expense notebook  
**Idea:** 
- Single-file HTML expense notebook (Phil's Book)
- Gmail monitoring + Monarch API integration
- Bank CSV import + reconciliation
- Vendor normalization + rule builder

**Next:** **Strong candidate for promotion to PoC**  
**Note:** Very detailed, implementation-ready, has working prototype

---

### **6. BRAINSTORM_SEPARATION_NEEDED** 📋
**File:** `features/BRAINSTORM_SEPARATION_NEEDED.md`  
**Status:** Placeholder  
**Problem:** `8825_brainstorm_mining_this_chat.txt` contains 10 separate brainstorms  
**Next:** Manually separate into individual explorations

**Contains:**
- RAL Statement Tagger (needs context)
- TGIF Meeting Summary (promoted to PoC!)
- Weekend Soccer Advisor (promoted to JH assistant!)
- RAL Batch Collector
- TGIF Location Launch Prep
- TGIF Auto Rollout Adjuster
- Personal Time Tracker
- Dropbox File Reduction
- Wedgewood Offer Calculator
- LHL Re-Listing Pipeline

---

### **7. TGIF Multi-Channel Issue Tracker** 🎯 ⭐ **NEW**
**File:** `features/tgif_issue_tracker.md`  
**Status:** Planning  
**Problem:** Patricia/Mario can't track issues across multiple channels (email, text, calls, on-site)  
**Solution:** Multi-channel aggregator → Single dashboard → Auto-sync to Google Sheet  
**Next:** Validate with Patricia/Mario, answer open questions, decide on MVP scope

**Key Requirements:**
- Microsoft email integration (Patricia/Mario)
- Screenshot OCR (Mario's phone)
- Google Sheets sync
- Store phone number lookup
- Per-location dashboards

**Value:** Nothing falls through cracks, real-time visibility, pattern detection across stores

---

### **8. AI UX Precipice Principle** 🎨 ⭐ **NEW**
**File:** `philosophy/ai_ux_precipice_principle.md`  
**Status:** Philosophy Document  
**Context:** Guiding UX principle for AI-integrated products  
**Core Idea:** Balance power + empowerment without being creepy or intimidating

**Key Principles:**
- Seamless, not invisible (show your work)
- Frictionless, not effortless (keep agency)
- Progressive disclosure (reveal power over time)
- Explain the magic (in user terms)
- Manual override always (user has final say)

**Application:** Joju contributions pipeline, TGIF issue tracker, all AI features

---

## ✅ RECENTLY PROMOTED (2)

### **1. TGIF Meeting Automation** → PoC
**From:** Exploration brainstorm  
**To:** `8825_core/poc/projects/tgif_automation/`  
**Status:** ✅ Built and ready for validation  
**Components:**
- Otter integration → `poc/infrastructure/otter_integration/`
- Task tracking → `poc/infrastructure/task_tracking/`
- Daily/weekly processors → `poc/projects/tgif_automation/`

### **2. Universal Inbox** → Core
**From:** `explorations/features/UNIVERSAL_INBOX_COMPLETE.md`  
**To:** `8825_core/inbox/UNIVERSAL_INBOX.md`  
**Status:** ✅ Production ready

### **3. MCP Server Setup** → Core
**From:** `explorations/tools/MCP_SERVER_SETUP_COMPLETE.md`  
**To:** `8825_core/mcp/INBOX_SERVER_SETUP.md`  
**Status:** ✅ Production ready

---

## 📦 ARCHIVED (2)

### **1. ChatGPT Quick Setup**
**File:** `archived/CHATGPT_QUICK_SETUP.md`  
**Reason:** Resolved by current workflow

### **2. ChatGPT Instructions**
**File:** `archived/CHATGPT_INSTRUCTIONS.md`  
**Reason:** Resolved by current workflow

---

## 🎯 RECOMMENDED ACTIONS

### **Immediate:**

1. **Phil's Ledger Pipeline** → Promote to PoC
   - Very detailed (52KB)
   - Implementation-ready
   - Clear architecture
   - **Action:** Move to `8825_core/poc/projects/phils_ledger/`

2. **Separate Combined Brainstorms**
   - Extract 10 brainstorms from `BRAINSTORM_SEPARATION_NEEDED.md`
   - Note: 2 already promoted (TGIF, Soccer Advisor)
   - **Action:** Create individual exploration files

### **This Week:**

3. **Review for Promotion:**
   - Joju Dropbox Miner
   - Contractor Bid Tool
   - Phil's Book

4. **Time-box for Validation:**
   - TV Memory Layer (2 weeks)
   - ChatGPT Mobile MCP (when available)

---

## 📊 PIPELINE HEALTH

### **Current State:**
- **Active:** 8 explorations
- **Promoted (last month):** 3 (TGIF, Universal Inbox, MCP Setup)
- **Archived:** 2
- **Avg age:** ~2 weeks (healthy)
- **New today:** 2 (TGIF Issue Tracker, AI UX Principle)

### **Status:**
- ✅ **Healthy pipeline** (5-15 explorations)
- ✅ **Good graduation rate** (3 promotions recently)
- ✅ **Active innovation** (new ideas flowing)

### **Next Review:** 2025-11-23 (2 weeks)

---

## 🚀 GRADUATION CANDIDATES

### **High Priority:**
1. **Phil's Ledger Pipeline** - Very detailed, ready for PoC
2. **Weekend Soccer Advisor** - Already promoted to JH assistant

### **Medium Priority:**
3. **Joju Dropbox Miner** - Needs review
4. **Contractor Bid Tool** - Needs review

### **Low Priority:**
5. **Phil's Book** - Needs more detail
6. **TV Memory Layer** - Needs validation

---

## 📝 NOTES

### **Pattern Observed:**
- Detailed brainstorms (like Phil's Ledger, 52KB) are ready for PoC
- Brief brainstorms need more exploration
- Some explorations waiting on external factors (ChatGPT mobile)

### **Success:**
- TGIF automation went from brainstorm → exploration → PoC in <1 week
- Clear path: Idea → Exploration → PoC → Production

---

**Explorations pipeline healthy. Phil's Ledger ready for promotion. Combined brainstorms need separation.** ✅
