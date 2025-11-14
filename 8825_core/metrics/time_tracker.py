#!/usr/bin/env python3
"""
Build Time & User Time Savings Tracker
Tracks actual vs estimated build times and user time savings
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

TRACKER_FILE = Path(__file__).parent / "build_time_tracker.json"

# Make findable system-wide
SYSTEM_ROOT = Path(__file__).parent.parent.parent
if not TRACKER_FILE.exists():
    # Check if it exists elsewhere in system
    for possible_location in [
        SYSTEM_ROOT / "8825_core" / "metrics" / "build_time_tracker.json",
        SYSTEM_ROOT / "INBOX_HUB" / "build_time_tracker.json",
        Path.home() / ".8825" / "build_time_tracker.json"
    ]:
        if possible_location.exists():
            TRACKER_FILE = possible_location
            break


class TimeTracker:
    """Track build times and user savings"""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """Load tracking data"""
        if TRACKER_FILE.exists():
            with open(TRACKER_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        """Save tracking data"""
        with open(TRACKER_FILE, 'w') as f:
            json.dump(self.data, indent=2, fp=f)
    
    def add_build(self, 
                  build_id: str,
                  features: list,
                  estimated_hours: float,
                  actual_minutes: int,
                  lines_of_code: int = 0,
                  files_created: int = 0,
                  notes: str = ""):
        """Record a completed build"""
        
        actual_hours = actual_minutes / 60.0
        efficiency = estimated_hours / actual_hours if actual_hours > 0 else 0
        
        build_record = {
            "build_id": build_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "start_time": (datetime.now() - timedelta(minutes=actual_minutes)).strftime("%H:%M:%S"),
            "end_time": datetime.now().strftime("%H:%M:%S"),
            "estimated_hours": estimated_hours,
            "actual_minutes": actual_minutes,
            "actual_hours": round(actual_hours, 2),
            "efficiency_multiplier": round(efficiency, 1),
            "features_built": features,
            "lines_of_code": lines_of_code,
            "files_created": files_created,
            "notes": notes
        }
        
        if "builds" not in self.data:
            self.data["builds"] = []
        
        self.data["builds"].append(build_record)
        self._update_cumulative_stats()
        self._save_data()
        
        print(f"\n✅ Build tracked: {build_id}")
        print(f"   Estimated: {estimated_hours}h")
        print(f"   Actual: {actual_minutes}m ({actual_hours:.2f}h)")
        print(f"   Efficiency: {efficiency:.1f}x faster than estimated\n")
    
    def _update_cumulative_stats(self):
        """Update cumulative statistics"""
        builds = self.data.get("builds", [])
        
        total_estimated = sum(b["estimated_hours"] for b in builds)
        total_actual = sum(b["actual_hours"] for b in builds)
        total_saved = total_estimated - total_actual
        avg_efficiency = sum(b["efficiency_multiplier"] for b in builds) / len(builds) if builds else 0
        
        self.data["cumulative_stats"] = {
            "total_estimated_hours": round(total_estimated, 2),
            "total_actual_hours": round(total_actual, 2),
            "total_time_saved_hours": round(total_saved, 2),
            "average_efficiency_multiplier": round(avg_efficiency, 1),
            "builds_completed": len(builds)
        }
    
    def show_stats(self):
        """Display tracking statistics"""
        stats = self.data.get("cumulative_stats", {})
        
        print("\n" + "="*70)
        print("📊 Build Efficiency Stats")
        print("="*70)
        print(f"\nBuilds completed: {stats.get('builds_completed', 0)}")
        print(f"Total estimated time: {stats.get('total_estimated_hours', 0)}h")
        print(f"Total actual time: {stats.get('total_actual_hours', 0)}h")
        print(f"Time saved: {stats.get('total_time_saved_hours', 0)}h")
        print(f"Average efficiency: {stats.get('average_efficiency_multiplier', 0)}x faster")
        print("="*70 + "\n")
    
    def show_user_savings(self):
        """Display user time savings projections"""
        savings = self.data.get("user_time_savings", {})
        
        print("\n" + "="*70)
        print("⏱️  User Time Savings")
        print("="*70)
        
        for scenario in savings.get("scenarios", []):
            print(f"\n{scenario['scenario']}:")
            print(f"  Time per scan: {scenario['time_per_scan_minutes']} min")
            print(f"  Daily time: {scenario['daily_time_minutes']} min")
            
            if "time_saved_per_day_minutes" in scenario:
                print(f"  ✅ Saves: {scenario['time_saved_per_day_minutes']} min/day")
                print(f"           {scenario['time_saved_per_week_minutes']} min/week")
                print(f"           {scenario['time_saved_per_month_hours']} hours/month")
        
        annual = savings.get("projected_annual_savings", {})
        if annual:
            print(f"\n📈 Annual Savings per User:")
            print(f"   {annual['per_user_hours']} hours/year")
            print(f"   {annual['per_user_days']} days/year")
            print(f"   {annual['description']}")
        
        print("="*70 + "\n")
    
    def show_recent_builds(self, count: int = 5):
        """Show recent builds"""
        builds = self.data.get("builds", [])[-count:]
        
        print("\n" + "="*70)
        print(f"Recent Builds (last {count})")
        print("="*70)
        
        for build in builds:
            print(f"\n{build['build_id']} ({build['date']})")
            print(f"  Estimated: {build['estimated_hours']}h")
            print(f"  Actual: {build['actual_minutes']}m")
            print(f"  Efficiency: {build['efficiency_multiplier']}x")
            print(f"  Features: {len(build['features_built'])}")
        
        print("="*70 + "\n")


def main():
    """CLI for time tracker"""
    import sys
    
    tracker = TimeTracker()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  time_tracker.py stats          # Show build efficiency stats")
        print("  time_tracker.py savings        # Show user time savings")
        print("  time_tracker.py recent [N]     # Show recent N builds")
        print("  time_tracker.py add <build_id> <estimated_hours> <actual_minutes>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "stats":
        tracker.show_stats()
    
    elif command == "savings":
        tracker.show_user_savings()
    
    elif command == "recent":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        tracker.show_recent_builds(count)
    
    elif command == "add":
        if len(sys.argv) < 5:
            print("Usage: time_tracker.py add <build_id> <estimated_hours> <actual_minutes>")
            sys.exit(1)
        
        build_id = sys.argv[2]
        estimated = float(sys.argv[3])
        actual = int(sys.argv[4])
        
        tracker.add_build(
            build_id=build_id,
            features=[],
            estimated_hours=estimated,
            actual_minutes=actual
        )
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
