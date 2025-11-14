# 8825 v3.1 - Layered Architecture

**Version:** 3.1.0  
**Codename:** Layered Architecture  
**Status:** ✅ **Production Ready**  
**Created:** 2025-11-07  
**Last Updated:** 2025-11-13

---

## 🎯 What is v3.1?

v3.1 implements a **layered promotion-based architecture** with clear paths from experimentation to production:

### Key Features
- ✅ **Layered Structure** - Clear L0-L4 promotion system
- ✅ **Zero Duplicates** - One canonical location per resource
- ✅ **POC Management** - Automated auditing and promotion
- ✅ **Version Agnostic** - No version numbers in paths
- ✅ **Multi-Cascade Safe** - Lock system prevents conflicts
- ✅ **Fast Discovery** - Find anything in <30 seconds
- ✅ **MCP Consolidated** - All servers in ~/mcp_servers/

### Layers
- **L0 - Sandbox:** Experiments (experimental → graduated)
- **L1 - Users:** User-specific data
- **L2 - Focuses:** Focus-specific production (hcss, joju, jh_assistant, team76)
- **L3 - Shared:** Cross-focus resources (automations, templates, libraries)
- **L4 - Core:** Universal system essentials

**Promotion Flow:** `sandbox → shared/focuses → core`

---

## 🚀 Quick Start

### **New Users: Installation**

```bash
# 1. Run installation
./scripts/install.sh

# 2. Add OpenAI API key
nano .env  # Add your sk-proj-... key

# 3. Run onboarding
./scripts/onboard.sh

# 4. Get started
source venv/bin/activate
python3 8825_core/agents/accountability_loop_agent.py --list
```

**See:** `QUICKSTART.md` for 5-minute guide | `INSTALLATION.md` for details

### **Existing Users: Launch System**

```bash
launch_8825
```

### Manage POCs
```bash
# Audit POC readiness
audit-pocs

# Promote a POC
promote-poc sandbox/graduated/my-feature shared/automations

# Check Cascade lock
check-lock
```

---

## 📚 Documentation

### Essential Guides
- **[WORKFLOWS](WORKFLOWS.md)** - Complete operational guide ⭐
- **[ARCHITECTURE](ARCHITECTURE.md)** - System architecture
- **[Refactor Summary](migrations/REFACTOR_COMPLETE_2025-11-13.md)** - v3.1 changes

### Layer Guides
- **[Core](core/README.md)** - Universal essentials
- **[Shared](shared/README.md)** - Cross-focus resources
- **[Sandbox](sandbox/README.md)** - Experiments & POCs
- **[Focuses](focuses/README.md)** - Focus-specific work

### Tools
- **POC Auditor:** `./8825_core/system/8825_audit_poc.sh`
- **Promotion Helper:** `./8825_core/system/promote_poc.sh`
- **Cascade Lock:** `./8825_core/system/cascade_lock.sh`
- **Version Info:** `cat version.json`

---

## 📁 Architecture

```
8825-system/
├── core/                   # L4: Universal essentials
│   ├── pipelines/
│   ├── integrations/
│   ├── protocols/
│   └── utilities/
├── shared/                 # L3: Cross-focus resources
│   ├── automations/        # TGIF automation lives here
│   ├── templates/
│   └── libraries/
├── sandbox/                # L0: Experiments
│   ├── experimental/       # Active POCs
│   └── graduated/          # Ready to promote
├── focuses/                # L2: Focus-specific
│   ├── hcss/              # Client work
│   ├── joju/              # App development
│   ├── jh_assistant/      # Personal assistant
│   └── team76/            # Platform work
├── users/                  # L1: User data
│   └── justin_harmon/
├── 8825_core/              # System infrastructure
│   ├── protocols/          # 13 protocols
│   ├── agents/             # 18 agents
│   ├── workflows/          # Ingestion, mining, etc.
│   ├── integrations/       # MCP server, Goose
│   └── templates/          # Focus/user templates
│
├── 8825_index/             # Fast discovery layer
│   ├── master_index.json   # All files
│   ├── concept_index.json  # Cross-focus concepts
│   └── refs_graph.json     # Knowledge graph
│
├── users/                  # Private user data
│   └── justin_harmon/
│       ├── profile.json    # User profile
│       ├── .env            # Credentials (not committed)
│       ├── joju/           # Joju focus data
│       ├── hcss/           # HCSS focus data
│       └── jh_assistant/   # Jh focus data
│
└── focuses/                # Symlinked workspaces
    ├── joju@ → users/justin_harmon/joju/
    ├── hcss@ → users/justin_harmon/hcss/
    └── jh_assistant@ → users/justin_harmon/jh_assistant/
```

---

## 🚀 Quick Start:

### **1. Setup User Environment:**
```bash
cd users/justin_harmon
cp .env.template .env
# Edit .env with your credentials
```

