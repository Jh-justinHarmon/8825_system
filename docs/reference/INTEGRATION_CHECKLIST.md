# Integration Update Checklist

**Purpose:** When adding/fixing any integration, use this checklist to ensure all documentation and systems are updated.

**Created:** November 10, 2025  
**Based on:** Notion task integration debugging session

---

## 📋 Complete Update Checklist

### 1. ✅ Fix the Code
- [ ] Identify and fix the root cause
- [ ] Add error handling
- [ ] Add fallbacks for variations
- [ ] Lock dependency versions in requirements.txt
- [ ] Test the fix thoroughly

### 2. ✅ Local Documentation (Component Level)
- [ ] **README.md** - Add critical warnings at top
- [ ] **QUICKSTART.md** - Add prerequisites section
- [ ] **SETUP.md** - Update setup instructions
- [ ] **TROUBLESHOOTING.md** - Document all errors encountered
- [ ] **requirements.txt** - Lock all SDK versions with comments
- [ ] Create **LESSONS_LEARNED.md** - Document what went wrong
- [ ] Create **[COMPONENT]_SETUP_COMPLETE.md** - Full history

### 3. ✅ Validation Tools
- [ ] Create **check_setup.sh** - Automated validation script
  - Check dependencies
  - Verify configuration
  - Test connectivity
  - Provide actionable errors
- [ ] Make executable: `chmod +x check_setup.sh`

### 4. ✅ System-Wide Documentation
- [ ] **DEVELOPER_GUIDE.md** - Add to prerequisites section
- [ ] **ADMIN_GUIDE.md** - Add detailed setup section
- [ ] **STARTUP_AUTOMATION.md** - Add to dependencies
- [ ] **API_REFERENCE.md** - Document any new APIs
- [ ] **ARCHITECTURE.md** - Update if architecture changed

### 5. ✅ Integration Points
- [ ] **MCP servers** - Update if they use the integration
- [ ] **MCP documentation** - Add prerequisites
- [ ] **Startup scripts** - Add validation checks
- [ ] **Related components** - Update anything that depends on it

### 6. ✅ Startup & Automation
- [ ] **start_all_mcps.sh** - Add setup validation
- [ ] **check_dependencies.sh** - Add new dependencies
- [ ] **LaunchAgents** - Update if needed
- [ ] Test startup sequence

### 7. ✅ Learning Loop
- [ ] **Create Memory** - For AI assistants
  - Critical requirements
  - Common errors
  - Solutions
  - Setup steps
- [ ] **Tag appropriately** - For easy retrieval

### 8. ✅ Cross-References
- [ ] Link between related docs
- [ ] Add "See also" sections
- [ ] Update main README if significant
- [ ] Update DOCUMENTATION_INDEX.md

---

## 🎯 Specific File Locations to Check

### Always Update These:
```
/DEVELOPER_GUIDE.md
/STARTUP_AUTOMATION.md
/[component]/README.md
/[component]/QUICKSTART.md
/[component]/requirements.txt
```

### Often Update These:
```
/ADMIN_GUIDE.md (if in 8825_core/integrations/goose/)
/API_REFERENCE.md (if new APIs)
/ARCHITECTURE.md (if structure changed)
/start_all_mcps.sh (if MCP-related)
/[component]/TROUBLESHOOTING.md
```

### Create If Missing:
```
/[component]/check_setup.sh
/[component]/LESSONS_LEARNED.md
/[component]/[INTEGRATION]_SETUP_COMPLETE.md
/[component]/TROUBLESHOOTING.md
```

---

## 🔍 Common Integration Issues to Document

### SDK Version Issues
- [ ] Lock version in requirements.txt
- [ ] Document why specific version needed
- [ ] Add version check to setup script
- [ ] Document breaking changes

### Configuration Issues
- [ ] Document where config files are
- [ ] Document where credentials are stored
- [ ] Add config validation
- [ ] Provide example configs

### Property/Schema Mismatches
- [ ] Add fallbacks in code
- [ ] Document actual schema
- [ ] Document expected schema
- [ ] Add schema validation

### Connection Issues
- [ ] Add connection testing
- [ ] Document common errors
- [ ] Provide diagnostic commands
- [ ] Add retry logic

---

## 📝 Documentation Template

### For Each Integration, Create:

#### 1. [INTEGRATION]_SETUP_COMPLETE.md
```markdown
# [Integration] Setup Complete

**Date:** [Date]
**Status:** [Status]

## What Was Done
- List all fixes
- List all changes
- List all files updated

## Current Status
- Connection details
- Statistics
- Last sync

## How to Use
- Setup steps
- Testing steps
- Common commands

## Troubleshooting
- Common errors
- Solutions
- Diagnostic commands
```

