# Contributing to 8825 Core

Thank you for your interest in contributing to 8825 Core! This document provides guidelines for contributions.

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## How to Contribute

### Reporting Issues

- Check existing issues first to avoid duplicates
- Use the issue template when available
- Provide clear reproduction steps
- Include relevant system information

### Suggesting Features

- Open an issue with the "feature request" label
- Explain the use case and benefits
- Consider if it fits the framework philosophy (patterns, not implementations)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**
4. **Test thoroughly** (see Testing section)
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature`
7. **Open a Pull Request**

## Development Guidelines

### Code Style

**Python**:
- Follow PEP 8
- Use type hints where appropriate
- Document functions with docstrings
- Keep functions focused and small

**SQL**:
- Use uppercase for keywords
- Indent consistently
- Comment complex queries

**Markdown**:
- Use ATX-style headers (`#`)
- Keep lines under 120 characters
- Include code examples

### Testing

Before submitting:

```bash
# Test Python code compiles
find . -name "*.py" -exec python3 -m py_compile {} \;

# Run examples
cd core/library/examples
python demo_library.py

cd ../../tools/template_word_generator
python template_word_generator_v2.py examples/demo_template.docx examples/demo_content.json test_output.docx
```

### Documentation

- Update README.md if adding features
- Add examples with synthetic data only
- Document integration points
- Explain design decisions

## What We're Looking For

### High Priority

- 🎯 Additional handler examples for Universal Inbox
- 🎯 More library integration examples
- 🎯 Performance optimizations
- 🎯 Better error handling
- 🎯 Additional architecture docs

### Welcome Contributions

- Bug fixes
- Documentation improvements
- Example implementations
- Test coverage
- Performance benchmarks

### Not Accepting

- Features that require proprietary data
- Implementations specific to one use case
- Breaking changes without discussion
- Code that violates privacy principles

## Framework Philosophy

8825 Core is a **framework, not an implementation**:

✅ **Do contribute**:
- Generic patterns and protocols
- Reusable utilities
- Architecture improvements
- Integration examples (synthetic data)

❌ **Don't contribute**:
- Specific implementations with real data
- Proprietary algorithms
- Client-specific code
- Personal configurations

## Review Process

1. **Automated checks** - CI runs safety scans and tests
2. **Maintainer review** - Code quality and alignment with philosophy
3. **Community feedback** - For significant changes
4. **Approval** - Requires 1+ maintainer approval
5. **Merge** - Squash and merge to main

## Security

- **Never commit** API keys, tokens, or secrets
- **Never commit** personal or client data
- **Always use** environment variables for sensitive config
- **Report vulnerabilities** privately to maintainers

## Questions?

- Open a discussion for general questions
- Tag maintainers for urgent issues
- Check existing docs and issues first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make 8825 Core better! 🎉
