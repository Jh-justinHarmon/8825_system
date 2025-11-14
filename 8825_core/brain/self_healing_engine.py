#!/usr/bin/env python3
"""
8825 Self-Healing Engine
Detects and fixes common issues autonomously
"""

import json
import subprocess
import shutil
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

class SelfHealingEngine:
    """Detects issues and heals autonomously"""
    
    def __init__(self, brain_state: Dict[str, Any]):
        self.state = brain_state
        self.config_dir = Path.home() / ".8825"
        self.strategies = self.load_healing_strategies()
    
    def check_and_heal(self) -> Dict[str, Any]:
        """
        Check for issues and heal if possible
        
        Returns:
            Healing report with issues found and healed
        """
        print("🔍 Scanning for issues...\n")
        
        # Detect issues
        issues = self.detect_issues()
        
        if not issues:
            return {
                "issues_found": 0,
                "issues_healed": 0,
                "status": "healthy",
                "message": "✅ No issues detected"
            }
        
        print(f"⚠️  Found {len(issues)} issue(s)\n")
        
        # Heal each issue
        healed = []
        failed = []
        
        for i, issue in enumerate(issues, 1):
            print(f"[{i}/{len(issues)}] {issue['type']}: {issue.get('description', 'Unknown')}")
            
            if self.can_auto_heal(issue):
                result = self.heal(issue)
                
                if result['success']:
                    print(f"  ✅ Healed")
                    healed.append(issue)
                else:
                    print(f"  ❌ Failed: {result.get('error', 'Unknown')}")
                    failed.append(issue)
            else:
                print(f"  ⚠️  Cannot auto-heal - escalating to user")
                failed.append(issue)
        
        print()
        
        return {
            "issues_found": len(issues),
            "issues_healed": len(healed),
            "issues_failed": len(failed),
            "status": "healed" if len(failed) == 0 else "partial",
            "healed": healed,
            "failed": failed
        }
    
    def detect_issues(self) -> List[Dict[str, Any]]:
        """Scan for problems"""
        issues = []
        
        # Check component health
        issues.extend(self.check_component_health())
        
        # Check for stale processes
        issues.extend(self.check_stale_processes())
        
        # Check resource usage
        issues.extend(self.check_resource_usage())
        
        # Check for orphaned files
        issues.extend(self.check_orphaned_files())
        
        return issues
    
    def check_component_health(self) -> List[Dict[str, Any]]:
        """Check if components are healthy"""
        issues = []
        
        health = self.state.get('health', {})
        components = health.get('components', [])
        
        for component in components:
            if not component.get('healthy', True):
                issues.append({
                    "type": "component_unhealthy",
                    "component": component.get('id'),
                    "description": f"Component {component.get('id')} is unhealthy",
                    "details": component.get('error'),
                    "severity": "high"
                })
        
        return issues
    
    def check_stale_processes(self) -> List[Dict[str, Any]]:
        """Check for stale/zombie processes"""
        issues = []
        
        registry = self.state.get('registry', {})
        components = registry.get('components', [])
        
        for component in components:
            if component.get('type') == 'daemon':
                if self.is_stale(component):
                    issues.append({
                        "type": "stale_process",
                        "component": component.get('id'),
                        "description": f"Daemon {component.get('id')} appears stale",
                        "severity": "medium"
                    })
        
        return issues
    
    def is_stale(self, component: Dict[str, Any]) -> bool:
        """Check if a daemon is stale"""
        # Check if process exists but not responding
        component_id = component.get('id', '')
        
        try:
            # Check if running
            result = subprocess.run(
                ["pgrep", "-f", component_id],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False  # Not running, not stale
            
            # TODO: Add actual health check (ping, status endpoint, etc.)
            # For now, assume running = healthy
            return False
            
        except:
            return False
    
    def check_resource_usage(self) -> List[Dict[str, Any]]:
        """Check system resource usage"""
        issues = []
        
        # Check disk space
        disk_usage = self.get_disk_usage()
        if disk_usage > 0.85:
            issues.append({
                "type": "disk_space_low",
                "description": f"Disk space at {disk_usage*100:.0f}%",
                "usage": disk_usage,
                "severity": "medium" if disk_usage < 0.95 else "high"
            })
        
        # Check memory (if available)
        memory_usage = self.get_memory_usage()
        if memory_usage and memory_usage > 0.90:
            issues.append({
                "type": "memory_high",
                "description": f"Memory usage at {memory_usage*100:.0f}%",
                "usage": memory_usage,
                "severity": "medium"
            })
        
        return issues
    
    def get_disk_usage(self) -> float:
        """Get disk usage percentage"""
        try:
            total, used, free = shutil.disk_usage("/")
            return used / total
        except:
            return 0.0
    
    def get_memory_usage(self) -> float:
        """Get memory usage percentage"""
        try:
            result = subprocess.run(
                ["vm_stat"],
                capture_output=True,
                text=True
            )
            # Parse vm_stat output (macOS specific)
            # This is simplified - real implementation would parse properly
            return None  # Not implemented yet
        except:
            return None
    
    def check_orphaned_files(self) -> List[Dict[str, Any]]:
        """Check for orphaned temporary files"""
        issues = []
        
        # Check for old PID files
        pid_files = list(self.config_dir.glob("*.pid"))
        for pid_file in pid_files:
            try:
                with open(pid_file) as f:
                    pid = int(f.read().strip())
                
                # Check if process exists
                result = subprocess.run(
                    ["ps", "-p", str(pid)],
                    capture_output=True
                )
                
                if result.returncode != 0:
                    # Process doesn't exist, PID file is orphaned
                    issues.append({
                        "type": "orphaned_pid_file",
                        "file": str(pid_file),
                        "description": f"Orphaned PID file: {pid_file.name}",
                        "severity": "low"
                    })
            except:
                pass
        
        # Check for old socket files
        socket_files = ["/tmp/8825_brain.sock"]
        for socket_file in socket_files:
            socket_path = Path(socket_file)
            if socket_path.exists():
                # Check if socket is actually in use
                try:
                    import socket as sock
                    test_sock = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
                    test_sock.connect(socket_file)
                    test_sock.close()
                except:
                    # Socket exists but not in use
                    issues.append({
                        "type": "orphaned_socket",
                        "file": socket_file,
                        "description": f"Orphaned socket: {socket_file}",
                        "severity": "low"
                    })
        
        return issues
    
    def can_auto_heal(self, issue: Dict[str, Any]) -> bool:
        """Check if we have a healing strategy"""
        return issue['type'] in self.strategies
    
    def heal(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Execute healing strategy"""
        strategy = self.strategies[issue['type']]
        
        # Record healing attempt
        self.record_healing_attempt(issue, strategy)
        
        # Execute strategy
        result = strategy.heal(issue, self.state)
        
        # Record outcome
        if result['success']:
            self.record_healing_success(issue, strategy)
        else:
            self.record_healing_failure(issue, strategy, result)
        
        return result
    
    def load_healing_strategies(self):
        """Load healing strategies"""
        from healing_strategies.restart_component import RestartComponentStrategy
        from healing_strategies.cleanup_disk import CleanupDiskStrategy
        from healing_strategies.remove_orphaned_file import RemoveOrphanedFileStrategy
        
        return {
            "component_unhealthy": RestartComponentStrategy(),
            "stale_process": RestartComponentStrategy(),
            "disk_space_low": CleanupDiskStrategy(),
            "orphaned_pid_file": RemoveOrphanedFileStrategy(),
            "orphaned_socket": RemoveOrphanedFileStrategy()
        }
    
    def record_healing_attempt(self, issue: Dict[str, Any], strategy):
        """Record healing attempt"""
        # TODO: Log to file
        pass
    
    def record_healing_success(self, issue: Dict[str, Any], strategy):
        """Record successful healing"""
        outcome = {
            "timestamp": datetime.now().isoformat(),
            "issue_type": issue['type'],
            "issue": issue,
            "strategy": strategy.__class__.__name__,
            "success": True
        }
        
        self.state['history'].append(outcome)
        self.save_healing_history(outcome)
    
    def record_healing_failure(self, issue: Dict[str, Any], strategy, result: Dict[str, Any]):
        """Record failed healing"""
        outcome = {
            "timestamp": datetime.now().isoformat(),
            "issue_type": issue['type'],
            "issue": issue,
            "strategy": strategy.__class__.__name__,
            "success": False,
            "error": result.get('error')
        }
        
        self.state['history'].append(outcome)
        self.save_healing_history(outcome)
    
    def save_healing_history(self, outcome: Dict[str, Any]):
        """Save healing history to file"""
        history_file = self.config_dir / "healing_history.json"
        
        try:
            existing = []
            if history_file.exists():
                with open(history_file) as f:
                    existing = json.load(f)
            
            existing.append(outcome)
            
            # Keep last 100 entries
            if len(existing) > 100:
                existing = existing[-100:]
            
            with open(history_file, 'w') as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save healing history: {e}")

def main():
    """Test the self-healing engine"""
    # Mock brain state
    state = {
        "registry": {"components": []},
        "health": {"components": []},
        "history": []
    }
    
    engine = SelfHealingEngine(state)
    result = engine.check_and_heal()
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
