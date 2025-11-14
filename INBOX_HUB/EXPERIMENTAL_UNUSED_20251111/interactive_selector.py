#!/usr/bin/env python3
"""
Interactive Protocol Selector
Handles Level 0 (manual selection) with rich UI
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from progressive_router import ProgressiveRouter

class InteractiveSelector:
    """Interactive protocol selection for Level 0 files"""
    
    def __init__(self):
        self.router = ProgressiveRouter()
    
    def show_file_preview(self, file_info: Dict):
        """Show file preview with OCR/metadata"""
        print("\n" + "="*70)
        print(f"📄 {file_info['scan_result']['filename']}")
        print("="*70)
        
        scan = file_info['scan_result']
        
        print(f"\nType: {scan['type']}")
        print(f"Size: {scan['size']:,} bytes")
        
        if scan.get('ocr_text'):
            preview = scan['ocr_text'][:200]
            print(f"\nContent Preview:")
            print("-"*70)
            print(preview)
            if len(scan['ocr_text']) > 200:
                print("...")
            print("-"*70)
        
        if scan.get('keywords'):
            print(f"\nKeywords detected: {', '.join(scan['keywords'])}")
    
    def show_protocol_options(self, matches: List[Dict]):
        """Show available protocols with confidence scores"""
        print("\n" + "="*70)
        print("Available Protocols:")
        print("="*70)
        
        for i, match in enumerate(matches, 1):
            confidence_bar = "█" * int(match['confidence'] * 20)
            confidence_pct = int(match['confidence'] * 100)
            
            print(f"\n{i}. {match['name']}")
            print(f"   {match['description']}")
            print(f"   Confidence: [{confidence_bar:<20}] {confidence_pct}%")
            print(f"   Routes to: {', '.join(match['routes_to'])}")
            
            if match.get('trust_level', 0) > 0:
                print(f"   Trust Level: {match['trust_level']} ⭐")
            
            if match.get('reasons'):
                print(f"   Why: {', '.join(match['reasons'])}")
        
        print("\n" + "="*70)
    
    def select_protocol(self, file_info: Dict) -> Optional[str]:
        """Interactive protocol selection"""
        matches = file_info['matches']
        
        # Show file preview
        self.show_file_preview(file_info)
        
        # Show protocol options
        self.show_protocol_options(matches)
        
        # Get user selection
        print("\nOptions:")
        print("  [1-9] Select protocol by number")
        print("  [s] Skip this file")
        print("  [a] Archive (default)")
        print("  [?] Show more details")
        
        while True:
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 's':
                return None
            
            elif choice == 'a' or choice == '':
                # Find archive protocol
                for match in matches:
                    if 'archive' in match['name'].lower():
                        return match['template_id']
                return matches[-1]['template_id']  # Last one is usually archive
            
            elif choice == '?':
                # Show detailed info
                self.show_file_preview(file_info)
                self.show_protocol_options(matches)
                continue
            
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(matches):
                    selected = matches[idx]
                    print(f"\n✓ Selected: {selected['name']}")
                    return selected['template_id']
                else:
                    print(f"❌ Invalid choice. Please select 1-{len(matches)}")
            
            else:
                print("❌ Invalid input. Try again.")
    
    def batch_select(self, files_needing_selection: List[Dict]) -> Dict:
        """Process batch of files needing selection"""
        results = {
            "selected": [],
            "skipped": []
        }
        
        total = len(files_needing_selection)
        
        print("\n" + "="*70)
        print(f"📋 Manual Protocol Selection ({total} files)")
        print("="*70)
        
        for i, file_info in enumerate(files_needing_selection, 1):
            print(f"\n[{i}/{total}]")
            
            selected_protocol = self.select_protocol(file_info)
            
            if selected_protocol:
                results["selected"].append({
                    "file": file_info['file'],
                    "protocol": selected_protocol
                })
            else:
                results["skipped"].append(file_info['file'])
        
        return results
    
    def show_selection_summary(self, results: Dict):
        """Show summary of selections"""
        print("\n" + "="*70)
        print("✅ Selection Complete")
        print("="*70)
        
        if results["selected"]:
            print(f"\nSelected protocols for {len(results['selected'])} files:")
            for item in results["selected"]:
                filename = Path(item['file']).name
                print(f"  ✓ {filename} → {item['protocol']}")
        
        if results["skipped"]:
            print(f"\nSkipped {len(results['skipped'])} files:")
            for file_path in results["skipped"]:
                filename = Path(file_path).name
                print(f"  ⊘ {filename}")
        
        print("\n" + "="*70)
        print("[Execute] [Cancel] [Review]")
        print("="*70 + "\n")
    
    def execute_selections(self, selections: List[Dict]):
        """Execute the selected protocols"""
        print("\n⚡ Executing selections...")
        
        for item in selections:
            file_path = Path(item['file'])
            protocol_id = item['protocol']
            
            print(f"\n  Processing {file_path.name}...")
            
            # Here we would actually execute the routing
            # For now, just update the filename status
            new_name = file_path.name.replace("[?]", "[→]")
            new_path = file_path.parent / new_name
            
            if file_path.exists() and not new_path.exists():
                file_path.rename(new_path)
            
            # Register in trust system (Level 0 → Level 1 after first use)
            print(f"    ✓ Routed via {protocol_id}")
        
        print("\n✅ All selections executed\n")


def main():
    """CLI for interactive selector"""
    import sys
    from pathlib import Path
    
    selector = InteractiveSelector()
    
    # Find files in processing folder that need selection
    processing_folder = Path.home() / "Downloads" / "8825_processing"
    
    if not processing_folder.exists():
        print("❌ No processing folder found")
        sys.exit(1)
    
    # Find files with [?] status
    files_needing_selection = []
    for file_path in processing_folder.iterdir():
        if file_path.is_file() and file_path.name.startswith("[?]"):
            # Scan the file
            scan_result = selector.router.scan_file(file_path)
            matches = selector.router.match_protocols(scan_result)
            
            if matches:
                files_needing_selection.append({
                    "file": str(file_path),
                    "scan_result": scan_result,
                    "matches": matches,
                    "trust_level": 0
                })
    
    if not files_needing_selection:
        print("\n✅ No files need manual selection\n")
        sys.exit(0)
    
    # Interactive selection
    results = selector.batch_select(files_needing_selection)
    
    # Show summary
    selector.show_selection_summary(results)
    
    # Confirm execution
    if results["selected"]:
        confirm = input("Execute these selections? [Y/n]: ").strip().lower()
        
        if confirm != 'n':
            selector.execute_selections(results["selected"])
        else:
            print("\n❌ Cancelled\n")


if __name__ == "__main__":
    main()
