#!/usr/bin/env python3
"""
System Health Monitor - Track system changes for Brain Transport regeneration

Monitors:
- LaunchAgents (running/stopped)
- Integration scripts (new/modified)
- Workflow status files
- Configuration files
- Archive activity

Calculates change score and determines when Brain Transport needs regeneration.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import hashlib

from safe_file_ops import safe_read_json, safe_write_json

class SystemHealthMonitor:
    """Monitor system state and detect significant changes"""
    
    # Change score weights
    WEIGHTS = {
        'launchagent_change': 10,    # High priority
        'config_change': 5,           # High priority
        'integration_change': 3,      # Medium priority
        'workflow_change': 2,         # Medium priority
        'archive_activity': 1         # Low priority
    }
    
    REGENERATION_THRESHOLD = 10  # Points needed to trigger regeneration
    
    def __init__(self, system_root: Path = None):
        if system_root is None:
            system_root = Path(__file__).parent.parent.parent
        
        self.system_root = system_root
        self.state_file = Path(__file__).parent / "state" / "system_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.current_state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load previous system state"""
        default_state = {
            'last_check': datetime.now().isoformat(),
            'launchagents': {},
            'integration_hashes': {},
            'workflow_hashes': {},
            'config_hashes': {},
            'archive_dirs': [],
            'accumulated_score': 0,
            'last_regeneration': None
        }
        return safe_read_json(self.state_file, default=default_state)
    
    def _save_state(self):
        """Save current system state"""
        self.current_state['last_check'] = datetime.now().isoformat()
        safe_write_json(self.state_file, self.current_state, backup=True)
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get hash of file contents"""
        try:
            if not file_path.exists():
                return ""
            content = file_path.read_text()
            return hashlib.sha256(content.encode()).hexdigest()
        except:
            return ""
    
    def _check_launchagents(self) -> Dict:
        """Check LaunchAgent status"""
        changes = {
            'new_agents': [],
            'stopped_agents': [],
            'started_agents': [],
            'score': 0
        }
        
        try:
            # Get currently loaded LaunchAgents
            result = subprocess.run(
                ['launchctl', 'list'],
                capture_output=True,
                text=True
            )
            
            current_agents = {}
            for line in result.stdout.split('\n'):
                if '8825' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        pid = parts[0]
                        name = parts[2]
                        current_agents[name] = {
                            'running': pid != '-',
                            'pid': pid if pid != '-' else None
                        }
            
            previous_agents = self.current_state['launchagents']
            
            # Detect new agents
            for name in current_agents:
                if name not in previous_agents:
                    changes['new_agents'].append(name)
                    changes['score'] += self.WEIGHTS['launchagent_change']
            
            # Detect stopped agents
            for name in previous_agents:
                if name not in current_agents:
                    changes['stopped_agents'].append(name)
                    changes['score'] += self.WEIGHTS['launchagent_change']
                elif previous_agents[name]['running'] and not current_agents[name]['running']:
                    changes['stopped_agents'].append(name)
                    changes['score'] += self.WEIGHTS['launchagent_change']
            
            # Detect started agents
            for name in current_agents:
                if name in previous_agents:
                    if not previous_agents[name]['running'] and current_agents[name]['running']:
                        changes['started_agents'].append(name)
                        changes['score'] += self.WEIGHTS['launchagent_change']
            
            # Update state
            self.current_state['launchagents'] = current_agents
            
        except Exception as e:
            print(f"⚠️  Error checking LaunchAgents: {e}")
        
        return changes
    
    def _check_integrations(self) -> Dict:
        """Check integration scripts for changes"""
        changes = {
            'new_scripts': [],
            'modified_scripts': [],
            'score': 0
        }
        
        integrations_dir = self.system_root / "8825_core" / "integrations"
        if not integrations_dir.exists():
            return changes
        
        try:
            # Find all Python scripts with main()
            current_scripts = {}
            for py_file in integrations_dir.rglob("*.py"):
                if "ARCHIVED" in str(py_file) or "__pycache__" in str(py_file):
                    continue
                
                # Check if it has a main() function
                try:
                    content = py_file.read_text()
                    if "def main(" in content:
                        rel_path = str(py_file.relative_to(self.system_root))
                        current_scripts[rel_path] = self._get_file_hash(py_file)
                except:
                    continue
            
            previous_scripts = self.current_state.get('integration_hashes', {})
            
            # Detect new scripts
            for script in current_scripts:
                if script not in previous_scripts:
                    changes['new_scripts'].append(script)
                    changes['score'] += self.WEIGHTS['integration_change']
                elif current_scripts[script] != previous_scripts[script]:
                    changes['modified_scripts'].append(script)
                    changes['score'] += self.WEIGHTS['integration_change']
            
            # Update state
            self.current_state['integration_hashes'] = current_scripts
            
        except Exception as e:
            print(f"⚠️  Error checking integrations: {e}")
        
        return changes
    
    def _check_workflows(self) -> Dict:
        """Check workflow status files"""
        changes = {
            'new_workflows': [],
            'modified_workflows': [],
            'score': 0
        }
        
        workflows_dir = self.system_root / "8825_core" / "workflows"
        if not workflows_dir.exists():
            return changes
        
        try:
            current_workflows = {}
            
            # Check for README and STATUS files
            for status_file in workflows_dir.rglob("README.md"):
                if "ARCHIVED" in str(status_file):
                    continue
                rel_path = str(status_file.relative_to(self.system_root))
                current_workflows[rel_path] = self._get_file_hash(status_file)
            
            for status_file in workflows_dir.rglob("STATUS.md"):
                if "ARCHIVED" in str(status_file):
                    continue
                rel_path = str(status_file.relative_to(self.system_root))
                current_workflows[rel_path] = self._get_file_hash(status_file)
            
            previous_workflows = self.current_state.get('workflow_hashes', {})
            
            # Detect changes
            for workflow in current_workflows:
                if workflow not in previous_workflows:
                    changes['new_workflows'].append(workflow)
                    changes['score'] += self.WEIGHTS['workflow_change']
                elif current_workflows[workflow] != previous_workflows[workflow]:
                    changes['modified_workflows'].append(workflow)
                    changes['score'] += self.WEIGHTS['workflow_change']
            
            # Update state
            self.current_state['workflow_hashes'] = current_workflows
            
        except Exception as e:
            print(f"⚠️  Error checking workflows: {e}")
        
        return changes
    
    def _check_configs(self) -> Dict:
        """Check configuration files"""
        changes = {
            'new_configs': [],
            'modified_configs': [],
            'score': 0
        }
        
        try:
            current_configs = {}
            
            # Check for config.json files
            for config_file in self.system_root.rglob("config.json"):
                if "ARCHIVED" in str(config_file) or "node_modules" in str(config_file):
                    continue
                rel_path = str(config_file.relative_to(self.system_root))
                current_configs[rel_path] = self._get_file_hash(config_file)
            
            # Check for .plist files
            for plist_file in self.system_root.rglob("*.plist"):
                if "ARCHIVED" in str(plist_file):
                    continue
                rel_path = str(plist_file.relative_to(self.system_root))
                current_configs[rel_path] = self._get_file_hash(plist_file)
            
            previous_configs = self.current_state.get('config_hashes', {})
            
            # Detect changes
            for config in current_configs:
                if config not in previous_configs:
                    changes['new_configs'].append(config)
                    changes['score'] += self.WEIGHTS['config_change']
                elif current_configs[config] != previous_configs[config]:
                    changes['modified_configs'].append(config)
                    changes['score'] += self.WEIGHTS['config_change']
            
            # Update state
            self.current_state['config_hashes'] = current_configs
            
        except Exception as e:
            print(f"⚠️  Error checking configs: {e}")
        
        return changes
    
    def _check_archives(self) -> Dict:
        """Check for new archive directories"""
        changes = {
            'new_archives': [],
            'score': 0
        }
        
        try:
            current_archives = []
            
            # Find ARCHIVED directories
            for archive_dir in self.system_root.rglob("ARCHIVED*"):
                if archive_dir.is_dir():
                    rel_path = str(archive_dir.relative_to(self.system_root))
                    current_archives.append(rel_path)
            
            previous_archives = self.current_state.get('archive_dirs', [])
            
            # Detect new archives
            for archive in current_archives:
                if archive not in previous_archives:
                    changes['new_archives'].append(archive)
                    changes['score'] += self.WEIGHTS['archive_activity']
            
            # Update state
            self.current_state['archive_dirs'] = current_archives
            
        except Exception as e:
            print(f"⚠️  Error checking archives: {e}")
        
        return changes
    
    def check_system_state(self) -> Dict:
        """Check entire system state and calculate change score"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'launchagents': self._check_launchagents(),
            'integrations': self._check_integrations(),
            'workflows': self._check_workflows(),
            'configs': self._check_configs(),
            'archives': self._check_archives(),
            'total_score': 0,
            'accumulated_score': 0,
            'regenerate_brain_transport': False,
            'changes_summary': []
        }
        
        # Calculate total score from this check
        result['total_score'] = (
            result['launchagents']['score'] +
            result['integrations']['score'] +
            result['workflows']['score'] +
            result['configs']['score'] +
            result['archives']['score']
        )
        
        # Add to accumulated score
        self.current_state['accumulated_score'] += result['total_score']
        result['accumulated_score'] = self.current_state['accumulated_score']
        
        # Generate summary
        if result['launchagents']['new_agents']:
            result['changes_summary'].append(f"New LaunchAgents: {', '.join(result['launchagents']['new_agents'])}")
        if result['launchagents']['stopped_agents']:
            result['changes_summary'].append(f"Stopped LaunchAgents: {', '.join(result['launchagents']['stopped_agents'])}")
        if result['integrations']['new_scripts']:
            result['changes_summary'].append(f"New integrations: {len(result['integrations']['new_scripts'])}")
        if result['workflows']['new_workflows']:
            result['changes_summary'].append(f"New workflows: {len(result['workflows']['new_workflows'])}")
        if result['configs']['modified_configs']:
            result['changes_summary'].append(f"Modified configs: {len(result['configs']['modified_configs'])}")
        
        # Check if regeneration threshold met
        if result['accumulated_score'] >= self.REGENERATION_THRESHOLD:
            result['regenerate_brain_transport'] = True
            # Reset accumulated score after regeneration
            self.current_state['accumulated_score'] = 0
            self.current_state['last_regeneration'] = datetime.now().isoformat()
        
        # Save state
        self._save_state()
        
        return result
    
    def get_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            'last_check': self.current_state.get('last_check'),
            'accumulated_score': self.current_state.get('accumulated_score', 0),
            'threshold': self.REGENERATION_THRESHOLD,
            'last_regeneration': self.current_state.get('last_regeneration'),
            'tracked_items': {
                'launchagents': len(self.current_state.get('launchagents', {})),
                'integrations': len(self.current_state.get('integration_hashes', {})),
                'workflows': len(self.current_state.get('workflow_hashes', {})),
                'configs': len(self.current_state.get('config_hashes', {})),
                'archives': len(self.current_state.get('archive_dirs', []))
            }
        }
    
    def reset_score(self):
        """Manually reset accumulated score"""
        self.current_state['accumulated_score'] = 0
        self._save_state()


def main():
    """Test the monitor"""
    monitor = SystemHealthMonitor()
    
    print("🔍 Checking system state...\n")
    result = monitor.check_system_state()
    
    print(f"Total Score: {result['total_score']}")
    print(f"Accumulated Score: {result['accumulated_score']}/{monitor.REGENERATION_THRESHOLD}")
    print(f"Regenerate: {result['regenerate_brain_transport']}")
    
    if result['changes_summary']:
        print("\nChanges Detected:")
        for change in result['changes_summary']:
            print(f"  - {change}")
    else:
        print("\nNo changes detected")
    
    print("\nStatus:")
    status = monitor.get_status()
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
