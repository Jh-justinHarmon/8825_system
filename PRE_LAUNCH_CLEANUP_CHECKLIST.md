# Pre-Launch Cleanup Checklist

**Status:** In Progress
**Date:** November 14, 2025
**Goal:** Remove all secrets, personal data, and client information before open source launch

---

## ✅ COMPLETED

### Licensing
- [x] Created LICENSE (Apache 2.0)
- [x] Created NOTICE file
- [x] Updated .gitignore with comprehensive rules

---

## 🔴 CRITICAL - MUST DELETE BEFORE LAUNCH

### Client Data (NDA/Confidential)

**HCSS Client Data:**
```
DELETE:
- /8825_core/projects/8825_HCSS*.json (3 files)
- /8825_core/protocols/8825_hcss_focus.json
- /8825_core/system/8825_HCSS_core.json
- /8825_core/workflows/HCSS_CALENDAR_SYNC_SETUP.md
- /8825_core/workflows/hcss_calendar_sync.md
- /8825_core/workflows/hcss_calendar_templates.md
- /8825_core/workflows/process_hcss_meetings.sh
- /8825_core/workflows/sync_hcss_calendar.sh
- /8825_index/hcss_index.json
- /focuses/hcss/ (entire directory)
- /users/justin_harmon/hcss/ (entire directory)
- /mcp_migration_backup_20251113_110156/hcss-bridge/ (entire directory)

KEEP (as examples, but scrub client names):
- Calendar sync workflow (rename to generic "calendar_sync_example.md")
- Meeting automation (rename to generic "meeting_automation_example.md")
```

**TGIF Client Data:**
```
DELETE:
- /8825_core/projects/8825_HCSS-TGIF.json
- /shared/automations/tgif/ (entire directory)
```

**Personal User Data:**
```
DELETE:
- /users/justin_harmon/ (entire directory except .env.template)
- /INBOX_HUB/users/jh/ (entire directory)
- /focuses/*/knowledge/ (all knowledge directories)
- /focuses/*/user_engagement/ (all user engagement data)
```

**Email/Personal Communications:**
```
DELETE:
- /8825_core/explorations/email_inspiration/email_inspiration.json
- Any files containing harmon.justin@gmail.com data
- Any files containing jkl.7247.ap@gmail.com data
```

---

## ⚠️ IMPORTANT - SCRUB BEFORE LAUNCH

### Hardcoded Paths
```
SEARCH & REPLACE in all files:
- "/Users/justinharmon/" → "${HOME}/" or "${SYSTEM_ROOT}/"
- "justinharmon" → "${USER_NAME}" or generic examples
- Specific Dropbox paths → generic examples
```

**Files with hardcoded paths (45 files found):**
- All files in /8825_core/content_index/
- All files in /INBOX_HUB/ARCHIVED_REDUNDANT_SYSTEMS_20251111/
- Various scripts and Python files

### API Keys & Secrets
```
VERIFY REMOVED (already in docs/examples only):
- OpenAI API keys (sk-*)
- Gmail app passwords
- Google credentials
- Reddit API keys
```

**Status:** Appears clean - only found in documentation/templates

---

## 📝 DOCUMENTATION TO UPDATE

### Public-Facing Docs
```
UPDATE:
- README.md - Remove Justin-specific examples
- QUICKSTART.md - Use generic examples
- INSTALLATION.md - Remove personal paths
- ARCHITECTURE.md - Create (doesn't exist yet)
```

### Example Workflows
```
CREATE GENERIC EXAMPLES:
- calendar_sync_example.md (from HCSS calendar sync)
- meeting_automation_example.md (from HCSS meeting automation)
- email_monitoring_example.md (from Phil's Ledger concept)
```

---

## 🧪 TESTING REQUIRED

### Before Launch
```
TEST:
1. Fresh clone in new directory
2. Run installation as new user
3. Verify no hardcoded paths break
4. Verify no secrets exposed
5. Verify all examples work with generic data
```

---

## 📊 STATISTICS

**Files to Delete:** ~200+ files (client data, personal data)
**Files to Scrub:** ~45 files (hardcoded paths)
**Files to Update:** ~10 files (documentation)

**Estimated Time:** 3-4 hours

---

## 🚀 NEXT STEPS

### Immediate (Tonight/Tomorrow)
1. [ ] Delete all client data (HCSS, TGIF)
2. [ ] Delete personal user data
3. [ ] Create generic examples from client workflows
4. [ ] Update documentation

### Before Launch (This Week)
1. [ ] Scrub all hardcoded paths
2. [ ] Test fresh installation
3. [ ] Create ARCHITECTURE.md
4. [ ] Update README with public messaging

### Launch Week
1. [ ] Final security audit
2. [ ] Test in clean environment
3. [ ] Tag v1.0.0
4. [ ] Push to GitHub

---

## ⚠️ CRITICAL REMINDERS

1. **Never commit .env files** - Already in .gitignore ✅
2. **Client data is under NDA** - Must be completely removed
3. **Personal data is private** - Must be completely removed
4. **Test before launch** - Fresh install must work
5. **Examples must be generic** - No real client names

---

## 🔍 AUDIT COMMANDS

```bash
# Search for API keys
grep -r "sk-" --exclude-dir=node_modules --exclude-dir=.git .

# Search for email addresses
grep -r "@gmail.com" --exclude-dir=node_modules --exclude-dir=.git .

# Search for hardcoded paths
grep -r "/Users/justinharmon" --exclude-dir=node_modules --exclude-dir=.git .

# Search for client names
grep -r "HCSS\|TGIF" --exclude-dir=node_modules --exclude-dir=.git .
```

---

**Last Updated:** November 14, 2025 3:46am
**Next Review:** After client data deletion
