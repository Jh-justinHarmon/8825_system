# Joju Source Code - Full Dependency Analysis

**Generated:** 2025-11-10  
**Analysis Tool:** madge v8.0.0  
**Files Analyzed:** 123 TypeScript/TSX files  
**Circular Dependencies:** ✅ None found

---

## Executive Summary

**Architecture:** React 18 + TypeScript + Vite + Supabase  
**Component Count:** 123 files  
**Dependency Health:** ✅ Excellent (no circular dependencies)  
**Complexity:** Moderate (max depth: 14 imports from App.tsx)

### Key Metrics
- **Total files:** 123
- **Pages:** 10
- **Components:** 94
- **Services:** 2
- **Contexts:** 2
- **Hooks:** 2
- **UI Components (shadcn/ui):** 60+

---

## Architecture Overview

```
App.tsx (Entry Point)
├── Routing (React Router)
├── Theme Provider
├── Auth Context
├── CV Context
└── Pages (10)
    ├── Index
    ├── ProfilePage
    ├── ProfileEditPage
    ├── PublicProfilePage
    ├── LoginPage
    ├── AuthCallbackPage
    ├── ExportPreviewPage
    ├── ResumeReviewPage
    ├── PrivacyPolicyPage
    └── NotFound
```

---

## Dependency Tree Analysis

### Top-Level Dependencies (App.tsx → 14 imports)

**App.tsx** is the central hub importing:
1. `ProtectedRoute.tsx` - Route guards
2. `ThemeProvider.tsx` - Dark/light mode
3. `AuthContext.tsx` - Authentication state
4. `CVContext.tsx` - CV data management
5. 10 page components

### Most Connected Components

**By Import Count:**
1. **App.tsx** - 14 dependencies
2. **ProfileHeader.tsx** - 3 dependencies
3. **main.tsx** - 2 dependencies
4. **ContactSection.tsx** - 1 dependency
5. **DroppableColumn.tsx** - 1 dependency

**Most Imported (Leaf Nodes):**
- **CVView.tsx** - Used by 5 components
- **ThemeProvider.tsx** - Used by 2 components
- All other components: 0-1 imports

---

## Component Categories

### 1. Pages (10 files)
```
pages/
├── Index.tsx                  # Landing page
├── ProfilePage.tsx            # User profile view
├── ProfileEditPage.tsx        # Profile editing
├── PublicProfilePage.tsx      # Public-facing profile
├── LoginPage.tsx              # Authentication
├── AuthCallbackPage.tsx       # OAuth callback
├── ExportPreviewPage.tsx      # PDF export preview
├── ResumeReviewPage.tsx       # Resume review
├── PrivacyPolicyPage.tsx      # Privacy policy
└── NotFound.tsx               # 404 page
```

### 2. Core Components (40 files)
```
components/
├── Auth.tsx                   # Auth UI
├── ProtectedRoute.tsx         # Route protection
├── ThemeProvider.tsx          # Theme management
├── ThemeToggle.tsx            # Theme switcher
├── UserMenu.tsx               # User dropdown
├── ProfileHeader.tsx          # Profile header (3 deps)
├── ProfilePhotoModal.tsx      # Photo upload
├── CVView.tsx                 # CV display (imported by 5)
├── CVDocument.tsx             # CV document structure
├── StickyToolbar.tsx          # Floating toolbar
├── EnhancedStickyToolbar.tsx  # Enhanced toolbar
├── SlugSettings.tsx           # URL slug config
├── SectionTemplates.tsx       # Section templates
├── DroppableColumn.tsx        # Drag-drop column
├── SortableItem.tsx           # Sortable list item
└── AIProviderSelector.tsx     # AI provider selection
```

