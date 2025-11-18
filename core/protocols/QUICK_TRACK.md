# Quick Protocol Tracking Reference

**Copy-paste these commands during work:**

---

## Record Usage (Most Common)

```bash
# Success
./track_protocol.py PROTOCOL_NAME --success --context "Brief description"

# Failure
./track_protocol.py PROTOCOL_NAME --fail --context "Why it didn't work"
```

---

## Common Protocols

```bash
# Deep Dive Research
./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --success --context "What you researched"

# Context First
./track_protocol.py CONTEXT_FIRST_PROTOCOL --success --context "What you built"

# Workflow Orchestration
./track_protocol.py WORKFLOW_ORCHESTRATION_PROTOCOL --success --context "What workflow"

# Learning Fundamentals
./track_protocol.py LEARNING_FUNDAMENTALS_PROTOCOL --success --context "What you learned"

# Decision Matrix
./track_protocol.py DECISION_MATRIX_PROTOCOL --success --context "What decision"

# Definition of Done
./track_protocol.py definition_of_done --success --context "What you completed"

# Task Classification
./track_protocol.py TASK_CLASSIFICATION_PROTOCOL --success --context "What you classified"
```

---

## Quick Views

```bash
# List all
./track_protocol.py --list

# Show report
./track_protocol.py --report

# Show promoted only
./track_protocol.py --list --status promoted

# Show decaying (need attention)
./track_protocol.py --list --status decaying
```

---

## Tips

1. **Track immediately** - Right after using protocol
2. **Be honest** - Mark failures too
3. **Add context** - Helps understand patterns
4. **Review weekly** - Check what's working

---

## Proof Protocol Status

- ✨ **Promoted** - 3+ uses, 70%+ success
- ✅ **Active** - Used recently, decent success
- ⏳ **Decaying** - Not used in 30+ days
- ❌ **Deprecated** - Not used in 90+ days OR low success
- 🆕 **Unused** - Never tracked
