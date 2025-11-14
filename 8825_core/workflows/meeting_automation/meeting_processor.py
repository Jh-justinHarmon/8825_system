#!/usr/bin/env python3
"""
Meeting Processor - Context-Enhanced High-Fidelity Extraction
Uses GPT-4 with Brain Transport and TGIF knowledge for accurate extraction
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI

class MeetingProcessor:
    """Process meeting transcripts with context-enhanced GPT-4"""
    
    def __init__(self, api_key=None):
        """
        Initialize processor
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter"
            )
        
        self.client = OpenAI(api_key=api_key)
        self.brain_transport = None
        self.tgif_knowledge = None
    
    def load_context(self):
        """Load Brain Transport and TGIF knowledge"""
        # Load Brain Transport
        brain_path = Path.home() / "Documents" / "8825_BRAIN_TRANSPORT.json"
        if brain_path.exists():
            with open(brain_path) as f:
                self.brain_transport = json.load(f)
            print(f"✅ Loaded Brain Transport ({brain_path})")
        else:
            print(f"⚠️  Brain Transport not found at {brain_path}")
            self.brain_transport = {}
        
        # Load TGIF Knowledge
        tgif_path = Path(__file__).parent.parent.parent.parent.parent / "8825_files" / "HCSS" / "TGIF_KNOWLEDGE.json"
        if tgif_path.exists():
            with open(tgif_path) as f:
                self.tgif_knowledge = json.load(f)
            print(f"✅ Loaded TGIF Knowledge ({tgif_path})")
        else:
            print(f"⚠️  TGIF Knowledge not found at {tgif_path}")
            self.tgif_knowledge = {}
    
    def build_prompt(self, meeting_data):
        """
        Build context-enhanced prompt for GPT-4
        
        Args:
            meeting_data: Dict with meeting info from Gmail
            
        Returns:
            Prompt string
        """
        transcript = meeting_data.get('transcript', '')
        title = meeting_data.get('title', 'Unknown Meeting')
        date = meeting_data.get('date', 'Unknown Date')
        otter_summary = meeting_data.get('otter_summary', '')
        
        prompt = f"""You are an expert meeting analyst processing a transcript from Otter.ai's automatic transcription service. The transcript may contain errors in:
- Names of people, systems, or locations
- Technical terminology
- Numbers and codes
- Acronyms and abbreviations

SYSTEM CONTEXT (Brain Transport):
{json.dumps(self.brain_transport, indent=2)}

PROJECT CONTEXT (TGIF Knowledge Base):
{json.dumps(self.tgif_knowledge, indent=2)}

MEETING INFORMATION:
Title: {title}
Date: {date}
Otter.ai Summary: {otter_summary if otter_summary else 'Not provided'}

MEETING TRANSCRIPT:
{transcript}

TASK:
1. Review the transcript carefully
2. Identify and CORRECT any obvious transcription errors using the context provided
3. Interpret ambiguous references using your knowledge of the project
4. Extract high-fidelity structured data

Return a JSON object with the following structure:
{{
  "corrections_made": [
    {{
      "original": "text as transcribed",
      "corrected": "corrected text",
      "confidence": "high|medium|low",
      "reason": "why this correction was made"
    }}
  ],
  "meeting_metadata": {{
    "title": "Corrected meeting title",
    "date": "{date}",
    "duration_minutes": estimated_duration,
    "attendees": [
      {{
        "name": "Full Name",
        "role": "Their role",
        "company": "Company name"
      }}
    ],
    "meeting_type": "weekly_sync|accounting_integration|project_call|operations_review|other"
  }},
  "key_topics": [
    "Main discussion topic 1",
    "Main discussion topic 2"
  ],
  "decisions": [
    {{
      "text": "Decision made with corrected terminology",
      "category": "technical|business|operational|financial",
      "impact": "high|medium|low",
      "confidence": "high|medium|low",
      "context": "Why this decision matters"
    }}
  ],
  "actions": [
    {{
      "what": "Clear action description",
      "who": "Full name (not just first name)",
      "due": "YYYY-MM-DD or 'TBD'",
      "priority": "critical|high|medium|low",
      "context": "Why this action is needed",
      "confidence": "high|medium|low"
    }}
  ],
  "risks": [
    {{
      "text": "Risk description",
      "severity": "critical|high|medium|low",
      "mitigation": "How to address it",
      "owner": "Who is responsible",
      "confidence": "high|medium|low"
    }}
  ],
  "blockers": [
    {{
      "text": "Blocker description",
      "impact": "What is blocked",
      "resolution_needed_by": "YYYY-MM-DD or 'ASAP' or 'TBD'",
      "owner": "Who can unblock",
      "confidence": "high|medium|low"
    }}
  ],
  "issues_discussed": [
    {{
      "topic": "Issue description",
      "status": "open|in_progress|resolved",
      "owner": "Who is handling it",
      "notes": "Additional context"
    }}
  ],
  "next_meeting": {{
    "date": "YYYY-MM-DD or null",
    "agenda": ["Agenda item 1", "Agenda item 2"]
  }},
  "notes": "Any additional important context or observations"
}}

IMPORTANT GUIDELINES:
- Be thorough but don't invent information
- If uncertain about a correction, note it in the confidence field
- Use the context to interpret ambiguous references
- Correct obvious transcription errors (e.g., "net sweet" → "NetSuite")
- Expand first names to full names when you can identify them from context
- Extract dates in YYYY-MM-DD format
- Be specific about who is responsible for actions
- Include context to explain why things matter

Return ONLY the JSON object, no additional text.
"""
        return prompt
    
    def process(self, meeting_data):
        """
        Process meeting with GPT-4
        
        Args:
            meeting_data: Dict with meeting info from Gmail
            
        Returns:
            Dict with structured meeting data
        """
        if not self.brain_transport or not self.tgif_knowledge:
            print("⚠️  Loading context...")
            self.load_context()
        
        print(f"\n🤖 Processing with GPT-4 Turbo...")
        print(f"   Title: {meeting_data.get('title', 'Unknown')}")
        print(f"   Date: {meeting_data.get('date', 'Unknown')}")
        
        prompt = self.build_prompt(meeting_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # High-fidelity model
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert meeting analyst with deep context awareness. You correct transcription errors and extract structured data with high fidelity."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for accuracy
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Add metadata
            result['processing_metadata'] = {
                'processed_at': datetime.now().isoformat(),
                'model': 'gpt-4-turbo-preview',
                'gmail_id': meeting_data.get('gmail_id'),
                'otter_link': meeting_data.get('otter_link'),
                'raw_transcript_length': len(meeting_data.get('transcript', '')),
                'tokens_used': response.usage.total_tokens,
                'cost_estimate': response.usage.total_tokens * 0.00001  # Rough estimate
            }
            
            print(f"   ✅ Processed successfully")
            print(f"   📊 Tokens used: {response.usage.total_tokens}")
            print(f"   💰 Est. cost: ${result['processing_metadata']['cost_estimate']:.4f}")
            print(f"   🔧 Corrections made: {len(result.get('corrections_made', []))}")
            print(f"   📋 Decisions: {len(result.get('decisions', []))}")
            print(f"   ✅ Actions: {len(result.get('actions', []))}")
            print(f"   ⚠️  Risks: {len(result.get('risks', []))}")
            print(f"   🚫 Blockers: {len(result.get('blockers', []))}")
            
            return result
        
        except Exception as e:
            print(f"   ❌ Error processing with GPT-4: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_results(self, meeting_data, processed_data, output_dir=None):
        """
        Save processed meeting data
        
        Args:
            meeting_data: Original meeting data from Gmail
            processed_data: Processed data from GPT-4
            output_dir: Output directory (default: data/processed)
            
        Returns:
            Paths to saved files
        """
        if output_dir is None:
            output_dir = Path(__file__).parent / "data" / "processed"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        date = processed_data.get('meeting_metadata', {}).get('date', 'unknown')
        title = processed_data.get('meeting_metadata', {}).get('title', 'meeting')
        
        # Clean title for filename
        clean_title = title.lower()
        clean_title = clean_title.replace('hcss meeting - ', '')
        clean_title = clean_title.replace('tgi fridays | ', '')
        clean_title = clean_title.replace('tgif - ', '')
        clean_title = clean_title.replace(' | ', '_')
        clean_title = clean_title.replace(' - ', '_')
        clean_title = clean_title.replace(' ', '_')
        clean_title = ''.join(c for c in clean_title if c.isalnum() or c == '_')
        clean_title = clean_title[:50]  # Limit length
        
        base_filename = f"{date}_{clean_title}"
        
        # Save JSON
        json_file = output_dir / f"{base_filename}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'original_data': meeting_data,
                'processed_data': processed_data
            }, f, indent=2)
        
        # Generate Markdown
        md_file = output_dir / f"{base_filename}.md"
        markdown = self._generate_markdown(processed_data)
        with open(md_file, 'w') as f:
            f.write(markdown)
        
        print(f"\n💾 Saved results:")
        print(f"   JSON: {json_file}")
        print(f"   Markdown: {md_file}")
        
        return {
            'json': json_file,
            'markdown': md_file
        }
    
    def _generate_markdown(self, data):
        """Generate markdown summary"""
        metadata = data.get('meeting_metadata', {})
        
        md = f"# {metadata.get('title', 'Meeting Summary')}\n\n"
        md += f"**Date:** {metadata.get('date', 'Unknown')}  \n"
        md += f"**Type:** {metadata.get('meeting_type', 'Unknown')}  \n"
        
        attendees = metadata.get('attendees', [])
        if attendees:
            md += f"**Attendees:** {', '.join([a.get('name', 'Unknown') for a in attendees])}  \n"
        
        md += "\n---\n\n"
        
        # Corrections
        corrections = data.get('corrections_made', [])
        if corrections:
            md += "## 🔧 Transcription Corrections\n\n"
            for corr in corrections:
                md += f"- **{corr['original']}** → **{corr['corrected']}** ({corr['confidence']} confidence)\n"
                if corr.get('reason'):
                    md += f"  - {corr['reason']}\n"
            md += "\n"
        
        # Key Topics
        topics = data.get('key_topics', [])
        if topics:
            md += "## 📋 Key Topics\n\n"
            for topic in topics:
                md += f"- {topic}\n"
            md += "\n"
        
        # Decisions
        decisions = data.get('decisions', [])
        if decisions:
            md += "## 🎯 Decisions\n\n"
            for dec in decisions:
                md += f"### {dec['text']}\n"
                md += f"- **Category:** {dec['category']}\n"
                md += f"- **Impact:** {dec['impact']}\n"
                if dec.get('context'):
                    md += f"- **Context:** {dec['context']}\n"
                md += "\n"
        
        # Actions
        actions = data.get('actions', [])
        if actions:
            md += "## ✅ Action Items\n\n"
            md += "| Action | Owner | Due | Priority |\n"
            md += "|--------|-------|-----|----------|\n"
            for action in actions:
                md += f"| {action['what']} | {action['who']} | {action['due']} | {action['priority']} |\n"
            md += "\n"
        
        # Risks
        risks = data.get('risks', [])
        if risks:
            md += "## ⚠️ Risks\n\n"
            for risk in risks:
                md += f"### {risk['text']}\n"
                md += f"- **Severity:** {risk['severity']}\n"
                md += f"- **Mitigation:** {risk.get('mitigation', 'TBD')}\n"
                md += f"- **Owner:** {risk.get('owner', 'TBD')}\n"
                md += "\n"
        
        # Blockers
        blockers = data.get('blockers', [])
        if blockers:
            md += "## 🚫 Blockers\n\n"
            for blocker in blockers:
                md += f"### {blocker['text']}\n"
                md += f"- **Impact:** {blocker['impact']}\n"
                md += f"- **Resolution Needed By:** {blocker.get('resolution_needed_by', 'TBD')}\n"
                md += f"- **Owner:** {blocker.get('owner', 'TBD')}\n"
                md += "\n"
        
        # Issues
        issues = data.get('issues_discussed', [])
        if issues:
            md += "## 📌 Issues Discussed\n\n"
            for issue in issues:
                md += f"- **{issue['topic']}** ({issue['status']})\n"
                if issue.get('owner'):
                    md += f"  - Owner: {issue['owner']}\n"
                if issue.get('notes'):
                    md += f"  - Notes: {issue['notes']}\n"
            md += "\n"
        
        # Next Meeting
        next_mtg = data.get('next_meeting', {})
        if next_mtg and next_mtg.get('date'):
            md += "## 📅 Next Meeting\n\n"
            md += f"**Date:** {next_mtg['date']}\n\n"
            if next_mtg.get('agenda'):
                md += "**Agenda:**\n"
                for item in next_mtg['agenda']:
                    md += f"- {item}\n"
            md += "\n"
        
        # Notes
        notes = data.get('notes')
        if notes:
            md += "## 📝 Additional Notes\n\n"
            md += f"{notes}\n\n"
        
        # Processing metadata
        proc_meta = data.get('processing_metadata', {})
        if proc_meta:
            md += "---\n\n"
            md += "*Processed with GPT-4 Turbo on " + proc_meta.get('processed_at', 'Unknown') + "*\n"
        
        return md

