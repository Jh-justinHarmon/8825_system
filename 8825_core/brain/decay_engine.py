#!/usr/bin/env python3
"""
Decay Engine - Applies time-based decay to learnings
"""

from datetime import datetime
from typing import Dict

class DecayEngine:
    """Applies time-based decay to learnings"""
    
    def apply_decay(self, memories: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Apply decay to all memories
        
        Returns updated memories
        """
        now = datetime.now()
        decayed_count = 0
        
        for memory_id, memory in memories.items():
            # Skip if recently used (resets decay)
            last_used = memory.get('last_used')
            if last_used:
                try:
                    last_used_dt = datetime.fromisoformat(last_used)
                    if (now - last_used_dt).days < 30:
                        continue  # Used recently, no decay
                except:
                    pass
            
            # Calculate age
            created_at = memory.get('created_at')
            if not created_at:
                continue
            
            try:
                created = datetime.fromisoformat(created_at)
                age_days = (now - created).days
            except:
                continue
            
            # Get half-life (default 180 days)
            half_life = memory.get('half_life_days', 180)
            
            # Apply decay
            original_confidence = memory.get('original_confidence', memory.get('confidence', 0.5))
            decay_factor = 0.5 ** (age_days / half_life)
            new_confidence = original_confidence * decay_factor
            
            # Only update if confidence changed significantly
            if abs(new_confidence - memory.get('confidence', 0)) > 0.01:
                memory['confidence'] = new_confidence
                memory['original_confidence'] = original_confidence
                decayed_count += 1
                
                # Update status based on confidence
                if new_confidence < 0.3:
                    memory['status'] = 'deprecated'
                elif new_confidence < 0.5:
                    memory['status'] = 'legacy'
                else:
                    memory['status'] = 'active'
        
        if decayed_count > 0:
            print(f"⏳ Applied decay to {decayed_count} learnings")
        
        return memories
    
    def reset_decay(self, memory: Dict):
        """Reset decay when learning is validated"""
        original = memory.get('original_confidence', memory.get('confidence', 0.5))
        memory['confidence'] = original
        memory['last_used'] = datetime.now().isoformat()
        memory['status'] = 'active'
        print(f"🔄 Reset decay for: {memory['title'][:50]}...")
    
    def get_decaying_learnings(self, memories: Dict[str, Dict], threshold: float = 0.5) -> list:
        """Get learnings that are decaying (confidence < threshold)"""
        decaying = []
        
        for memory_id, memory in memories.items():
            confidence = memory.get('confidence', 1.0)
            original = memory.get('original_confidence', confidence)
            
            if confidence < threshold and original >= threshold:
                decaying.append({
                    'id': memory_id,
                    'title': memory['title'],
                    'confidence': confidence,
                    'original_confidence': original,
                    'status': memory.get('status', 'active'),
                    'age_days': self._calculate_age(memory.get('created_at'))
                })
        
        return sorted(decaying, key=lambda x: x['confidence'])
    
    def _calculate_age(self, created_at: str) -> int:
        """Calculate age in days"""
        if not created_at:
            return 0
        try:
            created = datetime.fromisoformat(created_at)
            return (datetime.now() - created).days
        except:
            return 0


def test_decay_engine():
    """Test the decay engine"""
    from auto_memory_creator import AutoMemoryCreator
    from learning_extractor import Learning, LearningType
    from datetime import timedelta
    
    print("🧪 Testing Decay Engine\n")
    
    # Create test learnings with different ages
    creator = AutoMemoryCreator()
    
    # Recent learning (should not decay)
    recent = Learning(
        type=LearningType.DECISION,
        title="Recent: Use SuperAPI",
        content="Just started using SuperAPI",
        context="New project",
        confidence=0.9,
        tags=["api"],
        source="test"
    )
    recent.created_at = datetime.now().isoformat()
    recent.last_used = datetime.now().isoformat()
    
    # Old learning (should decay)
    old = Learning(
        type=LearningType.DECISION,
        title="Old: Use Graph API",
        content="Using Graph API for integration",
        context="Legacy project",
        confidence=0.9,
        tags=["api"],
        source="test"
    )
    old_date = datetime.now() - timedelta(days=365)  # 1 year old
    old.created_at = old_date.isoformat()
    old.last_used = old_date.isoformat()
    
    # Save learnings
    creator.save_learning(recent)
    creator.save_learning(old)
    
    print("📊 Initial State:")
    print(f"   Recent: confidence={recent.confidence:.2f}, age=0 days")
    print(f"   Old: confidence={old.confidence:.2f}, age=365 days")
    
    # Apply decay
    print("\n⏳ Applying decay...")
    engine = DecayEngine()
    memories = creator.get_all_memories()
    updated = engine.apply_decay(memories)
    
    # Check results
    print("\n📊 After Decay:")
    for memory_id, memory in updated.items():
        title = memory['title']
        conf = memory['confidence']
        status = memory.get('status', 'active')
        print(f"   {title}: confidence={conf:.2f}, status={status}")
    
    # Get decaying learnings
    print("\n⚠️  Decaying Learnings (confidence < 0.5):")
    decaying = engine.get_decaying_learnings(updated, threshold=0.5)
    for item in decaying:
        print(f"   {item['title']}: {item['confidence']:.2f} (was {item['original_confidence']:.2f})")
    
    print("\n✅ Decay Engine Test Complete!")


if __name__ == "__main__":
    test_decay_engine()
