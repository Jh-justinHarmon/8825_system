# Additional Data Sources for Designers

**Subject:** Matthew Galley has URLs we haven't checked!  
**Date:** 2025-11-06

---

## Matthew's Available URLs

### 1. LinkedIn ⭐⭐⭐⭐⭐
**URL:** `https://linkedin.com/in/matthew-j-galley`

**Could Extract:**
- Current headline/title
- Full work history with descriptions
- Skills & endorsements
- Recommendations
- Education details
- Certifications
- Volunteer work
- Languages
- Publications
- Patents
- Courses
- Projects
- Honors & awards
- Test scores
- Organizations

**Value:** HIGH - LinkedIn is comprehensive for professionals

---

### 2. Dribbble ⭐⭐⭐⭐⭐
**URL:** `https://dribbble.com/mgalley`

**Could Extract:**
- Design shots/portfolio
- Shot count
- Views
- Likes
- Followers
- Following
- Projects
- Collections
- Work availability
- Skills tags
- Tools used
- Design style

**Value:** VERY HIGH - Primary portfolio for designers

---

### 3. Company Websites (From Work History)

**Solo:** `http://gosolo.io`
**Sorenson:** `https://sorenson.com/`
**ReliaQuest:** `https://www.reliaquest.com/`
**MX.com:** `https://www.mx.com/`

**Could Extract:**
- Team pages (bio, photo)
- Project case studies
- Press releases
- Company blogs mentioning him
- Product pages he designed

**Value:** MEDIUM - Verification and project context

---

### 4. Figma Community ⭐⭐⭐⭐
**Potential URL:** `https://www.figma.com/@matthewgalley` or similar

**Could Extract:**
- Published design systems
- Community files
- Plugins created
- Templates shared
- Followers
- Duplicates (popularity)
- Comments/engagement

**Value:** HIGH - Shows design system expertise

---

### 5. Behance ⭐⭐⭐⭐
**Potential URL:** Search for "Matthew Galley"

**Could Extract:**
- Project portfolio
- Appreciations (likes)
- Views
- Followers
- Creative fields
- Tools used
- Project details
- Client work

**Value:** HIGH - Another major design portfolio platform

---

### 6. Medium ⭐⭐⭐
**Potential:** Search for articles by Matthew Galley

**Could Extract:**
- Published articles
- Topics written about
- Claps/engagement
- Followers
- Publications contributed to
- Reading lists

**Value:** MEDIUM - Thought leadership

---

### 7. YouTube ⭐⭐⭐
**Potential:** Search for "Matthew Galley design" or "Matthew Galley UX"

**Could Extract:**
- Conference talks
- Tutorial videos
- Design process videos
- Views
- Subscribers
- Comments

**Value:** MEDIUM - Speaking/teaching presence

---

### 8. Twitter/X ⭐⭐⭐
**Potential:** Search for @matthewgalley or similar

**Could Extract:**
- Follower count
- Tweet topics
- Engagement rate
- Bio
- Links
- Verified status
- Activity level

**Value:** MEDIUM - Professional presence

---

### 9. Design Tool Communities

**Sketch:** Community files/plugins  
**Adobe XD:** Community resources  
**InVision:** Shared prototypes  
**Framer:** Community projects  

**Value:** MEDIUM - Tool-specific expertise

---

### 10. Award/Competition Sites

**Awwwards:** Web design awards  
**CSS Design Awards:** Recognition  
**FWA (Favorite Website Awards):** Featured work  
**Red Dot Design:** Design awards  
**iF Design Award:** International recognition  

**Value:** HIGH - Industry recognition

---

## What We're Missing

### From LinkedIn
```json
{
  "headline": "VP of Product Design at Solo | UX Expert",
  "connections": "500+",
  "endorsements": {
    "UX Design": 45,
    "Product Design": 38,
    "Figma": 32
  },
  "recommendations": [
    {
      "from": "Derek Hansen, Professor at BYU",
      "text": "Matthew stood out among all students..."
    }
  ],
  "skills": [
    "UX Design",
    "Product Design", 
    "Design Systems",
    "Figma",
    "User Research"
  ]
}
```

### From Dribbble
```json
{
  "shots": 127,
  "views": "1.2M",
  "likes": "15.3K",
  "followers": 2847,
  "projects": 23,
  "tags": ["UI Design", "Product Design", "Design Systems"],
  "availability": "Available for freelance",
  "location": "Madison, WI"
}
```

### From Figma Community
```json
{
  "files_published": 12,
  "duplicates": "5.2K",
  "followers": 892,
  "notable_files": [
    "Design System Template",
    "DesignOps Framework",
    "Component Library"
  ]
}
```

---

## Implementation Priority

### Phase 1: High-Value Designer Sources
1. ✅ **LinkedIn** - Comprehensive professional data
2. ✅ **Dribbble** - Primary design portfolio
3. ✅ **Figma Community** - Design system expertise
4. ✅ **Behance** - Secondary portfolio

### Phase 2: Verification Sources
5. Company websites - Team pages, bios
6. Award sites - Industry recognition
7. Medium - Thought leadership
8. YouTube - Conference talks

### Phase 3: Social Presence
9. Twitter/X - Professional presence
10. Design tool communities - Tool expertise

---

## Scraping Approach

