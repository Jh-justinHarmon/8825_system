# 8825 System - Architecture Documentation

**Version:** 3.1 (Layered Architecture)  
**Last Updated:** November 13, 2025

---

## 🏗️ System Overview

8825 is a unified personal knowledge management and automation system built on a **layered, promotion-based architecture**.

### Design Principles

1. **Layered Promotion** - Code graduates from sandbox → shared → core
2. **Clear Boundaries** - Each layer has specific criteria
3. **No Duplicates** - One canonical location for each resource
4. **Findable** - Clear hierarchy makes everything easy to locate
5. **Version-Agnostic Paths** - No version numbers in folder names
6. **Maintainability** - Clear structure, good documentation, automated promotion

---

## 📊 Layered Architecture

```
┌────────────────────────────────────────────────────────┐
│                     8825 System                        │
└────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬──────────┐
        │                 │                 │          │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐  ┌──▼──┐
   │  CORE   │      │ SHARED  │      │ FOCUSES │  │USERS│
   │  (L4)   │      │  (L3)   │      │  (L2)   │  │(L1) │
   └────┬────┘      └────┬────┘      └────┬────┘  └──┬──┘
        │                │                │          │
   ┌────▼────────────────▼────────────────▼──────────▼───┐
   │              SANDBOX (L0)                            │
   │         experimental → graduated                     │
   └──────────────────────────────────────────────────────┘
```

### Layer Definitions

**L0 - Sandbox:** Experiments, POCs, development  
**L1 - Users:** User-specific data and workflows  
**L2 - Focuses:** Focus-specific production code  
**L3 - Shared:** Cross-focus production resources  
**L4 - Core:** Universal system essentials  

### Promotion Flow

```
Everything starts in sandbox/experimental/
    ↓ (stable, tested)
sandbox/graduated/
    ↓ (decision point)
    ├─→ focuses/{name}/  (if focus-specific)
    ├─→ shared/          (if multi-focus)
    └─→ core/            (if universal/essential)
```

---

## 🗂️ Directory Structure

### Root Level

```
8825-system/
├── core/               # L4: System essentials (everyone uses)
├── focuses/            # Focus-specific workspaces (symlinks)
├── users/              # User-specific data
├── INBOX_HUB/          # Inbox automation
├── Documents/          # Generated outputs
└── [Config files]      # System configuration
```

### Core System (`8825_core/`)

```
8825_core/
├── agents/             # AI agents and tools
│   ├── agent_registry.json
│   └── AGENT_INDEX.md
│
├── integrations/       # External service integrations
│   ├── google/         # Drive, Gmail, Calendar, Vision
│   ├── notion/         # (via focuses)
│   ├── figjam/         # Sticky note processing
│   ├── dropbox/        # File sync
│   ├── goose/          # Goose MCP bridge
│   └── mcp/            # MCP server framework
│
├── inbox/              # Inbox processing pipeline
│   ├── ingestion_engine.py
│   ├── classifier.py
│   └── config/
│
├── workflows/          # Automated workflows
│   ├── meeting_summary_pipeline.py
│   ├── analyze_user_testing.py
│   └── extract_all_tasks.py
│
├── protocols/          # System protocols
│   └── PARTNER_CREDIT_README.md
│
└── projects/           # Project configurations
    ├── 8825_00-general.json
    ├── 8825_76-joju.json
    └── 8825_00-hcss.json
```

### Focuses (`focuses/`)

```
focuses/
├── joju/               # Joju product focus
│   ├── tasks/          # Task management
│   ├── user_engagement/# User feedback
│   └── mcp_server/     # Joju MCP server
│
├── hcss/               # HCSS client focus
│   ├── workflows/
│   └── automation/
│
└── [user]/jh_assistant/# Personal assistant
    └── poc/
```

---

## 🔄 Data Flow

### Inbox Processing Flow

```
┌──────────────┐
│  iCloud      │
│  Downloads   │
└──────┬───────┘
       │ Sync
       ▼
┌──────────────┐
│ Local        │
│ Downloads    │
└──────┬───────┘
       │ Process
       ▼
┌──────────────┐
│ Classifier   │
│ (ML/Rules)   │
└──────┬───────┘
       │ Route
       ├─────────────┬─────────────┐
       ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Joju    │  │  HCSS    │  │    JH    │
│  Focus   │  │  Focus   │  │ Assistant│
└──────────┘  └──────────┘  └──────────┘
```

### Task Management Flow

