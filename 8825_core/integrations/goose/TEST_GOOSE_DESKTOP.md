# Test Goose Desktop with HCSS Tools

**Purpose:** Verify Desktop app can access MCP bridge and HCSS tools  
**Date:** 2025-11-06

---

## Quick Test Commands

Copy and paste these into Goose Desktop:

### 1. Check HCSS Status
```
Use check_status to see the HCSS system status
```

**Expected:** Shows scheduler status, file counts, last processing time

---

### 2. List Recent Files
```
Use list_recent_files to show me the latest processed files
```

**Expected:** Lists recent JSON files from raw/ directory

---

### 3. Get Routing Statistics
```
Use get_routing_stats to see project distribution
```

**Expected:** Shows breakdown by TGIF, RAL, LHL, 76

---

### 4. Read Corrections Log
```
Use read_corrections_log with lines=20 to show recent corrections
```

**Expected:** Shows last 20 correction entries

---

### 5. Analyze the System
```
Use check_status and get_routing_stats, then analyze the HCSS system health and suggest any improvements
```

**Expected:** Goose uses both tools and provides analysis

---

## If Tools Work ✅

You should see:
- Tool execution messages
- Results from HCSS scripts
- Data from your actual files

This confirms:
- ✅ MCP bridge is connected
- ✅ Desktop can access HCSS tools
- ✅ Integration is working

---

## If Tools Don't Work ❌

### Check MCP Server in Settings

1. Click Settings (gear icon)
2. Go to "MCP Servers"
3. Verify `hcss-bridge` is listed
4. Check the path is correct
5. Try restarting Goose app

### Verify Config File

```bash
cat ~/.config/goose/config.json
```

Should show hcss-bridge configuration.

---

## Next Steps After Testing

### Try More Complex Queries

```
Analyze the routing accuracy by using get_routing_stats and list_recent_files, then tell me if any projects seem under-represented
```

```
Use read_corrections_log with lines=100 and identify the top 5 most common corrections
```

```
Use check_status and ingest_gmail, then summarize what happened
```

### Ask About the Codebase

```
Explain how the HCSS routing algorithm works
```

```
What are the main components of the Gmail extractor?
```

```
Suggest improvements to the correction rules system
```

---

## Success Criteria

✅ Tools execute without errors  
✅ Real data is returned  
✅ Goose can analyze the results  
✅ You can ask follow-up questions  

**If all working → Integration complete!** 🎉
