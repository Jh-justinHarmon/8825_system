#!/usr/bin/env python3
"""
Router
Routes files to appropriate destinations based on match results
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def route_file(file_path, match_result, config):
    """
    Route file based on match result
    
    Args:
        file_path: Path to file
        match_result: Match result from project_matcher
        config: Project configuration
    """
    action = match_result['action']
    project = match_result['project']
    confidence = match_result['confidence']
    destination = match_result['destination']
    
    if action == 'auto_route':
        # High confidence - auto move
        auto_route(file_path, destination, project, confidence)
    
    elif action == 'suggest':
        # Medium confidence - notify and suggest
        suggest_route(file_path, destination, project, confidence, match_result)
    
    else:
        # Low confidence - ask user
        ask_user(file_path, match_result)

def auto_route(file_path, destination, project, confidence):
    """Automatically route file to destination"""
    try:
        # Ensure destination exists
        os.makedirs(destination, exist_ok=True)
        
        # Get destination path
        filename = os.path.basename(file_path)
        dest_path = os.path.join(destination, filename)
        
        # Handle duplicates
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base}_{timestamp}{ext}"
            dest_path = os.path.join(destination, filename)
        
        # Move file
        shutil.move(file_path, dest_path)
        
        print(f"✅ Auto-routed to {project} ({confidence}%)")
        print(f"   → {dest_path}")
        
        # Send notification
        send_notification(
            title="File Auto-Routed",
            message=f"{filename} → {project} ({confidence}%)",
            sound=False
        )
        
    except Exception as e:
        print(f"❌ Error auto-routing: {str(e)}")

def suggest_route(file_path, destination, project, confidence, match_result):
    """Suggest route to user with notification"""
    filename = os.path.basename(file_path)
    
    print(f"💡 Suggested: {project} ({confidence}%)")
    print(f"   File: {filename}")
    print(f"   Reasoning: {', '.join(match_result['reasoning'][:3])}")
    print(f"   Destination: {destination}")
    print(f"\n   To accept: Move file manually or approve in notification")
    
    # Send interactive notification
    send_notification(
        title=f"Route to {project}?",
        message=f"{filename} ({confidence}% match)",
        sound=True
    )

def ask_user(file_path, match_result):
    """Ask user for routing decision"""
    filename = os.path.basename(file_path)
    
    print(f"❓ Low confidence match")
    print(f"   File: {filename}")
    print(f"   Best guess: {match_result['project']} ({match_result['confidence']}%)")
    print(f"\n   Top 3 matches:")
    
    # Show top 3 scores
    sorted_scores = sorted(
        match_result['all_scores'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    for proj, score in sorted_scores:
        print(f"      {proj}: {score}%")
    
    print(f"\n   Please route manually")
    
    # Send notification
    send_notification(
        title="Manual Routing Needed",
        message=f"{filename} - unclear destination",
        sound=True
    )

def send_notification(title, message, sound=False):
    """Send macOS notification"""
    try:
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        
        if sound:
            script += ' sound name "default"'
        
        subprocess.run(['osascript', '-e', script], check=False)
    except:
        pass  # Notifications are optional

if __name__ == "__main__":
    # Test
    import sys
    import json
    
    if len(sys.argv) > 1:
        print("Router test - would route file based on match result")
