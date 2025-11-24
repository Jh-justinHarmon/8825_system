# 8825 Open Source Policy

**Version**: 1.0.0  
**Effective Date**: 2025-11-24  
**Last Updated**: 2025-11-24

---

## Purpose

This document defines what components of the 8825 system are open source (public) versus proprietary (private). It serves as the canonical reference for all OSS evaluation decisions.

---

## Core Principles

1. **Framework, Not Implementation**: We open source the patterns, protocols, and architecture. Specific implementations with client data or competitive advantage remain closed.
2. **Safety First**: When in doubt, keep it closed. We can always open source later, but we cannot undo a leak.
3. **Generic Examples Only**: Any code examples in OSS must use synthetic data and generic naming (no client names, no personal details).
4. **Continuous Evaluation**: Every production-ready component must go through OSS evaluation before being marked complete.

---

## Open Source (Public in `oss/`)

### Core Framework
- ✅ Layered architecture documentation (L0/L1/L2)
- ✅ Protocol system (all protocol documents, scrubbed)
- ✅ Workflow patterns and guides
- ✅ Architecture diagrams and design docs

### Library System
- ✅ Database schema (`init_library_db.sql`)
- ✅ Generic engine code (CRUD operations, search)
- ✅ Type definitions and models
- ✅ CLI interface (generic, no personal data)
- ✅ Integration guides and examples
- ❌ Actual `library.db` with real data
- ❌ Migration logs with personal content
- ❌ User-specific configurations

### Intelligence & Routing
- ✅ DLI routing protocol and architecture docs
- ✅ Three-tier routing pattern (Tier 0/1/2)
- ✅ Telemetry schema and architecture
- ✅ PPM (Prompt Pattern Memory) schema and docs
- ✅ Reference DLI MCP implementation (toy example)
- ❌ Production DLI router with tuned heuristics
- ❌ Actual PPM patterns database
- ❌ Cost optimization logic
- ❌ Trained Pattern Engine index (29K+ entities)

### Tools & Utilities
- ✅ Universal Inbox pattern (generic file watcher)
- ✅ OCR MCP (tesseract-only, no Google Vision)
- ✅ Template Word Generator (v2, generic templates only)
- ✅ Goose background worker pattern (generic shell)
- ✅ Learning integration workflow (pattern docs only)
- ❌ HCSS-specific automations
- ❌ Joju-specific pipelines
- ❌ Client-branded templates
- ❌ Personal configurations

### Examples & Tutorials
- ✅ Demo library setup with synthetic data
- ✅ Sample focus structure (empty template)
- ✅ Tutorial on building a custom focus
- ✅ Example MCP server implementations

---

## Proprietary (Private in `8825-Jh`)

### Client Work
- ❌ HCSS automations and workflows
- ❌ TGIF meeting systems
- ❌ Any client-specific configurations
- ❌ RAL, LHL, or other client projects

### Personal & User Data
- ❌ `/users/justin_harmon/**` (except templates)
- ❌ Personal email, calendar, contacts
- ❌ Real library entries with personal content
- ❌ Personal knowledge base entries

### Competitive Advantages
- ❌ Clinical Scribe agent (code and prompts)
- ❌ Production-tuned DLI router
- ❌ Trained indexes and pattern databases
- ❌ Cost optimization heuristics
- ❌ Client-specific integrations

### Infrastructure & Credentials
- ❌ API keys, tokens, secrets
- ❌ Production MCP configurations
- ❌ Deployment scripts with real paths
- ❌ Backup databases with real data

---

## OSS Evaluation Checklist

For each component being evaluated for open source:

### 1. Classification
- [ ] Is this Core Framework, Library, Intelligence, Tool, or Example?
- [ ] Does it provide unique competitive advantage?
- [ ] Is it client-specific or personal?

### 2. Safety Checks
- [ ] No hardcoded paths (`/Users/justinharmon`, Dropbox paths)
- [ ] No client identifiers (HCSS, TGIF, RAL, LHL, etc.)
- [ ] No personal emails or contact info
- [ ] No API keys, tokens, or secrets
- [ ] No real user data or content

### 3. Dependency Analysis
- [ ] All imports reference OSS-safe modules
- [ ] No runtime dependencies on proprietary components
- [ ] Configuration files are generic
- [ ] Environment variables are documented

### 4. Documentation Quality
- [ ] README exists and is complete
- [ ] Examples use synthetic data only
- [ ] Installation instructions are tested
- [ ] Architecture is explained clearly

### 5. Testing
- [ ] Unit tests exist and pass
- [ ] Integration tests use mock data
- [ ] No tests depend on private resources
- [ ] CI pipeline is defined

---

## Approval Process

1. **Self-Evaluation**: Developer runs `scripts/oss_evaluate.sh [path]`
2. **Automated Checks**: Script validates safety criteria
3. **Manual Review**: Check against this policy document
4. **Documentation**: Update OSS_MIGRATION_LOG.md
5. **Migration**: Run `scripts/promote_to_oss.sh [path] [dest]`
6. **Verification**: Test in isolated `oss/` directory
7. **Publish**: Push to public repo via `scripts/publish_oss.sh`

---

## Exceptions & Gray Areas

### Case-by-Case Decisions
Some components may require special consideration:

- **Joju-related code**: Keep closed until we determine if Joju becomes a separate product
- **Clinical Scribe**: Keep closed; competitive advantage
- **Advanced MCP servers**: Evaluate individually based on value vs risk

### When Uncertain
Default to **keeping it private**. We can always publish later after:
- More scrubbing
- More genericization  
- More documentation
- Legal/IP review

---

## Maintenance

- Review this policy quarterly
- Update after major system changes
- Document exceptions in OSS_MIGRATION_LOG.md
- Refine automated checks based on edge cases

---

## Questions?

For questions about OSS policy:
1. Check this document first
2. Review existing decisions in OSS_MIGRATION_LOG.md
3. When in doubt, err on the side of privacy

---

**Remember**: It's easier to open source later than to undo a leak.
