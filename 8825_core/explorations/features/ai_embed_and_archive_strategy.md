# AI File Embed & Archive Strategy

**Problem:** Deep image archives with linked AI files - can't determine which images are in use without breaking links.

**Solution:** Programmatically embed all linked images into AI files, then safely archive the entire image archive.

---

## 🎯 THE WORKFLOW

### **Phase 1: Identify Active AI Files**
```
1. Scan for .ai files
2. Filter by modification date (keep files modified in last 6-12 months)
3. Group by project/folder
4. Result: List of "active" AI files that need embedding
```

### **Phase 2: Automated Embedding**
```
For each active AI file:
1. Open in Illustrator (via scripting)
2. Check for linked images
3. If links found:
   - Verify link paths exist
   - Embed all linked images
   - Save file
4. Close file
5. Log results
```

### **Phase 3: Verification**
```
1. Re-scan AI files
2. Verify no broken links
3. Generate report of embedded images
4. Test open random sample (5-10 files)
```

### **Phase 4: Archive Image Folders**
```
1. Move image archive folders to "Archive/Images_YYYY-MM-DD/"
2. Generate manifest (what was moved, from where)
3. Keep manifest for rollback
4. Calculate space saved
```

---

## 🛠️ IMPLEMENTATION OPTIONS

### **Option A: Adobe Illustrator Scripting** ⭐ Most Reliable

**Technology:** ExtendScript (JavaScript for Illustrator)

**Pros:**
- Native Illustrator API
- Reliable embedding
- Handles all AI file versions
- Can batch process

**Cons:**
- Requires Illustrator installed
- Slower (opens each file)
- Mac/Windows specific

**Script:**
```javascript
// embed_links.jsx
#target illustrator

function embedAllLinks(filePath) {
    var doc = app.open(new File(filePath));
    var links = doc.placedItems;
    var embedded = 0;
    var errors = [];
    
    for (var i = 0; i < links.length; i++) {
        try {
            if (links[i].file != null) {
                links[i].embed();
                embedded++;
            }
        } catch (e) {
            errors.push(links[i].file.fsName + ": " + e.message);
        }
    }
    
    doc.save();
    doc.close();
    
    return {
        embedded: embedded,
        errors: errors
    };
}

// Process all AI files in folder
function processFolder(folderPath) {
    var folder = new Folder(folderPath);
    var files = folder.getFiles("*.ai");
    var results = [];
    
    for (var i = 0; i < files.length; i++) {
        if (files[i] instanceof File) {
            var result = embedAllLinks(files[i].fsName);
            results.push({
                file: files[i].name,
                embedded: result.embedded,
                errors: result.errors
            });
        }
    }
    
    return results;
}
```

**Python wrapper:**
```python
import subprocess
import json

def embed_ai_files(folder_path, script_path):
    """Run Illustrator script to embed all links"""
    cmd = [
        'osascript',
        '-e', f'tell application "Adobe Illustrator"',
        '-e', f'do javascript file "{script_path}" with arguments "{folder_path}"',
        '-e', 'end tell'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)
```

---

### **Option B: Python + AI File Parsing** ⚠️ Complex

**Technology:** Custom AI file parser

**Pros:**
- No Illustrator required
- Faster (direct file manipulation)
- Can run on server

**Cons:**
- AI format is complex (PDF-based)
- May not handle all AI versions
- Risk of file corruption
- Hard to maintain

**Not recommended** - too risky for production files

---

### **Option C: Hybrid Approach** ⭐ Recommended

**Combine:**
1. Python for scanning/filtering
2. Illustrator scripting for embedding
3. Python for archiving/verification

**Workflow:**
```python
# 1. Scan and filter
active_ai_files = scan_ai_files(root_path, min_age_months=6)

# 2. Batch embed via Illustrator
results = batch_embed_illustrator(active_ai_files)

# 3. Verify
verify_no_broken_links(active_ai_files)

# 4. Archive images
archive_image_folders(image_archive_path, results)
```

---

## 📋 DETAILED IMPLEMENTATION PLAN

### **Step 1: Scan & Filter AI Files**
```python
def find_active_ai_files(root_path, months=6):
    """Find AI files modified in last N months"""
    cutoff_date = datetime.now() - timedelta(days=months*30)
    active_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.ai'):
                filepath = os.path.join(dirpath, filename)
                mtime = os.path.getmtime(filepath)
                if mtime > cutoff_date.timestamp():
                    active_files.append(filepath)
    
    return active_files
```

