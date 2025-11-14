#!/usr/bin/env python3
"""
Response Generator
Generates 3 response options (brief, standard, detailed) in user's voice
"""

from typing import Dict, List
import os

class ResponseGenerator:
    """Generates contextually appropriate responses"""
    
    def __init__(self, voice_profile: Dict = None):
        """
        Initialize response generator
        
        Args:
            voice_profile: User's voice characteristics
        """
        self.voice_profile = voice_profile or self._default_voice_profile()
    
    def _default_voice_profile(self) -> Dict:
        """Default voice profile"""
        return {
            'tone': 'professional_friendly',
            'formality': 'medium',
            'verbosity': 'medium',
            'personality_traits': ['direct', 'helpful', 'thoughtful'],
            'common_phrases': [],
            'avoid_phrases': []
        }
    
    def generate_responses(self, context: Dict, contact_info: Dict = None) -> List[Dict]:
        """
        Generate 3 response options
        
        Args:
            context: Context from context_analyzer
            contact_info: Contact information from matrix
        
        Returns:
            List of 3 response dictionaries (brief, standard, detailed)
        """
        message_type = context.get('message_type', 'statement')
        sentiment = context.get('sentiment', 'neutral')
        urgency = context.get('urgency', 'low')
        last_message = context.get('last_message', {})
        
        # Adjust tone based on contact
        relationship_type = 'professional'
        if contact_info:
            relationship_type = contact_info.get('relationship', {}).get('type', 'professional')
        
        responses = []
        
        # Generate brief response
        responses.append({
            'level': 'brief',
            'text': self._generate_brief(message_type, sentiment, relationship_type, last_message),
            'word_count': None  # Will be calculated
        })
        
        # Generate standard response
        responses.append({
            'level': 'standard',
            'text': self._generate_standard(message_type, sentiment, relationship_type, last_message),
            'word_count': None
        })
        
        # Generate detailed response
        responses.append({
            'level': 'detailed',
            'text': self._generate_detailed(message_type, sentiment, relationship_type, last_message),
            'word_count': None
        })
        
        # Calculate word counts
        for response in responses:
            response['word_count'] = len(response['text'].split())
        
        return responses
    
    def _generate_brief(self, message_type: str, sentiment: str, relationship: str, last_message: Dict) -> str:
        """Generate brief response (1-2 sentences)"""
        
        if message_type == 'question':
            return "Yes, I can help with that. Let me get back to you shortly."
        
        elif message_type == 'request':
            return "On it. I'll have this to you soon."
        
        elif message_type == 'acknowledgment':
            return "You're welcome!"
        
        elif message_type == 'greeting':
            return "Hey! How can I help?"
        
        else:
            return "Got it, thanks for the update."
    
    def _generate_standard(self, message_type: str, sentiment: str, relationship: str, last_message: Dict) -> str:
        """Generate standard response (2-4 sentences)"""
        
        if message_type == 'question':
            return "Thanks for reaching out. I can definitely help with that. Let me review the details and I'll get back to you by end of day with a comprehensive answer."
        
        elif message_type == 'request':
            return "Absolutely, I'm on it. I'll prioritize this and have it to you within the next few hours. I'll send you a quick update if anything comes up."
        
        elif message_type == 'acknowledgment':
            return "You're very welcome! Happy to help. Let me know if you need anything else."
        
        elif message_type == 'greeting':
            return "Hey! Good to hear from you. I'm doing well, thanks for asking. What can I help you with today?"
        
        else:
            return "Thanks for the update, I appreciate you keeping me in the loop. This is helpful context. I'll review and reach out if I have any questions."
    
    def _generate_detailed(self, message_type: str, sentiment: str, relationship: str, last_message: Dict) -> str:
        """Generate detailed response (4-6 sentences)"""
        
        if message_type == 'question':
            return "Thanks so much for reaching out with this question. I can definitely help you with that. Let me take some time to review the details thoroughly and gather all the relevant information. I want to make sure I give you a comprehensive and accurate answer. I'll get back to you by end of day with a detailed response. In the meantime, if you think of any additional context that might be helpful, feel free to send it my way."
        
        elif message_type == 'request':
            return "Absolutely, I'm happy to help with this. I'll prioritize this request and start working on it right away. Based on what you've shared, I should be able to have this completed within the next few hours. I'll keep you updated on my progress and let you know immediately if I run into any issues or need clarification on anything. Thanks for trusting me with this, I'll make sure it's done well."
        
        elif message_type == 'acknowledgment':
            return "You're very welcome! I'm really glad I could help with this. It's always a pleasure working with you on these kinds of projects. If anything else comes up or if you need any follow-up support, please don't hesitate to reach out. I'm here to help and always happy to jump in. Looking forward to our next collaboration!"
        
        elif message_type == 'greeting':
            return "Hey! It's great to hear from you. I hope you're doing well! I'm doing great, thanks for asking. Things have been busy but productive on my end. I'm always happy to chat or help out with anything you might need. What's on your mind today? How can I support you?"
        
        else:
            return "Thanks so much for this update, I really appreciate you taking the time to keep me in the loop. This context is super helpful and gives me a much better understanding of the situation. I'll review everything carefully and make sure I'm aligned with where things are heading. If I have any questions or need clarification on anything, I'll reach out. Otherwise, I'll proceed based on this information. Thanks again for the thorough communication!"
    
    def apply_voice_consistency(self, response: str) -> str:
        """
        Apply voice consistency rules to response
        
        Args:
            response: Generated response text
        
        Returns:
            Response with voice adjustments applied
        """
        # Apply personality traits
        if 'direct' in self.voice_profile.get('personality_traits', []):
            # Remove excessive pleasantries
            response = response.replace('I would really appreciate', 'I appreciate')
            response = response.replace('if you could possibly', 'if you could')
        
        # Apply common phrases
        for phrase in self.voice_profile.get('common_phrases', []):
            # Could implement phrase injection here
            pass
        
        # Remove avoided phrases
        for phrase in self.voice_profile.get('avoid_phrases', []):
            response = response.replace(phrase, '')
        
        return response.strip()

if __name__ == "__main__":
    # Test
    generator = ResponseGenerator()
    
    test_context = {
        'message_type': 'question',
        'sentiment': 'neutral',
        'urgency': 'medium',
        'last_message': {'text': 'Can you send me the report?'}
    }
    
    responses = generator.generate_responses(test_context)
    
    for response in responses:
        print(f"\n{response['level'].upper()} ({response['word_count']} words):")
        print(response['text'])
