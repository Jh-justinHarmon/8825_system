# Matthew (MG) 1:1 - Assembled Agenda

**Date:** 2025-11-10  
**Purpose:** Joju Contributions Workshop + Skills/Goals Discussion  
**Status:** Ready for Meeting

---

## 🎯 Meeting Objectives

1. **Validate Joju data model** for contributions (achievements JSONB schema)
2. **Review component status** (built but not in production?)
3. **Workshop user flow** for integrations
4. **Decide if design sprint needed**
5. **Align on Q1 2025 SMART goals**
6. **Discuss Hard Skills, Soft Skills, Personal Goals** (job-related)

---

## PART 1: JOJU CONTRIBUTIONS PIPELINE

### 1. Achievements Data Model - Validation Needed ⚠️

**Context:**
- Brainstorm assumes achievements table with JSONB is production-ready
- Component built but not in production
- Need to understand current state before building integrations

**Questions:**

1. **What's the current status of the achievements component?**
   - Is it in production or still in development?
   - What's blocking production deployment?

2. **How is contribution data currently being received/stored?**
   - Is the JSONB schema finalized?
   - Any constraints or limitations?

3. **What does the data model look like today?**
   - Can we review the actual Supabase schema?
   - Any recent changes?

4. **Example transformation - Does this fit?**
   ```json
   {
     "type": "design_file",
     "data": {
       "title": "Design System - Components",
       "platform": "Figma",
       "file_key": "abc123",
       "thumbnail_url": "https://...",
       "created_date": "2024-01-15",
       "contributors": ["justinharmon", "designer2"],
       "source": "figma_api"
     }
   }
   ```

5. **Timeline: When will achievements be production-ready?**

**Decision Needed:**
- ✅ Proceed with integration development
- ⏸️ Pause until achievements component ships
- 🔄 Build in parallel, integrate when ready

---

### 2. User Flow & Integration Approach - Design Sprint?

**Context:**
- Local Dropbox miner proven (2,740 files scanned)
- Ready to build cloud integrations (Figma, GitHub)
- No UI/UX designed yet for import flow

**Proposed Flow:**
```
Joju Settings → Integrations → Connect Figma
  → OAuth flow
  → Scan files (loading state)
  → Preview: "Found 12 files"
  → Select files to import
  → Confirm → Import to achievements
```

**Questions:**

1. **Is this the right approach for Joju?**
   - Settings-based integrations?
   - Or different entry point?

2. **What's the lowest friction execution?**
   - One-time import vs ongoing sync?
   - Manual selection vs auto-import?
   - Bulk import vs per-file review?

3. **Should we run a design sprint?**
   - Full 5-day sprint?
   - Or 1-day rapid workshop?
   - Who should participate?

4. **What user flows already exist in Joju?**
   - Onboarding flow?
   - Settings patterns?
   - Similar integrations we can reference?

5. **Rate limiting & error handling patterns?**
   - How does Joju handle long-running operations?
   - Progress indicators?
   - Error recovery?

**Recommendation:**
If this is the approach, **run a design sprint** on:
- User flow for 8825 contribution integration
- Lowest friction execution
- Error states and edge cases

---

### 3. Integration Priority Survey

**Context:**
- Survey workspace created
- 16-question survey ready
- Targets 50+ responses from Joju users

**Questions:**

1. **Do we have 50+ Joju users to survey?**
   - Current user count?
   - Beta vs production users?

2. **Should we survey before or after design sprint?**
   - Before: Validates which integrations to prioritize
   - After: Validates designed approach

3. **Who owns recruiting respondents?**

4. **Timeline: When to launch?**

**Decision Needed:**
- Launch survey now (validate priorities)
- Wait until after design sprint (validate approach)
- Skip survey, use analytics/feedback instead

---

### 4. Deduplication & File Reduction Strategy

**Context:**
- Same project might exist in multiple places (Dropbox, Figma, Behance)
- Need deduplication for contributions
- Opportunity for Dropbox file reduction

**Two-Part Strategy:**

