#!/usr/bin/env python3
"""
Learning Extractor - Automatically extracts learnings from checkpoint summaries
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class LearningType(Enum):
    DECISION = "decision"
    PATTERN = "pattern"
    POLICY = "policy"
    SOLUTION = "solution"
    MISTAKE = "mistake"

@dataclass
class Learning:
    """Represents a captured learning with evolution tracking"""
    # Core fields
    type: LearningType
    title: str
    content: str
    context: str
    confidence: float  # 0.0 to 1.0
    tags: List[str]
    source: str  # checkpoint ID or conversation reference
    
    # Evolution tracking
    created_at: str = None  # ISO format timestamp
    half_life_days: int = 180  # 6 months default
    
    # Usage tracking
    tries: int = 0
    successes: int = 0
    failures: int = 0
    last_used: Optional[str] = None  # ISO format timestamp
    
    # Context tracking (multiple contexts where this was validated)
    contexts: List[str] = None
    sources: List[str] = None
    
    # Tool tracking
    tools: List[Dict] = None  # [{name, version, released}]
    
    # Evolution tracking
    superseded_by: Optional[str] = None
    supersedes: Optional[str] = None
    status: str = "active"  # active, legacy, deprecated, archived
    
    def __post_init__(self):
        """Initialize default values for mutable fields"""
        if self.created_at is None:
            from datetime import datetime
            self.created_at = datetime.now().isoformat()
        if self.contexts is None:
            self.contexts = [self.context] if self.context else []
        if self.sources is None:
            self.sources = [self.source] if self.source else []
        if self.tools is None:
            self.tools = []
    
    @property
    def age_days(self) -> int:
        """Calculate age in days"""
        from datetime import datetime
        created = datetime.fromisoformat(self.created_at)
        return (datetime.now() - created).days
    
    @property
    def current_confidence(self) -> float:
        """Confidence with time-based decay applied"""
        decay_factor = 0.5 ** (self.age_days / self.half_life_days)
        return self.confidence * decay_factor
    
    @property
    def success_rate(self) -> float:
        """Overall success rate"""
        if self.tries == 0:
            return 0.0
        return self.successes / self.tries
    
    @property
    def recent_success_rate(self) -> float:
        """Success rate for recent uses (last 10 tries)"""
        # TODO: Track individual attempts with timestamps
        return self.success_rate  # Simplified for now

class LearningExtractor:
    """Extracts learnings from checkpoint summaries"""
    
    # Strong signal patterns (high confidence)
    STRONG_SIGNALS = {
        LearningType.DECISION: [
            r"decided to (.+?) because (.+)",
            r"chose (.+?) over (.+?) because (.+)",
            r"going with (.+?) because (.+)",
            r"selected (.+?) due to (.+)",
        ],
        LearningType.PATTERN: [
            r"discovered that (.+?) leads to (.+)",
            r"pattern: (.+)",
            r"noticed that (.+?) results in (.+)",
            r"found that (.+?) causes (.+)",
        ],
        LearningType.POLICY: [
            r"from now on[,:]? (.+)",
            r"policy: (.+)",
            r"new approach: (.+)",
            r"going forward[,:]? (.+)",
        ],
        LearningType.SOLUTION: [
            r"solved by (.+)",
            r"solution: (.+)",
            r"fixed by (.+)",
            r"resolved with (.+)",
        ],
        LearningType.MISTAKE: [
            r"didn't work because (.+)",
            r"failed because (.+)",
            r"mistake: (.+)",
            r"anti-pattern: (.+)",
        ]
    }
    
    # Medium signal patterns (need context validation)
    MEDIUM_SIGNALS = {
        LearningType.DECISION: [
            r"we'll use (.+)",
            r"implementing (.+)",
        ],
        LearningType.PATTERN: [
            r"realized that (.+)",
            r"insight: (.+)",
        ],
        LearningType.POLICY: [
            r"should always (.+)",
            r"must (.+)",
        ],
        LearningType.SOLUTION: [
            r"works better with (.+)",
            r"approach: (.+)",
        ],
        LearningType.MISTAKE: [
            r"doesn't work (.+)",
            r"avoid (.+)",
        ]
    }
    
    def __init__(self):
        self.learnings: List[Learning] = []
    
    def extract_learnings(self, checkpoint_text: str, source: str = "unknown") -> List[Learning]:
        """
        Extract all learnings from checkpoint text
        
        Args:
            checkpoint_text: The checkpoint summary text
            source: Identifier for the source (checkpoint ID, conversation ID)
        
        Returns:
            List of extracted learnings
        """
        self.learnings = []
        
        # Split into sentences for context
        sentences = self._split_sentences(checkpoint_text)
        
        # Extract each type of learning
        for i, sentence in enumerate(sentences):
            context = self._get_context(sentences, i)
            
            # Try strong signals first (high confidence)
            for learning_type, patterns in self.STRONG_SIGNALS.items():
                for pattern in patterns:
                    match = re.search(pattern, sentence, re.IGNORECASE)
                    if match:
                        learning = self._create_learning(
                            learning_type=learning_type,
                            sentence=sentence,
                            match=match,
                            context=context,
                            confidence=0.9,
                            source=source
                        )
                        if learning:
                            self.learnings.append(learning)
            
            # Try medium signals (need validation)
            for learning_type, patterns in self.MEDIUM_SIGNALS.items():
                for pattern in patterns:
                    match = re.search(pattern, sentence, re.IGNORECASE)
                    if match and self._validate_context(sentence, context, learning_type):
                        learning = self._create_learning(
                            learning_type=learning_type,
                            sentence=sentence,
                            match=match,
                            context=context,
                            confidence=0.6,
                            source=source
                        )
                        if learning:
                            self.learnings.append(learning)
        
        return self.learnings
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting (can be improved)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_context(self, sentences: List[str], index: int, window: int = 2) -> str:
        """Get surrounding context for a sentence"""
        start = max(0, index - window)
        end = min(len(sentences), index + window + 1)
        return ' '.join(sentences[start:end])
    
    def _validate_context(self, sentence: str, context: str, learning_type: LearningType) -> bool:
        """
        Validate if medium signal is actually a learning
        
        Args:
            sentence: The sentence with the signal
            context: Surrounding sentences
            learning_type: Type of learning detected
        
        Returns:
            True if this is likely a real learning
        """
        # Check for decision context
        if learning_type == LearningType.DECISION:
            decision_markers = ['because', 'due to', 'since', 'after considering']
            return any(marker in context.lower() for marker in decision_markers)
        
        # Check for pattern context
        if learning_type == LearningType.PATTERN:
            pattern_markers = ['always', 'whenever', 'tends to', 'results in']
            return any(marker in context.lower() for marker in pattern_markers)
        
        # Check for policy context
        if learning_type == LearningType.POLICY:
            policy_markers = ['rule', 'standard', 'approach', 'methodology']
            return any(marker in context.lower() for marker in policy_markers)
        
        # Check for solution context
        if learning_type == LearningType.SOLUTION:
            solution_markers = ['problem', 'issue', 'challenge', 'fixed']
            return any(marker in context.lower() for marker in solution_markers)
        
        # Check for mistake context
        if learning_type == LearningType.MISTAKE:
            mistake_markers = ['failed', 'error', 'wrong', 'instead']
            return any(marker in context.lower() for marker in mistake_markers)
        
        return False
    
    def _create_learning(
        self,
        learning_type: LearningType,
        sentence: str,
        match: re.Match,
        context: str,
        confidence: float,
        source: str
    ) -> Optional[Learning]:
        """
        Create a Learning object from extracted information
        
        Args:
            learning_type: Type of learning
            sentence: The sentence containing the learning
            match: Regex match object
            context: Surrounding context
            confidence: Confidence score (0.0 to 1.0)
            source: Source identifier
        
        Returns:
            Learning object or None if invalid
        """
        try:
            # Generate title based on type
            title = self._generate_title(learning_type, sentence, match)
            
            # Extract content
            content = self._extract_content(learning_type, sentence, match, context)
            
            # Generate tags
            tags = self._generate_tags(learning_type, sentence, context)
            
            return Learning(
                type=learning_type,
                title=title,
                content=content,
                context=context,
                confidence=confidence,
                tags=tags,
                source=source
            )
        except Exception as e:
            print(f"Error creating learning: {e}")
            return None
    
    def _generate_title(self, learning_type: LearningType, sentence: str, match: re.Match) -> str:
        """Generate a descriptive title for the learning"""
        # Extract key terms from sentence
        key_terms = self._extract_key_terms(sentence)
        
        # Format based on type
        if learning_type == LearningType.DECISION:
            return f"Decision: {key_terms[:50]}"
        elif learning_type == LearningType.PATTERN:
            return f"Pattern: {key_terms[:50]}"
        elif learning_type == LearningType.POLICY:
            return f"Policy: {key_terms[:50]}"
        elif learning_type == LearningType.SOLUTION:
            return f"Solution: {key_terms[:50]}"
        elif learning_type == LearningType.MISTAKE:
            return f"Anti-Pattern: {key_terms[:50]}"
        
        return key_terms[:50]
    
    def _extract_content(
        self,
        learning_type: LearningType,
        sentence: str,
        match: re.Match,
        context: str
    ) -> str:
        """Extract the full content of the learning"""
        # For now, use the full sentence + context
        # Can be refined to extract just the relevant parts
        return f"{sentence}\n\nContext: {context}"
    
    def _extract_key_terms(self, text: str) -> str:
        """Extract key terms from text for title"""
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = text.split()
        key_words = [w for w in words if w.lower() not in common_words]
        return ' '.join(key_words[:10])  # First 10 key words
    
    def _generate_tags(self, learning_type: LearningType, sentence: str, context: str) -> List[str]:
        """Generate relevant tags for the learning"""
        tags = [learning_type.value]
        
        # Extract potential tags from text
        text = (sentence + ' ' + context).lower()
        
        # Common project/domain tags
        tag_keywords = {
            'tgif': ['tgif', 'restaurant', 'rollout'],
            'joju': ['joju', 'contribution', 'achievement'],
            'excel': ['excel', 'spreadsheet', 'csv'],
            'api': ['api', 'integration', 'endpoint'],
            'documentation': ['doc', 'documentation', 'readme'],
            'performance': ['performance', 'speed', 'optimization'],
            'workflow': ['workflow', 'process', 'automation'],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def filter_by_confidence(self, min_confidence: float = 0.7) -> List[Learning]:
        """Filter learnings by minimum confidence threshold"""
        return [l for l in self.learnings if l.confidence >= min_confidence]
    
    def filter_by_type(self, learning_type: LearningType) -> List[Learning]:
        """Filter learnings by type"""
        return [l for l in self.learnings if l.type == learning_type]
    
    def to_dict(self) -> List[Dict]:
        """Convert learnings to dictionary format"""
        return [
            {
                'type': l.type.value,
                'title': l.title,
                'content': l.content,
                'context': l.context,
                'confidence': l.confidence,
                'tags': l.tags,
                'source': l.source
            }
            for l in self.learnings
        ]


def test_extractor():
    """Test the learning extractor with sample text"""
    
    sample_checkpoint = """
    Session focused on TGIF rollout opportunities. Initially brainstormed 10 generic 
    solutions but user feedback indicated they weren't game-changing. 
    
    Decided to analyze meeting transcript instead of assuming pain points. Discovered 
    that Patricia/Mario can't track issues across multiple channels (email, text, calls).
    
    From now on: validate pain points with real data before brainstorming solutions.
    
    Excel export failed because Mac Excel crashes on large files. Solved by creating 
    simplified versions with fewer rows.
    
    Pattern: Discovery beats assumption. Real pain points lead to better solutions.
    """
    
    extractor = LearningExtractor()
    learnings = extractor.extract_learnings(sample_checkpoint, source="test_checkpoint")
    
    print(f"\n🧠 Extracted {len(learnings)} learnings:\n")
    
    for i, learning in enumerate(learnings, 1):
        print(f"{i}. [{learning.type.value.upper()}] {learning.title}")
        print(f"   Confidence: {learning.confidence:.1%}")
        print(f"   Tags: {', '.join(learning.tags)}")
        print(f"   Content: {learning.content[:100]}...")
        print()
    
    # Filter high-confidence learnings
    high_confidence = extractor.filter_by_confidence(0.8)
    print(f"\n✅ {len(high_confidence)} high-confidence learnings (>80%)")


if __name__ == "__main__":
    test_extractor()
