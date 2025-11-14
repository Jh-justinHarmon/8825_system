# Data Ingestion Options for Joju

**Date:** 2025-11-06  
**Purpose:** Evaluate all available data import/ingestion methods

---

## Available Options

### 1. **MCP Server (Dormant but Ready)** ⭐⭐⭐⭐⭐

**Location:** `/goose_sandbox/mcp-servers/hcss-bridge/`

**What It Is:**
- Model Context Protocol server
- Exposes tools to AI agents (Goose, Claude, etc.)
- Already built and tested for HCSS

**Current Tools (HCSS-focused):**
1. `ingest_gmail` - Gmail ingestion
2. `check_status` - System status
3. `list_recent_files` - File listing
4. `read_corrections_log` - Corrections tracking
5. `get_routing_stats` - Routing statistics

**Status:** ✅ Infrastructure intact, not actively configured

**For Joju, Could Add:**
- `ingest_resume` - PDF/DOCX resume parsing
- `ingest_linkedin` - LinkedIn profile import
- `ingest_github` - GitHub profile import
- `ingest_readcv` - ReadCV JSON import
- `ingest_csv` - CSV bulk import
- `merge_profiles` - Combine multiple sources

**Pros:**
- ✅ Already built and tested
- ✅ Works with multiple AI tools (Goose, Claude Desktop, Cline)
- ✅ Standardized protocol
- ✅ Easy to extend with new tools
- ✅ Can be used from any MCP-compatible client

**Cons:**
- ⚠️ Requires Node.js
- ⚠️ Needs configuration in client app
- ⚠️ Currently dormant (not active)

**Value for Joju:** ⭐⭐⭐⭐⭐ (Best for AI-driven workflows)

---

### 2. **Profile Builder (Active)** ⭐⭐⭐⭐

**Location:** `/joju_sandbox/profile_builder.py`

**What It Does:**
- Fetches from 8 online sources
- GitHub, Wikipedia, LinkedIn, Stack Overflow, etc.
- Generates Joju-ready JSON

**Modes:**
- CREATE - New profile from scratch
- UPDATE - Add to existing (preserves data)

**Pros:**
- ✅ Already working
- ✅ Multi-source aggregation
- ✅ Evidence-based skills
- ✅ Identity verification
- ✅ Additive UPDATE mode

**Cons:**
- ⚠️ Requires GitHub as foundation
- ⚠️ Limited for non-developers
- ⚠️ LinkedIn blocked by anti-scraping

**Value for Joju:** ⭐⭐⭐⭐ (Great for developers)

---

### 3. **Gmail Extractor (HCSS)** ⭐⭐⭐⭐

**Location:** `/hcss_sandbox/8825_gmail_extractor.py`

**What It Does:**
- Extracts emails from Gmail
- Processes Otter.ai transcripts
- Routes content to projects

**For Joju, Could Adapt:**
- Extract resume attachments from email
- Process LinkedIn messages
- Import recommendations/testimonials
- Track job applications

**Pros:**
- ✅ Already working for HCSS
- ✅ Gmail API integration
- ✅ Attachment handling
- ✅ Automated processing

**Cons:**
- ⚠️ HCSS-specific currently
- ⚠️ Needs adaptation for Joju
- ⚠️ Requires Gmail API setup

**Value for Joju:** ⭐⭐⭐ (If adapted)

---

### 4. **Manual JSON Import** ⭐⭐⭐⭐⭐

**Current Examples:**
- `/references/MG-readCV_format.json` (Matthew Galley)
- `/references/justin-harmon-cv_joju-export.json`
- `/references/joju-template_download-homepage.json`

**What It Does:**
- Direct JSON file import
- ReadCV exports
- Joju exports
- Custom JSON formats

**Pros:**
- ✅ Works now
- ✅ No parsing needed
- ✅ High quality data
- ✅ User has full control

**Cons:**
- ⚠️ Manual export required
- ⚠️ Not automated
- ⚠️ Limited to JSON sources

**Value for Joju:** ⭐⭐⭐⭐⭐ (Easiest, highest quality)

---

### 5. **File Upload (Need to Build)** ⭐⭐⭐⭐⭐

**Formats to Support:**
- PDF resumes
- DOCX resumes
- CSV work history
- Excel project lists
- Markdown portfolios

**Would Need:**
- PDF parser (PyPDF2, pdfplumber)
- DOCX parser (python-docx)
- CSV parser (pandas)
- Resume structure detection
- Data extraction logic

**Pros:**
- ✅ Most common format (PDF/DOCX)
- ✅ One-time import
- ✅ Complete data
- ✅ User-friendly

**Cons:**
- ❌ Not built yet
- ⚠️ Parsing complexity
- ⚠️ Format variations
- ⚠️ Quality depends on resume structure

**Value for Joju:** ⭐⭐⭐⭐⭐ (Highest priority to build)

---

### 6. **API Integrations (Need Keys)** ⭐⭐⭐⭐⭐

**Available APIs:**
- LinkedIn API (requires approval)
- Dribbble API (requires token)
- Behance API (requires key)
- GitHub API (working ✅)
- Stack Overflow API (working ✅)

