#!/usr/bin/env python3
"""
Quick Sentiment Recording Script
Usage: python3 record_sentiment.py "Your feedback here" [rating 1-5]
"""

import sys
from sentiment_monitor import SentimentMonitor

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 record_sentiment.py \"Your feedback\" [rating]")
        print("\nExamples:")
        print("  python3 record_sentiment.py \"System is much faster now!\" 5")
        print("  python3 record_sentiment.py \"Still seeing some errors\"")
        return
    
    text = sys.argv[1]
    rating = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    monitor = SentimentMonitor()
    result = monitor.record_sentiment(
        source='manual',
        text=text,
        explicit_rating=rating
    )
    
    print(f"✅ Sentiment recorded!")
    print(f"   Text: {text}")
    print(f"   Score: {result['sentiment_score']}")
    print(f"   Label: {result['sentiment_label']}")
    if rating:
        print(f"   Rating: {rating}/5")
    
    # Show comparison if baseline exists
    try:
        comparison = monitor.compare_to_baseline()
        if 'error' not in comparison:
            print(f"\n📊 Current vs Baseline:")
            print(f"   Sentiment: {comparison['current']['avg_sentiment']:.2f} (baseline: {comparison['baseline'].get('avg_sentiment', 0):.2f})")
            print(f"   Change: {comparison['changes']['sentiment_change']:+.2f}")
    except:
        pass

if __name__ == '__main__':
    main()
