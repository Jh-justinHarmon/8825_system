# Workflow Protocols - Quick Start Guide

**Version:** 3.2.0  
**Date:** 2025-11-13

---

## 🚀 For Users

### First Time Here?
Read this 3-minute guide to understand how to work most effectively with 8825.

### The Problem These Solve
You've probably experienced:
- Starting to build something, then realizing you need to rebuild it for actual use
- Spending 30 minutes building from scratch, then finding it already existed
- Getting stuck because you jumped in without understanding the scope
- Teaching moments that didn't stick because wrong format

**These protocols prevent all that.**

---

## 📊 Quick Decision Tree

```
Got a task?
    ↓
One-time thing? ──Yes──> Just do it (skip protocols)
    ↓ No
Multiple steps or users? ──Yes──> Use protocols (keep reading)
```

---

## 🎯 The 3-Question Method

Before starting any multi-step task, ask yourself:

### 1. "What am I building?"
- One-off task → Do it, minimal docs
- Repeatable workflow → Document steps
- Pipeline → Full protocols
- For other users → Definitely use protocols

**Read:** `TASK_CLASSIFICATION_PROTOCOL.md`

### 2. "Does this already exist?"
- Search before building
- 2 minutes now saves 20 minutes later

**Read:** `CONTEXT_FIRST_PROTOCOL.md`

### 3. "Who am I optimizing for?"
- Just me, right now → Fast and dirty is fine
- Future me or others → Make it easy to use

**Read:** `DECISION_MATRIX_PROTOCOL.md`

---

## 🤖 For AI (Cascade)

### Default Behavior (Unless User Says "Skip Protocols")

**When user presents task:**
```
1. Quick classify (30 seconds)
   "This looks like a [Pipeline]. I'll search for context first."

2. Context search (appropriate depth)
   One-off: 30s, Workflow: 2min, Pipeline: 5-10min

3. If Pipeline/Agent/Protocol:
   "Let me run through PromptGen methodology (3 min)"
   
4. Present findings + plan
   "Found [X, Y, Z]. Here's the plan: [comprehensive]"

5. Execute with periodic updates

6. After completion:
   "This works for now. Want to make it repeatable?"
   
7. If repeatable:
   Run through Definition of Done checklist
```

**Full process:** `WORKFLOW_ORCHESTRATION_PROTOCOL.md`

---

## 📚 Protocol Cheat Sheet

| Protocol | Use When | Time | Saves |
|----------|----------|------|-------|
| **Orchestration** | Every task | 0s (auto) | Prevents all pitfalls |
| **Classification** | User presents task | 30s | 30-60 min rework |
| **Context-First** | Before executing | 30s-10min | 20-120 min reinventing |
| **Decision Matrix** | After classifying | 10s | 15-30 min wrong approach |
| **PromptGen** | Pipelines/agents | 3-5min | 2+ hours of rework |
| **Learning** | Teaching moments | varies | Better comprehension |

---

## 💡 Real Examples

### Example 1: "Process this meeting transcript" (One-Off)
```
Classify: One-off task
Context: Quick check (30s)
Mode: Results-driven
PromptGen: Skip
Execute: Use pandoc or GPT-4
Done: Complete, no follow-up
Time: 2 minutes total
```

### Example 2: "Automate meeting processing" (Pipeline)
```
Classify: Pipeline (repeated, automated)
Context: Deep search (5min) → Found Gmail API, GPT-4 patterns
Mode: User-driven (will use repeatedly)
PromptGen: Full analysis (5min) → Found edge cases early
Execute: Build with error handling, monitoring
Completion: Make repeatable? Already is!
DoD: Check all 5 items
Time: 2 days, but handles 100+ meetings
```

### Example 3: "Fix this bug" (Depends)
```
Classify: If simple fix → One-off
         If systemic → Could be pattern/protocol
Context: Quick search for root cause
Mode: Results-driven (fix now) unless affects users
PromptGen: Skip unless needs design change
Execute: Fix with appropriate scope
Time: 5 min to 2 hours depending on scope
```

---

## 🚩 Red Flags (Protocol Would Have Helped)

You're hitting a wall if:
- "Wait, I need to do this again next week" → Should have classified as Workflow
- "Didn't we build something like this?" → Should have done context search
- "Why is this so hard to use?" → Should have chosen user-driven mode
- "This keeps breaking" → Should have used PromptGen for edge cases
- "I don't understand this" → Should have matched learning style
- "Wait, this isn't actually done" → Should have used DoD checklist

