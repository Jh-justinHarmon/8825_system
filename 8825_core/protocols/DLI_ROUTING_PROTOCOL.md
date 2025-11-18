# DLI Routing Protocol

**Version:** 1.0.0  
**Created:** 2025-11-18  
**Status:** Active  
**Owner:** 8825 System Architecture

---

## 1. Purpose

This protocol defines **when and how** to use the DLI (Dual-Layer Intelligence) system via the Pattern Engine MCP server.

**Problem it solves:**
- Prevents over-reliance on DLI for questions answerable by web/LLM
- Prevents under-use of DLI for 8825-specific internal knowledge
- Keeps the Pattern Engine index lean but powerful
- Provides clear routing rules for AI agents (Windsurf/Cascade, Goose, etc.)

**Core principle:**  
DLI is not a replacement for general knowledge—it's a **specialized context engine** for 8825 internal systems and our opinionated integrations.

---

## 2. Knowledge Layers

Think of knowledge in three distinct layers:

### L0: Public / Generic Knowledge
**What:** Information any good LLM + web search can answer.

**Examples:**
- "How does Windsurf's built-in memory work?"
- "How do I use the OpenAI Python SDK?"
- "What does `git rebase` do?"
- "How do I write a Python context manager?"

**Source:** Model training data + `search_web` tool.

**DLI role:** None—skip DLI entirely.

---

### L1: Personal / Meta Preferences
**What:** Your personal workflows and preferences, but not encoded as 8825 system artifacts.

**Examples:**
- "I'm on macOS"
- "I dislike terminal friction; prefer auto-run"
- "We use Sonnet for most coding"
- "Default to Yellow (urgent) sentiment mode"

**Source:** Cascade's built-in memory system (global/user memories).

**DLI role:** None—these live in Cascade memories, not Pattern Engine.

---

### L2: 8825 Internal System Knowledge
**What:** Things that only exist because of the 8825 system and your files.

**Examples:**
- Joju task layer, meeting automation, downloads workflow
- Brain daemon architecture, MCP layout, INBOX_HUB protocols
- Focuses (joju/hcss/jh_assistant), TGIF pipeline, governance scripts
- Refactor plans, system version history, integration docs

**Source:** Pattern Engine index + DLI MCP (`mcp1_dli_deep_dive`).

**DLI role:** Primary source of truth.

---

## 3. DLI Roles

DLI operates in **two distinct modes**:

### Authority Mode
**When:** The answer lives entirely inside 8825.

**Behavior:** DLI is the **primary source of truth**. Use Pattern Engine first, optionally supplement with web/LLM for supporting details (e.g., explaining a library).

**Example:**  
Q: "How does our downloads workflow handle empty Otter transcripts?"  
→ DLI authority mode → finds `DOWNLOADS_WORKFLOW.md` → provides answer.

---

### Augmentor Mode
**When:** The primary answer is external/public, but 8825 has **our opinionated way** of doing it.

**Behavior:** Use web/LLM for the generic product explanation, then call DLI with a **narrow internal topic** to find our overlay (integration docs, constraints, preferences, gotchas).

**Example:**  
Q: "How should we configure Windsurf memories for 8825 mode?"  
→ Web search for Windsurf memory features (generic)  
→ DLI augmentor for "8825 Windsurf integration" (our setup)  
→ Merge both into final answer.

---

## 4. Query Classification

To route correctly, classify the query into one of three types:

### Internal Query
**Triggers:**
- Mentions 8825, focuses (joju/hcss/jh_assistant), brain, INBOX_HUB, TGIF, Pattern Engine, DLI, governance
- References specific internal files/paths (e.g., `8825_core/`, `focuses/`, `users/{user}/`)
- Phrases like "in our system", "in 8825 mode", "our workflow", "how we handle"
- Questions about internal components: inbox_server, brain daemon, BRAIN_TRANSPORT, meeting automation, downloads workflow

**Routing:** → **DLI Authority Mode**

