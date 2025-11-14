# 8825 System Workflows

**Version:** 3.1.0  
**Last Updated:** 2025-11-13

Common operations and workflows for the 8825 system.

---

## 🚀 Starting a New POC/Experiment

### 1. Create in Sandbox
```bash
cd sandbox/experimental
mkdir my-new-feature
cd my-new-feature

# Create basic structure
touch README.md
touch requirements.txt  # or package.json
```

### 2. Build and Test
Work on your POC in `sandbox/experimental/`

### 3. When Ready to Graduate
```bash
# Move to graduated
mv sandbox/experimental/my-feature sandbox/graduated/

# Or use the audit tool to check readiness
./8825_core/system/8825_audit_poc.sh
```

---

## 📊 Auditing POCs

### Check All POCs
```bash
cd /path/to/8825-system
./8825_core/system/8825_audit_poc.sh
```

**Output:**
- 🟢 READY - Score 80-100, ready to promote
- 🟡 ALMOST - Score 50-79, needs more work
- 🔴 NOT READY - Score 0-49, keep or delete

### Criteria Checked:
- Stability (14+ days since last change)
- Documentation (has README)
- Production use (referenced in code)
- Requirements file
- Tests

---

## 🎓 Promoting a POC

### Manual Promotion
```bash
./8825_core/system/promote_poc.sh <source> <destination>

# Examples:
./8825_core/system/promote_poc.sh sandbox/graduated/my-feature shared/automations
./8825_core/system/promote_poc.sh sandbox/graduated/hcss-tool focuses/hcss/workflows
```

### Promotion Destinations:
- `shared/automations` - Cross-focus automations
- `shared/templates` - Reusable templates
- `shared/libraries` - Shared code
- `focuses/{name}/workflows` - Focus-specific
- `core/pipelines` - Universal pipelines
- `core/integrations` - Universal integrations

### What Happens:
1. POC moved to destination
2. `.PROMOTION` metadata created
3. References checked
4. Confirmation required

---

## 🔒 Multi-Cascade Operations

### Before System-Wide Changes
```bash
# Check if another Cascade is working
./8825_core/system/cascade_lock.sh check

# Acquire lock (prevents conflicts)
./8825_core/system/cascade_lock.sh acquire "my operation"

# Do your work...

# Release lock
./8825_core/system/cascade_lock.sh release
```

### Lock Features:
- 15-minute auto-unlock
- Shows who has lock
- Force unlock option (use with caution)

---

## 🗑️ Deleting Items

### Always Log Deletions
```bash
# Log before deleting
./8825_core/system/log_deletion.sh "/path/to/item" "reason" "high"

# Then delete
rm -rf /path/to/item
```

### View Deletion Log
```bash
cat migrations/deleted_items_log.json
```

---

## 📦 Adding a New Focus

### 1. Create Structure
```bash
cd focuses
mkdir new-focus
cd new-focus

mkdir knowledge projects workflows

# Create README
cat > README.md << 'EOF'
# New Focus

Purpose: [Describe the focus]

## Contents
- knowledge/ - Focus-specific documentation
- projects/ - Active projects
- workflows/ - How things work
EOF
```

### 2. Create User Data Symlink
```bash
# From within the focus directory
ln -s ../../users/justin_harmon/new-focus user_data
```

### 3. Update Focus README
Edit `focuses/README.md` to include the new focus.

---

## 🔄 Moving Items Between Layers

### Experimental → Graduated
```bash
# When POC is stable and working
mv sandbox/experimental/my-poc sandbox/graduated/my-poc
```

### Graduated → Shared
```bash
# Use promotion helper
./8825_core/system/promote_poc.sh sandbox/graduated/my-poc shared/automations
```

### Shared → Core
```bash
# Only when truly universal
# Manual move + update references
mv shared/automations/universal-thing core/integrations/
```

### Focus-Specific → Shared
```bash
# When becomes cross-focus
./8825_core/system/promote_poc.sh focuses/hcss/workflows/automation shared/automations
```

