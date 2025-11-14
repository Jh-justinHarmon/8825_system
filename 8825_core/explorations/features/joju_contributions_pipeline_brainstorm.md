# Joju Contributions Pipeline - Full Brainstorm

**Status:** Draft  
**Version:** 0.1.0  
**Created:** 2025-11-09  
**Owner:** Justin Harmon

---

## 📋 EXECUTIVE SUMMARY

### Problem
Users need to aggregate professional contributions from multiple sources (Dropbox, Figma, GitHub, Behance, etc.) into their Joju portfolio, but manually entering this data is:
- Time-consuming
- Incomplete
- Prone to errors
- Difficult to keep updated

### Solution
Build a **Contributions Mining Pipeline** that automatically discovers, attributes, and imports professional work from multiple sources into Joju's achievements database.

### Current Status
✅ **Proof of Concept Complete:**
- Local Dropbox miner successfully scanned 2,740 design files
- XMP parsing extracts creator attribution from .ai/.psd files
- Mining report format validated
- No API permission issues (uses local filesystem)

### Key Architecture Decision Needed
**Should we use MCP (Model Context Protocol) or direct APIs for integrations?**

---

## 🏗️ JOJU ARCHITECTURE REVIEW

### Current Stack
```
Frontend: React + TypeScript + Vite
Backend: Supabase (PostgreSQL + Auth)
Deployment: Vercel
State: React Context + TanStack Query
```

### Data Model
```
Users (Supabase Auth)
  ↓
Profiles (user_id, username, display_name, etc.)
  ↓
Achievements (user_id, type, data: JSONB, sort_order)
  ↓
Views (user_id, name, system_slug, is_pinned, template_key)
  ↓
View Sections (view_id, section_type, title, sort_order)
  ↓
View Items (view_section_id, achievement_id, sort_order)
```

### Key Insight
**Achievements table uses JSONB** - This is perfect for flexible contribution data from various sources!

