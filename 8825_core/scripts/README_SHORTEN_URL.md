# URL Shortener Tool

**Location:** `8825_core/scripts/shorten_url.py`  
**Purpose:** Create short URLs using free APIs (no account required)  
**Last Updated:** November 10, 2025

---

## Features

- ✅ No account required
- ✅ Custom short names (if available)
- ✅ Automatic clipboard copy (macOS)
- ✅ Fallback to v.gd if is.gd fails
- ✅ Support for underscores in custom names
- ✅ Interactive and command-line modes

---

## Usage

### Interactive Mode
```bash
python3 8825_core/scripts/shorten_url.py
```

### With URL
```bash
python3 8825_core/scripts/shorten_url.py "https://example.com/very/long/url"
```

### With Custom Name
```bash
python3 8825_core/scripts/shorten_url.py "https://example.com" "my_custom_name"
```

---

## Services Used

### Primary: is.gd
- Free, no account needed
- Simple API
- Good for general use

### Fallback: v.gd
- Sister site of is.gd
- Better support for custom names with underscores
- Used automatically if is.gd fails

---

## Custom Names

### ⚠️ IMPORTANT: Hyphens Will Fail!
**If you see a hyphen (-) in a custom name, it WILL fail on free services.**
- ✅ Use underscores: `joju_screener`
- ❌ Avoid hyphens: `joju-screener` (will fail)

### Tips:
- **Always use underscores (_) instead of hyphens (-)** 
- Keep names short and memorable
- Custom names may already be taken on free services
- No special characters beyond underscores
- Lowercase recommended

### Examples:
- ✅ `joju_screener` (works!)
- ✅ `my_link_2025` (works!)
- ❌ `joju-screener` (WILL FAIL - has hyphen)
- ❌ `my-link` (WILL FAIL - has hyphen)
- ❌ `my link` (WILL FAIL - has spaces)

---

## Recent Usage

### Joju Screener Survey (Nov 10, 2025)
```bash
python3 shorten_url.py "https://www.notion.so/2a8fe28ff8d6803f8313cfddbe3e231e?pvs=106" "joju_screener"
```

**Result:** `https://v.gd/joju_screener`

---

## Output

The script will:
1. Create the short URL
2. Display the result
3. Copy to clipboard (macOS)
4. Show success/error message

---

## Error Handling

### Common Errors:

**Custom name already taken:**
```
❌ Error: Custom name already in use
```
Solution: Try a different name or use auto-generated URL

**Network error:**
```
❌ Network error: Connection timeout
```
Solution: Check internet connection and try again

**Invalid URL:**
```
❌ Error: Invalid URL format
```
Solution: Ensure URL starts with http:// or https://

---

## Integration

### In Python Scripts:
```python
from shorten_url import shorten_url

# Basic usage
short = shorten_url("https://example.com")

# With custom name
short = shorten_url("https://example.com", "my_name")
```

### In Shell Scripts:
```bash
#!/bin/bash
SHORT_URL=$(python3 shorten_url.py "$LONG_URL" "$CUSTOM_NAME")
echo "Short URL: $SHORT_URL"
```

---

## Alternatives

If you need more control or branded links:

### Rebrandly (Free tier)
- Custom domain support
- Analytics
- 500 links/month free
- Requires account

### Bitly (Free tier)
- Popular service
- Analytics
- Requires account

### Custom Domain
- Full control
- Best for branding
- Requires domain ownership
- Example: `joju.app/screener`

---

## Saved URLs

All shortened URLs should be documented in:
- `focuses/[project]/url_mappings.json`
- Project-specific documentation

Example for Joju:
- `focuses/joju/user_engagement/surveys/url_mappings.json`

---

## Dependencies

```bash
pip3 install requests
```

---

## Troubleshooting

### Script not executable
```bash
chmod +x 8825_core/scripts/shorten_url.py
```

### Clipboard not working
- Only works on macOS
- Requires `pbcopy` command
- URL still displayed even if copy fails

### Custom name fails
- Try with underscores instead of hyphens
- Try a different name
- Use auto-generated URL

---

## Related Documentation

- `focuses/joju/user_engagement/surveys/joju_screener_survey.md`
- `focuses/joju/user_engagement/surveys/url_mappings.json`

---

**Maintained by:** 8825 Core Team  
**Support:** Check 8825 documentation or create issue
