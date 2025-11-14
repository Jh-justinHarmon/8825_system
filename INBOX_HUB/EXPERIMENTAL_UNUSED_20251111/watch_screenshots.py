#!/usr/bin/env python3
"""
Screenshot Watcher - Auto-process new screenshots

Monitors: ~/Hammer Consulting Dropbox/Justin Harmon/Screenshots/
When new file appears:
1. Wait 2 seconds (ensure file is fully written)
2. Run OCR
3. Detect type (KARSEN, Bill, Standard)
4. Process accordingly
5. Move to - ARCHV -

Run as daemon:
    python3 watch_screenshots.py &
"""

import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

SCREENSHOTS_FOLDER = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Screenshots"
SCRIPT_DIR = Path(__file__).parent

class ScreenshotHandler(FileSystemEventHandler):
    """Handle new screenshot files"""
    
    def __init__(self):
        self.processing = set()
    
    def on_created(self, event):
        """Called when a file is created"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Only process images
        if file_path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            return
        
        # Skip if in archive folder
        if '- ARCHV -' in str(file_path):
            return
        
        # Skip if already processing
        if file_path in self.processing:
            return
        
        print(f"\n🔔 New screenshot detected: {file_path.name}")
        self.processing.add(file_path)
        
        # Wait for file to be fully written
        time.sleep(2)
        
        # Process the screenshot
        self.process_screenshot(file_path)
        
        self.processing.remove(file_path)
    
    def process_screenshot(self, file_path):
        """Process screenshot with OCR processor"""
        print(f"🔄 Processing...")
        
        try:
            # Run OCR processor in auto mode
            result = subprocess.run(
                ['python3', str(SCRIPT_DIR / 'ocr_processor_v2.py')],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(result.stdout)
            
            if result.returncode == 0:
                print(f"✅ Processing complete")
            else:
                print(f"⚠️  Processing had issues")
                if result.stderr:
                    print(result.stderr)
        
        except Exception as e:
            print(f"❌ Error processing: {e}")

def main():
    print("\n" + "="*80)
    print("SCREENSHOT WATCHER - Auto-OCR Daemon")
    print("="*80)
    print(f"\nMonitoring: {SCREENSHOTS_FOLDER}")
    print("Press Ctrl+C to stop\n")
    
    # Create observer
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SCREENSHOTS_FOLDER), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping watcher...")
        observer.stop()
    
    observer.join()
    print("✅ Watcher stopped")

if __name__ == '__main__':
    main()
