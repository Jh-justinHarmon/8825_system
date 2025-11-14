# Enhanced Logic: Sequencing & Fuzzy Matching

**Status:** Design Document  
**Priority:** HIGH  
**Date:** 2025-11-06

---

## 1. Sequencing Logic

### Current Issue
Operations run in fixed order without dependency awareness

### Proposed Solution
Smart sequencing based on dependencies and data availability

---

## Sequencing Architecture

### Phase-Based Execution

```python
class SequencedProfileBuilder:
    def __init__(self, username, mode='create'):
        self.phases = {
            'foundation': [],    # Must run first
            'enrichment': [],    # Depends on foundation
            'verification': [],  # Depends on enrichment
            'finalization': []   # Depends on verification
        }
        self.dependencies = {}
        self.execution_order = []
    
    def register_task(self, task_name, phase, depends_on=None):
        """Register task with dependencies"""
        self.phases[phase].append(task_name)
        if depends_on:
            self.dependencies[task_name] = depends_on
    
    def calculate_execution_order(self):
        """Calculate optimal execution order"""
        # Topological sort based on dependencies
        pass
    
    def execute_sequenced(self):
        """Execute tasks in optimal order"""
        for phase in ['foundation', 'enrichment', 'verification', 'finalization']:
            self.execute_phase(phase)
```

---

## Execution Phases

### Phase 1: Foundation (Required)
**Must complete before anything else**

```python
foundation_tasks = [
    'fetch_github_data',      # Primary data source
    'load_existing_library'   # If UPDATE mode
]

# Dependencies: None
# Failure: Fatal - cannot continue
```

### Phase 2: Enrichment (Parallel)
**Can run in parallel, independent of each other**

```python
enrichment_tasks = [
    'fetch_wikipedia_data',
    'fetch_linkedin_data',
    'fetch_stackoverflow_data',
    'fetch_wayback_data',
    'search_awards',
    'search_conference_talks',
    'search_publications'
]

# Dependencies: GitHub data (for name lookup)
# Failure: Non-fatal - continue with available data
# Optimization: Run in parallel threads
```

### Phase 3: Verification (Sequential)
**Must run after enrichment**

```python
verification_tasks = [
    'verify_identity',           # Cross-check all sources
    'calculate_confidence',      # Score each source
    'generate_warnings'          # Flag issues
]

# Dependencies: All enrichment data
# Failure: Non-fatal - mark as unverified
```

### Phase 4: Finalization (Sequential)
**Must run after verification**

```python
finalization_tasks = [
    'build_character',           # Depends on verified data
    'build_profile',             # Depends on character
    'format_for_joju',           # Depends on profile
    'calculate_completeness',    # Depends on all data
    'save_files'                 # Final step
]

# Dependencies: Verification complete
# Failure: Fatal - cannot produce output
```

---

## Dependency Graph

```
GitHub Data (Foundation)
    ├─→ Wikipedia Search (needs name)
    ├─→ LinkedIn Search (needs name)
    ├─→ Stack Overflow Search (needs name)
    ├─→ Wayback Search (needs website)
    └─→ Awards Search (needs repos)

All Enrichment Data
    └─→ Identity Verification
        └─→ Character Building
            └─→ Profile Building
                └─→ Joju Formatting
                    └─→ Save Files
```

---

## Smart Sequencing Features

### 1. Conditional Execution
```python
def should_run_task(task_name):
    """Determine if task should run"""
    
    # Skip if data already exists (UPDATE mode)
    if mode == 'update' and has_existing_data(task_name):
        if not should_refresh(task_name):
            return False
    
    # Skip if dependencies failed
    if dependencies_failed(task_name):
        return False
    
    # Skip if not applicable
    if not is_applicable(task_name):
        return False
    
    return True
```

### 2. Parallel Execution
```python
def execute_enrichment_parallel():
    """Run enrichment tasks in parallel"""
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_wikipedia_data): 'wikipedia',
            executor.submit(fetch_linkedin_data): 'linkedin',
            executor.submit(fetch_stackoverflow_data): 'stackoverflow',
            executor.submit(fetch_wayback_data): 'wayback',
            executor.submit(search_awards): 'awards'
        }
        
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                print(f"✅ {source} completed")
            except Exception as e:
                print(f"⚠️  {source} failed: {e}")
```

