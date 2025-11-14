# Phase 1: Unified Startup System - Execution Plan

**Date:** 2025-11-10  
**Status:** READY FOR APPROVAL  
**Estimated Time:** 6-8 hours (can split across sessions)

---

## What We're Building

**Single command:** `8825 start`

**What it does:**
1. Validates registry (auto-updates if needed)
2. Checks dependencies (installs if missing)
3. Runs health checks (validates system)
4. Audits current state (reports status)
5. Confirms ready (green light to work)

**Result:** One ritual, full confidence.

---

## Deliverables

### **1. Registry System**
**File:** `8825_core/registry/SYSTEM_REGISTRY.json`

**Contains:**
- All daemons (what they do, dependencies, status)
- All scripts (paths, dependencies, what they touch)
- All critical paths (who touches them)
- System dependencies (python, jq, rsync, etc.)
- Component dependencies (what each script needs)

**Initial population:** Manual scan of current system

---

### **2. Startup Script**
**File:** `8825_core/registry/8825_start.sh`

**Flow:**
```bash
#!/bin/bash
# 8825 Unified Startup

echo "=== 8825 Startup Protocol ==="

# Step 1: Registry validation
./validate_registry.sh
# - Checks if registry exists
# - Scans for new scripts/daemons
# - Auto-adds to registry
# - Reports changes

# Step 2: Dependency check
./check_dependencies.sh
# - Reads registry for required deps
# - Checks if installed
# - Installs if missing
# - Reports status

# Step 3: Health check
./check_health.sh
# - Checks daemon status
# - Checks Downloads size
# - Checks BRAIN_TRANSPORT
# - Checks for conflicts
# - Reports health

# Step 4: System audit
./audit_system.sh
# - Counts components
# - Checks for duplicates
# - Reports topology
# - Confirms ready

echo "=== System Ready ==="
```

---

### **3. Registry Validation**
**File:** `8825_core/registry/validate_registry.sh`

**Does:**
```bash
# Check if registry exists
if [ ! -f SYSTEM_REGISTRY.json ]; then
    echo "Registry not found, creating..."
    ./create_registry.sh
fi

# Scan for new scripts
current_scripts=$(find ../../ -name "*.sh" -o -name "*.py")
registered_scripts=$(jq -r '.scripts[].path' SYSTEM_REGISTRY.json)

# Find differences
new_scripts=$(comm -23 <(sort current) <(sort registered))

# Auto-register new scripts
if [ -n "$new_scripts" ]; then
    echo "New scripts detected:"
    for script in $new_scripts; do
        echo "  - $script"
        ./auto_register.sh "$script"
    done
    echo "Registry updated"
fi
```

---

### **4. Dependency Checker**
**File:** `8825_core/registry/check_dependencies.sh`

**Does:**
```bash
# Read system dependencies from registry
deps=$(jq -r '.system_dependencies | keys[]' SYSTEM_REGISTRY.json)

for dep in $deps; do
    check_cmd=$(jq -r ".system_dependencies.$dep.check" SYSTEM_REGISTRY.json)
    
    if ! eval "$check_cmd" > /dev/null 2>&1; then
        echo "⚠️  $dep not installed"
        install_cmd=$(jq -r ".system_dependencies.$dep.install" SYSTEM_REGISTRY.json)
        echo "Installing $dep..."
        eval "$install_cmd"
    else
        echo "✅ $dep"
    fi
done
```

---

### **5. Health Checker**
**File:** `8825_core/registry/check_health.sh`

**Does:**
```bash
# Check daemon status
for daemon in $(jq -r '.daemons[].name' SYSTEM_REGISTRY.json); do
    if ps aux | grep -v grep | grep "$daemon" > /dev/null; then
        echo "✅ $daemon: running"
    else
        echo "✅ $daemon: stopped (expected)"
    fi
done

# Check Downloads size
downloads_size=$(du -sm ~/Downloads | cut -f1)
if [ $downloads_size -gt 100 ]; then
    echo "⚠️  Downloads: ${downloads_size}MB (cleanup recommended)"
else
    echo "✅ Downloads: ${downloads_size}MB (healthy)"
fi

# Check BRAIN_TRANSPORT
if [ -f ~/Downloads/0-8825_BRAIN_TRANSPORT.json ]; then
    echo "✅ BRAIN_TRANSPORT: Present"
else
    echo "⚠️  BRAIN_TRANSPORT: Missing"
fi

# Check for conflicts
# (Compare exclusion patterns across scripts)
```

---

### **6. Auto-Register Script**
**File:** `8825_core/registry/auto_register.sh`

**Does:**
```bash
#!/bin/bash
# Auto-register a new script

script_path=$1

# Analyze script
script_name=$(basename "$script_path")
script_type=$(file "$script_path" | grep -o "Python\|Bash")

# Extract dependencies (basic heuristics)
if grep -q "import watchdog" "$script_path"; then
    deps+=("watchdog")
fi
if grep -q "rsync" "$script_path"; then
    deps+=("rsync")
fi

# Add to registry
jq ".scripts += [{
    \"name\": \"$script_name\",
    \"path\": \"$script_path\",
    \"type\": \"$script_type\",
    \"dependencies\": $deps,
    \"added\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
}]" SYSTEM_REGISTRY.json > tmp.json && mv tmp.json SYSTEM_REGISTRY.json

echo "Registered: $script_name"
```

