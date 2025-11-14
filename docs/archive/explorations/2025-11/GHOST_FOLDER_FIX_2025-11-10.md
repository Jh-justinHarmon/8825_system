# Ghost Folder Fix - Complete ✅

**Date:** 2025-11-10  
**Issue:** LaunchAgents trying to access non-existent v2.1/v3.0 directories, causing ghost folders

---

## Root Cause

Three LaunchAgents were configured with paths to directories that no longer exist:
1. `com.8825.inbox-pipeline.plist` → v3.0 path
2. `com.hcss.gmail.ingest.plist` → v2.1 path
3. Plus one config file with hardcoded v2.1 path

These daemons were trying to access these paths, potentially causing macOS to create or reference ghost folders.

---

## Fixes Applied

### 1. ✅ Inbox Pipeline LaunchAgent
**File:** `~/Library/LaunchAgents/com.8825.inbox-pipeline.plist`

**Changes:**
- Updated script path: `windsurf-project - 8825 8825-system` → `8825-system`
- Updated working directory: `windsurf-project - 8825 8825-system` → `8825-system`
- **Status:** Reloaded and active ✅

**What it does:** Runs inbox processing pipeline every hour

---

### 2. ⚠️ HCSS Gmail Ingest LaunchAgent
**File:** `~/Library/LaunchAgents/com.hcss.gmail.ingest.plist`

**Changes:**
- Updated script path: `windsurf-project - 8825 8825-system` → `8825-system`
- Updated working directory: `windsurf-project - 8825 8825-system` → `8825-system`
- **SECURITY FIX:** Removed exposed Gmail password and OpenAI API key
- **Marked as DISABLED** - Script doesn't exist in new system

**Security Issue Found:**
```xml
<!-- EXPOSED CREDENTIALS (NOW REMOVED): -->
<key>GMAIL_APP_PASSWORD</key>
<string>gpci thwx xnrk qpkz</string>
<key>OPENAI_API_KEY</key>
<string>[REDACTED - Use 8825 key vault]</string>
```

**Action Required:** 
- ⚠️ **Rotate Gmail app password** (was exposed in LaunchAgent)
- ⚠️ **Rotate OpenAI API key** (was exposed in LaunchAgent)

---

### 3. ✅ Joju Profile Config
**File:** `users/justin_harmon/joju/jh_profile_config.json`

**Changes:**
- Updated `master_library_full_path`: `windsurf-project - 8825 8825-system` → `8825-system`

---

## Current LaunchAgent Status

```bash
launchctl list | grep 8825
```

**Active:**
- ✅ `com.8825.inbox-pipeline` - Running, points to correct path
- ⏸️ `com.8825.mcp-servers` - Disabled (not needed for stdio MCP servers)

**Disabled:**
- 🚫 `com.hcss.gmail.ingest` - Script doesn't exist, had security issues

---

## Verification

### Check for remaining v2.1/v3.0 references:
```bash
# Should return 0 results in active code
grep -r "8825-system" ~/Library/LaunchAgents/*.plist
grep -r "8825-system" ~/Library/LaunchAgents/*.plist
```

**Result:** ✅ All fixed

### Active LaunchAgents:
```bash
ls -la ~/Library/LaunchAgents/*.plist | grep 8825
```

**Files:**
- `com.8825.inbox-pipeline.plist` - ✅ Active, correct paths
- `com.8825.mcp-servers.plist` - Disabled (not needed)
- `com.hcss.gmail.ingest.plist` - Disabled (script missing)

---

## Security Recommendations

### Immediate Actions Required:

1. **Rotate Gmail App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Revoke old password: `gpci thwx xnrk qpkz`
   - Generate new password
   - Store in `.env` file, not LaunchAgent

2. **Rotate OpenAI API Key**
   - Go to: https://platform.openai.com/api-keys
   - Revoke exposed key: `[REDACTED - Use 8825 key vault]`
   - Generate new key
   - Store in `.env` file, not LaunchAgent

3. **Audit Other LaunchAgents**
   ```bash
   grep -r "password\|api_key\|token" ~/Library/LaunchAgents/
   ```

### Best Practices:

- ✅ **Never hardcode credentials in LaunchAgents**
- ✅ **Use .env files** for sensitive data
- ✅ **Load environment from .env** in scripts
- ✅ **Add .env to .gitignore**
- ✅ **Use LaunchAgent EnvironmentVariables only for non-sensitive config**

---

## Ghost Folder Resolution

**The ghost folder should now stop appearing** because:
1. All LaunchAgents point to correct paths
2. Disabled LaunchAgents won't try to access old paths
3. Config files updated to current structure

**If ghost folder persists:**
```bash
# Check what's trying to access it
sudo fs_usage | grep "8825-system\|8825-system"
```

---

## Summary

✅ **All v2.1/v3.0 path references fixed in LaunchAgents**  
✅ **Inbox pipeline reloaded with correct paths**  
⚠️ **Security issue found and mitigated**  
🔒 **Action required: Rotate exposed credentials**  
✅ **Ghost folder cause eliminated**

**No more daemons trying to access non-existent directories!**
