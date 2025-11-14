#!/usr/bin/env python3
"""
List contents of a specific Google Drive folder
"""

import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

def main():
    folder_id = '1vc7S0jYpxWoCB8hn-I2elA6O1-teihxf'
    
    if len(sys.argv) > 1:
        folder_id = sys.argv[1]
    
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    # Get folder details
    folder = service.files().get(
        fileId=folder_id,
        fields='id,name,owners,webViewLink'
    ).execute()
    
    print(f"\n{'='*80}")
    print(f"📁 Folder: {folder['name']}")
    print(f"{'='*80}\n")
    print(f"ID: {folder['id']}")
    print(f"Link: {folder['webViewLink']}")
    
    if 'owners' in folder:
        owners = [o.get('displayName', o.get('emailAddress')) for o in folder['owners']]
        print(f"Owner(s): {', '.join(owners)}")
    
    # List contents
    print(f"\n{'─'*80}")
    print('📂 Contents:')
    print(f"{'─'*80}\n")
    
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields='files(id,name,mimeType,webViewLink,modifiedTime)',
        pageSize=100,
        orderBy='name'
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print('📭 Folder is empty')
    else:
        for i, item in enumerate(items, 1):
            icon = '📁' if item['mimeType'] == 'application/vnd.google-apps.folder' else '📄'
            mime_type = item['mimeType'].split('.')[-1]
            print(f"{i}. {icon} {item['name']}")
            print(f"   Type: {mime_type}")
            print(f"   Link: {item['webViewLink']}")
            print(f"   Modified: {item['modifiedTime']}")
            print()
    
    print(f"{'='*80}")
    print(f"Total items: {len(items)}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
