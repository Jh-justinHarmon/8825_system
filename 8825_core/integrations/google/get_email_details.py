#!/usr/bin/env python3
"""
Get full details of a specific email
"""

import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import re

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def get_credentials():
    """Get credentials"""
    token_path = Path(__file__).parent / 'token.json'
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    return creds

def get_email_body(service, msg_id):
    """Get email body and extract Drive links"""
    message = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()
    
    payload = message.get('payload', {})
    body_text = ""
    
    # Get body
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] in ['text/plain', 'text/html']:
                data = part['body'].get('data', '')
                if data:
                    body_text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    elif 'body' in payload and 'data' in payload['body']:
        data = payload['body']['data']
        body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    # Extract Drive links
    drive_links = re.findall(r'https://drive\.google\.com/[^\s<>"]+', body_text)
    folder_ids = re.findall(r'folders/([a-zA-Z0-9_-]+)', body_text)
    
    return body_text, drive_links, folder_ids

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_email_details.py <message_id>")
        print("\nFor Joju Intake Design Sprint email:")
        print("python3 get_email_details.py 198eeeef22c390c8")
        return
    
    msg_id = sys.argv[1]
    
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    print(f"\n{'='*80}")
    print(f"📧 Email Details")
    print(f"{'='*80}\n")
    
    body, links, folder_ids = get_email_body(service, msg_id)
    
    print("Drive Links Found:")
    for link in links:
        print(f"  • {link}")
    
    print(f"\nFolder IDs Found:")
    for fid in folder_ids:
        print(f"  • {fid}")
        print(f"    Direct link: https://drive.google.com/drive/folders/{fid}")
    
    print(f"\n{'='*80}\n")
    
    if folder_ids:
        print(f"✅ Found folder ID: {folder_ids[0]}")
        print(f"\nYou can access it at:")
        print(f"https://drive.google.com/drive/folders/{folder_ids[0]}")

if __name__ == "__main__":
    main()
