#!/usr/bin/env python3
"""
AI System-Wide Sweep - Find touchpoints, patterns, and conflicts
"""

import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from classifier import InboxItem


@dataclass
class Touchpoint:
    """A file/location that would be affected by the change"""
    file_path: str
    type: str  # workflow, protocol, agent, library
    relevance: float  # 0.0-1.0
    description: str


@dataclass
class RelatedPattern:
    """A similar pattern found elsewhere"""
    pattern_name: str
    location: str
    similarity: float  # 0.0-1.0
    context: str


@dataclass
class Conflict:
    """A potential conflict with existing patterns"""
    type: str  # override, duplicate, incompatible
    severity: str  # low, medium, high
    description: str
    affected_files: List[str]


@dataclass
class AISweepResult:
    """Result of system-wide AI sweep"""
    touchpoints: List[Touchpoint]
    related_patterns: List[RelatedPattern]
    conflicts: List[Conflict]
    blast_radius: str  # local, focus-wide, system-wide
    recommendation: str
    confidence: float


class PatternSearcher:
    """Search for patterns across workspace"""
    
    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent.parent
        
        self.workspace_root = Path(workspace_root)
        
        # Load critical rules
        config_path = Path(__file__).parent / 'config' / 'critical_rules.json'
        with open(config_path, 'r') as f:
            self.critical_rules = json.load(f)['critical_rules']
    
    def keyword_search(self, keywords: List[str], scope: str = 'all') -> List[str]:
        """
        Grep-based keyword search
        
        Scope: all, core, focuses, joju
        """
        search_paths = self._get_search_paths(scope)
        results = []
        
        # Exclusion patterns
        exclude_patterns = [
            'node_modules',
            '__pycache__',
            '.git',
            'venv',
            '.pyc',
            '.egg-info',
            'dist',
            'build'
        ]
        
        for keyword in keywords:
            for search_path in search_paths:
                try:
                    # Build grep command with exclusions
                    cmd = ['grep', '-r', '-l', '-i']
                    
                    # Add exclusions
                    for pattern in exclude_patterns:
                        cmd.extend(['--exclude-dir', pattern])
                    
                    cmd.extend([keyword, str(search_path)])
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        files = result.stdout.strip().split('\n')
                        results.extend([f for f in files if f])
                        
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
        
        # Deduplicate and make relative
        unique_results = list(set(results))
        
        # Filter out excluded patterns (double-check)
        filtered = []
        for f in unique_results:
            if not Path(f).exists():
                continue
            
            # Check if any exclude pattern is in path
            rel_path = str(Path(f).relative_to(self.workspace_root))
            if any(pattern in rel_path for pattern in exclude_patterns):
                continue
            
            filtered.append(rel_path)
        
        return filtered
    
    def check_critical_rules(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Check if change affects protected patterns
        """
        affected = []
        
        for rule in self.critical_rules:
            rule_path = self.workspace_root / rule['location']
            
            # Check if any keywords match rule name or location
            rule_text = f"{rule['name']} {rule['location']}".lower()
            
            for keyword in keywords:
                if keyword.lower() in rule_text:
                    affected.append({
                        'rule': rule['name'],
                        'location': rule['location'],
                        'reason': rule['reason'],
                        'protected': rule['protected']
                    })
                    break
        
        return affected
    
    def find_similar_files(self, content_type: str, target_focus: str) -> List[str]:
        """
        Find files with similar content_type in other focuses
        """
        results = []
        
        # Search in other focuses
        focuses = ['hcss', 'joju', 'team76']
        for focus in focuses:
            if focus == target_focus:
                continue
            
            focus_path = self.workspace_root / 'focuses' / focus
            if not focus_path.exists():
                continue
            
            # Look for similar content types
            pattern_files = list(focus_path.rglob(f'*{content_type}*'))
            results.extend([str(f.relative_to(self.workspace_root)) 
                          for f in pattern_files])
        
        return results
    
    def _get_search_paths(self, scope: str) -> List[Path]:
        """Get paths to search based on scope"""
        if scope == 'all':
            return [
                self.workspace_root / '8825_core',
                self.workspace_root / 'focuses',
                self.workspace_root / 'joju_sandbox'
            ]
        elif scope == 'core':
            return [self.workspace_root / '8825_core']
        elif scope == 'focuses':
            return [self.workspace_root / 'focuses']
        elif scope == 'joju':
            return [self.workspace_root / 'joju_sandbox']
        else:
            return [self.workspace_root]


class AISystemSweep:
    """Main AI sweep orchestrator"""
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.searcher = PatternSearcher(workspace_root)
        self.workspace_root = self.searcher.workspace_root
    
    def sweep(self, item: InboxItem) -> AISweepResult:
        """
        Run complete system-wide sweep
        
        Steps:
        1. Extract keywords from proposed change
        2. Find touchpoints (affected files)
        3. Find related patterns
        4. Detect conflicts
        5. Calculate blast radius
        6. Generate recommendation
        """
        # Extract keywords
        keywords = self._extract_keywords(item)
        
        # Find touchpoints
        touchpoints = self.find_touchpoints(item, keywords)
        
        # Find related patterns
        related = self.find_related_patterns(item, keywords)
        
        # Detect conflicts
        conflicts = self.detect_conflicts(item, touchpoints, related)
        
        # Calculate blast radius
        blast_radius = self.calculate_blast_radius(touchpoints)
        
        # Generate recommendation
        recommendation = self.generate_recommendation(item, conflicts, blast_radius)
        
        # Calculate confidence
        confidence = self._calculate_confidence(touchpoints, related, conflicts)
        
        return AISweepResult(
            touchpoints=touchpoints,
            related_patterns=related,
            conflicts=conflicts,
            blast_radius=blast_radius,
            recommendation=recommendation,
            confidence=confidence
        )
    
    def find_touchpoints(self, item: InboxItem, keywords: List[str]) -> List[Touchpoint]:
        """
        Find files/locations that would be affected
        """
        touchpoints = []
        
        # Keyword search
        found_files = self.searcher.keyword_search(keywords, scope='all')
        
        # Score and filter by relevance
        scored_files = []
        for file_path in found_files:
            file_type = self._classify_file_type(file_path)
            
            # Calculate relevance based on file type and location
            relevance = 0.5  # Base
            
            if file_type in ['workflow', 'protocol']:
                relevance = 0.8
            elif file_type == 'agent':
                relevance = 0.7
            elif file_type == 'library':
                relevance = 0.6
            
            # Boost for 8825_core
            if '8825_core' in file_path and 'inbox' not in file_path:
                relevance += 0.1
            
            # Boost for focus match
            if item.target_focus in file_path:
                relevance += 0.1
            
            scored_files.append((file_path, file_type, min(1.0, relevance)))
        
        # Sort by relevance and take top results
        scored_files.sort(key=lambda x: x[2], reverse=True)
        
        # Only include files with relevance > 0.6
        for file_path, file_type, relevance in scored_files[:10]:
            if relevance < 0.6:
                continue
            
            touchpoints.append(Touchpoint(
                file_path=file_path,
                type=file_type,
                relevance=relevance,
                description=f"Contains keywords: {', '.join(keywords[:3])}"
            ))
        
        # Check critical rules (always include)
        critical_affected = self.searcher.check_critical_rules(keywords)
        for rule in critical_affected:
            touchpoints.append(Touchpoint(
                file_path=rule['location'],
                type='protocol',
                relevance=1.0,  # Critical rules are highly relevant
                description=f"CRITICAL: {rule['reason']}"
            ))
        
        return touchpoints
    
    def find_related_patterns(self, item: InboxItem, keywords: List[str]) -> List[RelatedPattern]:
        """
        Find similar patterns in other focuses
        """
        related = []
        
        # Find similar files in other focuses
        similar_files = self.searcher.find_similar_files(
            item.content_type,
            item.target_focus
        )
        
        for file_path in similar_files[:5]:  # Top 5
            related.append(RelatedPattern(
                pattern_name=Path(file_path).stem,
                location=file_path,
                similarity=0.6,  # Placeholder - would use semantic similarity
                context=f"Similar {item.content_type} in different focus"
            ))
        
        return related
    
    def detect_conflicts(self, item: InboxItem, 
                        touchpoints: List[Touchpoint],
                        related: List[RelatedPattern]) -> List[Conflict]:
        """
        Detect potential conflicts
        """
        conflicts = []
        
        # Check for critical rule conflicts
        critical_touchpoints = [t for t in touchpoints if 'CRITICAL' in t.description]
        if critical_touchpoints:
            conflicts.append(Conflict(
                type='override',
                severity='high',
                description=f"Would affect {len(critical_touchpoints)} critical protected patterns",
                affected_files=[t.file_path for t in critical_touchpoints]
            ))
        
        # Check for duplicate patterns
        if len(related) > 2:
            conflicts.append(Conflict(
                type='duplicate',
                severity='medium',
                description=f"Similar patterns exist in {len(related)} other locations",
                affected_files=[r.location for r in related]
            ))
        
        # Check for scope mismatch
        if item.scope_intent == 'system-wide' and item.target_focus != 'jh':
            conflicts.append(Conflict(
                type='incompatible',
                severity='low',
                description="System-wide scope but focus-specific target",
                affected_files=[]
            ))
        
        return conflicts
    
    def calculate_blast_radius(self, touchpoints: List[Touchpoint]) -> str:
        """
        Calculate how wide the impact would be
        """
        if not touchpoints:
            return 'local'
        
        # Count unique directories affected
        dirs = set(str(Path(t.file_path).parent) for t in touchpoints)
        
        # Check if 8825_core is affected
        core_affected = any('8825_core' in t.file_path for t in touchpoints)
        
        if core_affected or len(dirs) > 5:
            return 'system-wide'
        elif len(dirs) > 2:
            return 'focus-wide'
        else:
            return 'local'
    
    def generate_recommendation(self, item: InboxItem, 
                                conflicts: List[Conflict],
                                blast_radius: str) -> str:
        """
        Generate AI recommendation
        """
        if not conflicts:
            return f"Safe to proceed. {blast_radius.title()} impact, no conflicts detected."
        
        high_severity = [c for c in conflicts if c.severity == 'high']
        
        if high_severity:
            return f"⚠️ CAUTION: {len(high_severity)} high-severity conflicts. Recommend refactoring existing patterns instead of adding new one."
        
        if blast_radius == 'system-wide':
            return "Consider narrowing scope to specific focus before implementing."
        
        return f"Proceed with review. {len(conflicts)} potential conflicts to address."
    
    def _extract_keywords(self, item: InboxItem) -> List[str]:
        """Extract meaningful keywords from item"""
        content_str = json.dumps(item.content).lower()
        
        # Common meaningful words in 8825 context
        keywords = []
        
        important_terms = [
            'workflow', 'protocol', 'agent', 'routing', 'auto-route',
            'tgif', 'hcss', 'joju', 'pattern', 'feature', 'inbox',
            'mcp', 'sync', 'validation', 'integration'
        ]
        
        for term in important_terms:
            if term in content_str:
                keywords.append(term)
        
        # Add content_type
        keywords.append(item.content_type)
        
        return keywords[:10]  # Limit to 10
    
    def _classify_file_type(self, file_path: str) -> str:
        """Classify file type based on path/name"""
        path_lower = file_path.lower()
        
        if 'workflow' in path_lower:
            return 'workflow'
        elif 'protocol' in path_lower:
            return 'protocol'
        elif 'agent' in path_lower:
            return 'agent'
        elif 'library' in path_lower or '.json' in path_lower:
            return 'library'
        else:
            return 'other'
    
    def _calculate_confidence(self, touchpoints: List[Touchpoint],
                             related: List[RelatedPattern],
                             conflicts: List[Conflict]) -> float:
        """Calculate confidence in sweep results"""
        # More touchpoints = higher confidence
        # More conflicts = lower confidence (uncertain situation)
        
        base_confidence = 0.5
        
        if touchpoints:
            base_confidence += min(len(touchpoints) * 0.05, 0.3)
        
        if conflicts:
            base_confidence -= min(len(conflicts) * 0.1, 0.2)
        
        return max(0.3, min(1.0, base_confidence))


if __name__ == '__main__':
    # Test AI sweep
    from classifier import InboxClassifier
    
    classifier = InboxClassifier()
    sweep = AISystemSweep()
    
    test_data = {
        'content_type': 'pattern',
        'target_focus': 'hcss',
        'content': {
            'title': 'New TGIF auto-route workflow',
            'description': 'Automatically route all Friday meetings to HCSS'
        },
        'metadata': {
            'source': 'chatgpt',
            'timestamp': '2025-11-08T16:00:00'
        }
    }
    
    item = classifier.classify(test_data, 'test.json')
    result = sweep.sweep(item)
    
    print(f"Touchpoints: {len(result.touchpoints)}")
    print(f"Related: {len(result.related_patterns)}")
    print(f"Conflicts: {len(result.conflicts)}")
    print(f"Blast radius: {result.blast_radius}")
    print(f"Recommendation: {result.recommendation}")
    print(f"Confidence: {result.confidence:.2f}")
