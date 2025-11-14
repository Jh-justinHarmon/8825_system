#!/usr/bin/env python3
"""
POC Auditor - Analyzes sandbox POCs for promotion readiness
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))
from paths import get_system_root

SYSTEM_ROOT = get_system_root()
SANDBOX_ROOT = SYSTEM_ROOT / "sandbox"

class POCAuditor:
    def __init__(self):
        self.results = []
    
    def get_last_modified_days(self, path):
        """Get days since last modification using git"""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct", str(path)],
                cwd=SYSTEM_ROOT,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                timestamp = int(result.stdout.strip())
                last_modified = datetime.fromtimestamp(timestamp)
                days_ago = (datetime.now() - last_modified).days
                return days_ago
            return None
        except:
            return None
    
    def has_file(self, path, filename):
        """Check if directory has a specific file"""
        return (path / filename).exists()
    
    def count_python_files(self, path):
        """Count Python files in directory"""
        return len(list(path.rglob("*.py")))
    
    def check_production_use(self, poc_name):
        """Check if POC is referenced in production code"""
        try:
            # Search for references outside sandbox
            result = subprocess.run(
                ["grep", "-r", poc_name, 
                 "--include=*.py", "--include=*.sh", "--include=*.md",
                 str(SYSTEM_ROOT / "focuses"),
                 str(SYSTEM_ROOT / "shared"),
                 str(SYSTEM_ROOT / "8825_core")],
                capture_output=True,
                text=True
            )
            references = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            return references > 0, references
        except:
            return False, 0
    
    def analyze_poc(self, poc_path, category):
        """Analyze a single POC"""
        poc_name = poc_path.name
        
        # Get last modified
        days_since_modified = self.get_last_modified_days(poc_path)
        
        # Check documentation
        has_readme = self.has_file(poc_path, "README.md")
        has_requirements = self.has_file(poc_path, "requirements.txt") or self.has_file(poc_path, "package.json")
        has_tests = any(poc_path.rglob("test_*.py")) or any(poc_path.rglob("*_test.py"))
        
        # Check production use
        in_production, reference_count = self.check_production_use(poc_name)
        
        # Count code
        python_files = self.count_python_files(poc_path)
        
        # Check origin
        origin = None
        if (poc_path / ".ORIGIN").exists():
            with open(poc_path / ".ORIGIN") as f:
                origin = f.read().strip().split('\n')[0].replace("Migrated from: ", "")
        
        # Calculate promotion readiness score
        score = 0
        reasons = []
        
        # Required criteria
        if days_since_modified and days_since_modified >= 14:
            score += 25
            reasons.append("✅ Stable (14+ days since last change)")
        elif days_since_modified:
            reasons.append(f"⚠️  Recently modified ({days_since_modified} days ago, need 14+)")
        
        if has_readme:
            score += 25
            reasons.append("✅ Documented (has README)")
        else:
            reasons.append("❌ Missing README")
        
        if in_production:
            score += 30
            reasons.append(f"✅ In production ({reference_count} references)")
        else:
            reasons.append("❌ Not used in production")
        
        # Nice to have criteria
        if has_requirements:
            score += 10
            reasons.append("✅ Has requirements file")
        
        if has_tests:
            score += 10
            reasons.append("✅ Has tests")
        
        # Determine recommendation
        if score >= 80:
            recommendation = "PROMOTE to shared/ or focuses/"
            status = "🟢 READY"
        elif score >= 50:
            recommendation = "GRADUATE to sandbox/graduated/"
            status = "🟡 ALMOST"
        else:
            recommendation = "KEEP in experimental/ or DELETE if abandoned"
            status = "🔴 NOT READY"
        
        return {
            "name": poc_name,
            "category": category,
            "path": str(poc_path.relative_to(SYSTEM_ROOT)),
            "days_since_modified": days_since_modified,
            "python_files": python_files,
            "has_readme": has_readme,
            "has_requirements": has_requirements,
            "has_tests": has_tests,
            "in_production": in_production,
            "reference_count": reference_count,
            "origin": origin,
            "score": score,
            "status": status,
            "recommendation": recommendation,
            "reasons": reasons
        }
    
    def audit_sandbox(self):
        """Audit all POCs in sandbox"""
        # Check experimental
        experimental_dir = SANDBOX_ROOT / "experimental"
        if experimental_dir.exists():
            for poc_path in experimental_dir.iterdir():
                if poc_path.is_dir() and not poc_path.name.startswith('.'):
                    result = self.analyze_poc(poc_path, "experimental")
                    self.results.append(result)
        
        # Check graduated
        graduated_dir = SANDBOX_ROOT / "graduated"
        if graduated_dir.exists():
            for poc_path in graduated_dir.iterdir():
                if poc_path.is_dir() and not poc_path.name.startswith('.'):
                    result = self.analyze_poc(poc_path, "graduated")
                    # Graduated POCs should have higher standards
                    result["recommendation"] = "PROMOTE to shared/ or focuses/ (already graduated)"
                    self.results.append(result)
        
        return self.results
    
    def generate_report(self):
        """Generate human-readable report"""
        print("=" * 80)
        print("POC AUDIT REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        if not self.results:
            print("✅ No POCs found in sandbox/")
            return
        
        # Sort by score descending
        sorted_results = sorted(self.results, key=lambda x: x['score'], reverse=True)
        
        for result in sorted_results:
            print(f"{result['status']} {result['name']}")
            print(f"   Location: {result['path']}")
            print(f"   Score: {result['score']}/100")
            if result['origin']:
                print(f"   Origin: {result['origin']}")
            if result['days_since_modified']:
                print(f"   Last modified: {result['days_since_modified']} days ago")
            print(f"   Python files: {result['python_files']}")
            print()
            
            print("   Criteria:")
            for reason in result['reasons']:
                print(f"      {reason}")
            print()
            
            print(f"   📋 Recommendation: {result['recommendation']}")
            print()
            print("-" * 80)
            print()
        
        # Summary
        ready = sum(1 for r in self.results if r['status'] == '🟢 READY')
        almost = sum(1 for r in self.results if r['status'] == '🟡 ALMOST')
        not_ready = sum(1 for r in self.results if r['status'] == '🔴 NOT READY')
        
        print("SUMMARY")
        print(f"  🟢 Ready to promote: {ready}")
        print(f"  🟡 Almost ready: {almost}")
        print(f"  🔴 Not ready: {not_ready}")
        print(f"  📊 Total POCs: {len(self.results)}")
        print()
    
    def save_json_report(self, output_file):
        """Save detailed JSON report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_pocs": len(self.results),
            "summary": {
                "ready": sum(1 for r in self.results if r['status'] == '🟢 READY'),
                "almost": sum(1 for r in self.results if r['status'] == '🟡 ALMOST'),
                "not_ready": sum(1 for r in self.results if r['status'] == '🔴 NOT READY')
            },
            "pocs": self.results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report saved to: {output_file}")


if __name__ == "__main__":
    auditor = POCAuditor()
    auditor.audit_sandbox()
    auditor.generate_report()
    
    # Save JSON report
    report_file = SYSTEM_ROOT / "migrations" / f"poc_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    auditor.save_json_report(report_file)
