# ✅ read.CV Format - CORRECTED

**Issue Identified:** The JSON structure was flat instead of using read.CV's nested sections format.

---

## 🔴 What Was Wrong

### **Incorrect Structure (Before):**
```json
{
  "general": { ... },
  "skills": [ ... ],           ← WRONG: Flat array
  "projects": [ ... ],         ← WRONG: Flat array
  "workExperience": [ ... ],   ← WRONG: Flat array
  "education": [ ... ],        ← WRONG: Flat array
  "certifications": [ ... ]    ← WRONG: Flat array
}
```

**Problems:**
- Skills section doesn't exist in read.CV format
- All content sections were flat arrays
- Missing `sections` wrapper
- Missing `name` and `items` structure

---

## ✅ Correct Structure (After)

### **Proper read.CV Format:**
```json
{
  "general": {
    "profilePhoto": "/content/media/profilePhoto.jpg",
    "username": "justinharmon",
    "displayName": "Justin Harmon",
    "profession": "Product Developer / UX Leader / Entrepreneur",
    "location": "Dallas, Texas",
    "pronouns": "He/Him",
    "byline": "...",
    "website": "prtclinc.com",
    "websiteURL": "https://prtclinc.com",
    "about": "...",
    "status": {
      "text": "...",
      "emoji": "🚀",
      "timestamp": "2025-11-07"
    },
    "sectionOrder": [
      "Projects",
      "Work Experience",
      "Education",
      "Certifications",
      "Contact"
    ]
  },
  "sections": [                    ← REQUIRED: Wrapper array
    {
      "name": "Projects",          ← REQUIRED: Section name
      "items": [                   ← REQUIRED: Items array
        {
          "id": "...",
          "year": "2024 — Now",    ← Format: "YYYY — Now" or "YYYY — YYYY"
          "heading": "Title at Company",  ← Format: "Title at Company"
          "url": null,
          "collaborators": [],
          "description": "...",
          "attachments": [...],
          "type": "project",
          "title": "Title",
          "company": "Company"
        }
      ]
    },
    {
      "name": "Work Experience",
      "items": [...]
    },
    {
      "name": "Education",
      "items": [...]
    },
    {
      "name": "Certifications",
      "items": [...]
    },
    {
      "name": "Contact",
      "items": [...]
    }
  ]
}
```

---

## 🔧 Key Fixes Applied

### **1. Structure**
- ✅ Added `sections` array wrapper
- ✅ Each section has `name` and `items`
- ✅ Removed flat arrays

### **2. Year Format**
- ✅ Changed: `"year": "2025"` → `"year": "2024 — Now"`
- ✅ Changed: `"year": "2005-2012"` → `"year": "2005 — 2012"`
- ✅ Single year: `"year": "2009"` (unchanged)

### **3. Heading Format**
- ✅ Changed: `"heading": "Title"` → `"heading": "Title at Company"`
- ✅ Example: `"Trustybits - Hiring Manager Intelligence Tool at Innovation Project"`

### **4. Education Fields**
- ✅ Changed: `"institution"` → `"school"`
- ✅ Changed: `"field"` → `"location"` (used for field/specialization)
- ✅ Kept: `"degree"` (correct)

### **5. Certification Fields**
- ✅ Changed: `"institution"` → `"organization"`
- ✅ Changed: `"title"` → `"name"`
- ✅ Kept: `"heading"` format as "Name from Organization"

### **6. Contact Format**
- ✅ Changed from object to items array
- ✅ Each contact has: `platform`, `handle`, `url`
- ✅ Removed nested `social` object

### **7. Skills Section**
- ✅ **REMOVED** - Not part of read.CV format
- Skills are implied through projects and work experience

---

## 📋 Section-by-Section Comparison

### **Projects**
```json
// BEFORE (Wrong)
"projects": [
  {
    "year": "2025",
    "heading": "Trustybits - Hiring Manager Intelligence Tool",
    "company": "Innovation Project"
  }
]

// AFTER (Correct)
"sections": [
  {
    "name": "Projects",
    "items": [
      {
        "year": "2024 — Now",
        "heading": "Trustybits - Hiring Manager Intelligence Tool at Innovation Project",
        "company": "Innovation Project"
      }
    ]
  }
]
```

### **Education**
```json
// BEFORE (Wrong)
"education": [
  {
    "institution": "California College of the Arts",
    "field": "Industrial Design"
  }
]

// AFTER (Correct)
"sections": [
  {
    "name": "Education",
    "items": [
      {
        "school": "California College of the Arts",
        "location": "Industrial Design"
      }
    ]
  }
]
```

### **Certifications**
```json
// BEFORE (Wrong)
"certifications": [
  {
    "institution": "Nielsen Norman Group",
    "title": "UX Certification"
  }
]

// AFTER (Correct)
"sections": [
  {
    "name": "Certifications",
    "items": [
      {
        "organization": "Nielsen Norman Group",
        "name": "UX Certification with specialty in UX Management"
      }
    ]
  }
]
```

### **Contact**
```json
// BEFORE (Wrong)
"contact": {
  "email": "harmon.justin@gmail.com",
  "social": {
    "linkedin": "https://..."
  }
}

// AFTER (Correct)
"sections": [
  {
    "name": "Contact",
    "items": [
      {
        "platform": "LinkedIn",
        "handle": "justin-harmon-a21337a9",
        "url": "https://www.linkedin.com/in/justin-harmon-a21337a9/"
      },
      {
        "platform": "Email",
        "handle": "harmon.justin@gmail.com",
        "url": "mailto:harmon.justin@gmail.com"
      }
    ]
  }
]
```

---

## ✅ What's Now Correct

### **General Section:**
- ✅ Profile photo reference
- ✅ Username, display name, profession
- ✅ Location, pronouns, byline
- ✅ Website and URL
- ✅ About text
- ✅ Status (text, emoji, timestamp)
- ✅ Section order array

### **Projects Section:**
- ✅ 10 projects with proper structure
- ✅ 7 projects with image attachments
- ✅ Year format: "YYYY — Now" or "YYYY — YYYY"
- ✅ Heading format: "Title at Company"
- ✅ All required fields present

### **Work Experience Section:**
- ✅ 5 positions
- ✅ Proper year ranges
- ✅ Heading format correct
- ✅ Location field included

### **Education Section:**
- ✅ 2 schools
- ✅ Uses `school` not `institution`
- ✅ Uses `location` for field/specialization
- ✅ Degree field correct

### **Certifications Section:**
- ✅ 1 certification
- ✅ Uses `organization` not `institution`
- ✅ Uses `name` not `title`
- ✅ Heading format: "Name from Organization"

### **Contact Section:**
- ✅ Items array format
- ✅ Platform, handle, url fields
- ✅ LinkedIn and Email included

---

## 🎯 File Status

**Corrected File:**
```
joju_sandbox/output/joju_upload_ready_with_images.json
```

**Old File (backup):**
```
joju_sandbox/output/joju_upload_ready_with_images_OLD.json
```

---

## 📊 Validation Checklist

- [x] Uses `sections` array wrapper
- [x] Each section has `name` and `items`
- [x] Year format uses em dash (—) not hyphen (-)
- [x] Heading includes "at Company"
- [x] Education uses `school` and `location`
- [x] Certifications use `organization` and `name`
- [x] Contact is items array with platform/handle/url
- [x] No skills section (not in read.CV format)
- [x] All images properly referenced
- [x] Profile photo included

---

## 🚀 Ready for Upload

The JSON now matches the exact read.CV format structure as seen in Matthew Galley's reference file.

**Status:** ✅ Format corrected and validated
