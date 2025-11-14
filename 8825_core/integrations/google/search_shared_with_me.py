#!/usr/bin/env python3
"""
Search in "Shared with me" for folders
"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def get_credentials():
    token_path = Path(__file__).parent / 'token.json'
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    return creds

def main():
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    print(f"\n{'='*80}")
    print(f"🔍 Searching 'Shared with me' for Joju folders")
    print(f"{'='*80}\n")
    
    # Search in shared with me
    results = service.files().list(
        q="sharedWithMe=true and name contains 'Joju' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive',
        fields='files(id,name,owners,webViewLink,capabilities,permissions)',
        pageSize=100
    ).execute()
    
    folders = results.get('files', [])
    
    if not folders:
        print("❌ No Joju folders found in 'Shared with me'")
        print("\nTrying broader search...")
        
        # Try without name filter
        results = service.files().list(
            q="sharedWithMe=true and mimeType='application/vnd.google-apps.folder'",
            spaces='drive',
            fields='files(id,name,owners,webViewLink)',
            pageSize=100,
            orderBy='modifiedTime desc'
        ).execute()
        
        folders = results.get('files', [])
        print(f"\nFound {len(folders)} total shared folders:")
        for f in folders[:10]:  # Show first 10
            print(f"  • {f['name']}")
        
        return
    
    print(f"✅ Found {len(folders)} Joju folder(s):\n")
    
    for i, folder in enumerate(folders, 1):
        print(f"{i}. 📁 {folder['name']}")
        print(f"   ID: {folder['id']}")
        print(f"   Link: {folder['webViewLink']}")
        
        if 'owners' in folder:
            owners = [o.get('displayName', o.get('emailAddress')) for o in folder['owners']]
            print(f"   Owner(s): {', '.join(owners)}")
        
        # Try to list contents
        try:
            contents = service.files().list(
                q=f"'{folder['id']}' in parents and trashed=false",
                fields='files(id,name,mimeType)',
                pageSize=10
            ).execute()
            
            items = contents.get('files', [])
            print(f"   Contents: {len(items)} item(s)")
            
            if items:
                for item in items[:3]:
                    icon = '📁' if 'folder' in item['mimeType'] else '📄'
                    print(f"     {icon} {item['name']}")
        except Exception as e:
            print(f"   ⚠️  Cannot list contents: {e}")
        
        print()
    
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
