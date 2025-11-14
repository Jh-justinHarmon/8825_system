# Competitive Analysis Tool - Quick Start

**Get started in 5 minutes!**

---

## 🚀 Quick Setup

### 1. Navigate to Project
```bash
cd /Users/justinharmon/Hammer\ Consulting\ Dropbox/Justin\ Harmon/Public/8825/windsurf-project\ -\ 8825\ version\ 2.0/Jh_sandbox/projects/competitive-analysis
```

### 2. Make Scripts Executable
```bash
chmod +x scripts/*.py
```

---

## 📋 Basic Workflow

### Step 1: Add a Competitor
```bash
python3 scripts/add_competitor.py "https://competitor.com" "Competitor Name"
```

**Example:**
```bash
python3 scripts/add_competitor.py "https://figma.com" "Figma"
```

### Step 2: List All Competitors
```bash
python3 scripts/list_competitors.py
```

### Step 3: Analyze a Competitor
```bash
python3 scripts/analyze_basic.py "competitor-id"
```

**Example:**
```bash
python3 scripts/analyze_basic.py "Figma"
```

---

## 🎯 What You Get (No API Keys Needed!)

### Basic Analysis Includes:
- ✅ **Meta Information** - Title, description, keywords
- ✅ **Technology Detection** - CMS, frameworks, analytics
- ✅ **Snapshots** - Historical tracking
- ✅ **Company Info** - Basic details

### Technologies Detected:
- **CMS:** WordPress, Shopify, Wix, Squarespace
- **Analytics:** Google Analytics, Mixpanel, Segment
- **Frameworks:** React, Vue, Angular, Next.js
- **Tools:** Stripe, Intercom, HubSpot

---

## 💡 Example Session

```bash
# Add competitors
python3 scripts/add_competitor.py "https://figma.com" "Figma"
python3 scripts/add_competitor.py "https://sketch.com" "Sketch"
python3 scripts/add_competitor.py "https://adobe.com/products/xd" "Adobe XD"

# List them
python3 scripts/list_competitors.py

# Analyze one
python3 scripts/analyze_basic.py "Figma"

# View results in data/snapshots/
```

---

## 📊 Next Steps

### Add More Competitors
Build your competitive landscape by adding all relevant players

### Run Regular Analysis
Track changes over time by re-running analysis weekly/monthly

### Compare Results
Look at snapshots to see how competitors evolve

### Upgrade to Paid APIs (Optional)
- Add traffic data (SimilarWeb)
- Add SEO data (SEMrush)
- Add backlink data (Ahrefs)

---

## 🔧 Advanced: Add API Keys

### Optional: Enhance with Paid APIs

Edit `config.json`:
```json
{
  "api_keys": {
    "builtwith_api_key": "YOUR_KEY",
    "google_api_key": "YOUR_KEY",
    "google_cx": "YOUR_SEARCH_ENGINE_ID",
    "clearbit_api_key": "YOUR_KEY"
  }
}
```

**Free Tier APIs:**
- Built.with: https://builtwith.com/api
- Google Custom Search: https://developers.google.com/custom-search
- Clearbit: https://clearbit.com

---

## 📁 File Structure

```
competitive-analysis/
├── competitors.json       # Your competitor database
├── config.json           # API keys (optional)
├── scripts/
│   ├── add_competitor.py     # Add new competitor
│   ├── list_competitors.py   # View all
│   └── analyze_basic.py      # Run analysis
└── data/
    └── snapshots/        # Historical data
```

---

## 🎯 Common Commands

```bash
# Add competitor
python3 scripts/add_competitor.py "URL" "Name"

# List all
python3 scripts/list_competitors.py

# Analyze
python3 scripts/analyze_basic.py "name-or-id"

# View snapshots
ls -la data/snapshots/
```

---

**Ready to start tracking competitors!** 🚀

**No API keys needed for basic analysis!**
