#!/usr/bin/env python3
"""
Routing Refiner - Audit and improve multi-destination routing
Handles user-specific routing preferences and learning
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
USERS_DIR = SCRIPT_DIR / "users"
CONFIDENCE_THRESHOLD = 0.75  # Below this = needs review


class RoutingRefiner:
    """Manages routing decisions, user preferences, and learning"""
    
    def __init__(self, user_id: str = "jh"):
        self.user_id = user_id
        self.user_dir = USERS_DIR / user_id
        self.rules_file = self.user_dir / "routing_rules.json"
        self.audit_file = self.user_dir / "routing_audit.json"
        self.review_queue_file = self.user_dir / "routing_review_queue.json"
        
        # Ensure directories exist
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize rules
        self.rules = self._load_rules()
        self.audit_trail = self._load_audit_trail()
        self.review_queue = self._load_review_queue()
    
    def _load_rules(self) -> dict:
        """Load user-specific routing rules"""
        if self.rules_file.exists():
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        
        # Default rules
        return {
            "user": self.user_id,
            "version": "1.0",
            "routing_preferences": {
                "KARSEN": {
                    "destinations": ["calendar"],
                    "priority": "high",
                    "auto_route": True
                },
                "bills": {
                    "destinations": ["calendar", "drive", "ledger"],
                    "priority": "high",
                    "auto_route": True
                },
                "screenshots_default": {
                    "destinations": ["archive"],
                    "priority": "low",
                    "auto_route": True
                }
            },
            "learned_patterns": {},
            "keyword_mappings": {
                "KARSEN": "calendar",
                "invoice": "bills",
                "bill": "bills",
                "payment due": "bills",
                "finder": "folder_screenshot"
            }
        }
    
    def _save_rules(self):
        """Save routing rules"""
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, indent=2, fp=f)
    
    def _load_audit_trail(self) -> list:
        """Load routing audit trail"""
        if self.audit_file.exists():
            with open(self.audit_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_audit_trail(self):
        """Save audit trail"""
        with open(self.audit_file, 'w') as f:
            json.dump(self.audit_trail, indent=2, fp=f)
    
    def _load_review_queue(self) -> list:
        """Load items needing review"""
        if self.review_queue_file.exists():
            with open(self.review_queue_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_review_queue(self):
        """Save review queue"""
        with open(self.review_queue_file, 'w') as f:
            json.dump(self.review_queue, indent=2, fp=f)
    
    def calculate_routing_confidence(self, file_path: str, ocr_text: str) -> List[Dict]:
        """
        Calculate confidence scores for possible routing destinations
        Returns list of {destination, confidence, reason}
        """
        routing_options = []
        text_lower = ocr_text.lower()
        
        # Check keyword mappings
        for keyword, destination in self.rules["keyword_mappings"].items():
            if keyword.lower() in text_lower:
                confidence = 0.9  # High confidence for keyword matches
                routing_options.append({
                    "destination": destination,
                    "confidence": confidence,
                    "reason": f"Keyword '{keyword}' detected"
                })
        
        # Check learned patterns
        file_name = Path(file_path).name
        for pattern, destination in self.rules["learned_patterns"].items():
            if self._matches_pattern(file_name, pattern):
                confidence = 0.85  # High confidence for learned patterns
                routing_options.append({
                    "destination": destination,
                    "confidence": confidence,
                    "reason": f"Learned pattern: {pattern}"
                })
        
        # Default archive option
        if not routing_options:
            routing_options.append({
                "destination": "archive",
                "confidence": 0.5,
                "reason": "Default fallback"
            })
        
        # Sort by confidence
        routing_options.sort(key=lambda x: x["confidence"], reverse=True)
        
        return routing_options
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern (supports wildcards)"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def route_with_confidence(self, file_path: str, ocr_text: str) -> Dict:
        """
        Route file with confidence scoring
        Returns routing decision with metadata
        """
        routing_options = self.calculate_routing_confidence(file_path, ocr_text)
        
        # Select best option
        best_option = routing_options[0]
        
        decision = {
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "ocr_preview": ocr_text[:200],
            "routing_options": routing_options,
            "selected": best_option["destination"],
            "confidence": best_option["confidence"],
            "reason": best_option["reason"],
            "needs_review": best_option["confidence"] < CONFIDENCE_THRESHOLD,
            "auto_routed": best_option["confidence"] >= CONFIDENCE_THRESHOLD
        }
        
        # Add to review queue if confidence is low
        if decision["needs_review"]:
            self.review_queue.append(decision)
            self._save_review_queue()
        
        # Add to audit trail
        self.audit_trail.append(decision)
        self._save_audit_trail()
        
        return decision
    
    def review_pending(self) -> int:
        """Show items needing review, return count"""
        if not self.review_queue:
            print("\n✅ No items need review")
            return 0
        
        print(f"\n📋 Review Queue ({len(self.review_queue)} items)")
        print("="*70)
        
        for i, item in enumerate(self.review_queue, 1):
            print(f"\n{i}. {Path(item['file']).name}")
            print(f"   Suggested: {item['selected']} (confidence: {item['confidence']:.2f})")
            print(f"   Reason: {item['reason']}")
            print(f"   OCR Preview: {item['ocr_preview'][:100]}...")
            print(f"   Other options: {', '.join([o['destination'] for o in item['routing_options'][1:]])}")
        
        return len(self.review_queue)
    
    def confirm_routing(self, item_index: int, confirmed_destination: str = None):
        """
        Confirm or correct a routing decision
        If confirmed_destination is None, accepts the suggested routing
        """
        if item_index >= len(self.review_queue):
            print(f"❌ Invalid index: {item_index}")
            return
        
        item = self.review_queue[item_index]
        
        if confirmed_destination is None:
            confirmed_destination = item["selected"]
        
        # Learn from this decision
        file_pattern = self._extract_pattern(item["file"])
        if file_pattern:
            self.rules["learned_patterns"][file_pattern] = confirmed_destination
            self._save_rules()
            print(f"✅ Learned: {file_pattern} → {confirmed_destination}")
        
        # Update audit trail
        for audit_item in self.audit_trail:
            if audit_item["file"] == item["file"]:
                audit_item["user_confirmed"] = True
                audit_item["confirmed_destination"] = confirmed_destination
                audit_item["corrected"] = confirmed_destination != item["selected"]
                break
        
        self._save_audit_trail()
        
        # Remove from review queue
        self.review_queue.pop(item_index)
        self._save_review_queue()
        
        print(f"✅ Confirmed: {Path(item['file']).name} → {confirmed_destination}")
    
    def _extract_pattern(self, file_path: str) -> str:
        """Extract a learnable pattern from filename"""
        filename = Path(file_path).name
        
        # Common patterns
        if filename.startswith("IMG_"):
            return "IMG_*.jpeg"
        elif filename.startswith("Screenshot"):
            return "Screenshot*.png"
        elif "KARSEN" in filename.upper():
            return "*KARSEN*"
        
        return None
    
    def show_stats(self):
        """Show routing statistics"""
        print("\n📊 Routing Statistics")
        print("="*70)
        
        total = len(self.audit_trail)
        if total == 0:
            print("No routing decisions yet")
            return
        
        auto_routed = sum(1 for item in self.audit_trail if item.get("auto_routed", False))
        reviewed = sum(1 for item in self.audit_trail if item.get("user_confirmed", False))
        corrected = sum(1 for item in self.audit_trail if item.get("corrected", False))
        
        print(f"\nTotal decisions: {total}")
        print(f"Auto-routed: {auto_routed} ({auto_routed/total*100:.1f}%)")
        print(f"User reviewed: {reviewed} ({reviewed/total*100:.1f}%)")
        print(f"Corrections: {corrected} ({corrected/total*100:.1f}%)")
        
        # Accuracy
        if reviewed > 0:
            accuracy = (reviewed - corrected) / reviewed * 100
            print(f"\nRouting accuracy: {accuracy:.1f}%")
        
        # Learned patterns
        print(f"\nLearned patterns: {len(self.rules['learned_patterns'])}")
        for pattern, destination in self.rules["learned_patterns"].items():
            print(f"  • {pattern} → {destination}")
    
    def interactive_review(self):
        """Interactive review session"""
        while self.review_queue:
            count = self.review_pending()
            if count == 0:
                break
            
            print("\n" + "="*70)
            choice = input("\nReview item # (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.review_queue):
                    item = self.review_queue[index]
                    
                    print(f"\nSuggested: {item['selected']}")
                    print("Options:")
                    for i, opt in enumerate(item['routing_options'], 1):
                        print(f"  {i}. {opt['destination']} (confidence: {opt['confidence']:.2f})")
                    
                    decision = input("\nAccept suggestion (y), choose number, or enter custom: ").strip()
                    
                    if decision.lower() == 'y':
                        self.confirm_routing(index)
                    elif decision.isdigit():
                        opt_index = int(decision) - 1
                        if 0 <= opt_index < len(item['routing_options']):
                            destination = item['routing_options'][opt_index]['destination']
                            self.confirm_routing(index, destination)
                    else:
                        self.confirm_routing(index, decision)
                else:
                    print("❌ Invalid index")
            except ValueError:
                print("❌ Invalid input")


def main():
    """CLI for routing refiner"""
    import sys
    
    refiner = RoutingRefiner()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  routing_refiner.py review          # Show review queue")
        print("  routing_refiner.py interactive     # Interactive review session")
        print("  routing_refiner.py stats           # Show statistics")
        print("  routing_refiner.py confirm <index> [destination]  # Confirm routing")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "review":
        refiner.review_pending()
    
    elif command == "interactive":
        refiner.interactive_review()
    
    elif command == "stats":
        refiner.show_stats()
    
    elif command == "confirm":
        if len(sys.argv) < 3:
            print("❌ Usage: routing_refiner.py confirm <index> [destination]")
            sys.exit(1)
        
        index = int(sys.argv[2]) - 1
        destination = sys.argv[3] if len(sys.argv) > 3 else None
        refiner.confirm_routing(index, destination)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