---

### **7. Symlink to PATH**
```bash
# Make accessible from anywhere
sudo ln -s /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 3.0/8825_core/registry/8825_start.sh /usr/local/bin/8825
```

**Usage:**
```bash
# From anywhere
8825 start
```

---

## Implementation Steps

### **Step 1: Create Registry Structure (1 hour)**
1. Create `8825_core/registry/` directory
2. Create `SYSTEM_REGISTRY.json` with schema
3. Manually populate with current components:
   - 2 daemons (downloads_sync, inbox_sync)
   - ~47 scripts (from INBOX_HUB, 8825_core/sync, etc.)
   - 8 critical paths (Downloads, inbox, etc.)
   - System dependencies (python, jq, rsync, watchdog)

---

### **Step 2: Build Core Scripts (3-4 hours)**
1. `8825_start.sh` - main startup orchestrator
2. `validate_registry.sh` - registry validation
3. `check_dependencies.sh` - dependency checking
4. `check_health.sh` - health checks
5. `auto_register.sh` - auto-registration
6. `audit_system.sh` - system audit

---

### **Step 3: Test & Refine (1-2 hours)**
1. Run `8825 start` on clean system
2. Verify all checks pass
3. Test auto-registration (create dummy script)
4. Test dependency installation (remove jq, run startup)
5. Test health checks (bloat Downloads, run startup)
6. Refine output formatting

---

### **Step 4: Document & Deploy (1 hour)**
1. Create `8825_core/registry/README.md`
2. Document usage patterns
3. Add to `.windsurf/workflows/`
4. Create symlink to PATH
5. Test from different directories

---

## Success Criteria

### **Must Have:**
- [ ] `8825 start` runs without errors
- [ ] Registry auto-updates when new scripts added
- [ ] Dependencies auto-install when missing
- [ ] Health checks detect daemon status correctly
- [ ] Health checks detect Downloads bloat correctly
- [ ] BRAIN_TRANSPORT presence verified
- [ ] Command accessible from anywhere via PATH

### **Nice to Have:**
- [ ] Colored output (green/yellow/red)
- [ ] Progress indicators
- [ ] Estimated time for dependency installs
- [ ] Summary at end (X/Y checks passed)

---

## Risks & Mitigations

### **Risk 1: Auto-registration misses dependencies**
**Impact:** Medium - script might fail later
**Mitigation:** Start with basic heuristics, refine over time
**Fallback:** Manual registry updates still possible

### **Risk 2: Dependency installation fails**
**Impact:** Medium - system not ready
**Mitigation:** Catch errors, report clearly, continue with other checks
**Fallback:** User can install manually

### **Risk 3: Registry gets out of sync**
**Impact:** Low - startup will catch and fix
**Mitigation:** Auto-validation on every startup
**Fallback:** Manual registry rebuild script

### **Risk 4: Startup takes too long**
**Impact:** Low - annoying but not breaking
**Mitigation:** Run checks in parallel where possible
**Fallback:** Add `--quick` flag for fast startup

---

## Testing Plan

### **Test 1: Fresh System**
1. Delete registry
2. Run `8825 start`
3. Verify registry created
4. Verify all components found

### **Test 2: New Component**
1. Create `test_script.sh`
2. Run `8825 start`
3. Verify script auto-registered
4. Verify dependencies detected

### **Test 3: Missing Dependency**
1. Uninstall `jq`
2. Run `8825 start`
3. Verify detection
4. Verify auto-install
5. Verify success

### **Test 4: Unhealthy System**
1. Start downloads_sync daemon
2. Bloat Downloads to 200MB
3. Run `8825 start`
4. Verify warnings shown
5. Verify recommendations given

### **Test 5: From Different Directory**
1. `cd ~`
2. Run `8825 start`
3. Verify works from anywhere

---

## Post-Implementation

### **Daily Usage:**
```bash
# Every morning
8825 start

# Before any work session
8825 start

# After pulling changes
8825 start
```

### **When Adding New Components:**
```bash
# Create new script
vim new_tool.sh

# Next startup auto-registers
8825 start
# → "New script detected: new_tool.sh"
# → "Analyzing dependencies..."
# → "Added to registry"
```

### **Monitoring:**
```bash
# Check registry
cat 8825_core/registry/SYSTEM_REGISTRY.json | jq '.scripts | length'
# → 48 scripts registered

# Check health
8825 start | grep "Health:"
# → Overall Health: GOOD
```

---

## Next Steps After Phase 1

**If successful:**
- Phase 2: Add `8825 audit` commands
- Phase 3: Add `8825 impact` analysis
- Phase 4: Brain integration

**If issues:**
- Refine Phase 1
- Address pain points
- Adjust approach

---

## Approval Checklist

Before proceeding, confirm:
- [ ] Approach makes sense
- [ ] Deliverables are clear
- [ ] Effort estimate is reasonable (6-8 hours)
- [ ] Success criteria are achievable
- [ ] Risks are acceptable
- [ ] Testing plan is sufficient
- [ ] Ready to execute

---

**Ready to build?**
