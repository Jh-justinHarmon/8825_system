# Team Execution Protocol

**Version:** 1.0  
**Status:** Production Ready  
**Date:** 2025-11-13  
**Purpose:** Coordinate multi-person execution on 8825 system development

---

## Core Principles

1. **Proof Protocol First** - Let usage determine what survives
2. **PromptGen Before Code** - Structured thinking before execution
3. **Clear Ownership** - One person owns each component
4. **Async-First** - Daily updates, weekly sync
5. **Quality Over Speed** - Working code > fast code

---

## Team Roles

### Architect (Justin)
**Responsibilities:**
- Define system architecture
- Review all PRs/changes
- Resolve conflicts and blockers
- Set priorities
- Final approval on all work

**Time Commitment:** 1-2 hours daily for reviews

### Agent Implementers (2-3 people)
**Responsibilities:**
- Build agents per spec
- Write tests
- Document usage
- Track protocol usage
- Submit work for review

**Skills Required:**
- Python 3.9+
- API integration experience
- JSON/file handling
- Basic testing

### Integration Specialist (1 person)
**Responsibilities:**
- Connect agents to workflows
- Test end-to-end flows
- Monitor production systems
- Handle API integrations
- Deploy to production

**Skills Required:**
- System integration experience
- API debugging
- Production monitoring
- Error handling

### QA/Operations (1 person)
**Responsibilities:**
- Test implementations
- Provide operational feedback
- Document edge cases
- Track success metrics
- Capture learnings

**Skills Required:**
- Testing mindset
- Documentation skills
- User perspective
- Attention to detail

---

## Workflow

### 1. Planning Phase (Architect + Team)

**Input:** Agent from registry (priority score)

**Process:**
1. Architect presents agent requirements
2. Team applies PromptGen methodology together
3. Generate detailed spec
4. Identify success criteria
5. Assign owner

**Output:** Detailed agent spec in `team/assignments/`

**Duration:** 1-2 hours (sync or async)

---

### 2. Implementation Phase (Agent Implementer)

**Input:** Agent spec from planning

**Process:**
1. Read spec and PromptGen checklist
2. Set up development environment
3. Implement core functionality
4. Write tests
5. Self-test against success criteria
6. Document usage examples
7. Update registry status

**Output:** Working code + tests + docs

**Duration:** 3-7 days depending on complexity

**Daily Updates:** Post progress in `team/standups/`

---

### 3. Review Phase (Architect)

**Input:** Submitted work from implementer

**Process:**
1. Check against PromptGen criteria
2. Test functionality
3. Review code quality
4. Review documentation
5. Verify registry update
6. Approve or provide feedback

**Output:** Approved work or change requests

**Duration:** 1-2 hours

**Feedback:** Detailed comments in `team/reviews/`

---

### 4. Integration Phase (Integration Specialist)

**Input:** Approved agent implementation

**Process:**
1. Connect to existing workflows
2. Test end-to-end flows
3. Verify API integrations
4. Check error handling
5. Deploy to production
6. Monitor initial usage

**Output:** Agent live in production

**Duration:** 1-2 days

---

### 5. Validation Phase (QA/Operations)

**Input:** Agent in production

**Process:**
1. Real-world testing
2. Track usage patterns
3. Capture learnings
4. Document edge cases
5. Report issues
6. Track success metrics

**Output:** Usage data + learnings + issues

**Duration:** Ongoing (1 week minimum)

---

### 6. Evolution Phase (Automatic via ALS)

**Input:** Usage data from validation

**Process:**
1. Usage tracking (automatic)
2. Decay monitoring (automatic)
3. Competition resolution (automatic)
4. Learning extraction (automatic)

**Output:** Agent promoted, maintained, or deprecated

**Duration:** Continuous

---

## Communication Cadence

### Daily (Async)
**Format:** Standup update in `team/standups/YYYY-MM-DD.md`

**Template:**
```markdown
## [Your Name] - [Date]

### Yesterday
- What you completed
- Blockers resolved

### Today
- What you're working on
- Expected completion

### Blockers
- Any issues preventing progress
- Help needed
```

**Time:** 5 minutes to write, 10 minutes to read all

---

### Weekly (Sync - 30 min)
**Format:** Video/voice call or detailed async discussion

**Agenda:**
1. Review progress (10 min)
2. Discuss blockers (10 min)
3. Reprioritize if needed (5 min)
4. Plan next week (5 min)

**Output:** Updated priorities, resolved blockers

---

### Monthly (Sync - 1 hour)
**Format:** Retrospective + planning

**Agenda:**
1. Review metrics (15 min)
   - Agents completed
   - Quality issues
   - Team velocity
2. Process improvements (20 min)
   - What worked
   - What didn't
   - Changes to make
3. Plan next month (20 min)
   - Agent priorities
   - Resource allocation
4. Celebrate wins (5 min)

**Output:** Process updates, next month plan

---

## Handoff Procedures

### Starting New Work

**Checklist:**
- [ ] Read agent spec from `team/assignments/`
- [ ] Review PromptGen checklist
- [ ] Check agent registry for context
- [ ] Set up development environment
- [ ] Post standup: "Starting [Agent Name]"
- [ ] Create working branch (if using Git)

**Questions?** Ask in team channel or tag Architect

---

### Submitting Work

**Checklist:**
- [ ] Self-test against success criteria
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Usage examples provided
- [ ] Registry status updated
- [ ] Protocol usage tracked
- [ ] Submit for review in `team/reviews/`

