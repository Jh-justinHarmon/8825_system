# Dropbox API Failure → Local Filesystem Pivot

**Date:** 2024-11-09  
**Project:** Joju Contributions Pipeline  
**Type:** Adaptation (Success)  
**Tags:** dropbox, api_restrictions, local_files, team_accounts, pivot

---

## Context

Building Joju contributions miner to scan Dropbox for design files (.ai, .psd, .indd, etc.). Initial plan was to use Dropbox API for cloud-based scanning.

**Initial Approach:**
- Create Dropbox app
- Use REST API to scan folders
- Extract file metadata remotely

---

## What Happened

### Attempt 1: Dropbox API with Scoped Access
- Created app with "App Folder" scope
- Generated access token
- API calls worked, but only accessed dedicated app folder
- User's actual files not visible

### Attempt 2: Full Dropbox Access
- Tried to upgrade to "Full Dropbox" access
- Updated permissions in app console
- Regenerated token
- **Still showed as "scoped" access**

### Discovery:
- Account was originally personal, now under team account
- Team account restrictions prevent full Dropbox API access
- Dropbox API documentation doesn't clearly explain team account limitations

### Pivot Decision:
**Abandoned API approach, switched to local filesystem scanning**

---

## Outcome

✅ **Success - Better than original plan:**

**Implementation:**
- Scan `/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/` (local sync folder)
- Hash files for deduplication
- Parse XMP metadata for attribution
- Generate mining report

**Results:**
- Scanned 2,740 design files successfully
- Extracted creator attribution from XMP
- No API rate limits
- No permission issues
- Faster than API calls would have been

---

## Why It Worked

### Root Causes of API Failure:
1. **Team account restrictions** - Dropbox limits API access for business accounts
2. **Poor documentation** - Team account limitations not prominent in docs
3. **Complex permission model** - App folder vs full access vs team permissions

### Why Local Approach Succeeded:
1. **Direct filesystem access** - No API permissions needed
2. **Dropbox already synced locally** - Files available on disk
3. **Faster** - No network latency
4. **No rate limits** - Can scan as fast as disk allows
5. **More metadata** - XMP accessible via ExifTool

---

## Lessons Learned

### 1. **Check API Access Early**
- Don't assume API will work
- Verify permissions BEFORE building
- Test with actual account (not just docs)
- Team/business accounts often have different rules

### 2. **Local-First Can Be Better Than Cloud APIs**
- If data is already synced locally (Dropbox, Google Drive), use filesystem
- Avoids rate limits, auth issues, network latency
- More metadata often available locally (XMP, extended attributes)

### 3. **Team Accounts Complicate Everything**
- Personal → Team migration breaks things
- Always check: "Is this a team account?"
- Document team account limitations in brainstorms

### 4. **Pivot Fast**
- Spent ~2 hours on API troubleshooting
- Pivoted to local files in 30 minutes
- Got working proof-of-concept same day
- **Don't get stuck on original plan**

### 5. **XMP Parsing Is Powerful**
- ExifTool extracts rich metadata from .ai, .psd files
- Creator names, edit history, tool versions
- Better attribution than API file metadata

---

## Reusable Pattern?

- [x] **YES** - Created pattern: [Local-First When API Fails](../patterns/local_first_when_api_fails.md)

---

## Prevention/Application

### Before Choosing API Approach:
1. **Check if data is locally synced**
   - Dropbox → Use local folder
   - Google Drive → Use File Stream mount
   - OneDrive → Use local sync
2. **Verify API access with actual account**
   - Test before committing to implementation
   - Check team account restrictions
3. **Compare local vs API benefits**
   - Speed: Local usually faster
   - Rate limits: Local has none
   - Metadata: Local often richer
4. **Have fallback plan**
   - Design for both API and local access
   - Make data source swappable

### Decision Framework:
```
Is data synced locally?
├─ YES: Use local filesystem (unless cloud-specific features needed)
├─ NO: Use API
└─ PARTIAL: Hybrid approach
```

---

## Related

**Code:**
- [local_miner.py](../../integrations/dropbox/local_miner.py) - Working implementation
- [dropbox_miner.py](../../integrations/dropbox/dropbox_miner.py) - Deprecated API version

**Documentation:**
- [Joju Contributions Pipeline Brainstorm](../../explorations/features/joju_contributions_pipeline_brainstorm.md)
- [Dropbox Miner README](../../integrations/dropbox/README.md)

**Patterns:**
- [Local-First When API Fails](../patterns/local_first_when_api_fails.md)

**Similar Lessons:**
- TBD: Google Drive local access (when we build it)
- TBD: GitHub API vs git local (comparison)

---

## Metrics

- **Time to pivot:** 30 minutes (after 2 hours of API troubleshooting)
- **Files scanned:** 2,740
- **Performance:** ~50 files/second (local) vs ~5 files/second (API estimate)
- **Success rate:** 100% (vs uncertain with API permissions)

---

## Update Log

- 2024-11-09: Initial documentation
- [Future]: Add comparison when building other cloud integrations
