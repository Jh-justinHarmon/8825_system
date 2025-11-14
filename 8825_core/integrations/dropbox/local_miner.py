#!/usr/bin/env python3
"""
Joju Local Contribution Miner - MVP
Scans local Dropbox folder for design files (no API needed)
"""

import os
import sys
import json
import argparse
import hashlib
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'utils'))
from paths import get_dropbox_root, get_user_dir

# Configuration
DROPBOX_ROOT = get_dropbox_root()
SUPPORTED_EXTENSIONS = ['.ai', '.psd', '.pdf', '.indd', '.sketch', '.fig', '.afdesign', '.afphoto']

# Output directory
OUTPUT_DIR = get_user_dir('justin_harmon') / 'joju' / 'data' / 'mining_reports'

class LocalMiner:
    def __init__(self, with_xmp: bool = False):
        if not DROPBOX_ROOT.exists():
            raise FileNotFoundError(f"Dropbox folder not found: {DROPBOX_ROOT}")
        
        self.with_xmp = with_xmp
        
        # Check if exiftool is available
        if self.with_xmp:
            try:
                subprocess.run(['exiftool', '-ver'], capture_output=True, check=True)
                print(f"✓ XMP parsing enabled (exiftool found)")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"⚠ XMP parsing disabled (exiftool not found)")
                self.with_xmp = False
        
        print(f"✓ Using Dropbox folder: {DROPBOX_ROOT}")
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate content hash for deduplication"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return f"error:{e}"
    
    def parse_xmp(self, file_path: Path) -> Dict:
        """Parse XMP metadata using exiftool"""
        if not self.with_xmp:
            return {}
        
        try:
            # Run exiftool and get JSON output
            result = subprocess.run(
                ['exiftool', '-j', '-G', str(file_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {'error': 'exiftool failed'}
            
            data = json.loads(result.stdout)[0]
            
            # Extract relevant XMP fields
            xmp = {
                'creator_tool': data.get('XMP:CreatorTool') or data.get('File:Creator'),
                'create_date': data.get('XMP:CreateDate'),
                'modify_date': data.get('XMP:ModifyDate'),
                'metadata_date': data.get('XMP:MetadataDate'),
                'title': data.get('XMP:Title'),
            }
            
            # Try to find user names from file paths in linked resources
            users = set()
            for key, value in data.items():
                if isinstance(value, str) and '/Users/' in value:
                    # Extract username from paths like /Users/wcastro/...
                    match = re.search(r'/Users/([^/]+)/', value)
                    if match:
                        users.add(match.group(1))
            
            if users:
                xmp['inferred_users'] = list(users)
            
            # Get history if available
            history = []
            if 'XMP:HistoryWhen' in data:
                whens = data['XMP:HistoryWhen']
                actions = data.get('XMP:HistoryAction', [])
                
                if isinstance(whens, str):
                    whens = [whens]
                    actions = [actions] if isinstance(actions, str) else []
                
                for i, when in enumerate(whens):
                    history.append({
                        'when': when,
                        'action': actions[i] if i < len(actions) else None
                    })
            
            if history:
                xmp['history'] = history[:5]  # Limit to first 5 entries
            
            return xmp
            
        except Exception as e:
            return {'error': str(e)}
    
    def scan_folder(self, folder_path: Path, recursive: bool = True) -> List[Dict]:
        """Scan local folder for design files"""
        print(f"\n📁 Scanning: {folder_path}")
        print(f"   Recursive: {recursive}")
        
        files = []
        
        if not folder_path.exists():
            print(f"✗ Folder not found: {folder_path}")
            return files
        
        # Scan for files
        pattern = '**/*' if recursive else '*'
        
        for ext in SUPPORTED_EXTENSIONS:
            # Find files with this extension
            found = list(folder_path.glob(f'{pattern}{ext}'))
            found.extend(list(folder_path.glob(f'{pattern}{ext.upper()}')))
            
            for file_path in found:
                # Skip hidden files and system folders
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                
                try:
                    stat = file_path.stat()
                    
                    file_info = {
                        'path': str(file_path.relative_to(DROPBOX_ROOT)),
                        'absolute_path': str(file_path),
                        'name': file_path.name,
                        'ext': file_path.suffix.lower(),
                        'size_bytes': stat.st_size,
                        'content_hash': self.calculate_file_hash(file_path),
                        'created': datetime.fromtimestamp(stat.st_birthtime).isoformat() if hasattr(stat, 'st_birthtime') else None,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                    }
                    
                    # Parse XMP for design files
                    if self.with_xmp and file_info['ext'] in ['.ai', '.psd', '.indd', '.pdf']:
                        xmp = self.parse_xmp(file_path)
                        if xmp:
                            file_info['xmp'] = xmp
                    
                    files.append(file_info)
                    
                except Exception as e:
                    print(f"  ⚠ Error processing {file_path.name}: {e}")
        
        print(f"✓ Found {len(files)} design files")
        return files
    
    def attribute_files(self, files: List[Dict]) -> List[Dict]:
        """Add attribution info to files"""
        print(f"\n🔍 Attributing {len(files)} files...")
        
        for file in files:
            # Start with filesystem data
            creator_info = {
                'source': 'filesystem',
                'timestamp': file.get('created'),
            }
            
            editor_info = {
                'source': 'filesystem',
                'timestamp': file['modified']
            }
            
            # Enhance with XMP data if available
            if 'xmp' in file:
                xmp = file['xmp']
                
                # Update creator info
                if xmp.get('inferred_users'):
                    creator_info['inferred_users'] = xmp['inferred_users']
                    creator_info['source'] = 'xmp_file_paths'
                
                if xmp.get('create_date'):
                    creator_info['xmp_create_date'] = xmp['create_date']
                
                if xmp.get('creator_tool'):
                    creator_info['tool'] = xmp['creator_tool']
                
                # Update editor info
                if xmp.get('modify_date'):
                    editor_info['xmp_modify_date'] = xmp['modify_date']
                    editor_info['source'] = 'xmp'
                
                if xmp.get('history'):
                    editor_info['edit_count'] = len(xmp['history'])
                    editor_info['last_action'] = xmp['history'][-1] if xmp['history'] else None
            
            file['creator'] = creator_info
            file['last_editor'] = editor_info
        
        print(f"✓ Attribution complete")
        if self.with_xmp:
            with_xmp_count = sum(1 for f in files if 'xmp' in f)
            print(f"   XMP parsed: {with_xmp_count}/{len(files)} files")
        
        return files
    
    def aggregate_contributions(self, files: List[Dict]) -> Dict:
        """Aggregate contributions statistics"""
        print(f"\n📊 Aggregating contributions...")
        
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
            if file['modified']:
                dates.append(file['modified'])
        
        if dates:
            stats['date_range']['earliest'] = min(dates)
            stats['date_range']['latest'] = max(dates)
        
        # Convert defaultdicts to regular dicts
        stats['by_extension'] = dict(stats['by_extension'])
        stats['by_folder'] = dict(sorted(stats['by_folder'].items(), key=lambda x: x[1], reverse=True)[:20])
        stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        
        print(f"✓ Aggregation complete")
        print(f"   Total files: {stats['total_files']}")
        print(f"   Total size: {stats['total_size_mb']} MB")
        print(f"   File types: {dict(stats['by_extension'])}")
        
        return stats
    
    def export_mining_report(self, files: List[Dict], stats: Dict, folder_path: Path) -> Path:
        """Export mining report in Joju format"""
        print(f"\n💾 Exporting mining report...")
        
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mining_report_local_{timestamp}.json"
        output_path = OUTPUT_DIR / filename
        
        # Create report
        report = {
            'content_type': 'mining_report',
            'target_focus': 'joju',
            'metadata': {
                'source': 'local_filesystem_miner',
                'version': '0.1.0-mvp',
                'timestamp': datetime.now().isoformat(),
                'folder_root': str(folder_path),
                'scan_type': 'local_filesystem',
                'dropbox_root': str(DROPBOX_ROOT),
                'limitations': [
                    'Creator attribution requires XMP parsing',
                    'Editor attribution simplified (filesystem modified date)',
                    'No Dropbox revision history',
                    'No cloud-only files (only locally synced)'
                ]
            },
            'files': files,
            'statistics': stats,
            'contributors': [
                {
                    'note': 'MVP: Contributor attribution not implemented yet',
                    'next_steps': [
                        'Add XMP parsing for .ai/.psd files',
                        'Add Git history analysis if available',
                        'Implement deduplication logic',
                        'Add Dropbox API for cloud metadata'
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
    
    def mine(self, folder_path: Path) -> Path:
        """Main mining workflow"""
        print(f"\n{'='*60}")
        print(f"Joju Local Contribution Miner")
        print(f"XMP Parsing: {'Enabled' if self.with_xmp else 'Disabled'}")
        print(f"{'='*60}")
        
        # Step 1: Scan folder
        files = self.scan_folder(folder_path, recursive=True)
        
        if not files:
            print("\n⚠ No design files found")
            return None
        
        # Step 2: Attribute files
        files = self.attribute_files(files)
        
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
        description='Joju Local Contribution Miner - MVP (No API needed)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a folder relative to Dropbox root
  python3 local_miner.py --folder "Public/Design"
  
  # Scan with absolute path
  python3 local_miner.py --folder "/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/Design"
  
  # Scan entire Dropbox
  python3 local_miner.py --folder "."

Note: Uses local Dropbox folder, no API token needed!
        """
    )
    
    parser.add_argument(
        '--folder',
        required=True,
        help='Folder path to scan (relative to Dropbox root or absolute)'
    )
    
    parser.add_argument(
        '--with-xmp',
        action='store_true',
        help='Parse XMP metadata for creator attribution (slower, requires exiftool)'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse folder path
        folder_path = Path(args.folder)
        
        # If relative, make it relative to Dropbox root
        if not folder_path.is_absolute():
            folder_path = DROPBOX_ROOT / folder_path
        
        # Validate path
        if not folder_path.exists():
            print(f"✗ Folder not found: {folder_path}")
            return 1
        
        # Create miner
        miner = LocalMiner(with_xmp=args.with_xmp)
        
        # Run mining
        output_path = miner.mine(folder_path)
        
        if output_path:
            print(f"\n📄 View report: {output_path}")
            print(f"\n💡 Next steps:")
            print(f"   1. Review the mining report")
            print(f"   2. Import to Joju library (manual for MVP)")
            print(f"   3. Add XMP parsing for better attribution")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
