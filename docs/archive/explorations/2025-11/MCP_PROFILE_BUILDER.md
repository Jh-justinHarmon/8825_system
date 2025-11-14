# MCP-Powered Joju Profile Builder

**Concept:** Use MCP servers to fetch external data and build complete Joju profiles  
**Inspired by:** Goose MCP Wikipedia example  
**Input:** Person name  
**Output:** Individual library + uploadable profile  

---

## Architecture

```
MCP Servers (Data Sources)
    ↓
Profile Builder Script
    ↓
Individual Library File
    ↓
Joju Upload Format
```

---

## MCP Servers Needed

### 1. LinkedIn MCP Server
**Purpose:** Fetch LinkedIn profile data

**Tools:**
- `fetch_linkedin_profile` - Get profile info
- `extract_experience` - Pull work history
- `extract_skills` - Get skills list
- `extract_education` - Get education

### 2. GitHub MCP Server
**Purpose:** Fetch GitHub activity

**Tools:**
- `fetch_github_profile` - Get user info
- `list_repositories` - Get repos
- `analyze_contributions` - Get activity
- `extract_projects` - Get project details

### 3. Web Scraper MCP Server
**Purpose:** Fetch portfolio/website data

**Tools:**
- `scrape_portfolio` - Get portfolio content
- `extract_projects` - Pull project descriptions
- `extract_testimonials` - Get recommendations

### 4. Resume Parser MCP Server
**Purpose:** Parse uploaded resumes

**Tools:**
- `parse_pdf_resume` - Extract from PDF
- `parse_docx_resume` - Extract from Word
- `extract_achievements` - Pull achievements

---

## Workflow

### Step 1: Initialize
```bash
# In Joju Mode
> Create sample profile for "John Doe"
```

**System actions:**
1. Create `john_doe_library.json` (empty)
2. Set target output: `john_doe_joju_profile.json`
3. Initialize extraction log

---

### Step 2: MCP Data Collection

**LinkedIn Extraction:**
```
Use linkedin_mcp.fetch_profile("John Doe")
Use linkedin_mcp.extract_experience("John Doe")
Use linkedin_mcp.extract_skills("John Doe")
```

**GitHub Extraction:**
```
Use github_mcp.fetch_profile("johndoe")
Use github_mcp.list_repositories("johndoe")
Use github_mcp.analyze_contributions("johndoe")
```

**Web Scraping:**
```
Use web_mcp.scrape_portfolio("https://johndoe.com")
Use web_mcp.extract_projects("https://johndoe.com")
```

**Resume Parsing (if provided):**
```
Use resume_mcp.parse_pdf("john_doe_resume.pdf")
Use resume_mcp.extract_achievements("john_doe_resume.pdf")
```

---

### Step 3: Build Individual Library

**Aggregate all extracted data:**

```json
{
  "person": "John Doe",
  "created": "2025-11-06",
  "sources": {
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe",
    "portfolio": "https://johndoe.com",
    "resume": "john_doe_resume.pdf"
  },
  "achievements": [
    {
      "id": "jd_001",
      "title": "Led team of 5 engineers",
      "source": "linkedin",
      "category": "leadership",
      "verified": true
    }
  ],
  "skills": [
    {
      "name": "Python",
      "level": "expert",
      "years": 8,
      "source": "github"
    }
  ],
  "projects": [
    {
      "name": "Project X",
      "description": "...",
      "technologies": ["Python", "React"],
      "source": "github"
    }
  ],
  "experience": [
    {
      "company": "Tech Corp",
      "role": "Senior Engineer",
      "duration": "2020-2023",
      "source": "linkedin"
    }
  ]
}
```

**Save to:** `/joju_sandbox/libraries/john_doe_library.json`

---

### Step 4: Deduplication

**Check for duplicates within the library:**
- Similar achievements
- Overlapping skills
- Duplicate projects

**Merge and consolidate:**
```json
{
  "achievement": "Led engineering team",
  "sources": ["linkedin", "resume"],
  "confidence": 0.95
}
```

---

### Step 5: Format for Joju Upload

**Transform to Joju format:**

