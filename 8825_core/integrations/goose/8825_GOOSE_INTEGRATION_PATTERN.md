# 8825 → Goose Integration Pattern

**Date:** 2025-11-08  
**Source:** ChatGPT conversation  
**Status:** Pattern defined, ready to implement

---

## Core Concept

**Two-Layer Automation:**
1. **8825 (Brain)** - Context, routing, spec generation
2. **Goose (Arms & Legs)** - Local execution via MCP

---

## The Pattern

### Windsurf as Dry Lab
- Test and refine 8825 workflows
- Generate explicit task specs
- Validate logic before execution

### Goose as Execution Layer
- Receives explicit JSON task specs
- Acts on local files via MCP
- No schema inference - 8825 defines structure

---

## Task Spec Format

### Base Structure

```json
{
  "meta": {
    "source": "windsurf-8825",
    "project": "8825",
    "intent": "update_local_asset"
  },
  "task": {
    "name": "update_joju_library",
    "description": "Append new achievement objects mined from chat to the joju library on disk."
  },
  "io": {
    "workspace_root": "/Users/justinharmon/8825/projects",
    "target_file": "/Users/justinharmon/8825/projects/8825_76-joju.json",
    "backup": true
  },
  "steps": [
    {
      "id": "read-file",
      "action": "fs.read",
      "path": "/Users/justinharmon/8825/projects/8825_76-joju.json"
    },
    {
      "id": "merge-data",
      "action": "transform.merge",
      "strategy": "append_if_new",
      "source_field": "new_achievements",
      "target_field": "achievements"
    },
    {
      "id": "write-file",
      "action": "fs.write",
      "path": "/Users/justinharmon/8825/projects/8825_76-joju.json",
      "from_step": "merge-data"
    }
  ],
  "payload": {
    "new_achievements": [
      {
        "id": "joju-2025-11-07-001",
        "statement": "Documented 8825→Goose integration flow.",
        "evidence": ["chatlog:2025-11-07"]
      }
    ]
  }
}
```

---

## Guarded Version (Create If Missing)

```json
{
  "meta": {
    "source": "windsurf-8825",
    "project": "8825",
    "intent": "ensure_library_present_and_update"
  },
  "task": {
    "name": "ensure_joju_library_and_update",
    "description": "Check for joju library file; create with base schema if missing; then append new achievements."
  },
  "io": {
    "workspace_root": "/Users/justinharmon/8825/projects",
    "target_file": "/Users/justinharmon/8825/projects/8825_76-joju.json",
    "backup": true
  },
  "steps": [
    {
      "id": "check-file",
      "action": "fs.exists",
      "path": "/Users/justinharmon/8825/projects/8825_76-joju.json"
    },
    {
      "id": "create-if-missing",
      "action": "fs.write",
      "path": "/Users/justinharmon/8825/projects/8825_76-joju.json",
      "when": {
        "from_step": "check-file",
        "equals": false
      },
      "content": {
        "meta": {
          "schema": "joju-library-v1",
          "created_by": "8825",
          "created_at": "AUTO"
        },
        "achievements": []
      }
    },
    {
      "id": "read-file",
      "action": "fs.read",
      "path": "/Users/justinharmon/8825/projects/8825_76-joju.json"
    },
    {
      "id": "merge-data",
      "action": "transform.merge",
      "strategy": "append_if_new",
      "target_field": "achievements",
      "source_field": "new_achievements"
    },
    {
      "id": "write-file",
      "action": "fs.write",
      "path": "/Users/justinharmon/8825/projects/8825_76-joju.json",
      "from_step": "merge-data"
    }
  ],
  "payload": {
    "new_achievements": [
      {
        "id": "joju-2025-11-07-001",
        "statement": "Documented 8825→Goose integration flow.",
        "evidence": ["chatlog:2025-11-07"]
      }
    ]
  }
}
```

---

## Real-World Use Case: Scanned Letter Processing

### Flow

```
1. Detect new file in scan/upload folder
   ↓
2. Run OCR and produce raw_text
   ↓
3. Run 8825 context pass
   → Route to RAL/HCSS/JH based on text
   ↓
4. Run dedicated deadline extractor pass
   → Produce normalized dates
   ↓
5. Agent (Goose) creates calendar event(s)
   → For target recipient
   → Moves original scan to 'processed'
```

### Safety Rule

**If deadline language is relative** (e.g., "within 10 days"):
- Mark as `needs_human=true`
- Create draft event only
- Require human confirmation

---

## Key Principles

### 1. 8825 is the Brain
- Maintains context
- Defines structure
- Routes decisions
- Generates specs

### 2. Goose Gives It Arms & Legs
- Executes locally
- Accesses file system
- Writes to calendar
- Performs actions

### 3. Explicit Specs, No Inference
- 8825 defines exact schema
- Goose follows instructions
- No guessing structure
- Clear handoff contract

### 4. Windsurf as Dry Lab
- Test workflows first
- Refine before execution
- Validate logic
- Generate production specs

---

## Integration Points

### From Windsurf
1. User works with 8825 in Windsurf
2. 8825 generates task spec
3. Spec saved to handoff location
4. Goose picks up and executes

### From ChatGPT
1. User interacts with ChatGPT
2. ChatGPT calls MCP inbox server
3. File lands in pending
4. Windsurf processes via "fetch inbox"
5. 8825 generates task spec for Goose

---

## Highlights

- **Windsurf is a viable 'dry lab'** for testing and refining 8825 workflows before execution
- **Goose should receive explicit JSON task specs:** meta → task → io → steps → payload
- **8825 remains the source of truth** for structure; Goose should not infer schema
- **Scanned-letter flow:** scan → OCR → 8825 context pass → narrow deadline pass → calendar write
- **User intent:** Make 8825 the brain they already designed and let Goose give LLMs "arms and legs"

---

## Next Steps

1. **Build Goose MCP bridge** to accept 8825 task specs
2. **Define standard action vocabulary** (fs.read, fs.write, transform.merge, etc.)
3. **Create handoff folder** for spec exchange
4. **Test with scanned letter use case**
5. **Document patterns** as they emerge

---

## Status

**Pattern:** Defined ✅  
**Architecture:** Clear ✅  
**Use Case:** Validated ✅  
**Implementation:** Pending

**Next:** Build Goose MCP bridge for task spec execution
