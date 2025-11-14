#!/usr/bin/env python3
"""
Competition Resolver - Resolves competitions between learnings based on success rates
"""

from typing import Dict, List, Optional
from datetime import datetime

class CompetitionResolver:
    """Resolves competitions between learnings"""
    
    MIN_TRIES_TO_RESOLVE = 5  # Need at least 5 tries each to resolve
    SIGNIFICANT_DIFFERENCE = 1.2  # 20% better to be considered "winner"
    
    def check_competitions(self, memories: Dict, usage_tracker) -> List[Dict]:
        """
        Check all active competitions and resolve if possible
        
        Args:
            memories: Dict of all memories
            usage_tracker: UsageTracker instance
        
        Returns:
            List of resolutions
        """
        resolutions = []
        
        for memory_id, memory in memories.items():
            if 'competing_with' not in memory:
                continue
            
            # Get stats for old learning
            old_stats = usage_tracker.get_usage_stats(memory_id)
            
            # Find new learning
            new_title = memory['competing_with']
            new_id = self._find_memory_by_title(new_title, memories)
            
            if not new_id:
                continue
            
            new_stats = usage_tracker.get_usage_stats(new_id)
            
            # Need minimum tries to resolve
            if old_stats['tries'] < self.MIN_TRIES_TO_RESOLVE or new_stats['tries'] < self.MIN_TRIES_TO_RESOLVE:
                continue
            
            # Resolve competition
            resolution = self._resolve(old_stats, new_stats, memory_id, new_id, memories)
            if resolution:
                resolutions.append(resolution)
        
        return resolutions
    
    def _resolve(self, old_stats: Dict, new_stats: Dict, old_id: str, new_id: str, memories: Dict) -> Optional[Dict]:
        """
        Determine winner based on success rates
        
        Args:
            old_stats: Usage stats for old learning
            new_stats: Usage stats for new learning
            old_id: ID of old learning
            new_id: ID of new learning
            memories: Dict of all memories
        
        Returns:
            Resolution dict or None
        """
        old_rate = old_stats['success_rate']
        new_rate = new_stats['success_rate']
        
        # New tool significantly better (20%+ higher success)
        if new_rate > old_rate * self.SIGNIFICANT_DIFFERENCE:
            memories[old_id]['status'] = 'superseded'
            memories[old_id]['superseded_by'] = new_id
            memories[old_id]['superseded_at'] = datetime.now().isoformat()
            del memories[old_id]['competing_with']  # Competition resolved
            
            memories[new_id]['status'] = 'active'
            memories[new_id]['supersedes'] = old_id
            
            return {
                'winner': 'new',
                'old_id': old_id,
                'new_id': new_id,
                'old_title': memories[old_id]['title'],
                'new_title': memories[new_id]['title'],
                'reason': f"New tool {new_rate:.0%} success vs {old_rate:.0%}",
                'old_rate': old_rate,
                'new_rate': new_rate
            }
        
        # Old tool still better
        elif old_rate > new_rate * self.SIGNIFICANT_DIFFERENCE:
            memories[new_id]['status'] = 'failed_replacement'
            memories[new_id]['failed_to_replace'] = old_id
            del memories[old_id]['competing_with']  # Competition resolved
            
            return {
                'winner': 'old',
                'old_id': old_id,
                'new_id': new_id,
                'old_title': memories[old_id]['title'],
                'new_title': memories[new_id]['title'],
                'reason': f"Old tool still better: {old_rate:.0%} vs {new_rate:.0%}",
                'old_rate': old_rate,
                'new_rate': new_rate
            }
        
        # Both valid in different contexts (close race)
        else:
            memories[old_id]['status'] = 'legacy_but_valid'
            memories[new_id]['status'] = 'active'
            del memories[old_id]['competing_with']  # Competition resolved
            
            return {
                'winner': 'both',
                'old_id': old_id,
                'new_id': new_id,
                'old_title': memories[old_id]['title'],
                'new_title': memories[new_id]['title'],
                'reason': f"Both valid: {old_rate:.0%} vs {new_rate:.0%}",
                'old_rate': old_rate,
                'new_rate': new_rate
            }
    
    def _find_memory_by_title(self, title: str, memories: Dict) -> Optional[str]:
        """Find memory ID by title"""
        for memory_id, memory in memories.items():
            if memory.get('title') == title:
                return memory_id
        return None
    
    def get_competition_status(self, memories: Dict, usage_tracker) -> List[Dict]:
        """Get status of all active competitions"""
        status = []
        
        for memory_id, memory in memories.items():
            if 'competing_with' not in memory:
                continue
            
            old_stats = usage_tracker.get_usage_stats(memory_id)
            new_title = memory['competing_with']
            new_id = self._find_memory_by_title(new_title, memories)
            
            if not new_id:
                continue
            
            new_stats = usage_tracker.get_usage_stats(new_id)
            
            status.append({
                'old_id': memory_id,
                'old_title': memory['title'],
                'old_tries': old_stats['tries'],
                'old_rate': old_stats['success_rate'],
                'new_title': new_title,
                'new_tries': new_stats['tries'],
                'new_rate': new_stats['success_rate'],
                'can_resolve': (old_stats['tries'] >= self.MIN_TRIES_TO_RESOLVE and 
                               new_stats['tries'] >= self.MIN_TRIES_TO_RESOLVE)
            })
        
        return status


