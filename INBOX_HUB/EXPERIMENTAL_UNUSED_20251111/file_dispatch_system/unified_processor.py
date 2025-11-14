#!/usr/bin/env python3
"""
Unified Processor - Orchestrates file processing
Part of Unified File Processing System
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from smart_classifier import SmartClassifier
from ingestion_router import IngestionRouter
from screenshot_processor import ScreenshotProcessor
from output_manager import OutputManager
from meeting_router import MeetingRouter

class UnifiedProcessor:
    """Main processor - orchestrates all components"""
    
    def __init__(self, config_path: Path):
        """Initialize with config"""
        self.config_path = Path(config_path)
        
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        self.log_dir = Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "unified_processor.log"
        
        # Initialize components
        self.classifier = SmartClassifier(self.config_path)
        
        ingestion_path = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/ingestion"
        self.ingestion_router = IngestionRouter(ingestion_path, self.log_dir / "ingestion_router.log")
        
        self.screenshot_processor = ScreenshotProcessor(self.config, self.log_dir / "screenshot_processor.log")
        
        self.output_manager = OutputManager(self.config, self.log_dir / "output_manager.log")
        
        self.meeting_router = MeetingRouter(self.log_dir / "meeting_router.log")
        
        self.log("🚀 Unified Processor initialized", "INFO")
    
    def process_file(self, file_path: Path) -> bool:
        """
        Process a single file through the unified system
        
        Returns:
            True if successful
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.log(f"⚠️  File not found: {file_path}", "WARN")
                return False
            
            self.log(f"📥 Processing: {file_path.name}", "INFO")
            
            # Classify file
            classification = self.classifier.classify(file_path)
            action = classification['action']
            processor = classification['processor']
            
            self.log(f"   Classification: {action} → {processor}", "DEBUG")
            self.log(f"   Reason: {classification['reason']}", "DEBUG")
            
            # Route to appropriate processor
            if action == 'protected':
                # Copy to output, keep in place
                self.output_manager.copy_to_brain(file_path)
                self.log(f"✓ Protected file handled: {file_path.name}", "INFO")
                return True
                
            elif action == 'ingestion':
                # Route to ingestion system
                success = self.ingestion_router.route(file_path)
                if success:
                    self.log(f"✓ Routed to ingestion: {file_path.name}", "INFO")
                return success
                
            elif action == 'screenshot':
                # Process screenshot
                success = self.screenshot_processor.process(file_path)
                if success:
                    self.log(f"✓ Screenshot processed: {file_path.name}", "INFO")
                return success
                
            elif action == 'meeting':
                # Route to user-specific meeting processor
                success = self.meeting_router.route(file_path)
                if success:
                    self.log(f"✓ Meeting transcript routed: {file_path.name}", "INFO")
                else:
                    self.log(f"⚠️  Meeting transcript not processed (no config): {file_path.name}", "WARN")
                return success
                
            elif action == 'progressive':
                # Use progressive router
                try:
                    from progressive_router import ProgressiveRouter
                    router = ProgressiveRouter(dry_run=False)
                    router.process_file(file_path)
                    self.log(f"✓ Progressive router handled: {file_path.name}", "INFO")
                    return True
                except Exception as e:
                    self.log(f"❌ Progressive router error: {e}", "ERROR")
                    return False
            
            elif action == 'skip':
                # Skip this file (manual inspection only)
                self.log(f"⏭️  Skipped: {file_path.name} - {classification['reason']}", "INFO")
                return True  # Return True so it doesn't get marked as error
            
            else:
                self.log(f"⚠️  Unknown action: {action}", "WARN")
                return False
                
        except Exception as e:
            self.log(f"❌ Error processing {file_path}: {e}", "ERROR")
            return False
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Process file from command line"""
    if len(sys.argv) < 2:
        print("Usage: python3 unified_processor.py <file_path>")
        sys.exit(1)
    
    config_path = Path(__file__).parent.parent / "sandbox_target_acquisition/user_config.json"
    processor = UnifiedProcessor(config_path)
    
    file_path = Path(sys.argv[1])
    success = processor.process_file(file_path)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
