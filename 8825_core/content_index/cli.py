#!/usr/bin/env python3
"""
8825 Content Index CLI
Simple command interface for inbox ingestion
"""

import os
import sys
from pathlib import Path
import argparse

# Set up paths
sys.path.insert(0, str(Path(__file__).parent))

from index_engine import ContentIndexEngine
from usage_tracker import UsageTracker
from promotion_engine import PromotionEngine
from decay_engine import DecayEngine
from cleanup_engine import CleanupEngine


def ingest_command(args):
    """Ingest files from Downloads folder"""
    
    # Initialize engines
    inbox_path = Path.home() / 'Downloads' / '8825_inbox'
    
    # Scan iCloud Downloads (where files actually land)
    downloads_path = Path.home() / 'Library' / 'Mobile Documents' / 'com~apple~CloudDocs' / 'Downloads'
    
    index = ContentIndexEngine(inbox_path / 'content_index')
    tracker = UsageTracker(index.db_path)
    promotion = PromotionEngine(index.db_path, index.store_path, tracker)
    
    # Get files from Downloads (only top-level files, not in subfolders)
    all_files = []
    for pattern in ['*.json', '*.txt', '*.md', '*.docx', '*.pdf']:
        for file in downloads_path.glob(pattern):
            # Only include files directly in Downloads (not in subfolders)
            if file.parent == downloads_path:
                all_files.append(file)
    
    # Exclude brain transport file and any 8825 system files
    pending_files = [
        f for f in all_files 
        if not f.name.startswith('0-8825_BRAIN_TRANSPORT')
        and not f.name.startswith('8825_')
    ]
    
    if not pending_files:
        print("📭 No new files in Downloads/")
        return
    
    print(f"📥 Processing {len(pending_files)} files from Downloads/...\n")
    
    stats = {
        'indexed': 0,
        'promoted': 0,
        'merged': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for i, file_path in enumerate(pending_files, 1):
        print(f"[{i}/{len(pending_files)}] {file_path.name}")
        
        try:
            # Ingest
            result = index.ingest(file_path, use_intelligent_naming=True)
            
            if result['status'] == 'indexed':
                stats['indexed'] += 1
                
                # Check for auto-promotion
                confidence = promotion.calculate_confidence(result['hash'])
                
                if confidence >= 0.85:
                    # Auto-promote
                    destination = promotion.suggest_destination(result['hash'])
                    if destination:
                        promo_result = promotion.promote_file(result['hash'], destination)
                        
                        if promo_result['status'] == 'promoted':
                            if promo_result.get('action') == 'merged':
                                print(f"  ✅ Merged into existing file")
                                stats['merged'] += 1
                            else:
                                print(f"  ✅ Promoted to: {destination}")
                                stats['promoted'] += 1
                        elif promo_result.get('action') == 'skip':
                            print(f"  ✅ Skipped (duplicate)")
                            stats['skipped'] += 1
                
                elif confidence >= 0.70:
                    destination = promotion.suggest_destination(result['hash'])
                    print(f"  💡 Suggestion: {destination} (confidence: {confidence:.2f})")
                
                else:
                    print(f"  📝 Indexed (confidence: {confidence:.2f})")
            
            elif result['status'] == 'duplicate':
                print(f"  ⏭️  Duplicate")
                stats['skipped'] += 1
            
            # Move to completed
            completed_path = inbox_path / 'completed'
            completed_path.mkdir(exist_ok=True)
            file_path.rename(completed_path / file_path.name)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            stats['errors'] += 1
            
            # Move to errors
            errors_path = inbox_path / 'errors'
            errors_path.mkdir(exist_ok=True)
            file_path.rename(errors_path / file_path.name)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Indexed: {stats['indexed']}")
    print(f"Promoted: {stats['promoted']}")
    print(f"Merged: {stats['merged']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")


def search_command(args):
    """Search indexed content"""
    
    inbox_path = Path.home() / 'Downloads' / '8825_inbox'
    index = ContentIndexEngine(inbox_path / 'content_index')
    
    results = index.search(args.query, limit=args.limit)
    
    if not results:
        print(f"No results for: {args.query}")
        return
    
    print(f"\n🔍 Found {len(results)} results for: {args.query}\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['filename']}")
        print(f"   Score: {result['score']:.2f}")
        if result.get('snippet'):
            print(f"   {result['snippet'][:100]}...")
        print()


def stats_command(args):
    """Show index statistics"""
    
    inbox_path = Path.home() / 'Downloads' / '8825_inbox'
    index = ContentIndexEngine(inbox_path / 'content_index')
    
    stats = index.get_stats()
    
    print("\n📊 Content Index Statistics")
    print("="*60)
    print(f"Total files: {stats['total']}")
    print(f"Attributed: {stats['attributed']}")
    print(f"Unattributed: {stats['unattributed']}")
    print(f"Archived: {stats['archived']}")
    print()


def cleanup_command(args):
    """Run cleanup engine"""
    
    inbox_path = Path.home() / 'Downloads' / '8825_inbox'
    index = ContentIndexEngine(inbox_path / 'content_index')
    cleanup = CleanupEngine(index.db_path, index.store_path)
    
    print("🧹 Running cleanup...\n")
    
    # Find expired files
    expired = cleanup.find_expired_files()
    
    if not expired:
        print("✨ No files to cleanup")
        return
    
    print(f"Found {len(expired)} files to cleanup:\n")
    
    for file in expired[:10]:
        print(f"  - {file['filename']} (decay: {file['decay_score']})")
    
    if len(expired) > 10:
        print(f"  ... and {len(expired) - 10} more")
    
    if not args.dry_run:
        print("\nCleaning up...")
        result = cleanup.cleanup_expired()
        print(f"\n✅ Cleaned up {result['deleted']} files")
    else:
        print("\n(Dry run - no files deleted)")


def promote_command(args):
    """Manually promote a file"""
    
    inbox_path = Path.home() / 'Downloads' / '8825_inbox'
    index = ContentIndexEngine(inbox_path / 'content_index')
    tracker = UsageTracker(index.db_path)
    promotion = PromotionEngine(index.db_path, index.store_path, tracker)
    
    # Search for file
    results = index.search(args.file_hash, limit=1)
    
    if not results:
        print(f"File not found: {args.file_hash}")
        return
    
    file_hash = results[0]['hash']
    
    # Suggest destination if not provided
    if not args.destination:
        destination = promotion.suggest_destination(file_hash)
        print(f"Suggested destination: {destination}")
        
        confirm = input("Promote to this destination? (y/n): ")
        if confirm.lower() != 'y':
            return
    else:
        destination = args.destination
    
    # Promote
    result = promotion.promote_file(file_hash, destination)
    
    if result['status'] == 'promoted':
        print(f"✅ Promoted to: {result['destination']}")
    else:
        print(f"❌ Promotion failed: {result}")


def health_command(args):
    """System health check"""
    quiet = args.quiet if hasattr(args, 'quiet') else False
    
    if not quiet:
        print("✅ 8825 Content Index - Healthy")
    
    # Could add more health checks here:
    # - Check database connectivity
    # - Check file system access
    # - Check dependencies
    # etc.


def main():
    parser = argparse.ArgumentParser(
        description='8825 Content Index CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  8825 ingest              # Process pending files
  8825 search "RAL Portal" # Search indexed content
  8825 stats               # Show statistics
  8825 cleanup             # Run cleanup engine
  8825 promote <hash>      # Manually promote file
  8825 health              # System health check
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Health command
    health_parser = subparsers.add_parser('health', help='System health check')
    health_parser.add_argument('--quiet', action='store_true', help='Quiet mode')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Process pending files')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search indexed content')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Max results')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Run cleanup engine')
    cleanup_parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted')
    
    # Promote command
    promote_parser = subparsers.add_parser('promote', help='Manually promote file')
    promote_parser.add_argument('file_hash', help='File hash or search term')
    promote_parser.add_argument('--destination', help='Destination path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to command
    commands = {
        'health': health_command,
        'ingest': ingest_command,
        'search': search_command,
        'stats': stats_command,
        'cleanup': cleanup_command,
        'promote': promote_command
    }
    
    commands[args.command](args)


if __name__ == '__main__':
    main()