#### Part A: Contribution Deduplication (Phase 2)
1. Content hash matching (MD5 of file)
2. Metadata similarity (name + date + size)
3. User review of potential duplicates
4. Merge duplicates → single achievement

#### Part B: Dropbox File Reduction (Piggyback)
If we're already scanning all files, we can ALSO:
1. Identify duplicate files (same content, different locations)
2. Create snapshots/archives of duplicates
3. Calculate space savings potential
4. Optionally delete duplicates (after user confirmation)

**Questions:**

1. **Should we build file reduction into the scanner?**
2. **What's the risk tolerance?**
   - Aggressive (auto-delete)?
   - Conservative (user confirms each)?
   - Moderate (auto-archive, manual delete)?
3. **Is there an existing Dropbox file reduction exploration?**
4. **Timeline: Build this with MVP or later?**

---

### 5. SMART Goals Alignment - Q1 2025

#### Goal 1: Production-Ready Local Miner
**Specific:** Package local_miner.py as reusable module  
**Measurable:** CLI + API, documented, tested  
**Achievable:** Extend existing proof of concept  
**Relevant:** Foundation for all file-based integrations  
**Time-bound:** Complete by Dec 15, 2024

**Key Results:**
- Modular API (importable as library)
- CLI with --folder, --output, --thumbnails flags
- Unit tests (>80% coverage)
- Documentation (README + code comments)

---

#### Goal 2: Integration Priority Survey Results
**Specific:** Run survey, analyze, update roadmap  
**Measurable:** 50+ responses, priority scores calculated  
**Achievable:** Survey ready, need recruitment plan  
**Relevant:** Data-driven roadmap for Q1 2025  
**Time-bound:** Complete by Jan 15, 2025

**Key Results:**
- 50+ survey responses
- Analysis report with priority scores
- Updated Joju roadmap in Notion
- Top 3 integrations identified

---

#### Goal 3: Design Sprint - Contributions UX
**Specific:** Workshop user flow for integrations  
**Measurable:** UI mockups, user flow diagrams, technical spec  
**Achievable:** 1-2 day sprint with team  
**Relevant:** Required before building cloud integrations  
**Time-bound:** Complete by Jan 30, 2025

**Key Results:**
- User flow diagram (Settings → Import → Review → Confirm)
- UI mockups (Figma)
- Technical spec (OAuth, API calls, error handling)
- Rate limiting & progress indicator patterns

---

#### Goal 4: MVP Cloud Integration (TBD based on survey)
**Specific:** Build top-priority integration (likely Figma or GitHub)  
**Measurable:** Working OAuth, import flow, 5 beta users tested  
**Achievable:** 2-week build after design sprint  
**Relevant:** Validates cloud integration approach  
**Time-bound:** Complete by Feb 28, 2025

**Key Results:**
- OAuth flow working
- User can scan & preview files
- User can import selected files
- Achievements populate in Joju
- 0 critical bugs
- 5 beta users successfully import

---

#### Goal 5: Notion/Windsurf Task Management System
**Specific:** Build intelligent task tracking/management system integrating Notion + Windsurf  
**Measurable:** Automated task sync, AI-powered prioritization, working dashboard  
**Achievable:** Leverage existing Notion API + Windsurf capabilities  
**Relevant:** Improves productivity and project visibility across tools  
**Time-bound:** Complete by Feb 15, 2025

**Key Results:**
- Bi-directional sync between Notion and Windsurf task lists
- AI-powered task prioritization based on context/deadlines
- Automated task creation from meeting notes/conversations
- Dashboard showing task status across all projects
- Intelligence layer that suggests next actions based on current context

---

## PART 2: SKILLS & PERSONAL GOALS (JOB-RELATED)

### NEW: Skills & Goals Discussion

**Context:** Matthew requested I think about and come up with lists for:
- Hard Skills
- Soft Skills  
- Personal Goals

**Note:** These should be related to my job, not specifically about me personally.

---

### Hard Skills (Customer Success + Strategic Technical)

