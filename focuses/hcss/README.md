# HCSS Focus

**Projects:** HCSS, RAL, TGIF  
**Status:** Active Development

---

## 📁 STRUCTURE

```
focuses/hcss/
├── README.md                    # This file
├── poc/                         # Proof of Concept bucket
│   ├── README.md               # PoC overview
│   └── tgif_automation/        # TGIF automation PoC
├── production/                  # Production deployments (future)
├── workflows/                   # Workflow documentation
├── knowledge/                   # Knowledge base (meetings, emails, tasks)
├── projects/                    # Project definitions
└── mcp_server/                 # MCP server (if applicable)
```

---

## 🎯 ACTIVE PROJECTS

### **1. TGIF Meeting Automation** 🟡 PoC Phase

**Location:** `poc/tgif_automation/`  
**Status:** Ready for Validation  
**Start Date:** 2025-11-09  
**Target Production:** 2025-12-07

**What It Does:**
- Processes TGIF meeting transcripts from Otter.ai
- Processes flagged emails daily (12pm)
- Tracks action items across all sources
- Generates weekly digest (Friday 3pm)

**Next Steps:**
1. Setup environment (see `poc/tgif_automation/QUICKSTART.md`)
2. Run for 2 weeks
3. Collect feedback
4. Refine and deploy to production

**Documentation:**
- [PoC Overview](poc/README.md)
- [Quick Start](poc/tgif_automation/QUICKSTART.md)
- [Full Documentation](poc/tgif_automation/README.md)
- [PoC Status](poc/tgif_automation/POC_STATUS.md)

---

### **2. RAL Portal Management** 📋 Planning

**Status:** Documentation phase  
**Projects:** RAL governance, invoice tracking

**Documentation:**
- `8825_core/projects/8825_HCSS-RAL.json`

---

## 🚀 POC BUCKET

The `poc/` directory is where new HCSS projects are validated before production:

**Purpose:**
- Test with real data
- Validate workflows
- Collect feedback
- Refine before production

**Current PoCs:**
1. ✅ TGIF Automation (ready for validation)

**See:** `poc/README.md` for full PoC process

---

## 📊 PRODUCTION

**Status:** No production deployments yet

Once PoCs are validated, they move to `production/`:
```
focuses/hcss/production/
└── tgif_automation/  (future)
```

---

## 📚 DOCUMENTATION

### **Workflows:**
- `workflows/tgif_meeting_automation.md` - Full pipeline spec
- `workflows/TGIF_OUTPUT_AND_ROLLUP_ARCHITECTURE.md` - Architecture
- `workflows/TGIF_DAILY_EMAIL_PROCESSING.md` - Daily processing
- `workflows/OTTER_API_RISK_ANALYSIS.md` - Risk mitigation

### **Projects:**
- `8825_core/projects/8825_HCSS-TGIF.json` - TGIF project definition
- `8825_core/projects/8825_HCSS-RAL.json` - RAL project definition

### **Protocols:**
- `8825_core/protocols/8825_hcss_focus.json` - HCSS focus protocol

---

## 🎯 GETTING STARTED

### **For TGIF Automation:**

1. **Read the docs:**
   ```bash
   cat poc/README.md
   cat poc/tgif_automation/QUICKSTART.md
   ```

2. **Setup:**
   ```bash
   cd poc/tgif_automation
   # Follow QUICKSTART.md
   ```

3. **Monitor:**
   - Check `POC_STATUS.md` for progress
   - Log issues in `ISSUES.md`
   - Document learnings in `LEARNINGS.md`

---

## 📞 CONTACTS

**Focus Owner:** Justin Harmon  
**Projects:**
- TGIF: Justin Harmon
- RAL: Justin Harmon
- HCSS: Justin Harmon

---

**HCSS Focus active. Start with `poc/README.md`** ✅
