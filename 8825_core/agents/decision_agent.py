#!/usr/bin/env python3
"""
8825 Decision Agent Implementation
Version: 1.0.0
Based on: protocols/8825_decision-making

Intelligent decision maker using confidence matrix:
(intent × 0.4) + (stakes_inverse × 0.3) + (efficiency × 0.2) + (reversibility × 0.1)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import json


class DecisionAction(Enum):
    """Decision outcomes"""
    PROCEED = "proceed"
    DEFAULT = "default"
    ASK = "ask"


@dataclass
class DecisionFactors:
    """Factors for decision matrix calculation"""
    intent_clarity: float  # 0.0-1.0
    stakes_inverse: float  # 0.0-1.0 (higher = lower stakes)
    efficiency: float      # 0.0-1.0
    reversibility: float   # 0.0-1.0


@dataclass
class DecisionResult:
    """Result of decision calculation"""
    action: DecisionAction
    score: float
    reasoning: str
    options: Optional[List[str]] = None
    rationale: Optional[str] = None


class DecisionAgent:
    """
    Intelligent decision maker based on 8825 decision-making protocol.
    
    Calculates confidence scores and determines whether to:
    - Proceed immediately (score ≥ 0.7)
    - Use sensible default (score 0.5-0.7)
    - Ask for clarification (score < 0.5)
    """
    
    # Weights for decision matrix
    WEIGHTS = {
        'intent': 0.4,
        'stakes': 0.3,
        'efficiency': 0.2,
        'reversibility': 0.1
    }
    
    # Decision thresholds
    THRESHOLD_PROCEED = 0.7
    THRESHOLD_DEFAULT = 0.5
    
    # Override conditions (always ask)
    DESTRUCTIVE_KEYWORDS = [
        'delete', 'remove', 'drop', 'destroy', 'erase', 'wipe', 'purge'
    ]
    SECURITY_KEYWORDS = [
        'auth', 'permission', 'security', 'password', 'token', 'credential', 'encrypt'
    ]
    
    def __init__(self, user_preferences: Optional[Dict] = None):
        """
        Initialize decision agent.
        
        Args:
            user_preferences: Optional dict with user-specific thresholds and preferences
        """
        self.user_preferences = user_preferences or {}
        self.decision_history: List[Dict] = []
        
    def calculate_score(self, factors: DecisionFactors) -> float:
        """
        Calculate confidence score using weighted formula.
        
        Formula: (intent × 0.4) + (stakes_inverse × 0.3) + (efficiency × 0.2) + (reversibility × 0.1)
        
        Args:
            factors: DecisionFactors with values 0.0-1.0
            
        Returns:
            Confidence score 0.0-1.0
        """
        score = (
            factors.intent_clarity * self.WEIGHTS['intent'] +
            factors.stakes_inverse * self.WEIGHTS['stakes'] +
            factors.efficiency * self.WEIGHTS['efficiency'] +
            factors.reversibility * self.WEIGHTS['reversibility']
        )
        return round(score, 2)
    
    def check_safety_override(self, request: str) -> Tuple[bool, str]:
        """
        Check if request requires safety override (always ask).
        
        Args:
            request: User request string
            
        Returns:
            Tuple of (should_override, reason)
        """
        request_lower = request.lower()
        
        # Check for destructive operations
        for keyword in self.DESTRUCTIVE_KEYWORDS:
            if keyword in request_lower:
                return True, f"Destructive operation detected: '{keyword}'"
        
        # Check for security-related operations
        for keyword in self.SECURITY_KEYWORDS:
            if keyword in request_lower:
                return True, f"Security-related operation detected: '{keyword}'"
        
        return False, ""
    
    def make_decision(
        self,
        request: str,
        factors: DecisionFactors,
        context: Optional[Dict] = None
    ) -> DecisionResult:
        """
        Make decision based on request and factors.
        
        Args:
            request: User request string
            factors: DecisionFactors for calculation
            context: Optional context (project patterns, user history, etc.)
            
        Returns:
            DecisionResult with action, score, and reasoning
        """
        # Check safety overrides first
        override, override_reason = self.check_safety_override(request)
        if override:
            result = DecisionResult(
                action=DecisionAction.ASK,
                score=0.0,
                reasoning=f"Safety override: {override_reason}",
                options=["Confirm and proceed", "Cancel operation"]
            )
            self._log_decision(request, factors, result, override=True)
            return result
        
        # Check for zero reversibility or stakes (always ask)
        if factors.reversibility == 0.0:
            result = DecisionResult(
                action=DecisionAction.ASK,
                score=0.0,
                reasoning="Irreversible operation - confirmation required",
                options=["Confirm and proceed", "Cancel operation"]
            )
            self._log_decision(request, factors, result, override=True)
            return result
        
        if factors.stakes_inverse == 0.0:
            result = DecisionResult(
                action=DecisionAction.ASK,
                score=0.0,
                reasoning="Critical stakes - confirmation required",
                options=["Confirm and proceed", "Cancel operation"]
            )
            self._log_decision(request, factors, result, override=True)
            return result
        
        # Calculate confidence score
        score = self.calculate_score(factors)
        
        # Apply thresholds
        if score >= self.THRESHOLD_PROCEED:
            result = DecisionResult(
                action=DecisionAction.PROCEED,
                score=score,
                reasoning=self._generate_reasoning(factors, "proceed")
            )
        elif score >= self.THRESHOLD_DEFAULT:
            result = DecisionResult(
                action=DecisionAction.DEFAULT,
                score=score,
                reasoning=self._generate_reasoning(factors, "default"),
                rationale="Using sensible default - can be adjusted later if needed"
            )
        else:
            result = DecisionResult(
                action=DecisionAction.ASK,
                score=score,
                reasoning=self._generate_reasoning(factors, "ask"),
                options=self._generate_options(request, context)
            )
        
        self._log_decision(request, factors, result)
        return result
    
    def _generate_reasoning(self, factors: DecisionFactors, action: str) -> str:
        """Generate human-readable reasoning for decision."""
        parts = []
        
        if factors.intent_clarity >= 0.8:
            parts.append("clear intent")
        elif factors.intent_clarity >= 0.5:
            parts.append("reasonable intent")
        else:
            parts.append("unclear intent")
        
        if factors.stakes_inverse >= 0.8:
            parts.append("low stakes")
        elif factors.stakes_inverse >= 0.5:
            parts.append("medium stakes")
        else:
            parts.append("high stakes")
        
        if factors.reversibility >= 0.8:
            parts.append("easily reversible")
        elif factors.reversibility >= 0.5:
            parts.append("moderately reversible")
        else:
            parts.append("hard to reverse")
        
        reasoning = f"Decision to {action}: {', '.join(parts)}"
        return reasoning
    
    def _generate_options(self, request: str, context: Optional[Dict]) -> List[str]:
        """Generate options when asking for clarification."""
        # This is a placeholder - in real implementation, would be more sophisticated
        return [
            "Option 1: Proceed with standard approach",
            "Option 2: Use alternative approach",
            "Option 3: Cancel and reconsider"
        ]
    
    def _log_decision(
        self,
        request: str,
        factors: DecisionFactors,
        result: DecisionResult,
        override: bool = False
    ):
        """Log decision for learning and analysis."""
        self.decision_history.append({
            'request': request,
            'factors': {
                'intent_clarity': factors.intent_clarity,
                'stakes_inverse': factors.stakes_inverse,
                'efficiency': factors.efficiency,
                'reversibility': factors.reversibility
            },
            'score': result.score,
            'action': result.action.value,
            'override': override,
            'reasoning': result.reasoning
        })
    
    def get_decision_history(self) -> List[Dict]:
        """Return decision history for analysis."""
        return self.decision_history
    
    def export_history(self, filepath: str):
        """Export decision history to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.decision_history, f, indent=2)


