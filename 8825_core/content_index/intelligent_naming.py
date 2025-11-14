#!/usr/bin/env python3
"""
Intelligent Naming Engine
Uses LLM to analyze content and generate meaningful filenames
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from openai import OpenAI


class IntelligentNamingEngine:
    """
    LLM-powered content analysis and filename generation
    
    Features:
    - Reads and analyzes file content
    - Generates descriptive filenames
    - Extracts category and entities
    - Suggests destination folder
    """
    
    def __init__(self):
        # Get OpenAI API key from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Cheap model for naming
    
    def extract_text(self, file_path: Path, content: bytes) -> str:
        """Extract text from various file formats"""
        
        ext = file_path.suffix.lower()
        
        # Text files
        if ext in ['.txt', '.md']:
            return content.decode('utf-8', errors='ignore')
        
        # DOCX files
        if ext == '.docx':
            try:
                import docx
                doc = docx.Document(file_path)
                return '\n'.join([p.text for p in doc.paragraphs])
            except:
                return content.decode('utf-8', errors='ignore')
        
        # PDF files
        if ext == '.pdf':
            try:
                import PyPDF2
                from io import BytesIO
                pdf = PyPDF2.PdfReader(BytesIO(content))
                text = []
                for page in pdf.pages[:5]:  # First 5 pages
                    text.append(page.extract_text())
                return '\n'.join(text)
            except:
                return "PDF content (could not extract text)"
        
        # Default: try to decode as text
        return content.decode('utf-8', errors='ignore')
    
    def analyze_and_name(self, file_path: Path, content: bytes) -> Dict:
        """
        Analyze content and generate intelligent metadata
        WITH brain context for better decisions
        
        Returns:
            dict with suggested_filename, category, main_topic, entities, destination
        """
        
        # Load brain context
        brain_context = self._load_brain_context()
        
        # Extract text
        text = self.extract_text(file_path, content)
        
        # Truncate to reasonable length for LLM
        text_sample = text[:3000]
        
        # Build prompt with brain context
        prompt = f"""Analyze this document with context about the user's knowledge system.

SYSTEM CONTEXT:
{brain_context}

DOCUMENT TO ANALYZE:

Filename: {file_path.name}
Content (first 3000 chars):
{text_sample}

Provide metadata based on BOTH the document content AND the system context:
1. suggested_filename: Match naming patterns from existing files in the target focus
2. category: Use categories that already exist in the system
3. main_topic: Brief topic description (2-4 words)
4. entities: Key entities mentioned
5. destination: Best folder based on existing structure and similar files
6. reasoning: Brief explanation of why this destination based on context

Rules for filename:
- Be descriptive and specific
- Use underscores instead of spaces
- Keep it under 60 characters
- Include the original extension ({file_path.suffix})
- Examples: "RAL_Portal_API_Authentication_Guide.md", "HCSS_Meeting_Notes_2025_11_11.txt"

Rules for destination:
- Use destinations that exist in the system context
- If similar files exist, suggest the same destination
- Match the organizational structure shown in context

