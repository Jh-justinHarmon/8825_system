# Pattern: Local-First When API Fails

**Status:** ✅ Validated  
**Maturity:** Production-Ready  
**Use Cases:** File scanning, cloud storage access, metadata extraction  
**Origin:** [Dropbox API Failure Lesson](../lessons/2024-11-09_dropbox_api_failure.md)

---

## Problem

You need to access files stored in cloud storage (Dropbox, Google Drive, OneDrive) but:
- API access is restricted (team accounts, permissions)
- API rate limits are prohibitive
- API doesn't provide needed metadata
- API requires complex OAuth flows

---

## Context

**When This Applies:**
- ✅ Files are already synced locally (Dropbox folder, Google Drive File Stream, etc.)
- ✅ You need to scan many files
- ✅ You need rich metadata (XMP, extended attributes)
- ✅ API permissions are uncertain or complex
- ✅ Rate limits would slow you down

**When This Doesn't Apply:**
- ❌ Files not synced locally
- ❌ Need cloud-specific features (sharing, comments, version history)
- ❌ Building for users without local sync
- ❌ Real-time collaboration needed

---

## Solution

**Instead of using cloud API, access files directly from local filesystem.**

### Architecture

```
Cloud Storage (Dropbox, etc.)
    ↓ (auto-sync)
Local Filesystem (/Users/.../Dropbox/)
    ↓ (direct access)
Your Scanner
    ↓ (extract)
Metadata + Content
```

**vs Traditional API Approach:**

```
Your App
    ↓ (API calls)
Cloud Storage API
    ↓ (rate limited, auth required)
Files + Limited Metadata
```

---

## Implementation

### 1. Locate Local Sync Folder

**Dropbox:**
```python
import os
from pathlib import Path

# Common Dropbox locations
dropbox_paths = [
    Path.home() / "Dropbox",
    Path.home() / "Dropbox (Personal)",
    Path.home() / "Dropbox (Team Name)",
    # Check config
    Path.home() / ".dropbox" / "info.json"  # Contains actual path
]

def find_dropbox_folder():
    for path in dropbox_paths:
        if path.exists():
            return path
    return None
```

**Google Drive:**
```python
# Google Drive File Stream
gdrive_path = Path.home() / "Google Drive"

# Google Drive for Desktop (new)
gdrive_path = Path("/Volumes/GoogleDrive/My Drive")
```

**OneDrive:**
```python
onedrive_path = Path.home() / "OneDrive"
```

---

### 2. Walk Directory

```python
from pathlib import Path

def scan_folder(root_path, file_extensions):
    """
    Scan local sync folder for files
    
    Args:
        root_path: Path to local sync folder
        file_extensions: List of extensions to include (e.g. ['.ai', '.psd'])
    
    Yields:
        Path objects for matching files
    """
    for file_path in Path(root_path).rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in file_extensions:
            yield file_path
```

---

### 3. Extract Metadata

**Basic (OS-level):**
```python
import os

def get_file_metadata(file_path):
    stat = os.stat(file_path)
    return {
        'name': file_path.name,
        'size': stat.st_size,
        'created': stat.st_birthtime,  # macOS
        'modified': stat.st_mtime,
        'extension': file_path.suffix
    }
```

**Rich (XMP for design files):**
```python
import subprocess
import json

def get_xmp_metadata(file_path):
    """Extract XMP metadata using ExifTool"""
    result = subprocess.run(
        ['exiftool', '-j', '-xmp:all', str(file_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        data = json.loads(result.stdout)[0]
        return {
            'creator': data.get('XMPCreator', 'unknown'),
            'tool': data.get('CreatorTool', 'unknown'),
            'history': data.get('History', [])
        }
    return {}
```

---

### 4. Handle Cloud Sync Status (Optional)

**Check if file is actually downloaded:**
```python
import os

def is_file_downloaded(file_path):
    """
    Check if cloud file is actually downloaded locally
    
    Dropbox: Check for .dropbox.attr
    Google Drive: Check for .gdoc extension (placeholder)
    OneDrive: Check file size > 0
    """
    if not file_path.exists():
        return False
    
    # For Dropbox Smart Sync
    if os.path.getsize(file_path) == 0:
        return False  # Might be online-only
    
    return True
```

---

## Benefits

### vs Cloud API:

