#!/usr/bin/env python3
"""
Rhino Contribution Scanner
Scans .3dm files to generate portfolio metrics and contribution stats
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

try:
    import rhino3dm
    RHINO3DM_AVAILABLE = True
except ImportError:
    RHINO3DM_AVAILABLE = False
    print("⚠️  rhino3dm not installed. Install with: pip install rhino3dm")
    print("   Will use file system metadata only.\n")


class RhinoContributionScanner:
    """Scan Rhino files and generate contribution statistics"""
    
    def __init__(self, archive_path):
        self.archive_path = Path(archive_path)
        self.stats = {
            "total_files": 0,
            "by_year": defaultdict(int),
            "by_month": defaultdict(int),
            "by_category": defaultdict(int),
            "file_list": [],
            "date_range": {"earliest": None, "latest": None},
            "total_size_mb": 0
        }
    
    def scan(self):
        """Scan directory for .3dm files"""
        print(f"🔍 Scanning: {self.archive_path}\n")
        
        if not self.archive_path.exists():
            print(f"❌ Path not found: {self.archive_path}")
            return
        
        # Find all .3dm files
        rhino_files = list(self.archive_path.rglob("*.3dm"))
        
        if not rhino_files:
            print("❌ No .3dm files found")
            return
        
        print(f"📁 Found {len(rhino_files)} Rhino files\n")
        
        for file_path in rhino_files:
            self._process_file(file_path)
        
        self._calculate_metrics()
        self._generate_report()
        self._save_json()
    
    def _process_file(self, file_path):
        """Process individual Rhino file"""
        try:
            # Get file stats
            stat = file_path.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            size_mb = stat.st_size / (1024 * 1024)
            
            # Categorize by folder structure
            category = self._categorize_file(file_path)
            
            # Update stats
            self.stats["total_files"] += 1
            self.stats["by_year"][modified_time.year] += 1
            self.stats["by_month"][modified_time.strftime("%Y-%m")] += 1
            self.stats["by_category"][category] += 1
            self.stats["total_size_mb"] += size_mb
            
            # Track date range
            if not self.stats["date_range"]["earliest"] or modified_time < self.stats["date_range"]["earliest"]:
                self.stats["date_range"]["earliest"] = modified_time
            if not self.stats["date_range"]["latest"] or modified_time > self.stats["date_range"]["latest"]:
                self.stats["date_range"]["latest"] = modified_time
            
            # Store file info
            file_info = {
                "name": file_path.name,
                "path": str(file_path.relative_to(self.archive_path)),
                "modified": modified_time.isoformat(),
                "size_mb": round(size_mb, 2),
                "category": category
            }
            
            # Try to extract Rhino metadata if available
            if RHINO3DM_AVAILABLE:
                try:
                    file3dm = rhino3dm.File3dm.Read(str(file_path))
                    if file3dm:
                        file_info["rhino_version"] = str(file3dm.Settings.ModelUnitSystem)
                        file_info["object_count"] = len(file3dm.Objects)
                except Exception as e:
                    file_info["metadata_error"] = str(e)
            
            self.stats["file_list"].append(file_info)
            
        except Exception as e:
            print(f"⚠️  Error processing {file_path.name}: {e}")
    
    def _categorize_file(self, file_path):
        """Categorize file based on path"""
        path_str = str(file_path).lower()
        
        # Check for common categories
        if any(x in path_str for x in ["eyewear", "glasses", "sunglass", "optical"]):
            return "Eyewear"
        elif any(x in path_str for x in ["watch", "timepiece"]):
            return "Watches"
        elif any(x in path_str for x in ["nike", "costa", "dragon", "fossil", "marchon"]):
            # Extract brand name
            for brand in ["nike", "costa", "dragon", "fossil", "marchon", "shinola"]:
                if brand in path_str:
                    return brand.title()
        elif "prototype" in path_str or "proto" in path_str:
            return "Prototypes"
        elif "concept" in path_str:
            return "Concepts"
        else:
            return "Other"
    
    def _calculate_metrics(self):
        """Calculate portfolio metrics"""
        if not self.stats["date_range"]["earliest"]:
            return
        
        earliest = self.stats["date_range"]["earliest"]
        latest = self.stats["date_range"]["latest"]
        
        years_span = (latest - earliest).days / 365.25
        self.stats["years_of_experience"] = round(years_span, 1)
        
        # Calculate average files per year
        if years_span > 0:
            self.stats["avg_files_per_year"] = round(self.stats["total_files"] / years_span, 1)
    
    def _generate_report(self):
        """Generate human-readable report"""
        print("\n" + "="*60)
        print("📊 RHINO CONTRIBUTION REPORT")
        print("="*60 + "\n")
        
        # Overview
        print("📈 OVERVIEW")
        print(f"   Total Rhino Files: {self.stats['total_files']}")
        print(f"   Total Size: {self.stats['total_size_mb']:.1f} MB")
        
        if self.stats["date_range"]["earliest"]:
            print(f"   Date Range: {self.stats['date_range']['earliest'].strftime('%Y-%m-%d')} to {self.stats['date_range']['latest'].strftime('%Y-%m-%d')}")
            print(f"   Years of Experience: {self.stats.get('years_of_experience', 0)} years")
            print(f"   Avg Files/Year: {self.stats.get('avg_files_per_year', 0)}")
        
        # By Category
        print("\n📂 BY CATEGORY")
        for category, count in sorted(self.stats["by_category"].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.stats["total_files"]) * 100
            print(f"   {category}: {count} files ({percentage:.1f}%)")
        
        # By Year
        print("\n📅 BY YEAR")
        for year in sorted(self.stats["by_year"].keys()):
            count = self.stats["by_year"][year]
            bar = "█" * (count // 5 + 1)
            print(f"   {year}: {count:3d} files {bar}")
        
        # Portfolio Metrics
        print("\n💼 PORTFOLIO METRICS")
        print(f"   ✓ {self.stats.get('years_of_experience', 0)} years of Rhino 3D experience")
        print(f"   ✓ {self.stats['total_files']} products/models designed")
        
        categories = list(self.stats["by_category"].keys())
        if len(categories) > 1:
            print(f"   ✓ Range of work: {', '.join(categories[:3])}")
        
        print("\n" + "="*60)
    
    def _save_json(self):
        """Save stats to JSON file"""
        output_file = Path("rhino_contribution_stats.json")
        
        # Convert defaultdict to dict and datetime to string
        stats_json = {
            "total_files": self.stats["total_files"],
            "total_size_mb": round(self.stats["total_size_mb"], 2),
            "years_of_experience": self.stats.get("years_of_experience", 0),
            "avg_files_per_year": self.stats.get("avg_files_per_year", 0),
            "by_year": dict(self.stats["by_year"]),
            "by_month": dict(self.stats["by_month"]),
            "by_category": dict(self.stats["by_category"]),
            "date_range": {
                "earliest": self.stats["date_range"]["earliest"].isoformat() if self.stats["date_range"]["earliest"] else None,
                "latest": self.stats["date_range"]["latest"].isoformat() if self.stats["date_range"]["latest"] else None
            },
            "file_list": self.stats["file_list"],
            "generated": datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(stats_json, f, indent=2)
        
        print(f"\n💾 Stats saved to: {output_file}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python rhino_contribution_scanner.py <path_to_archive>")
        print("\nExample:")
        print('  python rhino_contribution_scanner.py "/path/to/Jh-ARCHV"')
        sys.exit(1)
    
    archive_path = sys.argv[1]
    scanner = RhinoContributionScanner(archive_path)
    scanner.scan()


if __name__ == "__main__":
    main()
