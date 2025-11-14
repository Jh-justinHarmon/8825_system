# 8825 Learning Repository

**Purpose:** Systematic capture of lessons learned, failures, patterns, and adaptations  
**Protocol:** Observe → Adapt → Log → Update  
**Status:** Active

---

## Overview

This repository implements the Learning Protocol by documenting:
- **Successes:** What worked and why
- **Failures:** What didn't work and why
- **Adaptations:** How we pivoted
- **Patterns:** Reusable solutions
- **Preventions:** How to avoid known pitfalls

---

## Structure

```
learning/
├── README.md (this file)
├── lessons/
│   ├── 2024-11-09_dropbox_api_failure.md
│   ├── [date]_[topic].md
│   └── ...
├── patterns/
│   ├── local_first_when_api_fails.md
│   ├── [pattern_name].md
│   └── ...
├── retrospectives/
│   ├── 2024-Q4_retrospective.md
│   └── [quarter]_retrospective.md
└── failure_modes/
    ├── api_restrictions.md
    └── [failure_category].md
```

---

## Lesson Template

Use this template for every lesson learned:

```markdown
# [Lesson Title]

**Date:** YYYY-MM-DD  
**Project:** [Phil's Ledger / Joju / Core]  
**Type:** Success / Failure / Adaptation / Pattern  
**Tags:** [tag1, tag2, tag3]

---

## Context
What was the situation?

## What Happened
What did we try/do?

## Outcome
What was the result?

## Why It Worked/Failed
Root cause analysis

## Lessons Learned
1. Key insight 1
2. Key insight 2
3. Key insight 3

## Reusable Pattern?
- [ ] Yes - Created pattern: [link]
- [ ] No - Situation-specific

## Prevention/Application
How to apply this learning going forward?

## Related
- Link to code
- Link to brainstorm
- Link to related lessons
```

---

## Current Lessons

| Date | Lesson | Type | Status |
|------|--------|------|--------|
| 2024-11-09 | [Dropbox API Failure → Local Files](./lessons/2024-11-09_dropbox_api_failure.md) | Adaptation | ✅ Documented |
| TBD | XMP Parsing Success | Success | 📋 To Document |
| TBD | Phil's Ledger POC Speed | Success | 📋 To Document |

---

## Pattern Library

| Pattern | Use Case | Maturity |
|---------|----------|----------|
| [Local-First When API Fails](./patterns/local_first_when_api_fails.md) | API restrictions | ✅ Validated |
| Two-Stage Mining | Content extraction | ⚠️ Partial |
| Piggyback Opportunities | Resource optimization | 🆕 New |

---

## Failure Modes

| Failure Mode | Impact | Prevention |
|--------------|--------|------------|
| [API Access Restrictions](./failure_modes/api_restrictions.md) | HIGH | Check permissions early |
| Scope Creep | MEDIUM | SMART goals, roadmap |
| Low Shipping Velocity | HIGH | Time-box research phases |

---

## Quarterly Retrospectives

- [Q4 2024 Retrospective](./retrospectives/2024-Q4_retrospective.md) - 📋 Scheduled for Dec 31

---

## Usage

### After Every Project/Sprint:
1. Create lesson document using template
2. Extract reusable patterns
3. Update failure modes database
4. Cross-reference related lessons

### During Planning:
1. Review relevant lessons before starting
2. Check failure modes for known pitfalls
3. Apply validated patterns
4. Reference in decision logs

### Quarterly:
1. Run retrospective
2. Analyze trends
3. Update protocols
4. Archive old lessons

---

## Integration with Other Protocols

**Decision-Making:**
- Check lessons before major decisions
- Document decision outcomes as lessons

**Mining:**
- Extract lessons from conversation logs
- Mine project outcomes for insights

**Prompt Generation:**
- Use lessons to improve future prompts
- Reference patterns in generated content

---

## Success Metrics

- [ ] Every project ends with documented lesson
- [ ] Patterns library grows (target: 1 new pattern/month)
- [ ] Failure modes decrease over time (same mistake not repeated)
- [ ] Quarterly retrospectives completed on time
- [ ] Lessons referenced in future decisions

---

## Quick Add

**To document a quick lesson:**
```bash
# Create new lesson
touch learning/lessons/$(date +%Y-%m-%d)_topic_name.md

# Use template
cat learning/lesson_template.md > learning/lessons/$(date +%Y-%m-%d)_topic_name.md
```

---

## Maintenance

- **Weekly:** Add lessons from completed work
- **Monthly:** Review and categorize
- **Quarterly:** Retrospective and cleanup
- **Yearly:** Archive old lessons, update patterns