### 3. Section Components (14 files)
```
components/
├── ContactSection.tsx         # Contact info
├── SummarySection.tsx         # Professional summary
├── WorkExperienceSection.tsx  # Work history
├── EducationSection.tsx       # Education
├── ProjectsSection.tsx        # Projects
├── SideProjectsSection.tsx    # Side projects
├── SkillsSection.tsx          # Skills
├── LanguagesSection.tsx       # Languages
├── AwardsSection.tsx          # Awards
├── CertificationsSection.tsx  # Certifications
├── VolunteeringSection.tsx    # Volunteering
├── SpeakingSection.tsx        # Speaking engagements
├── WritingSection.tsx         # Publications
├── ExhibitionsSection.tsx     # Exhibitions
└── FeaturesSection.tsx        # Media features
```

### 4. Inline Editing Components (4 files)
```
components/
├── InlineEdit.tsx             # Generic inline editor
├── InlineDateEdit.tsx         # Date picker
├── InlineDropdownEdit.tsx     # Dropdown selector
└── InlineFileEdit.tsx         # File upload
```

### 5. UI Components (60+ shadcn/ui files)
```
components/ui/
├── accordion.tsx
├── alert-dialog.tsx
├── alert.tsx
├── aspect-ratio.tsx
├── avatar.tsx
├── badge.tsx
├── breadcrumb.tsx
├── button.tsx
├── calendar.tsx
├── card.tsx
├── carousel.tsx
├── chart.tsx
├── checkbox.tsx
├── collapsible.tsx
├── command.tsx
├── context-menu.tsx
├── date-picker.tsx
├── dialog.tsx
├── drawer.tsx
├── dropdown-menu.tsx
├── form.tsx
├── hover-card.tsx
├── image-carousel.tsx
├── image-grid.tsx
├── input-otp.tsx
├── input.tsx
├── label.tsx
├── list-item.tsx
├── matricks-background.tsx
├── menubar.tsx
├── navigation-menu.tsx
├── pagination.tsx
├── popover.tsx
├── progress.tsx
├── radio-group.tsx
├── reddit-icon.tsx
├── resizable.tsx
├── scroll-area.tsx
├── section-manager.tsx
├── select.tsx
├── separator.tsx
├── sheet.tsx
├── sidebar.tsx
├── skeleton.tsx
├── slider.tsx
├── sonner.tsx
├── switch.tsx
├── table.tsx
├── tabs.tsx
├── textarea.tsx
├── toast.tsx
├── toaster.tsx
├── toggle-group.tsx
├── toggle.tsx
├── toolbar-expandable.tsx
├── tooltip.tsx
└── use-toast.ts
```

### 6. Context & State (2 files)
```
context/
├── AuthContext.tsx            # Authentication state
└── CVContext.tsx              # CV data state
```

### 7. Services (2 files)
```
services/
├── profileService.ts          # Profile CRUD operations
└── storageService.ts          # File storage operations
```

### 8. Library & Utils (6 files)
```
lib/
├── supabase.ts                # Supabase client
├── utils.ts                   # Utility functions
├── cvDataProcessor.ts         # CV data processing
├── dateUtils.ts               # Date formatting
├── pdf.ts                     # PDF generation
└── sanitize.ts                # Input sanitization
```

### 9. Configuration (1 file)
```
config/
└── section-configs.ts         # Section configurations
```

### 10. Schemas (1 file)
```
schemas/
└── cvDataSchema.ts            # Zod validation schemas
```

### 11. Types (1 file)
```
types/
└── cv.ts                      # TypeScript type definitions
```

---

## Third-Party Dependencies

### Core Framework
- **react** ^18.3.1
- **react-dom** ^18.3.1
- **react-router-dom** ^6.26.2
- **vite** ^5.4.1
- **typescript** ^5.5.3

### UI Framework
- **@radix-ui/react-*** (20+ components)
- **lucide-react** ^0.462.0 (icons)
- **tailwindcss** ^3.4.11
- **next-themes** ^0.3.0

### Backend & Data
- **@supabase/supabase-js** ^2.58.0
- **@tanstack/react-query** ^5.56.2
- **zod** ^3.25.76 (validation)