```
┌──────────────┐
│    Goose     │
│  (Natural    │
│  Language)   │
└──────┬───────┘
       │ MCP Protocol
       ▼
┌──────────────┐
│ MCP Bridge   │
│ (Python)     │
└──────┬───────┘
       │ Call
       ▼
┌──────────────┐
│ Task Layer   │
│ (Python)     │
└──────┬───────┘
       │ API
       ▼
┌──────────────┐
│   Notion     │
│   Database   │
└──────────────┘
```

### User Engagement Flow

```
┌──────────────┐
│ User Testing │
│  Sessions    │
└──────┬───────┘
       │ Extract
       ▼
┌──────────────┐
│  Insights    │
│  (JSON)      │
└──────┬───────┘
       │ Analyze
       ▼
┌──────────────┐
│  Dashboard   │
│  (HTML)      │
└──────┬───────┘
       │ Query via Goose
       ▼
┌──────────────┐
│ Task Creation│
└──────────────┘
```

---

## 🔌 Integration Architecture

### MCP Server Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AI Assistants                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Goose   │  │  Claude  │  │  Cline   │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼─────────────┼─────────────┼────────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │ MCP Protocol (stdio/JSON-RPC)
        ┌─────────────▼─────────────┐
        │     MCP Bridge Layer      │
        │  ┌─────────────────────┐  │
        │  │  Joju MCP (8827)    │  │
        │  │  HCSS MCP (8826)    │  │
        │  │  JH MCP (8828)      │  │
        │  └─────────────────────┘  │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │      Service Layer        │
        │  ┌─────────────────────┐  │
        │  │  Task Management    │  │
        │  │  User Engagement    │  │
        │  │  System Operations  │  │
        │  └─────────────────────┘  │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │    External Services      │
        │  ┌─────────────────────┐  │
        │  │  Notion API         │  │
        │  │  Google APIs        │  │
        │  │  Dropbox API        │  │
        │  └─────────────────────┘  │
        └───────────────────────────┘
```

### Focus Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Focus (e.g., Joju)                │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │    Tasks     │  │    User      │  │   MCP    │ │
│  │  Management  │  │  Engagement  │  │  Server  │ │
│  └──────┬───────┘  └──────┬───────┘  └────┬─────┘ │
│         │                 │                │       │
│         └─────────────────┼────────────────┘       │
│                           │                        │
│  ┌────────────────────────▼──────────────────────┐ │
│  │           Focus Data Layer                    │ │
│  │  • Local cache                                │ │
│  │  • Configuration                              │ │
│  │  • Logs                                       │ │
│  └───────────────────────────────────────────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

### Credential Management

```
┌─────────────────────────────────────────────────────┐
│              Credential Isolation                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Focus Layer (e.g., joju/tasks/)             │  │
│  │  • config.json (Notion API key)              │  │
│  │  • .gitignore (prevents commits)             │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Integration Layer (e.g., google/)           │  │
│  │  • credentials.json (Service account)        │  │
│  │  • .gitignore (prevents commits)             │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  MCP Bridge                                   │  │
│  │  • NO credentials stored                     │  │
│  │  • Calls service layers                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Access Control

```
┌─────────────────────────────────────────────────────┐
│              Access Control Layers                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Layer 1: MCP Authentication                        │
│  • User list in CONFIG                              │
│  • Per-request validation                           │
│                                                      │
│  Layer 2: Service Authentication                    │
│  • API keys for external services                   │
│  • OAuth tokens where applicable                    │
│                                                      │
│  Layer 3: Focus Isolation                           │
│  • Each focus has own credentials                   │
│  • No cross-focus access                            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 📈 Scalability

### Horizontal Scaling (Focuses)

```
┌─────────────────────────────────────────────────────┐
│                   8825 Core                          │
│              (Shared Infrastructure)                 │
└─────────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬─────────────┐
        │             │             │             │
   ┌────▼────┐   ┌───▼────┐   ┌───▼────┐   ┌───▼────┐
   │  Joju   │   │  HCSS  │   │   JH   │   │  New   │
   │  Focus  │   │ Focus  │   │ Focus  │   │ Focus  │
   └─────────┘   └────────┘   └────────┘   └────────┘
   
   Each focus:
   • Independent data
   • Own MCP server
   • Own credentials
   • Own workflows
```

### Vertical Scaling (Within Focus)

```
┌─────────────────────────────────────────────────────┐
│                    Joju Focus                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │    Tasks     │  │    User      │  │   New    │ │
│  │  (Existing)  │  │  Engagement  │  │ Feature  │ │
│  └──────────────┘  │  (Existing)  │  │  (Add)   │ │
│                    └──────────────┘  └──────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 State Management

### Task State