**Pros:**
- ✅ Official, reliable data
- ✅ Complete information
- ✅ Real-time updates
- ✅ Structured format

**Cons:**
- ⚠️ Requires API keys/approval
- ⚠️ Rate limits
- ⚠️ Some require payment
- ⚠️ Setup complexity

**Value for Joju:** ⭐⭐⭐⭐⭐ (Best quality, needs setup)

---

### 7. **Web Scraping (Limited)** ⭐⭐⭐

**Current:**
- `/joju_sandbox/scrape_designer_profiles.py`
- Basic Dribbble scraping
- LinkedIn blocked

**Pros:**
- ✅ No API keys needed
- ✅ Can get public data
- ✅ Quick to implement

**Cons:**
- ⚠️ Anti-scraping protection
- ⚠️ Limited data extraction
- ⚠️ Fragile (breaks when sites change)
- ⚠️ Legal/ethical concerns

**Value for Joju:** ⭐⭐⭐ (Backup option only)

---

## Comparison Matrix

| Method | Ease of Use | Data Quality | Automation | Coverage | Priority |
|--------|-------------|--------------|------------|----------|----------|
| **MCP Server** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 High |
| **Profile Builder** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Done |
| **Gmail Extractor** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 🟡 Medium |
| **JSON Import** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ✅ Done |
| **File Upload** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 High |
| **API Integration** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 High |
| **Web Scraping** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 🟢 Low |

---

## Recommended Implementation Order

### Phase 1: Quick Wins (Now)
1. ✅ **JSON Import** - Already works
2. ✅ **Profile Builder** - Already works
3. ✅ **Manual Entry** - Always available

### Phase 2: High Impact (Next)
4. 🔴 **Resume Parser** (PDF/DOCX)
   - Most requested feature
   - Highest user value
   - Standard format

5. 🔴 **MCP Server for Joju**
   - Extend existing HCSS bridge
   - Add Joju-specific tools
   - Enable AI-driven workflows

6. 🔴 **LinkedIn API**
   - Apply for access
   - Most comprehensive professional data
   - Industry standard

### Phase 3: Enhanced Coverage (Later)
7. 🟡 **CSV/Excel Import**
   - Bulk data entry
   - Easy for users
   - Flexible format

8. 🟡 **Designer APIs** (Dribbble, Behance, Figma)
   - Portfolio metrics
   - Community presence
   - Design-specific data

9. 🟡 **Gmail Adaptation**
   - Resume attachments
   - Recommendations
   - Application tracking

---

## MCP Server: The Game Changer

### Why MCP is Powerful for Joju

**Current State:**
- Built for HCSS
- 5 tools implemented
- Works with Goose, Claude, etc.
- Dormant but ready

**For Joju, Add These Tools:**

```javascript
{
  name: 'ingest_resume',
  description: 'Parse PDF/DOCX resume and add to Joju library',
  inputSchema: {
    type: 'object',
    properties: {
      file_path: { type: 'string' },
      username: { type: 'string' }
    }
  }
}

{
  name: 'ingest_github',
  description: 'Fetch GitHub profile and add to Joju library',
  inputSchema: {
    type: 'object',
    properties: {
      github_username: { type: 'string' }
    }
  }
}

{
  name: 'ingest_linkedin',
  description: 'Import LinkedIn profile data',
  inputSchema: {
    type: 'object',
    properties: {
      linkedin_url: { type: 'string' }
    }
  }
}

{
  name: 'merge_profiles',
  description: 'Merge multiple data sources into single profile',
  inputSchema: {
    type: 'object',
    properties: {
      username: { type: 'string' },
      sources: { type: 'array' }
    }
  }
}

{
  name: 'export_joju',
  description: 'Export profile in Joju-ready format',
  inputSchema: {
    type: 'object',
    properties: {
      username: { type: 'string' },
      format: { type: 'string', enum: ['json', 'markdown'] }
    }
  }
}
```

**Benefits:**
- Use from Goose: "Ingest Matthew's resume from ~/Downloads/resume.pdf"
- Use from Claude Desktop: Natural language commands
- Use from any MCP client: Standardized interface
- Automated workflows: Chain multiple tools together

---

## Summary

### What We Have (Working Now)
1. ✅ Profile Builder (GitHub + 7 sources)
2. ✅ JSON Import (ReadCV, Joju exports)
3. ✅ Manual Entry
4. ✅ MCP Infrastructure (dormant)
5. ✅ Gmail Extractor (HCSS, adaptable)

### What We Need (Priority Order)
1. 🔴 **Resume Parser** (PDF/DOCX) - Highest user value
2. 🔴 **MCP Server for Joju** - Best AI integration
3. 🔴 **LinkedIn API** - Most comprehensive data
4. 🟡 CSV/Excel Import - Bulk data
5. 🟡 Designer APIs - Portfolio metrics

### Best Next Step
**Build Resume Parser + Activate MCP Server**
- Resume parser handles most common use case
- MCP server enables AI-driven workflows
- Both complement each other perfectly

---

**Want me to start with the resume parser or activate the MCP server for Joju?** 🎯