```sql
achievements (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES profiles(id),
  type VARCHAR, -- 'work', 'education', 'project', 'contribution', etc.
  data JSONB,   -- ← Flexible schema for any contribution type
  sort_order INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

⚠️ **STATUS CHECK NEEDED:** Component built but not in production. Need to validate with Matthew:
- Is achievements schema finalized?
- When will it be production-ready?
- How is contribution data currently being received?

**See:** [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md) - Item #1

---

## 🔍 MCP VS API ANALYSIS

### What is MCP?
**Model Context Protocol** = Standardized way for LLMs to interact with external tools/services.

**MCP Benefits:**
- ✅ Standardized interface across tools
- ✅ Context-aware operations
- ✅ Built-in auth handling
- ✅ Composable tool chains
- ✅ LLM can orchestrate complex workflows

**MCP Limitations:**
- ❌ Not all services have MCP servers
- ❌ Additional abstraction layer
- ❌ May be slower than direct API calls
- ❌ Requires MCP bridge infrastructure

### Integration Decision Matrix

| Source | MCP Available? | API Available? | Recommendation | Rationale |
|--------|---------------|----------------|----------------|-----------|
| **Dropbox** | ❌ No official | ✅ Yes (REST) | **Local Files** | Team account API issues, local files proven |
| **Figma** | ❌ Not yet | ✅ Yes (REST) | **API** | Well-documented REST API, file metadata available |
| **GitHub** | ✅ Yes (unofficial) | ✅ Yes (REST/GraphQL) | **API** | GraphQL API superior for contribution queries |
| **Behance** | ❌ No | ⚠️ Limited | **Web Scraping** | No public API, may need scraping |
| **Dribbble** | ❌ No | ✅ Yes (REST) | **API** | REST API available for shots/projects |
| **LinkedIn** | ❌ No | ⚠️ Restricted | **Manual Import** | API heavily restricted, privacy concerns |
| **Adobe CC** | ❌ No | ⚠️ Limited | **XMP Parsing** | Local file metadata (proven with Dropbox miner) |
| **Notion** | ✅ Yes (official) | ✅ Yes (REST) | **MCP** | Official MCP server exists, complex data model |
| **Google Drive** | ❌ No | ✅ Yes (REST) | **API** | Well-documented Drive API |
| **Webflow** | ❌ No | ✅ Yes (REST) | **API** | Designer API available |

### MCP Strategy Recommendation

**Hybrid Approach:**
1. **Local File Mining** (Dropbox, Adobe CC files) → No API needed
2. **Direct APIs** (Figma, GitHub, Dribbble) → Fast, reliable, well-documented
3. **MCP Bridge** (Future) → For orchestrating multi-source imports via LLM

**Key Insight:** Don't force MCP where APIs work better. Use MCP for orchestration, not data fetching.

---

## 📊 CONTRIBUTION SOURCES ANALYSIS

### Priority Tier 1 (MVP) - High Value, Low Complexity

#### 1. **Local Design Files** ✅ VALIDATED
**Sources:** .ai, .psd, .indd, .sketch, .fig (exported), .afdesign, .afphoto  
**Method:** Local filesystem + XMP parsing  
**Attribution:** Creator name from XMP metadata  
**Status:** ✅ Working (2,740 files scanned successfully)

**Data Extracted:**
- File name, type, size
- Creator (from XMP paths)
- Creation/modification dates
- Tool used (Adobe Illustrator 25.2, etc.)
- Edit history (from XMP)

**Joju Mapping:**
```json
{
  "type": "design_work",
  "data": {
    "title": "shinola_collab_collection_2_runwell",
    "file_type": "Illustrator",
    "created_date": "2021-06-28",
    "tool": "Adobe Illustrator 25.2",
    "file_size_mb": 119.3,
    "tags": ["shinola", "collaboration", "product-design"],
    "creator": "justinharmon",
    "thumbnail_url": null,
    "source": "local_dropbox_miner"
  }
}
```

#### 2. **Figma** 🎯 HIGH PRIORITY
**API:** Figma REST API  
**Attribution:** File ownership, version history, contributors  
**Complexity:** Medium

**Figma API Capabilities:**
- List all files user has access to
- Get file metadata (name, thumbnail, last modified)
- Get version history (who edited, when)
- Get comments (collaboration data)
- Export thumbnails/previews

**Key Questions:**
- ✅ Does Figma API exist? **Yes - REST API**
- ✅ Can we get contributor data? **Yes - owner + version history**
- ✅ Can we get thumbnails? **Yes - export endpoint**
- ⚠️ Is there an MCP? **No official MCP yet**

**Recommended Approach:** Direct Figma API

**Data to Extract:**
```json
{
  "type": "design_file",
  "data": {
    "title": "Design System - Components",
    "platform": "Figma",
    "file_key": "abc123",
    "thumbnail_url": "https://...",
    "created_date": "2024-01-15",
    "last_modified": "2024-11-05",
    "owner": "justinharmon",
    "contributors": ["justinharmon", "designer2"],
    "version_count": 47,
    "comment_count": 12,
    "public_url": "https://figma.com/file/abc123",
    "source": "figma_api"
  }
}
```

**Implementation Plan:**
1. User connects Figma account (OAuth)
2. Scan all files user owns or contributed to
3. Extract metadata + thumbnails
4. Detect contribution type:
   - **Owner** → Created this file
   - **Editor** → Made significant edits
   - **Commenter** → Provided feedback
5. Import as achievements with `type: 'design_file'`

#### 3. **GitHub Contributions** 🎯 HIGH PRIORITY
**API:** GitHub GraphQL API  
**Attribution:** Commits, PRs, issues, repos owned  
**Complexity:** Medium

**GitHub Data Available:**
- Repositories owned/contributed to
- Commit history (author, date, files changed)
- Pull requests (created, reviewed, merged)
- Issues (created, commented on)
- Code review activity
- Languages used
- Stars/forks received

**Recommended Approach:** GitHub GraphQL API (more efficient than REST)

**GraphQL Query Example:**
```graphql
query UserContributions($username: String!) {
  user(login: $username) {
    repositories(first: 100, ownerAffiliations: [OWNER, COLLABORATOR]) {
      nodes {
        name
        description
        createdAt
        updatedAt
        primaryLanguage { name }
        stargazerCount
        forkCount
        url
      }
    }
    contributionsCollection(from: "2024-01-01T00:00:00Z") {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
    }
  }
}
```

**Joju Mapping:**
```json
{
  "type": "code_project",
  "data": {
    "title": "8825 PCMS v3.0",
    "platform": "GitHub",
    "description": "Personal Context Memory System",
    "repo_url": "https://github.com/...",
    "created_date": "2024-01-01",
    "primary_language": "TypeScript",
    "stars": 15,
    "forks": 3,
    "my_role": "Owner",
    "commit_count": 247,
    "source": "github_api"
  }
}
```

### Priority Tier 2 (Post-MVP) - High Value, Higher Complexity

#### 4. **Behance** 🎨
**API:** ⚠️ No official public API  
**Attribution:** Project ownership  
**Method:** Web scraping or manual import

**Current Options:**
1. **Manual CSV Import** - User exports project list
2. **Web Scraping** - Parse public profile page
3. **Adobe API** - Check if Behance is part of Adobe Creative Cloud API

**Recommended Approach:** Start with manual import, investigate Adobe CC API

#### 5. **Dribbble** 🏀
**API:** ✅ REST API available  
**Attribution:** Shot ownership, team collaboration

**Dribbble API Capabilities:**
- User shots (designs posted)
- Shot metadata (views, likes, comments)
- Team membership
- Projects

**Joju Mapping:**
```json
{
  "type": "design_showcase",
  "data": {
    "title": "Mobile App Redesign",
    "platform": "Dribbble",
    "thumbnail_url": "https://...",
    "views": 1247,
    "likes": 89,
    "comments": 12,
    "tags": ["mobile", "ui", "redesign"],
    "posted_date": "2024-03-15",
    "public_url": "https://dribbble.com/shots/...",
    "source": "dribbble_api"
  }
}
```

#### 6. **LinkedIn Experience** 💼
**API:** ⚠️ Heavily restricted  
**Attribution:** Work history, skills, recommendations  
**Method:** Manual import or LinkedIn Data Export

**Recommended Approach:** 
- Option A: User requests LinkedIn data export (GDPR)
- Option B: Manual form entry in Joju
- Option C: Resume parser (if user uploads LinkedIn PDF)

### Priority Tier 3 (Future) - Lower Priority

#### 7. **Google Drive Design Files**
**API:** ✅ Google Drive API  
**Similar to:** Dropbox approach, but cloud-based

#### 8. **Webflow Sites**
**API:** ✅ Webflow Designer API  
**Data:** Sites designed, pages created

#### 9. **Medium / Substack Articles**
**API:** Medium API (limited), RSS feeds  
**Data:** Articles written, publications

#### 10. **YouTube / Vimeo Videos**
**API:** ✅ Both have APIs  
**Data:** Videos created, channel stats

---

## 🏗️ PROPOSED ARCHITECTURE

### Option A: Direct Import (Recommended for MVP)

```
User Action
  ↓
