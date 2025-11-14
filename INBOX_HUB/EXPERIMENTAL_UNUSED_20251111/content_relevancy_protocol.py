#!/usr/bin/env python3
"""
Content Relevancy Protocol - Semantic deduplication and novelty detection
Checks if file content is novel, redundant, stale, or partially overlapping
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from collections import Counter
import docx
from PIL import Image
import pytesseract

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SYSTEM_ROOT = SCRIPT_DIR.parent
CONTENT_INDEX_FILE = SCRIPT_DIR / "users" / "jh" / "content_index.json"

# Search paths for existing content
SEARCH_PATHS = [
    SYSTEM_ROOT / "8825_core",
    SYSTEM_ROOT / "project_lanes",
    SYSTEM_ROOT / "INBOX_HUB" / "users" / "jh" / "processed",
    SYSTEM_ROOT / "Documents",
]

# Stale thresholds by content type
STALE_THRESHOLDS = {
    "user_feedback": 90,  # days
    "meeting_notes": 180,
    "documentation": 365,
    "code": 30,
    "default": 180
}


class ContentRelevancyProtocol:
    """Check content novelty and relevancy"""
    
    def __init__(self):
        self.content_index_file = CONTENT_INDEX_FILE
        self.content_index_file.parent.mkdir(parents=True, exist_ok=True)
        self.content_index = self._load_content_index()
    
    def _load_content_index(self) -> dict:
        """Load content index"""
        if self.content_index_file.exists():
            with open(self.content_index_file, 'r') as f:
                return json.load(f)
        
        return {
            "version": "1.0",
            "content_hashes": {},
            "entity_index": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_content_index(self):
        """Save content index"""
        self.content_index["last_updated"] = datetime.now().isoformat()
        with open(self.content_index_file, 'w') as f:
            json.dump(self.content_index, indent=2, fp=f)
    
    def extract_text_content(self, file_path: Path) -> str:
        """Extract text from various file types"""
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == '.txt':
                return file_path.read_text(encoding='utf-8', errors='ignore')
            
            elif suffix == '.md':
                return file_path.read_text(encoding='utf-8', errors='ignore')
            
            elif suffix == '.json':
                data = json.loads(file_path.read_text())
                # Extract all string values recursively
                return self._extract_json_strings(data)
            
            elif suffix == '.docx':
                doc = docx.Document(file_path)
                return '\n'.join([para.text for para in doc.paragraphs])
            
            elif suffix in ['.png', '.jpg', '.jpeg', '.gif']:
                img = Image.open(file_path)
                return pytesseract.image_to_string(img)
            
            else:
                return ""
        
        except Exception as e:
            print(f"⚠️  Could not extract text from {file_path.name}: {e}")
            return ""
    
    def _extract_json_strings(self, obj, max_depth=10, current_depth=0) -> str:
        """Recursively extract strings from JSON"""
        if current_depth > max_depth:
            return ""
        
        if isinstance(obj, str):
            return obj + " "
        elif isinstance(obj, dict):
            return " ".join(self._extract_json_strings(v, max_depth, current_depth+1) for v in obj.values())
        elif isinstance(obj, list):
            return " ".join(self._extract_json_strings(item, max_depth, current_depth+1) for item in obj)
        else:
            return str(obj) + " "
    
    def normalize_content(self, text: str) -> str:
        """Normalize content for comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove dates (various formats)
        text = re.sub(r'\d{4}[-_/]\d{2}[-_/]\d{2}', '', text)
        text = re.sub(r'\d{2}[-_/]\d{2}[-_/]\d{4}', '', text)
        text = re.sub(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},?\s+\d{4}', '', text, flags=re.IGNORECASE)
        
        # Remove timestamps
        text = re.sub(r'\d{2}:\d{2}(:\d{2})?(\s*(am|pm|mdt|pst|est))?', '', text, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common filler words
        filler_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for']
        words = text.split()
        words = [w for w in words if w not in filler_words]
        
        return ' '.join(words).strip()
    
    def calculate_content_hash(self, text: str) -> str:
        """Calculate hash of normalized content"""
        normalized = self.normalize_content(text)
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract key entities from text"""
        entities = {
            "people": [],
            "features": [],
            "dates": [],
            "keywords": []
        }
        
        # Extract people names (capitalized words)
        people_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        entities["people"] = list(set(re.findall(people_pattern, text)))
        
        # Extract feature mentions
        feature_patterns = [
            r'feature\s+[A-Z]',
            r'feature\s+\w+',
            r'[A-Z][a-z]+\s+feature'
        ]
        for pattern in feature_patterns:
            entities["features"].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Extract dates
        date_patterns = [
            r'\d{4}[-_/]\d{2}[-_/]\d{2}',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}'
        ]
        for pattern in date_patterns:
            entities["dates"].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Extract keywords (words appearing frequently)
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        word_freq = Counter(words)
        entities["keywords"] = [word for word, count in word_freq.most_common(20) if count > 2]
        
        return entities
    
    def search_existing_content(self, content_hash: str, entities: Dict) -> List[Dict]:
        """Search for similar content in the system"""
        matches = []
        
        # Check content hash index
        if content_hash in self.content_index["content_hashes"]:
            existing = self.content_index["content_hashes"][content_hash]
            matches.append({
                "type": "exact",
                "similarity": 1.0,
                "location": existing["location"],
                "incorporated_date": existing.get("date_incorporated"),
                "reason": "Exact content match"
            })
            return matches
        
        # Check entity index for semantic matches
        entity_index = self.content_index.get("entity_index", {})
        
        for existing_hash, existing_entities in entity_index.items():
            similarity = self._calculate_entity_similarity(entities, existing_entities)
            
            if similarity > 0.85:
                existing_info = self.content_index["content_hashes"].get(existing_hash, {})
                matches.append({
                    "type": "semantic",
                    "similarity": similarity,
                    "location": existing_info.get("location", "unknown"),
                    "incorporated_date": existing_info.get("date_incorporated"),
                    "reason": f"Similar content ({int(similarity*100)}% match)",
                    "matching_entities": self._get_matching_entities(entities, existing_entities)
                })
        
        # Sort by similarity
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        return matches[:5]  # Top 5 matches
    
    def _calculate_entity_similarity(self, entities1: Dict, entities2: Dict) -> float:
        """Calculate similarity between two entity sets"""
        scores = []
        
        for entity_type in ["people", "features", "keywords"]:
            set1 = set(str(e).lower() for e in entities1.get(entity_type, []))
            set2 = set(str(e).lower() for e in entities2.get(entity_type, []))
            
            if not set1 and not set2:
                continue
            
            if not set1 or not set2:
                scores.append(0.0)
                continue
            
            # Jaccard similarity
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            scores.append(intersection / union if union > 0 else 0.0)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _get_matching_entities(self, entities1: Dict, entities2: Dict) -> Dict:
        """Get overlapping entities"""
        matching = {}
        
        for entity_type in ["people", "features", "keywords"]:
            set1 = set(str(e).lower() for e in entities1.get(entity_type, []))
            set2 = set(str(e).lower() for e in entities2.get(entity_type, []))
            overlap = set1 & set2
            if overlap:
                matching[entity_type] = list(overlap)
        
        return matching
    
    def extract_metadata(self, file_path: Path, content: str) -> Dict:
        """Extract metadata from filename and content"""
        metadata = {
            "filename": file_path.name,
            "type": "default",
            "date": None,
            "age_days": None
        }
        
        # Detect content type
        filename_lower = file_path.name.lower()
        content_lower = content.lower()
        
        if any(word in filename_lower or word in content_lower for word in ["user test", "feedback", "session"]):
            metadata["type"] = "user_feedback"
        elif any(word in filename_lower or word in content_lower for word in ["meeting", "notes", "minutes"]):
            metadata["type"] = "meeting_notes"
        elif any(word in filename_lower or word in content_lower for word in ["doc", "spec", "requirements"]):
            metadata["type"] = "documentation"
        elif file_path.suffix in ['.py', '.js', '.java', '.cpp']:
            metadata["type"] = "code"
        
        # Extract date from filename
        date_patterns = [
            r'(\d{4})[-_](\d{2})[-_](\d{2})',
            r'(\d{4})(\d{2})(\d{2})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, file_path.name)
            if match:
                try:
                    year, month, day = match.groups()
                    metadata["date"] = datetime(int(year), int(month), int(day))
                    metadata["age_days"] = (datetime.now() - metadata["date"]).days
                    break
                except:
                    pass
        
        # Try file modification time if no date in filename
        if not metadata["date"]:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            metadata["date"] = mtime
            metadata["age_days"] = (datetime.now() - mtime).days
        
        return metadata
    
    def is_stale(self, metadata: Dict) -> bool:
        """Check if content is stale based on type and age"""
        if not metadata.get("age_days"):
            return False
        
        threshold = STALE_THRESHOLDS.get(metadata["type"], STALE_THRESHOLDS["default"])
        return metadata["age_days"] > threshold
    
    def check_relevancy(self, file_path: Path) -> Dict:
        """
        Main relevancy check
        Returns: novel, redundant, stale, or partial
        """
        # Extract content
        content = self.extract_text_content(file_path)
        
        if not content or len(content.strip()) < 50:
            return {
                "status": "unknown",
                "reason": "Could not extract sufficient content",
                "action": "manual_review"
            }
        
        # Calculate content hash
        content_hash = self.calculate_content_hash(content)
        
        # Extract entities
        entities = self.extract_entities(content)
        
        # Extract metadata
        metadata = self.extract_metadata(file_path, content)
        
        # Search for existing content
        similar_content = self.search_existing_content(content_hash, entities)
        
        # Check for exact match
        if similar_content and similar_content[0]["type"] == "exact":
            return {
                "status": "redundant",
                "reason": "Exact content match",
                "similarity": 1.0,
                "existing_locations": [similar_content[0]["location"]],
                "incorporated_date": similar_content[0].get("incorporated_date"),
                "action": "skip",
                "metadata": metadata
            }
        
        # Check for high semantic similarity
        if similar_content and similar_content[0]["similarity"] > 0.85:
            return {
                "status": "redundant",
                "reason": f"Similar content exists ({int(similar_content[0]['similarity']*100)}% match)",
                "similarity": similar_content[0]["similarity"],
                "existing_locations": [m["location"] for m in similar_content],
                "matching_entities": similar_content[0].get("matching_entities", {}),
                "action": "review",
                "metadata": metadata
            }
        
        # Check if stale
        if self.is_stale(metadata):
            return {
                "status": "stale",
                "reason": f"Content is {metadata['age_days']} days old",
                "age_days": metadata["age_days"],
                "threshold": STALE_THRESHOLDS.get(metadata["type"], STALE_THRESHOLDS["default"]),
                "content_type": metadata["type"],
                "action": "archive",
                "metadata": metadata,
                "similar_content": similar_content if similar_content else []
            }
        
        # Check for partial overlap
        if similar_content and 0.5 < similar_content[0]["similarity"] <= 0.85:
            return {
                "status": "partial",
                "reason": f"Partial overlap ({int(similar_content[0]['similarity']*100)}% match)",
                "similarity": similar_content[0]["similarity"],
                "existing_locations": [m["location"] for m in similar_content],
                "matching_entities": similar_content[0].get("matching_entities", {}),
                "action": "extract_novel",
                "metadata": metadata
            }
        
        # Novel content
        return {
            "status": "novel",
            "reason": "New content not found in system",
            "action": "process",
            "metadata": metadata,
            "content_hash": content_hash,
            "entities": entities
        }
    
    def register_content(self, file_path: Path, destination: str, content_hash: str = None, entities: Dict = None):
        """Register processed content in index"""
        if not content_hash:
            content = self.extract_text_content(file_path)
            content_hash = self.calculate_content_hash(content)
        
        if not entities:
            content = self.extract_text_content(file_path)
            entities = self.extract_entities(content)
        
        self.content_index["content_hashes"][content_hash] = {
            "original_file": str(file_path),
            "location": destination,
            "date_incorporated": datetime.now().isoformat(),
            "status": "incorporated"
        }
        
        self.content_index["entity_index"][content_hash] = entities
        
        self._save_content_index()
    
    def batch_check(self, files: List[Path]) -> Dict:
        """Check relevancy for batch of files"""
        results = {
            "novel": [],
            "redundant": [],
            "stale": [],
            "partial": [],
            "unknown": []
        }
        
        for file_path in files:
            check = self.check_relevancy(file_path)
            status = check["status"]
            
            results[status].append({
                "file": str(file_path),
                "filename": file_path.name,
                "check": check
            })
        
        return results
    
    def show_relevancy_report(self, results: Dict):
        """Show relevancy check report"""
        print("\n" + "="*70)
        print("🔍 Content Relevancy Report")
        print("="*70)
        
        total = sum(len(results[status]) for status in results)
        print(f"\nScanned: {total} files")
        print(f"  ✓ Novel: {len(results['novel'])}")
        print(f"  ⚠️  Redundant: {len(results['redundant'])}")
        print(f"  ⏰ Stale: {len(results['stale'])}")
        print(f"  🔀 Partial: {len(results['partial'])}")
        print(f"  ? Unknown: {len(results['unknown'])}")
        
        # Show redundant details
        if results["redundant"]:
            print("\n" + "-"*70)
            print("Redundant Content:")
            print("-"*70)
            for item in results["redundant"]:
                check = item["check"]
                print(f"\n❌ {item['filename']}")
                print(f"   {check['reason']}")
                if check.get("existing_locations"):
                    print(f"   Exists at:")
                    for loc in check["existing_locations"][:3]:
                        print(f"     • {loc}")
                if check.get("incorporated_date"):
                    print(f"   Incorporated: {check['incorporated_date'][:10]}")
        
        # Show stale details
        if results["stale"]:
            print("\n" + "-"*70)
            print("Stale Content:")
            print("-"*70)
            for item in results["stale"]:
                check = item["check"]
                print(f"\n⏰ {item['filename']}")
                print(f"   Age: {check['age_days']} days (threshold: {check['threshold']})")
                print(f"   Type: {check['content_type']}")
        
        # Show partial details
        if results["partial"]:
            print("\n" + "-"*70)
            print("Partial Overlap:")
            print("-"*70)
            for item in results["partial"]:
                check = item["check"]
                print(f"\n🔀 {item['filename']}")
                print(f"   {check['reason']}")
                if check.get("matching_entities"):
                    print(f"   Matching entities:")
                    for entity_type, entities in check["matching_entities"].items():
                        print(f"     {entity_type}: {', '.join(entities[:5])}")
        
        # Show novel details
        if results["novel"]:
            print("\n" + "-"*70)
            print(f"Novel Content ({len(results['novel'])} files):")
            print("-"*70)
            for item in results["novel"]:
                print(f"  ✓ {item['filename']}")
        
        print("\n" + "="*70 + "\n")


def main():
    """CLI for content relevancy protocol"""
    import sys
    
    protocol = ContentRelevancyProtocol()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  content_relevancy_protocol.py check <file>")
        print("  content_relevancy_protocol.py scan <directory>")
        print("  content_relevancy_protocol.py register <file> <destination>")
        print("  content_relevancy_protocol.py stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            print("Usage: content_relevancy_protocol.py check <file>")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        result = protocol.check_relevancy(file_path)
        
        print(f"\nFile: {result.get('metadata', {}).get('filename', file_path.name)}")
        print(f"Status: {result['status'].upper()}")
        print(f"Reason: {result['reason']}")
        print(f"Action: {result['action']}")
        
        if result.get('similarity'):
            print(f"Similarity: {int(result['similarity']*100)}%")
        
        if result.get('existing_locations'):
            print(f"\nExisting locations:")
            for loc in result['existing_locations']:
                print(f"  • {loc}")
        
        if result.get('metadata'):
            meta = result['metadata']
            if meta.get('age_days'):
                print(f"\nAge: {meta['age_days']} days")
            print(f"Type: {meta['type']}")
        
        print()
    
    elif command == "scan":
        if len(sys.argv) < 3:
            print("Usage: content_relevancy_protocol.py scan <directory>")
            sys.exit(1)
        
        directory = Path(sys.argv[2])
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            sys.exit(1)
        
        files = [f for f in directory.iterdir() if f.is_file() and not f.name.startswith('.')]
        results = protocol.batch_check(files)
        protocol.show_relevancy_report(results)
    
    elif command == "register":
        if len(sys.argv) < 4:
            print("Usage: content_relevancy_protocol.py register <file> <destination>")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        destination = sys.argv[3]
        
        protocol.register_content(file_path, destination)
        print(f"✅ Registered: {file_path.name} → {destination}")
    
    elif command == "stats":
        print("\n" + "="*70)
        print("Content Index Stats")
        print("="*70)
        print(f"\nTracked content hashes: {len(protocol.content_index['content_hashes'])}")
        print(f"Entity index entries: {len(protocol.content_index.get('entity_index', {}))}")
        print(f"Last updated: {protocol.content_index['last_updated']}")
        print("="*70 + "\n")
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
