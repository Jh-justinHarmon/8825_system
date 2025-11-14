#!/usr/bin/env python3
"""
Screenshot Processor - Handles screenshot routing and archiving
Part of Unified File Processing System
"""

import shutil
from pathlib import Path
from datetime import datetime
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class ScreenshotProcessor:
    """Process screenshots with protocol matching"""
    
    def __init__(self, config: dict, log_file: Path):
        self.config = config
        self.log_file = Path(log_file)
        self.screenshots_path = Path(config['inputs']['screenshots'])
        self.archive_path = self.screenshots_path / "- ARCHV -"
        
        # Ensure archive exists
        self.archive_path.mkdir(exist_ok=True)
    
    def process(self, file_path: Path) -> bool:
        """
        Process screenshot:
        1. Run through progressive router (for protocol matching)
        2. Archive original to -ARCHV- folder
        
        Returns:
            True if successful
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.log(f"⚠️  File not found: {file_path.name}", "WARN")
                return False
            
            # Import progressive router
            try:
                from progressive_router import ProgressiveRouter
                router = ProgressiveRouter(dry_run=False)
                
                # Process through router
                self.log(f"📸 Processing screenshot: {file_path.name}", "INFO")
                router.process_file(file_path)
                
            except Exception as e:
                self.log(f"⚠️  Progressive router error: {e}", "WARN")
                # Continue to archive even if routing fails
            
            # Archive original
            if file_path.exists():  # May have been moved by router
                archive_dest = self.archive_path / file_path.name
                
                # Handle duplicates in archive
                if archive_dest.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    stem = archive_dest.stem
                    suffix = archive_dest.suffix
                    archive_dest = self.archive_path / f"{stem}_{timestamp}{suffix}"
                
                shutil.move(str(file_path), str(archive_dest))
                self.log(f"📦 Archived: {file_path.name}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error processing {file_path.name}: {e}", "ERROR")
            return False
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Test processor"""
    import json
    
    config_path = Path(__file__).parent.parent / "sandbox_target_acquisition/user_config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    log_file = Path(__file__).parent / "logs/screenshot_processor.log"
    log_file.parent.mkdir(exist_ok=True)
    
    processor = ScreenshotProcessor(config, log_file)
    
    print(f"Screenshots path: {processor.screenshots_path}")
    print(f"Archive path: {processor.archive_path}")
    print(f"Log file: {log_file}")

if __name__ == '__main__':
    main()
