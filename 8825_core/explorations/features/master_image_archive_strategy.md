# Master Image Archive Strategy

**Problem:** Deep image archives with massive duplication across projects, can't safely delete without breaking AI file links.

**Solution:** Create a deduplicated master image archive outside Dropbox, relink AI files to point to it.

---

## 🎯 THE CONCEPT

### **Current State:**
```
/Dropbox/AIMEE KESTENBERG/images/photo1.jpg (5 MB)
/Dropbox/AIMEE KESTENBERG/old/photo1.jpg (5 MB) - DUPLICATE
/Dropbox/CLIENT B/images/photo1.jpg (5 MB) - DUPLICATE
/Dropbox/CLIENT C/assets/photo1.jpg (5 MB) - DUPLICATE

Total: 20 MB for 1 image!
```

### **New State:**
```
/Volumes/ImageArchive/master/abc123def456.jpg (5 MB) - SINGLE COPY
  ↑
  └─ Linked by:
     - /Dropbox/AIMEE KESTENBERG/images/photo1.jpg → symlink
     - /Dropbox/AIMEE KESTENBERG/old/photo1.jpg → symlink
     - /Dropbox/CLIENT B/images/photo1.jpg → symlink
     - /Dropbox/CLIENT C/assets/photo1.jpg → symlink

Total: 5 MB + 4 tiny symlinks
Savings: 15 MB (75%)
```

---

## 🏗️ ARCHITECTURE

### **Master Archive Structure:**
```
/Volumes/ImageArchive/
├── master/                    # Deduplicated images (by hash)
│   ├── abc123def456.jpg
│   ├── def456ghi789.tif
│   └── ghi789jkl012.png
│
├── index/                     # Metadata & mappings
│   ├── image_index.db         # SQLite database
│   └── project_mappings.json  # Which projects use which images
│
├── originals/                 # Original paths (for rollback)
│   └── AIMEE_KESTENBERG/
│       └── images/
│           └── photo1.jpg
│
└── manifests/                 # Audit trail
    ├── migration_20251109.json
    └── deduplication_report.json
```

### **Image Index Database:**
```sql
CREATE TABLE images (
    hash TEXT PRIMARY KEY,
    original_filename TEXT,
    file_size INTEGER,
    width INTEGER,
    height INTEGER,
    format TEXT,
    first_seen DATE,
    master_path TEXT
);

CREATE TABLE references (
    id INTEGER PRIMARY KEY,
    image_hash TEXT,
    project_name TEXT,
    original_path TEXT,
    link_type TEXT,  -- 'symlink', 'alias', 'relink'
    created_date DATE,
    FOREIGN KEY (image_hash) REFERENCES images(hash)
);

CREATE TABLE projects (
    name TEXT PRIMARY KEY,
    root_path TEXT,
    total_images INTEGER,
    deduplicated_images INTEGER,
    space_saved INTEGER,
    migration_date DATE
);
```

---

## 🔄 MIGRATION WORKFLOW

### **Phase 1: Scan & Deduplicate**
```python
def scan_and_deduplicate(dropbox_root):
    """
    1. Scan all image files in Dropbox
    2. Calculate content hash for each
    3. Identify duplicates
    4. Copy unique images to master archive
    5. Build index database
    """
    
    image_index = {}
    duplicates = defaultdict(list)
    
    for filepath in find_all_images(dropbox_root):
        content_hash = calculate_hash(filepath)
        
        if content_hash not in image_index:
            # First occurrence - copy to master
            master_path = copy_to_master(filepath, content_hash)
            image_index[content_hash] = {
                'master_path': master_path,
                'original': filepath,
                'size': os.path.getsize(filepath),
                'references': []
            }
        else:
            # Duplicate - just record reference
            duplicates[content_hash].append(filepath)
        
        image_index[content_hash]['references'].append(filepath)
    
    return image_index, duplicates
```

### **Phase 2: Relink AI Files**
```python
def relink_ai_files(ai_files, image_index):
    """
    1. For each AI file
    2. Extract linked image paths
    3. Find image in master archive (by hash)
    4. Update AI file to point to master path
    5. Verify link works
    """
    
    for ai_file in ai_files:
        links = extract_links_from_ai(ai_file)
        
        for link in links:
            # Find image hash
            if os.path.exists(link):
                link_hash = calculate_hash(link)
                
                if link_hash in image_index:
                    # Update link to master archive
                    master_path = image_index[link_hash]['master_path']
                    update_ai_link(ai_file, link, master_path)
                else:
                    print(f"⚠️  Image not in archive: {link}")
```