#### 2. TROUBLESHOOTING.md
```markdown
# [Component] Troubleshooting

## Common Issues

### 1. [Error Message]
**Error:** [Exact error]
**Cause:** [Why it happens]
**Solution:** [How to fix]

### 2. [Next Error]
...
```

#### 3. LESSONS_LEARNED.md
```markdown
# [Integration] Lessons Learned

## The Problem
[What went wrong]

## Root Causes
[Why it happened]

## Solutions Implemented
[What we did]

## Best Practices
[What to do next time]

## Time Investment
[Time spent vs saved]
```

---

## 🎓 Learning Loop Integration

### Create Memory With:
- **Title:** Clear, searchable title
- **Content:** 
  - Critical requirements
  - Common errors with solutions
  - Setup steps
  - Files updated
- **Tags:** Component, issue type, technology
- **Corpus:** Workspace path
- **UserTriggered:** true (if user requested)

### Memory Template:
```
[Component] [Integration] requires specific setup:

**Critical Requirements:**
1. [Requirement 1]
2. [Requirement 2]

**Common Errors:**
- "[Error]" = [Solution]

**Setup Steps:**
1. [Step 1]
2. [Step 2]

**Files Updated:**
- [File 1]
- [File 2]
```

---

## ⚡ Quick Reference

### When You Fix Something:

**Immediate (Do First):**
1. Fix the code
2. Test it works
3. Lock versions

**Short-term (Do Same Day):**
4. Update local docs (README, QUICKSTART)
5. Create troubleshooting guide
6. Create setup checker

**Medium-term (Do Same Session):**
7. Update system-wide docs
8. Update related components
9. Update startup scripts

**Long-term (Before Closing):**
10. Create memory
11. Create lessons learned
12. Update checklist if needed

---

## 🚨 Red Flags That Mean You Need to Update Docs

- [ ] You had to search for credentials
- [ ] You got an error about missing dependencies
- [ ] You had to try multiple SDK versions
- [ ] Configuration wasn't obvious
- [ ] Error messages weren't clear
- [ ] You had to debug for >10 minutes
- [ ] You found the solution in old code
- [ ] Setup wasn't validated automatically

**If ANY of these happened, update the docs!**

---

## 📊 Documentation Quality Checklist

### Good Documentation Has:
- [ ] Clear warnings at the top
- [ ] Exact error messages
- [ ] Copy-paste solutions
- [ ] Links to related docs
- [ ] Diagnostic commands
- [ ] Version requirements
- [ ] Setup validation
- [ ] Common issues section

### Great Documentation Also Has:
- [ ] Automated setup checker
- [ ] Lessons learned
- [ ] Time investment analysis
- [ ] Memory for AI assistants
- [ ] Cross-references everywhere
- [ ] Examples of what went wrong
- [ ] Why each requirement exists

---

## 🎯 Success Metrics

### You Know Docs Are Good When:
- Setup takes <5 minutes with docs
- Setup takes >30 minutes without docs
- No questions from team members
- No repeated debugging
- AI assistants remember it
- New team members succeed alone

### Calculate ROI:
```
Time Spent Documenting: [X] minutes
Time Saved Per Setup: [Y] minutes
Expected Setups: [Z] times
Total Saved: Y × Z minutes
ROI: (Y × Z) / X
```

**Aim for 2x ROI minimum**

---

## 🔄 Maintenance

### Review This Checklist:
- After each integration issue
- When onboarding new team members
- Quarterly
- When documentation fails

### Update This Checklist:
- Add new file locations
- Add new common issues
- Add new documentation types
- Remove outdated items

---

## 📚 Related Resources

- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Development standards
- [STARTUP_AUTOMATION.md](STARTUP_AUTOMATION.md) - Startup procedures
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - All docs
- [focuses/joju/tasks/LESSONS_LEARNED.md](focuses/joju/tasks/LESSONS_LEARNED.md) - Example

---

## 💡 Pro Tips

1. **Document as you debug** - Don't wait until the end
2. **Copy exact error messages** - Makes searching easier
3. **Lock all versions** - Prevents future breaks
4. **Create setup checkers** - Catches issues early
5. **Link everything** - Easy navigation
6. **Use templates** - Consistency
7. **Create memories** - AI learns
8. **Calculate ROI** - Justify time spent

---

**Remember: If you had to figure it out, document it. Your future self will thank you!** 🎯

---

**Last Updated:** November 10, 2025  
**Next Review:** After next integration issue
