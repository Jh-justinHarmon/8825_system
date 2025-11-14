#!/usr/bin/env python3
"""
Email Campaign Inspiration Miner
Extract and analyze promotional emails from Gmail
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
import openai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from playwright.sync_api import sync_playwright
import re

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class EmailCampaignMiner:
    """Mine Gmail for email campaign inspiration"""
    
    def __init__(self, credentials_path: str, token_path: str):
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self.service = None
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Authenticated with Gmail")
    
    def fetch_promotional_emails(self, max_results: int = 50, days_back: int = 90) -> List[Dict]:
        """Fetch promotional emails from last N days"""
        
        # Calculate date filter
        after_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')
        
        # Query: promotional category, recent
        query = f'category:promotions after:{after_date}'
        
        print(f"\n📧 Fetching up to {max_results} promotional emails from last {days_back} days...")
        
        results = self.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print("No promotional emails found")
            return []
        
        print(f"Found {len(messages)} emails, fetching details...")
        
        emails = []
        for i, msg in enumerate(messages, 1):
            print(f"  [{i}/{len(messages)}] Fetching email {msg['id'][:8]}...")
            
            email_data = self._fetch_email_details(msg['id'])
            if email_data:
                emails.append(email_data)
        
        print(f"✅ Fetched {len(emails)} emails")
        return emails
    
    def _fetch_email_details(self, message_id: str) -> Dict:
        """Fetch full email details"""
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            
            # Extract body (text and HTML)
            text_body, html_body = self._extract_body(msg['payload'])
            
            return {
                'id': message_id,
                'thread_id': msg['threadId'],
                'subject': headers.get('Subject', 'No Subject'),
                'from': headers.get('From', 'Unknown'),
                'date': headers.get('Date', ''),
                'body_preview': text_body[:500] if text_body else '',
                'body_full': text_body,
                'html_body': html_body,
                'gmail_link': f"https://mail.google.com/mail/u/0/#inbox/{message_id}"
            }
        except Exception as e:
            print(f"    ⚠️  Error fetching {message_id}: {e}")
            return None
    
    def _extract_body(self, payload: Dict) -> tuple:
        """Extract email body from payload - returns (text_body, html_body)"""
        text_body = ""
        html_body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        text_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
        else:
            if 'body' in payload and 'data' in payload['body']:
                data = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
                # Guess if HTML or text
                if '<html' in data.lower() or '<body' in data.lower():
                    html_body = data
                else:
                    text_body = data
        
        return text_body, html_body
    
    def analyze_email(self, email: Dict) -> Dict:
        """Analyze email with LLM"""
        
        prompt = f"""Analyze this promotional email and extract key patterns:

Subject: {email['subject']}
From: {email['from']}
Body Preview: {email['body_preview']}

Provide analysis in JSON format:
{{
    "industry": "restaurant|saas|ecommerce|other",
    "hook_type": "urgency|discount|storytelling|educational|social_proof|other",
    "design_style": "minimal|rich_media|text_heavy",
    "cta_text": "main call-to-action text",
    "cta_strength": "strong|medium|weak",
    "key_takeaways": ["takeaway 1", "takeaway 2"],
    "subject_pattern": "brief description of subject line pattern"
}}

