# Future Enhancements - User Engagement Dashboard

## 🎯 Priority: High

### **Multi-Batch Filtering**

**Need:** As additional feedback comes in from different sources and time periods, team needs ability to filter which feedback group they're reviewing.

**Current State:**
- Dashboard shows all 91 quotes from 5 user testing sessions (Aug 28-29, 2025)
- No way to separate or filter different feedback batches

**Required Filters:**

1. **By Feedback Source**
   - User Testing Sessions
   - Notion Screener Surveys
   - Beta Tester Feedback
   - Support Tickets
   - NPS/CSAT Responses

2. **By Time Period**
   - This Week
   - Last Week
   - Last Month
   - Custom Date Range
   - By Sprint/Phase

3. **By Participant/Group**
   - Individual participants
   - Cohort (e.g., "Design Sprint Aug 2025")
   - User segment (e.g., "Power Users", "First-time Users")

4. **By Theme/Category**
   - Already have: Workflow, Customization, AI, etc.
   - Need ability to show/hide specific themes

5. **By Status**
   - New (unreviewed)
   - Reviewed
   - Actioned
   - Archived

**Proposed UI:**

```
┌─────────────────────────────────────────────┐
│  [Logo]                                     │
│  user engagement intelligence               │
├─────────────────────────────────────────────┤
│  Filters:                                   │
│  [All Sources ▼] [All Time ▼] [All Users ▼]│
│  [x] Workflow  [x] Customization  [x] AI   │
├─────────────────────────────────────────────┤
│  Stats (filtered)                           │
│  5 sessions | 91 quotes | 7 themes          │
└─────────────────────────────────────────────┘
```

**Implementation Notes:**

1. **Data Structure Update:**
   ```json
   {
     "quote": "...",
     "participant": "chris",
     "date": "2025-08-28",
     "source": "user_testing",
     "batch": "design_sprint_aug_2025",
     "status": "new",
     "theme": "workflow"
   }
   ```

2. **Filter State:**
   - Store in URL params for shareability
   - Save to localStorage for persistence
   - Example: `?source=user_testing&batch=aug_2025&theme=workflow`

3. **Dynamic Stats:**
   - Update stats based on active filters
   - Show "X of Y quotes" when filtered
   - Highlight active filters

**Priority Tasks:**

- [ ] Add metadata to all quotes (source, batch, status)
- [ ] Build filter UI components
- [ ] Implement filter logic
- [ ] Update stats to reflect filters
- [ ] Add URL param support
- [ ] Test with multiple feedback batches

---

## 🎨 Other Enhancements

### **Medium Priority:**

1. **Export Functionality**
   - Export filtered quotes to CSV
   - Generate PDF report
   - Copy to clipboard

2. **Search Enhancement**
   - Full-text search across all quotes
   - Search by participant
   - Search by date range

3. **Sorting Options**
   - Sort by date (newest/oldest)
   - Sort by mention count
   - Sort by participant

4. **Visualization**
   - Bar chart of themes by frequency
   - Timeline of feedback over time
   - Participant contribution breakdown

### **Low Priority:**

1. **Annotations**
   - Add notes to quotes
   - Tag quotes with custom labels
   - Link quotes to action items

2. **Collaboration**
   - Mark quotes as reviewed
   - Assign quotes to team members
   - Add comments/discussions

3. **Integration**
   - Auto-import from Notion
   - Sync with project management tools
   - Webhook for new feedback

---

## 📋 Implementation Plan

### **Phase 1: Multi-Batch Filtering (Week 1)**
- Add batch metadata to data structure
- Build filter dropdowns
- Implement filter logic
- Test with current data

### **Phase 2: Enhanced Filtering (Week 2)**
- Add source and status filters
- Implement URL params
- Add "clear filters" button
- Update documentation

### **Phase 3: Export & Search (Week 3)**
- Add export to CSV
- Enhance search functionality
- Add sorting options

### **Phase 4: Visualization (Week 4)**
- Add simple charts
- Timeline view
- Participant breakdown

---

**Created:** November 10, 2025
**Status:** 📝 Planning
**Owner:** Product Team
**Next Review:** After next feedback batch arrives
