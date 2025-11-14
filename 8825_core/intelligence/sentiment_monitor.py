#!/usr/bin/env python3
"""
Sentiment Monitor
Tracks user sentiment about system performance before and after LLOM Router activation
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

class SentimentMonitor:
    """
    Monitors user sentiment through:
    1. Explicit feedback (comments, notes)
    2. Implicit signals (error rates, retry patterns)
    3. Performance metrics (latency, success rate)
    """
    
    def __init__(self):
        self.sentiment_log = Path(__file__).parent / 'sentiment_log.jsonl'
        self.baseline_file = Path(__file__).parent / 'sentiment_baseline.json'
        
        # Sentiment keywords
        self.positive_keywords = [
            'fast', 'quick', 'good', 'great', 'excellent', 'perfect', 'love',
            'better', 'improved', 'smooth', 'efficient', 'works', 'nice'
        ]
        
        self.negative_keywords = [
            'slow', 'bad', 'terrible', 'broken', 'error', 'fail', 'wrong',
            'worse', 'issue', 'problem', 'stuck', 'frustrat', 'annoying'
        ]
        
        self.quality_keywords = [
            'accurate', 'correct', 'right', 'precise', 'quality', 'smart',
            'inaccurate', 'incorrect', 'wrong', 'mistake', 'dumb', 'stupid'
        ]
    
    def record_sentiment(self, 
                        source: str, 
                        text: str, 
                        explicit_rating: int = None,
                        metadata: Dict = None):
        """
        Record a sentiment data point
        
        Args:
            source: Where sentiment came from (chat, comment, feedback)
            text: The actual text
            explicit_rating: Optional 1-5 rating
            metadata: Additional context
        """
        
        # Analyze sentiment
        analysis = self._analyze_text(text)
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'text': text,
            'explicit_rating': explicit_rating,
            'sentiment_score': analysis['score'],
            'sentiment_label': analysis['label'],
            'keywords_found': analysis['keywords'],
            'metadata': metadata or {}
        }
        
        # Append to log
        with open(self.sentiment_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        return entry
    
    def _analyze_text(self, text: str) -> Dict:
        """Analyze text for sentiment"""
        
        text_lower = text.lower()
        
        # Count keyword matches
        positive_count = sum(1 for kw in self.positive_keywords if kw in text_lower)
        negative_count = sum(1 for kw in self.negative_keywords if kw in text_lower)
        
        # Calculate score (-1 to 1)
        total = positive_count + negative_count
        if total == 0:
            score = 0
            label = 'neutral'
        else:
            score = (positive_count - negative_count) / total
            if score > 0.3:
                label = 'positive'
            elif score < -0.3:
                label = 'negative'
            else:
                label = 'neutral'
        
        # Find which keywords matched
        keywords_found = {
            'positive': [kw for kw in self.positive_keywords if kw in text_lower],
            'negative': [kw for kw in self.negative_keywords if kw in text_lower]
        }
        
        return {
            'score': round(score, 2),
            'label': label,
            'keywords': keywords_found
        }
    
    def create_baseline(self):
        """Create baseline sentiment before LLOM Router activation"""
        
        print("📊 Creating sentiment baseline...\n")
        
        # Scan recent chat history for sentiment
        baseline_data = {
            'created_at': datetime.now().isoformat(),
            'phase': 'pre_llom_router',
            'sentiment_samples': [],
            'performance_baseline': {
                'avg_response_time': 'unknown',  # Will be measured
                'error_rate': 'unknown',
                'user_satisfaction': 'unknown'
            }
        }
        
        # Look for recent feedback in system
        feedback_sources = [
            self._scan_commit_messages(),
            self._scan_recent_notes(),
        ]
        
        for source_data in feedback_sources:
            baseline_data['sentiment_samples'].extend(source_data)
        
        # Calculate baseline metrics
        if baseline_data['sentiment_samples']:
            scores = [s['sentiment_score'] for s in baseline_data['sentiment_samples']]
            baseline_data['baseline_metrics'] = {
                'avg_sentiment': round(sum(scores) / len(scores), 2),
                'positive_count': sum(1 for s in baseline_data['sentiment_samples'] if s['sentiment_label'] == 'positive'),
                'negative_count': sum(1 for s in baseline_data['sentiment_samples'] if s['sentiment_label'] == 'negative'),
                'neutral_count': sum(1 for s in baseline_data['sentiment_samples'] if s['sentiment_label'] == 'neutral'),
                'total_samples': len(baseline_data['sentiment_samples'])
            }
        
        # Save baseline
        self.baseline_file.write_text(json.dumps(baseline_data, indent=2))
        
        print(f"✅ Baseline created with {len(baseline_data['sentiment_samples'])} samples")
        print(f"   Avg sentiment: {baseline_data.get('baseline_metrics', {}).get('avg_sentiment', 'N/A')}")
        print(f"   Positive: {baseline_data.get('baseline_metrics', {}).get('positive_count', 0)}")
        print(f"   Negative: {baseline_data.get('baseline_metrics', {}).get('negative_count', 0)}")
        print(f"   Neutral: {baseline_data.get('baseline_metrics', {}).get('neutral_count', 0)}")
        
        return baseline_data
    
    def _scan_commit_messages(self) -> List[Dict]:
        """Scan recent git commit messages for sentiment"""
        
        samples = []
        
        try:
            import subprocess
            
            # Get last 20 commit messages
            result = subprocess.run(
                ['git', 'log', '--format=%s', '-20'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent.parent
            )
            
            if result.returncode == 0:
                messages = result.stdout.strip().split('\n')
                
                for msg in messages:
                    if msg:
                        analysis = self._analyze_text(msg)
                        samples.append({
                            'source': 'git_commit',
                            'text': msg,
                            'sentiment_score': analysis['score'],
                            'sentiment_label': analysis['label'],
                            'timestamp': datetime.now().isoformat()
                        })
        except Exception as e:
            print(f"  ⚠️  Could not scan git commits: {e}")
        
        return samples
    
    def _scan_recent_notes(self) -> List[Dict]:
        """Scan recent notes/docs for sentiment"""
        
        samples = []
        
        # Look for recent markdown files with feedback
        system_root = Path(__file__).parent.parent.parent
        recent_files = [
            system_root / 'INBOX_HUB' / 'SYSTEM_STATUS.md',
            system_root / '8825_core' / 'intelligence' / 'IMPLEMENTATION_COMPLETE.md',
        ]
        
        for file_path in recent_files:
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    
                    # Extract sections with potential sentiment
                    lines = content.split('\n')
                    for line in lines:
                        if any(kw in line.lower() for kw in self.positive_keywords + self.negative_keywords):
                            analysis = self._analyze_text(line)
                            samples.append({
                                'source': f'doc:{file_path.name}',
                                'text': line.strip(),
                                'sentiment_score': analysis['score'],
                                'sentiment_label': analysis['label'],
                                'timestamp': datetime.now().isoformat()
                            })
                except Exception as e:
                    print(f"  ⚠️  Could not scan {file_path.name}: {e}")
        
        return samples
    
    def compare_to_baseline(self) -> Dict:
        """Compare current sentiment to baseline"""
        
        if not self.baseline_file.exists():
            return {'error': 'No baseline found. Run create_baseline() first.'}
        
        baseline = json.loads(self.baseline_file.read_text())
        
        # Read current sentiment log
        if not self.sentiment_log.exists():
            return {'error': 'No sentiment data collected yet.'}
        
        current_samples = []
        with open(self.sentiment_log, 'r') as f:
            for line in f:
                if line.strip():
                    current_samples.append(json.loads(line))
        
        # Calculate current metrics
        if not current_samples:
            return {'error': 'No current sentiment data.'}
        
        scores = [s['sentiment_score'] for s in current_samples]
        current_metrics = {
            'avg_sentiment': round(sum(scores) / len(scores), 2),
            'positive_count': sum(1 for s in current_samples if s['sentiment_label'] == 'positive'),
            'negative_count': sum(1 for s in current_samples if s['sentiment_label'] == 'negative'),
            'neutral_count': sum(1 for s in current_samples if s['sentiment_label'] == 'neutral'),
            'total_samples': len(current_samples)
        }
        
        # Compare
        baseline_metrics = baseline.get('baseline_metrics', {})
        
        comparison = {
            'baseline': baseline_metrics,
            'current': current_metrics,
            'changes': {
                'sentiment_change': current_metrics['avg_sentiment'] - baseline_metrics.get('avg_sentiment', 0),
                'positive_change': current_metrics['positive_count'] - baseline_metrics.get('positive_count', 0),
                'negative_change': current_metrics['negative_count'] - baseline_metrics.get('negative_count', 0)
            },
            'interpretation': self._interpret_changes(baseline_metrics, current_metrics)
        }
        
        return comparison
    
    def _interpret_changes(self, baseline: Dict, current: Dict) -> str:
        """Interpret sentiment changes"""
        
        sentiment_change = current['avg_sentiment'] - baseline.get('avg_sentiment', 0)
        
        if sentiment_change > 0.2:
            return "✅ SIGNIFICANT IMPROVEMENT - User sentiment has notably improved"
        elif sentiment_change > 0.05:
            return "📈 SLIGHT IMPROVEMENT - User sentiment trending positive"
        elif sentiment_change < -0.2:
            return "❌ SIGNIFICANT DECLINE - User sentiment has worsened"
        elif sentiment_change < -0.05:
            return "📉 SLIGHT DECLINE - User sentiment trending negative"
        else:
            return "➡️  NO SIGNIFICANT CHANGE - User sentiment stable"
    
    def print_comparison_report(self):
        """Print sentiment comparison report"""
        
        comparison = self.compare_to_baseline()
        
        if 'error' in comparison:
            print(f"⚠️  {comparison['error']}")
            return
        
        print("\n" + "="*70)
        print("😊 SENTIMENT COMPARISON REPORT")
        print("="*70 + "\n")
        
        print("📊 BASELINE (Pre-LLOM Router):")
        baseline = comparison['baseline']
        print(f"  Avg Sentiment: {baseline.get('avg_sentiment', 'N/A')}")
        print(f"  Positive: {baseline.get('positive_count', 0)}")
        print(f"  Negative: {baseline.get('negative_count', 0)}")
        print(f"  Neutral: {baseline.get('neutral_count', 0)}")
        print(f"  Total Samples: {baseline.get('total_samples', 0)}")
        
        print("\n📊 CURRENT (Post-LLOM Router):")
        current = comparison['current']
        print(f"  Avg Sentiment: {current['avg_sentiment']}")
        print(f"  Positive: {current['positive_count']}")
        print(f"  Negative: {current['negative_count']}")
        print(f"  Neutral: {current['neutral_count']}")
        print(f"  Total Samples: {current['total_samples']}")
        
        print("\n📈 CHANGES:")
        changes = comparison['changes']
        print(f"  Sentiment Change: {changes['sentiment_change']:+.2f}")
        print(f"  Positive Change: {changes['positive_change']:+d}")
        print(f"  Negative Change: {changes['negative_change']:+d}")
        
        print(f"\n{comparison['interpretation']}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Run sentiment monitoring"""
    
    monitor = SentimentMonitor()
    
    print("Creating baseline sentiment metrics...\n")
    monitor.create_baseline()
    
    print("\n" + "-"*70 + "\n")
    print("📝 Sentiment monitoring is now active!")
    print("\nTo record sentiment:")
    print("  monitor.record_sentiment('chat', 'This is working great!', explicit_rating=5)")
    print("\nTo compare to baseline:")
    print("  monitor.compare_to_baseline()")
    print("\nTo print report:")
    print("  monitor.print_comparison_report()")
    

if __name__ == '__main__':
    main()
