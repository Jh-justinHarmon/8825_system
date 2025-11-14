#!/usr/bin/env python3
"""
Onboarding Target Discovery Protocol
Learns user's actual file paths through guided actions
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
import os

class OnboardingDiscovery:
    def __init__(self):
        self.config_file = Path.home() / "Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/INBOX_HUB/users/jh/user_paths_config.json"
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.discovered_paths = {}
        
    def print_step(self, step_num: int, title: str):
        """Print step header"""
        print(f"\n{'='*60}")
        print(f"STEP {step_num}: {title}")
        print(f"{'='*60}\n")
    
    def find_recent_files_spotlight(self, seconds_ago: int, kind: str = None) -> list:
        """Use Spotlight to find ALL recent files system-wide"""
        import subprocess
        
        cutoff_time = datetime.now() - timedelta(seconds=seconds_ago)
        
        # Build mdfind query - use kMDItemKind which works better
        if kind == "image":
            # Search for common image types
            queries = [
                'kMDItemKind == "PNG image"',
                'kMDItemKind == "JPEG image"',
                'kMDItemKind == "Image"'
            ]
        else:
            # For any file, just search by modification date
            queries = [None]
        
        all_files = []
        for query in queries:
            if query:
                cmd = ["mdfind", "-onlyin", str(Path.home()), query]
            else:
                # Search all files modified recently
                cmd = ["find", str(Path.home()), "-type", "f", "-mtime", "-1"]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            all_files.append(line)
            except subprocess.TimeoutExpired:
                continue
        
        if not all_files:
            return []
        
        candidates = []
        for file_str in all_files:
            file_path = Path(file_str)
            if not file_path.exists() or not file_path.is_file():
                continue
            
            # Skip hidden files
            if file_path.name.startswith('.'):
                continue
            
            # Check modification time
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime > cutoff_time:
                    candidates.append((file_path, mtime))
            except (OSError, PermissionError):
                continue
        
        # Sort by most recent
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates]
    
    def prompt_user_selection(self, files: list, prompt: str) -> Path:
        """Show user a list of files and let them pick"""
        if not files:
            return None
        
        print(f"\n{prompt}")
        print("\nFound these recent files:\n")
        
        for i, file_path in enumerate(files[:10], 1):  # Show max 10
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            age = (datetime.now() - mtime).total_seconds()
            print(f"  {i}. {file_path.name}")
            print(f"     Location: {file_path.parent}")
            print(f"     Created: {int(age)} seconds ago")
            print()
        
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more\n")
        
        while True:
            choice = input("Enter number (or 'n' if none match): ").strip().lower()
            if choice == 'n':
                return None
            try:
                idx = int(choice) - 1
                if 0 <= idx < min(len(files), 10):
                    return files[idx]
            except ValueError:
                pass
            print("Invalid choice. Try again.")
    
    def step_1_screenshot_discovery(self):
        """Discover desktop screenshot location"""
        self.print_step(1, "Desktop Screenshot Discovery")
        
        print("📸 Please take a screenshot on your desktop")
        print("   Mac: Cmd+Shift+4 (select area) or Cmd+Shift+3 (full screen)")
        print("   Windows: Win+Shift+S")
        
        input("\nPress Enter when you've taken the screenshot...")
        
        print("\n🔍 Searching entire system for recent images...")
        recent_images = self.find_recent_files_spotlight(60, kind="image")
        
        screenshot = self.prompt_user_selection(
            recent_images,
            "Which of these is your screenshot?"
        )
        
        if not screenshot:
            print("❌ Could not find screenshot. Please try again.")
            return False
        
        screenshot_dir = screenshot.parent
        print(f"✅ Found screenshot at: {screenshot_dir}")
        print(f"   File: {screenshot.name}")
        
        # Create archive folder
        archive_dir = screenshot_dir / "-ARCHV-"
        archive_dir.mkdir(exist_ok=True)
        
        # Count old files
        old_files = []
        for item in screenshot_dir.iterdir():
            if item.name.startswith('.') or item.name == "-ARCHV-":
                continue
            if item.is_file():
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                age_minutes = (datetime.now() - mtime).total_seconds() / 60
                if age_minutes > 5:
                    old_files.append(item)
        
        print(f"\n📦 Found {len(old_files)} old files to archive")
        if old_files and input("Archive them now? (y/n): ").lower() == 'y':
            for old_file in old_files:
                old_file.rename(archive_dir / old_file.name)
            print(f"✅ Archived {len(old_files)} files")
        
        self.discovered_paths['screenshots'] = {
            'path': str(screenshot_dir),
            'rules': 'archive_old_copy_new',
            'archive_folder': str(archive_dir),
            'watch': True,
            'archive_age_minutes': 5
        }
        
        return True
    
    def step_2_downloads_discovery(self):
        """Discover browser downloads location"""
        self.print_step(2, "Browser Downloads Discovery")
        
        # Create test file
        test_content = f"8825 Test File - {datetime.now().isoformat()}"
        test_filename = "8825_test_download.txt"
        
        print("📥 Please download this test file from your browser:")
        print(f"\n   We'll create a test file for you to download.")
        print(f"   Filename: {test_filename}")
        
        # Create test file in temp location
        temp_test = Path("/tmp") / test_filename
        temp_test.write_text(test_content)
        
        print(f"\n   File created at: {temp_test}")
        print(f"   Open this file in your browser, then save it (Cmd+S or Ctrl+S)")
        print(f"   Or just copy it to your Downloads folder to simulate a download")
        
        input("\nPress Enter when you've downloaded/saved the file...")
        
        print("\n🔍 Searching entire system for recent files...")
        recent_files = self.find_recent_files_spotlight(120, kind="any")
        
        # Filter for .txt files first
        txt_files = [f for f in recent_files if f.suffix.lower() == '.txt']
        
        test_file = self.prompt_user_selection(
            txt_files if txt_files else recent_files,
            "Which of these is the test file you downloaded?"
        )
        
        if not test_file:
            print("❌ Could not find any recent downloads. Using default ~/Downloads")
            downloads_dir = Path.home() / "Downloads"
        else:
            downloads_dir = test_file.parent
            print(f"✅ Found downloads at: {downloads_dir}")
            print(f"   File: {test_file.name}")
            
            # Clean up test file
            if test_file.exists():
                test_file.unlink()
                print(f"   (Cleaned up test file)")
        
        self.discovered_paths['downloads'] = {
            'path': str(downloads_dir),
            'rules': 'process_in_place',
            'watch': True
        }
        
        # Clean up temp test file
        if temp_test.exists():
            temp_test.unlink()
        
        return True
    
    def step_3_cloud_upload_discovery(self):
        """Discover mobile cloud upload location"""
        self.print_step(3, "Mobile Cloud Upload Discovery")
        
        print("☁️  Please upload any file from your phone to your cloud folder")
        print("   Options:")
        print("   - Dropbox mobile app → Upload to any folder")
        print("   - iCloud → Save to Files app")
        print("   - Google Drive → Upload")
        print("\n   💡 Tip: Take a photo and upload it, or upload any existing file")
        
        input("\nPress Enter when you've uploaded the file...")
        
        print("\n🔍 Searching entire system for recent files...")
        recent_files = self.find_recent_files_spotlight(180, kind="any")
        
        cloud_file = self.prompt_user_selection(
            recent_files,
            "Which of these is the file you uploaded from your phone?"
        )
        
        if not cloud_file:
            print("❌ Could not find recent cloud upload.")
            print("   You can configure this manually later.")
            return True
        
        cloud_dir = cloud_file.parent
        print(f"✅ Found cloud upload at: {cloud_dir}")
        print(f"   File: {cloud_file.name}")
        
        self.discovered_paths['cloud_uploads'] = {
            'path': str(cloud_dir),
            'rules': 'process_in_place',
            'watch': True
        }
        
        return True
    
    def step_4_airdrop_discovery(self):
        """Discover AirDrop location"""
        self.print_step(4, "AirDrop Discovery")
        
        print("📱 Please AirDrop any file from your phone to this computer")
        print("   - Take a photo or select any existing file")
        print("   - Tap Share → AirDrop → This Computer")
        
        input("\nPress Enter when you've sent the AirDrop...")
        
        print("\n🔍 Searching entire system for recent files...")
        recent_files = self.find_recent_files_spotlight(120, kind="any")
        
        airdrop_file = self.prompt_user_selection(
            recent_files,
            "Which of these is the file you AirDropped?"
        )
        
        if not airdrop_file:
            print("❌ Could not find AirDrop file.")
            print("   AirDrop typically uses the same location as Downloads.")
            airdrop_dir = self.discovered_paths.get('downloads', {}).get('path', str(Path.home() / "Downloads"))
        else:
            airdrop_dir = str(airdrop_file.parent)
            print(f"✅ Found AirDrop at: {airdrop_dir}")
            print(f"   File: {airdrop_file.name}")
        
        # Check if same as downloads
        downloads_path = self.discovered_paths.get('downloads', {}).get('path')
        if airdrop_dir == downloads_path:
            print("   ℹ️  Same as Downloads folder (typical)")
            self.discovered_paths['airdrop'] = {
                'path': airdrop_dir,
                'rules': 'same_as_downloads'
            }
        else:
            print("   ℹ️  Different from Downloads folder (unusual)")
            self.discovered_paths['airdrop'] = {
                'path': airdrop_dir,
                'rules': 'process_in_place',
                'watch': True
            }
        
        return True
    
    def save_config(self):
        """Save discovered paths to config file"""
        config = {
            'user_id': 'jh',
            'discovered_paths': self.discovered_paths,
            'processing_folder': str(Path.home() / "Downloads/8825_processing"),
            'onboarding_complete': True,
            'discovered_at': datetime.now().isoformat()
        }
        
        self.config_file.write_text(json.dumps(config, indent=2))
        print(f"\n💾 Configuration saved to: {self.config_file}")
        
    def print_summary(self):
        """Print discovery summary"""
        print("\n" + "="*60)
        print("DISCOVERY COMPLETE")
        print("="*60)
        
        print("\n📋 Discovered Paths:\n")
        for name, config in self.discovered_paths.items():
            print(f"  {name.upper()}:")
            print(f"    Path: {config['path']}")
            print(f"    Rules: {config['rules']}")
            if 'watch' in config:
                print(f"    Watch: {'✓' if config['watch'] else '✗'}")
            if 'archive_folder' in config:
                print(f"    Archive: {config['archive_folder']}")
            print()
    
    def run(self):
        """Run full discovery protocol"""
        print("\n" + "="*60)
        print("8825 ONBOARDING - TARGET DISCOVERY PROTOCOL")
        print("="*60)
        print("\nThis will help 8825 learn where YOUR files live.")
        print("We'll guide you through 4 simple steps.\n")
        
        input("Press Enter to begin...")
        
        # Run all steps
        if not self.step_1_screenshot_discovery():
            print("\n❌ Discovery failed at Step 1")
            return False
        
        if not self.step_2_downloads_discovery():
            print("\n❌ Discovery failed at Step 2")
            return False
        
        if not self.step_3_cloud_upload_discovery():
            print("\n❌ Discovery failed at Step 3")
            return False
        
        if not self.step_4_airdrop_discovery():
            print("\n❌ Discovery failed at Step 4")
            return False
        
        # Save and summarize
        self.save_config()
        self.print_summary()
        
        print("✅ Onboarding complete! 8825 now knows where to find your files.")
        print("\nNext steps:")
        print("  1. Run: ./progressive_router.py scan")
        print("  2. Your discovered paths will be used automatically")
        
        return True

if __name__ == "__main__":
    discovery = OnboardingDiscovery()
    discovery.run()
