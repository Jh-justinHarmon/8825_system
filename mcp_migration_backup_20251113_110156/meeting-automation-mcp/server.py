#!/usr/bin/env python3
"""
Meeting Automation MCP Server
Provides Goose-compatible interface for meeting automation control
"""

import json
import sys
from pathlib import Path
from typing import Dict

class MeetingAutomationMCP:
    """MCP server for meeting automation control"""
    
    def __init__(self):
        self.users_dir = Path(__file__).parent.parent.parent.parent.parent / "users"
    
    def handle_request(self, method: str, params: dict) -> dict:
        """Handle MCP request"""
        
        # Extract user and focus from params
        user_id = params.get('user_id', 'justin_harmon')
        focus = params.get('focus', 'hcss')
        
        if method == "tools/list":
            return self._list_tools()
        
        elif method == "meeting/status":
            return self.get_status(user_id, focus)
        
        elif method == "meeting/start":
            return self.start_polling(user_id, focus)
        
        elif method == "meeting/stop":
            return self.stop_polling(user_id, focus)
        
        elif method == "meeting/health":
            return self.get_health(user_id, focus)
        
        elif method == "meeting/recent":
            return self.get_recent(user_id, focus, params.get('limit', 10))
        
        else:
            return {"error": f"Unknown method: {method}"}
    
    def _list_tools(self) -> dict:
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "meeting/status",
                    "description": "Get meeting automation status",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "focus": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "meeting/start",
                    "description": "Start meeting automation polling",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "focus": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "meeting/stop",
                    "description": "Stop meeting automation polling",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "focus": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "meeting/health",
                    "description": "Get health status of both sources",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "focus": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "meeting/recent",
                    "description": "Get recent meeting summaries",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "focus": {"type": "string"},
                            "limit": {"type": "integer"}
                        }
                    }
                }
            ]
        }
    
    def get_status(self, user_id: str, focus: str) -> dict:
        """Get meeting automation status"""
        config_path = self.users_dir / user_id / focus / "meeting_automation/config.json"
        
        if not config_path.exists():
            return {
                "status": "not_configured",
                "message": f"No config found at {config_path}"
            }
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check if poller is running
        pid_file = config_path.parent / ".poller.pid"
        is_running = pid_file.exists()
        
        return {
            "status": "enabled" if config.get('enabled') else "disabled",
            "polling": is_running,
            "strategy": config.get('strategy', {}).get('mode'),
            "primary_source": config.get('strategy', {}).get('primary'),
            "otter_enabled": config.get('otter_api', {}).get('enabled', False),
            "gmail_enabled": config.get('gmail', {}).get('enabled', False)
        }
    
    def start_polling(self, user_id: str, focus: str) -> dict:
        """Start polling"""
        import subprocess
        
        poller_path = self.users_dir / user_id / focus / "meeting_automation/poller.py"
        
        if not poller_path.exists():
            return {"error": "Poller not found"}
        
        try:
            subprocess.Popen(
                ['python3', str(poller_path), '--daemon'],
                cwd=poller_path.parent
            )
            return {"status": "started", "message": "Polling started"}
        except Exception as e:
            return {"error": str(e)}
    
    def stop_polling(self, user_id: str, focus: str) -> dict:
        """Stop polling"""
        import subprocess
        
        poller_path = self.users_dir / user_id / focus / "meeting_automation/poller.py"
        
        if not poller_path.exists():
            return {"error": "Poller not found"}
        
        try:
            subprocess.run(
                ['python3', str(poller_path), '--stop'],
                cwd=poller_path.parent,
                check=True
            )
            return {"status": "stopped", "message": "Polling stopped"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_health(self, user_id: str, focus: str) -> dict:
        """Get health status"""
        # TODO: Read health from dual_source_manager
        return {
            "otter_api": {"status": "unknown"},
            "gmail": {"status": "unknown"},
            "message": "Health monitoring not yet implemented"
        }
    
    def get_recent(self, user_id: str, focus: str, limit: int) -> dict:
        """Get recent meetings"""
        summaries_dir = self.users_dir / user_id / focus / "knowledge/meetings/summaries"
        
        if not summaries_dir.exists():
            return {"meetings": [], "count": 0}
        
        # Get recent markdown files
        files = sorted(summaries_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
        files = files[:limit]
        
        meetings = []
        for file in files:
            meetings.append({
                "title": file.stem,
                "path": str(file),
                "modified": file.stat().st_mtime
            })
        
        return {"meetings": meetings, "count": len(meetings)}

def main():
    """Main entry point"""
    server = MeetingAutomationMCP()
    
    # Read JSON-RPC request from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get('method')
            params = request.get('params', {})
            
            response = server.handle_request(method, params)
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    main()
