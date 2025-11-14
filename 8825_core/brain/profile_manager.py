#!/usr/bin/env python3
"""
Profile Manager
Manages user learning profiles - load, save, update, query
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))
from paths import get_user_dir, get_system_root


@dataclass
class LearningPreference:
    """Single learning preference with confidence"""
    preference: str
    confidence: float
    last_updated: str
    notes: str = ""


@dataclass
class ObservedPattern:
    """Pattern that works or fails for user"""
    pattern: str
    context: str
    confidence: float
    timestamp: str


@dataclass
class TeachingMoment:
    """Record of a teaching interaction"""
    date: str
    topic: str
    approach: str
    result: str
    rating: int
    notes: str = ""


class LearningProfile:
    """User's learning profile"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_path = get_user_dir(user_id) / 'profile' / 'learning_profile.json'
        self.data = self._load_or_create()
    
    def _load_or_create(self) -> Dict[str, Any]:
        """Load existing profile or create default"""
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_profile()
    
    def _create_default_profile(self) -> Dict[str, Any]:
        """Create default profile for new users"""
        now = datetime.utcnow().isoformat() + 'Z'
        
        return {
            "user_id": self.user_id,
            "display_name": self.user_id.replace('_', ' ').title(),
            "created_at": now,
            "last_updated": now,
            "version": "1.0.0",
            
            "learning_preferences": {
                "information_density": {
                    "preference": "moderate",
                    "confidence": 0.5,
                    "last_updated": now,
                    "notes": "Default: Concepts + examples"
                },
                "example_preference": {
                    "preference": "concrete",
                    "confidence": 0.5,
                    "last_updated": now,
                    "notes": "Default: Real examples from work"
                },
                "depth_approach": {
                    "preference": "top_down",
                    "confidence": 0.5,
                    "last_updated": now,
                    "notes": "Default: Big picture first"
                },
                "interaction_style": {
                    "preference": "show_and_explain",
                    "confidence": 0.5,
                    "last_updated": now,
                    "notes": "Default: Demonstrate then explain"
                },
                "error_tolerance": {
                    "preference": "medium",
                    "confidence": 0.5,
                    "last_updated": now,
                    "notes": "Default: Guided experimentation"
                }
            },
            
            "observed_patterns": {
                "what_works": [],
                "what_fails": []
            },
            
            "teaching_moments": {
                "successful": [],
                "unsuccessful": []
            },
            
            "adaptations": {
                "recent_changes": []
            },
            
            "meta": {
                "total_teaching_moments": 0,
                "successful_moments": 0,
                "unsuccessful_moments": 0,
                "success_rate": 0.0,
                "average_rating": 0.0,
                "confidence_trend": "stable",
                "last_interaction": now,
                "interactions_count": 0,
                "profile_maturity": "new"
            },
            
            "key_insights": []
        }
    
    def save(self):
        """Save profile to disk"""
        # Update last_updated
        self.data['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Ensure directory exists
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write profile
        with open(self.profile_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_preference(self, dimension: str) -> Optional[Dict[str, Any]]:
        """Get a specific learning preference"""
        return self.data['learning_preferences'].get(dimension)
    
    def update_preference(self, dimension: str, preference: str, confidence: float, notes: str = ""):
        """Update a learning preference"""
        now = datetime.utcnow().isoformat() + 'Z'
        
        if dimension not in self.data['learning_preferences']:
            raise ValueError(f"Unknown dimension: {dimension}")
        
        old_pref = self.data['learning_preferences'][dimension]
        
        # Record adaptation if preference changed
        if old_pref['preference'] != preference:
            self.data['adaptations']['recent_changes'].append({
                'dimension': dimension,
                'from': old_pref['preference'],
                'to': preference,
                'reason': notes or "Manual update",
                'timestamp': now,
                'confidence_before': old_pref['confidence'],
                'confidence_after': confidence
            })
        
        # Update preference
        self.data['learning_preferences'][dimension] = {
            'preference': preference,
            'confidence': confidence,
            'last_updated': now,
            'notes': notes
        }
        
        self.save()
    
    def add_teaching_moment(self, moment: Dict[str, Any], successful: bool):
        """Record a teaching moment"""
        key = 'successful' if successful else 'unsuccessful'
        self.data['teaching_moments'][key].append(moment)
        
        # Update meta
        self.data['meta']['total_teaching_moments'] += 1
        if successful:
            self.data['meta']['successful_moments'] += 1
        else:
            self.data['meta']['unsuccessful_moments'] += 1
        
        # Recalculate success rate
        total = self.data['meta']['total_teaching_moments']
        successful_count = self.data['meta']['successful_moments']
        self.data['meta']['success_rate'] = successful_count / total if total > 0 else 0.0
        
        # Update average rating
        all_moments = (self.data['teaching_moments']['successful'] + 
                      self.data['teaching_moments']['unsuccessful'])
        ratings = [m.get('rating', 0) for m in all_moments if 'rating' in m]
        self.data['meta']['average_rating'] = sum(ratings) / len(ratings) if ratings else 0.0
        
        self.save()
    
    def add_pattern(self, pattern: str, context: str, works: bool, confidence: float = 0.8):
        """Add an observed pattern"""
        now = datetime.utcnow().isoformat() + 'Z'
        
        pattern_obj = {
            'pattern': pattern,
            'context': context,
            'confidence': confidence,
            'timestamp': now
        }
        
        key = 'what_works' if works else 'what_fails'
        self.data['observed_patterns'][key].append(pattern_obj)
        
        self.save()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get profile summary"""
        return {
            'user_id': self.data['user_id'],
            'display_name': self.data.get('display_name', self.user_id),
            'maturity': self.data['meta']['profile_maturity'],
            'success_rate': self.data['meta']['success_rate'],
            'preferences': {
                dim: pref['preference'] 
                for dim, pref in self.data['learning_preferences'].items()
            },
            'confidence_scores': {
                dim: pref['confidence']
                for dim, pref in self.data['learning_preferences'].items()
            }
        }
    
    def export(self) -> str:
        """Export profile as JSON string"""
        return json.dumps(self.data, indent=2)


class ProfileManager:
    """Manages multiple user profiles"""
    
    @staticmethod
    def load_profile(user_id: str) -> LearningProfile:
        """Load a user's profile"""
        return LearningProfile(user_id)
    
    @staticmethod
    def create_profile(user_id: str, display_name: str = None) -> LearningProfile:
        """Create a new user profile"""
        profile = LearningProfile(user_id)
        if display_name:
            profile.data['display_name'] = display_name
        profile.save()
        return profile
    
    @staticmethod
    def list_profiles() -> List[str]:
        """List all user profiles"""
        users_dir = get_system_root() / 'users'
        if not users_dir.exists():
            return []
        
        profiles = []
        for user_dir in users_dir.iterdir():
            if user_dir.is_dir():
                profile_path = user_dir / 'profile' / 'learning_profile.json'
                if profile_path.exists():
                    profiles.append(user_dir.name)
        
        return profiles
    
    @staticmethod
    def delete_profile(user_id: str, confirm: bool = False):
        """Delete a user profile"""
        if not confirm:
            raise ValueError("Must confirm deletion with confirm=True")
        
        profile_path = get_user_dir(user_id) / 'profile' / 'learning_profile.json'
        if profile_path.exists():
            profile_path.unlink()


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage user learning profiles')
    parser.add_argument('--user', default='justin_harmon', help='User ID')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # View profile
    view_parser = subparsers.add_parser('view', help='View profile')
    
    # Update preference
    update_parser = subparsers.add_parser('update', help='Update preference')
    update_parser.add_argument('--dimension', required=True, 
                              choices=['information_density', 'example_preference', 
                                      'depth_approach', 'interaction_style', 'error_tolerance'])
    update_parser.add_argument('--value', required=True, help='New preference value')
    update_parser.add_argument('--confidence', type=float, default=0.8, help='Confidence score')
    update_parser.add_argument('--notes', default='', help='Notes about change')
    
    # List profiles
    list_parser = subparsers.add_parser('list', help='List all profiles')
    
    # Export profile
    export_parser = subparsers.add_parser('export', help='Export profile')
    
    # Create profile
    create_parser = subparsers.add_parser('create', help='Create new profile')
    create_parser.add_argument('--display-name', help='Display name')
    
    args = parser.parse_args()
    
    if args.command == 'view':
        profile = ProfileManager.load_profile(args.user)
        summary = profile.get_summary()
        print(f"\n📊 Learning Profile: {summary['display_name']}")
        print(f"   User ID: {summary['user_id']}")
        print(f"   Maturity: {summary['maturity']}")
        print(f"   Success Rate: {summary['success_rate']:.1%}")
        print("\n   Preferences:")
        for dim, pref in summary['preferences'].items():
            conf = summary['confidence_scores'][dim]
            print(f"     • {dim}: {pref} (confidence: {conf:.2f})")
        print()
    
    elif args.command == 'update':
        profile = ProfileManager.load_profile(args.user)
        profile.update_preference(args.dimension, args.value, args.confidence, args.notes)
        print(f"✅ Updated {args.dimension} to {args.value}")
    
    elif args.command == 'list':
        profiles = ProfileManager.list_profiles()
        print(f"\n📋 User Profiles ({len(profiles)}):")
        for user_id in profiles:
            profile = ProfileManager.load_profile(user_id)
            summary = profile.get_summary()
            print(f"   • {summary['display_name']} ({user_id}) - {summary['maturity']}")
        print()
    
    elif args.command == 'export':
        profile = ProfileManager.load_profile(args.user)
        print(profile.export())
    
    elif args.command == 'create':
        profile = ProfileManager.create_profile(args.user, args.display_name)
        print(f"✅ Created profile for {args.user}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
