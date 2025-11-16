---
description: Start collaborative dev cycle with structured research and planning
---

# Collaborative Dev Cycle

Triggers comprehensive ideation → research → planning → execution workflow.

## Trigger Phrases

Use any of these to start:
- `[collab]`
- `[collab sesh]`
- `[collab session]`
- `[LFG]`
- `[let's make]`
- "I have an idea to flush out"
- "want to figure something out"

## What This Does

Enters structured 6-phase cycle:

1. **Breadcrumb Collection** - Gathers all relevant protocols, patterns, philosophies
2. **Deep Dive** - Pulls additional context strings as needed
3. **Brainstorm & Analysis** - Applies PromptGen + Decision Matrix with teach-me explanations
4. **⏸️ PAUSE** - Stops for LLM switch to thinking model
5. **Detailed Plan** - Step-by-step execution with teach-me markers (💡🎯⚙️⚠️✅)
6. **Execution** - Clear instructions, test plan based on confidence level

## Protocol Used

// turbo
1. Execute collaborative cycle protocol
```bash
# Trigger the full collaborative development cycle
echo "🎯 COLLABORATIVE DEV CYCLE INITIATED"
echo ""
echo "📋 PHASE 1: Breadcrumb Collection"
echo "   Gathering protocols, patterns, and context..."
echo ""
echo "🔍 PHASE 2: Deep Dive"
echo "   Pulling additional context strings..."
echo ""
echo "🎨 PHASE 3: Brainstorm & Analysis"
echo "   Applying PromptGen + Decision Matrix..."
echo ""
echo "⏸️  PHASE 4: PAUSE for LLM switch"
echo ""
echo "📝 PHASE 5: Detailed Planning"
echo "   Creating step-by-step execution plan..."
echo ""
echo "⚡ PHASE 6: Execution"
echo "   Running implementation with test plan..."
```

See: `8825_core/protocols/COLLAB_CYCLE_PROTOCOL.md` for full details.

## Teaching Mode Markers

Watch for these emojis in responses:
- 💡 **TEACH ME** - Why we're doing this
- 🎯 **DECISION** - What we chose and why
- ⚙️ **IMPLEMENTATION** - How it works
- ⚠️ **GOTCHA** - Common mistakes to avoid
- ✅ **SUCCESS METRIC** - How to verify it worked

## Manual Override

Skip phases if needed:
- "Skip context, just brainstorm"
- "I already know the approach, go to planning"
- "Execute immediately" (skips to phase 6)
