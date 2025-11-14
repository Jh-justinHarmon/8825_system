#!/usr/bin/env python3
"""
File Dispatch System (FDS) - MCP Server
Goose-compatible interface for file processing control
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add FDS to path
FDS_PATH = Path(__file__).parent.parent.parent.parent.parent / "INBOX_HUB/file_dispatch_system"
sys.path.insert(0, str(FDS_PATH))

from unified_processor import UnifiedProcessor

class FDSMCPServer:
    """MCP Server for File Dispatch System"""
    
    def __init__(self):
        # FDS base directory
        self.base_dir = FDS_PATH
        self.config_path = self.base_dir.parent / "sandbox_target_acquisition/user_config.json"
        self.pid_file = self.base_dir / ".watcher.pid"
        self.log_dir = self.base_dir / "logs"
        
        # Initialize processor
        self.processor = UnifiedProcessor(self.config_path)
    
    def handle_request(self, method: str, params: dict) -> dict:
        """Handle MCP request"""
        try:
            if method == "fds/status":
                return self.get_status()
            elif method == "fds/start":
                return self.start_system()
            elif method == "fds/stop":
                return self.stop_system()
            elif method == "fds/process_file":
                return self.process_file(params.get("file_path"))
            elif method == "fds/get_logs":
                return self.get_logs(params.get("lines", 20))
            elif method == "fds/get_queue":
                return self.get_queue()
            elif method == "fds/clear_queue":
                return self.clear_queue()
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_status(self) -> dict:
        """Get system status"""
        # Check if running
        is_running = False
        pid = None
        
        if self.pid_file.exists():
            pid = int(self.pid_file.read_text().strip())
            try:
                subprocess.run(["ps", "-p", str(pid)], 
                             check=True, 
                             capture_output=True)
                is_running = True
            except subprocess.CalledProcessError:
                is_running = False
        
        # Get config
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        # Get queue size
        queue_file = self.base_dir / "processing_queue.txt"
        queue_size = 0
        if queue_file.exists():
            queue_size = len(queue_file.read_text().strip().split('\n'))
            if queue_size == 1 and not queue_file.read_text().strip():
                queue_size = 0
        
        # Get recent activity
        log_file = self.log_dir / "unified_processor.log"
        recent_activity = []
        if log_file.exists():
            lines = log_file.read_text().strip().split('\n')
            recent_activity = lines[-5:] if lines else []
        
        return {
            "status": "running" if is_running else "stopped",
            "pid": pid,
            "inputs": config.get("inputs", {}),
            "outputs": config.get("outputs", {}),
            "queue_size": queue_size,
            "recent_activity": recent_activity
        }
    
    def start_system(self) -> dict:
        """Start the file dispatch system"""
        if self.pid_file.exists():
            return {"error": "System already running"}
        
        try:
            # Start watch script
            start_script = self.base_dir / "start.sh"
            subprocess.Popen([str(start_script)], 
                           cwd=str(self.base_dir))
            
            return {"success": True, "message": "File Dispatch System started"}
        except Exception as e:
            return {"error": str(e)}
    
    def stop_system(self) -> dict:
        """Stop the file dispatch system"""
        if not self.pid_file.exists():
            return {"error": "System not running"}
        
        try:
            # Stop watch script
            stop_script = self.base_dir / "stop.sh"
            subprocess.run([str(stop_script)], 
                         cwd=str(self.base_dir),
                         check=True)
            
            return {"success": True, "message": "File Dispatch System stopped"}
        except Exception as e:
            return {"error": str(e)}
    
    def process_file(self, file_path: str) -> dict:
        """Process a specific file"""
        if not file_path:
            return {"error": "file_path required"}
        
        try:
            file_path = Path(file_path)
            success = self.processor.process_file(file_path)
            
            return {
                "success": success,
                "file": str(file_path),
                "message": "File processed" if success else "Processing failed"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_logs(self, lines: int = 20) -> dict:
        """Get recent log entries"""
        log_file = self.log_dir / "unified_processor.log"
        
        if not log_file.exists():
            return {"logs": []}
        
        try:
            all_lines = log_file.read_text().strip().split('\n')
            recent = all_lines[-lines:] if all_lines else []
            
            return {"logs": recent}
        except Exception as e:
            return {"error": str(e)}
    
    def get_queue(self) -> dict:
        """Get current processing queue"""
        queue_file = self.base_dir / "processing_queue.txt"
        
        if not queue_file.exists():
            return {"queue": []}
        
        try:
            content = queue_file.read_text().strip()
            if not content:
                return {"queue": []}
            
            files = content.split('\n')
            return {"queue": files}
        except Exception as e:
            return {"error": str(e)}
    
    def clear_queue(self) -> dict:
        """Clear the processing queue"""
        queue_file = self.base_dir / "processing_queue.txt"
        
        try:
            queue_file.write_text("")
            return {"success": True, "message": "Queue cleared"}
        except Exception as e:
            return {"error": str(e)}

def main():
    """Main MCP server loop"""
    server = FDSMCPServer()
    
    print(json.dumps({
        "jsonrpc": "2.0",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "file-dispatch-system",
                "version": "1.0.0"
            }
        }
    }), flush=True)
    
    # Read requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "tools/list":
                # Return available tools
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "fds_status",
                                "description": "Get File Dispatch System status",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "fds_start",
                                "description": "Start File Dispatch System",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "fds_stop",
                                "description": "Stop File Dispatch System",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "fds_process_file",
                                "description": "Process a specific file through FDS",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "file_path": {
                                            "type": "string",
                                            "description": "Path to file to process"
                                        }
                                    },
                                    "required": ["file_path"]
                                }
                            },
                            {
                                "name": "fds_get_logs",
                                "description": "Get recent FDS log entries",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "lines": {
                                            "type": "number",
                                            "description": "Number of log lines to retrieve",
                                            "default": 20
                                        }
                                    }
                                }
                            },
                            {
                                "name": "fds_get_queue",
                                "description": "Get current processing queue",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "fds_clear_queue",
                                "description": "Clear the processing queue",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                # Handle tool call
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})
                
                # Map tool name to internal method
                method_map = {
                    "fds_status": "fds/status",
                    "fds_start": "fds/start",
                    "fds_stop": "fds/stop",
                    "fds_process_file": "fds/process_file",
                    "fds_get_logs": "fds/get_logs",
                    "fds_get_queue": "fds/get_queue",
                    "fds_clear_queue": "fds/clear_queue"
                }
                
                internal_method = method_map.get(tool_name)
                if internal_method:
                    result = server.handle_request(internal_method, tool_params)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, indent=2)
                                }
                            ]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == '__main__':
    main()
