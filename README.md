# 8825 Core: An Open Knowledge OS

8825 is a framework for building AI-assisted productivity systems with clear knowledge layer separation.

## What is 8825?

8825 provides:
- **Layered Architecture** - Clear separation of experiments, production, and core
- **Protocol System** - Proven workflows for AI-assisted development
- **Knowledge Layer Separation** - L0 (public) / L1 (personal) / L2 (internal)
- **DLI Routing** - Smart routing between web/LLM and internal knowledge
- **Universal Inbox** - Unified ingestion pattern for all file types
- **Brain Transport** - State synchronization across AI sessions

## Quick Start

```bash
git clone https://github.com/yourusername/8825-core.git
cd 8825-core
./scripts/setup.sh
```

## Documentation

- [DLI Routing Protocol](core/protocols/DLI_ROUTING_PROTOCOL.md) - When to use DLI vs web/LLM
- [Architecture Guide](core/architecture/ARCHITECTURE.md) - System design
- [Workflows](core/architecture/WORKFLOWS.md) - Operational guide
- [All Protocols](core/protocols/) - Complete protocol list

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
