# Agent Specification: [AGENT_NAME]

**Agent ID:** [From registry - e.g., AGENT-LIBRARY-MINING-COMPLEXITY-ROUTER-0001]  
**Priority Score:** [From registry]  
**Assigned To:** [Team member name]  
**Start Date:** [YYYY-MM-DD]  
**Target Completion:** [YYYY-MM-DD]

---

## PromptGen Analysis

### 1. Problem Definition

**What problem are we solving?**
- Core need:
- Pain point:
- What happens if we don't solve this:
- Minimum viable solution:

**Current State:**
- What exists:
- What's missing:
- Why now:

---

### 2. Context Gathering

**What do we already know?**
- Existing solutions:
- Patterns we can reuse:
- Constraints that apply:
- Related agents/workflows:

**Dependencies:**
- Required integrations:
- Data sources needed:
- APIs to connect:

---

### 3. Requirements (Explicit)

**What MUST the solution do?**

#### Core Functionality
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

#### Performance Requirements
- Response time:
- Throughput:
- Accuracy:

#### Integration Requirements
- Input format:
- Output format:
- API endpoints:

---

### 4. Requirements (Implicit)

**What's assumed but not stated?**

- **Who will use this:** [User persona]
- **Where will it run:** [Environment]
- **When will it be used:** [Frequency/timing]
- **How often:** [Usage pattern]
- **Skill level required:** [Technical level]

---

### 5. Constraints

**Technical Constraints:**
- API limitations:
- Rate limits:
- Data format restrictions:
- Python version: 3.9+
- Dependencies:

**Process Constraints:**
- Must preserve Proof Protocol
- Cannot break production systems
- Backward compatibility required

**Resource Constraints:**
- API costs:
- Compute requirements:
- Storage needs:

---

### 6. Edge Cases

**What could go wrong?**

1. **Missing Data**
   - Scenario:
   - Handling:

2. **Invalid Input**
   - Scenario:
   - Handling:

3. **API Failures**
   - Scenario:
   - Handling:

4. **Network Issues**
   - Scenario:
   - Handling:

5. **Unexpected Formats**
   - Scenario:
   - Handling:

---

### 7. Success Criteria

**How do we know it works?**

#### Functional Success
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

#### Quality Success
- [ ] All tests passing
- [ ] Error handling complete
- [ ] Documentation complete
- [ ] Edge cases handled

#### Performance Success
- [ ] Response time < [X] seconds
- [ ] Accuracy > [X]%
- [ ] Handles [X] requests/hour

---

## Technical Design

### Input Format
```json
{
  "example": "input structure"
}
```

### Output Format
```json
{
  "example": "output structure"
}
```

### Decision Logic
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Adaptation Mechanism
- How agent learns:
- What triggers changes:
- How it improves:

---

## Implementation Plan

### Phase 1: Core Functionality
**Duration:** [X] days

**Tasks:**
- [ ] Set up project structure
- [ ] Implement main logic
- [ ] Add error handling
- [ ] Write unit tests

### Phase 2: Integration
**Duration:** [X] days

**Tasks:**
- [ ] Connect to data sources
- [ ] Implement API calls
- [ ] Add logging
- [ ] Write integration tests

### Phase 3: Documentation
**Duration:** [X] days

**Tasks:**
- [ ] Write README
- [ ] Create usage examples
- [ ] Document edge cases
- [ ] Update registry

---

## Testing Strategy

### Unit Tests
- Test core logic
- Test decision making
- Test error handling

### Integration Tests
- Test API connections
- Test data flow
- Test end-to-end scenarios

### Edge Case Tests
- Test with missing data
- Test with invalid input
- Test with API failures

---

## Documentation Requirements

### README.md
- Overview
- Installation
- Usage examples
- Configuration
- Troubleshooting

### API Documentation
- Input parameters
- Output format
- Error codes
- Rate limits

### Usage Examples
- Basic usage
- Advanced usage
- Common patterns
- Edge cases

---

## Dependencies

### Python Packages
```
package-name==version
```

### External APIs
- API name
- Authentication method
- Rate limits
- Documentation link

### System Requirements
- Python 3.9+
- Environment variables needed
- File system access

---

## Deployment Plan

### Development
- Local testing
- Unit tests
- Integration tests

### Staging
- End-to-end testing
- Performance testing
- Edge case validation

### Production
- Gradual rollout
- Monitoring setup
- Rollback plan

---

## Monitoring & Metrics

### Success Metrics
- Usage count
- Success rate
- Response time
- Error rate

### Logging
- Info level: Normal operations
- Warning level: Recoverable issues
- Error level: Failures

### Alerts
- Error rate > [X]%
- Response time > [X] seconds
- API failures

---

## Questions & Decisions

### Open Questions
1. [Question 1]
2. [Question 2]

### Decisions Made
1. [Decision 1] - [Rationale]
2. [Decision 2] - [Rationale]

### Assumptions
1. [Assumption 1]
2. [Assumption 2]

---

## Review Checklist

Before submitting for review:

- [ ] PromptGen analysis complete
- [ ] All requirements documented
- [ ] Edge cases identified
- [ ] Success criteria defined
- [ ] Implementation plan clear
- [ ] Testing strategy defined
- [ ] Documentation requirements listed
- [ ] Dependencies identified
- [ ] Architect approval received

---

**Spec Version:** 1.0  
**Last Updated:** [YYYY-MM-DD]  
**Status:** [Draft | Approved | In Progress | Complete]
