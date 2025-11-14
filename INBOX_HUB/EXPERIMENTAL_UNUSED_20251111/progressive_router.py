#!/usr/bin/env python3
"""
Progressive Routing System - Trust-Based Inbox Processing
Builds trust through successful uses, not time
"""

import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pytesseract
from PIL import Image

# Import protocols
from exclusion_protocol import ExclusionProtocol
from deduplication_protocol import DeduplicationProtocol
from auto_unpack_protocol import AutoUnpackProtocol
from content_relevancy_protocol import ContentRelevancyProtocol

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
DOWNLOADS = Path.home() / "Downloads"
PROCESSING_FOLDER = DOWNLOADS / "8825_processing"
PROCESSED_ARCHIVE = DOWNLOADS / "8825_processed"
USERS_DIR = SCRIPT_DIR / "users"
SCREENSHOT_INTAKE = USERS_DIR / "jh" / "intake" / "screenshots"

# Status emoji prefixes
STATUS_EMOJI = {
    "scanning": "⏳",
    "awaiting_selection": "?",
    "suggested": "→",
    "routing": "⚡",
    "routed": "✓",
    "error": "❌"
}

# Ensure directories exist
PROCESSING_FOLDER.mkdir(exist_ok=True)
PROCESSED_ARCHIVE.mkdir(exist_ok=True)


class ProtocolTemplate:
    """Pre-built protocol templates"""
    
    TEMPLATES = {
        "karsen_schedule": {
            "name": "KARSEN Schedule",
            "description": "Creates calendar events from KARSEN departure schedule",
            "detects": ["KARSEN"],
            "routes_to": ["calendar"],
            "confidence_threshold": 0.85,
            "enabled": False
        },
        "bills_invoices": {
            "name": "Bills & Invoices",
            "description": "Files bills to Drive and creates due date calendar events",
            "detects": ["invoice", "bill", "payment due", "amount due"],
            "routes_to": ["drive", "calendar"],
            "confidence_threshold": 0.75,
            "enabled": False
        },
        "meeting_screenshots": {
            "name": "Meeting Screenshots",
            "description": "OCR meeting screenshots and save to notes",
            "detects": ["meeting", "zoom", "teams", "agenda"],
            "routes_to": ["notes"],
            "confidence_threshold": 0.70,
            "enabled": False
        },
        "receipts": {
            "name": "Receipts",
            "description": "Track expenses from receipt images",
            "detects": ["receipt", "total", "paid", "transaction"],
            "routes_to": ["expense_tracker"],
            "confidence_threshold": 0.75,
            "enabled": False
        },
        "screenshot_archive": {
            "name": "Screenshot Archive",
            "description": "Archive general screenshots",
            "detects": [],  # Matches all
            "routes_to": ["archive"],
            "confidence_threshold": 0.50,
            "enabled": True  # Default fallback
        }
    }


