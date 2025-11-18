# Learning System Evolution Protocol

**Purpose:** Define how 8825 turns raw learnings into philosophy, protocols, patterns, workflows, or MCPs — and what must **never** be auto-promoted.

---

## 1. Scope

This protocol governs:
- How `*~learning` and related files are classified.
- When a learning can become a **protocol**, **pattern**, **workflow**, **MCP**, or **philosophy update**.
- Guardrails to prevent user-specific, test, or operational artifacts from polluting core protocols.

It does **not** redefine individual domain protocols; it defines **how those protocols evolve.**

---

## 2. Classification Rules (High Level)

Given a learning file L, the system should:

- **Philosophy / Case Study**
  - If L describes *why* we do something, trade-offs, values, or principles.
  - If L is heavily user-specific (e.g., a single user’s learning profile).

- **Protocol**
  - If L defines a repeatable, critical path that must be followed.
  - Contains formal steps, compliance requirements, or safety constraints.

- **Pattern**
  - If L describes reusable structures or templates.
  - Often includes code examples or repeated structures.

- **Workflow / MCP**
  - If L describes multi-step automations, agents, or MCP servers.

- **Doc Only**
  - If L is historical, exploratory, or primarily narrative with no reusable structure.

---

## 3. Hard Exclusions for Protocol Promotion

The learning integration system **must not** treat the following as protocol candidates:

1. **User Profile Data**
   - Paths: `users/*/profile/*`
   - Rationale: User data is input to teaching systems, not global governance.
   - Action: Integrate into philosophy as anonymized case studies only.

2. **Test Artifacts**
   - Paths containing `/testing/`.
   - Filenames like `*_COMPLETE.md`.
   - Rationale: Tests confirm behavior; they are not the behavior specification.
   - Action: Use as evidence when updating protocols, never as protocols directly.

3. **Operational Reports & Telemetry**
   - Paths containing `/workflows/` and `/reports/`.
   - Filenames like `*_report_*.json` or `*_metadata.json`.
   - Rationale: Reports capture one run’s state, not cross-run rules.

4. **Backups and Temporary Artifacts**
   - Any path or filename containing `.backup`.
   - Rationale: Backups are safety nets, not sources of truth.

5. **Existing Protocol Files**
   - Paths starting with `8825_core/protocols/`.
   - Rationale: Prevent "protocol → protocol" cloning (e.g., `X_protocol.md` → `X_protocol_protocol.md`).
   - Action: If there is genuine meta-learning about protocols, route it here or to `meta_learning_patterns.md`.

These rules are enforced in `learning_integration/learning_processor.py` via `_should_exclude_from_protocols`.

---

## 4. Promotion Workflow (Human-in-the-Loop)

1. **Candidate Identification**
   - LearningProcessor tags candidates for philosophy, protocol, pattern, workflow, or MCP.
   - Guardrails prevent obviously invalid protocol candidates.

2. **Human Review**
   - A human reviews:
     - Novelty: Is this genuinely new?
     - Scope: Does it apply across projects/users?
     - Risk: Does elevating this create hidden coupling or overfitting?

3. **Destination Selection**
   - If mostly **values/principles** → Philosophy.
   - If **must-follow process** → Protocol.
   - If **reusable structure** → Pattern.
   - If **multi-step automation** → Workflow or MCP.
   - If **user-specific** → Case study only.

4. **Implementation & Cross-References**
   - Update the chosen doc (philosophy/protocol/pattern/etc.).
   - Cross-link:
     - Source learning file path.
     - Related philosophies and protocols.

5. **Cleanup**
   - Once integrated, mark the learning as safe to delete.
   - Rely on integration reports to provide filenames safe for cleanup.

---

## 5. Meta-Learning Storage

To keep the system understandable:

- **Meta patterns** live in:
  - `patterns/meta_learning_patterns.md`

- **This protocol** (`learning_system_evolution.md`) governs how protocols and philosophies are updated.

- Domain-specific details (OCR, DLI, MCP development, etc.) stay in their respective protocols and workflows.

---

## 6. Review & Evolution

- This protocol should be revisited when:
  - The learning integration system adds new categories.
  - We see new classes of misclassification.
  - The cost/benefit of human review vs automation changes.

- Changes to this protocol should be:
  - Logged in a short changelog at the bottom of this file.
  - Propagated to `learning_processor.py` and related workflows.

---

## Changelog

- **2025-11-17:** Initial version created after misclassified profile/test/report learnings surfaced as protocol candidates.