Connect Account (OAuth)
  ↓
Scan Source (API/Local)
  ↓
Transform to Achievements
  ↓
Supabase Insert
  ↓
Joju UI (user reviews/edits)
```

**Pros:**
- ✅ Simple, direct
- ✅ Fast
- ✅ No MCP infrastructure needed
- ✅ Works with current Joju architecture

**Cons:**
- ❌ Each source needs custom code
- ❌ No orchestration layer
- ❌ User triggers each import manually

### Option B: MCP Orchestration (Future Enhancement)

```
User Request to LLM
  ↓
MCP Bridge (8825 Core)
  ↓
Parallel Tool Calls:
  - local_file_miner
  - figma_connector
  - github_connector
  - etc.
  ↓
Aggregate Results
  ↓
Deduplicate
  ↓
Transform to Achievements
  ↓
Supabase Insert via API
  ↓
Confirmation to User
```

**Pros:**
- ✅ Intelligent orchestration
- ✅ Can handle complex workflows
- ✅ Single "import everything" command
- ✅ LLM can resolve ambiguities

**Cons:**
- ❌ Requires MCP bridge infrastructure
- ❌ More complex
- ❌ Slower than direct API calls
- ❌ Overkill for simple imports

### Recommended Hybrid Approach

**Phase 1 (MVP):** Direct imports via Joju UI
```
Joju Settings → Integrations → Connect Figma
  → Scans files
  → Shows preview
  → User confirms import