---

### External Query
**Triggers:**
- Purely about vendor/tool/API with **no 8825 qualifier**
- Generic coding/technical questions
- Product documentation requests without integration context

**Routing:** → **Skip DLI** (use web/LLM only)

---

### Hybrid Query
**Triggers:**
- External tool/product + 8825 qualifier ("in our system", "for Joju", "in 8825 mode")
- Questions about **how we use** a tool (Windsurf, Notion, Otter, Figma Make, etc.)
- Integration questions ("how do we integrate X with Y")

**Routing:** → **Web/LLM + DLI Augmentor Mode**

**Special rule for known integrated tools:**  
If the query is about Windsurf, Notion, Otter, Figma Make, Dropbox, or other tools we've integrated, **default to Hybrid** even if "8825" isn't explicitly mentioned. It's safer to provide extra context than to miss it.

---

## 5. Routing Decision Table

| Query Type | DLI Role | Primary Source | Secondary Source | Cost Profile |
|------------|----------|----------------|------------------|--------------|
| **Internal** | Authority | DLI (Pattern Engine) | Web/LLM (optional) | Low ($0-0.02) |
| **External** | None | Web/LLM | None | Low (web only) |
| **Hybrid** | Augmentor | Web/LLM | DLI (narrow topic) | Medium ($0.01-0.03) |

**Trade-off acknowledgment:**  
Hybrid queries are the most expensive (two calls), but we accept this cost in exchange for higher-quality, context-aware answers.

---

## 6. Ingestion Guardrails

To keep the Pattern Engine index lean and valuable, follow these rules for what to index:

### ✅ DO Index (L2 Knowledge)

- **8825 architecture docs:** Core system design, component relationships, data flows
- **Workflows and protocols:** Repeatable processes, operational procedures
- **Integration docs:** "How we use X" notes (Windsurf, Notion, Otter, etc.)
- **Stable decisions:** Architecture decisions, constraints, patterns
- **Focus-specific content:** Joju, HCSS, JH Assistant docs and workflows
- **System configuration:** MCP setup, brain daemon config, startup scripts

**Test:** If I wiped 8825 tomorrow, could a random LLM still answer this?  
- No → Index it.

---

### ❌ DO NOT Index (L0 Knowledge)

- **Raw vendor docs:** Windsurf manual, Notion API reference, OpenAI docs
- **Generic tutorials:** "How to use Python", "Git basics", "React patterns"
- **Public API references:** Unless they contain our specific usage patterns
- **Ephemeral scratch notes:** Temporary experiments, one-off explorations

**Test:** Can I find this on the internet in 30 seconds?  
- Yes → Don't index it.

---

### 🤔 MAYBE Index (Context-Dependent)

- **Sandbox experiments:** If they become stable patterns, promote and index
- **External tool docs with our annotations:** If heavily customized for 8825, index the overlay
- **Historical decisions:** If they inform current architecture, index; if obsolete, archive

---

## 7. Examples (Routing Decisions)

### Internal Queries (DLI Authority)

**1. "Do we have Joju specs saved?"**
- **Classification:** Internal (mentions Joju focus)
- **Routing:** DLI authority mode
- **Expected:** Search `focuses/joju/` for specs, task docs, brand story
- **Validate:** Response mentions specific files like `JOJU_BRAND_STORY.md`, `tasks/README.md`

**2. "How does our downloads workflow handle empty Otter transcripts?"**
- **Classification:** Internal (our workflow)
- **Routing:** DLI authority mode
- **Expected:** Find `DOWNLOADS_WORKFLOW.md` or meeting automation docs
- **Validate:** Response references export-to-txt workaround, Downloads folder scanning

**3. "Where is the TGIF automation configured?"**
- **Classification:** Internal (TGIF is internal pipeline)
- **Routing:** DLI authority mode
- **Expected:** Find `shared/automations/tgif/` or related scripts
- **Validate:** Response points to specific paths and config files