### **Step 2: Extract Linked Images**
```python
def extract_linked_images(ai_file_path):
    """Parse AI file to find linked images"""
    links = []
    with open(ai_file_path, 'rb') as f:
        content = f.read()
        # Look for linked file references
        patterns = [
            rb'%%PlacedGraphic:\s*([^\r\n]+)',
            rb'/FileSpec\s*<<.*?/F\s*\(([^)]+)\)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            links.extend(m.decode('utf-8', errors='ignore').strip() for m in matches)
    return links
```

### **Step 3: Batch Embed via Illustrator**
```python
def batch_embed_illustrator(ai_files, batch_size=10):
    """Embed links in batches to avoid memory issues"""
    results = []
    
    for i in range(0, len(ai_files), batch_size):
        batch = ai_files[i:i+batch_size]
        
        # Create batch script
        script = generate_batch_script(batch)
        script_path = '/tmp/embed_batch.jsx'
        with open(script_path, 'w') as f:
            f.write(script)
        
        # Run via osascript
        result = run_illustrator_script(script_path)
        results.extend(result)
        
        # Progress
        print(f"Processed {i+len(batch)}/{len(ai_files)} files...")
    
    return results
```

### **Step 4: Verify No Broken Links**
```python
def verify_no_broken_links(ai_files):
    """Check that all links are now embedded"""
    broken = []
    
    for filepath in ai_files:
        links = extract_linked_images(filepath)
        if links:
            broken.append({
                'file': filepath,
                'links': links
            })
    
    return broken
```

### **Step 5: Archive Image Folders**
```python
def archive_image_folders(root_path, embed_results):
    """Move image folders to archive"""
    archive_path = f"{root_path}/Archive/Images_{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(archive_path, exist_ok=True)
    
    # Collect all image folders
    image_folders = find_image_folders(root_path)
    
    manifest = {
        'archive_date': datetime.now().isoformat(),
        'embedded_files': len(embed_results),
        'archived_folders': []
    }
    
    for folder in image_folders:
        # Move folder
        dest = os.path.join(archive_path, os.path.basename(folder))
        shutil.move(folder, dest)
        
        manifest['archived_folders'].append({
            'original': folder,
            'archived': dest,
            'size': get_folder_size(dest)
        })
    
    # Save manifest
    with open(f"{archive_path}/MANIFEST.json", 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest
```

---

## 🎯 COMPLETE WORKFLOW SCRIPT

```python
#!/usr/bin/env python3
"""
AI Embed & Archive Workflow
Embeds all linked images in active AI files, then archives image folders
"""

import os
import shutil
import json
from datetime import datetime, timedelta

def main(project_root, months_active=6):
    print("🎨 AI Embed & Archive Workflow")
    print("=" * 80)
    
    # Step 1: Find active AI files
    print("\n📁 Step 1: Finding active AI files...")
    active_ai_files = find_active_ai_files(project_root, months=months_active)
    print(f"   Found {len(active_ai_files)} active AI files")
    
    # Step 2: Extract current links (for reporting)
    print("\n🔗 Step 2: Analyzing linked images...")
    linked_images = {}
    for ai_file in active_ai_files:
        links = extract_linked_images(ai_file)
        if links:
            linked_images[ai_file] = links
    print(f"   Found {len(linked_images)} files with links")
    print(f"   Total linked images: {sum(len(v) for v in linked_images.values())}")
    
    # Step 3: Embed all links
    print("\n🔄 Step 3: Embedding linked images...")
    print("   This will take a while (opens each file in Illustrator)...")
    embed_results = batch_embed_illustrator(active_ai_files)
    
    successful = sum(1 for r in embed_results if r['errors'] == [])
    failed = len(embed_results) - successful
    print(f"   ✅ Successfully embedded: {successful} files")
    if failed > 0:
        print(f"   ❌ Failed: {failed} files")
    
    # Step 4: Verify
    print("\n✅ Step 4: Verifying no broken links...")
    broken = verify_no_broken_links(active_ai_files)
    if broken:
        print(f"   ⚠️  WARNING: {len(broken)} files still have links!")
        print("   Review these files manually before archiving images")
        return
    else:
        print("   ✅ All links embedded successfully!")
    
    # Step 5: Archive images
    print("\n📦 Step 5: Archiving image folders...")
    manifest = archive_image_folders(project_root, embed_results)
    
    total_saved = sum(f['size'] for f in manifest['archived_folders'])
    print(f"   ✅ Archived {len(manifest['archived_folders'])} folders")
    print(f"   💰 Space saved: {format_bytes(total_saved)}")
    
    # Step 6: Generate report
    print("\n📊 Step 6: Generating report...")
    report = {
        'date': datetime.now().isoformat(),
        'active_ai_files': len(active_ai_files),
        'files_with_links': len(linked_images),
        'total_links_embedded': sum(r['embedded'] for r in embed_results),
        'files_embedded': successful,
        'files_failed': failed,
        'archived_folders': len(manifest['archived_folders']),
        'space_saved_bytes': total_saved,
        'manifest_path': f"{project_root}/Archive/Images_{datetime.now().strftime('%Y%m%d')}/MANIFEST.json"
    }
    
    with open('embed_archive_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ WORKFLOW COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   - Active AI files processed: {len(active_ai_files)}")
    print(f"   - Links embedded: {sum(r['embedded'] for r in embed_results)}")
    print(f"   - Image folders archived: {len(manifest['archived_folders'])}")
    print(f"   - Space saved: {format_bytes(total_saved)}")
    print(f"\n📁 Manifest: {report['manifest_path']}")
    print(f"📁 Report: embed_archive_report.json")
    print("\n⚠️  To rollback, run: python3 rollback_archive.py")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 ai_embed_and_archive.py <project_root> [months_active]")
        print("\nExample:")
        print('  python3 ai_embed_and_archive.py "/path/to/AIMEE KESTENBERG" 6')
        sys.exit(1)
    
    project_root = sys.argv[1]
    months_active = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    
    main(project_root, months_active)
```