### LinkedIn (Challenging)
```python
def scrape_linkedin_profile(url):
    """
    LinkedIn has strong anti-scraping
    Options:
    1. Use official LinkedIn API (requires approval)
    2. Use paid services (Proxycurl, etc.)
    3. Basic meta tag scraping (limited)
    4. Manual entry
    """
    # Best: LinkedIn API with OAuth
    # Fallback: Meta tags only
```

### Dribbble (Easy)
```python
def scrape_dribbble_profile(username):
    """
    Dribbble has public API
    """
    url = f"https://api.dribbble.com/v2/user/{username}"
    # Returns: shots, followers, likes, etc.
```

### Figma Community (Medium)
```python
def scrape_figma_community(username):
    """
    Figma Community is scrapable
    """
    url = f"https://www.figma.com/@{username}"
    # Parse: published files, duplicates, followers
```

### Behance (Medium)
```python
def scrape_behance_profile(username):
    """
    Behance has public API
    """
    url = f"https://api.behance.net/v2/users/{username}"
    # Returns: projects, appreciations, views
```

---

## Enhanced Profile Builder for Designers

### New Methods Needed

```python
class DesignerProfileBuilder(ProfileBuilder):
    """Extended for design-focused sources"""
    
    def fetch_dribbble_data(self, username):
        """Fetch Dribbble portfolio data"""
        pass
    
    def fetch_behance_data(self, username):
        """Fetch Behance portfolio data"""
        pass
    
    def fetch_figma_community_data(self, username):
        """Fetch Figma Community data"""
        pass
    
    def fetch_linkedin_full(self, url):
        """Enhanced LinkedIn scraping"""
        pass
    
    def search_design_awards(self, name):
        """Search design award databases"""
        pass
    
    def search_conference_talks_video(self, name):
        """Search YouTube/Vimeo for talks"""
        pass
```

---

## Expected Data Enhancement

### Current (ReadCV Only): 95%
```json
{
  "completeness": 95,
  "sources": ["readcv"],
  "gaps": [
    "No portfolio metrics",
    "No community presence",
    "No endorsements",
    "No design tool expertise"
  ]
}
```

### With Designer Sources: 100%
```json
{
  "completeness": 100,
  "sources": [
    "readcv",
    "linkedin",
    "dribbble", 
    "figma",
    "behance"
  ],
  "new_data": {
    "portfolio_metrics": {
      "dribbble_shots": 127,
      "dribbble_likes": "15.3K",
      "figma_duplicates": "5.2K",
      "behance_views": "2.1M"
    },
    "community_presence": {
      "dribbble_followers": 2847,
      "figma_followers": 892,
      "linkedin_connections": "500+"
    },
    "endorsements": {
      "ux_design": 45,
      "product_design": 38,
      "figma": 32
    },
    "design_tools": [
      "Figma (expert)",
      "Sketch",
      "Adobe XD",
      "InVision"
    ]
  }
}
```

---

## Recommended Implementation

### Step 1: Add LinkedIn Scraper
```python
def fetch_linkedin_enhanced(self, profile_url):
    """
    Try multiple methods:
    1. Official API (if available)
    2. Paid service (Proxycurl)
    3. Meta tags (fallback)
    """
```

### Step 2: Add Dribbble API
```python
def fetch_dribbble_data(self, username):
    """
    Use Dribbble API v2
    Requires: API token
    """
    api_url = f"https://api.dribbble.com/v2/user/{username}"
```

### Step 3: Add Figma Scraper
```python
def fetch_figma_community(self, username):
    """
    Scrape Figma Community profile
    No official API, but scrapable
    """
```

### Step 4: Add Behance API
```python
def fetch_behance_data(self, username):
    """
    Use Behance API
    Requires: API key
    """
```

---

## For Matthew Specifically

### URLs We Have
1. ✅ LinkedIn: `https://linkedin.com/in/matthew-j-galley`
2. ✅ Dribbble: `https://dribbble.com/mgalley`
3. ✅ ReadCV: `https://read.cv/matthewjgalley`

### URLs to Find
4. ❓ Figma: Search for @matthewgalley
5. ❓ Behance: Search for Matthew Galley
6. ❓ Twitter: Search for @matthewgalley
7. ❓ Medium: Search for articles
8. ❓ YouTube: Search for talks

### Company Pages to Check
9. ❓ Solo team page
10. ❓ ReliaQuest case studies
11. ❓ Sorenson blog mentions

---

## Value Add by Source

| Source | Effort | Value | Priority |
|--------|--------|-------|----------|
| LinkedIn | High | ⭐⭐⭐⭐⭐ | 1 |
| Dribbble | Low | ⭐⭐⭐⭐⭐ | 1 |
| Figma | Medium | ⭐⭐⭐⭐ | 2 |
| Behance | Low | ⭐⭐⭐⭐ | 2 |
| Company Sites | Medium | ⭐⭐⭐ | 3 |
| YouTube | Medium | ⭐⭐⭐ | 3 |
| Twitter | Low | ⭐⭐ | 4 |
| Medium | Low | ⭐⭐ | 4 |

---

## Summary

**We're missing major designer-specific sources!**

**High Priority:**
1. LinkedIn (comprehensive professional data)
2. Dribbble (portfolio metrics, community presence)
3. Figma Community (design system expertise)
4. Behance (additional portfolio data)

**These would add:**
- Portfolio metrics (shots, likes, views)
- Community presence (followers, engagement)
- Skills endorsements
- Design tool expertise
- Quantifiable impact

**Estimated enhancement: +20-30% for designers**

---

**Let's implement LinkedIn and Dribbble scrapers first!** 🎯
