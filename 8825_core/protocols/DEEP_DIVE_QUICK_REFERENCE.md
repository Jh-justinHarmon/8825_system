# Deep Dive Research - Quick Reference

**Use when:** User says "deep dive", "fully understand", or mentions repeated failures

---

## 🔍 6-Phase Checklist

### ☐ Phase 1: Process Discovery
```bash
# Cast WIDE net
ps aux | grep -E "keyword1|keyword2|related|terms" | grep -v grep
ps aux -o pid,lstart,command | grep keyword  # Check start times
launchctl list | grep -i keyword
```

### ☐ Phase 2: File System Discovery
```bash
# Multiple naming patterns
find /path -name "*keyword*" -o -name "*related*"
grep -r "keyword" /path --include="*.py" --include="*.sh"
# Check ARCHIVED/EXPERIMENTAL folders
```

### ☐ Phase 3: Dependency Discovery
```bash
# Trace imports and calls
grep -r "from.*keyword" /path --include="*.py"
grep -r "import.*keyword" /path --include="*.py"
# Map the call chain
```

### ☐ Phase 4: State Discovery
```bash
# All configs
find /path -name "*config*.json" -o -name "*.conf"
# Environment vars
grep -r "export.*KEYWORD" ~/.*rc
# State files
find /path -name "*.pid" -o -name "*.lock"
```

### ☐ Phase 5: Log Discovery
```bash
# Find all logs
find /path -name "*.log"
ls /tmp/*keyword*.log
# Check contents
tail -100 /path/to/log
grep -i error /path/to/log
```

### ☐ Phase 6: Integration Discovery
```bash
# Who mentions this?
grep -r "system_name" /entire/codebase --include="*.py" --include="*.sh" --include="*.md"
# Check MCP servers, workflows
```

---

## ⚠️ Common Mistakes

- ❌ Searching too narrowly (`grep "exact_name"`)
- ✅ Cast wide net (`grep -E "related|terms|variations"`)

- ❌ Ignoring long-running processes
- ✅ Check start times (`ps aux -o lstart`)

- ❌ Assuming one system
- ✅ Keep searching until complete picture

- ❌ Ignoring archives
- ✅ Check EXPERIMENTAL/ARCHIVED folders

- ❌ Not mapping dependencies
- ✅ Trace full call chain

- ❌ Trusting documentation
- ✅ Verify actual state

---

## 📝 Documentation Requirements

1. ☐ Create `DEEP_DIVE_ANALYSIS_[DATE].md`
2. ☐ Create `PERMANENT_SOLUTION_[ISSUE].md`
3. ☐ Update README, ARCHITECTURE, TROUBLESHOOTING
4. ☐ Create memory with root cause + solution
5. ☐ Create `SYSTEM_STATUS.md`

---

## ✅ Complete Picture Checklist

Before proposing solution:

- [ ] All running processes identified
- [ ] All related files found (active + archived)
- [ ] All configuration files read
- [ ] All call chains mapped
- [ ] All logs checked
- [ ] All integrations identified
- [ ] All previous attempts documented
- [ ] Root cause identified (not symptoms)
- [ ] Architectural understanding
- [ ] Solution addresses root cause

**If you can't check all boxes, you're not done researching.**

---

## 🎯 Search Term Examples

For "Downloads sync issue":
```bash
grep -E "download|sync|watch|monitor|inbox|rsync|fswatch|watchdog|universal|daemon|agent|icloud|desktop|mobile|8825_inbox|8825_processed"
```

**Always use MULTIPLE related terms, not just exact matches.**

---

## 📊 Success Metrics

**Before Protocol:**
- 14 attempts to fix
- Incomplete analysis
- 7+ hours wasted

**After Protocol:**
- Complete system map
- Root cause identified
- 65 minutes total
- Never repeat conversation

---

**Full Protocol:** `DEEP_DIVE_RESEARCH_PROTOCOL.md`
