#!/usr/bin/env python3
"""
Session Manager
Manages working sessions and silent learning
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class SessionManager:
    """Manages communication sessions and learning data"""
    
    def __init__(self, data_dir: str = None):
        """Initialize session manager"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_file = self.data_dir / "current_session.json"
        self.learning_file = self.data_dir / "learning_data.json"
        
        self.current_session = self._load_or_create_session()
        self.learning_data = self._load_learning_data()
    
    def _load_or_create_session(self) -> Dict:
        """Load current session or create new one"""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                return json.load(f)
        
        return {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "started": datetime.now().isoformat(),
            "interactions": [],
            "silent_notes": []
        }
    
    def _load_learning_data(self) -> Dict:
        """Load learning data"""
        if self.learning_file.exists():
            with open(self.learning_file, 'r') as f:
                return json.load(f)
        
        return {
            "patterns": {},
            "preferences": {},
            "contact_insights": {},
            "response_effectiveness": {},
            "last_updated": None
        }
    
    def log_interaction(self, context: Dict, responses: List[Dict], selected: int = None):
        """
        Log an interaction (silent - no display)
        
        Args:
            context: Context from analyzer
            responses: Generated responses
            selected: Index of selected response (0-2) or None
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "context": {
                "message_type": context.get('message_type'),
                "sentiment": context.get('sentiment'),
                "urgency": context.get('urgency'),
                "contact": context.get('contact_context', {}).get('name')
            },
            "responses_generated": [
                {
                    "level": r['level'],
                    "word_count": r['word_count']
                } for r in responses
            ],
            "selected_response": selected,
            "selected_level": responses[selected]['level'] if selected is not None else None
        }
        
        self.current_session['interactions'].append(interaction)
        self._save_session()
    
    def add_silent_note(self, note_type: str, data: Dict):
        """
        Add a silent note for learning (not displayed to user)
        
        Args:
            note_type: Type of note (recommendation, pattern, insight)
            data: Note data
        """
        note = {
            "timestamp": datetime.now().isoformat(),
            "type": note_type,
            "data": data
        }
        
        self.current_session['silent_notes'].append(note)
        self._save_session()
    
    def _save_session(self):
        """Save current session"""
        with open(self.session_file, 'w') as f:
            json.dump(self.current_session, f, indent=2)
    
    def end_session(self):
        """
        End session and process learning
        
        Returns:
            Learning summary
        """
        # Process all interactions and silent notes
        learning_summary = self._process_learning()
        
        # Update learning data
        self._update_learning_data(learning_summary)
        
        # Archive session
        self._archive_session()
        
        # Create new session
        self.current_session = self._load_or_create_session()
        
        return learning_summary
    
    def _process_learning(self) -> Dict:
        """Process session data for learning"""
        summary = {
            "session_id": self.current_session['session_id'],
            "total_interactions": len(self.current_session['interactions']),
            "response_preferences": {},
            "context_patterns": {},
            "recommendations": []
        }
        
        # Analyze response preferences
        for interaction in self.current_session['interactions']:
            if interaction['selected_level']:
                level = interaction['selected_level']
                context_type = interaction['context']['message_type']
                
                # Track which response level is preferred for each context
                key = f"{context_type}_{interaction['context']['sentiment']}"
                if key not in summary['response_preferences']:
                    summary['response_preferences'][key] = {}
                
                if level not in summary['response_preferences'][key]:
                    summary['response_preferences'][key][level] = 0
                
                summary['response_preferences'][key][level] += 1
        
        # Extract patterns from silent notes
        for note in self.current_session['silent_notes']:
            if note['type'] == 'recommendation':
                summary['recommendations'].append(note['data'])
            elif note['type'] == 'pattern':
                context = note['data'].get('context', 'general')
                if context not in summary['context_patterns']:
                    summary['context_patterns'][context] = []
                summary['context_patterns'][context].append(note['data'])
        
        return summary
    
    def _update_learning_data(self, summary: Dict):
        """Update persistent learning data"""
        # Merge response preferences
        for context, prefs in summary['response_preferences'].items():
            if context not in self.learning_data['preferences']:
                self.learning_data['preferences'][context] = {}
            
            for level, count in prefs.items():
                if level not in self.learning_data['preferences'][context]:
                    self.learning_data['preferences'][context][level] = 0
                self.learning_data['preferences'][context][level] += count
        
        # Update patterns
        for context, patterns in summary['context_patterns'].items():
            if context not in self.learning_data['patterns']:
                self.learning_data['patterns'][context] = []
            self.learning_data['patterns'][context].extend(patterns)
        
        # Update timestamp
        self.learning_data['last_updated'] = datetime.now().isoformat()
        
        # Save learning data
        with open(self.learning_file, 'w') as f:
            json.dump(self.learning_data, f, indent=2)
    
    def _archive_session(self):
        """Archive completed session"""
        archive_dir = self.data_dir / "sessions"
        archive_dir.mkdir(exist_ok=True)
        
        archive_file = archive_dir / f"session_{self.current_session['session_id']}.json"
        
        # Add end time
        self.current_session['ended'] = datetime.now().isoformat()
        
        with open(archive_file, 'w') as f:
            json.dump(self.current_session, f, indent=2)
    
    def get_recommendation(self, context: Dict) -> str:
        """
        Get silent recommendation based on learning (not displayed)
        
        Args:
            context: Current context
        
        Returns:
            Recommended response level
        """
        message_type = context.get('message_type', 'statement')
        sentiment = context.get('sentiment', 'neutral')
        
        key = f"{message_type}_{sentiment}"
        
        # Check learned preferences
        if key in self.learning_data.get('preferences', {}):
            prefs = self.learning_data['preferences'][key]
            # Return most frequently selected level
            return max(prefs, key=prefs.get)
        
        # Default recommendations (not displayed, just tracked)
        defaults = {
            'question_urgent': 'standard',
            'request_urgent': 'standard',
            'acknowledgment_positive': 'brief',
            'greeting_neutral': 'brief'
        }
        
        return defaults.get(key, 'standard')
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        return {
            "session_id": self.current_session['session_id'],
            "started": self.current_session['started'],
            "interactions": len(self.current_session['interactions']),
            "silent_notes": len(self.current_session['silent_notes'])
        }

if __name__ == "__main__":
    # Test
    manager = SessionManager()
    
    # Simulate interaction
    test_context = {
        'message_type': 'question',
        'sentiment': 'neutral',
        'urgency': 'medium'
    }
    
    test_responses = [
        {'level': 'brief', 'word_count': 5},
        {'level': 'standard', 'word_count': 15},
        {'level': 'detailed', 'word_count': 30}
    ]
    
    manager.log_interaction(test_context, test_responses, selected=1)
    
    # Add silent note
    manager.add_silent_note('recommendation', {
        'context': 'question_neutral',
        'recommended': 'standard',
        'reason': 'User prefers balanced responses for questions'
    })
    
    print("Session stats:", manager.get_session_stats())
    
    # End session
    summary = manager.end_session()
    print("\nLearning summary:", json.dumps(summary, indent=2))
