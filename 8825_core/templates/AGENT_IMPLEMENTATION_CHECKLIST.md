# Agent Implementation Checklist

**Agent:** [Agent Name]  
**Implementer:** [Your Name]  
**Start Date:** [YYYY-MM-DD]  
**Target Date:** [YYYY-MM-DD]

---

## Pre-Implementation

### Setup
- [ ] Read agent spec completely
- [ ] Review PromptGen analysis
- [ ] Check agent registry for context
- [ ] Set up development environment
- [ ] Create working directory/branch
- [ ] Post standup: "Starting [Agent Name]"

### Understanding
- [ ] Understand problem being solved
- [ ] Understand success criteria
- [ ] Understand edge cases
- [ ] Understand integration points
- [ ] Questions answered by Architect

---

## Phase 1: Core Functionality

### Project Structure
- [ ] Create main agent file
- [ ] Create test file
- [ ] Create README.md
- [ ] Create requirements.txt
- [ ] Set up logging

### Core Logic
- [ ] Implement main decision logic
- [ ] Implement input validation
- [ ] Implement output formatting
- [ ] Add type hints
- [ ] Add docstrings

### Error Handling
- [ ] Handle missing data
- [ ] Handle invalid input
- [ ] Handle API failures
- [ ] Handle network issues
- [ ] Handle unexpected formats
- [ ] Add meaningful error messages

### Testing
- [ ] Write unit tests for core logic
- [ ] Write tests for decision making
- [ ] Write tests for error handling
- [ ] All tests passing locally

---

## Phase 2: Integration

### API Connections
- [ ] Implement API authentication
- [ ] Implement API calls
- [ ] Handle rate limits
- [ ] Handle timeouts
- [ ] Handle retries

### Data Flow
- [ ] Implement input processing
- [ ] Implement data transformation
- [ ] Implement output generation
- [ ] Validate data formats

### Logging
- [ ] Add info-level logging
- [ ] Add warning-level logging
- [ ] Add error-level logging
- [ ] Test log output

### Testing
- [ ] Write integration tests
- [ ] Test API connections
- [ ] Test data flow
- [ ] Test end-to-end scenarios
- [ ] All tests passing

---

## Phase 3: Edge Cases

### Edge Case Handling
- [ ] Test with missing data
- [ ] Test with invalid input
- [ ] Test with API failures
- [ ] Test with network issues
- [ ] Test with unexpected formats
- [ ] All edge cases handled gracefully

### Performance
- [ ] Test response time
- [ ] Test with large inputs
- [ ] Test concurrent requests
- [ ] Optimize if needed

---

## Phase 4: Documentation

### README.md
- [ ] Overview section
- [ ] Installation instructions
- [ ] Configuration instructions
- [ ] Usage examples (basic)
- [ ] Usage examples (advanced)
- [ ] Troubleshooting section
- [ ] API documentation (if applicable)

### Code Documentation
- [ ] All functions have docstrings
- [ ] Complex logic has comments
- [ ] Type hints added
- [ ] Examples in docstrings

### Usage Examples
- [ ] Basic usage example
- [ ] Advanced usage example
- [ ] Common patterns documented
- [ ] Edge case examples

---

## Phase 5: Quality Assurance

### Code Quality
- [ ] No hardcoded credentials
- [ ] Environment variables used
- [ ] Error messages are clear
- [ ] Code follows Python conventions
- [ ] No unused imports
- [ ] No debug print statements

### Testing Quality
- [ ] All success criteria tested
- [ ] All edge cases tested
- [ ] Test coverage > 80%
- [ ] Tests are readable
- [ ] Tests are maintainable

### Documentation Quality
- [ ] README is clear
- [ ] Examples are copy-paste ready
- [ ] Troubleshooting is helpful
- [ ] No broken links
- [ ] No typos

---

## Phase 6: Registry & Tracking

