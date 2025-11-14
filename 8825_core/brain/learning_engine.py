#!/usr/bin/env python3
"""
Learning Engine
Observes user interactions and adapts learning profiles
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))
from paths import get_user_dir

# Import profile manager
from profile_manager import LearningProfile, ProfileManager


class Signal(Enum):
    """User signals during interactions"""
    UNDERSTANDING = "understanding"
    CONFUSION = "confusion"
    BOREDOM = "boredom"
    OVERWHELM = "overwhelm"
    ENGAGEMENT = "engagement"


class TeachingApproach(Enum):
    """Different teaching approaches"""
    SHOW_FIRST = "show_first"
    EXPLAIN_FIRST = "explain_first"
    SHOW_AND_EXPLAIN = "show_and_explain"
    LET_EXPLORE = "let_explore"
    WALK_THROUGH = "walk_through"


@dataclass
class Interaction:
    """User interaction"""
    user_input: str
    ai_response: str
    timestamp: str
    context: str = ""
    signals: List[Signal] = None


@dataclass
class TeachingMoment:
    """Teaching moment details"""
    topic: str
    approach: TeachingApproach
    user_response: str
    signals_detected: List[Signal]
    successful: bool
    notes: str = ""


class LearningEngine:
    """
    Observes user interactions and updates learning profile
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile = ProfileManager.load_profile(user_id)
        self.interaction_history = []
    
    def detect_signals(self, user_response: str) -> List[Signal]:
        """
        Detect sentiment signals from user response
        
        Returns list of detected signals
        """
        response_lower = user_response.lower()
        signals = []
        
        # Understanding signals
        understanding_phrases = [
            "makes sense", "i see", "got it", "that makes sense",
            "i understand", "clear", "perfect", "exactly"
        ]
        if any(phrase in response_lower for phrase in understanding_phrases):
            signals.append(Signal.UNDERSTANDING)
        
        # Confusion signals
        confusion_phrases = [
            "wait", "huh", "what", "confused", "don't understand",
            "not sure", "lost", "unclear"
        ]
        if any(phrase in response_lower for phrase in confusion_phrases):
            signals.append(Signal.CONFUSION)
        
        # Boredom/too slow signals
        boredom_phrases = [
            "yeah yeah", "i got it", "skip", "move on",
            "just show me", "just do it", "faster"
        ]
        if any(phrase in response_lower for phrase in boredom_phrases):
            signals.append(Signal.BOREDOM)
        
        # Overwhelm/too fast signals
        overwhelm_phrases = [
            "slow down", "too much", "overwhelming", "too fast",
            "wait what", "too complicated", "simpler"
        ]
        if any(phrase in response_lower for phrase in overwhelm_phrases):
            signals.append(Signal.OVERWHELM)
        
        # Engagement signals
        engagement_phrases = [
            "interesting", "can we", "what if", "how about",
            "could i", "tell me more", "go deeper"
        ]
        # Also check for questions as engagement
        if any(phrase in response_lower for phrase in engagement_phrases) or \
           response_lower.strip().endswith('?'):
            signals.append(Signal.ENGAGEMENT)
        
        return signals
    
    def observe_interaction(self, interaction: Interaction):
        """Track user interaction and update profile if needed"""
        self.interaction_history.append(interaction)
        
        # Detect signals if not provided
        if not interaction.signals:
            interaction.signals = self.detect_signals(interaction.user_input)
        
        # Update profile based on signals
        if Signal.CONFUSION in interaction.signals:
            self._handle_confusion(interaction)
        elif Signal.BOREDOM in interaction.signals:
            self._handle_boredom(interaction)
        elif Signal.OVERWHELM in interaction.signals:
            self._handle_overwhelm(interaction)
        elif Signal.UNDERSTANDING in interaction.signals:
            self._reinforce_current_approach()
        
        # Update interaction count
        self.profile.data['meta']['interactions_count'] += 1
        self.profile.data['meta']['last_interaction'] = interaction.timestamp
        self.profile.save()
    
    def _handle_confusion(self, interaction: Interaction):
        """Handle confusion signal - may need to adjust approach"""
        # If user is confused, current approach might not be working
        current_style = self.profile.get_preference('interaction_style')
        
        # Lower confidence slightly
        new_confidence = max(0.3, current_style['confidence'] - 0.05)
        
        # Add pattern
        self.profile.add_pattern(
            pattern="User showed confusion",
            context=interaction.context or "Recent interaction",
            works=False,
            confidence=0.7
        )
    
    def _handle_boredom(self, interaction: Interaction):
        """Handle boredom signal - user wants faster pace"""
        # User is bored = we're going too slow or too detailed
        density_pref = self.profile.get_preference('information_density')
        
        # If currently moderate, suggest increasing
        if density_pref['preference'] == 'moderate':
            # Don't auto-change, but note the pattern
            self.profile.add_pattern(
                pattern="User wants faster pace / skip details",
                context=interaction.context or "Recent interaction",
                works=True,
                confidence=0.8
            )
    
    def _handle_overwhelm(self, interaction: Interaction):
        """Handle overwhelm signal - user wants slower pace"""
        # User is overwhelmed = we're going too fast or too dense
        self.profile.add_pattern(
            pattern="User wants slower pace / more examples",
            context=interaction.context or "Recent interaction",
            works=False,
            confidence=0.8
        )
    
    def _reinforce_current_approach(self):
        """Reinforce current approach when user understands"""
        # Slightly increase confidence in current preferences
        for dimension in self.profile.data['learning_preferences']:
            pref = self.profile.data['learning_preferences'][dimension]
            pref['confidence'] = min(0.99, pref['confidence'] + 0.02)
        
        self.profile.save()
    
    def track_teaching_moment(self, moment: TeachingMoment):
        """
        Record outcome of teaching moment and update profile
        """
        now = datetime.utcnow().isoformat() + 'Z'
        
        moment_dict = {
            'date': now,
            'topic': moment.topic,
            'approach': moment.approach.value if isinstance(moment.approach, TeachingApproach) else moment.approach,
            'result': 'success' if moment.successful else 'unsuccessful',
            'rating': 5 if moment.successful else 2,
            'notes': moment.notes,
            'signals': [s.value for s in moment.signals_detected]
        }
        
        self.profile.add_teaching_moment(moment_dict, moment.successful)
        
        # Update profile based on outcome
        if moment.successful:
            # Reinforce current approach
            self._reinforce_successful_approach(moment)
        else:
            # Adjust approach
            self._adjust_unsuccessful_approach(moment)
    
    def _reinforce_successful_approach(self, moment: TeachingMoment):
        """Reinforce approach that worked"""
        # Increase confidence in current interaction style
        style_pref = self.profile.get_preference('interaction_style')
        new_confidence = min(0.99, style_pref['confidence'] + 0.05)
        
        self.profile.update_preference(
            'interaction_style',
            style_pref['preference'],
            new_confidence,
            f"Reinforced by successful teaching: {moment.topic}"
        )
        
        # Add successful pattern
        self.profile.add_pattern(
            pattern=f"Teaching approach: {moment.approach.value}",
            context=moment.topic,
            works=True,
            confidence=0.85
        )
    
    def _adjust_unsuccessful_approach(self, moment: TeachingMoment):
        """Adjust approach that didn't work"""
        # Lower confidence in current approach
        style_pref = self.profile.get_preference('interaction_style')
        new_confidence = max(0.3, style_pref['confidence'] - 0.1)
        
        # Don't auto-change preference, but lower confidence
        self.profile.update_preference(
            'interaction_style',
            style_pref['preference'],
            new_confidence,
            f"Unsuccessful teaching: {moment.topic}"
        )
        
        # Add unsuccessful pattern
        self.profile.add_pattern(
            pattern=f"Teaching approach: {moment.approach.value}",
            context=moment.topic,
            works=False,
            confidence=0.85
        )
    
    def suggest_teaching_approach(self, topic: str, context: str = "") -> Dict[str, Any]:
        """
        Suggest best teaching approach based on profile
        
        Returns dict with approach details and confidence
        """
        prefs = self.profile.data['learning_preferences']
        
        # Get current preferences
        density = prefs['information_density']['preference']
        examples = prefs['example_preference']['preference']
        depth = prefs['depth_approach']['preference']
        style = prefs['interaction_style']['preference']
        tolerance = prefs['error_tolerance']['preference']
        
        # Calculate overall confidence
        confidences = [p['confidence'] for p in prefs.values()]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Build suggestion
        suggestion = {
            'approach': style,
            'confidence': avg_confidence,
            'guidelines': {
                'density': density,
                'examples': examples,
                'depth': depth,
                'error_tolerance': tolerance
            },
            'recommendations': self._generate_recommendations(prefs),
            'patterns_to_apply': self._get_relevant_patterns(context)
        }
        
        return suggestion
    
    def _generate_recommendations(self, prefs: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on preferences"""
        recommendations = []
        
        # Based on interaction style
        style = prefs['interaction_style']['preference']
        if style == 'show_and_explain':
            recommendations.append("Show working code first, then explain why")
        elif style == 'explain_first':
            recommendations.append("Explain concept before showing implementation")
        elif style == 'show_first':
            recommendations.append("Demonstrate immediately, explain after")
        
        # Based on example preference
        examples = prefs['example_preference']['preference']
        if examples == 'concrete':
            recommendations.append("Use real examples from user's actual work")
        elif examples == 'abstract':
            recommendations.append("Use theoretical examples to illustrate concepts")
        
        # Based on depth approach
        depth = prefs['depth_approach']['preference']
        if depth == 'top_down':
            recommendations.append("Start with big picture, drill into details")
        elif depth == 'bottom_up':
            recommendations.append("Start with specifics, build to concepts")
        
        # Based on error tolerance
        tolerance = prefs['error_tolerance']['preference']
        if tolerance == 'high':
            recommendations.append("Let user iterate and learn from failures")
        elif tolerance == 'low':
            recommendations.append("Explain thoroughly before user tries")
        
        return recommendations
    
    def _get_relevant_patterns(self, context: str) -> List[Dict[str, Any]]:
        """Get patterns relevant to current context"""
        patterns = []
        
        # Get what works
        for pattern in self.profile.data['observed_patterns']['what_works']:
            if context.lower() in pattern['context'].lower():
                patterns.append({
                    'pattern': pattern['pattern'],
                    'works': True,
                    'confidence': pattern['confidence']
                })
        
        # Get what fails
        for pattern in self.profile.data['observed_patterns']['what_fails']:
            if context.lower() in pattern['context'].lower():
                patterns.append({
                    'pattern': pattern['pattern'],
                    'works': False,
                    'confidence': pattern['confidence']
                })
        
        return patterns
    
    def calculate_profile_maturity(self) -> str:
        """
        Calculate profile maturity level
        
        Returns: 'new', 'developing', 'established', 'high'
        """
        meta = self.profile.data['meta']
        
        interactions = meta['interactions_count']
        teaching_moments = meta['total_teaching_moments']
        avg_confidence = sum(
            p['confidence'] 
            for p in self.profile.data['learning_preferences'].values()
        ) / 5
        
        if interactions < 10 or teaching_moments < 3:
            return 'new'
        elif interactions < 50 or teaching_moments < 10 or avg_confidence < 0.7:
            return 'developing'
        elif interactions < 100 or teaching_moments < 20 or avg_confidence < 0.85:
            return 'established'
        else:
            return 'high'
    
    def get_adaptation_suggestions(self) -> List[str]:
        """Get suggestions for profile adaptation"""
        suggestions = []
        prefs = self.profile.data['learning_preferences']
        
        # Check for low confidence preferences
        for dim, pref in prefs.items():
            if pref['confidence'] < 0.6:
                suggestions.append(
                    f"Low confidence in {dim} ({pref['confidence']:.2f}). "
                    f"Need more data to refine preference."
                )
        
        # Check success rate
        success_rate = self.profile.data['meta']['success_rate']
        if success_rate < 0.5 and self.profile.data['meta']['total_teaching_moments'] > 5:
            suggestions.append(
                f"Low success rate ({success_rate:.1%}). "
                "Consider adjusting teaching approach."
            )
        
        # Check for conflicting patterns
        works_patterns = [p['pattern'] for p in self.profile.data['observed_patterns']['what_works']]
        fails_patterns = [p['pattern'] for p in self.profile.data['observed_patterns']['what_fails']]
        
        conflicts = set(works_patterns) & set(fails_patterns)
        if conflicts:
            suggestions.append(
                f"Conflicting patterns detected: {', '.join(conflicts)}. "
                "May need manual review."
            )
        
        return suggestions


def main():
    """CLI interface for learning engine"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Learning Engine - Profile Adaptation')
    parser.add_argument('--user', default='justin_harmon', help='User ID')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Suggest approach
    suggest_parser = subparsers.add_parser('suggest', help='Suggest teaching approach')
    suggest_parser.add_argument('--topic', required=True, help='Topic to teach')
    suggest_parser.add_argument('--context', default='', help='Context')
    
    # Track moment
    track_parser = subparsers.add_parser('track', help='Track teaching moment')
    track_parser.add_argument('--topic', required=True, help='Topic taught')
    track_parser.add_argument('--approach', required=True, help='Approach used')
    track_parser.add_argument('--successful', action='store_true', help='Was successful')
    track_parser.add_argument('--notes', default='', help='Notes')
    
    # Get suggestions
    adapt_parser = subparsers.add_parser('adapt', help='Get adaptation suggestions')
    
    args = parser.parse_args()
    
    engine = LearningEngine(args.user)
    
    if args.command == 'suggest':
        suggestion = engine.suggest_teaching_approach(args.topic, args.context)
        print(f"\n📚 Teaching Suggestion for: {args.topic}")
        print(f"   Confidence: {suggestion['confidence']:.1%}")
        print(f"\n   Approach: {suggestion['approach']}")
        print(f"\n   Guidelines:")
        for key, value in suggestion['guidelines'].items():
            print(f"     • {key}: {value}")
        print(f"\n   Recommendations:")
        for rec in suggestion['recommendations']:
            print(f"     • {rec}")
        if suggestion['patterns_to_apply']:
            print(f"\n   Relevant Patterns:")
            for pattern in suggestion['patterns_to_apply']:
                status = "✅ Works" if pattern['works'] else "❌ Fails"
                print(f"     {status}: {pattern['pattern']} ({pattern['confidence']:.0%})")
        print()
    
    elif args.command == 'track':
        moment = TeachingMoment(
            topic=args.topic,
            approach=args.approach,
            user_response="",
            signals_detected=[],
            successful=args.successful,
            notes=args.notes
        )
        engine.track_teaching_moment(moment)
        status = "✅" if args.successful else "❌"
        print(f"{status} Tracked teaching moment: {args.topic}")
    
    elif args.command == 'adapt':
        suggestions = engine.get_adaptation_suggestions()
        print(f"\n🔄 Adaptation Suggestions:")
        if suggestions:
            for s in suggestions:
                print(f"   • {s}")
        else:
            print(f"   ✅ No adaptations needed - profile looks good")
        print()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
