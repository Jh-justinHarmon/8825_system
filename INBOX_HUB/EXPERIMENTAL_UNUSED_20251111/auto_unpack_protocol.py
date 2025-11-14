#!/usr/bin/env python3
"""
Auto-Unpack Protocol - Automatically extract archives for review
Handles zip, tar, gz, etc.
"""

import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import json

# Import deduplication protocol
from deduplication_protocol import DeduplicationProtocol

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
PROCESSING_FOLDER = Path.home() / "Downloads" / "8825_processing"
UNPACKED_FOLDER = PROCESSING_FOLDER / "_unpacked"

# Supported archive types
ARCHIVE_EXTENSIONS = {
    '.zip': 'zip',
    '.tar': 'tar',
    '.tar.gz': 'tar.gz',
    '.tgz': 'tar.gz',
    '.tar.bz2': 'tar.bz2',
    '.tbz2': 'tar.bz2',
    '.rar': 'rar',  # Would need rarfile package
    '.7z': '7z'     # Would need py7zr package
}


class AutoUnpackProtocol:
    """Automatically unpack archives for review"""
    
    def __init__(self):
        UNPACKED_FOLDER.mkdir(exist_ok=True)
        self.dedup_protocol = DeduplicationProtocol()
    
    def is_archive(self, file_path: Path) -> bool:
        """Check if file is an archive"""
        # Check single extension
        if file_path.suffix.lower() in ARCHIVE_EXTENSIONS:
            return True
        
        # Check double extension (e.g., .tar.gz)
        if len(file_path.suffixes) >= 2:
            double_ext = ''.join(file_path.suffixes[-2:]).lower()
            if double_ext in ARCHIVE_EXTENSIONS:
                return True
        
        return False
    
    def get_archive_type(self, file_path: Path) -> Optional[str]:
        """Get archive type"""
        # Check double extension first
        if len(file_path.suffixes) >= 2:
            double_ext = ''.join(file_path.suffixes[-2:]).lower()
            if double_ext in ARCHIVE_EXTENSIONS:
                return ARCHIVE_EXTENSIONS[double_ext]
        
        # Check single extension
        if file_path.suffix.lower() in ARCHIVE_EXTENSIONS:
            return ARCHIVE_EXTENSIONS[file_path.suffix.lower()]
        
        return None
    
    def unpack_zip(self, file_path: Path, dest_dir: Path) -> Dict:
        """Unpack zip file"""
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Get list of files
                file_list = zip_ref.namelist()
                
                # Extract all
                zip_ref.extractall(dest_dir)
                
                return {
                    "success": True,
                    "files_extracted": len(file_list),
                    "files": file_list,
                    "destination": str(dest_dir)
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def unpack_tar(self, file_path: Path, dest_dir: Path) -> Dict:
        """Unpack tar file (including .tar.gz, .tar.bz2)"""
        try:
            with tarfile.open(file_path, 'r:*') as tar_ref:
                # Get list of files
                file_list = tar_ref.getnames()
                
                # Extract all
                tar_ref.extractall(dest_dir)
                
                return {
                    "success": True,
                    "files_extracted": len(file_list),
                    "files": file_list,
                    "destination": str(dest_dir)
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def unpack_archive(self, file_path: Path) -> Dict:
        """Unpack any supported archive"""
        archive_type = self.get_archive_type(file_path)
        
        if not archive_type:
            return {
                "success": False,
                "error": "Unsupported archive type"
            }
        
        # Create destination directory
        dest_name = file_path.stem
        if dest_name.endswith('.tar'):  # Handle .tar.gz -> remove .tar too
            dest_name = Path(dest_name).stem
        
        dest_dir = UNPACKED_FOLDER / dest_name
        dest_dir.mkdir(exist_ok=True)
        
        # Unpack based on type
        if archive_type == 'zip':
            result = self.unpack_zip(file_path, dest_dir)
        elif archive_type.startswith('tar'):
            result = self.unpack_tar(file_path, dest_dir)
        else:
            return {
                "success": False,
                "error": f"Handler not implemented for {archive_type}"
            }
        
        # Add metadata
        if result["success"]:
            result["archive_name"] = file_path.name
            result["archive_type"] = archive_type
            result["unpacked_to"] = str(dest_dir)
            
            # Check for duplicates in unpacked files
            unpacked_files = [dest_dir / f for f in result["files"] if (dest_dir / f).is_file()]
            dedup_results = self.dedup_protocol.scan_batch(unpacked_files)
            
            result["deduplication"] = {
                "total_files": len(unpacked_files),
                "duplicates": len(dedup_results["duplicates"]),
                "unique": len(dedup_results["unique"]),
                "duplicate_files": [d["filename"] for d in dedup_results["duplicates"]]
            }
            
            # Save metadata file
            metadata_file = dest_dir / "_archive_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(result, indent=2, fp=f)
        
        return result
    
    def scan_and_unpack(self, directory: Path) -> Dict:
        """Scan directory for archives and unpack them"""
        results = {
            "archives_found": [],
            "unpacked": [],
            "failed": []
        }
        
        for file_path in directory.iterdir():
            if not file_path.is_file():
                continue
            
            if self.is_archive(file_path):
                results["archives_found"].append(str(file_path))
                
                print(f"\n📦 Found archive: {file_path.name}")
                print(f"   Type: {self.get_archive_type(file_path)}")
                print(f"   Unpacking...")
                
                result = self.unpack_archive(file_path)
                
                if result["success"]:
                    print(f"   ✓ Extracted {result['files_extracted']} files")
                    print(f"   → {result['unpacked_to']}")
                    
                    # Show deduplication results
                    if result.get("deduplication"):
                        dedup = result["deduplication"]
                        if dedup["duplicates"] > 0:
                            print(f"   ⚠️  {dedup['duplicates']} duplicates found (already processed)")
                            print(f"   ✓ {dedup['unique']} unique files")
                        else:
                            print(f"   ✓ All {dedup['unique']} files are unique")
                    
                    results["unpacked"].append(result)
                else:
                    print(f"   ❌ Failed: {result['error']}")
                    results["failed"].append({
                        "file": str(file_path),
                        "error": result["error"]
                    })
        
        return results
    
    def show_unpacked_summary(self, results: Dict):
        """Show summary of unpacked archives"""
        print("\n" + "="*70)
        print("📦 Archive Unpacking Summary")
        print("="*70)
        
        print(f"\nArchives found: {len(results['archives_found'])}")
        print(f"Successfully unpacked: {len(results['unpacked'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results["unpacked"]:
            print("\n" + "-"*70)
            print("Unpacked Archives:")
            print("-"*70)
            for item in results["unpacked"]:
                print(f"\n✓ {item['archive_name']}")
                print(f"  Files extracted: {item['files_extracted']}")
                print(f"  Location: {item['unpacked_to']}")
                
                # Show deduplication summary
                if item.get('deduplication'):
                    dedup = item['deduplication']
                    print(f"  Deduplication:")
                    print(f"    • Total files: {dedup['total_files']}")
                    print(f"    • Unique: {dedup['unique']}")
                    print(f"    • Duplicates: {dedup['duplicates']}")
                    
                    if dedup['duplicate_files']:
                        print(f"    • Duplicate files:")
                        for dup_file in dedup['duplicate_files'][:5]:
                            print(f"      - {dup_file}")
                        if len(dedup['duplicate_files']) > 5:
                            print(f"      ... and {len(dedup['duplicate_files']) - 5} more")
                
                # Show first few files
                if item.get('files'):
                    print(f"  Contents (first 5):")
                    for f in item['files'][:5]:
                        print(f"    • {f}")
                    if len(item['files']) > 5:
                        print(f"    ... and {len(item['files']) - 5} more")
        
        if results["failed"]:
            print("\n" + "-"*70)
            print("Failed to Unpack:")
            print("-"*70)
            for item in results["failed"]:
                print(f"\n❌ {Path(item['file']).name}")
                print(f"   Error: {item['error']}")
        
        print("\n" + "="*70)
        print(f"\nUnpacked files location: {UNPACKED_FOLDER}")
        print("="*70 + "\n")


def main():
    """CLI for auto-unpack protocol"""
    import sys
    
    protocol = AutoUnpackProtocol()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  auto_unpack_protocol.py scan <directory>")
        print("  auto_unpack_protocol.py unpack <file>")
        print("  auto_unpack_protocol.py check <file>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "scan":
        if len(sys.argv) < 3:
            # Default to processing folder
            directory = PROCESSING_FOLDER
        else:
            directory = Path(sys.argv[2])
        
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        
        results = protocol.scan_and_unpack(directory)
        protocol.show_unpacked_summary(results)
    
    elif command == "unpack":
        if len(sys.argv) < 3:
            print("Usage: auto_unpack_protocol.py unpack <file>")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        result = protocol.unpack_archive(file_path)
        
        if result["success"]:
            print(f"\n✓ Unpacked {file_path.name}")
            print(f"  Files extracted: {result['files_extracted']}")
            print(f"  Location: {result['unpacked_to']}\n")
        else:
            print(f"\n❌ Failed to unpack: {result['error']}\n")
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("Usage: auto_unpack_protocol.py check <file>")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        
        if protocol.is_archive(file_path):
            archive_type = protocol.get_archive_type(file_path)
            print(f"\n✓ {file_path.name} is a {archive_type} archive\n")
        else:
            print(f"\n✗ {file_path.name} is not a supported archive\n")
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