```
┌─────────────────────────────────────────────────────┐
│              Task State Management                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Source of Truth: Notion Database                   │
│                                                      │
│  Local Cache: focuses/joju/tasks/local/tasks.json  │
│  • Updated on sync                                   │
│  • Read for queries                                  │
│  • Invalidated on write                              │
│                                                      │
│  Sync Strategy:                                      │
│  • Pull: Notion → Local cache                       │
│  • Push: Local → Notion                             │
│  • Conflict: Notion wins                             │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### User Engagement State

```
┌─────────────────────────────────────────────────────┐
│         User Engagement State Management             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Source: focuses/joju/user_engagement/              │
│                                                      │
│  Structure:                                          │
│  • sessions/ - Raw session data                     │
│  • insights/ - Extracted insights                   │
│  • all_user_testing_data.json - Aggregated         │
│                                                      │
│  Update Strategy:                                    │
│  • Manual: Add new sessions                         │
│  • Automated: Extract insights                      │
│  • Regenerate: Dashboard on demand                  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Performance Considerations

### Caching Strategy

```
┌─────────────────────────────────────────────────────┐
│                  Caching Layers                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  L1: In-Memory Cache                                │
│  • Python objects                                    │
│  • Lifetime: Request duration                        │
│                                                      │
│  L2: Local File Cache                               │
│  • JSON files                                        │
│  • Lifetime: Until sync                              │
│                                                      │
│  L3: External Service                               │
│  • Notion, Google, etc.                             │
│  • Lifetime: Persistent                              │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Optimization Points

1. **Task Queries** - Use local cache (< 1s)
2. **Task Creation** - Direct to Notion (2-3s)
3. **Feedback Queries** - Local JSON (< 1s)
4. **Inbox Processing** - Batch operations (30-60s)

---

## 🔍 Monitoring & Observability

### Logging Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Logging System                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Component Logs:                                     │
│  • MCP Bridge: mcp-bridge/logs/                     │
│  • Inbox: 8825_core/inbox/logs/                     │
│  • Workflows: INBOX_HUB/logs/                       │
│                                                      │
│  Log Format:                                         │
│  YYYY-MM-DD HH:MM:SS - NAME - LEVEL - MESSAGE      │
│                                                      │
│  Log Levels:                                         │
│  • DEBUG: Detailed information                       │
│  • INFO: General information                         │
│  • WARNING: Warning messages                         │
│  • ERROR: Error messages                             │
│  • CRITICAL: Critical failures                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Metrics

```
Key Metrics:
• Task operations/hour
• API response times
• Error rates
• Cache hit rates
• Sync success rates
```

---

## 🔄 Deployment Architecture

### Development

```
Local Machine
├── Code changes
├── Local testing
└── Git commit
```

### Production

```
Production Environment
├── Auto-start MCPs (LaunchAgent)
├── Hourly inbox processing (LaunchAgent)
└── Manual workflows (on-demand)
```

---

## 🎯 Design Patterns

### 1. Focus Pattern
**Problem:** Need isolated workspaces  
**Solution:** Symlinked focuses with independent data

### 2. MCP Bridge Pattern
**Problem:** AI assistants need tool access  
**Solution:** MCP protocol servers per focus

### 3. Layer Pattern
**Problem:** Credential isolation  
**Solution:** Service layers with no credential sharing

### 4. Cache Pattern
**Problem:** API rate limits  
**Solution:** Local cache with sync strategy

---

## 📚 Technology Stack

### Languages
- **Python 3.7+** - Core system, workflows
- **JavaScript/Node.js** - Legacy MCP (deprecated)
- **Bash** - Automation scripts
- **HTML/CSS/JS** - Dashboards

### Frameworks
- **Flask** - MCP servers
- **Notion SDK** - Notion integration
- **Google APIs** - Google services

### Storage
- **JSON** - Configuration, cache
- **Markdown** - Documentation
- **Notion** - Task database

### Infrastructure
- **macOS** - Development/production
- **LaunchAgent** - Automation
- **Dropbox** - File sync

---

## 🔮 Future Architecture

### Planned Enhancements

1. **Database Layer**
   - SQLite for local data
   - Better query performance
   - Transaction support

2. **API Gateway**
   - Unified API endpoint
   - Rate limiting
   - Authentication

3. **Event System**
   - Pub/sub for events
   - Real-time updates
   - Webhook support

4. **Plugin System**
   - Dynamic tool loading
   - Third-party extensions
   - Marketplace

---

**Version:** 3.0  
**Last Updated:** November 10, 2025  
**Maintained By:** 8825 Architecture Team
