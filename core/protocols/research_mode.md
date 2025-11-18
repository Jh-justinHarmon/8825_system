# Research Mode Protocol

**Created:** 2025-11-12  
**Purpose:** Constraint-based exploration using only existing tools/workflows

---

## Core Principle

**Research Mode = Suggest existing solutions only. No new code.**

When user activates Research Mode, you operate under strict constraints:
- Use only tools/workflows that already exist
- No code blocks generated
- No new implementations
- Focus on what's available now

---

## Operating Rules

### 1. Suggest Existing Tools Only

**When asked to solve something:**
- Search for existing tools/workflows/patterns
- Reference what's already built
- Show how to combine existing pieces
- Point to documentation/examples

**Do NOT:**
- Write new code
- Create new workflows
- Implement new features
- Generate code blocks

### 2. Gap Identification

**If tool/workflow doesn't exist:**

State what's needed in 1-2 sentences:
```
Missing: [Tool Name]
Purpose: [Brief description in 1-2 sentences]
```

Then show the flow:
```
ASK > [Existing Tool] > [New Tool Needed] > RESULT
```

**Example:**
```
Missing: Health Data Aggregator
Purpose: Combines blood pressure, weight, and activity data into unified timeline view.

Flow:
ASK > Load records.json > [Health Data Aggregator] > Unified timeline
```

### 3. Workflow Assessment

**Can deliver with existing tools + 1 missing piece:**
- Name the missing piece
- Show the flow with gap identified
- Reference existing tools that get you 90% there

**Missing numerous steps:**
- State: "Numerous steps missing to deliver on this promise. New or Adjusted Workflow would be needed."
- Do NOT elaborate on what those steps are
- Do NOT suggest building them

### 4. No Code Blocks

**Never generate:**
- Code examples
- Implementation snippets
- Configuration files
- Script samples

**Instead reference:**
- Existing files by path
- Documented patterns
- Built workflows
- Available tools

---

## Response Format

### Pattern 1: Existing Solution Available

```
Research Mode: Existing Solution

Tool: [Name]
Location: [Path]
Usage: [How to use it]
Documentation: [Path to docs]

This solves your request using existing infrastructure.
```

### Pattern 2: One Missing Piece

```
Research Mode: Gap Identified

Existing Tools:
- [Tool 1]: [What it does]
- [Tool 2]: [What it does]

Missing: [Tool Name]
Purpose: [1-2 sentence description]

Flow:
ASK > [Tool 1] > [Tool 2] > [Missing Tool] > RESULT

Gap: Single tool needed to complete workflow.
```

### Pattern 3: Multiple Missing Pieces

```
Research Mode: Workflow Not Available

Current State: [What exists]
Request: [What you asked for]

Assessment: Numerous steps missing to deliver on this promise. New or Adjusted Workflow would be needed.
```

---

## Examples

### Example 1: Existing Solution

**User:** "How do I ingest customer health data?"

**Research Mode Response:**
```
Research Mode: Existing Solution

Tool: Customer Platform Core
Location: 8825_customers/lib/core.js
Function: ingest(customer_id, data, options)
Documentation: 8825_customers/README.md

Usage:
1. Load keys via smart_loader.sh (auto-loads in terminal)
2. Call core.ingest() with customer ID and data
3. System uses LLM router for intelligent extraction
4. Data stored in customer/records.json

This solves your request using existing infrastructure.
```

### Example 2: One Missing Piece

**User:** "Can I get a weekly health summary for a customer?"

**Research Mode Response:**
```
Research Mode: Gap Identified

Existing Tools:
- core.query(): Retrieves customer data with LLM analysis
- records.json: Stores all ingested health data
- LLM Router: Handles intelligent summarization

Missing: Weekly Summary Generator
Purpose: Aggregates records by week and generates comparative analysis across time periods.

Flow:
ASK > Load records.json > [Weekly Summary Generator] > LLM Router > Weekly report

Gap: Single tool needed to complete workflow.
```

### Example 3: Multiple Missing Pieces

**User:** "Can I build a predictive health model that forecasts issues?"

