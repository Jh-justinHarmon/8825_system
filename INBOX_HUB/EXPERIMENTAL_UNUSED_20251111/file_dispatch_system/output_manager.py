#!/usr/bin/env python3
"""
Output Manager - Manages outputs to iCloud Documents/8825/
Part of Unified File Processing System
"""

import shutil
from pathlib import Path
from datetime import datetime

class OutputManager:
    """Manage outputs to iCloud Documents/8825/"""
    
    def __init__(self, config: dict, log_file: Path):
        self.config = config
        self.log_file = Path(log_file)
        
        # Output paths
        self.brain_output = Path(config['outputs']['brain'])
        self.docs_output = Path(config['outputs']['docs'])
        
        # Ensure output folders exist
        self.brain_output.mkdir(parents=True, exist_ok=True)
        self.docs_output.mkdir(parents=True, exist_ok=True)
    
    def copy_to_brain(self, file_path: Path) -> bool:
        """
        Copy Brain transport file to output
        
        Returns:
            True if successful
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.log(f"⚠️  File not found: {file_path.name}", "WARN")
                return False
            
            # Always copy as BRAIN_TRANSPORT.json (latest)
            dest_path = self.brain_output / "BRAIN_TRANSPORT.json"
            
            # Also keep dated version
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dated_path = self.brain_output / f"BRAIN_TRANSPORT_{timestamp}.json"
            
            # Copy both
            shutil.copy2(file_path, dest_path)
            shutil.copy2(file_path, dated_path)
            
            self.log(f"🧠 Copied to BRAIN output: {file_path.name}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error copying to BRAIN: {e}", "ERROR")
            return False
    
    def copy_to_docs(self, file_path: Path, subfolder: str = None) -> bool:
        """
        Copy 8825-generated document to output
        
        Args:
            file_path: Path to file
            subfolder: Optional subfolder (e.g., 'sessions', 'reports')
        
        Returns:
            True if successful
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.log(f"⚠️  File not found: {file_path.name}", "WARN")
                return False
            
            # Determine destination
            if subfolder:
                dest_folder = self.docs_output / subfolder
                dest_folder.mkdir(exist_ok=True)
            else:
                dest_folder = self.docs_output
            
            dest_path = dest_folder / file_path.name
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            
            self.log(f"📄 Copied to DOCS output: {file_path.name}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error copying to DOCS: {e}", "ERROR")
            return False
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Test manager"""
    import json
    
    config_path = Path(__file__).parent.parent / "sandbox_target_acquisition/user_config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    log_file = Path(__file__).parent / "logs/output_manager.log"
    log_file.parent.mkdir(exist_ok=True)
    
    manager = OutputManager(config, log_file)
    
    print(f"BRAIN output: {manager.brain_output}")
    print(f"DOCS output: {manager.docs_output}")
    print(f"Log file: {log_file}")

if __name__ == '__main__':
    main()