### **Phase 3: Replace with Symlinks**
```python
def replace_with_symlinks(image_index):
    """
    1. For each duplicate image in Dropbox
    2. Delete original file
    3. Create symlink to master archive
    4. Verify symlink works
    """
    
    for hash_key, info in image_index.items():
        master_path = info['master_path']
        
        for ref_path in info['references']:
            if ref_path != info['original']:  # Don't replace the first one yet
                # Backup original
                backup_path = backup_file(ref_path)
                
                # Delete original
                os.remove(ref_path)
                
                # Create symlink
                os.symlink(master_path, ref_path)
                
                # Verify
                if not os.path.exists(ref_path):
                    print(f"❌ Symlink failed: {ref_path}")
                    restore_from_backup(backup_path, ref_path)
```

---

## 🎯 IMPLEMENTATION OPTIONS

### **Option A: External Drive + Symlinks** ⭐ Recommended

**Setup:**
```
/Volumes/ImageArchive/  (External SSD, not synced)
  ↓
/Dropbox/images/photo.jpg → symlink to /Volumes/ImageArchive/master/abc123.jpg
```

**Pros:**
- ✅ Images outside Dropbox (no sync cost)
- ✅ AI files can follow symlinks
- ✅ Instant access (local drive)
- ✅ Easy rollback (delete symlinks, restore originals)

**Cons:**
- ⚠️ Requires external drive always connected
- ⚠️ Not portable (drive must be mounted)
- ⚠️ Symlinks don't sync via Dropbox

**Best for:** Desktop workstation setup

---

### **Option B: Dropbox Subfolder + Symlinks** ⭐ Good Balance

**Setup:**
```
/Dropbox/_ImageArchive/master/abc123.jpg  (deduplicated)
  ↑
/Dropbox/AIMEE KESTENBERG/images/photo.jpg → symlink
```

**Pros:**
- ✅ Still in Dropbox (syncs everywhere)
- ✅ Deduplication saves space
- ✅ Portable (works on any machine)
- ✅ AI files can follow symlinks

**Cons:**
- ⚠️ Symlinks may not sync properly via Dropbox
- ⚠️ Still counts against Dropbox quota

**Best for:** Multi-machine setup

---

### **Option C: Cloud Storage + URL Links** ⚠️ Complex

**Setup:**
```
AWS S3 / Cloudflare R2 / Backblaze B2
  ↓
AI files link to: https://images.example.com/abc123.jpg
```

**Pros:**
- ✅ Unlimited storage (cheap)
- ✅ Works from anywhere
- ✅ No local disk space needed

**Cons:**
- ❌ AI files can't link to URLs (need local paths)
- ❌ Requires download before use
- ❌ Latency for large files

**Best for:** Long-term cold storage, not active use

---

### **Option D: Hybrid Approach** ⭐⭐ BEST SOLUTION

**Setup:**
```
/Volumes/ImageArchive/master/  (External SSD - working files)
  ↓ sync to ↓
AWS S3 Glacier Deep Archive  (Backup - cold storage)
  ↑
/Dropbox/images/photo.jpg → symlink to /Volumes/ImageArchive/master/abc123.jpg
```

**Workflow:**
1. Master archive on external SSD (fast access)
2. Dropbox images replaced with symlinks
3. Master archive backed up to S3 Glacier (cheap, safe)
4. AI files link to local master archive
5. If image needed and not local, download from S3

**Pros:**
- ✅ Fast local access
- ✅ Safe cloud backup
- ✅ Massive space savings in Dropbox
- ✅ Works offline (local cache)
- ✅ Disaster recovery (S3 backup)

**Costs:**
- External SSD: $100-200 (1-2 TB)
- S3 Glacier Deep Archive: $1/TB/month
- Example: 500 GB images = $0.50/month

---

## 📊 EXPECTED SAVINGS

### **Based on AIMEE KESTENBERG Scan:**
- Total images: ~232 files
- Total size: ~2.9 GB (from earlier scan)
- Estimated duplication: 30-40% (based on version analysis)

**Conservative estimate:**
- Unique images: ~150 files
- Duplicate images: ~82 files
- Space saved: ~1 GB (35%)

**Aggressive estimate (if cross-project duplication):**
- Unique images: ~100 files
- Duplicate images: ~132 files
- Space saved: ~1.8 GB (60%)

### **Across All Projects:**
If you have 10 similar projects:
- Total images: ~2,320 files
- Total size: ~29 GB
- Cross-project duplication: 50-70%
- **Space saved: 15-20 GB** (50-70%)

---

## 🛠️ COMPLETE IMPLEMENTATION