### Features
- **@dnd-kit/*** (drag & drop)
- **react-hook-form** ^7.53.0
- **@react-pdf/renderer** ^4.3.0
- **openai** ^5.9.0
- **framer-motion** ^12.6.5

### Utilities
- **date-fns** ^3.6.0
- **dompurify** ^3.2.7
- **uuid** ^11.1.0
- **clsx** ^2.1.1

---

## Data Flow Architecture

### State Management Pattern

```
User Action
    ↓
Component Event Handler
    ↓
CVContext / AuthContext
    ↓
Service Layer (profileService, storageService)
    ↓
Supabase Client
    ↓
Database / Storage
```

### Key State Containers

**1. AuthContext**
- User authentication state
- Login/logout handlers
- Session management

**2. CVContext**
- CV data state
- CRUD operations
- Section management
- Export functionality

---

## Import Patterns

### Clean Architecture ✅

**No circular dependencies found** - This indicates:
- Well-structured component hierarchy
- Clear separation of concerns
- Proper abstraction layers
- Good architectural discipline

### Dependency Depth

**Shallow dependency tree:**
- Most components: 0-1 imports
- Mid-level components: 2-3 imports
- Top-level (App.tsx): 14 imports

This is **healthy** - indicates modular, reusable components.

---

## Supabase Integration

### Current Status (from SUPABASE_SETUP.md)

**Completed:**
- ✅ Supabase project created
- ✅ Authentication configured
- ✅ API keys obtained
- ✅ Environment variables set
- ✅ Supabase client installed

**In Progress:**
- ⏸️ Phase 0: Basic authentication
- ⏸️ Database tables
- ⏸️ Row-Level Security (RLS)
- ⏸️ Profile service
- ⏸️ Achievement service

### Database Schema (Planned)

**Tables:**
1. **profiles** - User profile data
2. **achievements** - User achievements (JSONB)
3. **cv_data** - CV content
4. **storage** - File uploads

**Services:**
- `profileService.ts` - Profile CRUD
- `storageService.ts` - File management

---

## Component Relationships

### High-Level Component Graph

```
App.tsx
├── AuthContext (wraps everything)
│   └── CVContext (wraps main content)
│       ├── ThemeProvider
│       │   └── Pages
│       │       ├── ProfilePage
│       │       │   ├── ProfileHeader (3 deps)
│       │       │   │   ├── CVView (imported by 5)
│       │       │   │   ├── InlineEdit
│       │       │   │   └── ProfilePhotoModal
│       │       │   ├── ContactSection → CVView
│       │       │   ├── SummarySection → CVView
│       │       │   ├── SkillsSection → CVView
│       │       │   └── LanguagesSection → CVView
│       │       ├── ProfileEditPage
│       │       │   └── DroppableColumn → SortableItem
│       │       ├── PublicProfilePage
│       │       ├── ExportPreviewPage
│       │       └── ... (other pages)
│       └── ProtectedRoute
└── Router
```

### Shared Components (Most Reused)

**CVView.tsx** - Imported by 5 components:
1. ContactSection
2. InlineEdit
3. LanguagesSection
4. ProfileHeader
5. SkillsSection
6. SummarySection

**ThemeProvider.tsx** - Imported by 2 components:
1. App.tsx
2. ThemeToggle.tsx

---

## File Size & Complexity

### Largest Files (by import count)

1. **App.tsx** - 14 imports (routing, contexts, pages)
2. **ProfileHeader.tsx** - 3 imports (view, edit, modal)
3. **main.tsx** - 2 imports (React, App)
4. **Section components** - 1 import each (CVView)
5. **UI components** - 0 imports (leaf nodes)

### Complexity Analysis

**Low Complexity:**
- UI components (shadcn/ui) - Pure presentational
- Section components - Simple data display
- Utility functions - Single responsibility

**Medium Complexity:**
- ProfileHeader - Multiple sub-components
- DroppableColumn - Drag & drop logic
- CVContext - State management

**High Complexity (likely):**
- App.tsx - Routing + context orchestration
- CVDataProcessor - Data transformation
- ProfileService - CRUD operations

---

## Integration Points

### External APIs

**Supabase:**
- Authentication (Auth.tsx, AuthContext.tsx)
- Database (profileService.ts)
- Storage (storageService.ts)

**OpenAI:**
- AI provider selector (AIProviderSelector.tsx)
- Likely used for resume enhancement/suggestions

**Vercel:**
- Deployment platform
- API routes (via /api folder)

---

## Recommendations for Matthew's 1:1

### 1. Achievements Component Integration

**Current State:**
- No `achievements` folder found in components
- No `AchievementsSection.tsx` component
- Achievement service planned but not implemented

**Integration Points:**
```
New: AchievementsSection.tsx
    ↓
CVView.tsx (already imported by 5 components)
    ↓
CVContext (state management)
    ↓
achievementService.ts (new)
    ↓
Supabase achievements table (JSONB)
```

**Estimated Effort:**
- Component creation: 2-4 hours
- Service layer: 2-3 hours
- Database schema: 1-2 hours
- Integration testing: 2-3 hours
- **Total: 7-12 hours**

### 2. Contributions Pipeline Integration

**Proposed Flow:**
```
External Source (Figma, GitHub, Dropbox)
    ↓
Integration Service (new)
    ↓
achievementService.ts
    ↓
Supabase achievements table (JSONB)
    ↓
CVContext (state update)
    ↓
AchievementsSection.tsx (display)
```

**New Files Needed:**
1. `services/achievementService.ts`
2. `services/integrationService.ts`
3. `components/AchievementsSection.tsx`
4. `components/IntegrationSettings.tsx`
5. `types/achievement.ts`

**Estimated Effort:**
- Services: 8-12 hours
- Components: 6-8 hours
- Database: 2-4 hours
- Testing: 4-6 hours
- **Total: 20-30 hours**

### 3. Architecture Strengths

**✅ Good for Integration:**
- Clean component hierarchy
- No circular dependencies
- Established service layer pattern
- Context-based state management
- Modular UI components

**⚠️ Considerations:**
- Achievement service doesn't exist yet
- Need to define JSONB schema
- Integration settings UI not built
- OAuth flows not implemented

### 4. Technical Debt

**None detected in dependency analysis:**
- ✅ No circular dependencies
- ✅ Clean import structure
- ✅ Proper separation of concerns
- ✅ Modern tech stack

---

## Next Steps for Contributions Feature

### Phase 1: Foundation (Week 1)
1. Define achievements JSONB schema
2. Create Supabase table
3. Build `achievementService.ts`
4. Create `AchievementsSection.tsx`

### Phase 2: Integration (Week 2-3)
5. Build `integrationService.ts`
6. Create integration settings UI
7. Implement OAuth flows
8. Add file scanning logic

### Phase 3: Testing (Week 4)
9. Unit tests for services
10. Integration tests
11. User acceptance testing
12. Performance optimization

---

## Dependency Graph Files

**Generated Files:**
- `dependency-graph.json` - Full import tree (168 lines)
- `dependency-graph.svg` - Visual graph (requires Graphviz)

**To generate visual graph:**
```bash
brew install graphviz
npx madge --image dependency-graph.svg --extensions ts,tsx src/
```

---

## Summary

**Architecture Quality:** ✅ Excellent  
**Dependency Health:** ✅ No circular dependencies  
**Integration Readiness:** ⚠️ Needs achievement service layer  
**Estimated Integration Time:** 20-30 hours for full contributions pipeline

**Key Insight:** The codebase is well-structured and ready for the contributions feature. The main gap is the achievement service layer and database schema, which needs to be built before integrations can be added.

---

**Analysis completed in ~10 minutes using automated tooling.**
