# Agent Review Request: [AGENT_NAME]

**Agent ID:** [From registry]  
**Implementer:** [Your name]  
**Submission Date:** [YYYY-MM-DD]  
**Review Requested From:** [Architect name]

---

## Summary

**What Was Built:**
[1-2 sentence description of what this agent does]

**Why It Matters:**
[1-2 sentences on the problem this solves]

---

## Success Criteria

### Functional Requirements
- [x] [Requirement 1 from spec]
- [x] [Requirement 2 from spec]
- [x] [Requirement 3 from spec]
- [x] [Requirement 4 from spec]

### Quality Requirements
- [x] All tests passing
- [x] Error handling complete
- [x] Documentation complete
- [x] Edge cases handled

### Performance Requirements
- [x] Response time < [X] seconds
- [x] Accuracy > [X]%
- [x] Handles [X] requests/hour

**All success criteria met:** ✅ Yes / ⚠️ Partial / ❌ No

---

## Testing Summary

### Unit Tests
- **Count:** [X] tests
- **Coverage:** [X]%
- **Status:** ✅ All passing

**Key tests:**
- Test 1: [Description]
- Test 2: [Description]
- Test 3: [Description]

### Integration Tests
- **Count:** [X] scenarios
- **Status:** ✅ All passing

**Scenarios tested:**
- Scenario 1: [Description]
- Scenario 2: [Description]

### Edge Case Tests
- **Count:** [X] cases
- **Status:** ✅ All passing

**Cases tested:**
- Missing data: [How handled]
- Invalid input: [How handled]
- API failure: [How handled]
- Network issue: [How handled]

---

## Documentation

### Files Included
- [x] README.md (overview, installation, usage)
- [x] Usage examples (basic + advanced)
- [x] API documentation (if applicable)
- [x] Troubleshooting guide
- [x] requirements.txt

### Documentation Quality
- [x] Examples are copy-paste ready
- [x] All parameters documented
- [x] Error messages explained
- [x] No broken links
- [x] No typos

**Documentation location:** [Path to README]

---

## Code Quality

### Standards Met
- [x] Python 3.9+ compatible
- [x] Type hints added
- [x] Docstrings complete
- [x] Error handling comprehensive
- [x] Logging implemented
- [x] No hardcoded credentials
- [x] Environment variables used

### Code Statistics
- **Lines of code:** [X]
- **Functions:** [X]
- **Classes:** [X]
- **Test coverage:** [X]%

---

## Integration Points

### Dependencies
**Python packages:**
```
package-name==version
```

**External APIs:**
- API 1: [Name, purpose, rate limits]
- API 2: [Name, purpose, rate limits]

### System Integration
**Connects to:**
- [System/workflow 1]
- [System/workflow 2]

**Outputs to:**
- [Destination 1]
- [Destination 2]

**Backward compatible:** ✅ Yes / ❌ No

---

## Known Issues & Limitations

### Known Issues
1. [Issue 1 - severity, workaround]
2. [Issue 2 - severity, workaround]

**OR**

✅ No known issues

### Limitations
1. [Limitation 1 - why it exists]
2. [Limitation 2 - why it exists]

**OR**

✅ No significant limitations

### Future Improvements
1. [Nice-to-have 1]
2. [Nice-to-have 2]

---

## Questions for Reviewer

### Technical Questions
1. [Question 1]
2. [Question 2]

### Design Questions
1. [Question 1]
2. [Question 2]

**OR**

✅ No questions - ready for review

---

## Self-Review Checklist

### Pre-Submission
- [x] All checklist items from implementation guide complete
- [x] All tests passing locally
- [x] All documentation complete
- [x] Registry updated
- [x] Protocol usage tracked

### Code Review
- [x] Code is clean and readable
- [x] No debug statements
- [x] No unused imports
- [x] No hardcoded values
- [x] Error messages are clear

### Testing Review
- [x] All success criteria tested
- [x] All edge cases tested
- [x] Tests are maintainable
- [x] Test coverage adequate

### Documentation Review
- [x] README is clear
- [x] Examples work
- [x] Troubleshooting is helpful
- [x] No typos

---

## Protocol Tracking

### Protocols Used
- [x] Team Execution Protocol - ✅ Success
- [x] PromptGen Integration Protocol - ✅ Success

### Protocol Feedback
**What worked well:**
- [Feedback 1]
- [Feedback 2]

**What could be improved:**
- [Feedback 1]
- [Feedback 2]

**OR**

✅ Protocols worked perfectly

---

## Files Changed

### New Files
```
path/to/new/file1.py
path/to/new/file2.py
path/to/README.md
path/to/tests/test_agent.py
```

### Modified Files
```
path/to/modified/file1.py (reason)
path/to/modified/file2.py (reason)
```

**OR**

✅ No existing files modified

---

## Deployment Notes

### Environment Variables Needed
```bash
VARIABLE_NAME=description
VARIABLE_NAME_2=description
```

**OR**

✅ No new environment variables

### Configuration Changes
- [Change 1]
- [Change 2]

**OR**

✅ No configuration changes

### Migration Steps
1. [Step 1]
2. [Step 2]

**OR**

✅ No migration needed

---

## Testing Instructions for Reviewer

### Quick Test
```bash
# Run this to verify basic functionality
python3 path/to/agent.py --test
```

### Full Test Suite
```bash
# Run all tests
python3 -m pytest path/to/tests/

# Run with coverage
python3 -m pytest --cov=path/to/agent path/to/tests/
```

### Manual Testing
1. [Step 1]
2. [Step 2]
3. [Expected result]

---

## Timeline

**Start Date:** [YYYY-MM-DD]  
**Submission Date:** [YYYY-MM-DD]  
**Duration:** [X] days  
**Target Completion:** [YYYY-MM-DD]

**On schedule:** ✅ Yes / ⚠️ Delayed / ❌ Significantly delayed

**If delayed, reason:**
[Explanation]

---

## Learnings Captured

### What Went Well
1. [Learning 1]
2. [Learning 2]

### What Was Challenging
1. [Challenge 1 - how resolved]
2. [Challenge 2 - how resolved]

### What Would I Do Differently
1. [Improvement 1]
2. [Improvement 2]

**Learnings documented in:** `team/learnings/[agent-name]-learnings.md`

---

## Next Steps

### After Approval
1. Integration Specialist takes over
2. Deploy to staging
3. Test in staging
4. Deploy to production
5. Monitor initial usage

### If Changes Requested
1. Address feedback
2. Re-test
3. Update documentation
4. Resubmit

---

## Reviewer Section

**Reviewer:** [Name]  
**Review Date:** [YYYY-MM-DD]

### Review Status
- [ ] Approved - ready for integration
- [ ] Changes requested - see feedback below
- [ ] Rejected - see reasons below

### Feedback
[Reviewer fills this in]

### Changes Requested
[Reviewer fills this in]

### Approval Signature
[Reviewer name and date]

---

**Submission Version:** 1.0  
**Last Updated:** [YYYY-MM-DD]  
**Status:** Awaiting Review