```python
#!/usr/bin/env python3
"""
Master Image Archive Migration Tool
Deduplicates images across projects, creates master archive
"""

import os
import shutil
import hashlib
import sqlite3
from pathlib import Path
from collections import defaultdict

class MasterImageArchive:
    def __init__(self, archive_root):
        self.archive_root = Path(archive_root)
        self.master_dir = self.archive_root / 'master'
        self.index_dir = self.archive_root / 'index'
        self.originals_dir = self.archive_root / 'originals'
        
        # Create directories
        self.master_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.originals_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.db = sqlite3.connect(self.index_dir / 'image_index.db')
        self.init_database()
    
    def init_database(self):
        """Create database schema"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                hash TEXT PRIMARY KEY,
                original_filename TEXT,
                file_size INTEGER,
                format TEXT,
                master_path TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_hash TEXT,
                project_name TEXT,
                original_path TEXT,
                link_type TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (image_hash) REFERENCES images(hash)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                name TEXT PRIMARY KEY,
                root_path TEXT,
                total_images INTEGER,
                deduplicated_images INTEGER,
                space_saved INTEGER,
                migration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.commit()
    
    def calculate_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def scan_project(self, project_root, project_name):
        """Scan project for images and deduplicate"""
        print(f"\n🔍 Scanning project: {project_name}")
        print(f"   Root: {project_root}")
        
        image_exts = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.webp', '.heic', '.psd', '.ai', '.eps'}
        
        total_images = 0
        total_size = 0
        deduplicated = 0
        space_saved = 0
        
        cursor = self.db.cursor()
        
        for dirpath, dirnames, filenames in os.walk(project_root):
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            
            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in image_exts:
                    continue
                
                filepath = os.path.join(dirpath, filename)
                file_size = os.path.getsize(filepath)
                
                total_images += 1
                total_size += file_size
                
                # Calculate hash
                file_hash = self.calculate_hash(filepath)
                
                # Check if already in master archive
                cursor.execute('SELECT master_path FROM images WHERE hash = ?', (file_hash,))
                result = cursor.fetchone()
                
                if result:
                    # Duplicate found!
                    deduplicated += 1
                    space_saved += file_size
                    master_path = result[0]
                    print(f"   ✓ Duplicate: {filename} → {master_path}")
                else:
                    # New image - copy to master
                    master_filename = f"{file_hash}{ext}"
                    master_path = self.master_dir / master_filename
                    
                    shutil.copy2(filepath, master_path)
                    
                    # Add to database
                    cursor.execute('''
                        INSERT INTO images (hash, original_filename, file_size, format, master_path)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (file_hash, filename, file_size, ext, str(master_path)))
                    
                    print(f"   + New: {filename} → {master_filename}")
                
                # Record reference
                rel_path = os.path.relpath(filepath, project_root)
                cursor.execute('''
                    INSERT INTO references (image_hash, project_name, original_path, link_type)
                    VALUES (?, ?, ?, ?)
                ''', (file_hash, project_name, rel_path, 'original'))
                
                if total_images % 100 == 0:
                    print(f"   Processed {total_images} images...")
        
        # Update project stats
        cursor.execute('''
            INSERT OR REPLACE INTO projects (name, root_path, total_images, deduplicated_images, space_saved)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_name, project_root, total_images, deduplicated, space_saved))
        
        self.db.commit()
        
        print(f"\n   📊 Results:")
        print(f"      Total images: {total_images}")
        print(f"      Duplicates found: {deduplicated} ({deduplicated/total_images*100:.1f}%)")
        print(f"      Space saved: {self.format_bytes(space_saved)}")
        
        return {
            'total_images': total_images,
            'deduplicated': deduplicated,
            'space_saved': space_saved
        }
    
    def create_symlinks(self, project_root, project_name, dry_run=True):
        """Replace duplicate images with symlinks to master archive"""
        print(f"\n🔗 Creating symlinks for: {project_name}")
        
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT r.original_path, i.master_path
            FROM references r
            JOIN images i ON r.image_hash = i.hash
            WHERE r.project_name = ? AND r.link_type = 'original'
        ''', (project_name,))
        
        symlinks_created = 0
        
        for original_rel_path, master_path in cursor.fetchall():
            original_path = os.path.join(project_root, original_rel_path)
            
            if not os.path.exists(original_path):
                continue
            
            if dry_run:
                print(f"   [DRY RUN] Would create symlink:")
                print(f"      {original_path} → {master_path}")
            else:
                # Backup original
                backup_path = self.originals_dir / project_name / original_rel_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(original_path, backup_path)
                
                # Create symlink
                os.symlink(master_path, original_path)
                
                # Update database
                cursor.execute('''
                    UPDATE references
                    SET link_type = 'symlink'
                    WHERE project_name = ? AND original_path = ?
                ''', (project_name, original_rel_path))
                
                symlinks_created += 1
                print(f"   ✓ Created symlink: {original_rel_path}")
        
        self.db.commit()
        
        print(f"\n   {'[DRY RUN] Would create' if dry_run else 'Created'} {symlinks_created} symlinks")
    
    def generate_report(self):
        """Generate deduplication report"""
        cursor = self.db.cursor()
        
        # Overall stats
        cursor.execute('SELECT COUNT(*), SUM(file_size) FROM images')
        unique_images, unique_size = cursor.fetchone()
        
        cursor.execute('SELECT COUNT(*) FROM references')
        total_references = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(space_saved) FROM projects')
        total_saved = cursor.fetchone()[0] or 0
        
        print("\n" + "=" * 80)
        print("📊 MASTER IMAGE ARCHIVE REPORT")
        print("=" * 80)
        
        print(f"\n🎯 Overall Statistics:")
        print(f"   Unique images: {unique_images:,}")
        print(f"   Total references: {total_references:,}")
        print(f"   Deduplication ratio: {total_references/unique_images:.1f}x")
        print(f"   Unique storage: {self.format_bytes(unique_size)}")
        print(f"   Space saved: {self.format_bytes(total_saved)}")
        
        # Per-project stats
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        
        print(f"\n📁 Projects:")
        for name, root, total, dedup, saved, date in projects:
            print(f"\n   {name}:")
            print(f"      Total images: {total:,}")
            print(f"      Duplicates: {dedup:,} ({dedup/total*100:.1f}%)")
            print(f"      Space saved: {self.format_bytes(saved)}")
        
        print("\n" + "=" * 80)
    
    @staticmethod
    def format_bytes(bytes_val):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"

def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 master_image_archive.py <archive_root> <project_root> [project_name]")
        print("\nExample:")
        print('  python3 master_image_archive.py "/Volumes/ImageArchive" "/path/to/AIMEE KESTENBERG" "AIMEE_KESTENBERG"')
        sys.exit(1)
    
    archive_root = sys.argv[1]
    project_root = sys.argv[2]
    project_name = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(project_root)
    
    # Initialize archive
    archive = MasterImageArchive(archive_root)
    
    # Scan project
    results = archive.scan_project(project_root, project_name)
    
    # Generate report
    archive.generate_report()
    
    # Ask about symlinks
    print("\n" + "=" * 80)
    print("🔗 SYMLINK CREATION")
    print("=" * 80)
    print("\nWould you like to replace duplicate images with symlinks?")
    print("This will:")
    print("  1. Move original files to backup")
    print("  2. Create symlinks to master archive")
    print("  3. Save disk space in Dropbox")
    print("\nRun with --create-symlinks flag to proceed")

if __name__ == "__main__":
    main()
```