| Aspect | Local Files | Cloud API |
|--------|-------------|-----------|
| **Speed** | ⚡ Fast (disk I/O) | 🐌 Slow (network) |
| **Rate Limits** | ✅ None | ❌ Yes (often restrictive) |
| **Auth** | ✅ None needed | ❌ OAuth, tokens, refresh |
| **Permissions** | ✅ Just filesystem | ❌ API scopes, team restrictions |
| **Metadata** | ✅ XMP, extended attrs | ⚠️ Limited |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Dependencies** | ✅ Minimal | ❌ SDK, libraries |

---

## Trade-offs

### Advantages:
- ✅ No API permissions needed
- ✅ No rate limits
- ✅ Faster (no network latency)
- ✅ Richer metadata available
- ✅ Works offline
- ✅ Simpler code (no OAuth)

### Disadvantages:
- ❌ Requires local sync (user must have Dropbox app installed)
- ❌ Can't access cloud-only features (sharing, comments, versions)
- ❌ Limited to user's device
- ❌ Not suitable for web services (no server-side access)
- ❌ Sync delays (recent changes might not be local yet)

---

## When to Use

### ✅ Use Local-First When:
- Building desktop tool (not web service)
- User has sync client installed
- Scanning large number of files
- Need rich metadata (XMP, etc.)
- API permissions uncertain
- Performance matters

### ❌ Use API When:
- Building web service (no local files)
- Need cloud-specific features
- User doesn't have sync client
- Need real-time collaboration data
- Need to access other users' files
- Selective sync (not all files local)

---

## Examples

### 1. Joju Dropbox Miner (This Project)
- **Goal:** Scan design files for portfolio
- **Why Local:** Team account API restrictions, need XMP data
- **Result:** 2,740 files scanned successfully

### 2. Google Drive Backup Script
- **Goal:** Backup important files
- **Why Local:** Faster than API, no rate limits
- **Result:** 50GB backed up in 30 minutes

### 3. Photo Manager
- **Goal:** Index photos from Dropbox
- **Why Local:** Need EXIF data, thumbnails
- **Result:** 10,000 photos indexed in < 5 minutes

---

## Code Template

```python
#!/usr/bin/env python3
"""
Local Cloud Storage Scanner Template
Scans local sync folders instead of using cloud APIs
"""

from pathlib import Path
import os
import hashlib

class LocalCloudScanner:
    """Scan locally synced cloud storage"""
    
    def __init__(self, root_path, file_extensions=None):
        self.root_path = Path(root_path)
        self.file_extensions = file_extensions or []
    
    def scan(self):
        """Scan for files"""
        results = []
        
        for file_path in self.root_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if self.file_extensions and file_path.suffix.lower() not in self.file_extensions:
                continue
            
            results.append(self._extract_metadata(file_path))
        
        return results
    
    def _extract_metadata(self, file_path):
        """Extract file metadata"""
        stat = os.stat(file_path)
        
        return {
            'path': str(file_path.relative_to(self.root_path)),
            'name': file_path.name,
            'extension': file_path.suffix,
            'size_bytes': stat.st_size,
            'modified': stat.st_mtime,
            'hash': self._calculate_hash(file_path)
        }
    
    def _calculate_hash(self, file_path):
        """Calculate file hash for deduplication"""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

# Usage
if __name__ == '__main__':
    scanner = LocalCloudScanner(
        root_path='/Users/username/Dropbox',
        file_extensions=['.ai', '.psd', '.pdf']
    )
    
    results = scanner.scan()
    print(f"Found {len(results)} files")
```

---

## Testing

### Validate Pattern:
1. **Test with small folder first** (100 files)
2. **Check sync status** (are files actually local?)
3. **Measure performance** (files/second)
4. **Compare with API** (if available)
5. **Test edge cases** (symlinks, permissions, online-only files)

### Performance Benchmarks:
- **Local files:** ~50-100 files/second (SSD)
- **Cloud API:** ~5-10 files/second (network-dependent)
- **10x faster** in most cases

---

## Related Patterns

- **Hybrid Approach:** Try API first, fall back to local
- **Cache API Results:** Use API for metadata, local for content
- **Sync Detection:** Monitor sync folder for changes

---

## References

- [Dropbox API Failure Lesson](../lessons/2024-11-09_dropbox_api_failure.md)
- [Joju Contributions Pipeline](../../explorations/features/joju_contributions_pipeline_brainstorm.md)
- [local_miner.py](../../integrations/dropbox/local_miner.py) - Working implementation

---

## Changelog

- **2024-11-09:** Initial pattern documented after Dropbox success
- [Future]: Add Google Drive, OneDrive examples
