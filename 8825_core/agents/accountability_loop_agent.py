#!/usr/bin/env python3
"""
Accountability Loop Agent - Universal goal tracking with automated monitoring, 
decision-making, and alerts

Monitors any trackable goal, makes decisions about progress, suggests actions,
and alerts when targets are at risk.

Usage:
    # Define accountability loops in config
    python3 accountability_loop_agent.py --check-all
    
    # Check specific loop
    python3 accountability_loop_agent.py --check hcss_health
    
    # Add new loop
    python3 accountability_loop_agent.py --add "Exercise" --target "3x per week"
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum


class LoopStatus(Enum):
    """Status of accountability loop"""
    ON_TRACK = "on_track"      # 🟢 Meeting or exceeding target
    AT_RISK = "at_risk"        # 🟡 Below target but recoverable
    OFF_TRACK = "off_track"    # 🔴 Significantly behind
    UNKNOWN = "unknown"        # ⚪ Not enough data


class AlertLevel(Enum):
    """Alert severity"""
    INFO = "info"              # 📊 Informational
    SUCCESS = "success"        # ✅ Positive update
    WARNING = "warning"        # ⚠️ Needs attention
    CRITICAL = "critical"      # 🔴 Urgent action needed


@dataclass
class Metric:
    """A measurable metric for an accountability loop"""
    name: str
    current: float
    target: float
    unit: str
    trend: Optional[str] = None  # "increasing", "decreasing", "stable"
    last_updated: Optional[str] = None
    
    @property
    def percentage_of_target(self) -> float:
        """Calculate percentage of target achieved"""
        if self.target == 0:
            return 100.0 if self.current == 0 else 0.0
        return (self.current / self.target) * 100
    
    @property
    def status(self) -> LoopStatus:
        """Determine status based on percentage"""
        pct = self.percentage_of_target
        if pct >= 90:
            return LoopStatus.ON_TRACK
        elif pct >= 70:
            return LoopStatus.AT_RISK
        else:
            return LoopStatus.OFF_TRACK


@dataclass
class Alert:
    """An alert about accountability loop status"""
    level: AlertLevel
    message: str
    suggestion: Optional[str] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def format(self) -> str:
        """Format alert for display"""
        icons = {
            AlertLevel.INFO: "📊",
            AlertLevel.SUCCESS: "✅",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🔴"
        }
        
        icon = icons.get(self.level, "•")
        output = f"{icon} {self.message}"
        
        if self.suggestion:
            output += f"\n   💡 {self.suggestion}"
        
        return output


@dataclass
class AccountabilityLoop:
    """An accountability loop for tracking progress toward a goal"""
    id: str
    name: str
    description: str
    metrics: List[Metric]
    check_frequency: str  # "daily", "weekly", "monthly"
    data_source: str  # How to get current values
    last_checked: Optional[str] = None
    alerts: List[Alert] = None
    enabled: bool = True
    
    def __post_init__(self):
        if self.alerts is None:
            self.alerts = []
        # Convert dict metrics to Metric objects if needed
        if self.metrics and isinstance(self.metrics[0], dict):
            self.metrics = [Metric(**m) for m in self.metrics]
        # Convert dict alerts to Alert objects if needed
        if self.alerts and isinstance(self.alerts[0], dict):
            self.alerts = [Alert(level=AlertLevel(a['level']), message=a['message'], suggestion=a.get('suggestion'), created_at=a.get('created_at')) for a in self.alerts]
    
    @property
    def overall_status(self) -> LoopStatus:
        """Calculate overall status from all metrics"""
        if not self.metrics:
            return LoopStatus.UNKNOWN
        
        statuses = [m.status for m in self.metrics]
        
        # If any critical, overall is off track
        if LoopStatus.OFF_TRACK in statuses:
            return LoopStatus.OFF_TRACK
        # If any at risk, overall is at risk
        elif LoopStatus.AT_RISK in statuses:
            return LoopStatus.AT_RISK
        # Otherwise on track
        else:
            return LoopStatus.ON_TRACK
    
    def check(self) -> List[Alert]:
        """
        Check accountability loop and generate alerts
        
        Returns:
            List of alerts generated
        """
        new_alerts = []
        
        # Check each metric
        for metric in self.metrics:
            status = metric.status
            pct = metric.percentage_of_target
            
            if status == LoopStatus.OFF_TRACK:
                alert = Alert(
                    level=AlertLevel.CRITICAL,
                    message=f"{self.name}: {metric.name} at {pct:.0f}% of target ({metric.current:.1f}/{metric.target:.1f} {metric.unit})",
                    suggestion=self._generate_suggestion(metric, status)
                )
                new_alerts.append(alert)
            
            elif status == LoopStatus.AT_RISK:
                alert = Alert(
                    level=AlertLevel.WARNING,
                    message=f"{self.name}: {metric.name} at {pct:.0f}% of target ({metric.current:.1f}/{metric.target:.1f} {metric.unit})",
                    suggestion=self._generate_suggestion(metric, status)
                )
                new_alerts.append(alert)
            
            elif status == LoopStatus.ON_TRACK and pct >= 100:
                alert = Alert(
                    level=AlertLevel.SUCCESS,
                    message=f"{self.name}: {metric.name} target achieved! ({metric.current:.1f}/{metric.target:.1f} {metric.unit})"
                )
                new_alerts.append(alert)
        
        # Add trend alerts
        trend_alerts = self._check_trends()
        new_alerts.extend(trend_alerts)
        
        # Update alerts list
        self.alerts = new_alerts
        self.last_checked = datetime.now().isoformat()
        
        return new_alerts
    
    def _generate_suggestion(self, metric: Metric, status: LoopStatus) -> str:
        """Generate actionable suggestion based on metric and status"""
        pct = metric.percentage_of_target
        gap = metric.target - metric.current
        
        if status == LoopStatus.OFF_TRACK:
            return f"Need {gap:.1f} more {metric.unit} to reach target. Consider immediate action."
        elif status == LoopStatus.AT_RISK:
            return f"Need {gap:.1f} more {metric.unit}. Still recoverable with focused effort."
        
        return None
    
    def _check_trends(self) -> List[Alert]:
        """Check for concerning trends"""
        alerts = []
        
        for metric in self.metrics:
            if metric.trend == "decreasing" and metric.status != LoopStatus.ON_TRACK:
                alert = Alert(
                    level=AlertLevel.WARNING,
                    message=f"{self.name}: {metric.name} trending down",
                    suggestion="Investigate cause of decline"
                )
                alerts.append(alert)
        
        return alerts
    
    def update_metric(self, metric_name: str, current_value: float, trend: Optional[str] = None):
        """Update a metric's current value"""
        for metric in self.metrics:
            if metric.name == metric_name:
                metric.current = current_value
                metric.last_updated = datetime.now().isoformat()
                if trend:
                    metric.trend = trend
                break
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'metrics': [asdict(m) for m in self.metrics],
            'check_frequency': self.check_frequency,
            'data_source': self.data_source,
            'last_checked': self.last_checked,
            'alerts': [{'level': a.level.value, 'message': a.message, 'suggestion': a.suggestion, 'created_at': a.created_at} for a in self.alerts] if self.alerts else [],
            'enabled': self.enabled
        }


