# Failure Mode: API Access Restrictions

**Severity:** HIGH  
**Frequency:** Common with team/business accounts  
**Impact:** Blocks implementation, requires pivot

---

## Description

Cloud service APIs (Dropbox, Google, etc.) fail due to access restrictions, particularly with team/business accounts.

---

## Common Causes

1. **Team account limitations** - Business accounts restrict API access
2. **Scope mismatches** - App has wrong permissions
3. **Migration issues** - Personal → Team migration breaks access
4. **Undocumented restrictions** - Team policies not in API docs

---

## Symptoms

- API returns "insufficient permissions" errors
- Token shows "scoped" when expecting "full" access
- Some folders/files invisible to API
- Works in personal account, fails in team account

---

## Prevention

### Before Choosing API:
1. ✅ Verify with actual account (not just docs)
2. ✅ Check if team/business account
3. ✅ Test API access in dev BEFORE building
4. ✅ Have fallback plan (local files, manual export)

### Detection:
```python
# Test API access early
try:
    api.test_access()
except InsufficientPermissionsError:
    # Pivot to local files or alternative
    pass
```

---

## Mitigation

### If API Fails:
1. **Check if data is synced locally** → Use local files
2. **Request admin approval** → Elevate permissions
3. **Use alternative API** → Different service
4. **Manual export** → CSV, user uploads files

---

## Real Example

**Dropbox Team Account (2024-11-09):**
- Tried Dropbox API for file scanning
- Team account blocked full access
- Pivoted to local filesystem
- Result: 2,740 files scanned successfully

**See:** [Dropbox API Failure Lesson](../lessons/2024-11-09_dropbox_api_failure.md)

---

## Related Patterns

- [Local-First When API Fails](../patterns/local_first_when_api_fails.md)
