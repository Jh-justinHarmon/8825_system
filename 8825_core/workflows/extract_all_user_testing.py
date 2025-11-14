#!/usr/bin/env python3
"""
Extract quotes and insights from ALL user testing sessions
"""

import json
from pathlib import Path
from docx import Document
from collections import defaultdict
from datetime import datetime

def extract_text_from_docx(filepath):
    """Extract all text from Word document"""
    doc = Document(filepath)
    text = []
    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)
    return '\n'.join(text)

def extract_quotes(text, participant):
    """Extract notable quotes from text"""
    quotes = []
    lines = text.split('\n')
    
    # Keywords that indicate valuable feedback
    keywords = [
        'like', 'love', 'helpful', 'useful', 'great', 'easy',
        'difficult', 'confusing', 'problem', 'frustrated',
        'wish', 'would be better', 'suggest', 'recommend',
        'ai', 'feature', 'workflow', 'process'
    ]
    
    for line in lines:
        line_lower = line.lower()
        # Look for quoted text or lines with keywords
        if ('"' in line or any(kw in line_lower for kw in keywords)) and len(line) > 30:
            quotes.append({
                'text': line.strip(),
                'participant': participant,
                'type': classify_quote(line_lower)
            })
    
    return quotes[:20]  # Top 20 per session

def classify_quote(text):
    """Classify quote type"""
    if any(word in text for word in ['like', 'love', 'great', 'helpful', 'easy', 'useful']):
        return 'positive'
    elif any(word in text for word in ['difficult', 'confusing', 'problem', 'frustrated']):
        return 'pain_point'
    elif any(word in text for word in ['ai', 'artificial intelligence', 'automated']):
        return 'ai_feature'
    elif any(word in text for word in ['suggest', 'recommend', 'wish', 'would be better']):
        return 'suggestion'
    else:
        return 'general'

def group_similar_insights(all_quotes):
    """Group similar insights and count mentions"""
    # Simple grouping by keywords - in production would use semantic similarity
    themes = defaultdict(list)
    
    keywords_map = {
        'context_aware_ai': ['specific data', 'my information', 'personalized', 'context'],
        'automation': ['automate', 'automatic', 'auto-fill', 'auto-populate'],
        'ease_of_use': ['easy', 'simple', 'intuitive', 'straightforward'],
        'ai_accuracy': ['accurate', 'better than', 'more precise'],
        'workflow': ['workflow', 'process', 'steps', 'journey'],
        'customization': ['customize', 'personalize', 'tailor', 'adjust']
    }
    
    for quote in all_quotes:
        text_lower = quote['text'].lower()
        matched = False
        
        for theme, keywords in keywords_map.items():
            if any(kw in text_lower for kw in keywords):
                themes[theme].append(quote)
                matched = True
                break
        
        if not matched:
            themes['other'].append(quote)
    
    # Convert to list with counts
    grouped = []
    for theme, quotes in themes.items():
        if quotes:
            grouped.append({
                'theme': theme.replace('_', ' ').title(),
                'quotes': quotes,
                'mention_count': len(quotes),
                'users': list(set(q['participant'] for q in quotes)),
                'types': [q['type'] for q in quotes]
            })
    
    # Sort by mention count
    grouped.sort(key=lambda x: x['mention_count'], reverse=True)
    
    return grouped

def main():
    print(f"\n{'='*80}")
    print("Extracting All User Testing Data")
    print(f"{'='*80}\n")
    
    # Find all user testing files in Downloads/8825_inbox/processing/lane_b
    lane_b_dir = Path.home() / 'Downloads' / '8825_inbox' / 'processing' / 'lane_b'
    
    sessions = []
    if lane_b_dir.exists():
        for pattern in ['*User*Test*.docx', '*User*Testing*.docx']:
            sessions.extend(lane_b_dir.glob(pattern))
        
        # Exclude the summary document
        sessions = [s for s in sessions if 'Summary' not in s.name]
    
    # Remove duplicates
    sessions = list(set(sessions))
    
    print(f"Found {len(sessions)} session file(s)\n")
    
    all_quotes = []
    session_summaries = []
    
    for session_file in sessions:
        # Extract participant name
        filename = session_file.stem
        if 'Chris' in filename and 'Chrissy' not in filename:
            participant = 'Chris'
        elif 'Chrissy' in filename:
            participant = 'Chrissy'
        elif 'Kayson' in filename:
            participant = 'Kayson'
        elif 'Monique' in filename:
            participant = 'Monique'
        elif 'Philip' in filename:
            participant = 'Philip'
        else:
            participant = 'Unknown'
        
        print(f"Processing: {participant}")
        
        try:
            text = extract_text_from_docx(session_file)
            quotes = extract_quotes(text, participant)
            all_quotes.extend(quotes)
            
            session_summaries.append({
                'participant': participant,
                'date': '2025-08-28' if participant != 'Chrissy' else '2025-08-29',
                'quotes_count': len(quotes),
                'word_count': len(text.split())
            })
            
            print(f"  ✓ Extracted {len(quotes)} quotes")
            print(f"  ✓ {len(text.split())} words analyzed\n")
            
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
    
    # Group similar insights
    print(f"{'─'*80}")
    print("Grouping similar insights...\n")
    
    grouped_insights = group_similar_insights(all_quotes)
    
    for insight in grouped_insights[:10]:  # Top 10
        print(f"Theme: {insight['theme']}")
        print(f"  Mentioned by {insight['mention_count']} user(s): {', '.join(insight['users'])}")
        print()
    
    # Save comprehensive data
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_sessions': len(session_summaries),
        'total_quotes': len(all_quotes),
        'sessions': session_summaries,
        'all_quotes': all_quotes,
        'grouped_insights': grouped_insights
    }
    
    output_file = Path('/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/focuses/joju/user_engagement/all_user_testing_data.json')
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"{'='*80}")
    print(f"✅ Extraction Complete!")
    print(f"{'='*80}\n")
    print(f"Total Sessions: {len(session_summaries)}")
    print(f"Total Quotes: {len(all_quotes)}")
    print(f"Grouped Themes: {len(grouped_insights)}")
    print(f"\nData saved to: all_user_testing_data.json\n")

if __name__ == "__main__":
    main()