### 3. Retry Logic
```python
def execute_with_retry(task, max_retries=3):
    """Execute task with retry logic"""
    for attempt in range(max_retries):
        try:
            return task()
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️  Retry {attempt + 1}/{max_retries} in {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"❌ Failed after {max_retries} attempts")
                raise
```

### 4. Caching
```python
def fetch_with_cache(source_name, fetch_function):
    """Cache results to avoid redundant API calls"""
    cache_file = f".cache/{username}_{source_name}.json"
    cache_ttl = 3600  # 1 hour
    
    if cache_exists(cache_file) and not cache_expired(cache_file, cache_ttl):
        print(f"📦 Using cached {source_name} data")
        return load_cache(cache_file)
    
    result = fetch_function()
    save_cache(cache_file, result)
    return result
```

---

## 2. Fuzzy Matching Logic

### Current Issue
Exact string matching fails on variations

### Proposed Solution
Fuzzy matching with similarity scoring

---

## Fuzzy Matching Implementation

### Name Matching
```python
from difflib import SequenceMatcher

def fuzzy_name_match(name1, name2, threshold=0.8):
    """
    Match names with variations
    
    Examples:
    - "Linus Torvalds" vs "Linus Benedict Torvalds" → 0.85
    - "Mike Johnson" vs "Michael Johnson" → 0.92
    - "John Smith" vs "Jane Smith" → 0.73
    """
    # Normalize
    n1 = name1.lower().strip()
    n2 = name2.lower().strip()
    
    # Calculate similarity
    similarity = SequenceMatcher(None, n1, n2).ratio()
    
    return similarity >= threshold

# Enhanced matching
def smart_name_match(name1, name2):
    """Smart name matching with multiple strategies"""
    
    # Strategy 1: Exact match
    if name1.lower() == name2.lower():
        return 1.0
    
    # Strategy 2: Fuzzy match
    fuzzy_score = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
    
    # Strategy 3: Token match (handles middle names)
    tokens1 = set(name1.lower().split())
    tokens2 = set(name2.lower().split())
    token_overlap = len(tokens1 & tokens2) / max(len(tokens1), len(tokens2))
    
    # Strategy 4: Initials match
    initials1 = ''.join([word[0] for word in name1.split()])
    initials2 = ''.join([word[0] for word in name2.split()])
    initials_match = 1.0 if initials1 == initials2 else 0.0
    
    # Weighted combination
    score = (fuzzy_score * 0.4 + token_overlap * 0.4 + initials_match * 0.2)
    
    return score
```

### Location Matching
```python
def fuzzy_location_match(loc1, loc2, threshold=0.7):
    """
    Match locations with variations
    
    Examples:
    - "San Francisco" vs "SF" → 0.9
    - "Portland, OR" vs "Portland, Oregon" → 0.95
    - "New York" vs "NYC" → 0.9
    """
    # Normalization rules
    location_aliases = {
        'sf': 'san francisco',
        'nyc': 'new york',
        'la': 'los angeles',
        'pdx': 'portland',
        'sea': 'seattle'
    }
    
    state_aliases = {
        'ca': 'california',
        'ny': 'new york',
        'or': 'oregon',
        'wa': 'washington'
    }
    
    # Normalize
    l1 = normalize_location(loc1, location_aliases, state_aliases)
    l2 = normalize_location(loc2, location_aliases, state_aliases)
    
    # Check if one is substring of other
    if l1 in l2 or l2 in l1:
        return 1.0
    
    # Fuzzy match
    similarity = SequenceMatcher(None, l1, l2).ratio()
    
    return similarity >= threshold
```

### Company Matching
```python
def fuzzy_company_match(company1, company2, threshold=0.8):
    """
    Match companies with variations
    
    Examples:
    - "Google" vs "Google LLC" → 0.95
    - "Microsoft" vs "Microsoft Corporation" → 0.9
    - "Meta" vs "Facebook" → 0.7 (known alias)
    """
    # Known company aliases
    company_aliases = {
        'google': ['alphabet', 'google llc', 'google inc'],
        'facebook': ['meta', 'meta platforms', 'facebook inc'],
        'twitter': ['x', 'x corp'],
        'microsoft': ['msft', 'microsoft corporation'],
        'amazon': ['amzn', 'amazon.com']
    }
    
    # Normalize
    c1 = normalize_company(company1)
    c2 = normalize_company(company2)
    
    # Check aliases
    if are_aliases(c1, c2, company_aliases):
        return 1.0
    
    # Remove common suffixes
    c1 = remove_suffixes(c1, ['inc', 'llc', 'corp', 'corporation', 'ltd'])
    c2 = remove_suffixes(c2, ['inc', 'llc', 'corp', 'corporation', 'ltd'])
    
    # Fuzzy match
    similarity = SequenceMatcher(None, c1, c2).ratio()
    
    return similarity >= threshold
```