```json
{
  "profile_id": "john_doe_001",
  "name": "John Doe",
  "headline": "Senior Software Engineer",
  "summary": "...",
  "achievements": [
    {
      "title": "Led team of 5 engineers",
      "impact": "Increased productivity by 40%",
      "skills_used": ["Leadership", "Python", "Agile"]
    }
  ],
  "skills": {
    "technical": ["Python", "React", "AWS"],
    "soft": ["Leadership", "Communication"]
  },
  "projects": [
    {
      "name": "Project X",
      "role": "Lead Developer",
      "technologies": ["Python", "React"],
      "outcomes": "..."
    }
  ],
  "experience_summary": {
    "total_years": 8,
    "industries": ["Tech", "Finance"],
    "roles": ["Engineer", "Lead", "Architect"]
  }
}
```

**Save to:** `/joju_sandbox/output/john_doe_joju_profile.json`

---

## Implementation Plan

### Phase 1: Build MCP Servers

**Create 4 MCP servers:**

1. **LinkedIn MCP** (`/joju_sandbox/mcp-servers/linkedin-bridge/`)
2. **GitHub MCP** (`/joju_sandbox/mcp-servers/github-bridge/`)
3. **Web Scraper MCP** (`/joju_sandbox/mcp-servers/web-scraper/`)
4. **Resume Parser MCP** (`/joju_sandbox/mcp-servers/resume-parser/`)

### Phase 2: Profile Builder Script

**Create:** `/joju_sandbox/profile_builder.py`

```python
#!/usr/bin/env python3
"""
Joju Profile Builder using MCP servers
"""

def build_profile(name, sources):
    """
    Build complete Joju profile using MCP data sources
    
    Args:
        name: Person's name
        sources: Dict of source URLs/files
    
    Returns:
        Individual library + Joju upload file
    """
    # 1. Initialize
    library = initialize_library(name)
    
    # 2. Fetch from MCP servers
    if 'linkedin' in sources:
        linkedin_data = fetch_linkedin(name)
        library.add(linkedin_data)
    
    if 'github' in sources:
        github_data = fetch_github(sources['github'])
        library.add(github_data)
    
    if 'portfolio' in sources:
        web_data = scrape_portfolio(sources['portfolio'])
        library.add(web_data)
    
    if 'resume' in sources:
        resume_data = parse_resume(sources['resume'])
        library.add(resume_data)
    
    # 3. Deduplicate
    library.deduplicate()
    
    # 4. Save library
    library.save(f'libraries/{name}_library.json')
    
    # 5. Format for Joju
    joju_profile = format_for_joju(library)
    joju_profile.save(f'output/{name}_joju_profile.json')
    
    return library, joju_profile
```

### Phase 3: Integration with Joju Mode

**Update Joju Mode protocol:**

```json
{
  "commands": {
    "create_sample_profile": {
      "command": "create sample profile for [name]",
      "description": "Build complete profile using MCP",
      "workflow": "MCP fetch → Build library → Format → Output",
      "requires_mcp": true
    }
  }
}
```

---

## Usage Example

### Command
```
create sample profile for "Sarah Chen"
```

### System Response
```
🎯 Building profile for Sarah Chen...

✅ Fetching LinkedIn data...
✅ Fetching GitHub data...
✅ Scraping portfolio...
✅ Parsing resume...

📊 Extracted:
   - 15 achievements
   - 25 skills
   - 8 projects
   - 3 work experiences

🔄 Deduplicating...
   - Merged 3 similar achievements
   - Consolidated 5 skill entries

💾 Saved:
   - /joju_sandbox/libraries/sarah_chen_library.json
   - /joju_sandbox/output/sarah_chen_joju_profile.json

✅ Profile complete!
```

---

## Benefits

### Automated Data Collection
- No manual copy/paste
- Pull from multiple sources
- Consistent format

### Individual Libraries
- Each person has own library
- Easy to update
- Portable

### Standardized Output
- Same format for all profiles
- Ready for Joju upload
- Quality controlled

### Scalable
- Build multiple profiles
- Batch processing
- Reusable pipeline

---

## Next Steps

1. **Build MCP servers** (LinkedIn, GitHub, Web, Resume)
2. **Create profile_builder.py** script
3. **Test with sample person**
4. **Integrate with Joju Mode**
5. **Document usage**

---

## MCP Server Priority

**Start with:**
1. ✅ GitHub MCP (easiest - public API)
2. ✅ Resume Parser MCP (local files)
3. ⚠️ Web Scraper MCP (medium complexity)
4. ⚠️ LinkedIn MCP (hardest - requires auth)

---

**Ready to build the first MCP server?** 🚀
