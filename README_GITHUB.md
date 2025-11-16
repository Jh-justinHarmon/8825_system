# 8825 System

**AI-powered development system with adaptive learning, team coordination, and protocol-driven workflows.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active Development](https://img.shields.io/badge/status-active-green.svg)]()

---

## Overview

8825 is a comprehensive AI development system that learns your preferences, manages context across sessions, and provides protocol-driven workflows for consistent, high-quality output.

**Key Features:**
- 🧠 **Adaptive Learning** - System learns your preferences and adapts
- 🤝 **Team Coordination** - Multi-user collaboration support
- 📋 **Protocol System** - Reusable workflows and patterns
- 🔌 **MCP Integration** - Model Context Protocol servers
- 📚 **Content Indexing** - Semantic search across your codebase
- 🤖 **AI Manifests** - Normalize AI behavior across platforms

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Jh-justinHarmon/8825_system.git
cd 8825_system

# Run startup script
bash 8825_core/system/8825_unified_startup.sh
```

### Basic Usage

```bash
# Start the system
8825 start

# Check system health
8825 health

# View available focuses
list focuses

# Enter a focus
focus on joju
```

---

## Architecture

### Core Components

#### Brain System (`8825_core/brain/`)
- Adaptive learning engine
- Context management
- Memory system
- State tracking

#### Protocol System (`8825_core/protocols/`)
- Reusable workflows
- Decision frameworks
- Best practices
- Pattern library

#### MCP Servers (`8825_core/mcp_servers/`)
- AI Manifest Server - Normalize AI behavior
- Content Index Server - Semantic search
- Custom integrations

#### Focus System (`users/*/`)
- Project-specific contexts
- User preferences
- Learning profiles
- Work history

---

## Features

### Adaptive Learning
System observes your interactions and adapts:
- Learns your coding style
- Remembers your preferences
- Suggests relevant patterns
- Improves over time

### Protocol-Driven Workflows
Reusable protocols for common tasks:
- **Context-First Protocol** - Gather context before executing
- **Definition of Done** - Completion criteria
- **Workflow Orchestration** - Task classification and routing
- **Sentiment-Aware** - Adapt to user urgency

### AI Manifest System
Normalize AI behavior across platforms:
- Model-specific personality manifests
- Priority protocols per model
- Interaction style guidelines
- Strengths/weaknesses awareness

### Content Indexing
Semantic search across your codebase:
- Natural language queries
- Code understanding
- Pattern recognition
- Context retrieval

---

## Documentation

### Core Docs
- **[PHASE_0_COMPLETE_INVENTORY.md](PHASE_0_COMPLETE_INVENTORY.md)** - System inventory
- **[EXTRACTION_COMPLETE_SUMMARY.md](EXTRACTION_COMPLETE_SUMMARY.md)** - Open source extraction

### Protocols
- **[CONTEXT_FIRST_PROTOCOL.md](8825_core/protocols/CONTEXT_FIRST_PROTOCOL.md)** - Context gathering
- **[definition_of_done.md](8825_core/protocols/definition_of_done.md)** - Completion criteria
- **[WORKFLOW_ORCHESTRATION_PROTOCOL.md](8825_core/protocols/WORKFLOW_ORCHESTRATION_PROTOCOL.md)** - Task routing

### MCP Servers
- **[AI Manifest Server](8825_core/mcp_servers/ai_manifest_server/README.md)** - AI behavior normalization

---

## Project Structure

```
8825_system/
├── 8825_core/
│   ├── brain/              # Learning and coordination
│   ├── protocols/          # Reusable workflows
│   ├── mcp_servers/        # MCP integrations
│   ├── integrations/       # External services
│   └── system/             # Core system files
├── users/
│   └── justin_harmon/      # User-specific contexts
│       ├── joju/           # Joju focus
│       ├── jh_assistant/   # Personal assistant
│       └── profile.json    # User preferences
├── docs/                   # Documentation
└── .windsurf/              # Windsurf configuration
```

---

## Use Cases

### Software Development
- Context-aware code generation
- Pattern recognition and reuse
- Protocol-driven workflows
- Consistent code quality

### Team Collaboration
- Shared protocols and patterns
- Multi-user coordination
- Knowledge transfer
- Consistent practices

### Personal Assistant
- Task management
- Content organization
- Learning and adaptation
- Workflow automation

---

## Roadmap

### Current (v3.1)
- ✅ Core system architecture
- ✅ Protocol system
- ✅ MCP integrations
- ✅ AI Manifest system
- ✅ Content indexing

### Next (v3.2)
- [ ] Enhanced learning engine
- [ ] Multi-model orchestration
- [ ] Advanced team coordination
- [ ] Plugin system

### Future (v4.0)
- [ ] Distributed architecture
- [ ] Real-time collaboration
- [ ] Advanced analytics
- [ ] Enterprise features

---

## Contributing

Contributions are welcome! This is an open-source project.

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python3 -m pytest

# Start development server
bash 8825_core/system/8825_unified_startup.sh
```

### Guidelines
- Follow existing protocols
- Document new patterns
- Test thoroughly
- Update documentation

---

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

## Related Projects

- **[Forge Marketplace](https://github.com/Jh-justinHarmon/Forge)** - Token-based bounty marketplace
- **Joju** - Professional profile and achievement system
- **TrustyBits** - Parent organization

---

## Contact

**Built by:** TrustyBits / 8825 System  
**Maintainer:** Justin Harmon  
**Repository:** https://github.com/Jh-justinHarmon/8825_system  

---

## Status

**Version:** 3.1.0  
**Status:** ✅ Active Development  
**Last Updated:** November 14, 2025  

---

**Note:** This system is designed for developers and power users. Some features require configuration and setup.
