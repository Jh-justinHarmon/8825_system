#!/usr/bin/env python3
"""
Joju User Feedback Processor
Processes user testing sessions into structured insights
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from docx import Document

class FeedbackProcessor:
    """Process user feedback into structured format"""
    
    def __init__(self, feedback_dir: str = None):
        if feedback_dir is None:
            feedback_dir = Path(__file__).parent
        
        self.feedback_dir = Path(feedback_dir)
        self.sessions_dir = self.feedback_dir / 'sessions'
        self.insights_dir = self.feedback_dir / 'insights'
        self.themes_dir = self.feedback_dir / 'themes'
        self.actions_dir = self.feedback_dir / 'action_items'
        
        # Ensure directories exist
        for dir_path in [self.sessions_dir, self.insights_dir, self.themes_dir, self.actions_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def process_session(self, session_file: Path) -> Dict[str, Any]:
        """
        Process a single user testing session
        
        Args:
            session_file: Path to session document
            
        Returns:
            Structured session data
        """
        print(f"Processing: {session_file.name}")
        
        # Extract text from document
        if session_file.suffix == '.docx':
            text = self._extract_from_docx(session_file)
        elif session_file.suffix == '.json':
            with open(session_file) as f:
                return json.load(f)
        else:
            with open(session_file) as f:
                text = f.read()
        
        # Parse session data
        session_data = {
            'session_id': session_file.stem,
            'date': self._extract_date(session_file.name),
            'participant': self._extract_participant(session_file.name),
            'source_file': str(session_file),
            'processed_at': datetime.now().isoformat(),
            'raw_text': text,
            'insights': self._extract_insights(text),
            'pain_points': self._extract_pain_points(text),
            'positive_feedback': self._extract_positive(text),
            'suggestions': self._extract_suggestions(text),
            'quotes': self._extract_quotes(text)
        }
        
        # Save structured session
        output_file = self.sessions_dir / f"{session_data['session_id']}_processed.json"
        with open(output_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"  ✓ Extracted {len(session_data['insights'])} insights")
        print(f"  ✓ Found {len(session_data['pain_points'])} pain points")
        print(f"  ✓ Found {len(session_data['positive_feedback'])} positive items")
        
        return session_data
    
    def _extract_from_docx(self, filepath: Path) -> str:
        """Extract text from Word document"""
        doc = Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
    
    def _extract_date(self, filename: str) -> str:
        """Extract date from filename"""
        if filename.startswith('2025'):
            return filename[:10].replace('_', '-')
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_participant(self, filename: str) -> str:
        """Extract participant name from filename"""
        parts = filename.split('_')
        if len(parts) > 1:
            return parts[1] if not parts[1].startswith('2025') else 'Unknown'
        return 'Unknown'
    
    def _extract_insights(self, text: str) -> List[Dict[str, Any]]:
        """Extract insights from text"""
        insights = []
        lines = text.lower().split('\n')
        
        for i, line in enumerate(lines):
            if any(word in line for word in ['insight', 'learned', 'discovered', 'found that']):
                insights.append({
                    'text': line.strip(),
                    'line_number': i + 1,
                    'category': 'general'
                })
        
        return insights[:10]  # Limit to top 10
    
    def _extract_pain_points(self, text: str) -> List[str]:
        """Extract pain points from text"""
        pain_points = []
        lines = text.lower().split('\n')
        
        keywords = ['difficult', 'confusing', 'problem', 'issue', 'frustrated', 
                   'hard to', 'couldn\'t', 'failed', 'error', 'stuck']
        
        for line in lines:
            if any(word in line for word in keywords):
                pain_points.append(line.strip())
        
        return pain_points[:10]
    
    def _extract_positive(self, text: str) -> List[str]:
        """Extract positive feedback from text"""
        positive = []
        lines = text.lower().split('\n')
        
        keywords = ['easy', 'like', 'love', 'helpful', 'good', 'great', 
                   'intuitive', 'clear', 'simple', 'works well']
        
        for line in lines:
            if any(word in line for word in keywords):
                positive.append(line.strip())
        
        return positive[:10]
    
    def _extract_suggestions(self, text: str) -> List[str]:
        """Extract suggestions from text"""
        suggestions = []
        lines = text.lower().split('\n')
        
        keywords = ['suggest', 'recommend', 'would be better', 'should', 
                   'could', 'wish', 'if only', 'feature request']
        
        for line in lines:
            if any(word in line for word in keywords):
                suggestions.append(line.strip())
        
        return suggestions[:10]
    
    def _extract_quotes(self, text: str) -> List[str]:
        """Extract direct quotes from text"""
        quotes = []
        lines = text.split('\n')
        
        for line in lines:
            # Look for quoted text
            if '"' in line or "'" in line:
                quotes.append(line.strip())
        
        return quotes[:5]
    
    def generate_insights_report(self, sessions: List[Dict[str, Any]]) -> Path:
        """
        Generate insights report from multiple sessions
        
        Args:
            sessions: List of processed session data
            
        Returns:
            Path to insights report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'sessions_analyzed': len(sessions),
            'total_insights': sum(len(s['insights']) for s in sessions),
            'total_pain_points': sum(len(s['pain_points']) for s in sessions),
            'total_positive': sum(len(s['positive_feedback']) for s in sessions),
            'total_suggestions': sum(len(s['suggestions']) for s in sessions),
            'by_session': []
        }
        
        for session in sessions:
            report['by_session'].append({
                'session_id': session['session_id'],
                'participant': session['participant'],
                'date': session['date'],
                'insights_count': len(session['insights']),
                'pain_points_count': len(session['pain_points']),
                'positive_count': len(session['positive_feedback']),
                'suggestions_count': len(session['suggestions'])
            })
        
        # Save report
        report_file = self.insights_dir / f"insights_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def process_all_sessions(self) -> List[Dict[str, Any]]:
        """Process all sessions in sessions directory"""
        print(f"\n{'='*80}")
        print("Processing All User Testing Sessions")
        print(f"{'='*80}\n")
        
        # Find all session files
        session_files = []
        for ext in ['*.docx', '*.json', '*.md']:
            session_files.extend(self.sessions_dir.glob(ext))
        
        # Filter out already processed files
        session_files = [f for f in session_files if '_processed' not in f.name]
        
        if not session_files:
            print("No unprocessed sessions found")
            return []
        
        print(f"Found {len(session_files)} session(s) to process\n")
        
        processed_sessions = []
        for session_file in session_files:
            try:
                session_data = self.process_session(session_file)
                processed_sessions.append(session_data)
                print()
            except Exception as e:
                print(f"  ✗ Error: {e}\n")
        
        # Generate insights report
        if processed_sessions:
            report_file = self.generate_insights_report(processed_sessions)
            print(f"{'─'*80}")
            print(f"✓ Insights report generated: {report_file.name}")
        
        print(f"\n{'='*80}")
        print(f"Processed {len(processed_sessions)} session(s)")
        print(f"{'='*80}\n")
        
        return processed_sessions


def main():
    """Main entry point"""
    processor = FeedbackProcessor()
    processor.process_all_sessions()


if __name__ == "__main__":
    main()
