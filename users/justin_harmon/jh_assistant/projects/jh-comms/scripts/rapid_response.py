#!/usr/bin/env python3
"""
Rapid Response Tool
Desktop CLI for generating quick responses from screenshots
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

def extract_text_from_screenshot(screenshot_path: str) -> str:
    """
    Extract text from screenshot using OCR
    
    Args:
        screenshot_path: Path to screenshot image
    
    Returns:
        Extracted text
    """
    try:
        import pytesseract
        from PIL import Image
        
        image = Image.open(screenshot_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"❌ OCR Error: {str(e)}")
        print("   Make sure tesseract is installed: brew install tesseract")
        return ""

def copy_to_clipboard(text: str):
    """Copy text to macOS clipboard"""
    try:
        subprocess.run(['pbcopy'], input=text.encode(), check=True)
        print("📋 Copied to clipboard!")
    except:
        print("⚠️  Could not copy to clipboard")

def main():
    parser = argparse.ArgumentParser(description='Rapid Response Tool - Generate quick responses')
    parser.add_argument('--screenshot', '-s', help='Path to screenshot')
    parser.add_argument('--text', '-t', help='Direct text input (skip OCR)')
    parser.add_argument('--contact', '-c', help='Contact name')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    print("🚀 Rapid Response Tool")
    print("=" * 60)
    
    # Initialize components
    analyzer = ContextAnalyzer()
    generator = ResponseGenerator()
    matrix = ContactMatrix()
    
    # Get input text
    if args.screenshot:
        print(f"\n📸 Processing screenshot: {args.screenshot}")
        text = extract_text_from_screenshot(args.screenshot)
        if not text:
            print("❌ No text extracted from screenshot")
            return
    elif args.text:
        text = args.text
    elif args.interactive:
        print("\n📝 Enter message text (press Ctrl+D when done):")
        text = sys.stdin.read()
    else:
        parser.print_help()
        return
    
    print(f"\n📋 Extracted text ({len(text)} characters)")
    print("-" * 60)
    print(text[:200] + "..." if len(text) > 200 else text)
    print("-" * 60)
    
    # Find contact
    contact_info = None
    if args.contact:
        contact_info = matrix.find_contact(name=args.contact)
        if contact_info:
            print(f"\n👤 Contact: {contact_info['name']}")
            print(f"   Relationship: {contact_info['relationship']['type']}")
        else:
            print(f"\n⚠️  Contact '{args.contact}' not found in matrix")
    
    # Analyze context
    print("\n🔍 Analyzing context...")
    context = analyzer.analyze_screenshot(text, contact_info)
    
    print(f"   Type: {context['message_type']}")
    print(f"   Sentiment: {context['sentiment']}")
    print(f"   Urgency: {context['urgency']}")
    print(f"   Requires action: {context['requires_action']}")
    
    # Generate responses
    print("\n💬 Generating responses...")
    responses = generator.generate_responses(context, contact_info)
    
    print("\n" + "=" * 60)
    print("RESPONSE OPTIONS")
    print("=" * 60)
    
    for i, response in enumerate(responses, 1):
        print(f"\n{i}. {response['level'].upper()} ({response['word_count']} words)")
        print("-" * 60)
        print(response['text'])
    
    # Interactive selection
    print("\n" + "=" * 60)
    
    if args.interactive or sys.stdin.isatty():
        choice = input("\nSelect response (1-3) or press Enter to skip: ").strip()
        
        if choice in ['1', '2', '3']:
            selected = responses[int(choice) - 1]
            copy_to_clipboard(selected['text'])
            print(f"\n✅ {selected['level'].upper()} response copied to clipboard!")
            
            # Log interaction
            if contact_info:
                matrix.log_interaction(contact_info['contact_id'], {
                    'type': 'message_response',
                    'summary': context['message_type'],
                    'response_used': selected['level']
                })
        else:
            print("\n👋 No response selected")
    else:
        # Non-interactive: copy standard response
        copy_to_clipboard(responses[1]['text'])
        print("\n✅ Standard response copied to clipboard!")
    
    print()

if __name__ == "__main__":
    main()
