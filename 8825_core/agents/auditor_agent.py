#!/usr/bin/env python3
"""
Auditor Agent - Meta-agent for validating workflow outputs

This agent validates automation results by:
1. Gathering exhaustive context from all available sources
2. Using evidence triangulation to assess accuracy
3. Detecting gaps (what was missed)
4. Generating improvement recommendations with efficiency trade-offs

Key Design Principles:
- Thoroughness over speed (auditor can be slow/expensive)
- Evidence triangulation (multiple sources = high confidence)
- Actionable recommendations (distinguish auditor vs automation approaches)
- Graceful degradation (partial audit if sources unavailable)
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class Verdict(Enum):
    """Audit verdict options"""
    PASS = "PASS"           # High confidence, no significant issues
    REVIEW = "REVIEW"       # Medium confidence or minor issues found
    FAIL = "FAIL"           # Low confidence or critical issues found


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "critical"   # Must fix
    HIGH = "high"           # Should fix
    MEDIUM = "medium"       # Nice to fix
    LOW = "low"             # Optional


@dataclass
class Evidence:
    """Evidence for a single output item"""
    item: Dict[str, Any]
    confirmations: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]
    absences: List[Dict[str, Any]]
    confidence: float
    verdict: str


@dataclass
class Gap:
    """Missing information detected in output"""
    item: Dict[str, Any]
    source: str
    severity: str
    reason: str
    confidence: float


@dataclass
class Recommendation:
    """Improvement recommendation"""
    issue_found: str
    auditor_approach: str
    automation_options: List[Dict[str, Any]]
    priority: str


class AuditorAgent:
    """
    Meta-agent that validates workflow outputs through exhaustive context gathering
    and evidence triangulation
    """
    
    # Context source mapping per workflow type
    CONTEXT_SOURCES = {
        "meeting_automation": [
            "gmail_otter_emails",
            "brain_transport",
            "tgif_knowledge_base",
            "calendar_events",
            "meeting_transcript"
        ],
        "email_processing": [
            "gmail_full_thread",
            "sender_history",
            "brain_learnings",
            "attachment_analysis"
        ],
        "screenshot_processing": [
            "original_screenshot",
            "ocr_full_output",
            "related_emails",
            "system_logs"
        ]
    }
    
    def __init__(self, verbose: bool = False, baseline_dir: Optional[str] = None):
        """
        Initialize auditor agent
        
        Args:
            verbose: Print detailed progress information
            baseline_dir: Directory to store baseline metrics (default: baselines/)
        """
        self.verbose = verbose
        self.audit_start_time = None
        self.context_sources_checked = []
        self.total_cost = 0.0
        
        # Baseline tracking
        if baseline_dir is None:
            baseline_dir = Path(__file__).parent / "baselines"
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        
    def audit_workflow(
        self,
        workflow_output: Dict[str, Any],
        workflow_type: str,
        source_materials: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main audit entry point
        
        Args:
            workflow_output: The output from the workflow to audit
            workflow_type: Type of workflow (e.g., 'meeting_automation')
            source_materials: Optional pre-loaded source materials
            metadata: Optional metadata about the workflow run
            
        Returns:
            Complete audit report
        """
        self.audit_start_time = datetime.now()
        
        if self.verbose:
            print(f"\n🔍 Starting audit of {workflow_type}")
            print(f"   Timestamp: {self.audit_start_time.isoformat()}")
        
        # Handle nested structure from meeting processor
        full_output = workflow_output
        if "processed_data" in workflow_output:
            if self.verbose:
                print(f"   Detected nested structure, extracting processed_data")
            workflow_output = workflow_output["processed_data"]
            
            # Extract transcript from original_data if available
            if source_materials is None:
                source_materials = {}
            
            if "original_data" in full_output:
                transcript = full_output["original_data"].get("transcript", "")
                if transcript and transcript.strip():
                    source_materials["meeting_transcript"] = {"text": transcript}
                    if self.verbose:
                        print(f"   Extracted transcript from original_data ({len(transcript)} chars)")
        
        # Step 1: Gather context
        context = self.gather_context(workflow_type, metadata or {}, source_materials)
        
        # Step 2: Compare and analyze
        findings = self.compare_and_analyze(workflow_output, context)
        
        # Step 3: Detect gaps
        gaps = self.detect_gaps(workflow_output, context)
        
        # Step 4: Generate recommendations
        recommendations = self.generate_recommendations(findings, gaps, workflow_type)
        
        # Step 5: Create audit report
        report = self.create_audit_report(
            workflow_output=workflow_output,
            findings=findings,
            gaps=gaps,
            recommendations=recommendations,
            context=context,
            metadata=metadata or {}
        )
        
        # Step 6: Baseline comparison
        baseline_file = self._get_baseline_file(workflow_type)
        
        if not baseline_file.exists():
            # First run - save as baseline
            self._save_baseline(report, workflow_type)
            if self.verbose:
                print(f"\n📊 Baseline metrics saved for future comparison")
        else:
            # Compare to baseline
            comparison = self._compare_to_baseline(report, workflow_type)
            if comparison:
                report['baseline_comparison'] = comparison
                if self.verbose:
                    print(f"\n📈 vs Baseline: {comparison['summary']}")
        
        if self.verbose:
            print(f"\n✅ Audit complete")
            print(f"   Duration: {report['audit_metadata']['duration_seconds']:.1f}s")
            print(f"   Verdict: {report['overall_assessment']['verdict']}")
        
        return report
    
    def gather_context(
        self,
        workflow_type: str,
        metadata: Dict[str, Any],
        source_materials: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Gather exhaustive context from all available sources
        
        Args:
            workflow_type: Type of workflow being audited
            metadata: Metadata about the workflow run
            source_materials: Pre-loaded source materials (optional)
            
        Returns:
            Dictionary of context from all sources
        """
        if self.verbose:
            print(f"\n📚 Gathering context for {workflow_type}...")
        
        context = {}
        
        # Get expected sources for this workflow type
        expected_sources = self.CONTEXT_SOURCES.get(workflow_type, [])
        
        if self.verbose:
            print(f"   Expected sources: {len(expected_sources)}")
        
        # Use pre-loaded materials if provided
        if source_materials:
            context.update(source_materials)
            if self.verbose:
                print(f"   Pre-loaded sources: {len(source_materials)}")
        
        # Fetch each source
        for source_name in expected_sources:
            if source_name in context:
                continue  # Already have it
                
            try:
                source_data = self._fetch_source(source_name, metadata)
                context[source_name] = source_data
                self.context_sources_checked.append(source_name)
                
                if self.verbose:
                    print(f"   ✅ {source_name}")
                    
            except Exception as e:
                context[source_name] = {
                    "error": str(e),
                    "status": "unavailable"
                }
                if self.verbose:
                    print(f"   ⚠️  {source_name}: {e}")
        
        # Check for critical gaps
        if self._has_critical_gaps(context, workflow_type):
            if self.verbose:
                print(f"\n⚠️  Critical context missing - may need user input")
        
        return context
    
    def _fetch_source(self, source_name: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch data from a specific source
        
        This is a placeholder that should be extended with actual integrations:
        - MCP inbox server for emails
        - Brain queries for learnings
        - Filesystem for cached data
        - API calls for live data
        
        Args:
            source_name: Name of the source to fetch
            metadata: Metadata that may contain references/IDs
            
        Returns:
            Source data
        """
        # Brain Transport (cached system context)
        if source_name == "brain_transport":
            brain_path = Path.home() / "Documents" / "8825_BRAIN_TRANSPORT.json"
            if brain_path.exists():
                with open(brain_path) as f:
                    return json.load(f)
            return {"status": "not_found"}
        
        # TGIF Knowledge Base
        if source_name == "tgif_knowledge_base":
            # Look for TGIF knowledge in 8825_files
            # Use absolute path from auditor_agent.py location, not CWD
            auditor_file = Path(__file__).resolve()  # Get absolute path of THIS file
            tgif_path = auditor_file.parent.parent.parent.parent / "8825_files" / "HCSS" / "TGIF_KNOWLEDGE.json"
            
            if tgif_path.exists():
                with open(tgif_path) as f:
                    return json.load(f)
            return {"status": "not_found"}
        
        # Gmail/Otter emails (original email data)
        if source_name == "gmail_otter_emails":
            gmail_id = metadata.get("gmail_id")
            if not gmail_id:
                return {"status": "no_gmail_id"}
            
            # Look in meeting_automation/data/raw/ folder
            auditor_file = Path(__file__).resolve()
            workflows_dir = auditor_file.parent.parent / "workflows" / "meeting_automation"
            raw_dir = workflows_dir / "data" / "raw"
            
            # Find file matching gmail_id
            import glob
            matching_files = list(raw_dir.glob(f"*{gmail_id}*.json"))
            
            if matching_files:
                with open(matching_files[0]) as f:
                    return json.load(f)
            
            return {"status": "not_found", "gmail_id": gmail_id}
        
        # Meeting transcript (from source materials)
        if source_name == "meeting_transcript":
            if "transcript_file" in metadata:
                transcript_path = Path(metadata["transcript_file"])
                if transcript_path.exists():
                    with open(transcript_path) as f:
                        return json.load(f)
            return {"status": "not_provided"}
        
        # Calendar events (future implementation)
        if source_name == "calendar_events":
            return {
                "status": "not_implemented",
                "note": "Calendar integration not yet implemented"
            }
        
        # Unknown source
        return {
            "status": "not_implemented",
            "note": f"Source '{source_name}' fetching not yet implemented"
        }
    
    def _has_critical_gaps(self, context: Dict[str, Any], workflow_type: str) -> bool:
        """
        Check if critical context sources are missing
        
        Args:
            context: Gathered context
            workflow_type: Type of workflow
            
        Returns:
            True if critical sources are unavailable
        """
        # For meeting automation, transcript is critical
        if workflow_type == "meeting_automation":
            transcript = context.get("meeting_transcript", {})
            if transcript.get("status") in ["not_found", "not_provided", "unavailable"]:
                return True
        
        return False
    
    def compare_and_analyze(
        self,
        workflow_output: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Evidence]:
        """
        Compare workflow output against gathered context using evidence triangulation
        
        Args:
            workflow_output: Output from the workflow
            context: Gathered context from all sources
            
        Returns:
            List of evidence findings for each output item
        """
        if self.verbose:
            print(f"\n🔬 Analyzing output against context...")
        
        findings = []
        
        # Extract corrections for correction-aware checking
        corrections = workflow_output.get('corrections_made', [])
        
        # Get key output sections to validate
        sections_to_check = self._identify_output_sections(workflow_output)
        
        for section_name, items in sections_to_check.items():
            if self.verbose:
                print(f"   Checking {section_name}: {len(items)} items")
            
            for item in items:
                evidence = self._check_item_against_context(item, context, section_name, corrections)
                findings.append(evidence)
        
        return findings
    
    def _identify_output_sections(self, workflow_output: Dict[str, Any]) -> Dict[str, List[Any]]:
        """
        Identify which sections of output to validate
        
        Args:
            workflow_output: The workflow output
            
        Returns:
            Dictionary mapping section names to lists of items
        """
        sections = {}
        
        # Common sections in meeting automation
        for section in ["decisions", "actions", "risks", "blockers", "issues_discussed"]:
            if section in workflow_output:
                items = workflow_output[section]
                if isinstance(items, list):
                    sections[section] = items
        
        # Corrections made
        if "corrections_made" in workflow_output:
            sections["corrections_made"] = workflow_output["corrections_made"]
        
        return sections
    
    def _check_item_against_context(
        self,
        item: Dict[str, Any],
        context: Dict[str, Any],
        section_name: str,
        corrections: List[Dict[str, Any]] = None
    ) -> Evidence:
        """
        Check a single output item against all context sources
        
        Args:
            item: The output item to check
            context: All gathered context
            section_name: Name of the section this item is from
            corrections: List of corrections made by automation
            
        Returns:
            Evidence object with confirmations, contradictions, absences
        """
        confirmations = []
        contradictions = []
        absences = []
        
        # Extract key text from item
        item_text = self._extract_item_text(item)
        
        # Find related corrections for this item
        related_corrections = self._find_related_corrections(item_text, corrections or [])
        
        # Check each context source
        for source_name, source_data in context.items():
            if isinstance(source_data, dict) and source_data.get("status") in ["unavailable", "not_found", "not_implemented"]:
                continue  # Skip unavailable sources
            
            # Use correction-aware checking if corrections exist
            if related_corrections:
                match_result = self._check_with_corrections(
                    item_text, source_data, source_name, related_corrections
                )
            else:
                match_result = self._check_source_for_item(item_text, source_data, source_name)
            
            if match_result["type"] == "confirmation":
                confirmations.append(match_result)
            elif match_result["type"] == "contradiction":
                contradictions.append(match_result)
            elif match_result["type"] == "absence":
                absences.append(match_result)
        
        # Calculate confidence score (boost if corrections validated)
        confidence = self._calculate_confidence(confirmations, contradictions, absences)
        
        # Boost confidence if we validated a correction
        correction_validated = False
        if related_corrections and confirmations:
            for confirmation in confirmations:
                if confirmation.get("correction_validated"):
                    confidence = min(1.0, confidence + 0.3)  # Larger bonus for validating corrections
                    correction_validated = True
                    break
        
        # Determine verdict (lower thresholds if correction validated)
        if correction_validated:
            # More lenient thresholds when we validated a correction
            if confidence >= 0.6:
                verdict = "high_confidence"
            elif confidence >= 0.4:
                verdict = "medium_confidence"
            else:
                verdict = "low_confidence"
        else:
            # Standard thresholds
            if confidence >= 0.8:
                verdict = "high_confidence"
            elif confidence >= 0.5:
                verdict = "medium_confidence"
            else:
                verdict = "low_confidence"
        
        return Evidence(
            item=item,
            confirmations=confirmations,
            contradictions=contradictions,
            absences=absences,
            confidence=confidence,
            verdict=verdict
        )
    
    def _extract_item_text(self, item: Dict[str, Any]) -> str:
        """
        Extract searchable text from an item
        
        Args:
            item: The item to extract text from
            
        Returns:
            Combined text string
        """
        text_parts = []
        
        # Common text fields
        for field in ["text", "what", "topic", "original", "corrected", "description"]:
            if field in item:
                text_parts.append(str(item[field]))
        
        return " ".join(text_parts).lower()
    
    def _check_source_for_item(
        self,
        item_text: str,
        source_data: Any,
        source_name: str
    ) -> Dict[str, Any]:
        """
        Check if a source confirms, contradicts, or is silent about an item
        
        Args:
            item_text: Text to search for
            source_data: The source data
            source_name: Name of the source
            
        Returns:
            Match result dictionary
        """
        # Convert source to searchable text
        source_text = self._source_to_text(source_data)
        source_lower = source_text.lower()
        item_lower = item_text.lower()
        
        # Strategy 1: Phrase matching (most reliable)
        # Extract phrases (2-4 words) from item
        phrases = self._extract_phrases(item_text)
        phrase_matches = sum(1 for phrase in phrases if phrase.lower() in source_lower)
        
        # Strategy 2: Proper noun matching (names, places, systems)
        proper_nouns = self._extract_proper_nouns(item_text)
        noun_matches = sum(1 for noun in proper_nouns if self._fuzzy_match(noun, source_lower))
        
        # Strategy 3: Keyword matching (fallback)
        keywords = [word for word in item_text.split() if len(word) > 3]
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in source_lower)
        
        # Calculate combined score
        total_phrases = len(phrases) if phrases else 1
        total_nouns = len(proper_nouns) if proper_nouns else 1
        total_keywords = len(keywords) if keywords else 1
        
        phrase_score = phrase_matches / total_phrases
        noun_score = noun_matches / total_nouns
        keyword_score = keyword_matches / total_keywords
        
        # Weighted scoring (phrases most important, then nouns, then keywords)
        combined_score = (phrase_score * 0.5) + (noun_score * 0.3) + (keyword_score * 0.2)
        
        if combined_score >= 0.4:  # 40% threshold (more lenient)
            return {
                "type": "confirmation",
                "source": source_name,
                "match_strength": combined_score,
                "excerpt": self._extract_excerpt(source_text, phrases[:2] if phrases else keywords[:3]),
                "matches": {
                    "phrases": f"{phrase_matches}/{total_phrases}",
                    "nouns": f"{noun_matches}/{total_nouns}",
                    "keywords": f"{keyword_matches}/{total_keywords}"
                }
            }
        elif combined_score > 0.1:
            return {
                "type": "partial",
                "source": source_name,
                "match_strength": combined_score
            }
        else:
            return {
                "type": "absence",
                "source": source_name,
                "note": "No matching content found"
            }
    
    def _source_to_text(self, source_data: Any) -> str:
        """
        Convert source data to searchable text
        
        Args:
            source_data: Source data (can be dict, list, string, etc.)
            
        Returns:
            Text representation
        """
        if isinstance(source_data, str):
            return source_data
        elif isinstance(source_data, dict):
            return json.dumps(source_data)
        elif isinstance(source_data, list):
            return " ".join(str(item) for item in source_data)
        else:
            return str(source_data)
    
    def _extract_phrases(self, text: str, min_words: int = 2, max_words: int = 4) -> List[str]:
        """
        Extract meaningful phrases from text
        
        Args:
            text: Text to extract from
            min_words: Minimum words per phrase
            max_words: Maximum words per phrase
            
        Returns:
            List of phrases
        """
        words = text.split()
        phrases = []
        
        for n in range(min_words, max_words + 1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i+n])
                # Skip if all words are short (likely not meaningful)
                if all(len(w) > 2 for w in words[i:i+n]):
                    phrases.append(phrase)
        
        return phrases
    
    def _extract_proper_nouns(self, text: str) -> List[str]:
        """
        Extract likely proper nouns (capitalized words/phrases)
        
        Args:
            text: Text to extract from
            
        Returns:
            List of proper nouns
        """
        import re
        # Find capitalized words (but not at start of sentence)
        # Pattern: word boundary, capital letter, lowercase letters
        pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        matches = re.findall(pattern, text)
        
        # Also look for all-caps acronyms
        acronym_pattern = r'\b[A-Z]{2,}\b'
        acronyms = re.findall(acronym_pattern, text)
        
        return matches + acronyms
    
    def _find_related_corrections(self, item_text: str, corrections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find corrections that relate to this item
        
        Args:
            item_text: Text from the item
            corrections: List of all corrections
            
        Returns:
            List of related corrections
        """
        related = []
        item_lower = item_text.lower()
        
        for correction in corrections:
            corrected = correction.get('corrected', '').lower()
            original = correction.get('original', '').lower()
            
            # Check if corrected term appears in item
            if corrected and corrected in item_lower:
                related.append(correction)
            # Also check if original appears (less common but possible)
            elif original and original in item_lower:
                related.append(correction)
        
        return related
    
    def _check_with_corrections(
        self,
        item_text: str,
        source_data: Any,
        source_name: str,
        corrections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check item against source, accounting for corrections
        
        Args:
            item_text: Text to search for
            source_data: Source data
            source_name: Name of source
            corrections: Related corrections
            
        Returns:
            Match result with correction awareness
        """
        source_text = self._source_to_text(source_data)
        source_lower = source_text.lower()
        
        # Check if ORIGINAL terms exist in source (they should!)
        original_found = False
        corrected_found = False
        
        for correction in corrections:
            original = correction.get('original', '')
            corrected = correction.get('corrected', '')
            
            # Check for original with fuzzy matching (transcription errors)
            if original and self._fuzzy_match(original, source_lower, threshold=0.7):
                original_found = True
            
            # Check for corrected (might already be correct)
            if corrected and corrected.lower() in source_lower:
                corrected_found = True
        
        # Scoring logic
        if original_found and not corrected_found:
            # Best case: automation fixed a real error
            return {
                "type": "confirmation",
                "source": source_name,
                "match_strength": 0.9,
                "correction_validated": True,
                "note": "Found original term (before correction) in source - validates automation fix",
                "excerpt": self._extract_excerpt(source_text, [c.get('original', '') for c in corrections])
            }
        elif corrected_found:
            # Already correct in source
            return {
                "type": "confirmation",
                "source": source_name,
                "match_strength": 0.7,
                "note": "Found corrected term in source - was already correct",
                "excerpt": self._extract_excerpt(source_text, [c.get('corrected', '') for c in corrections])
            }
        else:
            # Neither found - possible hallucination or missing context
            return {
                "type": "absence",
                "source": source_name,
                "note": "Neither original nor corrected term found - needs review"
            }
    
    def _fuzzy_match(self, term: str, text: str, threshold: float = 0.8) -> bool:
        """
        Check if term appears in text with fuzzy matching
        
        Args:
            term: Term to search for
            text: Text to search in
            threshold: Similarity threshold (0-1)
            
        Returns:
            True if fuzzy match found
        """
        from difflib import SequenceMatcher
        
        term_lower = term.lower()
        text_lower = text.lower()
        
        # Exact match
        if term_lower in text_lower:
            return True
        
        # Fuzzy match - check against sliding window
        term_len = len(term_lower)
        if term_len == 0:
            return False
            
        for i in range(len(text_lower) - term_len + 1):
            window = text_lower[i:i + term_len]
            similarity = SequenceMatcher(None, term_lower, window).ratio()
            if similarity >= threshold:
                return True
        
        return False
    
    def _extract_excerpt(self, text: str, keywords: List[str], context_chars: int = 100) -> str:
        """
        Extract excerpt around keywords
        
        Args:
            text: Full text
            keywords: Keywords to find
            context_chars: Characters of context around keyword
            
        Returns:
            Excerpt string
        """
        text_lower = text.lower()
        for keyword in keywords:
            keyword_str = str(keyword).lower()
            pos = text_lower.find(keyword_str)
            if pos != -1:
                start = max(0, pos - context_chars)
                end = min(len(text), pos + len(keyword_str) + context_chars)
                return "..." + text[start:end] + "..."
        return ""
    
    def _calculate_confidence(
        self,
        confirmations: List[Dict[str, Any]],
        contradictions: List[Dict[str, Any]],
        absences: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate confidence score using evidence triangulation
        
        Multiple sources confirming = high confidence
        Contradictions = low confidence
        
        Args:
            confirmations: List of confirming sources
            contradictions: List of contradicting sources
            absences: List of sources that should mention but don't
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Base score from confirmations
        confirmation_score = min(len(confirmations) * 0.3, 0.9)
        
        # Penalty for contradictions
        contradiction_penalty = len(contradictions) * 0.4
        
        # Small penalty for absences
        absence_penalty = len(absences) * 0.05
        
        # Calculate final score
        score = max(0.0, min(1.0, confirmation_score - contradiction_penalty - absence_penalty))
        
        return round(score, 2)
    
    def detect_gaps(
        self,
        workflow_output: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Gap]:
        """
        Detect what's in context but missing from output
        
        Args:
            workflow_output: The workflow output
            context: Gathered context
            
        Returns:
            List of detected gaps
        """
        if self.verbose:
            print(f"\n🔍 Detecting gaps...")
        
        gaps = []
        
        # This is a simplified gap detection
        # In production, would use more sophisticated NLP/extraction
        
        # For now, just note if we have context but output is sparse
        output_sections = self._identify_output_sections(workflow_output)
        
        for section_name, items in output_sections.items():
            if len(items) == 0:
                gaps.append(Gap(
                    item={"section": section_name},
                    source="workflow_output",
                    severity=Severity.MEDIUM.value,
                    reason=f"Section '{section_name}' is empty",
                    confidence=0.5
                ))
        
        return gaps
    
    def generate_recommendations(
        self,
        findings: List[Evidence],
        gaps: List[Gap],
        workflow_type: str
    ) -> List[Recommendation]:
        """
        Generate improvement recommendations with efficiency trade-offs
        
        Args:
            findings: Evidence findings
            gaps: Detected gaps
            workflow_type: Type of workflow
            
        Returns:
            List of recommendations
        """
        if self.verbose:
            print(f"\n💡 Generating recommendations...")
        
        recommendations = []
        
        # Analyze low-confidence findings
        low_confidence = [f for f in findings if f.confidence < 0.6]
        
        if low_confidence:
            recommendations.append(Recommendation(
                issue_found=f"Found {len(low_confidence)} items with low confidence",
                auditor_approach="Checked multiple context sources, found insufficient confirmation",
                automation_options=[
                    {
                        "approach": "Add confidence threshold to workflow",
                        "impact": "Flag low-confidence extractions for manual review",
                        "cost": "Minimal (add confidence scoring)",
                        "trade_off": "Requires manual review of flagged items"
                    },
                    {
                        "approach": "Enhance context in workflow",
                        "impact": "Provide more context to extraction model",
                        "cost": "Medium (more tokens per run)",
                        "trade_off": "Slower, more expensive, but more accurate"
                    }
                ],
                priority=Severity.HIGH.value
            ))
        
        # Analyze gaps
        critical_gaps = [g for g in gaps if g.severity == Severity.CRITICAL.value]
        
        if critical_gaps:
            recommendations.append(Recommendation(
                issue_found=f"Found {len(critical_gaps)} critical gaps in output",
                auditor_approach="Compared context sources to output, found missing items",
                automation_options=[
                    {
                        "approach": "Add explicit extraction for missing categories",
                        "impact": "Ensure all expected sections are populated",
                        "cost": "Low (add to prompt template)",
                        "trade_off": "May extract empty sections if not present"
                    }
                ],
                priority=Severity.CRITICAL.value
            ))
        
        return recommendations
    
    def create_audit_report(
        self,
        workflow_output: Dict[str, Any],
        findings: List[Evidence],
        gaps: List[Gap],
        recommendations: List[Recommendation],
        context: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create comprehensive audit report
        
        Args:
            workflow_output: Original workflow output
            findings: Evidence findings
            gaps: Detected gaps
            recommendations: Improvement recommendations
            context: Gathered context
            metadata: Workflow metadata
            
        Returns:
            Complete audit report
        """
        audit_duration = (datetime.now() - self.audit_start_time).total_seconds()
        
        # Calculate overall scores
        accuracy_score = self._calculate_accuracy_score(findings)
        completeness_score = self._calculate_completeness_score(gaps)
        overall_confidence = sum(f.confidence for f in findings) / len(findings) if findings else 0.0
        
        # Determine verdict
        if accuracy_score >= 0.8 and completeness_score >= 0.8:
            verdict = Verdict.PASS.value
        elif accuracy_score >= 0.6 or completeness_score >= 0.6:
            verdict = Verdict.REVIEW.value
        else:
            verdict = Verdict.FAIL.value
        
        # Count available sources
        available_sources = sum(
            1 for source_data in context.values()
            if not (isinstance(source_data, dict) and source_data.get("status") in ["unavailable", "not_found", "not_implemented"])
        )
        
        report = {
            "audit_metadata": {
                "workflow_type": metadata.get("workflow_type", "unknown"),
                "workflow_id": metadata.get("workflow_id", "unknown"),
                "audit_date": self.audit_start_time.isoformat(),
                "sources_checked": len(self.context_sources_checked),
                "sources_available": available_sources,
                "total_sources": len(context),
                "duration_seconds": round(audit_duration, 2),
                "auditor_version": "1.0.0"
            },
            
            "overall_assessment": {
                "verdict": verdict,
                "accuracy_score": round(accuracy_score, 2),
                "completeness_score": round(completeness_score, 2),
                "confidence": round(overall_confidence, 2),
                "total_items_checked": len(findings),
                "gaps_found": len(gaps),
                "recommendations_count": len(recommendations)
            },
            
            "findings": {
                "high_confidence": [asdict(f) for f in findings if f.confidence >= 0.8],
                "medium_confidence": [asdict(f) for f in findings if 0.5 <= f.confidence < 0.8],
                "low_confidence": [asdict(f) for f in findings if f.confidence < 0.5]
            },
            
            "gaps": [asdict(g) for g in gaps],
            
            "recommendations": [asdict(r) for r in recommendations],
            
            "context_analysis": {
                "sources_used": list(context.keys()),
                "sources_available": available_sources,
                "sources_unavailable": [
                    name for name, data in context.items()
                    if isinstance(data, dict) and data.get("status") in ["unavailable", "not_found", "not_implemented"]
                ],
                "triangulation_coverage": self._calculate_triangulation_coverage(findings)
            }
        }
        
        return report
    
    def _calculate_accuracy_score(self, findings: List[Evidence]) -> float:
        """Calculate overall accuracy score from findings"""
        if not findings:
            return 0.0
        
        total_confidence = sum(f.confidence for f in findings)
        return total_confidence / len(findings)
    
    def _calculate_completeness_score(self, gaps: List[Gap]) -> float:
        """Calculate completeness score (inverse of gaps)"""
        # Simplified: fewer gaps = higher score
        # In production, would weight by severity
        if not gaps:
            return 1.0
        
        critical_gaps = sum(1 for g in gaps if g.severity == Severity.CRITICAL.value)
        high_gaps = sum(1 for g in gaps if g.severity == Severity.HIGH.value)
        
        # Heavy penalty for critical, medium for high
        penalty = (critical_gaps * 0.3) + (high_gaps * 0.15)
        
        return max(0.0, 1.0 - penalty)
    
    def _calculate_triangulation_coverage(self, findings: List[Evidence]) -> str:
        """Calculate what % of findings were validated by 2+ sources"""
        if not findings:
            return "0%"
        
        multi_source = sum(1 for f in findings if len(f.confirmations) >= 2)
        percentage = (multi_source / len(findings)) * 100
        
        return f"{percentage:.0f}%"
    
    def _get_baseline_file(self, workflow_type: str) -> Path:
        """Get path to baseline file for workflow type"""
        return self.baseline_dir / f"baseline_{workflow_type}.json"
    
    def _save_baseline(self, report: Dict[str, Any], workflow_type: str):
        """Save current audit as baseline for future comparison"""
        baseline_file = self._get_baseline_file(workflow_type)
        
        baseline = {
            "workflow_type": workflow_type,
            "baseline_date": self.audit_start_time.isoformat(),
            "baseline_metrics": {
                "accuracy": report["overall_assessment"]["accuracy_score"],
                "confidence": report["overall_assessment"]["confidence"],
                "completeness": report["overall_assessment"]["completeness_score"],
                "sources_available": report["audit_metadata"]["sources_available"],
                "sources_total": report["audit_metadata"]["sources_checked"],
                "high_confidence_items": len(report["findings"]["high_confidence"]),
                "medium_confidence_items": len(report["findings"]["medium_confidence"]),
                "low_confidence_items": len(report["findings"]["low_confidence"]),
                "total_items": report["overall_assessment"]["total_items_checked"]
            },
            "baseline_audit_file": f"audit_{workflow_type}_{self.audit_start_time.strftime('%Y%m%d_%H%M%S')}.json"
        }
        
        with open(baseline_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        if self.verbose:
            print(f"\n📊 Baseline metrics saved: {baseline_file}")
    
    def _compare_to_baseline(self, report: Dict[str, Any], workflow_type: str) -> Dict[str, Any]:
        """Compare current audit to baseline"""
        baseline_file = self._get_baseline_file(workflow_type)
        
        if not baseline_file.exists():
            return None
        
        with open(baseline_file) as f:
            baseline = json.load(f)
        
        baseline_metrics = baseline["baseline_metrics"]
        current_metrics = {
            "accuracy": report["overall_assessment"]["accuracy_score"],
            "confidence": report["overall_assessment"]["confidence"],
            "completeness": report["overall_assessment"]["completeness_score"],
            "sources_available": report["audit_metadata"]["sources_available"],
            "sources_total": report["audit_metadata"]["sources_checked"],
            "high_confidence_items": len(report["findings"]["high_confidence"]),
            "medium_confidence_items": len(report["findings"]["medium_confidence"]),
            "low_confidence_items": len(report["findings"]["low_confidence"]),
            "total_items": report["overall_assessment"]["total_items_checked"]
        }
        
        # Calculate changes
        accuracy_change = current_metrics["accuracy"] - baseline_metrics["accuracy"]
        confidence_change = current_metrics["confidence"] - baseline_metrics["confidence"]
        sources_change = current_metrics["sources_available"] - baseline_metrics["sources_available"]
        high_conf_change = current_metrics["high_confidence_items"] - baseline_metrics["high_confidence_items"]
        
        # Build improvements list
        improvements = []
        if accuracy_change > 0:
            improvements.append(f"Accuracy improved by {accuracy_change:.0%}")
        if confidence_change > 0:
            improvements.append(f"Confidence increased by {confidence_change:.2f}")
        if sources_change > 0:
            improvements.append(f"Added {sources_change} new context source(s)")
        if high_conf_change > 0:
            improvements.append(f"High confidence items increased by {high_conf_change}")
        
        # Build regressions list
        regressions = []
        if accuracy_change < 0:
            regressions.append(f"Accuracy decreased by {abs(accuracy_change):.0%}")
        if confidence_change < 0:
            regressions.append(f"Confidence decreased by {abs(confidence_change):.2f}")
        if sources_change < 0:
            regressions.append(f"Lost {abs(sources_change)} context source(s)")
        if high_conf_change < 0:
            regressions.append(f"High confidence items decreased by {abs(high_conf_change)}")
        
        comparison = {
            "baseline_date": baseline["baseline_date"],
            "baseline_audit_file": baseline["baseline_audit_file"],
            "changes": {
                "accuracy": {
                    "baseline": baseline_metrics["accuracy"],
                    "current": current_metrics["accuracy"],
                    "change": accuracy_change,
                    "change_percent": f"{accuracy_change:.0%}" if baseline_metrics["accuracy"] > 0 else "N/A"
                },
                "confidence": {
                    "baseline": baseline_metrics["confidence"],
                    "current": current_metrics["confidence"],
                    "change": confidence_change
                },
                "sources_available": {
                    "baseline": baseline_metrics["sources_available"],
                    "current": current_metrics["sources_available"],
                    "change": sources_change
                },
                "high_confidence_items": {
                    "baseline": baseline_metrics["high_confidence_items"],
                    "current": current_metrics["high_confidence_items"],
                    "change": high_conf_change
                }
            },
            "improvements": improvements,
            "regressions": regressions,
            "summary": self._generate_comparison_summary(improvements, regressions)
        }
        
        return comparison
    
    def _generate_comparison_summary(self, improvements: List[str], regressions: List[str]) -> str:
        """Generate human-readable comparison summary"""
        if not improvements and not regressions:
            return "No significant changes from baseline"
        
        if improvements and not regressions:
            return f"✅ {len(improvements)} improvement(s): " + "; ".join(improvements[:2])
        
        if regressions and not improvements:
            return f"⚠️ {len(regressions)} regression(s): " + "; ".join(regressions[:2])
        
        return f"Mixed: {len(improvements)} improvement(s), {len(regressions)} regression(s)"


def main():
    """Test the auditor agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit workflow outputs")
    parser.add_argument("--output-file", required=True, help="Path to workflow output JSON")
    parser.add_argument("--workflow-type", required=True, help="Type of workflow")
    parser.add_argument("--metadata", help="Optional metadata JSON file")
    parser.add_argument("--report-dir", default="audits", help="Directory to save audit reports")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Load workflow output
    with open(args.output_file) as f:
        workflow_output = json.load(f)
    
    # Load metadata if provided
    metadata = {}
    if args.metadata:
        with open(args.metadata) as f:
            metadata = json.load(f)
    
    # Extract gmail_id from workflow output if not in metadata
    if "gmail_id" not in metadata:
        # Check in original_data (for meeting automation)
        if "original_data" in workflow_output:
            gmail_id = workflow_output["original_data"].get("gmail_id")
            if gmail_id:
                metadata["gmail_id"] = gmail_id
        # Check in processing_metadata
        elif "processing_metadata" in workflow_output:
            gmail_id = workflow_output["processing_metadata"].get("gmail_id")
            if gmail_id:
                metadata["gmail_id"] = gmail_id
    
    # Create auditor
    auditor = AuditorAgent(verbose=args.verbose)
    
    # Run audit
    report = auditor.audit_workflow(
        workflow_output=workflow_output,
        workflow_type=args.workflow_type,
        metadata=metadata
    )
    
    # Save report
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"audit_{args.workflow_type}_{timestamp}.json"
    
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Audit report saved: {report_file}")
    print(f"\n{'='*60}")
    print(f"VERDICT: {report['overall_assessment']['verdict']}")
    print(f"Accuracy: {report['overall_assessment']['accuracy_score']:.0%}")
    print(f"Completeness: {report['overall_assessment']['completeness_score']:.0%}")
    print(f"{'='*60}")
    
    # Exit code based on verdict
    sys.exit(0 if report['overall_assessment']['verdict'] == Verdict.PASS.value else 1)


if __name__ == "__main__":
    main()