**Current Strengths:**
- [ ] Customer onboarding & training
- [ ] Technical troubleshooting & support
- [ ] Product documentation & knowledge base creation
- [ ] User feedback collection & analysis
- [ ] AI/LLM integration (prompts, workflows, agent design)
- [ ] Agentic workflow design (with AI assistance)
- [ ] Product thinking & requirements gathering
- [ ] Problem decomposition & systems thinking

**Skills to Develop (PRIORITY 1: Customer Success):**
- [ ] **Customer engagement strategies** (proactive outreach, retention)
- [ ] **Networking & relationship building** (LinkedIn, events, community)
- [ ] **Customer success metrics** (NPS, churn, engagement tracking)
- [ ] **Account management** (upsells, renewals, expansion)
- [ ] **Community building** (forums, user groups, advocacy programs)
- [ ] **Customer education** (webinars, workshops, training programs)
- [ ] **Sales enablement** (demos, case studies, ROI presentations)
- [ ] **Customer health monitoring** (usage analytics, early warning systems)

**Skills to Develop (PRIORITY 2: Technical - Joju Initiatives):**
- [ ] **Data mining & contribution extraction** (Dropbox, Figma, GitHub scanning)
- [ ] **Figma API integration** (OAuth, file scanning, metadata extraction)
- [ ] **GitHub API integration** (repo scanning, contribution tracking)
- [ ] **Agentic automation flows** (Make.com, n8n, workflow orchestration)
- [ ] **Integration pipeline design** (data normalization, deduplication)
- [ ] **Python scripting** (automation for customer-facing tools)
- [ ] **API integration patterns** (OAuth flows, rate limiting, error handling)
- [ ] **Database basics** (Supabase queries for customer data insights)

**Questions for Matthew:**
1. What customer success skills are most critical for my role at Joju?
2. How should I balance customer engagement vs building technical integrations?
3. Which technical skills (Figma/GitHub/Make automation) should I prioritize?
4. Can technical projects (contributions pipeline) support customer success goals?
5. What networking/community building should I prioritize?

---

### Soft Skills (Customer-Facing & Professional)

**Current Strengths:**
- [ ] Problem-solving & systems thinking
- [ ] Written communication (documentation, specs)
- [ ] Self-directed learning
- [ ] Project planning & organization
- [ ] Attention to detail
- [ ] Adaptability to new tools/frameworks

**Skills to Develop (PRIORITY: Customer Success):**
- [ ] **Active listening & empathy** (understanding customer pain points)
- [ ] **Relationship building** (trust, rapport, long-term connections)
- [ ] **Proactive communication** (check-ins, updates, anticipating needs)
- [ ] **Presentation & demo skills** (engaging, clear, value-focused)
- [ ] **Stakeholder management** (non-technical audiences, executives)
- [ ] **Conflict resolution** (handling complaints, difficult conversations)
- [ ] **Persuasion & influence** (driving adoption, behavior change)
- [ ] **Networking** (conferences, LinkedIn, community events)
- [ ] **Time management** (balancing multiple customer relationships)
- [ ] **Emotional intelligence** (reading the room, adapting communication style)

**Skills to Develop (Professional - Secondary):**
- [ ] Team collaboration (async/remote)
- [ ] Mentoring/knowledge sharing
- [ ] Strategic thinking (business context)
- [ ] Giving/receiving feedback

**Questions for Matthew:**
1. What customer-facing soft skills are most valuable for my role?
2. How can I improve my customer engagement and networking?
3. What's the best way to build relationships with Joju users?
4. How should I prioritize customer success vs technical work?

---

### Personal Goals (Job-Related)

**Q1 2025 Goals:**

#### Goal 1: Customer Engagement & Networking (PRIORITY)
- **What:** Build proactive customer engagement system and expand professional network
- **Why:** Customer success is core to my role; relationships drive retention and growth
- **How:** 
  - Weekly customer check-ins (5+ users/week)
  - Monthly LinkedIn networking (connect with 10+ relevant people)
  - Attend 1 industry event or webinar per month
  - Create customer feedback loop (surveys, interviews)
- **Measure:** 
  - 20+ meaningful customer conversations per month
  - 30+ new professional connections
  - 3+ customer success stories documented
  - Measurable improvement in customer satisfaction/engagement

