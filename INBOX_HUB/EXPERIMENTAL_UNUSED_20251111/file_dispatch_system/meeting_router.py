#!/usr/bin/env python3
"""
Meeting Router - Routes meeting transcripts to user-specific processors
Part of File Dispatch System (FDS)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class MeetingRouter:
    """Route meeting transcripts to user-specific processors"""
    
    def __init__(self, log_file: Path):
        """Initialize router"""
        self.base_dir = Path(__file__).parent
        self.users_dir = self.base_dir.parent.parent / "users"
        self.log_file = log_file
        
        self.log("📋 Meeting Router initialized", "INFO")
    
    def route(self, file_path: Path) -> bool:
        """
        Route meeting transcript to appropriate user processor
        
        Logic:
        1. Detect which user's inbox this came from
        2. Find user's meeting automation configs
        3. If enabled, invoke user's processor
        4. If not enabled, skip (log only)
        
        Returns:
            True if successfully routed and processed
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.log(f"⚠️  File not found: {file_path}", "WARN")
                return False
            
            self.log(f"📥 Routing meeting transcript: {file_path.name}", "INFO")
            
            # Detect user from file path
            user_id = self._detect_user(file_path)
            
            if not user_id:
                self.log(f"⚠️  Could not detect user for: {file_path}", "WARN")
                self.log(f"   File will not be processed automatically", "INFO")
                return False
            
            self.log(f"   Detected user: {user_id}", "DEBUG")
            
            # Find user's meeting automation configs
            configs = self._find_user_configs(user_id)
            
            if not configs:
                self.log(f"   No meeting automation configured for user: {user_id}", "INFO")
                self.log(f"   To enable: Create users/{user_id}/{{focus}}/meeting_automation/config.json", "INFO")
                return False
            
            # Process with each enabled config
            success = False
            for config in configs:
                if config.get('enabled'):
                    focus = config['_focus']
                    self.log(f"   Processing with {user_id}/{focus} config", "INFO")
                    
                    # For now, just log (user processors not built yet)
                    self.log(f"   ✓ Would process with: users/{user_id}/{focus}/meeting_automation/", "INFO")
                    success = True
                else:
                    self.log(f"   Skipping {config['_focus']} (disabled)", "DEBUG")
            
            return success
            
        except Exception as e:
            self.log(f"❌ Error routing {file_path}: {e}", "ERROR")
            return False
    
    def _detect_user(self, file_path: Path) -> Optional[str]:
        """
        Detect user from file path
        
        Strategy:
        1. Check if file is in a user's Downloads/Screenshots
        2. Match against configured input paths
        3. Return user_id
        """
        file_str = str(file_path)
        
        # Check each user directory
        if not self.users_dir.exists():
            return None
        
        for user_dir in self.users_dir.iterdir():
            if not user_dir.is_dir():
                continue
            
            user_id = user_dir.name
            
            # Check if file path contains user's name or directory
            if user_id.lower() in file_str.lower():
                return user_id
        
        # Fallback: Check common patterns
        # If file is in ~/Downloads or ~/Desktop, assume primary user
        if '/Downloads/' in file_str or '/Desktop/' in file_str:
            # Return first user found (typically justin_harmon)
            users = [d.name for d in self.users_dir.iterdir() if d.is_dir()]
            if users:
                return users[0]
        
        return None
    
    def _find_user_configs(self, user_id: str) -> List[Dict]:
        """
        Find all meeting automation configs for user
        
        Searches all focuses for meeting_automation/config.json
        """
        configs = []
        user_dir = self.users_dir / user_id
        
        if not user_dir.exists():
            return configs
        
        # Search all focuses for meeting_automation/config.json
        for focus_dir in user_dir.iterdir():
            if not focus_dir.is_dir():
                continue
            
            config_path = focus_dir / "meeting_automation/config.json"
            
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        config['_path'] = str(config_path)
                        config['_focus'] = focus_dir.name
                        configs.append(config)
                        
                        self.log(f"   Found config: {user_id}/{focus_dir.name}", "DEBUG")
                        
                except Exception as e:
                    self.log(f"   Error reading config {config_path}: {e}", "WARN")
        
        return configs
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Test router"""
    if len(sys.argv) < 2:
        print("Usage: python3 meeting_router.py <file_path>")
        sys.exit(1)
    
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "meeting_router.log"
    
    router = MeetingRouter(log_file)
    
    file_path = Path(sys.argv[1])
    success = router.route(file_path)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
