#!/usr/bin/env python3
"""
Ingestion Router - Routes JSON/TXT/TXF files to ingestion system
Part of Unified File Processing System
"""

import shutil
from pathlib import Path
from datetime import datetime

class IngestionRouter:
    """Route files to ingestion system"""
    
    def __init__(self, ingestion_path: Path, log_file: Path):
        self.ingestion_path = Path(ingestion_path)
        self.log_file = Path(log_file)
        
        # Ensure ingestion folder exists
        self.ingestion_path.mkdir(parents=True, exist_ok=True)
    
    def route(self, file_path: Path) -> bool:
        """
        Copy file to ingestion folder
        
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.log(f"⚠️  File not found: {file_path.name}", "WARN")
                return False
            
            # Destination path
            dest_path = self.ingestion_path / file_path.name
            
            # Check if already exists
            if dest_path.exists():
                # Check if same file (by size)
                if dest_path.stat().st_size == file_path.stat().st_size:
                    self.log(f"⏭️  Already in ingestion: {file_path.name}", "INFO")
                    return True
                else:
                    # Version it
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    stem = dest_path.stem
                    suffix = dest_path.suffix
                    dest_path = self.ingestion_path / f"{stem}_{timestamp}{suffix}"
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            self.log(f"📥 Routed to ingestion: {file_path.name}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error routing {file_path.name}: {e}", "ERROR")
            return False
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Test router"""
    ingestion_path = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/Documents/ingestion"
    log_file = Path(__file__).parent / "logs/ingestion_router.log"
    log_file.parent.mkdir(exist_ok=True)
    
    router = IngestionRouter(ingestion_path, log_file)
    
    print(f"Ingestion path: {ingestion_path}")
    print(f"Log file: {log_file}")

if __name__ == '__main__':
    main()
