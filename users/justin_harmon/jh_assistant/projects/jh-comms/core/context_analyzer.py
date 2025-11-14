#!/usr/bin/env python3
"""
Context Analyzer
Analyzes screenshots and messages to extract context for response generation
"""

import re
from datetime import datetime
from typing import Dict, List, Optional

class ContextAnalyzer:
    """Analyzes conversation context from screenshots and text"""
    
    def __init__(self):
        self.message_patterns = {
            'question': r'\?$',
            'urgent': r'(urgent|asap|immediately|now)',
            'request': r'(can you|could you|would you|please)',
            'thanks': r'(thanks|thank you|appreciate)',
            'greeting': r'^(hi|hello|hey|good morning|good afternoon)'
        }
    
    def analyze_screenshot(self, ocr_text: str, contact_info: Optional[Dict] = None) -> Dict:
        """
        Analyze OCR text from screenshot
        
        Args:
            ocr_text: Text extracted from screenshot
            contact_info: Optional contact information
        
        Returns:
            Context dictionary with analysis results
        """
        context = {
            'timestamp': datetime.now().isoformat(),
            'raw_text': ocr_text,
            'messages': self.extract_messages(ocr_text),
            'last_message': None,
            'sentiment': self.detect_sentiment(ocr_text),
            'urgency': self.detect_urgency(ocr_text),
            'message_type': self.classify_message(ocr_text),
            'requires_action': self.requires_action(ocr_text),
            'contact_context': contact_info or {}
        }
        
        # Identify last message
        if context['messages']:
            context['last_message'] = context['messages'][-1]
        
        return context
    
    def extract_messages(self, text: str) -> List[Dict]:
        """
        Extract individual messages from conversation text
        
        Returns:
            List of message dictionaries
        """
        messages = []
        
        # Split by common message separators
        lines = text.split('\n')
        
        current_message = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect message sender (simple heuristic)
            if self._looks_like_sender(line):
                if current_message:
                    messages.append(current_message)
                current_message = {
                    'sender': line,
                    'text': '',
                    'timestamp': None
                }
            elif current_message:
                current_message['text'] += line + ' '
        
        if current_message:
            messages.append(current_message)
        
        return messages
    
    def _looks_like_sender(self, line: str) -> bool:
        """Check if line looks like a sender name"""
        # Simple heuristics
        if len(line) < 3 or len(line) > 50:
            return False
        if line.endswith(':'):
            return True
        if line.isupper() and len(line.split()) <= 3:
            return True
        return False
    
    def detect_sentiment(self, text: str) -> str:
        """
        Detect sentiment of message
        
        Returns:
            'positive', 'negative', 'neutral', or 'urgent'
        """
        text_lower = text.lower()
        
        # Urgent indicators
        if any(word in text_lower for word in ['urgent', 'asap', 'immediately', 'emergency']):
            return 'urgent'
        
        # Positive indicators
        positive_words = ['thanks', 'great', 'awesome', 'perfect', 'excellent', 'appreciate']
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        # Negative indicators
        negative_words = ['problem', 'issue', 'wrong', 'error', 'failed', 'broken']
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def detect_urgency(self, text: str) -> str:
        """
        Detect urgency level
        
        Returns:
            'high', 'medium', or 'low'
        """
        text_lower = text.lower()
        
        # High urgency
        high_urgency = ['urgent', 'asap', 'immediately', 'emergency', 'critical', 'now']
        if any(word in text_lower for word in high_urgency):
            return 'high'
        
        # Medium urgency
        medium_urgency = ['soon', 'today', 'quick', 'when you can']
        if any(word in text_lower for word in medium_urgency):
            return 'medium'
        
        return 'low'
    
    def classify_message(self, text: str) -> str:
        """
        Classify message type
        
        Returns:
            Message type string
        """
        text_lower = text.lower()
        
        # Check patterns
        if re.search(self.message_patterns['question'], text):
            return 'question'
        elif re.search(self.message_patterns['request'], text_lower):
            return 'request'
        elif re.search(self.message_patterns['thanks'], text_lower):
            return 'acknowledgment'
        elif re.search(self.message_patterns['greeting'], text_lower):
            return 'greeting'
        else:
            return 'statement'
    
    def requires_action(self, text: str) -> bool:
        """
        Determine if message requires action/response
        
        Returns:
            True if action required
        """
        text_lower = text.lower()
        
        # Questions always require response
        if '?' in text:
            return True
        
        # Requests require response
        if re.search(self.message_patterns['request'], text_lower):
            return True
        
        # Urgent messages require response
        if self.detect_urgency(text) == 'high':
            return True
        
        # Thanks/acknowledgments may not need response
        if re.search(self.message_patterns['thanks'], text_lower) and len(text.split()) < 10:
            return False
        
        return True

if __name__ == "__main__":
    # Test
    analyzer = ContextAnalyzer()
    
    test_text = """
    John: Hey, can you send me the report by EOD?
    Me: Sure, I'll get that to you this afternoon.
    John: Thanks! Also, do you have time for a quick call?
    """
    
    context = analyzer.analyze_screenshot(test_text)
    
    import json
    print(json.dumps(context, indent=2, default=str))
