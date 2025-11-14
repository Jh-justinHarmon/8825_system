#!/usr/bin/env python3
"""
Extract and display all action items from recent meetings
"""

from meeting_summary_pipeline import MeetingSummaryPipeline
from datetime import datetime, timedelta
from typing import List, Dict

def main():
    """Extract all action items from recent meetings"""
    pipeline = MeetingSummaryPipeline()
    
    # Get date range for past 2 weeks
    today = datetime.now().date()
    two_weeks_ago = today - timedelta(days=14)
    
    start_date = datetime.combine(two_weeks_ago, datetime.min.time())
    end_date = datetime.combine(today, datetime.max.time())
    
    # Scan for meetings
    meeting_files = pipeline.scan_for_meetings(start_date, end_date)
    
    if not meeting_files:
        print("No meetings found")
        return
    
    # Collect all action items
    all_actions = []
    
    for meeting_file in meeting_files:
        try:
            meeting = pipeline.parse_meeting_file(meeting_file)
            
            for action in meeting.action_items:
                if isinstance(action, dict):
                    all_actions.append({
                        'meeting': meeting.title,
                        'date': meeting.date,
                        'what': action.get('what', str(action)),
                        'who': action.get('who', 'TBD'),
                        'due': action.get('due', 'TBD'),
                        'priority': action.get('priority', 'medium').upper()
                    })
                else:
                    all_actions.append({
                        'meeting': meeting.title,
                        'date': meeting.date,
                        'what': str(action),
                        'who': 'TBD',
                        'due': 'TBD',
                        'priority': 'MEDIUM'
                    })
        except Exception as e:
            print(f"Error processing {meeting_file.name}: {e}")
    
    # Sort by priority and due date
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    all_actions.sort(key=lambda x: (
        priority_order.get(x['priority'], 4),
        x['due'] if x['due'] and x['due'] != 'TBD' else '9999-99-99'
    ))
    
    # Display results
    print(f"\n{'='*100}")
    print(f"COMPLETE TASK LIST - All Recent HCSS Meetings")
    print(f"{'='*100}\n")
    print(f"Total Action Items: {len(all_actions)}\n")
    
    # Group by priority
    for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        priority_tasks = [a for a in all_actions if a['priority'] == priority]
        
        if priority_tasks:
            print(f"\n{'─'*100}")
            print(f"🔴 {priority} PRIORITY ({len(priority_tasks)} items)" if priority == 'CRITICAL' else
                  f"🟠 {priority} PRIORITY ({len(priority_tasks)} items)" if priority == 'HIGH' else
                  f"🟡 {priority} PRIORITY ({len(priority_tasks)} items)" if priority == 'MEDIUM' else
                  f"🟢 {priority} PRIORITY ({len(priority_tasks)} items)")
            print(f"{'─'*100}")
            
            for i, action in enumerate(priority_tasks, 1):
                print(f"\n{i}. {action['what']}")
                print(f"   Owner: {action['who']}")
                print(f"   Due: {action['due']}")
                print(f"   From: {action['meeting']} ({action['date']})")
    
    # Summary by owner
    print(f"\n\n{'='*100}")
    print(f"TASKS BY OWNER")
    print(f"{'='*100}\n")
    
    owners = {}
    for action in all_actions:
        owner = action['who']
        if owner not in owners:
            owners[owner] = []
        owners[owner].append(action)
    
    for owner in sorted(owners.keys()):
        tasks = owners[owner]
        print(f"\n{owner} ({len(tasks)} tasks):")
        for task in tasks:
            print(f"  • {task['what']} [Due: {task['due']}] [{task['priority']}]")
    
    print(f"\n{'='*100}\n")

if __name__ == "__main__":
    main()
