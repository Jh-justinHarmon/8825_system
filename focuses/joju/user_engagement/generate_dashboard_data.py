#!/usr/bin/env python3
"""
Generate dashboard data from user engagement files
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import Counter
from docx import Document

class DashboardDataGenerator:
    """Generate data for user engagement dashboard"""
    
    def __init__(self, engagement_dir: str = None):
        if engagement_dir is None:
            engagement_dir = Path(__file__).parent
        
        self.engagement_dir = Path(engagement_dir)
        self.sessions_dir = self.engagement_dir / 'sessions'
        self.insights_dir = self.engagement_dir / 'insights'
        self.competitive_dir = self.engagement_dir / 'competitive_intelligence'
    
    def generate_dashboard_data(self) -> dict:
        """Generate all dashboard data"""
        print("Generating dashboard data...")
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'stats': self._generate_stats(),
            'feedback_items': self._generate_feedback_items(),
            'insights': self._generate_insights(),
            'competitive_intel': self._generate_competitive_intel(),
            'themes': self._generate_themes()
        }
        
        # Save to JSON
        output_file = self.engagement_dir / 'dashboard_data.json'
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Dashboard data saved to: {output_file}")
        
        return data
    
    def _generate_stats(self) -> dict:
        """Generate high-level statistics"""
        stats = {
            'total_sessions': 0,
            'pain_points': 0,
            'positive_feedback': 0,
            'ai_features': 0,
            'platforms_mentioned': 0
        }
        
        # Count sessions
        if self.sessions_dir.exists():
            stats['total_sessions'] = len(list(self.sessions_dir.glob('*.docx'))) + \
                                     len(list(self.sessions_dir.glob('*.json')))
        
        # Count insights
        if self.insights_dir.exists():
            for insight_file in self.insights_dir.glob('*_processed.json'):
                try:
                    with open(insight_file) as f:
                        insight = json.load(f)
                        stats['pain_points'] += len(insight.get('pain_points', []))
                        stats['positive_feedback'] += len(insight.get('positive_feedback', []))
                except:
                    pass
        
        # Count competitive intel
        if self.competitive_dir.exists():
            ai_features_dir = self.competitive_dir / 'ai_features'
            if ai_features_dir.exists():
                stats['platforms_mentioned'] = len(list(ai_features_dir.glob('*.md')))
                # Count AI features from Teal analysis
                stats['ai_features'] = 5  # From Teal analysis
        
        return stats
    
    def _generate_feedback_items(self) -> list:
        """Generate feedback items with quotes"""
        items = []
        
        # Add Kayson/Teal feedback
        items.extend([
            {
                'participant': 'Kayson L Conlin',
                'date': '2025-08-28',
                'quote': 'Teal uses AI to generate bullet points and cover letters, which is more accurate than general chatbots like Claude or ChatGPT because it\'s based on my specific resume information.',
                'tags': ['AI Feature', 'Positive', 'Context-Aware AI'],
                'category': 'competitive ai positive'
            },
            {
                'participant': 'Kayson L Conlin',
                'date': '2025-08-28',
                'quote': 'Teal aims for a 65-75% correlation between the job requirements and the resume to appear authentic yet optimized.',
                'tags': ['AI Feature', 'Smart Optimization', 'Authenticity'],
                'category': 'competitive ai'
            },
            {
                'participant': 'Kayson L Conlin',
                'date': '2025-08-28',
                'quote': 'Teal boosted my confidence and generated more attention from employers. It\'s easy to use and parses existing resumes well.',
                'tags': ['Positive', 'User Impact'],
                'category': 'positive'
            },
            {
                'participant': 'Kayson L Conlin',
                'date': '2025-08-28',
                'quote': 'Missing feature: ability to pull information from a wider range of websites for job applications.',
                'tags': ['Pain Point', 'Feature Request'],
                'category': 'pain-points'
            }
        ])
        
        return items
    
    def _generate_insights(self) -> list:
        """Generate key insights"""
        return [
            {
                'title': 'Context-Aware AI Wins',
                'description': 'Users prefer AI that uses their specific data over generic responses'
            },
            {
                'title': 'Balance is Key',
                'description': '65-75% optimization maintains authenticity while improving results'
            },
            {
                'title': 'Automate Tedious, Not Creative',
                'description': 'Users want AI to handle repetitive tasks, not replace creativity'
            }
        ]
    
    def _generate_competitive_intel(self) -> list:
        """Generate competitive intelligence data"""
        return [
            {
                'platform': 'Teal',
                'description': 'AI-powered resume and job application platform',
                'ai_features': [
                    'Context-Aware AI',
                    'Smart Resume Tailoring',
                    'Auto-Population',
                    'AI Cover Letters',
                    'Job Intelligence'
                ]
            }
        ]
    
    def _generate_themes(self) -> list:
        """Generate recurring themes"""
        return [
            {
                'title': 'Multi-Platform Presence',
                'description': 'Users expect web, desktop, and browser extensions'
            },
            {
                'title': 'Integrated Workflows',
                'description': 'Features should connect across user\'s journey'
            }
        ]
    
    def update_dashboard_html(self, data: dict):
        """Update dashboard HTML with real data"""
        dashboard_file = self.engagement_dir / 'dashboard.html'
        
        if not dashboard_file.exists():
            print("Dashboard HTML not found")
            return
        
        # Read HTML
        with open(dashboard_file, 'r') as f:
            html = f.read()
        
        # Update stats
        html = html.replace('id="totalSessions">5', f'id="totalSessions">{data["stats"]["total_sessions"]}')
        html = html.replace('id="painPoints">18', f'id="painPoints">{data["stats"]["pain_points"]}')
        html = html.replace('id="positiveFeedback">45', f'id="positiveFeedback">{data["stats"]["positive_feedback"]}')
        html = html.replace('id="aiFeatures">5', f'id="aiFeatures">{data["stats"]["ai_features"]}')
        
        # Save updated HTML
        with open(dashboard_file, 'w') as f:
            f.write(html)
        
        print(f"✅ Dashboard HTML updated")


def main():
    """Main entry point"""
    print(f"\n{'='*80}")
    print("Generating User Engagement Dashboard Data")
    print(f"{'='*80}\n")
    
    generator = DashboardDataGenerator()
    data = generator.generate_dashboard_data()
    generator.update_dashboard_html(data)
    
    print(f"\n{'='*80}")
    print("Dashboard Ready!")
    print(f"{'='*80}\n")
    print(f"Open: focuses/joju/user_engagement/dashboard.html")
    print()


if __name__ == "__main__":
    main()