**4. "What's in the BRAIN_TRANSPORT file?"**
- **Classification:** Internal (BRAIN_TRANSPORT is 8825 artifact)
- **Routing:** DLI authority mode
- **Expected:** Find Documents path, key locations, structure
- **Validate:** Response shows `~/Documents/8825_BRAIN_TRANSPORT.json` details

**5. "How do we handle meeting automation for Gmail?"**
- **Classification:** Internal (our meeting automation)
- **Routing:** DLI authority mode
- **Expected:** Find `meeting_prep/` scripts, `process_meetings.py`
- **Validate:** Response references Gmail integration, Otter parsing, GPT-4 processing

---

### External Queries (Skip DLI)

**6. "How does git rebase work?"**
- **Classification:** External (generic Git question)
- **Routing:** Web/LLM only, no DLI
- **Expected:** Generic Git explanation
- **Validate:** No 8825-specific content, $0 DLI cost

**7. "What's the OpenAI Python SDK for embeddings?"**
- **Classification:** External (generic API usage)
- **Routing:** Web/LLM only
- **Expected:** Generic OpenAI SDK docs
- **Validate:** No internal context, web-based answer

**8. "How do I write a Python context manager?"**
- **Classification:** External (generic Python)
- **Routing:** Web/LLM only
- **Expected:** Generic Python tutorial
- **Validate:** No 8825 mention, pure language feature explanation

**9. "What's the Notion API for creating database entries?"**
- **Classification:** External (no 8825 qualifier)
- **Routing:** Web/LLM only
- **Expected:** Generic Notion API docs
- **Validate:** No internal integration details

**10. "How does Windsurf's Cascade feature work generally?"**
- **Classification:** External (explicitly "generally")
- **Routing:** Web/LLM only
- **Expected:** Generic Windsurf explanation
- **Validate:** No 8825-specific setup details

---

### Hybrid Queries (Web + DLI Augmentor)

**11. "How should we configure Windsurf memories for 8825 mode?"**
- **Classification:** Hybrid (Windsurf + "for 8825 mode")
- **Routing:** Web for Windsurf features + DLI for "8825 Windsurf integration"
- **Expected:** Generic Windsurf memory system + workspace paths, MCP config
- **Validate:** Both generic info AND 8825-specific details

**12. "How do we use Notion for Joju task management?"**
- **Classification:** Hybrid (Notion + "for Joju")
- **Routing:** Web for Notion + DLI for "Joju Notion integration"
- **Expected:** Generic Notion database features + `focuses/joju/tasks/` integration
- **Validate:** Both Notion API basics AND our task sync workflow

**13. "What's our pattern for storing Otter transcripts?"**
- **Classification:** Hybrid (Otter + "our pattern")
- **Routing:** Web for Otter + DLI for "downloads workflow transcripts"
- **Expected:** Otter.ai export features + our Downloads folder processing
- **Validate:** Both Otter info AND our specific workflow

**14. "How should we structure MCP servers in our 8825 setup?"**
- **Classification:** Hybrid (MCP + "our 8825 setup")
- **Routing:** Web for MCP spec + DLI for "8825 MCP centralization"
- **Expected:** Generic MCP server structure + our `~/mcp_servers/` pattern
- **Validate:** Both MCP protocol AND our architectural decision

**15. "How do we integrate Figma Make output into Joju?"**
- **Classification:** Hybrid (Figma Make + Joju integration)
- **Routing:** Web for Figma Make + DLI for "figma-make-transformer"
- **Expected:** Figma Make basics + our transformation pipeline
- **Validate:** Both Figma Make features AND our `figma-make-transformer/` scripts

---

## 8. Implementation for Agents

### For Windsurf/Cascade

**Step 1: Classify the query**
```
Is it about 8825 internals? → Internal
Is it purely external with no 8825 mention? → External
Is it about a tool we use + 8825 context? → Hybrid
Is it about a known integrated tool (Windsurf/Notion/Otter)? → Default to Hybrid
```

