#!/usr/bin/env python3
"""
Usage Tracker - Tracks when learnings are used and their outcomes
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from auto_memory_creator import AutoMemoryCreator

class UsageTracker:
    """Tracks learning usage and outcomes"""
    
    def __init__(self, memory_creator: AutoMemoryCreator):
        self.memory_creator = memory_creator
        self.usage_log_path = Path.home() / ".8825" / "usage_log.json"
        self.usage_log = self._load_usage_log()
    
    def _load_usage_log(self) -> list:
        """Load usage log from disk"""
        if self.usage_log_path.exists():
            try:
                with open(self.usage_log_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading usage log: {e}")
                return []
        return []
    
    def _save_usage_log(self):
        """Save usage log to disk"""
        try:
            self.usage_log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.usage_log_path, 'w') as f:
                json.dump(self.usage_log, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving usage log: {e}")
    
    def record_usage(self, learning_id: str, success: bool, context: str = ""):
        """
        Record that a learning was used
        
        Args:
            learning_id: ID of the learning
            success: Did it work?
            context: What context was it used in?
        """
        # Get the learning
        memory = self.memory_creator.get_memory(learning_id)
        if not memory:
            print(f"⚠️  Learning {learning_id} not found")
            return
        
        # Update usage stats
        memory['tries'] = memory.get('tries', 0) + 1
        if success:
            memory['successes'] = memory.get('successes', 0) + 1
        else:
            memory['failures'] = memory.get('failures', 0) + 1
        
        memory['last_used'] = datetime.now().isoformat()
        
        # Add context if new
        contexts = memory.get('contexts', [])
        if context and context not in contexts:
            contexts.append(context)
            memory['contexts'] = contexts
        
        # Log the usage
        self.usage_log.append({
            'learning_id': learning_id,
            'success': success,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save
        self.memory_creator.memories[learning_id] = memory
        self.memory_creator._save_memories()
        self._save_usage_log()
        
        print(f"📊 Recorded usage: {memory['title'][:50]}... → {'✅' if success else '❌'}")
    
    def get_usage_stats(self, learning_id: str) -> Dict:
        """Get usage statistics for a learning"""
        memory = self.memory_creator.get_memory(learning_id)
        if not memory:
            return {}
        
        tries = memory.get('tries', 0)
        successes = memory.get('successes', 0)
        
        return {
            'tries': tries,
            'successes': successes,
            'failures': memory.get('failures', 0),
            'success_rate': successes / tries if tries > 0 else 0,
            'last_used': memory.get('last_used'),
            'contexts': memory.get('contexts', []),
            'age_days': self._calculate_age(memory.get('created_at'))
        }
    
    def _calculate_age(self, created_at: str) -> int:
        """Calculate age in days"""
        if not created_at:
            return 0
        try:
            created = datetime.fromisoformat(created_at)
            return (datetime.now() - created).days
        except:
            return 0
    
    def get_recent_usage(self, days: int = 30) -> list:
        """Get usage in last N days"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        recent = []
        for entry in self.usage_log:
            try:
                timestamp = datetime.fromisoformat(entry['timestamp']).timestamp()
                if timestamp > cutoff:
                    recent.append(entry)
            except:
                continue
        
        return recent
    
    def get_top_learnings(self, limit: int = 10) -> list:
        """Get most-used learnings"""
        memories = self.memory_creator.get_all_memories()
        
        # Sort by tries
        sorted_memories = sorted(
            memories.values(),
            key=lambda m: m.get('tries', 0),
            reverse=True
        )
        
        return sorted_memories[:limit]


def test_usage_tracker():
    """Test the usage tracker"""
    from auto_memory_creator import AutoMemoryCreator
    from learning_extractor import Learning, LearningType
    
    print("🧪 Testing Usage Tracker\n")
    
    # Create test learning
    creator = AutoMemoryCreator()
    learning = Learning(
        type=LearningType.DECISION,
        title="Use Microsoft Graph API for TGIF",
        content="Decided to use Microsoft Graph API because Patricia/Mario can approve",
        context="TGIF project, IT approval available",
        confidence=0.9,
        tags=["tgif", "api", "microsoft"],
        source="test_session"
    )
    
    # Save learning
    result = creator.save_learning(learning)
    learning_id = result['memory_id']
    print(f"✅ Created learning: {learning_id}\n")
    
    # Create tracker
    tracker = UsageTracker(creator)
    
    # Record some usage
    print("📊 Recording usage...\n")
    tracker.record_usage(learning_id, success=True, context="TGIF production")
    tracker.record_usage(learning_id, success=True, context="TGIF testing")
    tracker.record_usage(learning_id, success=False, context="Project X (no IT approval)")
    tracker.record_usage(learning_id, success=True, context="TGIF production")
    
    # Get stats
    print("\n📈 Usage Stats:")
    stats = tracker.get_usage_stats(learning_id)
    print(f"   Tries: {stats['tries']}")
    print(f"   Successes: {stats['successes']}")
    print(f"   Failures: {stats['failures']}")
    print(f"   Success Rate: {stats['success_rate']:.0%}")
    print(f"   Contexts: {stats['contexts']}")
    print(f"   Last Used: {stats['last_used']}")
    
    # Get recent usage
    print("\n📅 Recent Usage (last 30 days):")
    recent = tracker.get_recent_usage(30)
    for entry in recent:
        success_icon = "✅" if entry['success'] else "❌"
        print(f"   {success_icon} {entry['context']} - {entry['timestamp'][:19]}")
    
    print("\n✅ Usage Tracker Test Complete!")


if __name__ == "__main__":
    test_usage_tracker()
