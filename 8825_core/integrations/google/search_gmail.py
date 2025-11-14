#!/usr/bin/env python3
"""
Search Gmail for specific emails
"""

import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

# Scopes needed
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def get_credentials():
    """Get or refresh Gmail credentials"""
    creds = None
    token_path = Path(__file__).parent / 'token.json'
    creds_path = Path(__file__).parent / 'credentials.json'
    
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except:
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                creds = None
        
        if not creds:
            if not creds_path.exists():
                print("❌ credentials.json not found")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_message_body(service, msg_id):
    """Get the body of an email message"""
    try:
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()
        
        payload = message.get('payload', {})
        
        # Try to get body from parts
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        
        # Try direct body
        if 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')
        
        return "(No body content)"
    
    except Exception as e:
        return f"(Error getting body: {e})"

def search_emails(service, query, max_results=10):
    """Search for emails matching query"""
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        return messages
    
    except Exception as e:
        print(f"❌ Error searching: {e}")
        return []

def get_message_details(service, msg_id):
    """Get details of a message"""
    try:
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='metadata',
            metadataHeaders=['From', 'To', 'Subject', 'Date']
        ).execute()
        
        headers = message.get('payload', {}).get('headers', [])
        details = {}
        
        for header in headers:
            name = header['name']
            if name in ['From', 'To', 'Subject', 'Date']:
                details[name] = header['value']
        
        details['snippet'] = message.get('snippet', '')
        details['id'] = msg_id
        
        return details
    
    except Exception as e:
        return {'error': str(e)}

def main():
    """Search Gmail for Joju Intake Design Sprint"""
    
    # Get search query from command line or use default
    if len(sys.argv) > 1:
        search_query = ' '.join(sys.argv[1:])
    else:
        search_query = "Joju Intake Design Sprint"
    
    print(f"\n{'='*80}")
    print(f"📧 Searching Gmail for: '{search_query}'")
    print(f"{'='*80}\n")
    
    creds = get_credentials()
    if not creds:
        return
    
    service = build('gmail', 'v1', credentials=creds)
    
    # Search for emails
    print("Searching...\n")
    messages = search_emails(service, search_query, max_results=20)
    
    if not messages:
        print(f"❌ No emails found matching '{search_query}'")
        print("\nTrying broader search for 'Joju'...")
        messages = search_emails(service, "Joju", max_results=20)
        
        if not messages:
            print("❌ No emails found for 'Joju' either")
            print("\nTrying 'Design Sprint'...")
            messages = search_emails(service, "Design Sprint", max_results=20)
    
    if not messages:
        print("\n❌ No relevant emails found")
        print("\nTips:")
        print("  • Check if the invitation was sent to a different email")
        print("  • Look for Google Drive share notifications")
        print("  • Check spam/trash folders")
        return
    
    print(f"✅ Found {len(messages)} email(s):\n")
    print(f"{'─'*80}\n")
    
    for i, msg in enumerate(messages, 1):
        details = get_message_details(service, msg['id'])
        
        print(f"{i}. From: {details.get('From', 'Unknown')}")
        print(f"   Date: {details.get('Date', 'Unknown')}")
        print(f"   Subject: {details.get('Subject', 'No subject')}")
        print(f"   Preview: {details.get('snippet', '')[:100]}...")
        print(f"   Message ID: {details['id']}")
        
        # Check if it's a Drive share
        if 'drive.google.com' in details.get('snippet', '').lower() or \
           'shared' in details.get('Subject', '').lower():
            print(f"   🔗 Likely a Google Drive share!")
        
        print()
    
    # Offer to show full content
    print(f"{'─'*80}")
    print(f"\n💡 To see full email content:")
    print(f"   python3 search_gmail.py --show <message_id>")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
