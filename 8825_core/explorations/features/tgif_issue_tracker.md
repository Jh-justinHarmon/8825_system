# TGIF Multi-Channel Issue Tracker

**Date:** 2025-11-10  
**Status:** Planning  
**Context:** Solving Patricia/Mario's issue tracking chaos during TGIF rollout

---

## 🎯 The Problem (From Meeting Transcript)

### Pain Points Identified:
> "Having trouble keeping track of issues due to multiple channels of communication (text, instant, email, on-site tech calling)"

> "Looking for a shared Google doc spreadsheet for each location to track issues and fixings, but not sure if it's possible or effective"

### Current State:
- Issues reported via: text, IM, email, phone calls, on-site
- No single source of truth
- Things get lost/forgotten
- Can't see patterns across locations
- Team considering manual spreadsheet (won't scale)

### Stakeholders:
- **Patricia** (IT) - Needs visibility, uses Microsoft email
- **Mario** (IT) - On-site, takes screenshots, uses Microsoft email
- **Store managers** - Report issues via various channels
- **On-site techs** - Call in issues

---

## 💡 The Solution: Multi-Channel Issue Aggregator

### What It Does:
Captures issues from all channels → Single dashboard → Auto-syncs to Google Sheet

### Core Value:
- Nothing falls through cracks
- Real-time visibility per location
- Pattern detection across stores
- No manual spreadsheet maintenance
- Works with existing communication habits

---

## 🏗️ Architecture

### Inputs (Multiple Channels):
```
1. Patricia's Microsoft Email
   - Issue reports from stores
   - Vendor communications
   - System alerts

2. Mario's Microsoft Email
   - On-site issue reports
   - Tech communications
   
3. Mario's Phone Screenshots
   - Visual issue documentation
   - Error messages
   - System states

4. Meeting Transcripts (Otter)
   - Issues discussed in meetings
   - Action items
   - Decisions

5. Quick Entry Form (Future)
   - On-site techs
   - Store managers
   - Quick capture
```

### Processing:
```
1. Ingestion
   - Microsoft Graph API (Patricia/Mario emails)
   - Screenshot OCR (Mario's phone)
   - Otter transcript mining
   - Email forwarding (fallback)

2. Extraction
   - Store location (phone number lookup)
   - Issue type (cash handling, POS, inventory, etc.)
   - Severity (critical, high, medium, low)
   - Reporter
   - Timestamp

3. Intelligence
   - Deduplicate (same issue, multiple reports)
   - Categorize automatically
   - Link related issues
   - Detect patterns (same issue at multiple stores)

4. Tracking
   - Status: Reported → Investigating → Fixed → Verified
   - Assignment
   - Resolution notes
   - Time to resolution
```

### Storage:
```
1. 8825 Task Tracker (JSON)
   - Primary data store
   - Full history
   - Relationships

2. Google Sheets (Sync)
   - Mario's desired format
   - Two-way sync
   - Familiar interface
   - Easy sharing
```

### Outputs:
```
1. Per-Store Dashboard
   - Stoughton's issues
   - Methuen's issues
   - etc.

2. Rollup Dashboard
   - All locations
   - By issue type
   - By severity
   - By status

3. Pattern Alerts
   - "Cash handling issue at 3 stores"
   - "Same POS error recurring"
   
4. Daily Digest
   - New issues
   - Resolved issues
   - Outstanding critical items
   
5. Google Sheet (Auto-updated)
   - Mario's requested format
   - Real-time sync
```

---

## 🔧 Technical Requirements

### Access Needed:

#### 1. Microsoft Email Integration
**Option A: Microsoft Graph API** (Preferred)
- Azure AD app registration (IT approval)
- OAuth consent from Patricia/Mario
- Permissions: `Mail.Read`, `Mail.ReadBasic`

**Option B: Email Forwarding** (Immediate)
- Create tgif-issues@gmail.com
- Patricia/Mario forward relevant emails
- Use existing Gmail ingestion

**Recommendation:** Start with B, migrate to A

#### 2. Screenshot Processing
**Mario's Phone → Cloud → 8825**

Options:
- A. Email screenshots to special address (easiest)
- B. Dropbox auto-upload (if he uses it)
- C. Google Drive integration

**Recommendation:** Email forwarding (instant, no setup)

#### 3. Google Sheets Access
- Read/write access to Mario's issue tracking sheet
- Google Sheets API integration
- Two-way sync logic

#### 4. Store Database/Mapping
**Challenge:** Match phone numbers to stores

Options:
- A. Direct database access (if IT allows)
- B. Static mapping file (phone → store)
- C. Google Sheet as directory

**Recommendation:** Start with B or C (no dependencies)

---

## 📋 Implementation Plan

### Phase 1: MVP (Week 1-2)
**Goal:** Prove value with minimal setup

**Setup:**
- [ ] Create tgif-issues@gmail.com
- [ ] Patricia/Mario forward emails to it
- [ ] Mario emails screenshots to it
- [ ] Get Google Sheet sharing access
- [ ] Create phone → store mapping file

**Build:**
- [ ] Email ingestion (use existing Gmail pipeline)
- [ ] Screenshot OCR (use existing pipeline)
- [ ] Basic issue extraction
- [ ] Store lookup logic
- [ ] Simple dashboard (JSON output)

**Test:**
- [ ] Process real emails/screenshots
- [ ] Validate store detection
- [ ] Show Patricia/Mario dashboard
- [ ] Get feedback

**Deliverable:** Working prototype with real data

---

### Phase 2: Google Sheets Integration (Week 3)
**Goal:** Auto-populate Mario's desired spreadsheet

**Build:**
- [ ] Google Sheets API setup
- [ ] Read existing sheet structure
- [ ] Two-way sync logic
- [ ] Conflict resolution

**Test:**
- [ ] Sync issues to sheet
- [ ] Manual edits in sheet → update tracker
- [ ] Verify no data loss

**Deliverable:** Auto-updating Google Sheet

---

### Phase 3: Microsoft Graph API (Week 4-5)
**Goal:** Direct email access (no forwarding)

**Setup:**
- [ ] Request Azure AD app from IT
- [ ] Get Patricia/Mario OAuth consent
- [ ] Configure API permissions

**Build:**
- [ ] Microsoft Graph authentication
- [ ] Email reading logic
- [ ] Attachment processing
- [ ] Migrate from forwarding

**Test:**
- [ ] Read emails directly
- [ ] Compare with forwarding results
- [ ] Verify no missed emails

**Deliverable:** Seamless email ingestion

---

### Phase 4: Dashboard & Intelligence (Week 6-7)
**Goal:** Rich visibility and insights

**Build:**
- [ ] Per-store dashboard
- [ ] Rollup dashboard
- [ ] Pattern detection
- [ ] Daily digest emails
- [ ] Status tracking workflow

**Test:**
- [ ] Show to full team
- [ ] Gather feedback
- [ ] Iterate on UI/UX

**Deliverable:** Production-ready dashboards

---

### Phase 5: Advanced Features (Week 8+)
**Future enhancements based on usage:**
- [ ] Quick entry web form
- [ ] Mobile app for on-site techs
- [ ] SMS integration
- [ ] Slack notifications
- [ ] Predictive analytics
- [ ] Integration health monitoring

---

## 🎯 Success Metrics

### Immediate (Week 1-2):
- [ ] 0 issues lost/forgotten
- [ ] 100% of issues captured in one place
- [ ] Patricia/Mario can see all issues instantly

### Short-term (Month 1):
- [ ] 50% reduction in "what's the status?" questions
- [ ] Pattern detection (same issue at multiple stores)
- [ ] Faster issue resolution (measurable)

### Long-term (Month 3):
- [ ] Google Sheet auto-maintained (0 manual updates)
- [ ] Predictive issue detection
- [ ] Full team adoption
- [ ] Reusable for future rollouts

---

## 💰 Value Proposition

### For Patricia/Mario:
- ✅ Visibility they're asking for
- ✅ No manual spreadsheet maintenance
- ✅ Nothing falls through cracks
- ✅ Pattern detection across stores
- ✅ Works with existing habits

### For Store Managers:
- ✅ Issues get tracked automatically
- ✅ Clear status visibility
- ✅ Faster resolution

### For Justin (You):
- ✅ Real customer success project
- ✅ Demonstrates 8825 value
- ✅ Case study for Joju
- ✅ Proves "Precipice Principle" in action
- ✅ Builds technical + customer success skills

### For HCSS/TGIF:
- ✅ Smoother rollouts
- ✅ Reduced coordination overhead
- ✅ Better issue resolution
- ✅ Institutional knowledge capture

---

## 🤔 Open Questions

### For Patricia/Mario:
1. **Email Access:** "Can we integrate with your Outlook? Or prefer email forwarding?"
2. **Screenshot Workflow:** "Mario, easiest way to get screenshots to us?"
3. **Google Sheet:** "Can we get edit access to auto-sync issues?"
4. **Store Database:** "Is there a store directory? Or should we maintain mapping?"
5. **Issue Categories:** "What types of issues do you track?"
6. **Priority:** "What's most painful right now - visibility, tracking, or something else?"

### Technical:
1. **Microsoft Graph API:** Can IT approve Azure AD app registration?
2. **Database Access:** Can we query store database for phone lookups?
3. **Real-time vs Batch:** How often should we sync? (every 5 min, hourly, etc.)
4. **Permissions:** Who needs access to dashboards?

---

## 🎨 The Pitch

> **"We can automate the issue tracking you're trying to do manually."**
>
> Instead of updating a spreadsheet, just forward emails and screenshots like you already do. We'll:
> - Capture everything automatically
> - Organize by store
> - Show patterns across locations
> - Keep your Google Sheet updated in real-time
> 
> You get the visibility you want without the manual work.
>
> **Week 1:** Email forwarding + basic tracking  
> **Week 2:** Auto-updating Google Sheet  
> **Week 3:** Full dashboard with insights
>
> No change to your workflow, just better visibility.

---

## 🚀 Next Steps

### This Week:
- [ ] Review this plan
- [ ] Validate assumptions with Patricia/Mario
- [ ] Get answers to open questions
- [ ] Decide: MVP now or wait for more info?

### Decision Point:
**Build MVP now?**
- Pro: Prove value quickly, iterate based on feedback
- Con: Might build wrong thing if assumptions are off

**OR**

**More discovery first?**
- Pro: Better understanding of pain points
- Con: Delays value delivery, risk of over-planning

---

## 📚 Related Context

### Existing 8825 Infrastructure:
- ✅ Gmail ingestion pipeline
- ✅ Screenshot OCR processing
- ✅ Task tracking system
- ✅ Meeting transcript mining (Otter)
- ✅ Email routing/classification

### Similar Projects:
- HCSS Calendar Sync (screenshot → calendar)
- TGIF Automation PoC (meetings → summaries)
- Phil's Ledger (email → bill tracking)

### Alignment with Goals:
- Customer success skills (stakeholder management)
- Technical skills (API integration, automation)
- Demonstrates AI-powered workflow
- Case study for Joju

---

## 💡 Key Insight

**This is the real opportunity** - not assumed pain points, but actual stated problem:

> "Having trouble keeping track of issues due to multiple channels"

The solution isn't complex dashboards or advanced analytics (yet). It's:
1. **Capture everything** (multiple channels → one place)
2. **Make it visible** (dashboard + Google Sheet)
3. **Show patterns** (same issue at multiple stores)

Start simple, prove value, expand based on feedback.

---

**Status:** Planning - needs validation with stakeholders  
**Next:** Discuss with Patricia/Mario, answer open questions, decide on MVP scope