```

**Phase 2 (Enhanced):** 8825 MCP Bridge
```
User to 8825: "Import all my design work into Joju"
  → MCP orchestrates multiple sources
  → Shows aggregated preview
  → User confirms
  → Imports to Supabase
```

---

## 🎯 MVP RECOMMENDATION

### Build These 3 Miners First:

#### 1. **Local Design Files Miner** ✅ DONE
- Status: Working
- Sources: Dropbox local files
- Next: Package as reusable module

#### 2. **Figma Connector**
- Priority: HIGH
- Method: Figma REST API
- Timeline: 1-2 weeks
- Value: Captures most active design work

#### 3. **GitHub Connector**
- Priority: HIGH  
- Method: GitHub GraphQL API
- Timeline: 1-2 weeks
- Value: Captures code contributions

**Why these three?**
- **Dropbox:** Proven to work, covers portfolio archive
- **Figma:** Where current design work lives
- **GitHub:** Where current code work lives

**Together:** Covers 80%+ of professional contributions for most users

---

## 📋 DATA-DRIVEN PRIORITIZATION FRAMEWORK

### Proposed: Surveys Workspace

**Location:** `/8825/8825-system/8825_core/explorations/surveys/`

**Purpose:**
- Track user requests for integrations
- Measure demand for each source
- Prioritize based on data
- Connect to Notion for roadmap tracking

**Survey Structure:**
```markdown
## Joju Integration Priority Survey

**Q1:** Which platforms do you currently use for professional work?
- [ ] Figma
- [ ] GitHub
- [ ] Behance
- [ ] Dribbble
- [ ] LinkedIn
- [ ] Webflow
- [ ] Adobe CC (Illustrator, Photoshop, etc.)
- [ ] Other: ___

**Q2:** Which ONE integration would add the most value to your Joju portfolio?
(Ranked choice)

**Q3:** How many projects/files do you have on each platform?
- Figma: ___
- GitHub: ___
- etc.

**Q4:** How often do you update your portfolio?
- Daily
- Weekly
- Monthly
- Quarterly
- Annually

**Q5:** Would you pay for automatic contribution mining?
- Yes
- No
- Depends on price
```

**Integration with Notion:**
```
8825 Surveys Workspace
  ↓
Export Results → CSV
  ↓
Import to Notion Database
  ↓
Calculate Priority Score:
  = (demand × 0.4) + (implementation_ease × 0.3) + (value × 0.3)
  ↓
Roadmap Prioritization
```

---

## 🔧 IMPLEMENTATION PLAN

### Phase 1: MVP (4-6 weeks)

**Week 1-2: Local Miner Enhancement**
- [x] XMP parsing working
- [ ] Package as reusable module
- [ ] Add thumbnail extraction
- [ ] Improve contributor detection
- [ ] Create import UI in Joju

**Week 3-4: Figma Connector**
- [ ] Figma OAuth integration
- [ ] API endpoints for file scanning
- [ ] Thumbnail download
- [ ] Transform to achievements format
- [ ] Import UI in Joju

**Week 5-6: GitHub Connector**
- [ ] GitHub OAuth integration
- [ ] GraphQL query implementation
- [ ] Repository metadata extraction
- [ ] Contribution stats aggregation
- [ ] Import UI in Joju

### Phase 2: Surveys & Prioritization (2 weeks)

**Week 1:**
- [ ] Create surveys workspace
- [ ] Design initial survey
- [ ] Set up Notion integration
- [ ] Recruit beta users

**Week 2:**
- [ ] Collect responses
- [ ] Analyze data
- [ ] Calculate priority scores
- [ ] Update roadmap

### Phase 3: Additional Integrations (TBD)

Based on survey results, implement:
- [ ] Dribbble connector
- [ ] Behance import (manual or scraped)
- [ ] LinkedIn data import
- [ ] Google Drive file miner
- [ ] Other sources as prioritized

### Phase 4: MCP Bridge (Future)

- [ ] Design MCP server architecture
- [ ] Create contribution mining tools
- [ ] Implement orchestration layer
- [ ] Test with 8825 PCMS integration

---

## ⚠️ GAPS TO ADDRESS BEFORE IMPLEMENTATION

### 1. Achievements Component Status ⚠️ CRITICAL
**Problem:** Component built but not in production  
**Impact:** Can't import contributions if achievements table isn't ready  
**Action:** Validate with Matthew in 1:1
- Is schema finalized?
- When will it be production-ready?
- Should we wait or build in parallel?

**See:** [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md) - Item #1

---

### 2. Deduplication Strategy ⚠️ HIGH PRIORITY
**Problem:** Duplicate contributions across platforms  
**Opportunity:** Piggyback on file reduction for Dropbox space savings  
**Action:** Workshop strategy with Matthew, add to SMART goals

**See:** 
- [Dropbox File Reduction Brainstorm](./dropbox_file_reduction_brainstorm.md)
- [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md) - Item #4

---

### 3. Thumbnail Generation 📦 PARKING LOT
**Problem:** Local files need thumbnails for Joju gallery  
**Decision:** NOT NEEDED FOR MVP  
**Rationale:** Show file type icons instead, add later if needed

**Options (if needed in future):**
- ImageMagick/sips to generate thumbnails
- Extract embedded thumbnails from XMP
- Use platform thumbnails (Figma, GitHub)

---

### 4. Import UI Flow ⚠️ NEEDS DESIGN SPRINT
**Problem:** No UI/UX designed for import flow  
**Impact:** Can't build connectors without knowing user experience  
**Action:** Workshop with Matthew, potentially run design sprint

**Proposed Flow (needs validation):**
```
Joju Settings → Integrations → Connect Figma
  → OAuth flow
  → Scan files (loading state)
  → Preview: "Found 12 files"
  → Select files to import
  → Confirm → Import to achievements
