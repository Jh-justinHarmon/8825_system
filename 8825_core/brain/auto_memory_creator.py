#!/usr/bin/env python3
"""
Auto Memory Creator - Automatically creates/updates memories from extracted learnings
"""

import json
import hashlib
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from learning_extractor import Learning, LearningType

class AutoMemoryCreator:
    """Automatically creates and manages memories from learnings"""
    
    def __init__(self, memory_store_path: Optional[Path] = None):
        """
        Initialize the auto-memory creator
        
        Args:
            memory_store_path: Path to store memories (default: ~/.8825/auto_memories.json)
        """
        if memory_store_path is None:
            self.memory_store_path = Path.home() / ".8825" / "auto_memories.json"
        else:
            self.memory_store_path = memory_store_path
        
        # Ensure directory exists
        self.memory_store_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing memories
        self.memories = self._load_memories()
    
    def _load_memories(self) -> Dict[str, Dict]:
        """Load existing memories from disk"""
        if self.memory_store_path.exists():
            try:
                with open(self.memory_store_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading memories: {e}")
                return {}
        return {}
    
    def _save_memories(self):
        """Save memories to disk"""
        try:
            with open(self.memory_store_path, 'w') as f:
                json.dump(self.memories, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving memories: {e}")
    
    def _generate_memory_id(self, learning: Learning) -> str:
        """Generate a unique ID for a learning"""
        # Use hash of title + type for consistent IDs
        content = f"{learning.type.value}:{learning.title}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _calculate_similarity(self, learning1: Learning, learning2_dict: Dict) -> float:
        """
        Calculate similarity between a learning and existing memory
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Simple similarity based on shared words in title
        words1 = set(learning1.title.lower().split())
        words2 = set(learning2_dict['title'].lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        # Jaccard similarity
        similarity = len(intersection) / len(union)
        
        # Boost if same type
        if learning1.type.value == learning2_dict['type']:
            similarity += 0.2
        
        return min(similarity, 1.0)
    
    def find_similar_memory(self, learning: Learning, threshold: float = 0.6) -> Optional[str]:
        """
        Find existing memory similar to this learning
        
        Args:
            learning: The learning to check
            threshold: Minimum similarity score (0.0 to 1.0)
        
        Returns:
            Memory ID if similar memory found, None otherwise
        """
        best_match = None
        best_score = 0.0
        
        for memory_id, memory in self.memories.items():
            similarity = self._calculate_similarity(learning, memory)
            if similarity > best_score and similarity >= threshold:
                best_score = similarity
                best_match = memory_id
        
        return best_match
    
    def create_memory(self, learning: Learning) -> str:
        """
        Create a new memory from a learning
        
        Args:
            learning: The learning to save
        
        Returns:
            Memory ID
        """
        memory_id = self._generate_memory_id(learning)
        
        memory = {
            'id': memory_id,
            'type': learning.type.value,
            'title': learning.title,
            'content': learning.content,
            'context': learning.context,
            'confidence': learning.confidence,
            'original_confidence': learning.confidence,  # Store original for decay reset
            'tags': learning.tags,
            'source': learning.source,
            'created_at': learning.created_at,
            'updated_at': datetime.now().isoformat(),
            'update_count': 0,
            'sources': learning.sources if learning.sources else [learning.source],
            
            # Evolution tracking
            'half_life_days': learning.half_life_days,
            'tries': learning.tries,
            'successes': learning.successes,
            'failures': learning.failures,
            'last_used': learning.last_used,
            'contexts': learning.contexts if learning.contexts else [learning.context],
            'tools': learning.tools if learning.tools else [],
            'superseded_by': learning.superseded_by,
            'supersedes': learning.supersedes,
            'status': learning.status
        }
        
        self.memories[memory_id] = memory
        self._save_memories()
        
        return memory_id
    
    def update_memory(self, memory_id: str, learning: Learning):
        """
        Update an existing memory with new information
        
        Args:
            memory_id: ID of memory to update
            learning: New learning to merge
        """
        if memory_id not in self.memories:
            print(f"⚠️  Memory {memory_id} not found")
            return
        
        memory = self.memories[memory_id]
        
        # Update content (append new info)
        memory['content'] += f"\n\n[Update {memory['update_count'] + 1}]: {learning.content}"
        
        # Update confidence (average)
        old_confidence = memory['confidence']
        new_confidence = (old_confidence + learning.confidence) / 2
        memory['confidence'] = new_confidence
        
        # Merge tags (unique)
        memory['tags'] = list(set(memory['tags'] + learning.tags))
        
        # Track source
        if learning.source not in memory['sources']:
            memory['sources'].append(learning.source)
        
        # Update metadata
        memory['updated_at'] = datetime.now().isoformat()
        memory['update_count'] += 1
        
        self._save_memories()
    
    def save_learning(self, learning: Learning, auto_update: bool = True) -> Dict:
        """
        Save a learning (create new or update existing)
        
        Args:
            learning: The learning to save
            auto_update: If True, update similar memory instead of creating duplicate
        
        Returns:
            Dict with action taken and memory ID
        """
        # Check for similar memory
        similar_id = self.find_similar_memory(learning) if auto_update else None
        
        if similar_id:
            # Update existing memory
            self.update_memory(similar_id, learning)
            return {
                'action': 'updated',
                'memory_id': similar_id,
                'title': learning.title
            }
        else:
            # Create new memory
            memory_id = self.create_memory(learning)
            return {
                'action': 'created',
                'memory_id': memory_id,
                'title': learning.title
            }
    
    def save_learnings(self, learnings: List[Learning], min_confidence: float = 0.7) -> List[Dict]:
        """
        Save multiple learnings
        
        Args:
            learnings: List of learnings to save
            min_confidence: Minimum confidence threshold
        
        Returns:
            List of results for each learning
        """
        results = []
        
        for learning in learnings:
            # Skip low-confidence learnings
            if learning.confidence < min_confidence:
                results.append({
                    'action': 'skipped',
                    'reason': 'low_confidence',
                    'title': learning.title,
                    'confidence': learning.confidence
                })
                continue
            
            # Save learning
            result = self.save_learning(learning)
            results.append(result)
        
        return results
    
    def get_memory(self, memory_id: str) -> Optional[Dict]:
        """Get a memory by ID"""
        return self.memories.get(memory_id)
    
    def get_all_memories(self) -> Dict[str, Dict]:
        """Get all memories"""
        return self.memories
    
    def get_memories_by_type(self, learning_type: LearningType) -> List[Dict]:
        """Get all memories of a specific type"""
        return [
            memory for memory in self.memories.values()
            if memory['type'] == learning_type.value
        ]
    
    def get_memories_by_tag(self, tag: str) -> List[Dict]:
        """Get all memories with a specific tag"""
        return [
            memory for memory in self.memories.values()
            if tag in memory['tags']
        ]
    
    def get_recent_memories(self, count: int = 10) -> List[Dict]:
        """Get most recently updated memories"""
        sorted_memories = sorted(
            self.memories.values(),
            key=lambda m: m['updated_at'],
            reverse=True
        )
        return sorted_memories[:count]
    
    def export_to_cascade_format(self) -> List[Dict]:
        """
        Export memories in Cascade memory system format
        
        Returns:
            List of memories in Cascade format
        """
        cascade_memories = []
        
        for memory in self.memories.values():
            cascade_memory = {
                'Title': memory['title'],
                'Content': memory['content'],
                'Tags': memory['tags'],
                'UserTriggered': False,  # Auto-captured
                'Metadata': {
                    'type': memory['type'],
                    'confidence': memory['confidence'],
                    'sources': memory['sources'],
                    'created_at': memory['created_at'],
                    'updated_at': memory['updated_at'],
                    'update_count': memory['update_count']
                }
            }
            cascade_memories.append(cascade_memory)
        
        return cascade_memories
    
    def get_stats(self) -> Dict:
        """Get statistics about stored memories"""
        total = len(self.memories)
        
        by_type = {}
        for memory in self.memories.values():
            mem_type = memory['type']
            by_type[mem_type] = by_type.get(mem_type, 0) + 1
        
        avg_confidence = sum(m['confidence'] for m in self.memories.values()) / total if total > 0 else 0
        
        return {
            'total_memories': total,
            'by_type': by_type,
            'average_confidence': avg_confidence,
            'storage_path': str(self.memory_store_path)
        }


def test_auto_memory():
    """Test the auto-memory creator"""
    from learning_extractor import LearningExtractor
    
    # Sample checkpoint
    sample_checkpoint = """
    Decided to use Microsoft Graph API instead of email forwarding for TGIF issue tracker
    because Patricia/Mario are IT and can approve API access.
    
    Discovered that brainstorming solutions without understanding pain points leads to 
    generic, low-value ideas. Meeting transcript revealed specific pain.
    
    From now on: No session summaries unless explicitly requested. Checkpoint system 
    handles continuity. This saves 30-40% of documentation time.
    
    Mac Excel crashes on large CSV files. Solved by creating simplified versions with 
    fewer rows and summary views instead of detailed data.
    """
    
    # Extract learnings
    print("🔍 Extracting learnings...")
    extractor = LearningExtractor()
    learnings = extractor.extract_learnings(sample_checkpoint, source="test_session_001")
    print(f"   Found {len(learnings)} learnings\n")
    
    # Create memory store
    print("💾 Saving to memory store...")
    creator = AutoMemoryCreator()
    results = creator.save_learnings(learnings, min_confidence=0.7)
    
    # Show results
    print("\n📊 Results:")
    for result in results:
        action = result['action']
        title = result['title']
        if action == 'created':
            print(f"   ✅ Created: {title}")
        elif action == 'updated':
            print(f"   🔄 Updated: {title}")
        elif action == 'skipped':
            print(f"   ⏭️  Skipped: {title} (confidence: {result['confidence']:.1%})")
    
    # Show stats
    print("\n📈 Memory Store Stats:")
    stats = creator.get_stats()
    print(f"   Total memories: {stats['total_memories']}")
    print(f"   Average confidence: {stats['average_confidence']:.1%}")
    print(f"   By type: {stats['by_type']}")
    print(f"   Storage: {stats['storage_path']}")
    
    # Test duplicate detection
    print("\n🔄 Testing duplicate detection...")
    print("   Extracting same learnings again...")
    learnings2 = extractor.extract_learnings(sample_checkpoint, source="test_session_002")
    results2 = creator.save_learnings(learnings2, min_confidence=0.7)
    
    updated_count = sum(1 for r in results2 if r['action'] == 'updated')
    print(f"   {updated_count} memories updated (not duplicated)")
    
    # Show recent memories
    print("\n📝 Recent Memories:")
    recent = creator.get_recent_memories(3)
    for i, memory in enumerate(recent, 1):
        print(f"\n   {i}. {memory['title']}")
        print(f"      Type: {memory['type']}")
        print(f"      Confidence: {memory['confidence']:.1%}")
        print(f"      Updates: {memory['update_count']}")
        print(f"      Sources: {', '.join(memory['sources'])}")


if __name__ == "__main__":
    test_auto_memory()
