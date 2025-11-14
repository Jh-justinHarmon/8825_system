# Focuses - Focus-Specific Workspaces

**Purpose:** Each focus has its own workspace for focus-specific code, knowledge, and projects.

---

## Active Focuses

### 1. HCSS (Hammond, Cook, Schmieder & Simpson)
**Path:** `focuses/hcss/`  
**Purpose:** Client automation and workflows

**Contents:**
- `knowledge/` - HCSS-specific documentation
- `projects/` - HCSS project work
- `workflows/` - HCSS workflow documentation
- `user_data@` - Symlink to user-specific HCSS data

### 2. Joju
**Path:** `focuses/joju/`  
**Purpose:** Joju app development and user engagement

**Contents:**
- `tasks/` - Joju task management
- `user_engagement/` - User engagement workflows
- `reddit_monitoring/` - Reddit community monitoring
- `standups/` - Standup notes
- `user_testing/` - Testing documentation
- Brand and technical docs
- `user_data@` - Symlink to user-specific Joju data

### 3. JH Assistant
**Path:** `focuses/jh_assistant/`  
**Purpose:** Personal assistant workflows

**Contents:**
- `knowledge/` - Assistant-specific knowledge
- `projects/` - Assistant projects
- `user_data@` - Symlink to user-specific assistant data

### 4. Team76
**Path:** `focuses/team76/`  
**Purpose:** Team76 platform work

**Contents:**
- `features/` - Feature development

---

## What Belongs in Focuses

### ✅ Keep in Focus:
- Focus-specific workflows
- Focus-specific knowledge/documentation
- Focus-specific projects
- Focus-specific integrations
- Client-specific code

### ❌ Move to Shared:
- Code used by 2+ focuses
- Reusable automations
- Cross-focus templates
- Shared libraries

### ❌ Move to Core:
- System-essential code
- Universal integrations
- Required by all focuses

---

## What Was Promoted

### From Focuses to Shared:
**TGIF Automation** - `focuses/hcss/poc/tgif_automation/` → `shared/automations/tgif/`
- **Reason:** Production automation with multi-focus potential
- **Date:** 2025-11-13
- **Duplicates removed:** 2 other copies deleted

---

## Focus Structure

Each focus should have:
```
{focus_name}/
├── README.md          (focus overview)
├── knowledge/         (focus-specific docs)
├── projects/          (active projects)
├── workflows/         (how things work)
└── user_data@         (symlink to users/{user}/{focus})
```

---

## Adding a New Focus

1. Create directory: `focuses/{focus_name}/`
2. Create subdirectories: `knowledge/`, `projects/`, `workflows/`
3. Create README.md
4. Create user_data symlink: `ln -s ../../users/justin_harmon/{focus_name} user_data`
5. Add to this README

---

## Maintenance

### Monthly Review:
- [ ] Check for cross-focus duplication
- [ ] Identify items that should be promoted to shared/
- [ ] Archive completed projects
- [ ] Update focus READMEs

### When to Promote to Shared:
- Item used by 2+ focuses
- Clear reuse potential
- Stable and documented
- Has maintainer

---

**Focuses are for focus-specific work. Cross-focus items belong in `shared/`.**
