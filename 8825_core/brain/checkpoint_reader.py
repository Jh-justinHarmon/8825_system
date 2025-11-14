#!/usr/bin/env python3
"""
Checkpoint Reader - Reads checkpoint summaries from Cascade
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

class CheckpointReader:
    """Reads checkpoint summaries from Cascade workspace"""
    
    def __init__(self, workspace_path: Optional[Path] = None):
        """
        Initialize checkpoint reader
        
        Args:
            workspace_path: Path to workspace (default: auto-detect)
        """
        if workspace_path is None:
            # Auto-detect workspace
            self.workspace_path = self._find_workspace()
        else:
            self.workspace_path = Path(workspace_path)
        
        # Cascade stores checkpoints in memory system
        # Checkpoints are the summaries you see at session start
        self.checkpoint_cache = {}
        self.last_checkpoint_id = None
    
    def _find_workspace(self) -> Path:
        """Find the current workspace path"""
        # Start from current directory and look up
        current = Path.cwd()
        
        # Look for .cascade directory (indicates workspace root)
        while current != current.parent:
            if (current / ".cascade").exists():
                return current
            current = current.parent
        
        # Default to current directory
        return Path.cwd()
    
    def get_latest_checkpoint(self) -> Optional[Dict]:
        """
        Get the latest checkpoint summary
        
        Cascade checkpoint summaries are provided at session start.
        For now, we'll read from a designated location where we can
        manually place checkpoint text for testing.
        
        Returns:
            Dict with checkpoint data or None
        """
        # Check for checkpoint file in brain directory
        checkpoint_file = Path.home() / ".8825" / "latest_checkpoint.txt"
        
        if not checkpoint_file.exists():
            return None
        
        try:
            # Read checkpoint text
            with open(checkpoint_file, 'r') as f:
                checkpoint_text = f.read()
            
            # Get file modification time as checkpoint ID
            mtime = checkpoint_file.stat().st_mtime
            checkpoint_id = f"checkpoint_{int(mtime)}"
            
            # Check if this is new
            if checkpoint_id == self.last_checkpoint_id:
                return None  # Already processed
            
            checkpoint = {
                'id': checkpoint_id,
                'text': checkpoint_text,
                'timestamp': datetime.fromtimestamp(mtime).isoformat(),
                'source': str(checkpoint_file)
            }
            
            self.last_checkpoint_id = checkpoint_id
            return checkpoint
            
        except Exception as e:
            print(f"⚠️  Error reading checkpoint: {e}")
            return None
    
    def save_checkpoint_for_testing(self, checkpoint_text: str):
        """
        Save a checkpoint for testing
        
        Args:
            checkpoint_text: The checkpoint summary text
        """
        checkpoint_file = Path.home() / ".8825" / "latest_checkpoint.txt"
        checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(checkpoint_file, 'w') as f:
            f.write(checkpoint_text)
        
        print(f"✅ Checkpoint saved to {checkpoint_file}")
    
    def get_checkpoint_history(self, limit: int = 10) -> List[Dict]:
        """
        Get checkpoint history
        
        Args:
            limit: Maximum number of checkpoints to return
        
        Returns:
            List of checkpoint dicts
        """
        # For now, just return the latest
        latest = self.get_latest_checkpoint()
        return [latest] if latest else []
    
    def clear_checkpoint(self):
        """Clear the current checkpoint (for testing)"""
        checkpoint_file = Path.home() / ".8825" / "latest_checkpoint.txt"
        if checkpoint_file.exists():
            checkpoint_file.unlink()
            print("✅ Checkpoint cleared")


def test_checkpoint_reader():
    """Test the checkpoint reader"""
    
    # Create test checkpoint
    test_checkpoint = """
    Session Summary - 2025-11-10
    
    Built automatic learning capture system. Decided to use brain daemon's 30-second 
    sync to automatically extract learnings from checkpoint summaries.
    
    Discovered that manual documentation takes 30-40% of session time. From now on: 
    minimal documentation policy - no session summaries unless requested.
    
    Built three components:
    1. Learning extractor - extracts decisions, patterns, policies, solutions, mistakes
    2. Auto-memory creator - creates/updates memories automatically
    3. Brain integration - runs every 30 seconds
    
    Pattern: If it's important enough to remember, it's important enough to automate.
    
    Solved the "did we remember this?" problem by making the system remember automatically.
    """
    
    print("📝 Testing Checkpoint Reader\n")
    
    # Initialize reader
    reader = CheckpointReader()
    print(f"Workspace: {reader.workspace_path}\n")
    
    # Save test checkpoint
    print("1. Saving test checkpoint...")
    reader.save_checkpoint_for_testing(test_checkpoint)
    
    # Read checkpoint
    print("\n2. Reading checkpoint...")
    checkpoint = reader.get_latest_checkpoint()
    
    if checkpoint:
        print(f"   ✅ Found checkpoint: {checkpoint['id']}")
        print(f"   Timestamp: {checkpoint['timestamp']}")
        print(f"   Length: {len(checkpoint['text'])} chars")
        print(f"   Preview: {checkpoint['text'][:100]}...")
    else:
        print("   ❌ No checkpoint found")
    
    # Try reading again (should return None - already processed)
    print("\n3. Reading again (should be cached)...")
    checkpoint2 = reader.get_latest_checkpoint()
    if checkpoint2:
        print("   ❌ Returned checkpoint again (should be None)")
    else:
        print("   ✅ Correctly returned None (already processed)")
    
    # Clear for next test
    print("\n4. Clearing checkpoint...")
    reader.clear_checkpoint()


if __name__ == "__main__":
    test_checkpoint_reader()
