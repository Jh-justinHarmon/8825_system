#!/usr/bin/env python3
"""
Merge Engine
Automatically merges new information into existing files
No backups, no logs - just merge and move on
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from openai import OpenAI


class MergeEngine:
    """
    Intelligent auto-merge of new content into existing files
    
    Philosophy: Build more, write less
    - No backups (git is your backup)
    - No logs (index is your audit trail)
    - Just merge and move on
    """
    
    def __init__(self, index_engine):
        self.index = index_engine
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # Use smart model for merging
    
    def check_similarity(self, new_file_hash: str, destination: str) -> Dict:
        """
        Check if new file content already exists in destination
        
        Returns:
            {
                'similar_files': [list of similar files],
                'best_match': {'file': path, 'score': float},
                'action': 'promote' | 'merge' | 'skip'
            }
        """
        
        # Get new file content
        new_content = self.index.get_full_content(new_file_hash)
        if not new_content:
            return {'action': 'skip', 'reason': 'content not found'}
        
        new_text = new_content.decode('utf-8', errors='ignore')[:3000]
        
        # Get new file metadata for smarter comparison
        metadata = self.index.get_metadata(new_file_hash)
        entities = json.loads(metadata.get('entities', '[]'))
        
        # Find files in destination with similar entities
        dest_path = Path(destination)
        if not dest_path.is_absolute():
            system_root = Path(__file__).parent.parent.parent
            dest_path = system_root / destination
        
        if not dest_path.exists():
            return {'action': 'promote', 'reason': 'destination empty'}
        
        existing_files = [f for f in dest_path.glob('**/*.md') if f.is_file()]
        
        if not existing_files:
            return {'action': 'promote', 'reason': 'no existing files'}
        
        # Quick filter: only compare files with overlapping entities
        candidates = []
        for existing_file in existing_files:
            existing_text = existing_file.read_text(errors='ignore')
            
            # Quick check: do they share entities?
            if any(entity.lower() in existing_text.lower() for entity in entities):
                candidates.append(existing_file)
        
        if not candidates:
            return {'action': 'promote', 'reason': 'no similar files'}
        
        # Compare with most likely candidate (first match)
        best_candidate = candidates[0]
        existing_text = best_candidate.read_text(errors='ignore')[:3000]
        
        # LLM comparison
        comparison = self._compare_content(new_text, existing_text, best_candidate.name)
        
        if comparison['score'] > 0.9:
            return {
                'action': 'skip',
                'reason': 'duplicate',
                'similar_files': [{'file': str(best_candidate), 'score': comparison['score']}]
            }
        elif comparison['score'] > 0.6:
            return {
                'action': 'merge',
                'best_match': {'file': best_candidate, 'score': comparison['score']},
                'new_info': comparison.get('new_information', 'Unknown')
            }
        else:
            return {'action': 'promote', 'reason': 'unique content'}
    
    def _compare_content(self, new_text: str, existing_text: str, existing_filename: str) -> Dict:
        """Quick LLM comparison"""
        
        prompt = f"""Compare these documents. Respond ONLY with JSON.

Document 1 (existing - {existing_filename}):
{existing_text}

Document 2 (new):
{new_text}

JSON format:
{{
    "score": 0.75,
    "new_information": "Brief description of what's new in doc 2"
}}

Score guide:
- 0.95+: Nearly identical
- 0.7-0.94: Significant overlap, some new info
- <0.7: Different content
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            # Clean JSON
            if result.startswith('```'):
                result = result.split('```')[1]
                if result.startswith('json'):
                    result = result[4:]
            
            return json.loads(result)
        except Exception as e:
            print(f"Comparison error: {e}")
            return {'score': 0.5, 'new_information': 'Unknown'}
    
    def auto_merge(self, new_file_hash: str, existing_file_path: Path) -> Dict:
        """
        Merge new content into existing file
        No backups, no logs - just do it
        
        For large files: only use first 10 pages (~5000 chars each)
        """
        
        # Get content
        new_content = self.index.get_full_content(new_file_hash)
        if not new_content:
            return {'status': 'error', 'reason': 'content not found'}
        
        new_text = new_content.decode('utf-8', errors='ignore')
        existing_text = existing_file_path.read_text(errors='ignore')
        
        # Chunk large files (max 10 pages = ~50,000 chars)
        MAX_CHARS = 50000
        
        if len(new_text) > MAX_CHARS:
            new_text = new_text[:MAX_CHARS] + "\n\n[... content truncated for merge ...]"
        
        if len(existing_text) > MAX_CHARS:
            existing_text = existing_text[:MAX_CHARS] + "\n\n[... content truncated for merge ...]"
        
        # LLM merge
        prompt = f"""Merge these documents intelligently. Output ONLY the merged content.

EXISTING DOCUMENT:
{existing_text}

NEW DOCUMENT (merge in):
{new_text}

Rules:
1. Keep ALL existing information
2. Add new information from NEW document
3. Maintain existing structure and formatting
4. If NEW has sections not in EXISTING, add them
5. If NEW has details for existing sections, enhance them
6. Update table of contents if present
7. NO explanations - just output the complete merged document
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical documentation editor. Output only the merged document."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=16000
            )
            
            merged_content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if LLM added them
            if merged_content.startswith('```'):
                merged_content = merged_content.split('```')[1]
                if merged_content.startswith('markdown'):
                    merged_content = merged_content[8:]
                merged_content = merged_content.strip()
            
            # Overwrite existing file
            existing_file_path.write_text(merged_content)
            
            return {
                'status': 'merged',
                'file': str(existing_file_path)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'reason': str(e)
            }


if __name__ == '__main__':
    from index_engine import ContentIndexEngine
    
    index = ContentIndexEngine()
    merge = MergeEngine(index)
    
    print("Merge Engine initialized")
    print("Ready to auto-merge content")