```

**Questions:**
- Is this the right approach for Joju?
- What's the lowest friction execution?
- Should we run a design sprint?

**See:** [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md) - Item #2

---

### 5. Rate Limiting & Error Handling ⚠️ NEEDS TECHNICAL SPEC
**Problem:** APIs have rate limits and can fail  
**Impact:** User experience degrades without proper handling  
**Action:** Add to technical spec for each connector

**Needed:**
- Exponential backoff for retries
- Queue for large imports
- Progress indicators
- Error recovery flows

**See:** [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md) - Item #2

---

## 🎨 USER EXPERIENCE FLOWS

⚠️ **NOTE:** These flows need validation in design sprint before implementation

### Flow 1: First-Time User

```
1. Sign up for Joju
2. See empty achievements list
3. Banner: "Import your work from Figma, GitHub, Dropbox"
4. Click "Connect Figma"
5. OAuth → Select files to import
6. Preview: "Found 12 design files"
7. Confirm import
8. Achievements populated
9. Drag into views
10. Publish portfolio
```

### Flow 2: Power User (8825 + Joju)

```
1. User has 8825 PCMS + Joju account
2. Says to 8825: "Update my Joju portfolio with all new work"
3. 8825 MCP Bridge:
   - Scans local Dropbox folder (new files since last scan)
   - Checks Figma (new files/versions)
   - Checks GitHub (new repos/commits)
4. Aggregates: "Found 3 new design files, 2 new repos, 47 commits"
5. Shows preview
6. User confirms
7. Imports to Joju
8. User gets notification: "Joju updated with 5 new achievements"
```

### Flow 3: Scheduled Auto-Import

```
1. User enables "Auto-import" in Joju settings
2. Sets schedule: "Weekly on Monday"
3. Every Monday:
   - Background job scans connected sources
   - Finds new contributions
   - Auto-imports if < 10 new items
   - Sends email summary if > 10 items for review
4. User's portfolio stays current automatically
```

---

## 🔐 SECURITY & PRIVACY

### OAuth Best Practices
- Use Supabase Auth for OAuth flow management
- Store tokens encrypted in Supabase
- Implement token refresh logic
- Allow users to disconnect integrations
- Delete tokens on disconnect

### Data Ownership
- User controls what gets imported
- User can edit/delete imported achievements
- User can disconnect sources anytime
- Respect platform TOS (don't over-scrape)

### Rate Limiting
- Respect API rate limits
- Implement backoff/retry logic
- Queue large imports
- Show progress to user

---

## 📊 SUCCESS METRICS

### MVP Success Criteria

**Adoption:**
- 50% of new users connect at least one integration
- 25% of users connect 2+ integrations
- Average 20+ achievements imported per user

**Retention:**
- Users with imported achievements have 2x retention vs manual entry
- 30% of users re-scan monthly for updates

**Value:**
- Users report "significantly easier" portfolio creation
- 80%+ of imported achievements are kept (not deleted)
- Average time to first published view: < 10 minutes

### Data to Track

```sql
-- Integration adoption
SELECT 
  integration_type,
  COUNT(DISTINCT user_id) as users,
  COUNT(*) as connections,
  AVG(achievements_imported) as avg_imports
