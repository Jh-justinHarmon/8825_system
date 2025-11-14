#!/usr/bin/env python3
"""
MD Converter - Convert Markdown to DOCX/PDF/HTML
Simple, fast, works every time.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

def convert_md_to_docx(input_file, output_file=None):
    """Convert MD to DOCX using Pandoc"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        return False
    
    # Generate output filename if not provided
    if output_file is None:
        output_file = input_path.stem + ".docx"
    
    output_path = Path(output_file)
    
    # Ensure output is in Downloads
    if not output_path.is_absolute():
        output_path = Path.home() / "Downloads" / output_path
    
    try:
        # Run Pandoc
        cmd = [
            "pandoc",
            str(input_path),
            "-o", str(output_path),
            "--standalone"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Export Complete!")
            print(f"📄 File: {output_path.name}")
            print(f"📁 Location: {output_path.parent}")
            return True
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def convert_md_to_pdf(input_file, output_file=None):
    """Convert MD to PDF using Pandoc"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        return False
    
    if output_file is None:
        output_file = input_path.stem + ".pdf"
    
    output_path = Path(output_file)
    
    if not output_path.is_absolute():
        output_path = Path.home() / "Downloads" / output_path
    
    try:
        cmd = [
            "pandoc",
            str(input_path),
            "-o", str(output_path),
            "--pdf-engine=xelatex",
            "--standalone"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Export Complete!")
            print(f"📄 File: {output_path.name}")
            print(f"📁 Location: {output_path.parent}")
            return True
        else:
            print(f"❌ Conversion failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python3 md_converter.py <input.md> <format>")
        print("Formats: docx, pdf")
        print("Example: python3 md_converter.py notes.md docx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    format_type = sys.argv[2].lower()
    
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    if format_type == "docx":
        convert_md_to_docx(input_file, output_file)
    elif format_type == "pdf":
        convert_md_to_pdf(input_file, output_file)
    else:
        print(f"❌ Unsupported format: {format_type}")
        print("Supported: docx, pdf")
        sys.exit(1)

if __name__ == "__main__":
    main()