**Solution:** Stop, back up, use appropriate protocol

---

## ⚡ Common Patterns

### Pattern 1: "Quick Question" → Becomes Complex
```
User: "How do I X?"
AI: [Starts answering]
User: "And also Y"
User: "And handle Z"
User: "And for other users"

❌ Without protocols: Rework 3 times
✅ With protocols: 
   - Classify early: "Sounds like a pipeline, let me plan properly"
   - PromptGen: Capture all requirements upfront
   - Execute once, correctly
```

### Pattern 2: Evolution Path
```
Start: One-off task → Works!
Later: "Can we do this weekly?" → Workflow
Later: "Can this be automated?" → Pipeline
Later: "Can others use this?" → Agent

✅ Protocols make evolution smooth:
   - Each step prompts: "Make repeatable?"
   - Clear upgrade path
   - Documentation grows with complexity
```

### Pattern 3: Teaching Moment
```
User: "Walk me through this"
AI without protocols: Generic explanation
User: "I don't get it"

AI with protocols:
   - Check learning profile
   - Justin → Show working code, real examples, top-down
   - Deliver in right format
   - Track what works
User: "Oh, that makes sense!"
```

---

## 🎓 Learning Path

### Day 1: Awareness
- Know protocols exist
- Know when you're in protocol territory (complex tasks)
- Let AI guide you through them

### Week 1: Recognition
- Start recognizing task types
- Notice when context search would help
- Understand optimization targets

### Month 1: Internalized
- Automatically classify tasks
- Naturally search context
- Choose right mode instinctively
- Protocols become invisible (just good workflow)

---

## 🛠️ Customization

### Your Learning Profile
Start with Justin's profile, adapt as you learn:
- Track what teaching formats work for you
- Note when you felt confused vs clear
- Update `LEARNING_FUNDAMENTALS_PROTOCOL.md` with your preferences

### Your Decision Bias
Understand your default:
- Do you tend toward "fast and dirty" or "perfect and polished"?
- Protocols help balance your natural tendency
- Results-driven when appropriate, user-driven when needed

---

## 🎯 Success Metrics

### You're Using Protocols Well When:
- ✅ Less rework (build once, build right)
- ✅ Faster overall (even with upfront thinking)
- ✅ Better solutions (edge cases handled)
- ✅ Clearer communication (AI knows what you want)
- ✅ More confidence (comprehensive plans)

### You're Fighting Protocols When:
- ❌ "This is too much overhead"
- ❌ Spending more time planning than executing
- ❌ Using protocols for obvious tasks
- ❌ Rigidly following when user says skip

**Balance:** Use judgment. Protocols serve you, not vice versa.

---

## 🚀 Next Steps

1. **Read:** `WORKFLOW_ORCHESTRATION_PROTOCOL.md` (5 min)
2. **Try:** Next complex task, let AI guide you through protocols
3. **Notice:** How much smoother it is vs jumping straight in
4. **Customize:** Update learning profile as you discover preferences
5. **Evolve:** Protocols will feel natural after a few uses

---

## 📞 Quick Commands

Tell AI:
- `"Use protocols"` → Follow full workflow
- `"Skip protocols"` → One-off, just do it
- `"Classify this"` → Help me understand what I'm building
- `"Search context"` → What already exists?
- `"PromptGen"` → Run through methodology
- `"Teach me"` → Explain in my learning style

---

## 📖 Full Documentation

All protocols in: `8825-system/8825_core/protocols/`

- `README.md` - Protocol index
- `WORKFLOW_ORCHESTRATION_PROTOCOL.md` - Master flow
- `TASK_CLASSIFICATION_PROTOCOL.md` - Classify tasks
- `CONTEXT_FIRST_PROTOCOL.md` - Search first
- `DECISION_MATRIX_PROTOCOL.md` - Choose target
- `PROMPTGEN_INTEGRATION_PROTOCOL.md` - Structured brainstorming
- `LEARNING_FUNDAMENTALS_PROTOCOL.md` - Teaching styles

**Total:** ~15,000 lines of structured guidance

---

**Remember:** Protocols aren't bureaucracy. They're accumulated wisdom from real mistakes, compressed into repeatable process.

**5 minutes of protocol saves 50 minutes of rework.**
