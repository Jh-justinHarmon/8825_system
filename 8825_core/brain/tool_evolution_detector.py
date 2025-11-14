#!/usr/bin/env python3
"""
Tool Evolution Detector - Detects when new tools replace old ones
"""

import re
from typing import Optional, Dict
from datetime import datetime

class ToolEvolutionDetector:
    """Detects tool replacements and evolution"""
    
    REPLACEMENT_SIGNALS = [
        "instead of",
        "replaced",
        "migrated from",
        "deprecated",
        "better than",
        "switched from",
        "moved from",
        "upgraded from"
    ]
    
    def detect_replacement(self, new_learning_content: str, new_learning_title: str, existing_memories: Dict) -> Optional[Dict]:
        """
        Detect if new learning replaces an old tool
        
        Args:
            new_learning_content: Content of new learning
            new_learning_title: Title of new learning
            existing_memories: Dict of existing memories
        
        Returns:
            Dict with old_learning_id and relationship, or None
        """
        content_lower = new_learning_content.lower()
        
        # Check for replacement signals
        for signal in self.REPLACEMENT_SIGNALS:
            if signal in content_lower:
                # Extract old tool name
                old_tool = self._extract_old_tool(new_learning_content, signal)
                
                if old_tool:
                    # Find existing learning with that tool
                    old_learning_id = self._find_learning_with_tool(old_tool, existing_memories)
                    
                    if old_learning_id:
                        return {
                            'old_learning_id': old_learning_id,
                            'new_learning_title': new_learning_title,
                            'signal': signal,
                            'old_tool': old_tool,
                            'detected_at': datetime.now().isoformat()
                        }
        
        return None
    
    def _extract_old_tool(self, content: str, signal: str) -> Optional[str]:
        """
        Extract old tool name from content
        
        Example: "Migrated from Graph API to SuperAPI" → "Graph API"
        """
        # Pattern: signal + "old tool" (capture until "to" or punctuation)
        pattern = rf"{signal}\s+([A-Za-z0-9\s]+?)(?:\s+to\s+|\s+because|\.|,|$)"
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            old_tool = match.group(1).strip()
            # Clean up common words
            old_tool = re.sub(r'\s+(the|a|an)\s+', ' ', old_tool, flags=re.IGNORECASE)
            return old_tool
        
        return None
    
    def _find_learning_with_tool(self, tool_name: str, memories: Dict) -> Optional[str]:
        """
        Find existing learning that mentions this tool
        
        Args:
            tool_name: Name of tool to find
            memories: Dict of memories
        
        Returns:
            Memory ID or None
        """
        tool_lower = tool_name.lower()
        
        for memory_id, memory in memories.items():
            # Check title and content
            title_lower = memory.get('title', '').lower()
            content_lower = memory.get('content', '').lower()
            
            if tool_lower in title_lower or tool_lower in content_lower:
                return memory_id
        
        return None
    
    def start_competition(self, replacement: Dict, memory_creator) -> Dict:
        """
        Start competition between old and new learning
        
        Args:
            replacement: Dict with old_learning_id and new_learning_title
            memory_creator: AutoMemoryCreator instance
        
        Returns:
            Competition record
        """
        old_memory = memory_creator.get_memory(replacement['old_learning_id'])
        
        if not old_memory:
            return {}
        
        # Mark as competing
        old_memory['competing_with'] = replacement['new_learning_title']
        old_memory['competition_started'] = datetime.now().isoformat()
        old_memory['competition_signal'] = replacement['signal']
        
        # Save
        memory_creator.memories[replacement['old_learning_id']] = old_memory
        memory_creator._save_memories()
        
        print(f"🥊 Competition started: {old_memory['title'][:40]}... vs {replacement['new_learning_title'][:40]}...")
        
        return {
            'old_id': replacement['old_learning_id'],
            'new_title': replacement['new_learning_title'],
            'started_at': datetime.now().isoformat()
        }
    
    def get_active_competitions(self, memories: Dict) -> list:
        """Get all active competitions"""
        competitions = []
        
        for memory_id, memory in memories.items():
            if 'competing_with' in memory:
                competitions.append({
                    'old_id': memory_id,
                    'old_title': memory['title'],
                    'new_title': memory['competing_with'],
                    'started': memory.get('competition_started'),
                    'signal': memory.get('competition_signal')
                })
        
        return competitions


def test_tool_evolution_detector():
    """Test the tool evolution detector"""
    from auto_memory_creator import AutoMemoryCreator
    from learning_extractor import Learning, LearningType
    
    print("🧪 Testing Tool Evolution Detector\n")
    
    # Create old learning
    creator = AutoMemoryCreator()
    old_learning = Learning(
        type=LearningType.DECISION,
        title="Use Microsoft Graph API for email",
        content="Using Microsoft Graph API for email integration",
        context="Production system",
        confidence=0.9,
        tags=["api", "email"],
        source="test"
    )
    result = creator.save_learning(old_learning)
    print(f"✅ Created old learning: {old_learning.title}\n")
    
    # Create detector
    detector = ToolEvolutionDetector()
    
    # Test replacement detection
    new_content = "Migrated from Microsoft Graph API to SuperAPI because it's 10x faster"
    new_title = "Use SuperAPI for email integration"
    
    print("🔍 Detecting replacement...")
    replacement = detector.detect_replacement(new_content, new_title, creator.get_all_memories())
    
    if replacement:
        print(f"   ✅ Detected replacement!")
        print(f"   Old tool: {replacement['old_tool']}")
        print(f"   Signal: {replacement['signal']}")
        print(f"   Old learning ID: {replacement['old_learning_id']}")
        
        # Start competition
        print("\n🥊 Starting competition...")
        competition = detector.start_competition(replacement, creator)
        print(f"   Competition: {competition}")
        
        # Check active competitions
        print("\n📊 Active Competitions:")
        active = detector.get_active_competitions(creator.get_all_memories())
        for comp in active:
            print(f"   {comp['old_title'][:40]}... vs {comp['new_title'][:40]}...")
            print(f"   Signal: {comp['signal']}, Started: {comp['started'][:19]}")
    else:
        print("   ❌ No replacement detected")
    
    print("\n✅ Tool Evolution Detector Test Complete!")


if __name__ == "__main__":
    test_tool_evolution_detector()
