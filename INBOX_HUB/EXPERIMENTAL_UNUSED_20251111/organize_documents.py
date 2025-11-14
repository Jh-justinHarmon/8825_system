#!/usr/bin/env python3
"""
Document Folder Organization

Principle: Light and easy to digest
- Word docs at top level (main content)
- Tech files hidden in [_TECH] folder (md, json, archived, errored)
- Other folders use numbers or different case to stand out
- Simple structures that appear obviously different

Structure:
/documents/
├── [_TECH]/           # Hidden tech files (starts with underscore)
│   ├── archived/
│   ├── errored/
│   ├── markdown/
│   └── json/
├── 01_ACTIVE/         # Numbered folders
├── 02_PROJECTS/
├── Document1.docx     # Word docs at top level
└── Document2.docx
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_documents(doc_folder, dry_run=True):
    """Organize document folder by file type"""
    doc_path = Path(doc_folder)
    
    if not doc_path.exists():
        print(f"❌ Folder not found: {doc_path}")
        return
    
    print(f"\n📁 Organizing: {doc_path}")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")
    
    # Create tech folder structure
    tech_folder = doc_path / "_TECH"
    tech_subfolders = {
        'archived': tech_folder / 'archived',
        'errored': tech_folder / 'errored',
        'markdown': tech_folder / 'markdown',
        'json': tech_folder / 'json',
        'logs': tech_folder / 'logs'
    }
    
    # File type mappings
    file_mappings = {
        '.md': 'markdown',
        '.json': 'json',
        '.log': 'logs',
        '.txt': 'logs',  # Assuming txt files are logs
    }
    
    # Scan files
    moves = []
    
    for item in doc_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            
            # Check if it should be moved to tech folder
            if ext in file_mappings:
                target_subfolder = tech_subfolders[file_mappings[ext]]
                moves.append((item, target_subfolder / item.name, 'tech'))
            
            # Check for archived/errored in filename
            elif 'archived' in item.name.lower() or 'archive' in item.name.lower():
                target_subfolder = tech_subfolders['archived']
                moves.append((item, target_subfolder / item.name, 'archived'))
            
            elif 'error' in item.name.lower() or 'failed' in item.name.lower():
                target_subfolder = tech_subfolders['errored']
                moves.append((item, target_subfolder / item.name, 'errored'))
            
            # Word docs stay at top level
            elif ext in ['.docx', '.doc']:
                print(f"✅ {item.name} - Keep at top level (Word doc)")
            
            # PDFs stay at top level for now
            elif ext == '.pdf':
                print(f"📄 {item.name} - Keep at top level (PDF)")
            
            else:
                print(f"❓ {item.name} - Unknown type, keeping at top level")
    
    # Show planned moves
    if moves:
        print(f"\n📦 Planned moves ({len(moves)}):\n")
        for source, target, category in moves:
            print(f"   {source.name}")
            print(f"      → _TECH/{category}/{source.name}")
    
    # Execute moves
    if not dry_run and moves:
        print(f"\n🚀 Executing moves...")
        
        # Create folders
        for subfolder in tech_subfolders.values():
            subfolder.mkdir(parents=True, exist_ok=True)
        
        # Move files
        for source, target, category in moves:
            try:
                shutil.move(str(source), str(target))
                print(f"   ✅ Moved: {source.name}")
            except Exception as e:
                print(f"   ❌ Error moving {source.name}: {e}")
    
    # Show final structure
    print(f"\n📊 Final Structure:")
    print(f"   /documents/")
    print(f"   ├── _TECH/           # {sum(1 for s,t,c in moves)} files")
    
    for name, folder in tech_subfolders.items():
        count = sum(1 for s,t,c in moves if c == name)
        if count > 0:
            print(f"   │   ├── {name}/    # {count} files")
    
    # Count remaining top-level files
    word_docs = list(doc_path.glob('*.docx')) + list(doc_path.glob('*.doc'))
    pdfs = list(doc_path.glob('*.pdf'))
    
    print(f"   ├── *.docx         # {len(word_docs)} Word docs")
    print(f"   └── *.pdf          # {len(pdfs)} PDFs")
    
    print(f"\n💡 Principle: Light and easy to digest")
    print(f"   - Word docs visible at top level")
    print(f"   - Tech files hidden in _TECH/")
    print(f"   - Folders use _ or numbers to stand out")

def main():
    print("\n" + "="*80)
    print("DOCUMENT FOLDER ORGANIZATION")
    print("="*80)
    
    # Default document locations
    doc_folders = [
        Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/intake/documents",
        Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/processed/documents",
    ]
    
    for folder in doc_folders:
        if folder.exists():
            organize_documents(folder, dry_run=True)
            
            # Ask to execute
            response = input(f"\n🚀 Execute organization for {folder.name}? (y/n): ")
            if response.lower() == 'y':
                organize_documents(folder, dry_run=False)
            
            print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