### **2. Activate a Focus:**
```bash
cd focuses/joju
# Work here - system reads from users/justin_harmon/joju/
```

### **3. Search the System:**
```bash
# Fast index-based search
python3 8825_core/workflows/search.py "achievement of fact"
# Returns results in <1 second
```

---

## 📊 Migration Status:

| Component | v2.0 → v3.0 | Status |
|-----------|-------------|--------|
| **Core System** | Refactoring | ✅ Complete |
| **Agents** | 18 agents | ✅ Complete |
| **Protocols** | 17 protocols | ✅ Complete |
| **Workflows** | 6 flows | ✅ Complete |
| **User Data** | Extraction | ✅ Complete |
| **Index** | Build | ✅ Complete |
| **Testing** | Validation | ✅ **Complete (2025-11-09)** |

---

## ✅ Key Improvements from v2.0:

### **1. User/System Separation:**
- **v2.0:** 0% (user data embedded everywhere)
- **v3.0:** 100% (complete separation)

### **2. Code Duplication:**
- **v2.0:** 3x (gmail, mining, dedup)
- **v3.0:** 1x (single implementations)

### **3. Discovery Speed:**
- **v2.0:** Slow (grep required)
- **v3.0:** <1 second (index-based)

### **4. Portability:**
- **v2.0:** 0% (hardcoded paths)
- **v3.0:** 100% (environment variables)

### **5. Shareability:**
- **v2.0:** 0% (credentials exposed)
- **v3.0:** 100% (shareable core)

---

## 📋 Migration Plan:

### **Phase 1: Core (Week 1)**
- Copy & refactor core system files
- Copy & refactor agents
- Copy & refactor workflows

### **Phase 2: User Data (Week 2)**
- Extract Joju user data
- Extract HCSS user data
- Extract Jh user data

### **Phase 3: Focuses (Week 2)**
- Create symlinked workspaces
- Test focus activation

### **Phase 4: Index (Week 3)**
- Build master index
- Build concept index
- Build refs graph

### **Phase 5: Test (Week 4)**
- Validate each focus
- Test workflows
- Measure metrics

---

## 🎯 Validation Metrics:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Discovery Speed | <1 sec | **2.3ms** | ✅ **434x faster** |
| Share Success | 100% | 95%+ | ✅ Validated |
| Code Duplication | 0 | 0 | ✅ Validated |
| Files Indexed | 133 | **266** | ✅ **2x more** |
| MCPs Running | 3 | 3 | ✅ Validated |
| Test Pass Rate | 95% | **100%** | ✅ Exceeded |

---

## 🧪 Testing & Validation:

**Comprehensive testing completed 2025-11-09:**
- **Test Report:** `TEST_REPORT_2025-11-09.md`
- **Performance Tests:** `test_performance.py`
- **Index Validation:** `test_index_integrity.py`

**Results:**
- 47 tests run, 47 passed (100% success rate)
- Query performance: 2.3ms average (434x faster than target)
- All 3 MCPs operational and validated
- 266 files indexed across all focuses

---

## 📖 Documentation:

- **Test Report:** `TEST_REPORT_2025-11-09.md` ✅
- **Message Counter Protocol:** `8825_core/protocols/8825_message_counter_protocol.json` ✅
- **User Guide:** `docs/USER_GUIDE.md` ✅
- **Phase 3 Brain:** `PHASE3_COMPLETE.md` ✅
- **Brain Usage:** `8825_core/brain/USAGE.md` ✅
- **Developer Guide:** `docs/DEVELOPER_GUIDE.md` (coming soon)
- **Migration Guide:** `docs/MIGRATION_GUIDE.md` (coming soon)
- **API Reference:** `docs/API_REFERENCE.md` (coming soon)

---

## 🔗 Related Versions:

- **v1.0:** Original knowledge base and governance
- **v2.0:** Unified base (source for v3.0 migration)
- **v2.1:** Advanced features (archived after migration)

---

## ⚠️ Important Notes:

### **v2.0 Remains Untouched:**
- v2.0 is the production system during v3.0 development
- No changes to v2.0 during migration
- v3.0 reads from v2.0, writes to v3.0

### **Credentials:**
- `.env` files are NOT committed
- Add `.env` to `.gitignore`
- Use `.env.template` for reference

### **Symlinks:**
- `focuses/` contains symlinks to `users/{user_id}/`
- Work in `focuses/`, data stored in `users/`

---

## 🚀 Status:

**Current Phase:** ✅ **Production Ready (Validated)**  
**Completed:** All 6 phases + comprehensive testing  
**Test Date:** 2025-11-09  
**v2.0 Impact:** Zero (v2.0 remains untouched)  

**v3.0 is production-ready and fully validated!** ✅🎯

**See:** `TEST_REPORT_2025-11-09.md` for complete validation results.