# Example usage and test cases
if __name__ == "__main__":
    agent = DecisionAgent()
    
    # Test Case 1: High confidence - proceed
    print("=" * 60)
    print("Test Case 1: Create config file")
    print("=" * 60)
    factors1 = DecisionFactors(
        intent_clarity=0.8,
        stakes_inverse=1.0,
        efficiency=1.0,
        reversibility=1.0
    )
    result1 = agent.make_decision("Create config file", factors1)
    print(f"Action: {result1.action.value}")
    print(f"Score: {result1.score}")
    print(f"Reasoning: {result1.reasoning}")
    print()
    
    # Test Case 2: Medium confidence - use default
    print("=" * 60)
    print("Test Case 2: Add logging")
    print("=" * 60)
    factors2 = DecisionFactors(
        intent_clarity=0.6,
        stakes_inverse=0.8,
        efficiency=0.5,
        reversibility=0.8
    )
    result2 = agent.make_decision("Add logging", factors2)
    print(f"Action: {result2.action.value}")
    print(f"Score: {result2.score}")
    print(f"Reasoning: {result2.reasoning}")
    if result2.rationale:
        print(f"Rationale: {result2.rationale}")
    print()
    
    # Test Case 3: Low confidence - ask
    print("=" * 60)
    print("Test Case 3: Optimize database")
    print("=" * 60)
    factors3 = DecisionFactors(
        intent_clarity=0.3,
        stakes_inverse=0.5,
        efficiency=0.0,
        reversibility=0.3
    )
    result3 = agent.make_decision("Optimize database", factors3)
    print(f"Action: {result3.action.value}")
    print(f"Score: {result3.score}")
    print(f"Reasoning: {result3.reasoning}")
    if result3.options:
        print("Options:")
        for option in result3.options:
            print(f"  - {option}")
    print()
    
    # Test Case 4: Safety override - always ask
    print("=" * 60)
    print("Test Case 4: Delete user data (safety override)")
    print("=" * 60)
    factors4 = DecisionFactors(
        intent_clarity=1.0,
        stakes_inverse=0.0,
        efficiency=1.0,
        reversibility=0.0
    )
    result4 = agent.make_decision("Delete user data", factors4)
    print(f"Action: {result4.action.value}")
    print(f"Score: {result4.score}")
    print(f"Reasoning: {result4.reasoning}")
    if result4.options:
        print("Options:")
        for option in result4.options:
            print(f"  - {option}")
    print()
    
    # Export decision history
    print("=" * 60)
    print("Decision History Summary")
    print("=" * 60)
    print(f"Total decisions: {len(agent.decision_history)}")
    for i, decision in enumerate(agent.decision_history, 1):
        print(f"{i}. {decision['request']}: {decision['action']} (score: {decision['score']})")