def test_competition_resolver():
    """Test the competition resolver"""
    from auto_memory_creator import AutoMemoryCreator
    from learning_extractor import Learning, LearningType
    from usage_tracker import UsageTracker
    from tool_evolution_detector import ToolEvolutionDetector
    
    print("🧪 Testing Competition Resolver\n")
    
    # Create old learning
    creator = AutoMemoryCreator()
    old_learning = Learning(
        type=LearningType.DECISION,
        title="Use Graph API",
        content="Using Graph API for integration",
        context="Production",
        confidence=0.9,
        tags=["api"],
        source="test"
    )
    old_result = creator.save_learning(old_learning)
    old_id = old_result['memory_id']
    
    # Create new learning
    new_learning = Learning(
        type=LearningType.DECISION,
        title="Use SuperAPI",
        content="Migrated from Graph API to SuperAPI because faster",
        context="Production",
        confidence=0.9,
        tags=["api"],
        source="test"
    )
    new_result = creator.save_learning(new_learning)
    new_id = new_result['memory_id']
    
    # Start competition
    detector = ToolEvolutionDetector()
    replacement = detector.detect_replacement(
        new_learning.content,
        new_learning.title,
        creator.get_all_memories()
    )
    
    if replacement:
        detector.start_competition(replacement, creator)
        print("✅ Competition started\n")
    
    # Simulate usage
    tracker = UsageTracker(creator)
    print("📊 Simulating usage...")
    
    # Old API: 3 successes, 2 failures (60% success)
    for i in range(3):
        tracker.record_usage(old_id, success=True, context="Legacy system")
    for i in range(2):
        tracker.record_usage(old_id, success=False, context="New feature")
    
    # New API: 5 successes, 0 failures (100% success)
    for i in range(5):
        tracker.record_usage(new_id, success=True, context="Production")
    
    print("\n📈 Usage Stats:")
    old_stats = tracker.get_usage_stats(old_id)
    new_stats = tracker.get_usage_stats(new_id)
    print(f"   Old: {old_stats['tries']} tries, {old_stats['success_rate']:.0%} success")
    print(f"   New: {new_stats['tries']} tries, {new_stats['success_rate']:.0%} success")
    
    # Resolve competition
    print("\n🏆 Resolving competition...")
    resolver = CompetitionResolver()
    resolutions = resolver.check_competitions(creator.get_all_memories(), tracker)
    
    if resolutions:
        for resolution in resolutions:
            print(f"   Winner: {resolution['winner']}")
            print(f"   Reason: {resolution['reason']}")
            print(f"   Old: {resolution['old_title'][:40]}... ({resolution['old_rate']:.0%})")
            print(f"   New: {resolution['new_title'][:40]}... ({resolution['new_rate']:.0%})")
    else:
        print("   No resolutions yet (need more data)")
    
    print("\n✅ Competition Resolver Test Complete!")


if __name__ == "__main__":
    test_competition_resolver()
