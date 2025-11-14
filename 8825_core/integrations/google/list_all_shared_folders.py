#!/usr/bin/env python3
"""
List all folders shared with you in Google Drive
"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes needed
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def get_credentials():
    """Get or refresh Google Drive credentials"""
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

def main():
    """List all shared folders"""
    print(f"\n{'='*80}")
    print(f"📂 Listing ALL Shared Folders in Google Drive")
    print(f"{'='*80}\n")
    
    creds = get_credentials()
    if not creds:
        return
    
    service = build('drive', 'v3', credentials=creds)
    
    # Get shared folders
    print("Fetching shared folders...\n")
    
    try:
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and sharedWithMe=true and trashed=false",
            spaces='drive',
            fields='files(id, name, owners, webViewLink, modifiedTime)',
            pageSize=100,
            orderBy='modifiedTime desc'
        ).execute()
        
        folders = results.get('files', [])
        
        if not folders:
            print("❌ No shared folders found")
            print("\nMake sure:")
            print("  • Folders are shared with harmon.justin@gmail.com")
            print("  • You've accepted the share invitation")
            return
        
        print(f"✅ Found {len(folders)} shared folder(s):\n")
        print(f"{'─'*80}\n")
        
        for i, folder in enumerate(folders, 1):
            print(f"{i}. 📁 {folder['name']}")
            print(f"   ID: {folder['id']}")
            print(f"   Link: {folder['webViewLink']}")
            print(f"   Modified: {folder['modifiedTime']}")
            
            if 'owners' in folder:
                owners = [o.get('displayName', o.get('emailAddress', 'Unknown')) for o in folder['owners']]
                print(f"   Owner(s): {', '.join(owners)}")
            
            print()
        
        print(f"{'─'*80}")
        print(f"\n💡 To search for a specific folder:")
        print(f"   python3 find_drive_folder.py \"folder name\"")
        print(f"\n{'='*80}\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