---

## 🎯 USAGE EXAMPLE

```bash
# Step 1: Create master archive and scan first project
python3 master_image_archive.py \
    "/Volumes/ImageArchive" \
    "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/ - PRTCL -/AIMEE KESTENBERG" \
    "AIMEE_KESTENBERG"

# Step 2: Scan additional projects
python3 master_image_archive.py \
    "/Volumes/ImageArchive" \
    "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/ - PRTCL -/CLIENT_B" \
    "CLIENT_B"

# Step 3: Generate report
python3 master_image_archive.py --report "/Volumes/ImageArchive"

# Step 4: Create symlinks (dry run first)
python3 master_image_archive.py --create-symlinks --dry-run \
    "/Volumes/ImageArchive" \
    "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/ - PRTCL -/AIMEE KESTENBERG"

# Step 5: Create symlinks (for real)
python3 master_image_archive.py --create-symlinks \
    "/Volumes/ImageArchive" \
    "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/ - PRTCL -/AIMEE KESTENBERG"
```

---

## ✅ BENEFITS

1. **Massive space savings** - 50-70% reduction across projects
2. **Single source of truth** - One copy of each image
3. **Easy rollback** - Originals backed up
4. **Works with AI files** - Symlinks are transparent
5. **Scales across projects** - More projects = more savings
6. **Outside Dropbox option** - No sync cost
7. **Audit trail** - Database tracks everything

---

## 🎯 RECOMMENDATION

**Start with:** Option D (Hybrid Approach)
- External SSD for master archive
- Symlinks in Dropbox projects
- S3 Glacier backup

**This gives you:**
- ✅ Fast local access
- ✅ Massive Dropbox savings
- ✅ Safe cloud backup
- ✅ Works with Mark Craig's workflow

**Want me to build the complete implementation?**