#### Goal 2: Customer Success Skills Development
- **What:** Master customer success fundamentals (metrics, strategies, tools)
- **Why:** Need structured approach to customer engagement, not just ad-hoc support
- **How:**
  - Complete customer success certification or course
  - Learn NPS, churn analysis, health scoring
  - Study best practices (case studies, books, mentors)
  - Practice demos and presentations weekly
- **Measure:**
  - Certification completed
  - Implement customer health dashboard
  - Deliver 5+ effective product demos
  - Positive feedback on presentation skills

#### Goal 3: Community Building & Advocacy
- **What:** Create and nurture Joju user community
- **Why:** Engaged community = retention, referrals, and product feedback
- **How:**
  - Launch user forum or Slack community
  - Host monthly user office hours or Q&A
  - Identify and cultivate power users/advocates
  - Create user-generated content opportunities
- **Measure:**
  - Community launched with 25+ active members
  - 3+ power users identified and engaged
  - Monthly engagement metrics trending up
  - 2+ user testimonials or case studies

#### Goal 4: Technical Initiatives (Customer-Enabling)
- **What:** Build Joju contributions pipeline & automation tools that enable customer success
- **Why:** Technical projects demonstrate value to customers and differentiate Joju
- **How:** 
  - Complete Figma integration (OAuth, file scanning, import to achievements)
  - Complete GitHub integration (repo scanning, contribution tracking)
  - Build Make.com/n8n agentic workflows for customer onboarding automation
  - Create data mining tools that help customers showcase their work
- **Measure:** 
  - Figma integration working (5+ beta users successfully import)
  - GitHub integration working (contribution tracking automated)
  - 1+ agentic workflow deployed (saves customer time)
  - Use technical projects in demos/sales (customer-facing value)

#### Goal 5: Strategic Customer Success Thinking
- **What:** Connect customer success work to business outcomes (retention, expansion, advocacy)
- **Why:** Ensure I'm driving revenue and growth, not just "being helpful"
- **How:** 
  - Track customer success metrics (NPS, retention, expansion revenue)
  - Identify upsell/expansion opportunities
  - Create ROI frameworks for customers
  - Align activities to business goals
- **Measure:** 
  - Customer success dashboard with key metrics
  - 2+ successful upsells or expansions
  - Customer retention rate improvement
  - Clear ROI demonstrated to leadership

**Questions for Matthew:**
1. Do these goals align with Joju's priorities for my role?
2. What goals am I missing that would be valuable?
3. How can I measure success on these goals?
4. What support do I need from you to achieve these?
5. What are YOUR goals for me in Q1 2025?

---

## 🚀 Outcomes Needed from This Meeting

### Must Have:
- ✅ **Decision:** Can we use achievements JSONB for contributions?
- ✅ **Timeline:** When will achievements component be production-ready?
- ✅ **Decision:** Run design sprint? (When, who, scope)
- ✅ **Aligned:** SMART goals for Q1 2025 (Joju contributions)
- ✅ **Aligned:** Hard skills, soft skills, personal goals for my role

### Nice to Have:
- 📋 **Plan:** Deduplication + file reduction strategy
- 📋 **Decision:** Survey timing and recruitment
- 📋 **Clarity:** Division of labor (who builds what)
- 📋 **Feedback:** Specific areas for improvement

---

## Action Items Template

**Justin:**
- [ ] 
- [ ] 
- [ ] 

**Matthew:**
- [ ] 
- [ ] 
- [ ] 

**Both:**
- [ ] 
- [ ] 

---

## Meeting Notes

### Achievements Component Status:
[Notes here]

### Design Sprint Decision:
[Notes here]

### SMART Goals Alignment:
[Notes here]

### Skills & Goals Discussion:
[Notes here]

### Parking Lot:
- Thumbnail generation (not needed for MVP)
- [Other items]

---

**Status:** Ready for Meeting  
**Created:** 2025-11-10  
**Next Review:** After meeting

**Let's make this conversation count!** 🚀
