#!/usr/bin/env python3
"""
Exclusion Protocol - System files that should NEVER be processed
Critical files that must remain in Downloads for system operation
"""

import json
from pathlib import Path
from typing import List, Dict
import fnmatch

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
EXCLUSIONS_FILE = SCRIPT_DIR / "users" / "jh" / "exclusions.json"


class ExclusionProtocol:
    """Manage files that should never be processed"""
    
    # Critical system files (never touch)
    CRITICAL_PATTERNS = [
        "8825_BRAIN_TRANSPORT.json",
        "*BRAIN_TRANSPORT*.json",
        ".DS_Store",
        "*.tmp",
        "*.lock"
    ]
    
    # Sticky files (user-defined, stay in Downloads)
    STICKY_PATTERNS = [
        "sticky_*",
        "*_sticky.*"
    ]
    
    def __init__(self):
        self.exclusions_file = EXCLUSIONS_FILE
        self.exclusions_file.parent.mkdir(parents=True, exist_ok=True)
        self.exclusions = self._load_exclusions()
    
    def _load_exclusions(self) -> dict:
        """Load exclusion rules"""
        if self.exclusions_file.exists():
            with open(self.exclusions_file, 'r') as f:
                return json.load(f)
        
        # Default exclusions
        return {
            "version": "1.0",
            "critical": {
                "patterns": self.CRITICAL_PATTERNS.copy(),
                "description": "System files that must never be processed",
                "reason": "Required for system operation"
            },
            "sticky": {
                "patterns": self.STICKY_PATTERNS.copy(),
                "description": "User files that should stay in Downloads",
                "reason": "User preference"
            },
            "custom": {
                "patterns": [],
                "description": "User-defined exclusions",
                "reason": "Custom rules"
            }
        }
    
    def _save_exclusions(self):
        """Save exclusion rules"""
        with open(self.exclusions_file, 'w') as f:
            json.dump(self.exclusions, indent=2, fp=f)
    
    def should_exclude(self, file_path: Path) -> Dict:
        """
        Check if file should be excluded from processing
        Returns: {excluded, reason, category}
        """
        filename = file_path.name
        
        # Check critical patterns
        for pattern in self.exclusions["critical"]["patterns"]:
            if fnmatch.fnmatch(filename, pattern):
                return {
                    "excluded": True,
                    "reason": "Critical system file",
                    "category": "critical",
                    "pattern": pattern,
                    "description": self.exclusions["critical"]["description"]
                }
        
        # Check sticky patterns
        for pattern in self.exclusions["sticky"]["patterns"]:
            if fnmatch.fnmatch(filename, pattern):
                return {
                    "excluded": True,
                    "reason": "Sticky file (stays in Downloads)",
                    "category": "sticky",
                    "pattern": pattern,
                    "description": self.exclusions["sticky"]["description"]
                }
        
        # Check custom patterns
        for pattern in self.exclusions["custom"]["patterns"]:
            if fnmatch.fnmatch(filename, pattern):
                return {
                    "excluded": True,
                    "reason": "Custom exclusion rule",
                    "category": "custom",
                    "pattern": pattern,
                    "description": self.exclusions["custom"]["description"]
                }
        
        return {
            "excluded": False,
            "reason": None,
            "category": None
        }
    
    def filter_batch(self, files: List[Path]) -> Dict:
        """Filter batch of files, separating excluded from processable"""
        results = {
            "processable": [],
            "excluded": {
                "critical": [],
                "sticky": [],
                "custom": []
            }
        }
        
        for file_path in files:
            check = self.should_exclude(file_path)
            
            if check["excluded"]:
                category = check["category"]
                results["excluded"][category].append({
                    "file": str(file_path),
                    "filename": file_path.name,
                    "reason": check["reason"],
                    "pattern": check["pattern"]
                })
            else:
                results["processable"].append(file_path)
        
        return results
    
    def add_exclusion(self, pattern: str, category: str = "custom"):
        """Add new exclusion pattern"""
        if category not in ["critical", "sticky", "custom"]:
            print(f"❌ Invalid category: {category}")
            return
        
        if pattern not in self.exclusions[category]["patterns"]:
            self.exclusions[category]["patterns"].append(pattern)
            self._save_exclusions()
            print(f"✅ Added exclusion: {pattern} ({category})")
        else:
            print(f"⚠️  Pattern already exists: {pattern}")
    
    def remove_exclusion(self, pattern: str, category: str = "custom"):
        """Remove exclusion pattern"""
        if category not in ["critical", "sticky", "custom"]:
            print(f"❌ Invalid category: {category}")
            return
        
        if pattern in self.exclusions[category]["patterns"]:
            self.exclusions[category]["patterns"].remove(pattern)
            self._save_exclusions()
            print(f"✅ Removed exclusion: {pattern}")
        else:
            print(f"⚠️  Pattern not found: {pattern}")
    
    def show_exclusions(self):
        """Display all exclusion rules"""
        print("\n" + "="*70)
        print("🚫 Exclusion Rules")
        print("="*70)
        
        for category in ["critical", "sticky", "custom"]:
            patterns = self.exclusions[category]["patterns"]
            if patterns:
                print(f"\n{category.upper()} ({len(patterns)} patterns):")
                print(f"  {self.exclusions[category]['description']}")
                for pattern in patterns:
                    print(f"    • {pattern}")
        
        print("="*70 + "\n")
    
    def show_filter_report(self, results: Dict):
        """Show filtering report"""
        print("\n" + "="*70)
        print("🔍 Exclusion Filter Report")
        print("="*70)
        
        total_excluded = sum(len(results["excluded"][cat]) for cat in results["excluded"])
        total_processable = len(results["processable"])
        total = total_excluded + total_processable
        
        print(f"\nScanned: {total} files")
        print(f"  ✓ Processable: {total_processable}")
        print(f"  🚫 Excluded: {total_excluded}")
        
        for category in ["critical", "sticky", "custom"]:
            excluded = results["excluded"][category]
            if excluded:
                print(f"\n{category.upper()} Exclusions ({len(excluded)}):")
                for item in excluded:
                    print(f"  🚫 {item['filename']}")
                    print(f"     Reason: {item['reason']}")
                    print(f"     Pattern: {item['pattern']}")
        
        if results["processable"]:
            print(f"\nProcessable Files ({len(results['processable'])}):")
            for file_path in results["processable"]:
                print(f"  ✓ {file_path.name}")
        
        print("="*70 + "\n")