### Registry Update
- [ ] Update agent status to "in_progress"
- [ ] Add implementation notes
- [ ] Add blockers (if any)
- [ ] Update completion estimate

### Protocol Tracking
- [ ] Track PromptGen usage
- [ ] Track Team Execution Protocol usage
- [ ] Note any protocol issues

---

## Phase 7: Self-Review

### Functional Review
- [ ] All success criteria met
- [ ] All requirements implemented
- [ ] All edge cases handled
- [ ] Performance acceptable

### Quality Review
- [ ] Code is clean
- [ ] Tests are comprehensive
- [ ] Documentation is complete
- [ ] No known bugs

### Integration Review
- [ ] Integrates with existing systems
- [ ] Doesn't break production
- [ ] Backward compatible
- [ ] Follows system conventions

---

## Phase 8: Submission

### Pre-Submission
- [ ] All tests passing
- [ ] All documentation complete
- [ ] Registry updated
- [ ] Protocol usage tracked
- [ ] Self-review complete

### Submission Package
- [ ] Code files
- [ ] Test files
- [ ] README.md
- [ ] requirements.txt
- [ ] Usage examples
- [ ] Review request in `team/reviews/`

### Review Request Format
```markdown
## [Agent Name] - Ready for Review

### What Was Built
[Brief description]

### Success Criteria Met
- [x] Criterion 1
- [x] Criterion 2
- [x] Criterion 3

### Testing Done
- Unit tests: [X] tests, [X]% coverage
- Integration tests: [X] scenarios
- Edge case tests: [X] cases

### Documentation
- README.md: Complete
- Usage examples: [X] examples
- API docs: [Yes/No]

### Known Issues
[Any issues or limitations]

### Questions for Reviewer
[Anything reviewer should know]
```

---

## Post-Submission

### During Review
- [ ] Respond to reviewer questions
- [ ] Make requested changes
- [ ] Re-test after changes
- [ ] Update documentation if needed
- [ ] Resubmit if needed

### After Approval
- [ ] Celebrate! 🎉
- [ ] Update registry to "completed"
- [ ] Post standup: "Completed [Agent Name]"
- [ ] Capture learnings in `team/learnings/`
- [ ] Help Integration Specialist with deployment

---

## Common Pitfalls

### ❌ Don't
- Skip PromptGen analysis
- Hardcode credentials
- Skip error handling
- Skip tests
- Skip documentation
- Submit without self-review

### ✅ Do
- Follow the spec
- Handle edge cases
- Write clear code
- Test thoroughly
- Document well
- Ask questions early

---

## Getting Help

### Stuck on Implementation?
- Review existing agents for patterns
- Check templates and examples
- Ask Integration Specialist
- Post in team channel

### Stuck on Testing?
- Review test examples
- Ask QA/Operations
- Check existing test files

### Stuck on Documentation?
- Review other agent READMEs
- Use templates
- Ask for feedback early

### Blocked?
- Post in daily standup
- Tag relevant person
- Escalate to Architect if urgent

---

## Success Indicators

### You're on track if:
- ✅ Daily standups posted
- ✅ Tests passing
- ✅ Documentation growing
- ✅ Questions answered
- ✅ On schedule

### Warning signs:
- ⚠️ No progress for 2+ days
- ⚠️ Tests failing
- ⚠️ Unclear requirements
- ⚠️ Scope creeping
- ⚠️ No documentation

**If you see warning signs, raise them immediately!**

---

## Completion Criteria

### Ready for Review When:
- ✅ All checklist items complete
- ✅ All tests passing
- ✅ All documentation complete
- ✅ Self-review done
- ✅ Registry updated
- ✅ Protocol usage tracked

### Ready for Integration When:
- ✅ Architect approval received
- ✅ All feedback addressed
- ✅ Final tests passing
- ✅ Documentation updated

---

**Checklist Version:** 1.0  
**Last Updated:** 2025-11-13  
**Owner:** 8825 Team