Respond ONLY with valid JSON, no other text:
{{
    "suggested_filename": "Descriptive_Name{file_path.suffix}",
    "category": "category",
    "main_topic": "topic",
    "entities": ["entity1", "entity2"],
    "destination": "path/to/folder/",
    "reasoning": "why this destination based on context"
}}"""
        
        try:
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a document analysis assistant. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
            
            metadata = json.loads(result_text)
            
            # Validate required fields (reasoning is optional)
            required = ['suggested_filename', 'category', 'main_topic', 'entities', 'destination']
            for field in required:
                if field not in metadata:
                    raise ValueError(f"Missing required field: {field}")
            
            # Reasoning is optional but helpful
            if 'reasoning' not in metadata:
                metadata['reasoning'] = 'No reasoning provided'
            
            # Ensure filename has extension
            if not metadata['suggested_filename'].endswith(file_path.suffix):
                metadata['suggested_filename'] += file_path.suffix
            
            return metadata
            
        except Exception as e:
            print(f"LLM naming error: {e}")
            
            # Fallback: simple naming based on content
            return self._fallback_naming(file_path, text_sample)
    
    def _load_brain_context(self) -> str:
        """
        Load brain context to inform naming decisions
        """
        
        brain_file = Path.home() / 'Downloads' / '8825_brain' / 'transport.json'
        
        if not brain_file.exists():
            return self._get_default_context()
        
        try:
            brain = json.loads(brain_file.read_text())
            
            # Build context from brain
            context_parts = []
            
            # Active focuses
            context_parts.append("ACTIVE FOCUSES:")
            context_parts.append("- focuses/hcss/knowledge/ - HCSS consulting, RAL Portal, Crunchtime")
            context_parts.append("- joju_sandbox/ - Personal achievements and contributions")
            context_parts.append("- focuses/team76/ - Team76 soccer content")
            context_parts.append("- users/justinharmon/personal/ - Personal notes and meetings")
            
            # Recent files (sample from knowledge base)
            context_parts.append("\nRECENT FILES IN HCSS:")
            hcss_path = Path(__file__).parent.parent.parent / 'focuses' / 'hcss' / 'knowledge'
            if hcss_path.exists():
                recent_files = list(hcss_path.glob('*.md'))[:10]
                for f in recent_files:
                    context_parts.append(f"  - {f.name}")
            
            # Naming patterns
            context_parts.append("\nNAMING PATTERNS:")
            context_parts.append("- Technical docs: Project_Name_Document_Type.md")
            context_parts.append("- API docs: Project_API_Component.md")
            context_parts.append("- Meeting notes: Project_Meeting_Notes_YYYY_MM_DD.md")
            
            return '\n'.join(context_parts)
            
        except Exception as e:
            print(f"Error loading brain context: {e}")
            return self._get_default_context()
    
    def _get_default_context(self) -> str:
        """Default context when brain not available"""
        return """
ACTIVE FOCUSES:
- focuses/hcss/knowledge/ - HCSS consulting, RAL Portal, Crunchtime technical docs
- joju_sandbox/ - Personal achievements and contributions  
- focuses/team76/ - Team76 soccer content
- users/justinharmon/personal/ - Personal notes and meetings

NAMING PATTERNS:
- Technical docs: Project_Name_Document_Type.md
- API docs: Project_API_Component.md
- Meeting notes: Project_Meeting_Notes_YYYY_MM_DD.md
"""
    
    def _fallback_naming(self, file_path: Path, text_sample: str) -> Dict:
        """Fallback naming when LLM fails"""
        
        # Simple keyword extraction
        keywords = []
        entities = []
        
        # Check for known entities
        entity_patterns = {
            'RAL Portal': ['ral portal', 'ral-portal'],
            'HCSS': ['hcss', 'hammer consulting'],
            'Crunchtime': ['crunchtime'],
            'Joju': ['joju'],
            'Team76': ['team76', 'team 76'],
            'OAuth': ['oauth'],
            'API': ['api', 'endpoint'],
            'Database': ['database', 'schema', 'erd']
        }
        
        text_lower = text_sample.lower()
        
        for entity, patterns in entity_patterns.items():
            if any(p in text_lower for p in patterns):
                entities.append(entity)
        
        # Determine category and destination
        if 'RAL Portal' in entities or 'HCSS' in entities:
            category = 'technical_documentation'
            destination = 'focuses/hcss/knowledge/'
            topic = 'HCSS Documentation'
        elif 'Joju' in entities:
            category = 'achievement'
            destination = 'joju_sandbox/'
            topic = 'Joju Content'
        elif 'Team76' in entities:
            category = 'sports'
            destination = 'focuses/team76/'
            topic = 'Team76 Content'
        else:
            category = 'note'
            destination = 'users/justinharmon/personal/'
            topic = 'Personal Note'
        
        # Generate simple filename
        if entities:
            name_parts = ['_'.join(entities[:2]), category]
        else:
            name_parts = [category, 'document']
        
        suggested_filename = '_'.join(name_parts) + file_path.suffix
        
        return {
            'suggested_filename': suggested_filename,
            'category': category,
            'main_topic': topic,
            'entities': entities,
            'destination': destination
        }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intelligent_naming.py <file_path>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    naming = IntelligentNamingEngine()
    content = file_path.read_bytes()
    
    print(f"Analyzing: {file_path.name}")
    print("="*80)
    
    metadata = naming.analyze_and_name(file_path, content)
    
    print(json.dumps(metadata, indent=2))
    
    print("\n" + "="*80)
    print(f"Suggested rename: {metadata['suggested_filename']}")
    print(f"Suggested location: {metadata['destination']}")
