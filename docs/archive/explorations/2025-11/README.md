# Joju Sandbox v1.1

**Focus:** Professional library management and profile curation  
**Version:** 1.1.0 (migrated from v1.0 with improvements)  
**Activation:** `focus on joju` (after `enter 8825 mode`)

---

## Overview

Joju Sandbox is a dedicated workspace for ingesting professional content, mining achievements, deduplicating information, and publishing to Joju-ready JSON format.

**Core Innovation:** Library-first workflow - master library updated FIRST, variations are curated views.

---

## Current State

- **Master Library:** `JH_master_library.json` (Rev 12, 79 achievements)
- **Variations:** 6 (BASE, CREATIVITY, TECHNICAL_PM, DESIGN_LEADERSHIP, ENTREPRENEURSHIP, UX_FOCUSED)
- **Sessions:** 10 completed
- **Last Updated:** 2025-11-05

---

## Folder Structure

```
joju_sandbox/
├── README.md                        # This file
│
├── raw/                             # Raw ingested files (PDFs, DOCX, etc.)
├── web/                             # Web-scraped content
├── pasted/                          # Direct paste content
├── scanned/                         # Folder scan results
├── api/                             # API-retrieved data
│
├── mined/                           # Mined structured achievements
├── deduped/                         # Deduplication analysis reports
├── analysis/                        # Gap analysis and insights
│
├── curations/                       # Working variations
│   ├── justin_harmon_joju_CREATIVITY.json
│   ├── justin_harmon_joju_TECHNICAL_PM.json
│   ├── justin_harmon_joju_DESIGN_LEADERSHIP.json
│   ├── justin_harmon_joju_ENTREPRENEURSHIP.json
│   ├── justin_harmon_joju_UX_FOCUSED.json
│   └── VARIATIONS_SUMMARY.md
│
├── output/                          # Final outputs
│   ├── joju_upload_ready.json       # Ready for Joju upload
│   ├── library_update_report.md     # Library changes
│   └── publish_report.md            # Publishing summary
│
├── backups/                         # Library backups
├── archives/                        # Completed session archives
└── logs/                            # Process logs
```

---

## Workflow

### Library-First Process

```
1. Extract → Mine achievements from source
2. Merge to Library → Auto-dedup at library level (>80% similarity)
3. Present Changes → Show new/enriched achievements
4. Update Variations → Pull from library, apply framing
5. Version → Create versioned copies
```

### Commands

- `focus on joju` - Enter Joju Focus
- `upload [file]` - Ingest file
- `scrape [url]` - Web ingestion
- `paste [content]` - Direct content
- `scan [folder]` - Folder scanning
- `publish joju` - Generate upload-ready JSON
- `exit focus` - Return to 8825 mode

---

## Variations

### BASE
- **Profession:** Product Designer / Industrial Designer / UX Leader
- **Website:** prtclinc.com
- **Emphasis:** Design craft + business outcomes (60/40)

### CREATIVITY
- **Profession:** Creative Technologist / Product Designer / Artist
- **Website:** justin-harmon.art
- **Emphasis:** Innovation + artistic expression

### TECHNICAL_PM
- **Profession:** Product Manager / Technical Product Leader
- **Website:** prtclinc.com
- **Emphasis:** Metrics + technical execution

### DESIGN_LEADERSHIP
- **Profession:** Design Leader / Creative Director
- **Emphasis:** Team building + mentorship

### ENTREPRENEURSHIP
- **Profession:** Entrepreneur / Founder
- **Emphasis:** Business building + innovation

### UX_FOCUSED
- **Profession:** UX Strategist / User Researcher
- **Emphasis:** Research + user-centered design

---

## Exit Protocol

Before leaving Joju Focus:

1. ✓ Verify library updated
2. ✓ Verify variations synced
3. ✓ Verify versioning complete
4. ✓ Verify session log updated
5. ✓ Verify files saved
6. ✓ Validate JSON

---

## Protocols

- **Full Protocol:** `/protocols/8825_joju_mode`
- **Focus Protocol:** `/protocols/8825_joju_focus.json`
- **Curation Agent:** `/protocols/8825_joju_curation_agent`
- **Library-First Mining:** `/protocols/joju_library_first_mining`

---

## v1.1 Improvements

### Added
- Multi-user support (JH, MG, CW)
- Workspace awareness (precise paths)
- Jarvis-76 personality
- Adaptive learning prompts

### Optimized
- Clearer folder structure
- Better documentation
- Streamlined workflows
- Enhanced exit protocol

### Maintained
- Library-first workflow
- Auto-dedup (>80%)
- 6 variations
- Session logging