Only return valid JSON, no other text."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an email marketing analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            print(f"    ⚠️  Analysis error: {e}")
            return {
                "industry": "unknown",
                "hook_type": "unknown",
                "design_style": "unknown",
                "cta_text": "",
                "cta_strength": "unknown",
                "key_takeaways": [],
                "subject_pattern": ""
            }
    
    def analyze_batch(self, emails: List[Dict]) -> List[Dict]:
        """Analyze all emails"""
        print(f"\n🤖 Analyzing {len(emails)} emails with LLM...")
        
        analyzed = []
        for i, email in enumerate(emails, 1):
            print(f"  [{i}/{len(emails)}] Analyzing: {email['subject'][:50]}...")
            
            analysis = self.analyze_email(email)
            
            analyzed.append({
                **email,
                'analysis': analysis
            })
        
        print(f"✅ Analysis complete")
        return analyzed
    
    def generate_html(self, emails: List[Dict], output_path: Path):
        """Generate interactive HTML dashboard"""
        
        # Group by category
        by_industry = {}
        by_hook = {}
        
        for email in emails:
            industry = email['analysis']['industry']
            hook = email['analysis']['hook_type']
            
            by_industry.setdefault(industry, []).append(email)
            by_hook.setdefault(hook, []).append(email)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Email Campaign Inspiration Library</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .email-card {{ border-left: 4px solid #007AFF; padding: 15px; margin: 10px 0; background: #f9f9f9; }}
        .email-card h3 {{ margin: 0 0 10px 0; color: #007AFF; }}
        .meta {{ color: #666; font-size: 14px; }}
        .tags {{ margin: 10px 0; }}
        .tag {{ display: inline-block; background: #e0e0e0; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px; }}
        .takeaways {{ margin: 10px 0; }}
        .takeaway {{ color: #333; margin: 5px 0; }}
        a {{ color: #007AFF; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>📧 Email Campaign Inspiration Library</h1>
    <p>Analyzed {len(emails)} promotional emails from last 90 days</p>
    
    <div class="stats">
        <div class="stat-card">
            <h3>{len(emails)}</h3>
            <p>Total Emails</p>
        </div>
        <div class="stat-card">
            <h3>{len(by_industry)}</h3>
            <p>Industries</p>
        </div>
        <div class="stat-card">
            <h3>{len(by_hook)}</h3>
            <p>Hook Types</p>
        </div>
    </div>
    
    <div class="section">
        <h2>By Industry</h2>
"""
        
        for industry, industry_emails in sorted(by_industry.items(), key=lambda x: len(x[1]), reverse=True):
            html += f"<h3>{industry.title()} ({len(industry_emails)})</h3>\n"
            
            for email in industry_emails[:5]:  # Top 5 per industry
                analysis = email['analysis']
                html += f"""
                <div class="email-card">
                    <h3>{email['subject']}</h3>
                    <div class="meta">From: {email['from']} | {email['date'][:16]}</div>
                    <div class="tags">
                        <span class="tag">{analysis['hook_type']}</span>
                        <span class="tag">{analysis['design_style']}</span>
                        <span class="tag">CTA: {analysis['cta_strength']}</span>
                    </div>
                    <div class="takeaways">
                        <strong>Key Takeaways:</strong>
                        {''.join([f'<div class="takeaway">• {t}</div>' for t in analysis['key_takeaways']])}
                    </div>
                    <a href="{email['gmail_link']}" target="_blank">View in Gmail →</a>
                </div>
                """
        
        html += """
    </div>
</body>
</html>
"""
        
        output_path.write_text(html)
        print(f"✅ HTML dashboard: {output_path}")
    
    def generate_markdown(self, emails: List[Dict], output_path: Path):
        """Generate markdown report"""
        
        # Aggregate patterns
        by_hook = {}
        by_industry = {}
        subject_patterns = []
        
        for email in emails:
            analysis = email['analysis']
            
            hook = analysis['hook_type']
            industry = analysis['industry']
            
            by_hook.setdefault(hook, []).append(email)
            by_industry.setdefault(industry, []).append(email)
            
            if analysis['subject_pattern']:
                subject_patterns.append({
                    'pattern': analysis['subject_pattern'],
                    'example': email['subject']
                })
        
        md = f"""# Email Campaign Inspiration Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Emails Analyzed:** {len(emails)}  
**Date Range:** Last 90 days

---

## Top Hook Types

"""
        
        for hook, hook_emails in sorted(by_hook.items(), key=lambda x: len(x[1]), reverse=True):
            md += f"### {hook.title()} ({len(hook_emails)} emails)\n\n"
            
            for email in hook_emails[:3]:
                md += f"- **{email['subject']}**\n"
                md += f"  - From: {email['from']}\n"
                for takeaway in email['analysis']['key_takeaways'][:2]:
                    md += f"  - {takeaway}\n"
                md += f"  - [View in Gmail]({email['gmail_link']})\n\n"
        
        md += "\n## By Industry\n\n"
        
        for industry, industry_emails in sorted(by_industry.items(), key=lambda x: len(x[1]), reverse=True):
            md += f"### {industry.title()} ({len(industry_emails)} emails)\n\n"
            
            for email in industry_emails[:3]:
                md += f"- {email['subject']}\n"
        
        md += "\n## Subject Line Patterns\n\n"
        
        for pattern in subject_patterns[:10]:
            md += f"- **Pattern:** {pattern['pattern']}\n"
            md += f"  - Example: {pattern['example']}\n\n"
        
        output_path.write_text(md)
        print(f"✅ Markdown report: {output_path}")
    
    def generate_json(self, emails: List[Dict], output_path: Path):
        """Generate JSON library"""
        
        library = {
            'generated': datetime.now().isoformat(),
            'total_emails': len(emails),
            'emails': emails
        }
        
        output_path.write_text(json.dumps(library, indent=2))
        print(f"✅ JSON library: {output_path}")
    
    def generate_screenshots(self, emails: List[Dict], output_dir: Path):
        """Save HTML files for manual screenshot (Playwright unstable)"""
        
        # iCloud Drive path
        icloud_path = Path.home() / 'Library' / 'Mobile Documents' / 'com~apple~CloudDocs' / 'Documents' / 'Joju' / 'Jh email campaign images'
        icloud_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📄 Saving HTML files to: {icloud_path}")
        print("   (Playwright screenshot unstable - saving HTML for manual screenshot)")
        
        # Save HTML files
        for i, email in enumerate(emails, 1):
            try:
                # Clean filename from subject
                safe_subject = re.sub(r'[^\w\s-]', '', email['subject'])[:50]
                filename = f"{i:02d}_{safe_subject}.html"
                output_path = icloud_path / filename
                
                print(f"  [{i}/{len(emails)}] {email['subject'][:60]}...")
                
                # Get HTML content
                html_body = email.get('html_body', '')
                if not html_body:
                    print(f"    ⚠️  No HTML content")
                    continue
                
                # Save HTML file
                output_path.write_text(html_body, encoding='utf-8')
                
            except Exception as e:
                print(f"    ⚠️  Error: {e}")
                continue
        
        print(f"\n✅ HTML files saved to: {icloud_path}")
        print(f"\n📸 To screenshot:")
        print(f"   1. Open HTML files in browser")
        print(f"   2. Cmd+Shift+4 to screenshot")
        print(f"   3. Or use: screencapture -w filename.png")


def main():
    """Run email campaign miner"""
    
    # Paths
    base_path = Path.home() / 'Hammer Consulting Dropbox' / 'Justin Harmon' / 'Public' / '8825' / '8825-system'
    creds_path = base_path / '8825_core' / 'integrations' / 'google' / 'credentials.json'
    token_path = base_path / '8825_core' / 'integrations' / 'google' / 'token.json'
    output_dir = base_path / '8825_core' / 'explorations' / 'email_inspiration'
    
    output_dir.mkdir(exist_ok=True)
    
    # Initialize miner
    miner = EmailCampaignMiner(creds_path, token_path)
    
    # Authenticate
    miner.authenticate()
    
    # Fetch emails
    emails = miner.fetch_promotional_emails(max_results=50, days_back=90)
    
    if not emails:
        print("No emails to process")
        return
    
    # Analyze
    analyzed = miner.analyze_batch(emails)
    
    # Generate all outputs
    print("\n📝 Generating outputs...")
    miner.generate_html(analyzed, output_dir / 'email_inspiration.html')
    miner.generate_markdown(analyzed, output_dir / 'email_inspiration.md')
    miner.generate_json(analyzed, output_dir / 'email_inspiration.json')
    
    # Generate screenshots
    miner.generate_screenshots(analyzed, output_dir)
    
    print(f"\n✅ Complete! Check {output_dir}/")
    print(f"\n💡 To search: 8825 search \"restaurant urgency\"")


if __name__ == '__main__':
    main()
