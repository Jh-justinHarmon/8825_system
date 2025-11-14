# Core - System Essentials

**Purpose:** Universal system-level components used by everyone and everything.

## What Goes Here

### Characteristics
- Used across ALL focuses
- Required for system operation
- Stable and mature
- Well-documented
- Has tests

### Examples
- System startup/initialization
- Universal protocols
- Core utilities (logging, config, etc.)
- System-wide integrations
- Foundational pipelines

## Subdirectories

### `/pipelines`
System-wide data processing pipelines
- Ingestion engine
- Content processing
- Universal routing

### `/integrations`
External service integrations used system-wide
- Cloud services
- APIs
- Third-party tools

### `/protocols`
Universal protocols and standards
- Communication protocols
- Data formats
- System conventions

### `/utilities`
Helper scripts and tools
- System maintenance
- Health checks
- Logging utilities

## Promotion Criteria

To promote something to `core/`:
- [ ] Used by 2+ focuses OR critical for system
- [ ] Stable (no major changes in 30 days)
- [ ] Documented
- [ ] Has basic tests
- [ ] Reviewed and approved

## NOT in Core

- Focus-specific code → `focuses/`
- Cross-focus but not universal → `shared/`
- Experimental → `sandbox/`
- User-specific → `users/`
