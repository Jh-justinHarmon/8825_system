# Shared - Cross-Focus Resources

**Purpose:** Production code/resources used by multiple focuses but not system-critical.

## What Goes Here

### Characteristics
- Used by 2+ focuses
- Production-ready
- Not system-essential (focuses could work without it)
- Graduated from sandbox
- Maintained

### Examples
- Multi-focus automations (TGIF)
- Shared templates
- Common libraries
- Cross-focus workflows

## Subdirectories

### `/automations`
Workflows and automation used across focuses
- Email processing
- Meeting automation
- Shared pipelines

### `/templates`
Reusable templates
- Document templates
- Code templates
- Workflow templates

### `/libraries`
Shared code libraries
- Common functions
- Utilities
- Helpers

## Promotion Path

```
sandbox/experimental → sandbox/graduated → shared → (if becomes universal) → core
```

## Promotion Criteria

To move something to `shared/`:
- [ ] Used by 2+ focuses
- [ ] Stable (14+ days without major changes)
- [ ] Documented (basic README)
- [ ] Has an owner/maintainer
- [ ] Graduated from sandbox

## Examples in Shared

**TGIF Automation:**
- Started in `focuses/hcss/poc/tgif_automation/`
- Needed by HCSS and future focuses
- Graduated to `shared/automations/tgif/`

**Email Templates:**
- Used across multiple focuses
- Lives in `shared/templates/email/`

## NOT in Shared

- Single focus only → `focuses/{name}/`
- System-critical → `core/`
- Experimental → `sandbox/`
- User-specific → `users/`
