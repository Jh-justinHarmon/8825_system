# 8825 Core - AI-Assisted Knowledge Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-green.svg)]()

**8825 Core** is an open-source framework for building AI-assisted productivity systems with persistent memory, intelligent routing, and cost-optimized LLM usage.

## 🎯 What is 8825?

8825 is a layered architecture for AI-powered knowledge work that reduces LLM costs by 95% while maintaining quality through intelligent routing and pattern matching.

### Key Features

- 🧠 **Library System** - SQLite-based knowledge management (knowledge, decisions, patterns)
- 🎯 **DLI Routing** - Three-tier routing (Pattern → Cheap → Expensive) for 95% cost savings
- 📥 **Universal Inbox** - Single entry point for all file types with smart routing
- 📝 **Template Generator** - Generate styled Word documents from JSON/Markdown
- 🔍 **Pattern Engine** - FREE pattern matching before expensive LLM calls
- 📊 **Telemetry** - Track every LLM call, cost, and routing decision

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/8825-core.git
cd 8825-core

# Initialize a library
cd core/library
sqlite3 my_library.db < schema/init_library_db.sql
python examples/demo_library.py

# Try the template generator
cd ../../tools/template_word_generator
python template_word_generator_v2.py examples/demo_template.docx examples/demo_content.json output.docx
```

## 📚 Architecture

### Layered Design

- **L0 (Foundation)**: Protocols, patterns, and core concepts
- **L1 (Intelligence)**: DLI routing, pattern matching, context management
- **L2 (Application)**: Your focus-specific implementations (not in this repo)

### What's Included

✅ **Framework** - Reusable patterns and protocols  
✅ **Schema** - Database structures and models  
✅ **Examples** - Working demos with synthetic data  
✅ **Documentation** - Architecture and integration guides  

❌ **Not Included** - Your data, trained models, or proprietary implementations

## 💡 Core Concepts

### DLI (Deep Learning Intelligence) Routing

Traditional approach: Every query → Expensive LLM → High cost

**8825 approach**: Three-tier routing
1. **Tier 0**: Pattern matching (FREE) - 60-80% of queries
2. **Tier 1**: Cheap model analysis ($0.0001) - Simple queries
3. **Tier 2**: Expensive model ($0.0046) - Complex reasoning only

**Result**: 95% cost reduction with same quality

See `core/architecture/DLI_ARCHITECTURE.md` for details.

### Library System

SQLite-based knowledge management for:
- **Knowledge** - Facts, concepts, learnings
- **Decisions** - Choices made and rationale
- **Patterns** - Reusable solutions
- **Achievements** - Milestones and wins

See `core/library/README.md` for usage.

### Universal Inbox

Single entry point for all file types:
```
~/inbox/ → Classify → Route → Process → Store
```

Supports: PDF, DOCX, TXT, MD, images, audio, code, and more.

See `tools/universal_inbox/README.md` for pattern orchestration

## Use Cases

- Knowledge management systems
- AI agent orchestration
- Development workflow automation
- Multi-project coordination

## What's Not Included

This is the framework. To use it, you'll need:
- Your own knowledge index
- Focus-specific implementations
- Integration with your tools

See [examples/](examples/) for tutorials on building your own.

## License

MIT (see LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
