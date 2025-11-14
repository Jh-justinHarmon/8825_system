#!/usr/bin/env python3
"""
Bulk promote 22 validated tasks to Released status
Based on VALIDATION_REPORT.json
"""

import json
from pathlib import Path
from notion_sync import NotionSync

def main():
    print("\n" + "="*80)
    print("BULK PROMOTE VALIDATED TASKS TO RELEASED")
    print("="*80 + "\n")
    
    # Load validation report
    report_file = Path(__file__).parent / 'VALIDATION_REPORT.json'
    if not report_file.exists():
        print("❌ No validation report found. Run validate_tasks_against_code.py first")
        return
    
    with open(report_file) as f:
        report = json.load(f)
    
    promotable = report['promotable_tasks']
    print(f"📋 Found {len(promotable)} tasks to promote\n")
    
    # Group by status
    by_status = {}
    for task in promotable:
        status = task['current_status']
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(task)
    
    # Show summary
    print("PROMOTION SUMMARY:\n")
    for status, tasks in sorted(by_status.items()):
        print(f"  {status} → Released: {len(tasks)} tasks")
    print()
    
    # Confirm
    response = input(f"Promote {len(promotable)} tasks to 'Released'? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return
    
    # Initialize Notion sync
    print("\nInitializing Notion connection...")
    sync = NotionSync()
    
    # Load current tasks to get IDs
    cache_file = Path(__file__).parent / 'local' / 'tasks.json'
    with open(cache_file) as f:
        data = json.load(f)
    tasks = {t['title']: t['id'] for t in data['tasks']}
    
    # Update tasks
    print("\n" + "-"*80)
    print("Promoting tasks...")
    print("-"*80 + "\n")
    
    success_count = 0
    failed = []
    
    for task in promotable:
        title = task['title']
        if title not in tasks:
            print(f"⚠️  Skipped: {title} (not found in cache)")
            failed.append(title)
            continue
        
        try:
            sync.notion.pages.update(
                page_id=tasks[title],
                properties={
                    'Status': {
                        'status': {
                            'name': 'Released'
                        }
                    }
                }
            )
            print(f"✅ {title}")
            success_count += 1
        except Exception as e:
            print(f"❌ {title}")
            print(f"   Error: {str(e)}")
            failed.append(title)
    
    print("\n" + "="*80)
    print(f"✅ Promoted {success_count}/{len(promotable)} tasks")
    if failed:
        print(f"❌ Failed: {len(failed)} tasks")
        for title in failed:
            print(f"   - {title}")
    print("="*80 + "\n")
    
    # Pull fresh data
    print("Pulling fresh data from Notion...")
    sync.pull()
    print("\n✅ Done! Task statuses updated.")
    
    # Show new stats
    with open(cache_file) as f:
        data = json.load(f)
    
    by_status = {}
    for task in data['tasks']:
        status = task['status']
        by_status[status] = by_status.get(status, 0) + 1
    
    print("\nNEW TASK BREAKDOWN:")
    for status in sorted(by_status.keys()):
        print(f"  {status}: {by_status[status]}")
    
    released = by_status.get('Released', 0)
    total = len(data['tasks'])
    pct = (released / total * 100) if total > 0 else 0
    print(f"\n📊 Completion: {released}/{total} ({pct:.1f}%)")

if __name__ == '__main__':
    main()
