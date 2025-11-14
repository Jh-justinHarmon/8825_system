#!/usr/bin/env python3
"""
Philosophy Document Validator

Validates PHILOSOPHY.md structure and format to prevent parser errors.

Usage:
    python3 philosophy_validator.py
    
    # Or import
    from philosophy_validator import validate_philosophy
    is_valid, errors = validate_philosophy()
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict

class PhilosophyValidator:
    """Validate PHILOSOPHY.md structure and format"""
    
    def __init__(self, philosophy_path: Path = None):
        if philosophy_path is None:
            philosophy_path = Path(__file__).parent.parent.parent / "PHILOSOPHY.md"
        
        self.philosophy_path = philosophy_path
        self.errors = []
        self.warnings = []
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Validate philosophy document
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Check file exists
        if not self.philosophy_path.exists():
            self.errors.append(f"File not found: {self.philosophy_path}")
            return False, self.errors, self.warnings
        
        try:
            content = self.philosophy_path.read_text()
        except Exception as e:
            self.errors.append(f"Cannot read file: {e}")
            return False, self.errors, self.warnings
        
        # Run validation checks
        self._validate_structure(content)
        self._validate_principles(content)
        self._validate_metadata(content)
        self._validate_markdown(content)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_structure(self, content: str):
        """Validate document structure"""
        required_sections = [
            "# 8825 Philosophy",
            "## Architecture Position",
            "## Iron-Clad Principles",
            "## Learned Principles",
            "## Usage Notes"
        ]
        
        for section in required_sections:
            if section not in content:
                self.errors.append(f"Missing required section: {section}")
    
    def _validate_principles(self, content: str):
        """Validate principle format"""
        lines = content.split('\n')
        
        in_principle = False
        principle_name = None
        has_metadata = False
        has_status = False
        
        for i, line in enumerate(lines, 1):
            # Detect principle start
            if re.match(r'^###\s+\d+\.\s+', line):
                # Check previous principle had required metadata
                if in_principle and principle_name:
                    if not has_metadata:
                        self.warnings.append(f"Line {i-1}: Principle '{principle_name}' missing metadata section")
                    if not has_status:
                        self.warnings.append(f"Line {i-1}: Principle '{principle_name}' missing **Status:** field")
                
                # Start new principle
                in_principle = True
                principle_name = line.strip()
                has_metadata = False
                has_status = False
            
            # Check for metadata markers
            if in_principle:
                if '**Added:**' in line or '**Use Count:**' in line or '**Last Used:**' in line:
                    has_metadata = True
                if '**Status:**' in line:
                    has_status = True
                    # Validate status value
                    status_match = re.search(r'\*\*Status:\*\*\s+([\w-]+)', line)
                    if status_match:
                        status = status_match.group(1)
                        valid_statuses = ['Active', 'Promoted', 'Decaying', 'Deprecated', 'Iron-Clad']
                        if status not in valid_statuses:
                            self.errors.append(f"Line {i}: Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}")
    
    def _validate_metadata(self, content: str):
        """Validate metadata format"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check Added date format
            if '**Added:**' in line:
                date_match = re.search(r'\*\*Added:\*\*\s+(\S+)', line)
                if date_match:
                    date_str = date_match.group(1)
                    if not re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                        self.errors.append(f"Line {i}: Invalid date format '{date_str}'. Expected YYYY-MM-DD")
            
            # Check Use Count format
            if '**Use Count:**' in line:
                count_match = re.search(r'\*\*Use Count:\*\*\s+(\d+)', line)
                if not count_match:
                    self.errors.append(f"Line {i}: Invalid Use Count format. Expected number")
            
            # Check Last Used format
            if '**Last Used:**' in line:
                date_match = re.search(r'\*\*Last Used:\*\*\s+(\S+)', line)
                if date_match:
                    date_str = date_match.group(1)
                    if date_str != 'Never' and not re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                        self.errors.append(f"Line {i}: Invalid Last Used format '{date_str}'. Expected YYYY-MM-DD or 'Never'")
    
    def _validate_markdown(self, content: str):
        """Validate markdown formatting"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for unclosed bold markers
            bold_count = line.count('**')
            if bold_count % 2 != 0:
                self.errors.append(f"Line {i}: Unclosed bold marker (**)")
            
            # Check for unclosed italic markers
            italic_count = line.count('_')
            if italic_count % 2 != 0 and '**_' not in line:  # Ignore bold+italic
                self.warnings.append(f"Line {i}: Possible unclosed italic marker (_)")
            
            # Check for malformed links
            if '[' in line and ']' in line:
                if line.count('[') != line.count(']'):
                    self.errors.append(f"Line {i}: Mismatched brackets in link")

def validate_philosophy(philosophy_path: Path = None) -> Tuple[bool, List[str], List[str]]:
    """Convenience function to validate philosophy
    
    Returns:
        (is_valid, errors, warnings)
    """
    validator = PhilosophyValidator(philosophy_path)
    return validator.validate()

def main():
    """Run validation and print results"""
    print("="*80)
    print("PHILOSOPHY.md Validation")
    print("="*80)
    
    validator = PhilosophyValidator()
    print(f"\nValidating: {validator.philosophy_path}")
    
    is_valid, errors, warnings = validator.validate()
    
    if errors:
        print(f"\n❌ {len(errors)} ERROR(S) FOUND:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for warning in warnings:
            print(f"  • {warning}")
    
    if is_valid:
        print("\n✅ PHILOSOPHY.md is valid!")
        return 0
    else:
        print(f"\n❌ PHILOSOPHY.md has {len(errors)} error(s)")
        print("\nPlease fix errors before continuing.")
        return 1

if __name__ == '__main__':
    exit(main())
