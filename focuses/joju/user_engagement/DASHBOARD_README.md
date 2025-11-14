# User Engagement Dashboard

Interactive HTML dashboard for viewing and analyzing user engagement data.

---

## 🎯 Features

### **High-Level Analytics**
- Total sessions conducted
- Pain points identified
- Positive feedback count
- AI features noted
- Real-time stats

### **Filtering**
- All feedback
- User testing sessions
- Survey responses
- Competitive intelligence
- Pain points only
- Positive feedback only
- AI features only

### **Search**
- Full-text search across all feedback
- Search quotes, insights, and tags
- Real-time filtering

### **Notable Quotes**
- Direct user quotes
- Categorized by type
- Tagged for easy filtering
- Participant attribution
- Date stamping

### **Competitive Intelligence**
- Platforms users mentioned
- AI features they valued
- Why features worked
- Visual feature cards

### **Key Insights**
- Extracted patterns
- Recurring themes
- Actionable insights
- Team learnings

---

## 🚀 Quick Start

### **Open Dashboard:**
```bash
open dashboard.html
```

Or double-click `dashboard.html` in Finder.

### **Update Data:**
```bash
python3 generate_dashboard_data.py
```

Then refresh the browser.

---

## 📊 Dashboard Sections

### **1. Stats Cards (Top)**
- Total Sessions
- Pain Points
- Positive Feedback
- AI Features Noted

### **2. Filters**
- Quick filter buttons
- Active state highlighting
- Instant filtering

### **3. Search Bar**
- Full-text search
- Real-time results
- Searches quotes and tags

### **4. Feedback & Quotes (Left)**
- Notable user quotes
- Participant names
- Session dates
- Category tags
- Hover effects

### **5. Insights (Right)**
- Key learnings
- Competitive intel cards
- Recurring themes
- Visual highlights

---

## 🎨 Design Features

### **Visual Design:**
- Modern gradient background
- Card-based layout
- Smooth animations
- Hover effects
- Responsive design

### **Color Coding:**
- 🔴 Pain Points (red)
- 🟢 Positive (green)
- 🟣 AI Features (purple)
- ⚪ General (gray)

### **Interactive Elements:**
- Clickable filters
- Search box
- Hover states
- Card animations

---

## 🔄 Updating Dashboard

### **Automatic Updates:**
The dashboard reads from `dashboard_data.json`. To update:

1. **Add new session data** to `sessions/`
2. **Run data generator:**
   ```bash
   python3 generate_dashboard_data.py
   ```
3. **Refresh browser** to see updates

### **Manual Updates:**
Edit `dashboard.html` directly to:
- Add new feedback items
- Update stats
- Add new filters
- Customize styling

---

## 📁 Files

```
user_engagement/
├── dashboard.html              # Main dashboard file
├── generate_dashboard_data.py  # Data generator script
├── dashboard_data.json         # Generated data (auto-created)
└── DASHBOARD_README.md         # This file
```

---

## 🎯 Use Cases

### **Team Reviews:**
- Weekly feedback review meetings
- Sprint planning sessions
- Feature prioritization
- Competitive analysis

### **Stakeholder Updates:**
- Show user sentiment
- Demonstrate insights
- Highlight patterns
- Justify decisions

### **Product Planning:**
- Validate feature ideas
- Identify pain points
- Learn from competitors
- Understand user needs

### **Research Analysis:**
- Review user testing results
- Analyze survey data
- Track themes over time
- Export insights

---

## 🔧 Customization

### **Add New Feedback:**
Edit `dashboard.html`, find the feedback section, and add:

```html
<div class="feedback-item" data-category="positive">
    <div class="feedback-header">
        <span class="participant-name">User Name</span>
        <span class="date">Date</span>
    </div>
    <div class="quote">
        "User quote here..."
    </div>
    <div class="tags">
        <span class="tag positive">Positive</span>
        <span class="tag">Custom Tag</span>
    </div>
</div>
```

### **Add New Filters:**
Add button in filters section:

```html
<button class="filter-btn" data-filter="new-category">New Category</button>
```

### **Change Colors:**
Edit the `<style>` section in `dashboard.html`:

```css
.stat-card {
    background: your-color;
}
```

---

## 📱 Mobile Responsive

Dashboard automatically adapts to:
- Desktop (1400px+)
- Tablet (768px-1400px)
- Mobile (<768px)

---

## 🚀 Future Enhancements

### **Planned Features:**
- [ ] Export to PDF
- [ ] Data visualization charts
- [ ] Time-based filtering
- [ ] Sentiment analysis
- [ ] Tag cloud
- [ ] Comparison views
- [ ] API integration
- [ ] Real-time updates

### **Advanced Analytics:**
- [ ] Trend analysis
- [ ] Cohort analysis
- [ ] Feature correlation
- [ ] User segmentation

---

## 📊 Data Sources

Dashboard pulls from:
- `sessions/` - User testing transcripts
- `surveys/` - Survey responses
- `insights/` - Extracted insights
- `competitive_intelligence/` - Platform analyses

---

## 🎓 Best Practices

### **Regular Updates:**
- Update after each user session
- Run generator weekly
- Review with team monthly

### **Data Quality:**
- Include direct quotes
- Tag appropriately
- Date everything
- Attribute to participants

### **Team Usage:**
- Share link with team
- Review in meetings
- Export key insights
- Track action items

---

## 🔗 Integration

### **With Other Tools:**
- Export quotes to Notion
- Share insights in Slack
- Include in presentations
- Link to roadmap items

### **With 8825 System:**
- Automatically processes new sessions
- Integrates with inbox pipeline
- Routes to joju focus
- Generates insights

---

**Created:** November 10, 2025
**Status:** ✅ Production Ready
**Location:** `focuses/joju/user_engagement/dashboard.html`
**Team Access:** Open in any browser
