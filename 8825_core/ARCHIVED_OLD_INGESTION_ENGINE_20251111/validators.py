#!/usr/bin/env python3
"""
Inbox Validators - Schema validation and auto-wrapping
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ValidationResult:
    """Result of validation check"""
    valid: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    auto_wrapped: bool = False
    data: Optional[Dict[str, Any]] = None


class InboxValidator:
    """Validates inbox files and auto-wraps non-JSON content"""
    
    REQUIRED_FIELDS = ['content_type', 'content', 'metadata']
    VALID_CONTENT_TYPES = [
        'mining_report', 'achievement', 'pattern', 
        'note', 'feature', 'decision'
    ]
    VALID_FOCUSES = ['joju', 'hcss', 'team76', 'jh']
    
    def validate_schema(self, file_path: str) -> ValidationResult:
        """
        Validate inbox file schema
        
        Hard fail: not JSON, missing required fields
        Soft fail: unknown content_type, missing target_focus
        """
        file_path = Path(file_path)
        
        # Check file exists
        if not file_path.exists():
            return ValidationResult(
                valid=False,
                error_type='file_not_found',
                error_message=f'File not found: {file_path}'
            )
        
        # If TXT, MD, DOCX, or PDF file, auto-wrap immediately
        if file_path.suffix.lower() in ['.txt', '.md', '.docx', '.pdf']:
            return self._try_auto_wrap(file_path)
        
        # Try to load JSON
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            # Try auto-wrap
            return self._try_auto_wrap(file_path)
        except Exception as e:
            return ValidationResult(
                valid=False,
                error_type='read_error',
                error_message=f'Error reading file: {str(e)}'
            )
        
        # Check required fields
        missing_fields = [f for f in self.REQUIRED_FIELDS if f not in data]
        if missing_fields:
            return ValidationResult(
                valid=False,
                error_type='missing_required_fields',
                error_message=f'Missing required fields: {", ".join(missing_fields)}'
            )
        
        # Validate content_type
        content_type = data.get('content_type', '')
        if content_type not in self.VALID_CONTENT_TYPES:
            # Soft fail - mark for human review
            return ValidationResult(
                valid=True,  # Allow through but flag
                error_type='unknown_content_type',
                error_message=f'Unknown content_type: {content_type}',
                data=data
            )
        
        # Validate target_focus (optional but recommended)
        target_focus = data.get('target_focus', '')
        if target_focus and target_focus not in self.VALID_FOCUSES:
            return ValidationResult(
                valid=True,  # Allow through but flag
                error_type='unknown_target_focus',
                error_message=f'Unknown target_focus: {target_focus}',
                data=data
            )
        
        # All good
        return ValidationResult(
            valid=True,
            data=data
        )
    
    def _try_auto_wrap(self, file_path: Path) -> ValidationResult:
        """
        Attempt to auto-wrap non-JSON content
        """
        try:
            # Handle DOCX files (binary format)
            if file_path.suffix.lower() == '.docx':
                try:
                    import docx
                    doc = docx.Document(str(file_path))
                    raw_text = '\n'.join([para.text for para in doc.paragraphs])
                except ImportError:
                    # If python-docx not available, treat as binary placeholder
                    raw_text = f"[DOCX file: {file_path.name} - requires python-docx for extraction]"
            # Handle PDF files (binary format)
            elif file_path.suffix.lower() == '.pdf':
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        raw_text = '\n'.join([page.extract_text() for page in pdf_reader.pages])
                except ImportError:
                    # If PyPDF2 not available, create placeholder
                    raw_text = f"[PDF file: {file_path.name} - requires PyPDF2 for extraction]"
                except Exception as e:
                    # PDF extraction failed, create placeholder with error
                    raw_text = f"[PDF file: {file_path.name} - extraction failed: {str(e)}]"
            else:
                # Handle text files (TXT, MD)
                with open(file_path, 'r') as f:
                    raw_text = f.read()
            
            wrapped = self.auto_wrap_text(raw_text, file_path.suffix.lower())
            
            return ValidationResult(
                valid=True,
                auto_wrapped=True,
                error_type='auto_wrapped',
                error_message='Non-JSON content auto-wrapped',
                data=wrapped
            )
        except Exception as e:
            return ValidationResult(
                valid=False,
                error_type='invalid_json',
                error_message=f'Invalid JSON and auto-wrap failed: {str(e)}'
            )
    
    def auto_wrap_text(self, raw_text: str, file_extension: str = '.txt') -> Dict[str, Any]:
        """
        Wrap non-JSON text in standard shell
        """
        format_map = {
            '.txt': 'text',
            '.md': 'markdown',
            '.docx': 'docx',
            '.pdf': 'pdf'
        }
        
        return {
            'content_type': 'note',
            'target_focus': 'jh',
            'content': {
                'text': raw_text,
                'auto_wrapped': True
            },
            'metadata': {
                'source': 'auto-wrapped',
                'timestamp': datetime.now().isoformat(),
                'original_format': format_map.get(file_extension, 'text')
            }
        }
    
    def validate_and_normalize(self, file_path: str) -> ValidationResult:
        """
        Validate and return normalized data
        """
        result = self.validate_schema(file_path)
        
        if not result.valid:
            return result
        
        # Normalize data
        data = result.data
        
        # Ensure metadata has timestamp
        if 'metadata' in data and 'timestamp' not in data['metadata']:
            data['metadata']['timestamp'] = datetime.now().isoformat()
        
        # Ensure target_focus exists (default to jh if missing)
        if 'target_focus' not in data or not data['target_focus']:
            data['target_focus'] = 'jh'
            result.error_type = 'missing_target_focus'
            result.error_message = 'target_focus missing, defaulted to jh'
        
        result.data = data
        return result


if __name__ == '__main__':
    # Test validator
    validator = InboxValidator()
    
    # Test auto-wrap
    wrapped = validator.auto_wrap_text("This is a test note")
    print("Auto-wrapped:", json.dumps(wrapped, indent=2))
