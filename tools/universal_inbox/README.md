# Universal Inbox Pattern

A unified entry point for processing all file types in an AI-assisted workflow.

## Concept

Instead of multiple scattered input mechanisms, the Universal Inbox provides:
- **Single watch directory** - All files go to one place
- **Automatic classification** - Detect file type and purpose
- **Smart routing** - Send to appropriate handler
- **Extensible handlers** - Easy to add new file types

## Architecture

```
~/inbox/
  ↓
File Watcher (watches for new files)
  ↓
Classifier (determines file type & purpose)
  ↓
Router (sends to appropriate handler)
  ↓
Handlers:
  - PDF/Images → OCR → Library
  - Text/Markdown → Direct to Library
  - Code → Analysis → Library
  - Audio → Transcription → Library
  - Email → Parse → Library
```

## Quick Start

```bash
# Create inbox directory
mkdir -p ~/inbox

# Run the watcher
python file_watcher.py ~/inbox
```

## Usage

1. **Drop files in inbox**: `cp document.pdf ~/inbox/`
2. **Watcher detects** and classifies
3. **Router sends** to appropriate handler
4. **Handler processes** and stores result

## Example Implementation

See `examples/simple_inbox.py` for a minimal working example.

## File Classification

The classifier detects:
- **Document type**: PDF, DOCX, TXT, MD, etc.
- **Content type**: Meeting notes, research, code, etc.
- **Priority**: Urgent, normal, low
- **Routing hints**: Tags, keywords, metadata

## Handlers

Create custom handlers for your workflow:

```python
def handle_pdf(file_path):
    # OCR the PDF
    text = ocr_engine.extract(file_path)
    
    # Store in library
    library.insert(text, source=file_path)
    
    # Archive original
    archive(file_path)
```

## Integration Points

- **OCR MCP** - For PDF/image processing
- **Library** - For knowledge storage
- **DLI Router** - For intelligent analysis
- **Notification system** - For alerts

## Benefits

- ✅ Single entry point (no scattered inputs)
- ✅ Automatic processing (no manual routing)
- ✅ Extensible (easy to add handlers)
- ✅ Auditable (all files logged)
- ✅ Recoverable (originals archived)

## Examples

See `examples/` for:
- `simple_inbox.py` - Basic file watcher
- `classifier_example.py` - File classification
- `handler_example.py` - Custom handler

## License

MIT
