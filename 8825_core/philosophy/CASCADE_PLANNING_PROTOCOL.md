# Cascade Planning Protocol

**Date:** 2025-11-10  
**Status:** ACTIVE PROTOCOL  
**Applies To:** All non-trivial system changes

---

## Core Principle:

**Brainstorm → Review → Refine → Plan → Execute**

Never jump straight to execution on complex changes.

---

## The Protocol:

### **Phase 1: Brainstorm**
Cascade generates comprehensive brainstorm covering:
- Full scope of proposed change
- All affected components/touchpoints
- Potential risks and conflicts
- Implementation approach
- Feasibility assessment for each step
- Alternative approaches

**Output:** Detailed brainstorm document

---

### **Phase 2: Review**
User reviews brainstorm:
- Identifies gaps or concerns
- Questions assumptions
- Suggests refinements
- Validates approach

**Output:** User feedback

---

### **Phase 3: Refine**
Cascade incorporates feedback:
- Addresses concerns
- Fills gaps
- Adjusts approach
- Re-assesses feasibility

**Output:** Refined plan

---

### **Phase 4: Finalize**
User approves final plan:
- Confirms scope
- Agrees on approach
- Validates execution order
- Sets success criteria

**Output:** Approved execution plan

---

### **Phase 5: Execute**
Cascade implements approved plan:
- Follows agreed steps
- Reports progress
- Handles issues as they arise
- Verifies success criteria

**Output:** Implemented changes

---

## When This Protocol Applies:

### **Always Use For:**
- System architecture changes
- New core components
- Changes affecting multiple subsystems
- Daemon/service modifications
- Protocol/workflow changes
- Anything with "sprawl risk"

### **Can Skip For:**
- Single file edits
- Bug fixes (clear root cause)
- Documentation updates
- Simple script additions

---

## Why This Matters:

**Without this protocol:**
- Jump to execution
- Miss touchpoints
- Create conflicts
- Break existing systems
- Require 12 cleanup cycles

**With this protocol:**
- Understand full scope
- Identify all dependencies
- Prevent conflicts
- Build sustainable solutions
- Get it right the first time

---

## Example: Downloads Sync Crisis

**What happened:** Jumped to fixing sync script without auditing all touchpoints.

**Result:** Fixed script, but daemon kept running and undid the work.

**Should have been:**
1. Brainstorm: Audit ALL scripts/daemons touching Downloads
2. Review: User validates list is complete
3. Refine: Add any missed touchpoints
4. Finalize: Agree on fix approach for each
5. Execute: Update all touchpoints simultaneously

---

## Cascade's Responsibility:

When user requests complex change:
1. Recognize it needs protocol
2. State: "This needs full planning protocol"
3. Generate comprehensive brainstorm
4. Wait for user review before executing

---

## User's Responsibility:

- Review brainstorms thoroughly
- Ask questions about unclear items
- Validate assumptions
- Approve before execution

---

**This protocol prevents the "fix one thing, break another" cycle.**