### Technology Matching
```python
def fuzzy_tech_match(tech1, tech2):
    """
    Match technologies with variations
    
    Examples:
    - "JavaScript" vs "JS" → 0.95
    - "Python" vs "Python3" → 0.9
    - "React" vs "ReactJS" → 0.95
    """
    tech_aliases = {
        'javascript': ['js', 'ecmascript', 'es6'],
        'typescript': ['ts'],
        'python': ['python2', 'python3', 'py'],
        'c++': ['cpp', 'cplusplus'],
        'c#': ['csharp'],
        'react': ['reactjs', 'react.js'],
        'vue': ['vuejs', 'vue.js']
    }
    
    t1 = tech1.lower().strip()
    t2 = tech2.lower().strip()
    
    # Check aliases
    if are_aliases(t1, t2, tech_aliases):
        return 1.0
    
    # Fuzzy match
    return SequenceMatcher(None, t1, t2).ratio()
```

---

## Enhanced Verification with Fuzzy Logic

### Updated Wikipedia Verification
```python
def verify_wikipedia_match_fuzzy(self, github_data, wiki_data):
    """Verify with fuzzy matching"""
    confidence = 0
    
    # Check 1: Fuzzy name match (25 points)
    github_name = github_data.get('name', '')
    wiki_title = wiki_data.get('title', '')
    
    name_similarity = smart_name_match(github_name, wiki_title)
    confidence += int(name_similarity * 25)
    
    # Check 2: Fuzzy location match (25 points)
    github_loc = github_data.get('location', '')
    wiki_text = wiki_data.get('extract', '')
    
    if github_loc:
        # Extract locations from wiki text
        wiki_locations = extract_locations(wiki_text)
        best_match = max([fuzzy_location_match(github_loc, loc) 
                         for loc in wiki_locations], default=0)
        confidence += int(best_match * 25)
    
    # Check 3: Fuzzy company match (25 points)
    github_company = github_data.get('company', '')
    if github_company:
        wiki_companies = extract_companies(wiki_text)
        best_match = max([fuzzy_company_match(github_company, comp) 
                         for comp in wiki_companies], default=0)
        confidence += int(best_match * 25)
    
    # Check 4: Fuzzy tech match (25 points)
    github_langs = self.library['data'].get('languages', {}).keys()
    tech_matches = []
    for lang in github_langs:
        if any(fuzzy_tech_match(lang, word) > 0.8 
               for word in wiki_text.lower().split()):
            tech_matches.append(lang)
    
    if tech_matches:
        confidence += min(25, len(tech_matches) * 8)
    
    return min(confidence, 100)
```

---

## Benefits

### Sequencing Logic
✅ Optimal execution order  
✅ Parallel processing where possible  
✅ Dependency management  
✅ Retry logic for failures  
✅ Caching for performance  

### Fuzzy Matching
✅ Handles name variations  
✅ Matches location aliases  
✅ Recognizes company aliases  
✅ Technology synonyms  
✅ Higher match rates  
✅ More accurate verification  

---

## Implementation Priority

### Phase 1 (High Priority)
1. ✅ Fuzzy name matching
2. ✅ Fuzzy location matching
3. ✅ Fuzzy company matching
4. ✅ Basic sequencing

### Phase 2 (Medium Priority)
5. Parallel execution
6. Retry logic
7. Caching
8. Fuzzy tech matching

### Phase 3 (Nice to Have)
9. Advanced dependency graph
10. Dynamic task scheduling
11. Performance optimization
12. Machine learning for matching

---

## Summary

**Enhanced logic provides:**
- Smart execution order
- Parallel processing
- Fuzzy matching for variations
- Better verification accuracy
- Improved performance

**Next step: Implement fuzzy matching first, then sequencing!** 🎯
