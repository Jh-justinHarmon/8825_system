# Template Word Generator

Generate styled Word documents from JSON or Markdown content using a template as a style guide.

## Features

- ✅ Generate Word documents from JSON or Markdown
- ✅ Preserve template styling (headers, footers, margins)
- ✅ Support for headings, paragraphs, lists, and tables
- ✅ Automatic style fallbacks for missing styles
- ✅ Clean, professional output

## Installation

```bash
pip install python-docx
```

## Usage

### From JSON

```bash
python template_word_generator_v2.py template.docx content.json output.docx
```

### From Markdown

```bash
python template_word_generator_v2.py template.docx content.md output.docx --text
```

## JSON Structure

```json
{
  "title": "Document Title",
  "sections": [
    {
      "heading": "Section Heading",
      "level": 1,
      "paragraphs": ["Paragraph text here"],
      "bullets": ["Bullet point 1", "Bullet point 2"],
      "numbered": ["Step 1", "Step 2"],
      "table": {
        "rows": [
          ["Header 1", "Header 2"],
          ["Data 1", "Data 2"]
        ],
        "style": "Light Grid Accent 1",
        "header": true
      }
    }
  ]
}
```

## Markdown Support

Supports standard Markdown syntax:
- Headings: `#`, `##`, `###`
- Bullets: `-`, `*`
- Numbered lists: `1.`, `2.`
- Code blocks: ` ``` `
- Paragraphs

## Examples

See `examples/` directory for:
- `demo_template.docx` - Sample template
- `demo_content.json` - Structured content example
- `demo_content.md` - Markdown content example

## How It Works

1. Creates a blank document
2. Copies header/footer from template (branding)
3. Copies page setup/margins from template
4. Adds your content with template styles
5. Falls back to standard styles if template styles missing

## API Reference

### TemplateWordGenerator

```python
from template_word_generator_v2 import TemplateWordGenerator

# Initialize
generator = TemplateWordGenerator('template.docx')

# Generate from JSON
generator.generate_from_dict(content_dict, 'output.docx')

# Generate from Markdown
generator.generate_from_text(markdown_text, 'output.docx')
```

## Troubleshooting

**Missing styles**: The generator automatically falls back to standard styles (List Bullet, List Number) if template styles are missing.

**Template not loading**: Ensure template is a valid `.docx` file. `.dotx` files need to be saved as `.docx` first.

**Margins not preserved**: Check that template has explicit margin settings. Zero margins are preserved intentionally.

## License

MIT

## Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- Examples use synthetic data only
- Documentation is updated
- Tests pass