class ProgressiveRouter:
    """Main routing system with progressive trust"""
    
    def __init__(self, user_id: str = "jh", dry_run: bool = False):
        self.user_id = user_id
        self.dry_run = dry_run
        self.user_dir = USERS_DIR / user_id
        self.trust_file = self.user_dir / "protocol_trust.json"
        self.undo_stack_file = self.user_dir / "undo_stack.json"
        self.templates_file = self.user_dir / "protocol_templates.json"
        self.paused_file = self.user_dir / ".paused"
        
        # Ensure user directory exists
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
        # Load state
        self.trust_data = self._load_trust()
        self.undo_stack = self._load_undo_stack()
        self.templates = self._load_templates()
        self.is_paused = self.paused_file.exists()
        
        # Initialize protocols
        self.exclusion_protocol = ExclusionProtocol()
        self.dedup_protocol = DeduplicationProtocol()
        self.unpack_protocol = AutoUnpackProtocol()
        self.relevancy_protocol = ContentRelevancyProtocol()
        
        # Track build time
        self.start_time = datetime.now()
    
    def _load_trust(self) -> dict:
        """Load protocol trust data"""
        if self.trust_file.exists():
            with open(self.trust_file, 'r') as f:
                return json.load(f)
        
        return {
            "user": self.user_id,
            "protocol_trust": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_trust(self):
        """Save protocol trust data"""
        self.trust_data["last_updated"] = datetime.now().isoformat()
        with open(self.trust_file, 'w') as f:
            json.dump(self.trust_data, indent=2, fp=f)
    
    def _load_undo_stack(self) -> list:
        """Load undo stack"""
        if self.undo_stack_file.exists():
            with open(self.undo_stack_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_undo_stack(self):
        """Save undo stack"""
        # Keep only last 7 days
        cutoff = datetime.now() - timedelta(days=7)
        self.undo_stack = [
            item for item in self.undo_stack
            if datetime.fromisoformat(item["timestamp"]) > cutoff
        ]
        
        with open(self.undo_stack_file, 'w') as f:
            json.dump(self.undo_stack, indent=2, fp=f)
    
    def _load_templates(self) -> dict:
        """Load protocol templates"""
        if self.templates_file.exists():
            with open(self.templates_file, 'r') as f:
                return json.load(f)
        
        # Initialize with default templates
        templates = ProtocolTemplate.TEMPLATES.copy()
        with open(self.templates_file, 'w') as f:
            json.dump(templates, indent=2, fp=f)
        return templates
    
    def _save_templates(self):
        """Save protocol templates"""
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, indent=2, fp=f)
    
    def pause(self):
        """Pause all automation"""
        self.paused_file.touch()
        self.is_paused = True
        print("\n⏸️  All automation paused")
        print("   Everything will require manual confirmation")
        print(f"   Resume anytime: 8825 inbox resume\n")
    
    def resume(self):
        """Resume automation"""
        if self.paused_file.exists():
            self.paused_file.unlink()
        self.is_paused = False
        print("\n▶️  Automation resumed\n")
    
    def scan_file(self, file_path: Path) -> Dict:
        """Scan file and extract content"""
        result = {
            "file": str(file_path),
            "filename": file_path.name,
            "type": file_path.suffix.lower(),
            "size": file_path.stat().st_size,
            "ocr_text": "",
            "keywords": []
        }
        
        # OCR for images
        if result["type"] in [".png", ".jpg", ".jpeg", ".gif"]:
            try:
                img = Image.open(file_path)
                result["ocr_text"] = pytesseract.image_to_string(img).strip()
                result["keywords"] = self._extract_keywords(result["ocr_text"])
            except Exception as e:
                result["error"] = str(e)
        
        return result
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        text_lower = text.lower()
        keywords = []
        
        # Check all template keywords
        for template_id, template in self.templates.items():
            if not template.get("enabled", False):
                continue
            
            for keyword in template.get("detects", []):
                if keyword.lower() in text_lower:
                    keywords.append(keyword)
        
        return list(set(keywords))
    
    def match_protocols(self, scan_result: Dict) -> List[Dict]:
        """Match file against available protocols"""
        matches = []
        
        for template_id, template in self.templates.items():
            if not template.get("enabled", False):
                continue
            
            # Calculate confidence
            confidence = 0.0
            reasons = []
            
            # Keyword matching
            detects = template.get("detects", [])
            if not detects:  # Matches all (like archive)
                confidence = template.get("confidence_threshold", 0.5)
                reasons.append("Default fallback")
            else:
                matched_keywords = [
                    kw for kw in detects
                    if kw.lower() in scan_result.get("ocr_text", "").lower()
                ]
                if matched_keywords:
                    confidence = min(0.95, len(matched_keywords) / len(detects) + 0.5)
                    reasons.append(f"Keywords: {', '.join(matched_keywords)}")
            
            # Get trust level for this protocol
            trust_key = f"{template_id}_{scan_result['type']}"
            trust_info = self.trust_data["protocol_trust"].get(trust_key, {})
            trust_level = trust_info.get("level", 0)
            
            # Boost confidence based on trust
            if trust_level > 0:
                confidence = min(0.99, confidence + (trust_level * 0.05))
                reasons.append(f"Trust level {trust_level}")
            
            if confidence >= template.get("confidence_threshold", 0.5):
                matches.append({
                    "template_id": template_id,
                    "name": template["name"],
                    "description": template["description"],
                    "routes_to": template["routes_to"],
                    "confidence": confidence,
                    "trust_level": trust_level,
                    "reasons": reasons
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches
    
    def _update_filename_status(self, file_path: Path, status: str):
        """Update filename with status emoji prefix"""
        emoji = STATUS_EMOJI.get(status, "")
        
        # Get clean filename (remove existing prefix if present)
        clean_name = file_path.name
        if clean_name.startswith("[") and "] " in clean_name:
            clean_name = clean_name.split("] ", 1)[1]
        
        # Create new name with status prefix
        new_name = f"[{emoji}] {clean_name}"
        new_path = file_path.parent / new_name
        
        # Rename if different and doesn't exist
        if file_path != new_path and not new_path.exists():
            file_path.rename(new_path)
        
        return new_path
    
    def move_to_processing(self, file_path: Path) -> Path:
        """Move file to processing folder"""
        dest = PROCESSING_FOLDER / file_path.name
        
        # Avoid name collisions
        counter = 1
        while dest.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            dest = PROCESSING_FOLDER / f"{stem}_{counter}{suffix}"
            counter += 1
        
        if not self.dry_run:
            shutil.move(str(file_path), str(dest))
        
        return dest
    
    def process_file(self, file_path: Path, selected_protocol: Optional[str] = None) -> Dict:
        """Process a single file"""
        # Move to processing folder
        processing_path = self.move_to_processing(file_path)
        processing_path = self._update_filename_status(processing_path, "scanning")
        
        # Scan file
        scan_result = self.scan_file(processing_path)
        
        # Match protocols
        matches = self.match_protocols(scan_result)
        
        if not matches:
            processing_path = self._update_filename_status(processing_path, "error")
            return {
                "status": "error",
                "message": "No protocols matched",
                "file": str(processing_path)
            }
        
        # Get trust info for top match
        top_match = matches[0]
        trust_key = f"{top_match['template_id']}_{scan_result['type']}"
        trust_info = self.trust_data["protocol_trust"].get(trust_key, {
            "level": 0,
            "successful_uses": 0,
            "failed_uses": 0,
            "last_used": None,
            "created": datetime.now().isoformat()
        })
        
        trust_level = trust_info["level"]
        
        # Check for confidence decay (30 days)
        if trust_info.get("last_used"):
            last_used = datetime.fromisoformat(trust_info["last_used"])
            days_since = (datetime.now() - last_used).days
            if days_since > 30 and trust_level > 0:
                trust_level = max(0, trust_level - 1)
                print(f"\n⚠️  {top_match['name']} demoted to Level {trust_level} (not used in {days_since} days)\n")
        
        # Determine action based on trust level
        if self.is_paused or trust_level == 0:
            # Level 0: Manual selection
            processing_path = self._update_filename_status(processing_path, "awaiting_selection")
            return {
                "status": "awaiting_selection",
                "file": str(processing_path),
                "scan_result": scan_result,
                "matches": matches,
                "trust_level": trust_level
            }
        
        elif trust_level == 1:
            # Level 1: Auto-suggested
            processing_path = self._update_filename_status(processing_path, "suggested")
            return {
                "status": "suggested",
                "file": str(processing_path),
                "scan_result": scan_result,
                "suggested_protocol": top_match,
                "trust_level": trust_level
            }
        
        elif trust_level == 2:
            # Level 2: Auto-applied, needs confirmation
            processing_path = self._update_filename_status(processing_path, "routing")
            
            if not self.dry_run:
                self._execute_routing(processing_path, top_match, scan_result)
            
            processing_path = self._update_filename_status(processing_path, "routed")
            
            return {
                "status": "auto_applied",
                "file": str(processing_path),
                "protocol": top_match,
                "trust_level": trust_level,
                "needs_confirmation": True
            }
        
        else:  # trust_level >= 3
            # Level 3: Full automation
            processing_path = self._update_filename_status(processing_path, "routing")
            
            if not self.dry_run:
                self._execute_routing(processing_path, top_match, scan_result)
            
            processing_path = self._update_filename_status(processing_path, "routed")
            
            # Auto-cleanup after 24 hours
            cleanup_time = datetime.now() + timedelta(hours=24)
            
            return {
                "status": "auto_routed",
                "file": str(processing_path),
                "protocol": top_match,
                "trust_level": trust_level,
                "auto_cleanup_at": cleanup_time.isoformat()
            }
    
    def _execute_routing(self, file_path: Path, protocol: Dict, scan_result: Dict):
        """Execute the routing (placeholder for actual routing logic)"""
        # This is where actual routing happens (calendar, drive, etc.)
        # For now, just log it
        print(f"   → Routing {file_path.name} via {protocol['name']}")
        
        # Archive to processed folder
        archive_path = PROCESSED_ARCHIVE / datetime.now().strftime("%Y-%m-%d")
        archive_path.mkdir(exist_ok=True)
        
        dest = archive_path / file_path.name
        shutil.copy2(str(file_path), str(dest))
    
    def confirm_routing(self, file_path: str, success: bool = True):
        """Confirm routing success or failure"""
        file_path = Path(file_path)
        
        # Extract protocol info from recent processing
        # (In real implementation, would track this better)
        
        if success:
            # Promote protocol
            print(f"✅ Confirmed: {file_path.name}")
            
            # Clean up from processing folder
            if file_path.exists() and file_path.parent == PROCESSING_FOLDER:
                file_path.unlink()
        else:
            # Demote protocol
            print(f"❌ Correction needed: {file_path.name}")
            # Move back to downloads for reprocessing
            dest = DOWNLOADS / file_path.name
            if file_path.exists():
                shutil.move(str(file_path), str(dest))
    
    def batch_process(self, files: List[Path]) -> Dict:
        """Process multiple files and group results"""
        # First, filter exclusions
        exclusion_results = self.exclusion_protocol.filter_batch(files)
        
        # Auto-unpack any archives
        processable = exclusion_results["processable"]
        archives_to_unpack = [f for f in processable if self.unpack_protocol.is_archive(f)]
        
        if archives_to_unpack:
            print("\n📦 Auto-unpacking archives...")
            for archive in archives_to_unpack:
                result = self.unpack_protocol.unpack_archive(archive)
                if result["success"]:
                    print(f"   ✓ {archive.name} - {result['files_extracted']} files")
                    if result.get("deduplication", {}).get("duplicates", 0) > 0:
                        dedup = result["deduplication"]
                        print(f"     ⚠️  {dedup['duplicates']} duplicates (already processed)")
        
        # Then check for duplicates on remaining files
        non_archives = [f for f in processable if not self.unpack_protocol.is_archive(f)]
        dedup_results = self.dedup_protocol.scan_batch(non_archives)
        
        # Check content relevancy
        unique_files = [Path(item["file"]) for item in dedup_results["unique"]]
        relevancy_results = self.relevancy_protocol.batch_check(unique_files)
        
        # Show filtering reports
        if exclusion_results["excluded"]["critical"] or exclusion_results["excluded"]["sticky"]:
            print("\n🚫 Excluded Files:")
            for category in ["critical", "sticky", "custom"]:
                excluded = exclusion_results["excluded"][category]
                if excluded:
                    print(f"\n{category.upper()}:")
                    for item in excluded:
                        print(f"  • {item['filename']} - {item['reason']}")
        
        # Show relevancy report
        if relevancy_results["redundant"] or relevancy_results["stale"]:
            print("\n📊 Content Relevancy:")
            if relevancy_results["redundant"]:
                print(f"\n  ⚠️  Redundant: {len(relevancy_results['redundant'])} files")
                for item in relevancy_results["redundant"]:
                    check = item["check"]
                    print(f"    • {item['filename']} - {check['reason']}")
            
            if relevancy_results["stale"]:
                print(f"\n  ⏰ Stale: {len(relevancy_results['stale'])} files")
                for item in relevancy_results["stale"]:
                    check = item["check"]
                    print(f"    • {item['filename']} - {check['age_days']} days old")
            
            if relevancy_results["partial"]:
                print(f"\n  🔀 Partial: {len(relevancy_results['partial'])} files (mixed content)")
        
        if dedup_results["duplicates"]:
            print("\n⚠️  Duplicates Skipped:")
            for dup in dedup_results["duplicates"]:
                print(f"  • {dup['filename']} - {dup['reason']}")
        
        # Process only novel content
        processable_files = [Path(item["file"]) for item in relevancy_results["novel"]]
        
        results = {
            "awaiting_selection": [],
            "suggested": [],
            "auto_applied": [],
            "auto_routed": [],
            "errors": [],
            "excluded": exclusion_results["excluded"],
            "duplicates": dedup_results["duplicates"],
            "archives_unpacked": len(archives_to_unpack),
            "redundant": relevancy_results["redundant"],
            "stale": relevancy_results["stale"],
            "partial": relevancy_results["partial"]
        }
        
        for file_path in processable_files:
            result = self.process_file(file_path)
            status = result["status"]
            
            if status == "error":
                results["errors"].append(result)
            elif status == "awaiting_selection":
                results["awaiting_selection"].append(result)
            elif status == "suggested":
                results["suggested"].append(result)
            elif status == "auto_applied":
                results["auto_applied"].append(result)
            elif status == "auto_routed":
                results["auto_routed"].append(result)
        
        return results
    
    def show_batch_summary(self, results: Dict):
        """Show smart batch confirmation"""
        print("\n" + "="*70)
        print("⚡ Batch Processing Complete")
        print("="*70)
        
        # Show exclusions summary
        total_excluded = sum(len(results.get("excluded", {}).get(cat, [])) for cat in ["critical", "sticky", "custom"])
        if total_excluded > 0:
            print(f"\n🚫 Excluded: {total_excluded} files (kept in Downloads)")
        
        # Show archives summary
        if results.get("archives_unpacked", 0) > 0:
            print(f"\n📦 Archives unpacked: {results['archives_unpacked']}")
        
        # Show duplicates summary
        if results.get("duplicates"):
            print(f"\n⚠️  Duplicates: {len(results['duplicates'])} files (skipped)")
        
        # Show redundant content summary
        if results.get("redundant"):
            print(f"\n⚠️  Redundant: {len(results['redundant'])} files (already in system)")
        
        # Show stale content summary
        if results.get("stale"):
            print(f"\n⏰ Stale: {len(results['stale'])} files (outdated content)")
        
        # Group by protocol
        protocols = {}
        for result in results.get("auto_applied", []) + results.get("auto_routed", []):
            protocol_name = result.get("protocol", {}).get("name", "Unknown")
            if protocol_name not in protocols:
                protocols[protocol_name] = []
            protocols[protocol_name].append(result)
        
        # Show grouped results
        for protocol_name, items in protocols.items():
            print(f"\n{protocol_name} ({len(items)} items):")
            for item in items:
                file_name = Path(item["file"]).name
                print(f"  ✓ {file_name}")
        
        # Show items needing attention
        if results.get("awaiting_selection"):
            print(f"\n📋 {len(results['awaiting_selection'])} items need manual selection")
        
        if results.get("suggested"):
            print(f"\n→ {len(results['suggested'])} items have suggestions")
        
        if results.get("errors"):
            print(f"\n❌ {len(results['errors'])} items had errors")
        
        print("\n" + "="*70)
        print("[✓ All Good] [Review Individual] [Undo Batch]")
        print("="*70 + "\n")
    
    def show_undo_stack(self):
        """Show undo stack"""
        if not self.undo_stack:
            print("\n✅ No recent actions to undo\n")
            return
        
        print("\n" + "="*70)
        print("Recent Actions (last 7 days):")
        print("="*70)
        
        for i, item in enumerate(self.undo_stack[-10:], 1):  # Show last 10
            timestamp = datetime.fromisoformat(item["timestamp"])
            time_str = timestamp.strftime("%b %d, %I:%M %p")
            print(f"{i}. {time_str} - {item['description']}")
        
        print("\nSelect to undo: [number] or [cancel]")
        print("="*70 + "\n")
    
    def celebrate_achievement(self, protocol_name: str, level: int, success_count: int):
        """Show achievement celebration"""
        if level == 3 and success_count == 10:
            print("\n" + "="*70)
            print("🎉 Achievement Unlocked!")
            print("="*70)
            print(f"\n{protocol_name} reached Level 3")
            print(f"{success_count} successful routes, 0 corrections")
            print("\nYour inbox is getting smarter!")
            print("="*70 + "\n")


def main():
    """CLI for progressive router"""
    import sys
    
    router = ProgressiveRouter()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  progressive_router.py scan [--dry-run] [--screenshots]")
        print("  progressive_router.py status")
        print("  progressive_router.py undo")
        print("  progressive_router.py pause")
        print("  progressive_router.py resume")
        print("  progressive_router.py templates")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "scan":
        dry_run = "--dry-run" in sys.argv
        include_screenshots = "--screenshots" in sys.argv
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No changes will be made\n")
        
        # Find files in Downloads
        files = [f for f in DOWNLOADS.iterdir() if f.is_file() and not f.name.startswith(".")]
        
        # Optionally include screenshots
        if include_screenshots and SCREENSHOT_INTAKE.exists():
            screenshot_files = [f for f in SCREENSHOT_INTAKE.iterdir() if f.is_file() and not f.name.startswith(".")]
            files.extend(screenshot_files)
            print(f"Including {len(screenshot_files)} screenshots from intake folder")
        
        if not files:
            print("\n✅ No files to process\n")
            sys.exit(0)
        
        print(f"\nFound {len(files)} files in Downloads")
        
        if dry_run:
            print("\nWould process:")
            for f in files:
                print(f"  • {f.name}")
            print("\n[Run For Real] [Cancel]")
        else:
            results = router.batch_process(files)
            router.show_batch_summary(results)
    
    elif command == "status":
        # Show processing folder status
        processing_files = list(PROCESSING_FOLDER.iterdir())
        
        if not processing_files:
            print("\n✅ No files in processing\n")
        else:
            print(f"\nProcessing ({len(processing_files)} items):")
            for f in processing_files:
                print(f"  {f.name}")
            print()
    
    elif command == "undo":
        router.show_undo_stack()
    
    elif command == "pause":
        router.pause()
    
    elif command == "resume":
        router.resume()
    
    elif command == "templates":
        print("\nAvailable Protocol Templates:")
        print("="*70)
        for template_id, template in router.templates.items():
            status = "✓" if template.get("enabled") else " "
            print(f"[{status}] {template['name']}")
            print(f"    {template['description']}")
        print("="*70 + "\n")
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