---

## 🚨 SAFETY MEASURES

### **Before Running:**
1. ✅ **Backup entire project folder** (or ensure Dropbox versioning is on)
2. ✅ **Test on small sample** (5-10 files)
3. ✅ **Verify Illustrator version** (script compatibility)
4. ✅ **Check disk space** (embedded files will be larger)

### **During Running:**
1. ✅ **Monitor progress** (log each file)
2. ✅ **Handle errors gracefully** (skip failed files, don't stop)
3. ✅ **Save intermediate results** (resume if interrupted)

### **After Running:**
1. ✅ **Verify random sample** (open 10 files, check images)
2. ✅ **Keep manifest** (for rollback)
3. ✅ **Test with Mark Craig** (open recent projects)
4. ✅ **Wait 1 week** before deleting archived images

---

## 📊 EXPECTED RESULTS

**For AIMEE KESTENBERG folder:**
- Active AI files: ~50-100 (modified in last 6 months)
- Linked images: ~200-500 (estimate)
- Image archive size: ~2-3 GB (based on earlier scan)
- Time to process: ~2-4 hours (depends on file sizes)
- Space saved: ~2-3 GB (entire image archive)

---

## 🎯 ROLLBACK PLAN

```python
#!/usr/bin/env python3
"""Rollback archived images"""

def rollback_archive(manifest_path):
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    print(f"Rolling back archive from {manifest['archive_date']}")
    
    for folder in manifest['archived_folders']:
        original = folder['original']
        archived = folder['archived']
        
        # Move back
        shutil.move(archived, original)
        print(f"  Restored: {original}")
    
    print("✅ Rollback complete!")
```

---

## 💡 NEXT STEPS

1. **Build Illustrator script** (embed_links.jsx)
2. **Build Python wrapper** (ai_embed_and_archive.py)
3. **Test on small sample** (5-10 files)
4. **Review with Mark Craig** (validate approach)
5. **Run on full project** (if test successful)
6. **Monitor for 1 week** (ensure no issues)
7. **Delete archived images** (if all good)

---

## ⚠️ IMPORTANT NOTES

1. **File size increase:** Embedded files will be larger than linked files
2. **Processing time:** Opens each file in Illustrator (slow)
3. **Illustrator required:** Must be installed and licensed
4. **Version compatibility:** Test with your AI version
5. **Backup first:** Always backup before running

---

## 🎯 ALTERNATIVE: INDESIGN FILES

If you also have InDesign files with links:

```javascript
// embed_indesign_links.jsx
#target indesign

function embedAllLinks(filePath) {
    var doc = app.open(new File(filePath));
    var links = doc.links;
    
    for (var i = 0; i < links.length; i++) {
        if (links[i].status == LinkStatus.NORMAL) {
            links[i].unlink();  // Embeds the link
        }
    }
    
    doc.save();
    doc.close();
}
```

Same workflow applies!

---

**Ready to build this?** This solves the "can't determine which images are in use" problem by making ALL images embedded, then archiving the entire image archive safely.