def main():
    """CLI for exclusion protocol"""
    import sys
    
    protocol = ExclusionProtocol()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  exclusion_protocol.py filter <directory>")
        print("  exclusion_protocol.py check <file>")
        print("  exclusion_protocol.py list")
        print("  exclusion_protocol.py add <pattern> [category]")
        print("  exclusion_protocol.py remove <pattern> [category]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "filter":
        if len(sys.argv) < 3:
            print("Usage: exclusion_protocol.py filter <directory>")
            sys.exit(1)
        
        directory = Path(sys.argv[2])
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        
        files = [f for f in directory.iterdir() if f.is_file()]
        results = protocol.filter_batch(files)
        protocol.show_filter_report(results)
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("Usage: exclusion_protocol.py check <file>")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        result = protocol.should_exclude(file_path)
        
        print(f"\nFile: {file_path.name}")
        if result["excluded"]:
            print(f"🚫 Excluded: {result['reason']}")
            print(f"   Category: {result['category']}")
            print(f"   Pattern: {result['pattern']}")
        else:
            print("✓ Not excluded (processable)")
    
    elif command == "list":
        protocol.show_exclusions()
    
    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: exclusion_protocol.py add <pattern> [category]")
            sys.exit(1)
        
        pattern = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "custom"
        protocol.add_exclusion(pattern, category)
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: exclusion_protocol.py remove <pattern> [category]")
            sys.exit(1)
        
        pattern = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "custom"
        protocol.remove_exclusion(pattern, category)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