---

## 📋 Monthly Maintenance

### 1. Audit POCs
```bash
./8825_core/system/8825_audit_poc.sh

# Review output:
# - Promote ready POCs
# - Delete abandoned POCs
# - Graduate almost-ready POCs
```

### 2. Check for Duplicates
```bash
# Find duplicate Python files
find . -name "*.py" -type f -exec basename {} \; | sort | uniq -d

# Find duplicate directories
find . -type d -name "*automation*" | sort
```

### 3. Archive Completed Work
```bash
# Move completed projects to archive
mv focuses/hcss/projects/completed-project migrations/completed-projects/
```

### 4. Update Documentation
- Update README files
- Archive outdated docs
- Review and update ARCHITECTURE.md

---

## 🔍 Finding Things

### Where Does X Belong?

**Is it system-essential?** → `core/`
- Required by all focuses
- Universal integrations
- System-wide protocols

**Is it used by 2+ focuses?** → `shared/`
- Cross-focus automations
- Shared templates
- Common libraries

**Is it focus-specific?** → `focuses/{name}/`
- Client-specific code
- Focus-specific workflows
- Focus knowledge

**Is it experimental?** → `sandbox/`
- New ideas
- POCs
- Not yet stable

**Is it user-specific?** → `users/justin_harmon/`
- Personal data
- User preferences
- User-specific workflows

### Quick Search
```bash
# Find by name
find . -name "*automation*" -type d

# Find by content
grep -r "function_name" --include="*.py"

# Find recent changes
find . -type f -mtime -7  # Modified in last 7 days
```

---

## 📝 Version Management

### Check Current Version
```bash
cat version.json | grep system_version
```

### After Major Changes
```bash
# Update version.json
# Add migration entry
# Update release notes
```

### Version Numbering:
- **Major (3.x.x)** - Architecture changes
- **Minor (x.1.x)** - New features/systems
- **Patch (x.x.1)** - Bug fixes/cleanup

---

## 🐛 Common Issues

### "Another Cascade is making changes"
```bash
# Check lock status
./8825_core/system/cascade_lock.sh check

# If stale (>15 min), will auto-remove
# Or force unlock (careful!)
./8825_core/system/cascade_lock.sh force-unlock
```

### "Can't find promoted POC"
```bash
# Check promotion metadata
cat shared/automations/poc-name/.PROMOTION

# Check deletion log
cat migrations/deleted_items_log.json | grep poc-name
```

### "Path references broken"
```bash
# Find old references
grep -r "old/path" --include="*.py" --include="*.md"

# Update references
find . -type f -exec sed -i '' 's|old/path|new/path|g' {} \;
```

---

## 🎯 Best Practices

### Always:
- ✅ Start new work in `sandbox/experimental/`
- ✅ Use Cascade lock for system-wide changes
- ✅ Log deletions before deleting
- ✅ Create README for new POCs
- ✅ Test after promotion

### Never:
- ❌ Put version numbers in paths
- ❌ Duplicate code across layers
- ❌ Skip POC audit before promotion
- ❌ Leave production code in sandbox
- ❌ Make system changes without lock

### Monthly:
- 📊 Run POC audit
- 🗑️ Clean up abandoned POCs
- 📁 Archive completed work
- 📚 Update documentation

---

## 🚀 Quick Reference

```bash
# Audit POCs
./8825_core/system/8825_audit_poc.sh

# Promote POC
./8825_core/system/promote_poc.sh <source> <dest>

# Check Cascade lock
./8825_core/system/cascade_lock.sh check

# Log deletion
./8825_core/system/log_deletion.sh <path> <reason> <confidence>

# Check version
cat version.json

# Launch system
launch_8825
```

---

**For detailed architecture, see:** `ARCHITECTURE.md`  
**For refactor history, see:** `REFACTOR_MASTER_PLAN.md`  
**For specific focus docs, see:** `focuses/{focus}/README.md`
