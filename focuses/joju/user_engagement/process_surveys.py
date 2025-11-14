#!/usr/bin/env python3
"""
Process survey data from Notion and other sources
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from collections import Counter

class SurveyProcessor:
    """Process survey responses into structured insights"""
    
    def __init__(self, engagement_dir: str = None):
        if engagement_dir is None:
            engagement_dir = Path(__file__).parent
        
        self.engagement_dir = Path(engagement_dir)
        self.surveys_dir = self.engagement_dir / 'surveys'
        self.insights_dir = self.engagement_dir / 'insights'
        
        # Ensure directories exist
        for dir_path in [self.surveys_dir, self.insights_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def process_notion_screener(self, survey_file: Path) -> Dict[str, Any]:
        """
        Process Notion screener survey responses
        
        Args:
            survey_file: Path to survey data file
            
        Returns:
            Processed survey insights
        """
        print(f"Processing Notion screener: {survey_file.name}")
        
        # Load survey data
        if survey_file.suffix == '.json':
            with open(survey_file) as f:
                data = json.load(f)
        elif survey_file.suffix == '.csv':
            data = self._load_csv(survey_file)
        else:
            raise ValueError(f"Unsupported file format: {survey_file.suffix}")
        
        # Extract insights
        insights = {
            'survey_id': data.get('survey_id', survey_file.stem),
            'survey_type': 'notion_screener',
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'total_responses': len(data.get('responses', [])),
            'completion_rate': data.get('metadata', {}).get('completion_rate', 0),
            'key_insights': self._extract_screener_insights(data),
            'demographics': self._analyze_demographics(data),
            'interest_levels': self._analyze_interest(data),
            'use_cases': self._extract_use_cases(data),
            'pain_points': self._extract_pain_points_from_survey(data)
        }
        
        # Save insights
        output_file = self.insights_dir / f"{insights['survey_id']}_insights.json"
        with open(output_file, 'w') as f:
            json.dump(insights, f, indent=2)
        
        print(f"  ✓ Processed {insights['total_responses']} responses")
        print(f"  ✓ Extracted {len(insights['key_insights'])} key insights")
        print(f"  ✓ Identified {len(insights['use_cases'])} use cases")
        
        return insights
    
    def _load_csv(self, filepath: Path) -> Dict[str, Any]:
        """Load CSV file into structured format"""
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            responses = list(reader)
        
        return {
            'survey_id': filepath.stem,
            'responses': responses,
            'metadata': {
                'total_responses': len(responses)
            }
        }
    
    def _extract_screener_insights(self, data: Dict[str, Any]) -> List[str]:
        """Extract key insights from screener responses"""
        insights = []
        responses = data.get('responses', [])
        
        if not responses:
            return insights
        
        # Analyze response patterns
        # This is a simplified version - expand based on actual survey structure
        
        # Example: Interest level distribution
        interest_levels = [r.get('answers', {}).get('interest_level') for r in responses]
        interest_counter = Counter(interest_levels)
        
        if interest_counter:
            most_common = interest_counter.most_common(1)[0]
            insights.append(f"Most common interest level: {most_common[0]} ({most_common[1]} responses)")
        
        return insights
    
    def _analyze_demographics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze demographic data from responses"""
        responses = data.get('responses', [])
        
        demographics = {
            'total': len(responses),
            'roles': Counter(),
            'experience_levels': Counter(),
            'company_sizes': Counter()
        }
        
        for response in responses:
            answers = response.get('answers', {})
            
            if 'role' in answers:
                demographics['roles'][answers['role']] += 1
            if 'experience_level' in answers:
                demographics['experience_levels'][answers['experience_level']] += 1
            if 'company_size' in answers:
                demographics['company_sizes'][answers['company_size']] += 1
        
        # Convert Counters to dicts for JSON serialization
        demographics['roles'] = dict(demographics['roles'])
        demographics['experience_levels'] = dict(demographics['experience_levels'])
        demographics['company_sizes'] = dict(demographics['company_sizes'])
        
        return demographics
    
    def _analyze_interest(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze interest levels"""
        responses = data.get('responses', [])
        
        interest_data = {
            'high': 0,
            'medium': 0,
            'low': 0,
            'distribution': {}
        }
        
        for response in responses:
            interest = response.get('answers', {}).get('interest_level', '').lower()
            
            if 'high' in interest or 'very interested' in interest:
                interest_data['high'] += 1
            elif 'medium' in interest or 'somewhat' in interest:
                interest_data['medium'] += 1
            elif 'low' in interest or 'not' in interest:
                interest_data['low'] += 1
        
        total = interest_data['high'] + interest_data['medium'] + interest_data['low']
        if total > 0:
            interest_data['distribution'] = {
                'high': round(interest_data['high'] / total * 100, 1),
                'medium': round(interest_data['medium'] / total * 100, 1),
                'low': round(interest_data['low'] / total * 100, 1)
            }
        
        return interest_data
    
    def _extract_use_cases(self, data: Dict[str, Any]) -> List[str]:
        """Extract use cases from responses"""
        responses = data.get('responses', [])
        use_cases = []
        
        for response in responses:
            answers = response.get('answers', {})
            
            # Look for use case related questions
            for key, value in answers.items():
                if 'use case' in key.lower() or 'how would you use' in key.lower():
                    if value and value not in use_cases:
                        use_cases.append(value)
        
        return use_cases[:20]  # Limit to top 20
    
    def _extract_pain_points_from_survey(self, data: Dict[str, Any]) -> List[str]:
        """Extract pain points from survey responses"""
        responses = data.get('responses', [])
        pain_points = []
        
        for response in responses:
            answers = response.get('answers', {})
            
            # Look for pain point related questions
            for key, value in answers.items():
                if any(word in key.lower() for word in ['pain', 'problem', 'challenge', 'difficult', 'frustrat']):
                    if value and value not in pain_points:
                        pain_points.append(value)
        
        return pain_points[:20]  # Limit to top 20
    
    def generate_survey_report(self, insights_list: List[Dict[str, Any]]) -> Path:
        """Generate comprehensive survey report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'surveys_analyzed': len(insights_list),
            'total_responses': sum(i['total_responses'] for i in insights_list),
            'surveys': []
        }
        
        for insights in insights_list:
            report['surveys'].append({
                'survey_id': insights['survey_id'],
                'type': insights['survey_type'],
                'date': insights['date'],
                'responses': insights['total_responses'],
                'completion_rate': insights['completion_rate'],
                'key_insights_count': len(insights['key_insights'])
            })
        
        # Save report
        report_file = self.insights_dir / f"survey_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def process_all_surveys(self) -> List[Dict[str, Any]]:
        """Process all surveys in surveys directory"""
        print(f"\n{'='*80}")
        print("Processing All Survey Data")
        print(f"{'='*80}\n")
        
        # Find all survey files
        survey_files = []
        for ext in ['*.json', '*.csv']:
            survey_files.extend(self.surveys_dir.glob(ext))
        
        # Filter out README and processed files
        survey_files = [f for f in survey_files if 'README' not in f.name and '_insights' not in f.name]
        
        if not survey_files:
            print("No survey files found")
            print(f"\nPlace survey data in: {self.surveys_dir}")
            return []
        
        print(f"Found {len(survey_files)} survey file(s) to process\n")
        
        processed_surveys = []
        for survey_file in survey_files:
            try:
                insights = self.process_notion_screener(survey_file)
                processed_surveys.append(insights)
                print()
            except Exception as e:
                print(f"  ✗ Error: {e}\n")
        
        # Generate report
        if processed_surveys:
            report_file = self.generate_survey_report(processed_surveys)
            print(f"{'─'*80}")
            print(f"✓ Survey report generated: {report_file.name}")
        
        print(f"\n{'='*80}")
        print(f"Processed {len(processed_surveys)} survey(s)")
        print(f"{'='*80}\n")
        
        return processed_surveys


def main():
    """Main entry point"""
    processor = SurveyProcessor()
    processor.process_all_surveys()


if __name__ == "__main__":
    main()