**Research Mode Response:**
```
Research Mode: Workflow Not Available

Current State: Customer platform ingests and queries health data using LLM intelligence.
Request: Predictive modeling with forecasting capabilities.

Assessment: Numerous steps missing to deliver on this promise. New or Adjusted Workflow would be needed.
```

---

## Tool Inventory Reference

### Available Now

**Customer Platform:**
- `core.ingest()` - Ingest customer data
- `core.query()` - Query customer context
- `core.analyze()` - Analyze customer data
- LLM Router - 3-tier intelligence routing
- JSON storage - Simple file-based storage

**API Key Management:**
- `smart_loader.sh` - Auto-load keys from Keychain/LastPass/Vault
- `setup_keys.sh` - Interactive key setup
- `scan_for_keys.sh` - Security scanner
- `cleanup_exposed_keys.sh` - Automated cleanup

**Documentation:**
- README files across all projects
- SETUP guides for major systems
- Troubleshooting docs
- Architecture docs

**Workflows:**
- Located in `.windsurf/workflows/`
- Accessible via slash commands
- Documented procedures

### How to Check What Exists

**Before responding in Research Mode:**
1. Search existing tools in project directories
2. Check `.windsurf/workflows/` for documented workflows
3. Review README files for available functions
4. Reference memory for known patterns

**If unsure:**
- Use grep_search to find existing implementations
- Use find_by_name to locate relevant files
- Use read_file to verify tool capabilities

---

## Activation

**User triggers Research Mode by saying:**
- "Research Mode"
- "What tools do we have for..."
- "Can we do this with existing tools..."

**Stay in Research Mode until:**
- User explicitly exits ("Exit Research Mode")
- User requests implementation ("Build this")
- User asks for code examples

---

## Benefits

**Why Research Mode:**
1. **Prevents Over-Engineering** - Use what exists before building new
2. **Faster Answers** - No implementation time, just reference existing
3. **Discovers Existing Solutions** - Often tools already exist
4. **Clear Gap Identification** - Know exactly what's missing
5. **Avoids Code Clutter** - No unnecessary code generation

**When to Use:**
- Exploring capabilities
- Planning new features
- Assessing feasibility
- Understanding what's available
- Identifying gaps before building

---

## Anti-Patterns

### ❌ Don't Do This in Research Mode

**Generating Code:**
```javascript
// Here's how you could implement it:
function weeklyReport() { ... }
```

**Building New Workflows:**
```
Step 1: Create new script
Step 2: Add configuration
Step 3: Integrate with...
```

**Detailed Implementation Plans:**
```
To build this you'll need:
- Database schema changes
- New API endpoints
- Frontend components
- Background jobs
```

### ✅ Do This Instead

**Reference Existing:**
```
Tool: core.query()
Location: 8825_customers/lib/core.js
Handles: Customer data retrieval with LLM analysis
```

**Identify Gaps Simply:**
```
Missing: Weekly Report Generator
Purpose: Aggregates records by week for comparative analysis.
```

**Assess Feasibility:**
```
Assessment: Numerous steps missing. New workflow needed.
```

---

## Quality Checks

**Before responding in Research Mode, verify:**

1. ✅ No code blocks in response
2. ✅ Only referenced existing tools
3. ✅ Gaps identified in 1-2 sentences max
4. ✅ Flow diagram uses existing tools + gaps
5. ✅ No implementation details provided

**If any check fails:**
- Revise response
- Remove code/implementation details
- Focus on existing tools only

---

## Exit Research Mode

**User can exit by:**
- "Exit Research Mode"
- "Let's build [something]"
- "Show me the code"
- "Implement this"

**Upon exit:**
- Return to normal operation mode
- Can generate code blocks
- Can implement new features
- Can create workflows

---

## Summary

**Research Mode = Constraint-based exploration**

**Rules:**
1. Suggest existing tools only
2. No code blocks
3. Gaps in 1-2 sentences
4. Flow: ASK > Tool > [Gap] > Result
5. Multiple gaps = "New workflow needed"

**Purpose:**
- Use what exists first
- Identify gaps clearly
- Avoid over-engineering
- Fast feasibility assessment

**File:** `8825_core/protocols/research_mode.md`

---

**Activation:** User says "Research Mode"  
**Deactivation:** User says "Exit Research Mode" or requests implementation
