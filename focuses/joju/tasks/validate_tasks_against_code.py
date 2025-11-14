#!/usr/bin/env python3
"""
Validate all Joju tasks against actual codebase
Check for evidence of completion in code
"""

import json
import os
from pathlib import Path
from typing import List, Dict

# Joju codebase location
JOJU_CODE = Path("/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/joju")

def check_file_exists(patterns: List[str]) -> bool:
    """Check if any files matching patterns exist in codebase"""
    for pattern in patterns:
        matches = list(JOJU_CODE.rglob(pattern))
        if matches:
            return True
    return False

def check_code_content(search_terms: List[str]) -> List[str]:
    """Search for terms in TypeScript/JavaScript files"""
    found_in = []
    for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
        for file in JOJU_CODE.rglob(ext):
            try:
                content = file.read_text()
                for term in search_terms:
                    if term.lower() in content.lower():
                        found_in.append(str(file.relative_to(JOJU_CODE)))
                        break
            except:
                pass
    return found_in

def analyze_task(task: Dict) -> Dict:
    """Analyze if task shows evidence of completion"""
    title = task.get('title', '')
    status = task.get('status', '')
    
    # Skip already released/archived
    if status in ['Released', 'Archived']:
        return None
    
    evidence = {
        'title': title,
        'current_status': status,
        'files_found': [],
        'code_evidence': [],
        'recommendation': 'Keep current status'
    }
    
    # Authentication tasks
    if 'authentication' in title.lower() or 'auth' in title.lower():
        files = check_code_content(['auth', 'login', 'AuthCallback'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # Profile tasks
    elif 'profile' in title.lower():
        files = check_code_content(['profile', 'ProfileEdit', 'ProfileView'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # CV/Resume tasks
    elif any(term in title.lower() for term in ['cv', 'resume', 'export']):
        files = check_code_content(['CVView', 'CVDocument', 'Export', 'PDF'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # Skills/Sections
    elif 'skill' in title.lower() or 'section' in title.lower():
        files = check_code_content(['SkillsSection', 'Section'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # UI components
    elif any(term in title.lower() for term in ['date picker', 'inline', 'edit']):
        files = check_code_content(['InlineDateEdit', 'InlineEdit', 'DatePicker'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # Privacy/Legal
    elif 'privacy' in title.lower() or 'policy' in title.lower():
        files = check_code_content(['PrivacyPolicy', 'privacy'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # Theme/Dark mode
    elif 'theme' in title.lower() or 'dark mode' in title.lower():
        files = check_code_content(['ThemeToggle', 'ThemeProvider', 'dark'])
        if files:
            evidence['files_found'] = files[:3]
            evidence['recommendation'] = 'Mark as Released'
    
    # Only return if we found evidence
    if evidence['files_found'] or evidence['recommendation'] != 'Keep current status':
        return evidence
    return None

def main():
    print("\n" + "="*80)
    print("JOJU TASK VALIDATION AGAINST CODEBASE")
    print("="*80 + "\n")
    
    # Load tasks
    cache_file = Path(__file__).parent / 'local' / 'tasks.json'
    with open(cache_file) as f:
        data = json.load(f)
    
    tasks = data.get('tasks', [])
    print(f"📋 Analyzing {len(tasks)} tasks...\n")
    
    # Analyze all tasks
    promotable = []
    for task in tasks:
        evidence = analyze_task(task)
        if evidence and evidence['recommendation'] == 'Mark as Released':
            promotable.append(evidence)
    
    print(f"\n{'='*80}")
    print(f"FOUND {len(promotable)} TASKS WITH EVIDENCE OF COMPLETION")
    print(f"{'='*80}\n")
    
    # Group by current status
    by_status = {}
    for task in promotable:
        status = task['current_status']
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(task)
    
    # Print results
    for status, tasks in sorted(by_status.items()):
        print(f"\n## {status} → Released ({len(tasks)} tasks)\n")
        for task in tasks:
            print(f"**{task['title']}**")
            if task['files_found']:
                print(f"   Evidence: {', '.join(task['files_found'][:2])}")
            print()
    
    # Save report
    report_file = Path(__file__).parent / 'VALIDATION_REPORT.json'
    with open(report_file, 'w') as f:
        json.dump({
            'total_analyzed': len(tasks),
            'promotable_count': len(promotable),
            'promotable_tasks': promotable,
            'by_status': {k: len(v) for k, v in by_status.items()}
        }, f, indent=2)
    
    print(f"\n✅ Report saved to: {report_file}\n")
    
    return promotable

if __name__ == '__main__':
    main()