**Format:**
```markdown
## [Agent Name] - Ready for Review

### What Was Built
- Brief description

### Success Criteria Met
- [x] Criterion 1
- [x] Criterion 2

### Testing Done
- Test scenarios covered

### Documentation
- Link to docs

### Questions/Concerns
- Anything reviewer should know
```

---

### Reviewing Work

**Checklist:**
- [ ] Check against PromptGen criteria
- [ ] Test core functionality
- [ ] Test edge cases
- [ ] Review code quality
- [ ] Review documentation
- [ ] Verify registry update
- [ ] Provide feedback or approve

**Feedback Format:**
```markdown
## Review: [Agent Name]

### ✅ Strengths
- What worked well

### 🔨 Changes Needed
- Specific issues to fix
- Why they matter

### 💡 Suggestions (Optional)
- Nice-to-haves
- Future improvements

### Decision
- [ ] Approved - ready for integration
- [ ] Changes requested - resubmit after fixes
```

---

## Quality Standards

### Code Quality
- **Python 3.9+** compatible
- **Type hints** where helpful
- **Error handling** for all external calls
- **Logging** for debugging
- **Comments** for complex logic
- **No hardcoded credentials** (use env vars)

### Testing Requirements
- **Unit tests** for core logic
- **Integration tests** for API calls
- **Edge case tests** for error handling
- **Success criteria** validated

### Documentation Requirements
- **README** with overview
- **Usage examples** (copy-paste ready)
- **API documentation** if applicable
- **Troubleshooting** section
- **Registry entry** updated

---

## PromptGen Integration

**REQUIRED:** Apply PromptGen before any implementation

### 7-Step Checklist

1. **Problem Definition**
   - What are we solving?
   - Why does it matter?
   - What's the minimum viable solution?

2. **Context Gathering**
   - What exists already?
   - What patterns can we reuse?
   - What constraints apply?

3. **Requirements (Explicit)**
   - What MUST the solution do?
   - Core functionality
   - Performance requirements

4. **Requirements (Implicit)**
   - Who will use this?
   - Where will it run?
   - How often?

5. **Constraints**
   - Technical limitations
   - Time constraints
   - Cost constraints

6. **Edge Cases**
   - What could go wrong?
   - Missing data
   - API failures
   - Invalid input

7. **Success Criteria**
   - How do we know it works?
   - What does "done" look like?
   - How do we validate?

**Output:** Detailed spec in `team/assignments/[agent-name]-spec.md`

---

## Protocol Tracking

**REQUIRED:** Track protocol usage for all work

### When to Track

**After completing work:**
```bash
./track_protocol.py TEAM_EXECUTION_PROTOCOL --success \
  --context "Implemented Library Mining Router"
```

**If protocol didn't work:**
```bash
./track_protocol.py TEAM_EXECUTION_PROTOCOL --fail \
  --notes "Spec was unclear, needed more examples"
```

**After using PromptGen:**
```bash
./track_protocol.py PROMPTGEN_INTEGRATION_PROTOCOL --success \
  --context "Planned Joju Curation Agent"
```

### Why Track?
- Proof Protocol in action
- Identifies what works
- Improves process over time
- Automatic decay of unused protocols

---

## Success Metrics

### Week 1
- [ ] Team has access to shared folders
- [ ] Everyone can read Brain Transport
- [ ] Roles assigned
- [ ] First agent in progress

### Month 1
- [ ] 2 high-priority agents completed
- [ ] Team using protocol tracking
- [ ] Zero production breaks
- [ ] Learnings captured

### Quarter 1
- [ ] All 4 remaining agents completed
- [ ] Team self-organizing
- [ ] Protocol usage shows patterns
- [ ] New workflows documented

---

## Conflict Resolution

### Technical Conflicts
1. Implementer explains approach
2. Architect provides alternative
3. Team discusses trade-offs
4. Architect makes final decision
5. Document decision in learnings

### Priority Conflicts
1. Review agent priority scores
2. Consider business impact
3. Check dependencies
4. Architect decides
5. Update registry

### Process Conflicts
1. Raise in weekly sync
2. Team discusses
3. Try new approach for 1 week
4. Evaluate results
5. Keep or revert

---

## Tools & Resources

### Required Access
- **Dropbox:** `8825-workspace/` folder (shared)
- **iCloud:** Brain Transport (read-only)
- **Capabilities Doc:** `8825_SYSTEM_CAPABILITIES.md`

### Key Files
- **Agent Registry:** `8825_core/registry/agents.json`
- **Templates:** `8825_core/templates/`
- **Protocols:** `8825_core/protocols/`
- **Team Workspace:** `team/`

### Tools
- **Protocol Tracker:** `8825_core/protocols/track_protocol.py`
- **Agent Registry:** `8825_core/registry/agents.json`
- **Brain Transport:** `~/Documents/8825_BRAIN_TRANSPORT.json`

---

## Getting Help

### Questions About...

**System Architecture**
- Ask Architect
- Check capabilities doc
- Review Brain Transport

**Implementation Details**
- Check existing agents
- Review templates
- Ask Integration Specialist

**Process/Workflow**
- This protocol
- Ask in team channel
- Raise in weekly sync

**Blockers**
- Post in daily standup
- Tag relevant person
- Escalate to Architect if urgent

---

## Version History

**v1.0 (2025-11-13)**
- Initial protocol
- 5-phase workflow
- Communication cadence
- Quality standards
- PromptGen integration

---

**Next Review:** 2025-12-13 (1 month)  
**Owner:** Justin Harmon  
**Status:** Ready for team use
