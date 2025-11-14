# Agent Review Checklist

**Agent:** [Agent Name]  
**Implementer:** [Name]  
**Reviewer:** [Your Name]  
**Review Date:** [YYYY-MM-DD]

---

## Pre-Review

### Submission Quality
- [ ] Review request is complete
- [ ] All required files included
- [ ] Documentation provided
- [ ] Test results included
- [ ] Self-review completed

### Context Understanding
- [ ] Read agent spec
- [ ] Understand problem being solved
- [ ] Understand success criteria
- [ ] Understand integration points

---

## Functional Review

### PromptGen Criteria

#### 1. Problem Definition
- [ ] Solves the stated problem
- [ ] Addresses the core need
- [ ] Meets minimum viable solution
- [ ] No scope creep

**Notes:**

---

#### 2. Context Gathering
- [ ] Uses existing patterns appropriately
- [ ] Integrates with existing systems
- [ ] Respects constraints
- [ ] Reuses code where appropriate

**Notes:**

---

#### 3. Requirements (Explicit)
- [ ] All explicit requirements met
- [ ] Core functionality complete
- [ ] Performance requirements met
- [ ] Integration requirements met

**Notes:**

---

#### 4. Requirements (Implicit)
- [ ] Appropriate for user skill level
- [ ] Runs in correct environment
- [ ] Handles expected usage patterns
- [ ] Frequency/timing appropriate

**Notes:**

---

#### 5. Constraints
- [ ] Respects technical constraints
- [ ] Preserves Proof Protocol
- [ ] Doesn't break production
- [ ] Backward compatible
- [ ] Within resource constraints

**Notes:**

---

#### 6. Edge Cases
- [ ] Missing data handled
- [ ] Invalid input handled
- [ ] API failures handled
- [ ] Network issues handled
- [ ] Unexpected formats handled

**Notes:**

---

#### 7. Success Criteria
- [ ] All success criteria met
- [ ] "Done" is clearly achieved
- [ ] Validation possible
- [ ] Metrics defined

**Notes:**

---

## Code Quality Review

### Structure & Organization
- [ ] Code is well-organized
- [ ] Logical file structure
- [ ] Clear separation of concerns
- [ ] No unnecessary complexity

**Notes:**

---

### Python Standards
- [ ] Python 3.9+ compatible
- [ ] Follows PEP 8 conventions
- [ ] Type hints used appropriately
- [ ] Docstrings complete
- [ ] No unused imports
- [ ] No debug statements

**Notes:**

---

### Error Handling
- [ ] All external calls have error handling
- [ ] Error messages are clear
- [ ] Errors logged appropriately
- [ ] Graceful degradation
- [ ] No silent failures

**Notes:**

---

### Security
- [ ] No hardcoded credentials
- [ ] Environment variables used
- [ ] Input validation present
- [ ] No SQL injection risks
- [ ] No command injection risks
- [ ] API keys protected

**Notes:**

---

### Performance
- [ ] No obvious performance issues
- [ ] Efficient algorithms used
- [ ] No unnecessary loops
- [ ] Appropriate data structures
- [ ] Resource usage reasonable

**Notes:**

---

## Testing Review

### Unit Tests
- [ ] Core logic tested
- [ ] Decision making tested
- [ ] Error handling tested
- [ ] Tests are readable
- [ ] Tests are maintainable
- [ ] Coverage adequate (>80%)

**Run tests yourself:**
```bash
python3 -m pytest path/to/tests/
```

**Test results:**

---

### Integration Tests
- [ ] API connections tested
- [ ] Data flow tested
- [ ] End-to-end scenarios tested
- [ ] Integration points verified

**Run integration tests:**
```bash
python3 -m pytest path/to/tests/integration/
```

**Test results:**

---

### Edge Case Tests
- [ ] All edge cases from spec tested
- [ ] Additional edge cases considered
- [ ] Error scenarios tested
- [ ] Boundary conditions tested

**Manual edge case testing:**
1. [Test case 1]
2. [Test case 2]

**Results:**

---

## Documentation Review

### README.md
- [ ] Overview is clear
- [ ] Installation instructions complete
- [ ] Configuration instructions clear
- [ ] Usage examples work
- [ ] Troubleshooting helpful
- [ ] No typos

**Test examples yourself:**
```bash
# Try the examples from README
```

**Results:**

---

### Code Documentation
- [ ] All functions have docstrings
- [ ] Complex logic has comments
- [ ] Type hints present
- [ ] Examples in docstrings
- [ ] Parameters documented
- [ ] Return values documented

**Notes:**

---

### API Documentation
- [ ] Input format documented
- [ ] Output format documented
- [ ] Error codes documented
- [ ] Rate limits documented (if applicable)

**OR**

✅ No API (not applicable)

**Notes:**

---

## Integration Review

### Dependencies
- [ ] All dependencies listed
- [ ] Versions pinned
- [ ] No unnecessary dependencies
- [ ] Dependencies are maintained
- [ ] License compatible

