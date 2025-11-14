#!/usr/bin/env python3
"""
Deduplication Protocol - Check files against existing records
Prevents reprocessing duplicates
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SYSTEM_ROOT = SCRIPT_DIR.parent
DEDUP_DB = SCRIPT_DIR / "users" / "jh" / "deduplication.json"

# Search locations for existing files
SEARCH_PATHS = [
    SYSTEM_ROOT / "INBOX_HUB" / "users" / "jh" / "processed",
    SYSTEM_ROOT / "INBOX_HUB" / "users" / "jh" / "intake",
    Path.home() / "Downloads" / "8825_processed",
    SYSTEM_ROOT / "8825_core" / "inbox",
    SYSTEM_ROOT / "Documents",
]


class DeduplicationProtocol:
    """Check for duplicate files before processing"""
    
    def __init__(self):
        self.db_file = DEDUP_DB
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self.db = self._load_db()
    
    def _load_db(self) -> dict:
        """Load deduplication database"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                return json.load(f)
        
        return {
            "version": "1.0",
            "files": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_db(self):
        """Save deduplication database"""
        self.db["last_updated"] = datetime.now().isoformat()
        with open(self.db_file, 'w') as f:
            json.dump(self.db, indent=2, fp=f)
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate file hash"""
        hasher = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                # Read in chunks for large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"⚠️  Could not hash {file_path.name}: {e}")
            return None
    
    def _find_existing_file(self, filename: str) -> Optional[Path]:
        """Search for existing file by name"""
        for search_path in SEARCH_PATHS:
            if not search_path.exists():
                continue
            
            # Search recursively
            for existing_file in search_path.rglob(filename):
                if existing_file.is_file():
                    return existing_file
        
        return None
    
    def check_duplicate(self, file_path: Path) -> Dict:
        """
        Check if file is a duplicate
        Returns: {is_duplicate, reason, existing_location, action}
        """
        result = {
            "file": str(file_path),
            "filename": file_path.name,
            "is_duplicate": False,
            "reason": None,
            "existing_location": None,
            "existing_hash": None,
            "action": "process"
        }
        
        # Calculate hash
        file_hash = self._calculate_hash(file_path)
        if not file_hash:
            return result
        
        # Check hash in database
        if file_hash in self.db["files"]:
            existing = self.db["files"][file_hash]
            result["is_duplicate"] = True
            result["reason"] = "Exact match (same hash)"
            result["existing_location"] = existing["location"]
            result["existing_hash"] = file_hash
            result["action"] = "skip"
            return result
        
        # Check by filename in known locations
        existing_file = self._find_existing_file(file_path.name)
        if existing_file:
            # Calculate hash of existing file
            existing_hash = self._calculate_hash(existing_file)
            
            if existing_hash == file_hash:
                result["is_duplicate"] = True
                result["reason"] = "Exact match (same content)"
                result["existing_location"] = str(existing_file)
                result["existing_hash"] = existing_hash
                result["action"] = "skip"
                
                # Add to database
                self.db["files"][file_hash] = {
                    "filename": file_path.name,
                    "location": str(existing_file),
                    "first_seen": datetime.now().isoformat(),
                    "size": file_path.stat().st_size
                }
                self._save_db()
            else:
                result["is_duplicate"] = False
                result["reason"] = "Same name, different content"
                result["existing_location"] = str(existing_file)
                result["action"] = "review"  # User should decide
        
        return result
    
    def register_file(self, file_path: Path, destination: str):
        """Register a processed file to prevent future duplicates"""
        file_hash = self._calculate_hash(file_path)
        if not file_hash:
            return
        
        self.db["files"][file_hash] = {
            "filename": file_path.name,
            "location": destination,
            "processed": datetime.now().isoformat(),
            "size": file_path.stat().st_size
        }
        self._save_db()
    
    def scan_batch(self, files: List[Path]) -> Dict:
        """Scan batch of files for duplicates"""
        results = {
            "duplicates": [],
            "unique": [],
            "review": []
        }
        
        for file_path in files:
            check = self.check_duplicate(file_path)
            
            if check["is_duplicate"]:
                results["duplicates"].append(check)
            elif check["action"] == "review":
                results["review"].append(check)
            else:
                results["unique"].append(check)
        
        return results
    
    def show_duplicate_report(self, results: Dict):
        """Show duplicate scan report"""
        print("\n" + "="*70)
        print("🔍 Deduplication Scan")
        print("="*70)
        
        total = len(results["duplicates"]) + len(results["unique"]) + len(results["review"])
        
        print(f"\nScanned: {total} files")
        print(f"  ✓ Unique: {len(results['unique'])}")
        print(f"  ⚠️  Duplicates: {len(results['duplicates'])}")
        print(f"  ? Need review: {len(results['review'])}")
        
        if results["duplicates"]:
            print("\n" + "-"*70)
            print("Duplicates Found:")
            print("-"*70)
            for dup in results["duplicates"]:
                print(f"\n❌ {dup['filename']}")
                print(f"   Reason: {dup['reason']}")
                print(f"   Exists at: {dup['existing_location']}")
                print(f"   Action: Skip (already processed)")
        
        if results["review"]:
            print("\n" + "-"*70)
            print("Need Review (same name, different content):")
            print("-"*70)
            for item in results["review"]:
                print(f"\n⚠️  {item['filename']}")
                print(f"   Existing: {item['existing_location']}")
                print(f"   Action: User should decide")
        
        if results["unique"]:
            print("\n" + "-"*70)
            print(f"Ready to Process ({len(results['unique'])} files):")
            print("-"*70)
            for item in results["unique"]:
                print(f"  ✓ {item['filename']}")
        
        print("\n" + "="*70 + "\n")


def main():
    """CLI for deduplication protocol"""
    import sys
    
    protocol = DeduplicationProtocol()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  deduplication_protocol.py scan <directory>")
        print("  deduplication_protocol.py check <file>")
        print("  deduplication_protocol.py stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "scan":
        if len(sys.argv) < 3:
            print("Usage: deduplication_protocol.py scan <directory>")
            sys.exit(1)
        
        directory = Path(sys.argv[2])
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        
        files = [f for f in directory.iterdir() if f.is_file()]
        results = protocol.scan_batch(files)
        protocol.show_duplicate_report(results)
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("Usage: deduplication_protocol.py check <file>")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        result = protocol.check_duplicate(file_path)
        
        print(f"\nFile: {result['filename']}")
        if result["is_duplicate"]:
            print(f"❌ Duplicate: {result['reason']}")
            print(f"   Exists at: {result['existing_location']}")
        else:
            print("✓ Unique file")
    
    elif command == "stats":
        print("\n" + "="*70)
        print("Deduplication Database Stats")
        print("="*70)
        print(f"\nTracked files: {len(protocol.db['files'])}")
        print(f"Last updated: {protocol.db['last_updated']}")
        print("="*70 + "\n")
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
