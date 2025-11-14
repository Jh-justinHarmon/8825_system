#!/usr/bin/env python3
"""
Mine Kayson's user testing session for platform mentions and valued features
"""

from docx import Document
from pathlib import Path
import re
import json
from datetime import datetime

def extract_text_from_docx(filepath):
    """Extract all text from Word document"""
    doc = Document(filepath)
    text = []
    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)
    return '\n'.join(text)

def find_platform_mentions(text):
    """Find mentions of platforms/tools"""
    platforms = []
    
    # Common patterns for platform mentions
    patterns = [
        r'(?:use|using|used|on|platform|tool|site|website|app|application)\s+(?:called\s+)?([A-Z][a-zA-Z0-9\s]{2,30})',
        r'([A-Z][a-zA-Z0-9]{2,20})(?:\.com|\.io|\.ai)',
        r'(?:like|similar to|compared to|better than)\s+([A-Z][a-zA-Z0-9\s]{2,30})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        platforms.extend(matches)
    
    # Clean up matches
    platforms = [p.strip() for p in platforms if len(p.strip()) > 2]
    
    # Remove common false positives
    exclude = ['The', 'This', 'That', 'These', 'Those', 'When', 'Where', 'What', 'Which', 'Who']
    platforms = [p for p in platforms if p not in exclude]
    
    return list(set(platforms))

def extract_features_mentioned(text):
    """Extract features and AI enhancements mentioned"""
    features = []
    
    # Split into sentences
    sentences = re.split(r'[.!?]\s+', text)
    
    # Keywords that indicate feature mentions
    feature_keywords = [
        'feature', 'functionality', 'capability', 'enhancement',
        'ai', 'artificial intelligence', 'machine learning', 'automation',
        'helps', 'allows', 'enables', 'can', 'ability to',
        'like', 'love', 'appreciate', 'value', 'useful', 'helpful'
    ]
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in feature_keywords):
            features.append(sentence.strip())
    
    return features

def extract_positive_mentions(text):
    """Extract things Kayson specifically liked or valued"""
    positive = []
    
    sentences = re.split(r'[.!?]\s+', text)
    
    positive_keywords = [
        'like', 'love', 'great', 'excellent', 'helpful', 'useful',
        'appreciate', 'value', 'impressed', 'amazing', 'fantastic',
        'really good', 'works well', 'easy', 'intuitive'
    ]
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in positive_keywords):
            positive.append(sentence.strip())
    
    return positive

def extract_ai_enhancements(text):
    """Extract specific AI enhancements mentioned"""
    ai_features = []
    
    sentences = re.split(r'[.!?]\s+', text)
    
    ai_keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'ml',
        'automated', 'automation', 'intelligent', 'smart',
        'suggests', 'recommends', 'predicts', 'learns',
        'natural language', 'nlp', 'chatbot', 'assistant'
    ]
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in ai_keywords):
            ai_features.append(sentence.strip())
    
    return ai_features

def mine_kayson_session(filepath):
    """Mine Kayson's session for platform and feature insights"""
    print(f"\n{'='*80}")
    print("Mining Kayson's User Testing Session")
    print(f"{'='*80}\n")
    
    # Extract text
    print(f"Reading: {filepath.name}")
    text = extract_text_from_docx(filepath)
    
    print(f"Extracted {len(text)} characters\n")
    
    # Mine for insights
    print("Analyzing content...\n")
    
    platforms = find_platform_mentions(text)
    features = extract_features_mentioned(text)
    positive = extract_positive_mentions(text)
    ai_enhancements = extract_ai_enhancements(text)
    
    # Create structured output
    insights = {
        'session_id': 'Kayson_20250828',
        'participant': 'Kayson',
        'date': '2025-08-28',
        'analyzed_at': datetime.now().isoformat(),
        'platforms_mentioned': platforms,
        'features_valued': features[:15],  # Top 15
        'positive_mentions': positive[:15],  # Top 15
        'ai_enhancements': ai_enhancements[:10],  # Top 10
        'raw_text_length': len(text)
    }
    
    # Display results
    print(f"{'─'*80}")
    print("🔍 PLATFORMS MENTIONED:")
    print(f"{'─'*80}")
    if platforms:
        for i, platform in enumerate(platforms, 1):
            print(f"{i}. {platform}")
    else:
        print("(Scanning full text for platform names...)")
    
    print(f"\n{'─'*80}")
    print("✨ AI ENHANCEMENTS VALUED:")
    print(f"{'─'*80}")
    for i, feature in enumerate(ai_enhancements[:10], 1):
        print(f"{i}. {feature}")
    
    print(f"\n{'─'*80}")
    print("💡 FEATURES VALUED:")
    print(f"{'─'*80}")
    for i, feature in enumerate(features[:10], 1):
        print(f"{i}. {feature}")
    
    print(f"\n{'─'*80}")
    print("👍 POSITIVE MENTIONS:")
    print(f"{'─'*80}")
    for i, mention in enumerate(positive[:10], 1):
        print(f"{i}. {mention}")
    
    # Save insights
    output_dir = Path(__file__).parent.parent.parent / 'focuses' / 'joju' / 'user_engagement' / 'insights'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'Kayson_20250828_platform_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ Analysis saved to: {output_file.name}")
    print(f"{'='*80}\n")
    
    # Also save full text for manual review
    text_file = output_dir / 'Kayson_20250828_full_transcript.txt'
    with open(text_file, 'w') as f:
        f.write(text)
    
    print(f"📄 Full transcript saved for manual review: {text_file.name}\n")
    
    return insights

def main():
    # Find Kayson's file
    kayson_file = Path("/Users/justinharmon/Downloads/8825_inbox/processing/lane_b/Kayson User Test - 2025_08_28 12_58 MDT - Notes by Gemini.docx")
    
    if not kayson_file.exists():
        print(f"❌ File not found: {kayson_file}")
        return
    
    insights = mine_kayson_session(kayson_file)
    
    # Print summary for manual verification
    print("\n" + "="*80)
    print("MANUAL REVIEW NEEDED:")
    print("="*80)
    print("\nPlease review the full transcript to identify:")
    print("1. The exact name of the platform Kayson mentioned")
    print("2. Specific features he valued")
    print("3. AI enhancements he highlighted")
    print("\nFull transcript location:")
    print("focuses/joju/user_engagement/insights/Kayson_20250828_full_transcript.txt")
    print()

if __name__ == "__main__":
    main()