def main():
    """Test processor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process meeting transcripts with context-enhanced GPT-4')
    parser.add_argument('--input-dir', default='data/raw', help='Input directory with raw meeting data')
    parser.add_argument('--output-dir', default='data/processed', help='Output directory for processed data')
    parser.add_argument('--file', help='Process specific file')
    
    args = parser.parse_args()
    
    processor = MeetingProcessor()
    
    if args.file:
        # Process single file
        with open(args.file) as f:
            meeting_data = json.load(f)
        
        processed = processor.process(meeting_data)
        if processed:
            processor.save_results(meeting_data, processed, args.output_dir)
    else:
        # Process all files in input directory
        input_dir = Path(args.input_dir)
        if not input_dir.exists():
            print(f"❌ Input directory not found: {input_dir}")
            sys.exit(1)
        
        json_files = list(input_dir.glob("*.json"))
        if not json_files:
            print(f"❌ No JSON files found in {input_dir}")
            sys.exit(1)
        
        print(f"📁 Found {len(json_files)} file(s) to process\n")
        
        for json_file in json_files:
            print(f"\n{'='*80}")
            print(f"Processing: {json_file.name}")
            print(f"{'='*80}")
            
            with open(json_file) as f:
                meeting_data = json.load(f)
            
            processed = processor.process(meeting_data)
            if processed:
                processor.save_results(meeting_data, processed, args.output_dir)

if __name__ == '__main__':
    main()
