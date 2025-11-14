#!/usr/bin/env python3
"""
Brain Transport Generator - Auto-generate Brain Transport JSON

Scans system to discover:
- Active LaunchAgents
- Available integrations
- Workflow status
- MCP servers
- System capabilities

Merges with manual overrides and generates updated Brain Transport.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import shutil

class BrainTransportGenerator:
    """Generate Brain Transport JSON from system state"""
    
    def __init__(self, system_root: Path = None):
        if system_root is None:
            system_root = Path(__file__).parent.parent.parent
        
        self.system_root = system_root
        self.manual_overrides_file = Path(__file__).parent / "brain_transport_overrides.json"
        
        # Output locations
        self.primary_output = system_root / "INBOX_HUB" / "users" / "jh" / "intake" / "documents" / "8825_BRAIN_TRANSPORT.json"
        self.documents_output = Path.home() / "Documents" / "8825_BRAIN_TRANSPORT.json"
        self.archive_dir = Path(__file__).parent / "state" / "brain_transport_archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_manual_overrides(self) -> Dict:
        """Load manual overrides that can't be auto-detected"""
        default_overrides = {
            "interaction_modes": {
                "dev_mode": {
                    "purpose": "GO MODE - Execute when plan is clear",
                    "approach": "Do first, minimal discussion",
                    "output": "Terse progress updates",
                    "code": "Only during execution",
                    "use_when": "You have plan and understand it"
                },
                "brainstorm_mode": {
                    "purpose": "ROADMAP CREATION - Design solution",
                    "approach": "Analyze, propose architecture with code blocks",
                    "output": "Complete roadmap with implementation",
                    "code": "YES - show patterns, workflows, examples",
                    "use_when": "Exploring ideas, need executable plan"
                },
                "teaching_mode": {
                    "purpose": "UNDERSTANDING THE PLAN - Help you comprehend",
                    "approach": "Plain language, analogies, no code",
                    "output": "Conceptual explanations",
                    "code": "NEVER - concepts only",
                    "use_when": "Need to understand before approving"
                }
            },
            "communication_style": {
                "dev_mode": "Terse, action-focused, no fluff",
                "brainstorm_mode": "Comprehensive, analytical, code blocks",
                "teaching_mode": "Conversational, analogies, no code",
                "general": "Markdown-heavy, bullet lists, scannable"
            },
            "critical_rules": {
                "professional_title": "NEVER change - exact format with slashes",
                "dev_mode": "Execute immediately when plan is clear",
                "brainstorm_mode": "Always include code blocks and roadmap",
                "teaching_mode": "Never show code, only concepts"
            }
        }
        
        if self.manual_overrides_file.exists():
            try:
                with open(self.manual_overrides_file) as f:
                    return json.load(f)
            except:
                return default_overrides
        
        return default_overrides
    
    def _scan_launchagents(self) -> Dict:
        """Scan active LaunchAgents"""
        agents = {}
        
        try:
            result = subprocess.run(
                ['launchctl', 'list'],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if '8825' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        pid = parts[0]
                        name = parts[2]
                        agents[name] = {
                            'status': 'running' if pid != '-' else 'loaded',
                            'pid': pid if pid != '-' else None
                        }
        except Exception as e:
            print(f"⚠️  Error scanning LaunchAgents: {e}")
        
        return agents
    
    def _scan_integrations(self) -> Dict:
        """Scan available integrations"""
        integrations = {}
        
        integrations_dir = self.system_root / "8825_core" / "integrations"
        if not integrations_dir.exists():
            return integrations
        
        for integration_type in integrations_dir.iterdir():
            if not integration_type.is_dir() or integration_type.name.startswith('.'):
                continue
            
            if "ARCHIVED" in integration_type.name:
                continue
            
            # Find main scripts
            scripts = []
            for py_file in integration_type.rglob("*.py"):
                if "ARCHIVED" in str(py_file) or "__pycache__" in str(py_file):
                    continue
                
                try:
                    content = py_file.read_text()
                    if "def main(" in content:
                        # Extract purpose from docstring
                        purpose = "Available"
                        if '"""' in content:
                            docstring = content.split('"""')[1].strip().split('\n')[0]
                            purpose = docstring
                        
                        scripts.append({
                            'script': py_file.name,
                            'purpose': purpose
                        })
                except:
                    continue
            
            if scripts:
                integrations[integration_type.name] = {
                    'status': 'available',
                    'scripts': scripts
                }
        
        return integrations
    
    def _scan_workflows(self) -> Dict:
        """Scan workflow status"""
        workflows = {}
        
        workflows_dir = self.system_root / "8825_core" / "workflows"
        if not workflows_dir.exists():
            return workflows
        
        for workflow_dir in workflows_dir.iterdir():
            if not workflow_dir.is_dir() or workflow_dir.name.startswith('.'):
                continue
            
            if "ARCHIVED" in workflow_dir.name:
                continue
            
            # Check for STATUS.md
            status_file = workflow_dir / "STATUS.md"
            readme_file = workflow_dir / "README.md"
            
            status = "available"
            purpose = workflow_dir.name.replace('_', ' ').title()
            
            if status_file.exists():
                try:
                    content = status_file.read_text()
                    if "Production" in content or "Active" in content:
                        status = "production"
                    elif "Development" in content:
                        status = "development"
                except:
                    pass
            
            if readme_file.exists():
                try:
                    content = readme_file.read_text()
                    # Extract first line after # header
                    for line in content.split('\n'):
                        if line.startswith('**Purpose:**') or line.startswith('**Status:**'):
                            purpose = line.split(':', 1)[1].strip()
                            break
                except:
                    pass
            
            workflows[workflow_dir.name] = {
                'status': status,
                'purpose': purpose
            }
        
        return workflows
    
    def _scan_mcp_servers(self) -> Dict:
        """Scan MCP server configurations"""
        mcp_servers = {}
        
        mcp_dir = self.system_root / "8825_core" / "integrations" / "mcp-servers"
        if not mcp_dir.exists():
            return mcp_servers
        
        for server_dir in mcp_dir.iterdir():
            if not server_dir.is_dir() or server_dir.name.startswith('.'):
                continue
            
            server_file = server_dir / "server.py"
            if server_file.exists():
                try:
                    content = server_file.read_text()
                    # Extract purpose from docstring
                    purpose = "MCP Server"
                    if '"""' in content:
                        docstring = content.split('"""')[1].strip().split('\n')[0]
                        purpose = docstring
                    
                    mcp_servers[server_dir.name] = {
                        'status': 'available',
                        'purpose': purpose
                    }
                except:
                    pass
        
        return mcp_servers
    
    def _get_system_architecture(self) -> Dict:
        """Get system architecture info"""
        return {
            "version": "3.0",
            "structure": {
                "core": "8825_core/ - Shareable system (protocols, agents, workflows)",
                "users": "users/justinharmon/ - Private user data",
                "focuses": "focuses/{hcss,joju,jh_assistant}/ - Team-specific workspaces",
                "index": "8825_index/ - Fast discovery layer"
            }
        }
    
    def _get_key_locations(self) -> Dict:
        """Get key file locations"""
        return {
            "system_root": str(self.system_root),
            "inbox": "~/Downloads/8825_inbox/",
            "brain_transport": str(self.primary_output),
            "philosophy": str(self.system_root / "PHILOSOPHY.md")
        }
    
    def generate(self) -> Dict:
        """Generate complete Brain Transport JSON"""
        print("🧠 Generating Brain Transport...")
        
        # Archive previous version
        if self.primary_output.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = self.archive_dir / f"brain_transport_{timestamp}.json"
            shutil.copy(self.primary_output, archive_path)
            print(f"   Archived previous version to {archive_path.name}")
        
        # Load manual overrides
        overrides = self._load_manual_overrides()
        
        # Scan system
        print("   Scanning LaunchAgents...")
        launchagents = self._scan_launchagents()
        
        print("   Scanning integrations...")
        integrations = self._scan_integrations()
        
        print("   Scanning workflows...")
        workflows = self._scan_workflows()
        
        print("   Scanning MCP servers...")
        mcp_servers = self._scan_mcp_servers()
        
        # Build transport
        transport = {
            "brain_version": "3.0",
            "export_date": datetime.now().isoformat(),
            "purpose": "Complete 8825 system context for LLM transport",
            "auto_generated": True,
            "generation_trigger": "System health monitor threshold reached",
            
            "system_architecture": self._get_system_architecture(),
            "key_locations": self._get_key_locations(),
            
            "active_launchagents": launchagents,
            "available_integrations": integrations,
            "workflows": workflows,
            "mcp_servers": mcp_servers,
            
            # Merge manual overrides
            "interaction_modes": overrides.get("interaction_modes", {}),
            "communication_style": overrides.get("communication_style", {}),
            "critical_rules": overrides.get("critical_rules", {}),
            
            "workflow": {
                "natural_flow": "Teaching (understand) → Brainstorm (plan) → Dev (execute)",
                "mode_switching": {
                    "explicit": "switch to [mode] mode",
                    "auto_detect": "Based on request type"
                }
            },
            
            "quick_commands": {
                "fetch_inbox": "Process files from ~/Downloads/8825_inbox/pending/",
                "focus_on_jh": "Activate JH personal focus",
                "focus_on_joju": "Activate Joju/Team 76 focus",
                "focus_on_hcss": "Activate HCSS client focus",
                "sync_brain": "Create comprehensive brain sync document",
                "switch_to_dev_mode": "Enter execution mode",
                "switch_to_brainstorm_mode": "Enter planning mode",
                "switch_to_teaching_mode": "Enter learning mode"
            },
            
            "status": f"Auto-generated v3.0 system snapshot - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
        
        # Save to primary location
        self.primary_output.parent.mkdir(parents=True, exist_ok=True)
        with open(self.primary_output, 'w') as f:
            json.dump(transport, f, indent=2)
        print(f"   ✅ Saved to {self.primary_output}")
        
        # Copy to Documents (separate from Downloads, accessible via Desktop symlink)
        self.documents_output.parent.mkdir(parents=True, exist_ok=True)
        with open(self.documents_output, 'w') as f:
            json.dump(transport, f, indent=2)
        print(f"   ✅ Copied to {self.documents_output}")
        
        print("🎯 Brain Transport generation complete!")
        
        return transport
    
    def get_generation_history(self) -> List[Dict]:
        """Get history of generated transports"""
        history = []
        
        for archive_file in sorted(self.archive_dir.glob("brain_transport_*.json")):
            try:
                with open(archive_file) as f:
                    data = json.load(f)
                    history.append({
                        'filename': archive_file.name,
                        'export_date': data.get('export_date'),
                        'version': data.get('brain_version')
                    })
            except:
                continue
        
        return history


def main():
    """Test the generator"""
    generator = BrainTransportGenerator()
    
    print("Testing Brain Transport Generator\n")
    
    # Show history
    history = generator.get_generation_history()
    if history:
        print(f"Previous generations: {len(history)}")
        for item in history[-3:]:  # Show last 3
            print(f"  - {item['filename']} ({item['export_date']})")
        print()
    
    # Generate new transport
    transport = generator.generate()
    
    print(f"\nGenerated transport with:")
    print(f"  - {len(transport.get('active_launchagents', {}))} LaunchAgents")
    print(f"  - {len(transport.get('available_integrations', {}))} integrations")
    print(f"  - {len(transport.get('workflows', {}))} workflows")
    print(f"  - {len(transport.get('mcp_servers', {}))} MCP servers")


if __name__ == '__main__':
    main()
