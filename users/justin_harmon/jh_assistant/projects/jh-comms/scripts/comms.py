#!/usr/bin/env python3
"""
Jh COMMs - Communication Management System
Streamlined workflow with silent learning
"""

import sys
import argparse
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.context_analyzer import ContextAnalyzer
from core.response_generator import ResponseGenerator
from core.contact_matrix import ContactMatrix
from core.session_manager import SessionManager

def extract_text_from_screenshot(screenshot_path: str) -> str:
    """Extract text from screenshot using OCR"""
    try:
        import pytesseract
        from PIL import Image
        
        image = Image.open(screenshot_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"❌ OCR Error: {str(e)}")
        return ""

def copy_to_clipboard(text: str):
    """Copy text to macOS clipboard"""
    try:
        subprocess.run(['pbcopy'], input=text.encode(), check=True)
        return True
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description='Jh COMMs - Communication Management')
    parser.add_argument('--screenshot', '-s', help='Path to screenshot')
    parser.add_argument('--text', '-t', help='Direct text input')
    parser.add_argument('--contact', '-c', help='Contact name')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--end-session', action='store_true', help='End session and save learning')
    
    args = parser.parse_args()
    
    # Handle end session
    if args.end_session:
        manager = SessionManager()
        summary = manager.end_session()
        print("✅ Session ended. Learning data saved.")
        print(f"   Interactions: {summary['total_interactions']}")
        print(f"   Patterns learned: {len(summary.get('context_patterns', {}))}")
        return
    
    print("💬 Jh COMMs")
    print("=" * 60)
    
    # Initialize components
    analyzer = ContextAnalyzer()
    generator = ResponseGenerator()
    matrix = ContactMatrix()
    session = SessionManager()
    
    # Get input text
    if args.screenshot:
        print(f"\n📸 Processing screenshot...")
        text = extract_text_from_screenshot(args.screenshot)
        if not text:
            print("❌ No text extracted")
            return
    elif args.text:
        text = args.text
    elif args.interactive:
        print("\n📝 Enter message text (Ctrl+D when done):")
        text = sys.stdin.read()
    else:
        parser.print_help()
        return
    
    # Find contact (silent)
    contact_info = None
    if args.contact:
        contact_info = matrix.find_contact(name=args.contact)
    
    # Analyze context (silent)
    context = analyzer.analyze_screenshot(text, contact_info)
    
    # Get silent recommendation (not displayed)
    recommended = session.get_recommendation(context)
    
    # Store recommendation silently
    session.add_silent_note('recommendation', {
        'context': f"{context['message_type']}_{context['sentiment']}",
        'recommended': recommended,
        'urgency': context['urgency']
    })
    
    # Generate responses
    responses = generator.generate_responses(context, contact_info)
    
    # Display responses (clean, no recommendations shown)
    print("\n" + "=" * 60)
    
    for i, response in enumerate(responses, 1):
        print(f"\n{i}. {response['level'].upper()} ({response['word_count']} words)")
        print("-" * 60)
        print(response['text'])
    
    print("\n" + "=" * 60)
    
    # Interactive selection
    selected_index = None
    
    if args.interactive or sys.stdin.isatty():
        choice = input("\nSelect (1-3) or Enter to skip: ").strip()
        
        if choice in ['1', '2', '3']:
            selected_index = int(choice) - 1
            selected = responses[selected_index]
            
            if copy_to_clipboard(selected['text']):
                print(f"\n✅ {selected['level'].upper()} copied to clipboard!")
            else:
                print(f"\n✅ {selected['level'].upper()} selected")
                print(f"\n{selected['text']}")
            
            # Log interaction with contact
            if contact_info:
                matrix.log_interaction(contact_info['contact_id'], {
                    'type': 'message_response',
                    'summary': context['message_type'],
                    'response_used': selected['level']
                })
    else:
        # Non-interactive: copy standard
        selected_index = 1
        if copy_to_clipboard(responses[1]['text']):
            print("\n✅ Standard response copied!")
    
    # Log interaction (silent learning)
    session.log_interaction(context, responses, selected_index)
    
    # Show session info (minimal)
    stats = session.get_session_stats()
    print(f"\n📊 Session: {stats['interactions']} interactions")
    print(f"💾 To save learning: comms.py --end-session\n")

if __name__ == "__main__":
    main()
