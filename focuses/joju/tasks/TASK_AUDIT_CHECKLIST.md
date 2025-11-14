# Task Audit Checklist

**Purpose:** Ensure accurate task completion tracking  
**Frequency:** Monthly or after major releases  
**Last Run:** November 10, 2025

---

## Pre-Audit Checklist

- [ ] Ensure `notion_sync.py` has pagination enabled
- [ ] Verify Notion API credentials are valid
- [ ] Pull ALL tasks (not just first 100)
- [ ] Check total task count matches Notion board
- [ ] Verify status property type is correct

---

## Audit Process

### 1. Pull Latest Tasks
```bash
cd focuses/joju/tasks
python3 notion_sync.py pull
```

**Verify:**
- [ ] Task count > 100 (should be ~238+)
- [ ] No errors during pull
- [ ] `local/tasks.json` updated

### 2. Check Codebase
```bash
# Verify Joju codebase location
ls -la /path/to/joju/src/pages
ls -la /path/to/joju/src/components
```

**Verify:**
- [ ] Can access Joju codebase
- [ ] All key components exist
- [ ] No permission issues

### 3. Run Audit Script
```python
# Compare tasks to codebase
# Check for implemented features
# Identify tasks that should be marked complete
```

**Check for:**
- [ ] Authentication (LoginPage.tsx)
- [ ] Profile features (ProfilePage.tsx, ProfileEditPage.tsx)
- [ ] Export (ExportPreviewPage.tsx)
- [ ] CV editing (CVView.tsx)
- [ ] Theme system (ThemeToggle.tsx)
- [ ] All section components

### 4. Review Findings
- [ ] List all tasks marked as complete
- [ ] Verify each has code evidence
- [ ] Check for false positives
- [ ] Document any unclear cases

### 5. Update Task Statuses
```python
# Update tasks to "Released" status
# NOT "Done" (doesn't exist)
```

**Verify:**
- [ ] Using correct status value ("Released")
- [ ] Using status type (not select)
- [ ] Batch updates work correctly
- [ ] No errors during update

### 6. Verify Updates
```bash
python3 notion_sync.py pull
```

**Check:**
- [ ] Status counts updated
- [ ] Released count increased
- [ ] Changes reflected in Notion board

---

## Post-Audit Checklist

### Documentation
- [ ] Create audit report (Markdown)
- [ ] Export to Word document
- [ ] Save to Documents folder
- [ ] Update this checklist

### Validation
- [ ] Review findings with team
- [ ] Get feedback on accuracy
- [ ] Note any corrections needed
- [ ] Update criteria if needed

### Follow-up
- [ ] Create tasks for any bugs found
- [ ] Update task naming conventions
- [ ] Improve task descriptions
- [ ] Link tasks to code (if possible)

---

## Common Issues & Solutions

### Issue: Only 100 tasks pulled
**Solution:** Check pagination in `notion_sync.py`

### Issue: Status update fails
**Solution:** Verify using `{'status': {'name': 'Released'}}` not select type

### Issue: Can't access Joju codebase
**Solution:** Check path and permissions

### Issue: False positives in audit
**Solution:** Refine matching criteria, check actual functionality

---

## Completion Criteria

**Task is complete if:**
1. ✅ Feature exists in codebase (file present)
2. ✅ Component is implemented (not just stub)
3. ✅ Functionality works (not broken)
4. ✅ Code evidence clear (not ambiguous)

**Task is NOT complete if:**
1. ❌ Only partially implemented
2. ❌ Broken or has critical bugs
3. ❌ Only in design/planning
4. ❌ Unclear or ambiguous evidence

---

## Status Mapping

### Complete Statuses:
- **Released** - Recently completed
- **Archived** - Older completed tasks

### Incomplete Statuses:
- Icebox - On hold
- Backlog - Not started
- Ready - Ready to start
- In progress - Being worked on
- Ready Review - Ready for review
- In review - Being reviewed
- In queue for release - About to release

---

## Metrics to Track

- [ ] Total tasks
- [ ] Complete tasks (Released + Archived)
- [ ] Completion percentage
- [ ] Tasks updated this audit
- [ ] False positives found
- [ ] Time spent on audit

---

## Report Template

```markdown
# Task Audit Report - [Date]

## Summary
- Total tasks: [count]
- Complete: [count] ([percentage]%)
- Updated: [count] tasks
- Time spent: [hours]

## Tasks Updated
1. [Task name] - [Reason]
2. ...

## Findings
- [Key findings]
- [Issues discovered]
- [Recommendations]

## Next Steps
- [Action items]
```

---

## Automation Opportunities

### Future Improvements:
1. **Automated matching** - Script to match tasks to code
2. **CI/CD integration** - Auto-update on deploy
3. **Regular scheduling** - Monthly automated audits
4. **Better linking** - Link tasks to commits/PRs
5. **Coverage tracking** - Link to test coverage

---

**Last Updated:** November 10, 2025  
**Next Audit:** December 10, 2025  
**Owner:** Development Team
