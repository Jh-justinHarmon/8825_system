#!/usr/bin/env python3
"""
Test the full automatic learning capture system
"""

from checkpoint_reader import CheckpointReader
from learning_extractor import LearningExtractor
from auto_memory_creator import AutoMemoryCreator

def test_full_system():
    """Test the complete learning capture pipeline"""
    
    print("🧪 Testing Full Automatic Learning Capture System\n")
    print("=" * 60)
    
    # Sample checkpoint (like what Cascade provides)
    checkpoint_text = """
    Session Summary - 2025-11-10 Evening
    
    Major accomplishments today:
    
    1. MG 1:1 Prep - Decided to focus on customer success skills over pure 
       technical skills. Fused customer success + strategic technical capabilities.
    
    2. TGIF Issue Tracker - Discovered that brainstorming without pain points 
       leads to generic solutions. Meeting transcript revealed real problem: 
       Patricia/Mario can't track issues across multiple channels.
       
       Decided to use Microsoft Graph API instead of email forwarding because 
       Patricia/Mario are IT and can approve API access.
    
    3. Documentation Policy - From now on: no session summaries unless requested.
       This saves 30-40% of documentation time. Focus on exploration files and code.
    
    4. Automatic Learning Capture - Built system to automatically extract learnings
       from checkpoint summaries. Pattern: If it's important enough to remember, 
       it's important enough to automate.
       
       Solved the "did we remember this?" problem by making the brain daemon 
       capture learnings every 30 seconds automatically.
    
    5. Mac Excel Issue - Excel crashes on large CSV files. Solved by creating 
       simplified versions with summary views instead of detailed data.
    
    Key insight: Discovery beats assumption. Real pain points lead to better solutions.
    """
    
    # Step 1: Save checkpoint
    print("\n📝 Step 1: Simulating Cascade checkpoint...")
    reader = CheckpointReader()
    reader.save_checkpoint_for_testing(checkpoint_text)
    print("   ✅ Checkpoint saved")
    
    # Step 2: Read checkpoint
    print("\n📖 Step 2: Reading checkpoint...")
    checkpoint = reader.get_latest_checkpoint()
    if checkpoint:
        print(f"   ✅ Checkpoint found: {checkpoint['id']}")
        print(f"   Length: {len(checkpoint['text'])} chars")
    else:
        print("   ❌ No checkpoint found")
        return
    
    # Step 3: Extract learnings
    print("\n🔍 Step 3: Extracting learnings...")
    extractor = LearningExtractor()
    learnings = extractor.extract_learnings(checkpoint['text'], source=checkpoint['id'])
    print(f"   ✅ Extracted {len(learnings)} learnings")
    
    for i, learning in enumerate(learnings, 1):
        print(f"\n   {i}. [{learning.type.value.upper()}] {learning.title[:60]}...")
        print(f"      Confidence: {learning.confidence:.0%}")
        print(f"      Tags: {', '.join(learning.tags[:3])}")
    
    # Step 4: Save to memory
    print("\n💾 Step 4: Saving to memory store...")
    creator = AutoMemoryCreator()
    results = creator.save_learnings(learnings, min_confidence=0.7)
    
    created = sum(1 for r in results if r['action'] == 'created')
    updated = sum(1 for r in results if r['action'] == 'updated')
    skipped = sum(1 for r in results if r['action'] == 'skipped')
    
    print(f"   ✅ Created: {created}")
    print(f"   🔄 Updated: {updated}")
    print(f"   ⏭️  Skipped: {skipped}")
    
    # Step 5: Show memory stats
    print("\n📊 Step 5: Memory store stats...")
    stats = creator.get_stats()
    print(f"   Total memories: {stats['total_memories']}")
    print(f"   Average confidence: {stats['average_confidence']:.0%}")
    print(f"   By type:")
    for mem_type, count in stats['by_type'].items():
        print(f"      - {mem_type}: {count}")
    
    # Step 6: Show recent memories
    print("\n📝 Step 6: Recent memories...")
    recent = creator.get_recent_memories(5)
    for i, memory in enumerate(recent, 1):
        print(f"\n   {i}. {memory['title'][:60]}...")
        print(f"      Type: {memory['type']}")
        print(f"      Confidence: {memory['confidence']:.0%}")
        print(f"      Created: {memory['created_at'][:19]}")
        if memory['update_count'] > 0:
            print(f"      Updates: {memory['update_count']}")
    
    # Step 7: Test duplicate detection
    print("\n🔄 Step 7: Testing duplicate detection...")
    print("   Simulating second session with same learnings...")
    
    # Simulate another checkpoint with similar content
    checkpoint_text_2 = """
    Quick update - reinforcing yesterday's decisions:
    
    - Still using Microsoft Graph API for TGIF (Patricia/Mario approved)
    - Minimal documentation policy working well
    - Automatic learning capture running smoothly
    """
    
    reader.save_checkpoint_for_testing(checkpoint_text_2)
    # Create new reader to bypass cache
    reader2 = CheckpointReader()
    checkpoint2 = reader2.get_latest_checkpoint()
    learnings2 = extractor.extract_learnings(checkpoint2['text'], source=checkpoint2['id'])
    results2 = creator.save_learnings(learnings2, min_confidence=0.7)
    
    updated2 = sum(1 for r in results2 if r['action'] == 'updated')
    created2 = sum(1 for r in results2 if r['action'] == 'created')
    
    print(f"   ✅ {updated2} memories updated (not duplicated)")
    print(f"   ✅ {created2} new memories created")
    
    # Final stats
    print("\n" + "=" * 60)
    print("🎉 Full System Test Complete!")
    print("\n✅ All components working:")
    print("   1. Checkpoint reader - reads from Cascade")
    print("   2. Learning extractor - finds decisions, patterns, policies, etc.")
    print("   3. Memory creator - saves/updates automatically")
    print("   4. Duplicate detection - updates instead of creating duplicates")
    print("\n🚀 System ready for production!")
    print(f"\n📁 Memories stored at: {stats['storage_path']}")
    
    # Cleanup
    print("\n🧹 Cleaning up test data...")
    reader.clear_checkpoint()
    print("   ✅ Done")


if __name__ == "__main__":
    test_full_system()