**Check requirements.txt:**
```bash
pip install -r requirements.txt
```

**Results:**

---

### System Integration
- [ ] Integrates with existing systems
- [ ] Doesn't break production
- [ ] Backward compatible
- [ ] Follows system conventions
- [ ] Uses existing utilities

**Notes:**

---

### Data Flow
- [ ] Input format matches spec
- [ ] Output format matches spec
- [ ] Data transformations correct
- [ ] No data loss

**Notes:**

---

## Production Readiness

### Configuration
- [ ] Environment variables documented
- [ ] Configuration is flexible
- [ ] Defaults are sensible
- [ ] No hardcoded values

**Notes:**

---

### Logging
- [ ] Info-level logging present
- [ ] Warning-level logging present
- [ ] Error-level logging present
- [ ] Log messages are clear
- [ ] No sensitive data in logs

**Notes:**

---

### Monitoring
- [ ] Success metrics defined
- [ ] Error tracking possible
- [ ] Performance monitoring possible
- [ ] Alerts defined (if needed)

**Notes:**

---

### Deployment
- [ ] Deployment steps clear
- [ ] Migration steps documented (if needed)
- [ ] Rollback plan exists
- [ ] No breaking changes

**Notes:**

---

## Protocol Compliance

### Team Execution Protocol
- [ ] Followed workflow phases
- [ ] Daily standups posted
- [ ] Quality standards met
- [ ] Handoff procedures followed

**Notes:**

---

### PromptGen Protocol
- [ ] PromptGen analysis complete
- [ ] All 7 steps addressed
- [ ] Spec matches implementation
- [ ] Success criteria validated

**Notes:**

---

### Proof Protocol
- [ ] Usage tracking possible
- [ ] Metrics defined
- [ ] Learning extraction possible
- [ ] Evolution path clear

**Notes:**

---

## Known Issues Review

### Issues Assessment
- [ ] All known issues documented
- [ ] Severity assessed correctly
- [ ] Workarounds provided
- [ ] No showstoppers

**Critical issues:**

**Non-critical issues:**

---

### Limitations Assessment
- [ ] Limitations documented
- [ ] Rationale provided
- [ ] Acceptable trade-offs

**Notes:**

---

## Decision

### Overall Assessment

**Strengths:**
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

**Areas for Improvement:**
1. [Area 1]
2. [Area 2]
3. [Area 3]

**Critical Issues:**
1. [Issue 1]
2. [Issue 2]

**OR**

✅ No critical issues

---

### Review Decision

Select one:

- [ ] **✅ APPROVED** - Ready for integration
  - All criteria met
  - No critical issues
  - Production ready

- [ ] **⚠️ APPROVED WITH MINOR CHANGES** - Can integrate after small fixes
  - Minor issues only
  - Changes can be made quickly
  - List changes below

- [ ] **🔨 CHANGES REQUESTED** - Needs rework before integration
  - Significant issues found
  - Requires re-testing
  - List changes below

- [ ] **❌ REJECTED** - Does not meet requirements
  - Critical issues
  - Requires major rework
  - List reasons below

---

### Required Changes

**If changes requested, list them here:**

#### Must Fix (Blocking)
1. [Change 1 - why it's critical]
2. [Change 2 - why it's critical]

#### Should Fix (Important)
1. [Change 1 - why it matters]
2. [Change 2 - why it matters]

#### Nice to Have (Optional)
1. [Suggestion 1]
2. [Suggestion 2]

---

### Next Steps

**If approved:**
1. Pass to Integration Specialist
2. Deploy to staging
3. Monitor initial usage

**If changes requested:**
1. Implementer addresses feedback
2. Re-test affected areas
3. Update documentation if needed
4. Resubmit for review

**If rejected:**
1. Discuss with implementer
2. Clarify requirements
3. Create new implementation plan

---

## Feedback for Implementer

### What Went Well
1. [Positive feedback 1]
2. [Positive feedback 2]
3. [Positive feedback 3]

### Learning Opportunities
1. [Learning 1]
2. [Learning 2]

### For Next Time
1. [Suggestion 1]
2. [Suggestion 2]

---

## Reviewer Notes

### Time Spent
- **Review time:** [X] hours
- **Testing time:** [X] hours
- **Total time:** [X] hours

### Difficulty
- [ ] Easy - straightforward review
- [ ] Medium - some complexity
- [ ] Hard - complex or large changes

### Confidence Level
- [ ] High - very confident in review
- [ ] Medium - mostly confident
- [ ] Low - need second opinion

**If low confidence, recommend second reviewer:**

---

## Approval Signature

**Reviewer:** [Your name]  
**Date:** [YYYY-MM-DD]  
**Decision:** [Approved / Changes Requested / Rejected]  
**Signature:** [Your initials]

---

**Review Checklist Version:** 1.0  
**Last Updated:** 2025-11-13  
**Owner:** 8825 Team