FROM user_integrations
GROUP BY integration_type;

-- Import success rate
SELECT
  source,
  COUNT(*) as total_imported,
  SUM(CASE WHEN deleted_at IS NULL THEN 1 ELSE 0 END) as kept,
  ROUND(100.0 * SUM(CASE WHEN deleted_at IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as keep_rate
FROM achievements
WHERE source IN ('local_miner', 'figma_api', 'github_api')
GROUP BY source;
```

---

## 🚀 NEXT STEPS

⚠️ **IMPORTANT:** Implementation on HOLD pending Matthew 1:1 to address critical gaps.

### Critical Path (Must Complete Before Building)

**1. Matthew 1:1 Meeting** 🎯 BLOCKING
- [ ] Schedule meeting
- [ ] Validate achievements component status
- [ ] Workshop import UI flow approach
- [ ] Decide: Design sprint needed?
- [ ] Align on Q1 2025 SMART goals

**Deliverables:**
- Go/No-Go decision on implementation
- Timeline for achievements component
- Design sprint scheduled (if needed)
- SMART goals finalized

**See:** [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md)

---

**2. Design Sprint (If Approved)** 🎯 BLOCKING
- [ ] Workshop user flow for integrations
- [ ] Create UI mockups (Figma)
- [ ] Define technical specs (OAuth, rate limiting, errors)
- [ ] Validate with 5 beta users

**Deliverables:**
- User flow diagrams
- UI mockups
- Technical specifications
- Validated approach

**Timeline:** 1-2 days (rapid workshop)

---

### Phase 1: Foundation (After Unblocked)

**3. Surveys Workspace** ✅ COMPLETE
- [x] Set up directory structure
- [x] Create integration priority survey
- [x] Plan Notion integration

**Next:** Launch when ready to recruit respondents

---

**4. Package Local Miner**
- [ ] Move to `8825_core/integrations/contribution_miners/`
- [ ] Create modular API
- [ ] Add CLI with flags
- [ ] Document usage
- [ ] Add unit tests

**Timeline:** 2-3 days  
**Owner:** Justin

---

**5. Deduplication + File Reduction Plan**
- [ ] Finalize strategy with Matthew
- [ ] Calculate estimated savings
- [ ] Define safety protocols
- [ ] Add report-only mode to scanner

**Timeline:** 1 week  
**Owner:** Justin (with Matthew input)

**See:** [Dropbox File Reduction Brainstorm](./dropbox_file_reduction_brainstorm.md)

---

### Phase 2: Cloud Integrations (After Design Sprint)

**6. Build Top Priority Integration** (Likely Figma or GitHub)
- [ ] Implement OAuth flow
- [ ] Build file/repo scanner
- [ ] Transform to achievements format
- [ ] Create import UI (per design sprint)
- [ ] Test with 5 beta users

**Timeline:** 2 weeks  
**Prerequisites:** Achievements component live, design sprint complete

---

**7. Run Integration Priority Survey**
- [ ] Recruit 50+ respondents
- [ ] Collect responses (2 weeks)
- [ ] Analyze results
- [ ] Calculate priority scores
- [ ] Update roadmap

**Timeline:** 3 weeks total  
**Deliverables:** Data-driven roadmap for Q2 integrations

---

### Phase 3: Iteration & Expansion (Q2 2025)

**8. Build Second Integration**
- Based on survey results
- 2-week build
- Beta test

**9. Add Deduplication**
- Implement full algorithm
- User review UI
- Merge workflows

**10. File Reduction Tool**
- If space savings justify effort
- Archive functionality
- Rollback capability

**11. MCP Bridge** (Future)
- If demand justifies complexity
- Orchestration layer
- Multi-source imports

---

### ⏸️ PARKING LOT (Not Needed for MVP)

- Thumbnail generation (use file type icons instead)
- Auto-import scheduling (manual import first)
- Team contribution tracking (solo users first)
- Analytics dashboard (focus on import UX)

---

## 📝 OPEN QUESTIONS

### Q1: Should Joju have its own MCP server?

**Scenario:** User asks 8825: "Show me my design work from the last quarter"

**Option A:** 8825 MCP → Joju API → Query achievements
**Option B:** 8825 MCP → Joju MCP Server → Direct DB access

**Recommendation:** Start with API (simpler), consider MCP server if complex queries needed

### **1. Deduplication Strategy** ⚠️ HIGH PRIORITY
**Problem:** Same project might exist in multiple places:
- Local Dropbox (.ai file)
- Figma (working file)
- Behance (showcase)

**Current Plan:** User review potential duplicates (manual)

**Improvement:** Add content hash matching + metadata similarity

**IMPORTANT - Two-Part Opportunity:**

#### Part A: Contribution Deduplication
- Merge duplicate contributions across platforms
- User reviews and confirms merges
- Phase 2 (after MVP integrations)

#### Part B: Dropbox File Reduction (Piggyback)
**NEW:** When we run full Dropbox scan for contributions, we can ALSO:
1. Identify duplicate files (same content, different paths)
2. Archive/snapshot duplicates
3. Calculate storage space savings
4. Reduce Dropbox footprint

**Prelim Plan Needed:**
- File reduction protocol (what to archive, what to delete)
- Estimated space savings calculation (% of total Dropbox)
- Safety measures (rollback, manifest, 30-day retention)
- Archive structure (/Archive/Duplicates_YYYY-MM-DD/)

**See:** [Dropbox File Reduction Brainstorm](./dropbox_file_reduction_brainstorm.md)

**Action:** 
- 🎯 Brainstorm file reduction strategy (Matthew 1:1)
- 🎯 Add to SMART goals (Q1 2025)
- 🔄 Build report-only version with contribution scanner (MVP)
- 🔄 Build full archive tool in Phase 2 if savings justify effort

### Q3: What's the business model for integrations?

**Free Tier:**
- Manual imports
- Local file mining
- 1 connected integration

**Pro Tier ($9/mo):**
- Unlimited integrations
- Auto-import (scheduled)
- Priority support

**Team Tier ($29/mo per user):**
- Team contribution tracking
- Shared achievement libraries
- Analytics dashboard

### Q4: How do we handle team contributions?

**Scenario:** Design project had 3 collaborators

**Options:**
1. **All get credit** - Everyone who contributed gets achievement
2. **Primary creator only** - Only file owner gets it
3. **Proportional credit** - Based on contribution %

**Recommendation:** Start with #1 (everyone gets credit), add #3 later for analytics

---

## 🎯 DECISION LOG

| Date | Decision | Rationale | Owner |
|------|----------|-----------|--------|
| 2025-11-09 | Use local files for Dropbox instead of API | Team account API restrictions, local proven to work | Justin |
| 2025-11-09 | Direct APIs over MCP for MVP | APIs more reliable, faster, simpler for initial integrations | Justin |
| 2025-11-09 | Prioritize Figma + GitHub after local miner | Highest impact, well-documented APIs | Justin |
| 2025-11-09 | Create surveys workspace for data-driven prioritization | Need user input to guide roadmap | Justin |
| 2025-11-09 | HOLD implementation pending Matthew 1:1 | Achievements component status unknown, UI flow not designed | Justin |
| 2025-11-09 | Parking lot: Thumbnail generation | Not needed for MVP, use file type icons | Justin |
| 2025-11-09 | Add file reduction to deduplication scan | Piggyback opportunity, calculate space savings | Justin |
| TBD | Achievements component ready for contributions? | Needs Matthew validation | Matthew |
| TBD | Design sprint approved? | Needs Matthew approval | Matthew |
| TBD | MCP bridge architecture | Defer until MVP validated | TBD |
| TBD | Auto-import vs manual | Depends on user feedback | TBD |

---

## 📚 REFERENCES

### APIs Reviewed
- [Figma API Documentation](https://www.figma.com/developers/api)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [Dribbble API](https://developer.dribbble.com/)
- [Dropbox API](https://www.dropbox.com/developers/documentation)
- [Webflow Designer API](https://developers.webflow.com/)

### Related Documents
- [Matthew 1:1 Agenda](./joju_contributions_1on1_matthew.md) - Critical items to discuss
- [Dropbox File Reduction Brainstorm](./dropbox_file_reduction_brainstorm.md) - Space savings strategy
- [Joju Integration Priority Survey](../../surveys/joju_integration_priority_survey.md) - Ready to launch
- [Surveys Workspace README](../../surveys/README.md) - Data-driven prioritization framework
- `local_miner.py` - Working Dropbox local file miner (PoC complete)
- `dropbox_miner.py` - Original API-based miner (deprecated due to API restrictions)
- `/joju/SUPABASE_SETUP.md` - Joju database schema
- `phils_ledger_pipeline_brainstorm.md` - Similar multi-source pipeline

### Prior Art
- 8825 PCMS mining protocol (two-stage approach)
- Phil's Ledger bill routing (multi-source ingestion)

---

## ✅ CONCLUSION

### Current Status: ⏸️ ON HOLD

**Implementation PAUSED pending Matthew 1:1 to address critical gaps:**

1. ⚠️ **Achievements component status** - Built but not in production
2. ⚠️ **Import UI flow** - Not designed, needs workshop/sprint
3. ⚠️ **Rate limiting/errors** - No technical spec yet
4. 🎯 **Deduplication + file reduction** - Strategy needs finalization

---

### What's Complete ✅

1. **Comprehensive brainstorm** - All integrations researched
2. **MCP vs API analysis** - Decision matrix created
3. **Local miner PoC** - 2,740 files scanned successfully
4. **Surveys workspace** - Ready to launch
5. **File reduction opportunity** - Identified piggyback strategy
6. **Matthew 1:1 agenda** - All critical items documented

---

### Critical Path Forward

**Before building anything:**

1. **Matthew 1:1** → Validate approach, get go/no-go
2. **Design sprint** (if approved) → Workshop UI/UX
3. **SMART goals alignment** → Q1 2025 objectives

**After unblocked:**

4. **Package local miner** → Production-ready module
5. **Deduplication plan** → Finalize with Matthew
6. **Build top integration** → Figma or GitHub (based on survey)
7. **Launch survey** → Validate priorities with data

---

### Key Insights

**1. Hybrid Approach Validated ✅**
- Local files → Filesystem (proven working)
- Cloud APIs → Direct integration (fast, reliable)
- MCP → Orchestration layer (future enhancement)

**2. Data-Driven Prioritization ✅**
- Survey framework ready
- Priority calculation formula defined
- Notion integration planned

**3. Piggyback Opportunities ✅**
- Deduplication scan → File reduction
- Contribution mining → Space savings
- Estimated 10-20% Dropbox storage reduction

**4. Design-First Approach ✅**
- Can't build without UI/UX clarity
- Design sprint needed before implementation
- User flows require validation

---

### Success Metrics (When Unblocked)

**Phase 1 Success:**
- ✅ Achievements component production-ready
- ✅ Local miner packaged and documented
- ✅ Design sprint complete with validated flows
- ✅ SMART goals aligned with Matthew

**MVP Success:**
- 1 cloud integration working (Figma or GitHub)
- 50+ survey responses analyzed
- Deduplication strategy finalized
- File reduction savings calculated

**Full Success:**
- 3 working integrations (Local + 2 cloud)
- Data-driven roadmap for Q2
- Users report "significantly easier" portfolio creation
- 50%+ of users connect at least one integration

---

### Next Action

**→ Schedule Matthew 1:1**  
**→ Review [1:1 Agenda](./joju_contributions_1on1_matthew.md)**  
**→ Get go/no-go decision**

---

**Bottom Line:** The research and planning are complete. The local miner proves the concept works. Now we need organizational alignment (Matthew 1:1) and design clarity (UI workshop) before building cloud integrations. The surveys framework is ready to validate priorities with real user data when the time is right.

**This is the right pause point.**
