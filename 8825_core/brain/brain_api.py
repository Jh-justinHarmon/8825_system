#!/usr/bin/env python3
"""
8825 Brain API Client
Interface for commands to communicate with brain daemon
"""

import json
import socket
from typing import Dict, Any

class BrainAPI:
    """Client for communicating with brain daemon"""
    
    def __init__(self):
        self.socket_path = "/tmp/8825_brain.sock"
    
    def _send_command(self, command: str, data: Any = None) -> Dict[str, Any]:
        """Send command to brain daemon"""
        try:
            # Connect to brain
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(self.socket_path)
            
            # Send request
            request = {"command": command, "data": data}
            client.send(json.dumps(request).encode())
            
            # Receive response
            response_data = client.recv(4096).decode()
            response = json.loads(response_data)
            
            client.close()
            return response
            
        except FileNotFoundError:
            return {
                "error": "Brain daemon not running",
                "hint": "Start with: python3 8825_core/brain/brain_daemon.py"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return self._send_command("get_status")
    
    def predict_action(self, action: str) -> Dict[str, Any]:
        """Predict impact of action"""
        return self._send_command("predict", {"action": action})
    
    def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute coordinated workflow"""
        return self._send_command("execute", workflow)
    
    def check_and_heal(self) -> Dict[str, Any]:
        """Check for issues and heal if possible"""
        return self._send_command("heal")

def main():
    """Test the API"""
    api = BrainAPI()
    
    print("Testing brain API...")
    status = api.get_status()
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()
