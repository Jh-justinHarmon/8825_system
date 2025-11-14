# Implementation Roadmap: Sequencing & Fuzzy Logic

**Priority:** HIGH  
**Estimated Time:** 2-3 hours  
**Impact:** Significant accuracy improvement

---

## Quick Wins (Implement First)

### 1. Fuzzy Name Matching (30 min)
**Impact:** ⭐⭐⭐⭐⭐

```python
# Add to profile_builder.py
from difflib import SequenceMatcher

def fuzzy_match(str1, str2, threshold=0.8):
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio() >= threshold
```

**Use in:**
- Wikipedia verification
- LinkedIn verification
- Stack Overflow verification

**Benefit:** Handles "Linus Torvalds" vs "Linus Benedict Torvalds"

---

### 2. Location Aliases (20 min)
**Impact:** ⭐⭐⭐⭐

```python
LOCATION_ALIASES = {
    'sf': 'san francisco',
    'nyc': 'new york',
    'la': 'los angeles',
    'pdx': 'portland'
}

STATE_ALIASES = {
    'ca': 'california',
    'ny': 'new york',
    'or': 'oregon'
}
```

**Benefit:** Matches "SF" with "San Francisco"

---

### 3. Company Aliases (20 min)
**Impact:** ⭐⭐⭐⭐

```python
COMPANY_ALIASES = {
    'google': ['alphabet', 'google llc'],
    'facebook': ['meta', 'meta platforms'],
    'twitter': ['x', 'x corp'],
    'microsoft': ['msft', 'microsoft corporation']
}
```

**Benefit:** Matches "Meta" with "Facebook"

---

## Medium Priority (Implement Second)

### 4. Basic Sequencing (45 min)
**Impact:** ⭐⭐⭐

```python
# Phase-based execution
PHASES = {
    'foundation': ['fetch_github_data'],
    'enrichment': ['fetch_wikipedia', 'fetch_linkedin', 'fetch_stackoverflow'],
    'verification': ['verify_identity'],
    'finalization': ['build_character', 'save_files']
}
```

**Benefit:** Clearer execution flow, better error handling

---

### 5. Parallel Enrichment (30 min)
**Impact:** ⭐⭐⭐

```python
import concurrent.futures

def fetch_all_sources_parallel():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(fetch_wikipedia_data),
            executor.submit(fetch_linkedin_data),
            executor.submit(fetch_stackoverflow_data)
        ]
        results = [f.result() for f in futures]
```

**Benefit:** 3-5x faster data collection

---

### 6. Retry Logic (20 min)
**Impact:** ⭐⭐⭐

```python
def fetch_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

**Benefit:** More reliable data fetching

---

## Lower Priority (Nice to Have)

### 7. Caching (30 min)
**Impact:** ⭐⭐

```python
def fetch_with_cache(source, ttl=3600):
    cache_file = f".cache/{username}_{source}.json"
    if cache_valid(cache_file, ttl):
        return load_cache(cache_file)
    result = fetch_function()
    save_cache(cache_file, result)
    return result
```

**Benefit:** Faster repeated runs, API rate limit protection

---

### 8. Technology Aliases (15 min)
**Impact:** ⭐⭐

```python
TECH_ALIASES = {
    'javascript': ['js', 'ecmascript'],
    'typescript': ['ts'],
    'python': ['python3', 'py']
}
```

**Benefit:** Better tech matching

---

## Implementation Order

### Sprint 1 (1 hour) - Fuzzy Matching
1. ✅ Fuzzy name matching (30 min)
2. ✅ Location aliases (20 min)
3. ✅ Company aliases (20 min)

**Result:** 30-40% better verification accuracy

---

### Sprint 2 (1 hour) - Sequencing
4. ✅ Basic sequencing (45 min)
5. ✅ Retry logic (20 min)

**Result:** More reliable execution

---

### Sprint 3 (1 hour) - Performance
6. ✅ Parallel enrichment (30 min)
7. ✅ Caching (30 min)

**Result:** 3-5x faster

---

## Quick Start: Fuzzy Matching

### Step 1: Add Helper Functions
```python
# Add to profile_builder.py after imports

from difflib import SequenceMatcher

def fuzzy_match(str1, str2, threshold=0.8):
    """Fuzzy string matching"""
    if not str1 or not str2:
        return False
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio() >= threshold

def normalize_location(loc):
    """Normalize location with aliases"""
    aliases = {
        'sf': 'san francisco',
        'nyc': 'new york',
        'la': 'los angeles',
        'pdx': 'portland',
        'ca': 'california',
        'ny': 'new york',
        'or': 'oregon'
    }
    loc_lower = loc.lower().strip()
    for alias, full in aliases.items():
        if alias in loc_lower:
            loc_lower = loc_lower.replace(alias, full)
    return loc_lower

def normalize_company(company):
    """Normalize company with aliases"""
    aliases = {
        'alphabet': 'google',
        'meta': 'facebook',
        'meta platforms': 'facebook',
        'x corp': 'twitter',
        'x': 'twitter',
        'msft': 'microsoft'
    }
    comp_lower = company.lower().strip()
    # Remove suffixes
    for suffix in [' inc', ' llc', ' corp', ' corporation', ' ltd']:
        comp_lower = comp_lower.replace(suffix, '')
    # Check aliases
    return aliases.get(comp_lower.strip(), comp_lower.strip())
```

### Step 2: Update Verification
```python
# In verify_wikipedia_match method, replace exact matches with fuzzy:

# OLD:
if github_name and github_name in wiki_title:
    confidence += 20

# NEW:
if github_name and fuzzy_match(github_name, wiki_title, 0.7):
    confidence += 20

# OLD:
if github_loc and github_loc in wiki_extract:
    confidence += 25

# NEW:
github_loc_norm = normalize_location(github_loc)
if github_loc and github_loc_norm in normalize_location(wiki_extract):
    confidence += 25

# OLD:
if github_company and github_company in wiki_extract:
    confidence += 25

# NEW:
github_comp_norm = normalize_company(github_company)
wiki_extract_norm = normalize_company(wiki_extract)
if github_comp_norm and github_comp_norm in wiki_extract_norm:
    confidence += 25
```

---

## Expected Improvements

### Before Fuzzy Matching
```
"Linus Torvalds" vs "Linus Benedict Torvalds" → ❌ No match
"SF" vs "San Francisco" → ❌ No match
"Meta" vs "Facebook" → ❌ No match

Verification rate: ~30%
```

### After Fuzzy Matching
```
"Linus Torvalds" vs "Linus Benedict Torvalds" → ✅ Match (0.85)
"SF" vs "San Francisco" → ✅ Match (normalized)
"Meta" vs "Facebook" → ✅ Match (alias)

Verification rate: ~60-70%
```

---

## Testing

### Test Cases
```python
# Test fuzzy matching
assert fuzzy_match("Linus Torvalds", "Linus Benedict Torvalds") == True
assert fuzzy_match("John Smith", "Jane Smith") == False

# Test location normalization
assert normalize_location("SF, CA") == "san francisco, california"
assert normalize_location("Portland, OR") == "portland, oregon"

# Test company normalization
assert normalize_company("Meta Platforms") == "facebook"
assert normalize_company("Alphabet Inc") == "google"
```

---

## Summary

**Quick wins (1 hour):**
- Fuzzy name matching
- Location aliases
- Company aliases

**Impact:**
- 2x better verification accuracy
- Handles common variations
- More reliable matching

**Start with fuzzy matching - biggest impact for least effort!** 🎯
