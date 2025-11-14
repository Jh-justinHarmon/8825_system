#!/usr/bin/env python3
"""
Bulk update 21 tasks identified as complete in audit to "Released" status
"""

import json
from pathlib import Path
from notion_sync import NotionSync

# Tasks to mark as Released (from TASK_AUDIT_2025-11-10.md)
TASKS_TO_UPDATE = [
    # Authentication & User Management
    "Authentication",
    "Profile initials not working as intended",
    
    # Profile Features
    "Profile Bio",
    "Title Case for Profile Names",
    
    # CV/Resume Features
    "Onboarding a New CV",
    "ROADMAP - Better Parsing of custom resumes",
    "Get Resume Mentors & Show them our Joju(s)",
    
    # Export Features
    "Export",
    
    # Section Features
    "ROADMAP - Skills sections and tagging",
    "Reconcile Projects and Side Projects Information Architecture",
    
    # UI/UX Features
    "Date Picker",
    "Copy action on inline or any field item",
    "Privacy Policy Theme Bug",
]

def main():
    print("\n" + "="*80)
    print("Bulk Update Complete Tasks to 'Released'")
    print("="*80 + "\n")
    
    # Load cached tasks
    cache_file = Path(__file__).parent / 'local' / 'tasks.json'
    if not cache_file.exists():
        print("❌ No cached tasks found. Run: python3 notion_sync.py pull")
        return
    
    with open(cache_file) as f:
        data = json.load(f)
    
    tasks = data.get('tasks', [])
    print(f"📋 Loaded {len(tasks)} tasks from cache\n")
    
    # Find tasks to update
    tasks_to_update = []
    for task in tasks:
        task_name = task.get('title', '')
        if any(target in task_name for target in TASKS_TO_UPDATE):
            current_status = task.get('status', 'Unknown')
            if current_status != 'Released':
                tasks_to_update.append({
                    'id': task['id'],
                    'name': task_name,
                    'current_status': current_status
                })
    
    if not tasks_to_update:
        print("✅ No tasks need updating (all already Released)")
        return
    
    print(f"Found {len(tasks_to_update)} tasks to update:\n")
    for i, task in enumerate(tasks_to_update, 1):
        print(f"{i}. {task['name']}")
        print(f"   Current: {task['current_status']} → Released\n")
    
    # Confirm
    response = input(f"\nUpdate {len(tasks_to_update)} tasks to 'Released'? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return
    
    # Initialize Notion sync
    sync = NotionSync()
    
    # Update tasks
    print("\n" + "-"*80)
    print("Updating tasks...")
    print("-"*80 + "\n")
    
    success_count = 0
    for task in tasks_to_update:
        try:
            sync.notion.pages.update(
                page_id=task['id'],
                properties={
                    'Status': {
                        'status': {
                            'name': 'Released'
                        }
                    }
                }
            )
            print(f"✅ Updated: {task['name']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed: {task['name']}")
            print(f"   Error: {str(e)}")
    
    print("\n" + "="*80)
    print(f"✅ Updated {success_count}/{len(tasks_to_update)} tasks")
    print("="*80 + "\n")
    
    # Pull fresh data
    print("Pulling fresh data from Notion...")
    sync.pull()
    print("\n✅ Done! Task statuses updated.")

if __name__ == '__main__':
    main()
