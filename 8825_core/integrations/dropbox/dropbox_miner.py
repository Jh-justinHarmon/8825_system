#!/usr/bin/env python3
"""
Joju Dropbox Contribution Miner - MVP
Scans Dropbox folder for design files and attributes contributions
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

try:
    import dropbox
    from dropbox.files import FileMetadata, FolderMetadata
    HAS_DROPBOX = True
except ImportError:
    HAS_DROPBOX = False
    print("Warning: dropbox package not installed")
    print("Install with: pip3 install dropbox")

# Configuration
DROPBOX_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
SUPPORTED_EXTENSIONS = ['.ai', '.psd', '.pdf', '.indd', '.sketch', '.fig']

# Output directory
OUTPUT_DIR = Path.home() / 'Hammer Consulting Dropbox' / 'Justin Harmon' / 'Public' / '8825' / '8825-system' / 'users' / 'justin_harmon' / 'joju' / 'data' / 'mining_reports'

class DropboxMiner:
    def __init__(self, token: str = None):
        if not HAS_DROPBOX:
            raise ImportError("dropbox package not installed")
        
        self.token = token or DROPBOX_TOKEN
        if not self.token:
            raise ValueError("DROPBOX_ACCESS_TOKEN not set. Set via environment or pass to constructor.")
        
        self.dbx = dropbox.Dropbox(self.token)
        self.account_cache = {}  # account_id -> name
        
        # Test connection
        try:
            account = self.dbx.users_get_current_account()
            print(f"✓ Connected to Dropbox as: {account.name.display_name}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Dropbox: {e}")
    
    def scan_folder(self, folder_path: str, recursive: bool = True) -> List[Dict]:
        """Scan Dropbox folder for design files"""
        print(f"\n📁 Scanning: {folder_path}")
        print(f"   Recursive: {recursive}")
        
        files = []
        
        try:
            # List folder contents
            result = self.dbx.files_list_folder(
                folder_path,
                recursive=recursive,
                include_non_downloadable_files=False
            )
            
            # Process entries
            files.extend(self._process_entries(result.entries))
            
            # Handle pagination
            while result.has_more:
                result = self.dbx.files_list_folder_continue(result.cursor)
                files.extend(self._process_entries(result.entries))
            
            print(f"✓ Found {len(files)} design files")
            return files
            
        except dropbox.exceptions.ApiError as e:
            print(f"✗ Error scanning folder: {e}")
            return []
    
    def _process_entries(self, entries) -> List[Dict]:
        """Process folder entries and extract file metadata"""
        files = []
        
        for entry in entries:
            # Skip folders
            if isinstance(entry, FolderMetadata):
                continue
            
            # Skip non-design files
            if not isinstance(entry, FileMetadata):
                continue
            
            file_ext = Path(entry.name).suffix.lower()
            if file_ext not in SUPPORTED_EXTENSIONS:
                continue
            
            # Extract basic metadata
            file_info = {
                'file_id': entry.id,
                'path': entry.path_display,
                'name': entry.name,
                'ext': file_ext,
                'size_bytes': entry.size,
                'content_hash': entry.content_hash,
                'server_modified': entry.server_modified.isoformat(),
                'client_modified': entry.client_modified.isoformat() if hasattr(entry, 'client_modified') else None,
            }
            
            files.append(file_info)
        
        return files
    
    def get_file_revisions(self, path: str, limit: int = 10) -> List[Dict]:
        """Get revision history for a file"""
        try:
            result = self.dbx.files_list_revisions(path, limit=limit)
            
            revisions = []
            for rev in result.entries:
                revision_info = {
                    'rev': rev.rev,
                    'server_modified': rev.server_modified.isoformat(),
                    'size': rev.size,
                    'is_deleted': getattr(rev, 'is_deleted', False)
                }
                revisions.append(revision_info)
            
            return revisions
            
        except Exception as e:
            print(f"  ⚠ Could not get revisions for {path}: {e}")
            return []
    
    def get_account_name(self, account_id: str) -> str:
        """Get display name for account ID (cached)"""
        if account_id in self.account_cache:
            return self.account_cache[account_id]
        
        # For MVP, just return account_id
        # In full version, would call users_get_account
        return account_id
    
    def attribute_files(self, files: List[Dict], with_revisions: bool = False) -> List[Dict]:
        """Add attribution info to files"""
        print(f"\n🔍 Attributing {len(files)} files...")
        
        attributed = []
        for i, file in enumerate(files, 1):
            if i % 10 == 0:
                print(f"   Progress: {i}/{len(files)}")
            
            # For MVP: Use server_modified as proxy for "last editor"
            # In full version: Use revisions API
            file['creator'] = {
                'source': 'unknown',
                'note': 'MVP: Creator attribution requires Business account or XMP parsing'
            }
            
            file['last_editor'] = {
                'source': 'server_modified',
                'timestamp': file['server_modified']
            }
            
            # Optionally get revisions
            if with_revisions:
                file['revisions'] = self.get_file_revisions(file['path'])
            
            attributed.append(file)
        
        print(f"✓ Attribution complete")
        return attributed
    
    def aggregate_contributions(self, files: List[Dict]) -> Dict:
        """Aggregate contributions per person (MVP: simplified)"""
        print(f"\n📊 Aggregating contributions...")
        
        # For MVP: Count files by extension
        # In full version: Count per person
        
        stats = {
            'total_files': len(files),
            'by_extension': defaultdict(int),
            'by_folder': defaultdict(int),
            'total_size_mb': 0,
            'date_range': {
                'earliest': None,
                'latest': None
            }
        }
        
        dates = []
        for file in files:
            # Count by extension
            stats['by_extension'][file['ext']] += 1
            
            # Count by folder
            folder = str(Path(file['path']).parent)
            stats['by_folder'][folder] += 1
            
            # Total size
            stats['total_size_mb'] += file['size_bytes'] / (1024 * 1024)
            
            # Date range
            dates.append(file['server_modified'])
        
        if dates:
            stats['date_range']['earliest'] = min(dates)
            stats['date_range']['latest'] = max(dates)
        
        # Convert defaultdicts to regular dicts
        stats['by_extension'] = dict(stats['by_extension'])
        stats['by_folder'] = dict(stats['by_folder'])
        stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        
        print(f"✓ Aggregation complete")
        print(f"   Total files: {stats['total_files']}")
        print(f"   Total size: {stats['total_size_mb']} MB")
        print(f"   File types: {dict(stats['by_extension'])}")
        
        return stats
    
    def export_mining_report(self, files: List[Dict], stats: Dict, folder_path: str) -> Path:
        """Export mining report in Joju format"""
        print(f"\n💾 Exporting mining report...")
        
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mining_report_dropbox_{timestamp}.json"
        output_path = OUTPUT_DIR / filename
        
        # Create report
        report = {
            'content_type': 'mining_report',
            'target_focus': 'joju',
            'metadata': {
                'source': 'dropbox_contribution_miner',
                'version': '0.1.0-mvp',
                'timestamp': datetime.now().isoformat(),
                'folder_root': folder_path,
                'scan_type': 'mvp',
                'limitations': [
                    'Creator attribution requires Business account or XMP parsing',
                    'Editor attribution simplified (server_modified only)',
                    'No deduplication across copies/renames',
                    'No XMP metadata parsing'
                ]
            },
            'files': files,
            'statistics': stats,
            'contributors': [
                {
                    'note': 'MVP: Contributor attribution not implemented yet',
                    'next_steps': [
                        'Add Business account team_log support',
                        'Add XMP parsing for .ai/.psd files',
                        'Implement deduplication logic',
                        'Add revision-based editor tracking'
                    ]
                }
            ]
        }
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Report exported: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
        
        return output_path
    
    def mine(self, folder_path: str, with_revisions: bool = False) -> Path:
        """Main mining workflow"""
        print(f"\n{'='*60}")
        print(f"Joju Dropbox Contribution Miner - MVP")
        print(f"{'='*60}")
        
        # Step 1: Scan folder
        files = self.scan_folder(folder_path, recursive=True)
        
        if not files:
            print("\n⚠ No design files found")
            return None
        
        # Step 2: Attribute files
        files = self.attribute_files(files, with_revisions=with_revisions)
        
        # Step 3: Aggregate contributions
        stats = self.aggregate_contributions(files)
        
        # Step 4: Export report
        output_path = self.export_mining_report(files, stats, folder_path)
        
        print(f"\n{'='*60}")
        print(f"✅ Mining complete!")
        print(f"{'='*60}")
        
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Joju Dropbox Contribution Miner - MVP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a folder
  python3 dropbox_miner.py --folder "/Team/Design"
  
  # Scan with revisions (slower)
  python3 dropbox_miner.py --folder "/Team/Design" --with-revisions
  
  # Use custom token
  python3 dropbox_miner.py --folder "/Team/Design" --token "YOUR_TOKEN"

Environment Variables:
  DROPBOX_ACCESS_TOKEN - Dropbox API access token
        """
    )
    
    parser.add_argument(
        '--folder',
        required=True,
        help='Dropbox folder path to scan (e.g., "/Team/Design")'
    )
    
    parser.add_argument(
        '--with-revisions',
        action='store_true',
        help='Fetch revision history for each file (slower)'
    )
    
    parser.add_argument(
        '--token',
        help='Dropbox access token (overrides DROPBOX_ACCESS_TOKEN env var)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create miner
        miner = DropboxMiner(token=args.token)
        
        # Run mining
        output_path = miner.mine(
            folder_path=args.folder,
            with_revisions=args.with_revisions
        )
        
        if output_path:
            print(f"\n📄 View report: {output_path}")
            print(f"\n💡 Next steps:")
            print(f"   1. Review the mining report")
            print(f"   2. Import to Joju library (manual for MVP)")
            print(f"   3. Iterate on attribution logic")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