class AccountabilityLoopAgent:
    """Agent that manages multiple accountability loops"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize agent
        
        Args:
            config_path: Path to config file (default: ~/.8825/accountability_loops.json)
        """
        if config_path is None:
            self.config_path = Path.home() / ".8825" / "accountability_loops.json"
        else:
            self.config_path = config_path
        
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load loops
        self.loops = self._load_loops()
    
    def _load_loops(self) -> Dict[str, AccountabilityLoop]:
        """Load accountability loops from config"""
        if not self.config_path.exists():
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            
            loops = {}
            for loop_id, loop_data in data.items():
                loops[loop_id] = AccountabilityLoop(**loop_data)
            
            return loops
        except Exception as e:
            print(f"⚠️  Error loading loops: {e}", file=sys.stderr)
            return {}
    
    def _save_loops(self):
        """Save accountability loops to config"""
        try:
            data = {loop_id: loop.to_dict() for loop_id, loop in self.loops.items()}
            
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving loops: {e}", file=sys.stderr)
    
    def add_loop(
        self,
        loop_id: str,
        name: str,
        description: str,
        metrics: List[Dict],
        check_frequency: str = "daily",
        data_source: str = "manual"
    ) -> AccountabilityLoop:
        """
        Add a new accountability loop
        
        Args:
            loop_id: Unique identifier
            name: Display name
            description: What this loop tracks
            metrics: List of metric dicts with name, target, unit
            check_frequency: How often to check
            data_source: Where to get data
        
        Returns:
            Created AccountabilityLoop
        """
        # Convert metric dicts to Metric objects
        metric_objects = [
            Metric(
                name=m['name'],
                current=m.get('current', 0.0),
                target=m['target'],
                unit=m['unit']
            )
            for m in metrics
        ]
        
        loop = AccountabilityLoop(
            id=loop_id,
            name=name,
            description=description,
            metrics=metric_objects,
            check_frequency=check_frequency,
            data_source=data_source
        )
        
        self.loops[loop_id] = loop
        self._save_loops()
        
        print(f"✅ Added accountability loop: {name}")
        return loop
    
    def remove_loop(self, loop_id: str):
        """Remove an accountability loop"""
        if loop_id in self.loops:
            name = self.loops[loop_id].name
            del self.loops[loop_id]
            self._save_loops()
            print(f"✅ Removed accountability loop: {name}")
        else:
            print(f"⚠️  Loop not found: {loop_id}")
    
    def update_metric(self, loop_id: str, metric_name: str, current_value: float, trend: Optional[str] = None):
        """Update a metric value"""
        if loop_id not in self.loops:
            print(f"⚠️  Loop not found: {loop_id}")
            return
        
        self.loops[loop_id].update_metric(metric_name, current_value, trend)
        self._save_loops()
        print(f"✅ Updated {metric_name} in {self.loops[loop_id].name}")
    
    def check_loop(self, loop_id: str) -> List[Alert]:
        """Check a specific accountability loop"""
        if loop_id not in self.loops:
            print(f"⚠️  Loop not found: {loop_id}")
            return []
        
        loop = self.loops[loop_id]
        
        if not loop.enabled:
            print(f"⚪ Loop disabled: {loop.name}")
            return []
        
        alerts = loop.check()
        self._save_loops()
        
        return alerts
    
    def check_all(self) -> Dict[str, List[Alert]]:
        """Check all enabled accountability loops"""
        all_alerts = {}
        
        for loop_id, loop in self.loops.items():
            if loop.enabled:
                alerts = self.check_loop(loop_id)
                if alerts:
                    all_alerts[loop_id] = alerts
        
        return all_alerts
    
    def get_status_report(self) -> str:
        """Generate a status report for all loops"""
        report = "# Accountability Loops Status\n\n"
        report += f"**Checked:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        if not self.loops:
            report += "No accountability loops configured.\n"
            return report
        
        # Group by status
        by_status = {
            LoopStatus.ON_TRACK: [],
            LoopStatus.AT_RISK: [],
            LoopStatus.OFF_TRACK: [],
            LoopStatus.UNKNOWN: []
        }
        
        for loop in self.loops.values():
            if loop.enabled:
                by_status[loop.overall_status].append(loop)
        
        # On track
        if by_status[LoopStatus.ON_TRACK]:
            report += "## 🟢 On Track\n\n"
            for loop in by_status[LoopStatus.ON_TRACK]:
                report += f"- **{loop.name}**: All metrics meeting targets\n"
            report += "\n"
        
        # At risk
        if by_status[LoopStatus.AT_RISK]:
            report += "## 🟡 At Risk\n\n"
            for loop in by_status[LoopStatus.AT_RISK]:
                report += f"### {loop.name}\n"
                for metric in loop.metrics:
                    if metric.status == LoopStatus.AT_RISK:
                        pct = metric.percentage_of_target
                        report += f"- {metric.name}: {pct:.0f}% of target ({metric.current:.1f}/{metric.target:.1f} {metric.unit})\n"
                report += "\n"
        
        # Off track
        if by_status[LoopStatus.OFF_TRACK]:
            report += "## 🔴 Off Track\n\n"
            for loop in by_status[LoopStatus.OFF_TRACK]:
                report += f"### {loop.name}\n"
                for metric in loop.metrics:
                    if metric.status == LoopStatus.OFF_TRACK:
                        pct = metric.percentage_of_target
                        report += f"- {metric.name}: {pct:.0f}% of target ({metric.current:.1f}/{metric.target:.1f} {metric.unit})\n"
                
                # Show alerts
                if loop.alerts:
                    report += "\n**Alerts:**\n"
                    for alert in loop.alerts:
                        if alert.level in [AlertLevel.WARNING, AlertLevel.CRITICAL]:
                            report += f"- {alert.format()}\n"
                report += "\n"
        
        return report
    
    def list_loops(self):
        """List all accountability loops"""
        if not self.loops:
            print("No accountability loops configured.")
            return
        
        print("\n# Accountability Loops\n")
        
        for loop in self.loops.values():
            status_icon = {
                LoopStatus.ON_TRACK: "🟢",
                LoopStatus.AT_RISK: "🟡",
                LoopStatus.OFF_TRACK: "🔴",
                LoopStatus.UNKNOWN: "⚪"
            }[loop.overall_status]
            
            enabled = "✓" if loop.enabled else "✗"
            
            print(f"{status_icon} [{enabled}] {loop.name} ({loop.id})")
            print(f"   {loop.description}")
            print(f"   Metrics: {len(loop.metrics)} | Check: {loop.check_frequency}")
            
            if loop.last_checked:
                checked = datetime.fromisoformat(loop.last_checked)
                print(f"   Last checked: {checked.strftime('%Y-%m-%d %H:%M')}")
            
            print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Accountability Loop Agent")
    
    # Actions
    parser.add_argument('--check-all', action='store_true', help='Check all loops')
    parser.add_argument('--check', help='Check specific loop by ID')
    parser.add_argument('--list', action='store_true', help='List all loops')
    parser.add_argument('--status', action='store_true', help='Show status report')
    
    # Add loop
    parser.add_argument('--add', help='Add new loop (provide name)')
    parser.add_argument('--description', help='Loop description')
    parser.add_argument('--metric-name', help='Metric name')
    parser.add_argument('--metric-target', type=float, help='Metric target')
    parser.add_argument('--metric-unit', help='Metric unit')
    
    # Update metric
    parser.add_argument('--update', help='Update metric (loop_id)')
    parser.add_argument('--metric', help='Metric name to update')
    parser.add_argument('--value', type=float, help='New value')
    parser.add_argument('--trend', choices=['increasing', 'decreasing', 'stable'], help='Trend')
    
    args = parser.parse_args()
    
    # Create agent
    agent = AccountabilityLoopAgent()
    
    # Handle actions
    if args.list:
        agent.list_loops()
    
    elif args.status:
        report = agent.get_status_report()
        print(report)
    
    elif args.check_all:
        print("Checking all accountability loops...\n")
        all_alerts = agent.check_all()
        
        if not all_alerts:
            print("✅ All loops on track!")
        else:
            for loop_id, alerts in all_alerts.items():
                loop = agent.loops[loop_id]
                print(f"\n## {loop.name}\n")
                for alert in alerts:
                    print(alert.format())
    
    elif args.check:
        alerts = agent.check_loop(args.check)
        
        if not alerts:
            print(f"✅ {agent.loops[args.check].name} on track!")
        else:
            for alert in alerts:
                print(alert.format())
    
    elif args.add:
        if not all([args.description, args.metric_name, args.metric_target, args.metric_unit]):
            parser.error("--add requires --description, --metric-name, --metric-target, --metric-unit")
        
        loop_id = args.add.lower().replace(' ', '_')
        
        agent.add_loop(
            loop_id=loop_id,
            name=args.add,
            description=args.description,
            metrics=[{
                'name': args.metric_name,
                'target': args.metric_target,
                'unit': args.metric_unit
            }]
        )
    
    elif args.update:
        if not all([args.metric, args.value]):
            parser.error("--update requires --metric and --value")
        
        agent.update_metric(args.update, args.metric, args.value, args.trend)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
