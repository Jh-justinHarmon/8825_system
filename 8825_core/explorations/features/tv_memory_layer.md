# Project 8825 TV Memory Layer

**Date:** 2025-11-08  
**Source:** ChatGPT Mobile  
**Status:** Concept / Spec Complete

---

## Executive Summary

**Concept:** Apply 8825's persistent memory/JSON infrastructure to TV/streaming to solve "where did we watch that show?" problem

**Core Insight:** Not replacing streaming apps or aggregators, but creating a memory layer that helps users remember which platform has their shows

**Technical Approach:** Bookmark/journal model vs full tracking - capture just platform + show, let apps handle episode details

**Viability:** Technically feasible using Siri Shortcuts, share sheets, and browser extensions - no API partnerships needed

---

## Problem Definition

### User Pain
Can't remember which streaming platform has which show

### Current Solutions
- **Apple TV App:** Incomplete coverage, pushes own content
- **JustWatch/Reelgood:** Search engines with affiliate links, no personal history
- **Trakt:** Third-party tracking service, requires manual setup

### Market Validation
Universal problem experienced by multi-platform streaming users

### Value Proposition
Personal viewing memory that works across all platforms and devices

---

## Technical Analysis

### Data Access Barriers

**APIs:**
- Status: Not available
- Reason: Netflix, Disney+, etc. don't expose watch history APIs
- Workarounds: Trakt bridge, browser extensions, manual logging

**Hardware Approaches:**
- HDMI passthrough: Feasible but high friction ($50-100 per unit)
- USB port: Not feasible (TV USB ports are power-only)

**Platform Restrictions:**
- Apple TV sandboxing: Apps cannot see other apps' activity
- Background access: Not permitted
- Remote button hijacking: Not possible

### Viable Solutions

#### 1. Siri Shortcuts (HIGH PRIORITY)
**Implementation:** App Intents framework  
**Capabilities:**
- Global voice commands
- Read/write to memory
- Works from any app

**Example Commands:**
- "Hey Siri, tell 8825 I'm watching The Bear on Hulu"
- "Hey Siri, where do I watch Succession?"
- "Hey Siri, ask 8825 what to watch tonight"

**Effort:** 2-3 days

#### 2. Mobile Share Sheets (HIGH PRIORITY)
**Implementation:** iOS/Android share extensions  
**Capabilities:** Capture title + platform from any streaming app  
**User Flow:** Watch → Share → Save to 8825  
**Effort:** 1-2 days

#### 3. Browser Extension (MEDIUM PRIORITY)
**Implementation:** Chrome/Safari/Firefox extension  
**Capabilities:** Auto-detect streaming on desktop  
**Automatic:** Yes  
**Effort:** 1 day

#### 4. Manual Bookmarking (HIGH PRIORITY)
**Implementation:** Simple UI with platform grid  
**Capabilities:** Quick manual entry with voice  
**Friction:** Low - tap and speak  
**Effort:** 1 day

---

## Data Model Integration

### Uses 8825 Core: YES

### Memory Structure
```json
{
  "memory_id": "mem_[uuid]",
  "type": "media_bookmark",
  "subject": "[show_name]",
  "timestamp": "[ISO8601]",
  "content": {
    "platform": "[Netflix|Hulu|Max|etc]",
    "title": "[show_name]",
    "context": {
      "viewers": ["array_of_names"],
      "location": "[living_room|bedroom|etc]",
      "device": "[TV|iPhone|laptop]",
      "mood": "[date_night|background|focused]"
    }
  },
  "intelligence": {
    "detected_genre": "[drama|comedy|etc]",
    "similar_watched": ["array_of_shows"],
    "platform_confidence": 0.0,
    "refs_used": ["previous_memory_ids"]
  }
}
```

### Integration Benefits
- Same SQLite/cloud sync infrastructure
- Same FTS5 search
- Same intelligence layer
- Cross-domain context (work + entertainment)
- Unified memory search

---

## Implementation Roadmap

### MVP Scope (1 week)

**Features:**
- Siri shortcuts for log/find/recommend
- Simple platform + show storage
- Basic tvOS UI with platform grid
- SQLite storage with 8825 schema

**Deliverables:**
- Siri Intents: LogShowIntent, FindShowIntent, WhatToWatchIntent
- UI: Platform grid launcher
- Storage: 8825-compatible JSON memories

### Phase 2: Enhancements (Week 2-3)
- Mobile share extension
- Browser extension for desktop
- ChatGPT recommendations
- Household sharing
- CloudKit sync

### Phase 3: Intelligence (Month 2)
- Pattern recognition
- Viewing habit analysis
- Predictive suggestions
- Cross-platform continue watching

---

## Key Decisions

### 1. Bookmark vs Tracking
**Decision:** Bookmark model  
**Rationale:** Platforms already track episodes, we just need to remember where shows live  
**Impact:** Dramatically simplifies technical requirements

### 2. Siri-First Approach
**Decision:** Lead with Siri integration  
**Rationale:** Works globally, Apple-blessed, solves friction  
**Impact:** Natural interaction model from day 1

### 3. Reuse 8825 Infrastructure
**Decision:** Use exact same memory model  
**Rationale:** Proves 8825 works for any domain, not just work  
**Impact:** 2-day addition instead of new product

---

## Competitive Analysis

### vs Apple TV App
**Advantages:**
- Platform neutral
- Complete coverage
- User-controlled data
- Voice-first interface

**Disadvantages:**
- Not built-in
- Requires user action

### vs JustWatch
**Advantages:**
- Personal history
- Household context
- Voice control
- Integrated with broader memory

**Disadvantages:**
- Less comprehensive catalog data

**Unique Value:** Only solution that treats viewing as personal memory, not just data

---

## Risk Assessment

| Risk | Mitigation | Severity |
|------|-----------|----------|
| User adoption friction | Siri integration makes logging effortless | MEDIUM |
| Platform API changes | Multiple capture methods (share, browser, manual) | LOW |
| Incomplete data | Bookmark model doesn't need episode-level precision | LOW |

---

## Success Metrics

### Week 1
- Siri shortcuts working
- 10 test users successfully logging
- Find queries returning correct platform

### Month 1
- 100 active users
- Average 5 shows logged per user
- 80% successful platform recalls
- ChatGPT recommendations rated helpful

---

## Strategic Value

### For 8825
- Proves memory layer works across domains
- Gateway drug for broader 8825 adoption
- Demonstrates practical value immediately
- Non-threatening entry point

### Market Opportunity
Could become default TV memory for households

### Acquisition Potential
Attractive to Apple/Roku/streaming platforms

---

## Next Actions

| ID | Task | Effort | Priority |
|----|------|--------|----------|
| TV-001 | Build Siri Shortcuts proof of concept | 8 hours | HIGH |
| TV-002 | Create platform grid UI for tvOS | 4 hours | HIGH |
| TV-003 | Test with 5 households | 2 hours | HIGH |
| TV-004 | Add ChatGPT recommendations | 4 hours | MEDIUM |

---

## Conclusion

**Viability:** HIGH  
**Alignment with 8825:** PERFECT  
**Effort Required:** 2-3 days for MVP  
**Recommendation:** Build as proof of concept for 8825's broader applicability  
**Key Insight:** Solving "where to watch" via memory + Siri is achievable today without any API partnerships

---

**Status:** Ready for prototyping  
**Next Step:** TV-001 - Build Siri Shortcuts POC