**Step 2: Choose routing**
```
Internal → Call mcp1_dli_deep_dive(topic="...", mode="pattern")
External → Use model + search_web, skip DLI
Hybrid → 
  1. Use model + search_web for generic answer
  2. Call mcp1_dli_deep_dive(topic="narrow internal topic", mode="pattern")
  3. Merge both sources
```

**Step 3: Execute**
```
Authority mode: DLI response is primary, supplement if needed
Augmentor mode: Web response is primary, DLI provides overlay context
```

---

### Query Phrasing for DLI

**Quality of results depends heavily on query phrasing.** The Pattern Engine works best with specific, contextual queries.

#### ✅ Good Query Patterns

**Include specific terms:**
- Component names: "brain sync daemon", "Pattern Engine", "INBOX_HUB"
- File names: "BRAIN_TRANSPORT", "DOWNLOADS_WORKFLOW.md", "8825_unified_startup.sh"
- Paths: "8825_core/protocols/", "focuses/joju/tasks/"

**Include context:**
- What you're trying to do: "automatic generation", "sync workflow", "configuration"
- Related systems: "Downloads folder processing", "Notion integration", "MCP setup"

**Be specific rather than generic:**
- ✅ "BRAIN_TRANSPORT automatic generation Documents location brain sync daemon"
- ❌ "BRAIN_TRANSPORT file structure location contents"

**Examples of effective queries:**
- "Joju Notion task board integration sync workflow"
- "downloads workflow empty Otter transcripts handling"
- "8825 Windsurf configuration MCP setup workspace"
- "Otter transcript storage pattern downloads folder processing workflow"

#### ❌ Poor Query Patterns

**Too generic:**
- "file structure" (too vague)
- "how does it work" (no specifics)
- "configuration" (which one?)

**Missing context:**
- "BRAIN_TRANSPORT" (what about it?)
- "downloads" (which workflow?)
- "Joju" (what aspect?)

**Vague terms:**
- "system stuff"
- "that thing"
- "the process"

#### Query Refinement Strategy

If DLI returns insufficient results:

1. **Add more specific terms** from the domain
2. **Include related component names**
3. **Add action verbs** (generation, processing, handling, integration)
4. **Reference file/folder names** if known

**Example refinement:**
- Initial: "BRAIN_TRANSPORT location" → 9 snippets, incomplete
- Refined: "BRAIN_TRANSPORT automatic generation Documents location brain sync daemon" → 23 snippets, complete

---

---

### For Other MCP Clients (Goose, etc.)

Same classification and routing logic applies. Use the appropriate MCP tool names for your client.

---

## 9. Maintenance

### When to Update This Protocol

- **New focus added:** Add to internal query triggers
- **New tool integrated:** Add to hybrid query examples
- **Routing errors observed:** Add clarifying examples
- **Index getting noisy:** Tighten ingestion guardrails

### Quarterly Review

1. Sample 20 random queries from recent sessions
2. Verify routing matches this protocol
3. Identify any systematic misrouting
4. Update examples or rules as needed

### Metrics to Track

- **DLI usage rate:** % of queries that call DLI
- **Routing accuracy:** % correctly classified
- **Cost efficiency:** Average cost per query type
- **Context quality:** User feedback on answer relevance

---

## 10. Related Documentation

- `8825_core/philosophy/dual_layer_intelligence.md` - DLI architecture overview
- `8825_core/intelligence/dli_router_mcp/` - DLI implementation
- `8825_core/testing/ai_comparison_test/pattern_engine/` - Pattern Engine details
- `8825_core/protocols/WORKFLOW_ORCHESTRATION_PROTOCOL.md` - Overall workflow guidance

---

**Version History:**
- v1.0.0 (2025-11-18): Initial protocol defining L0/L1/L2 layers, authority vs augmentor modes, routing rules, 15 examples, and query phrasing guidance. Tested with 95% success rate across 9 scenarios.
