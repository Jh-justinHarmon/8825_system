#!/usr/bin/env python3
"""
Find and access Google Drive folders
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

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
    
    # Load existing token
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"⚠️  Token file invalid, will re-authenticate: {e}")
            creds = None
    
    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️  Token refresh failed, will re-authenticate: {e}")
                creds = None
        
        if not creds:
            if not creds_path.exists():
                print("❌ credentials.json not found")
                print(f"   Expected at: {creds_path}")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def search_folders(service, query):
    """Search for folders matching query"""
    try:
        # Search for folders
        results = service.files().list(
            q=f"name contains '{query}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name, owners, shared, webViewLink, permissions)',
            pageSize=100
        ).execute()
        
        folders = results.get('files', [])
        return folders
    
    except Exception as e:
        print(f"❌ Error searching: {e}")
        return []

def list_folder_contents(service, folder_id, indent=0):
    """List contents of a folder"""
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(id, name, mimeType, webViewLink, modifiedTime)',
            pageSize=100
        ).execute()
        
        items = results.get('files', [])
        
        for item in items:
            prefix = "  " * indent
            icon = "📁" if item['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            print(f"{prefix}{icon} {item['name']}")
            print(f"{prefix}   ID: {item['id']}")
            print(f"{prefix}   Link: {item['webViewLink']}")
            print(f"{prefix}   Modified: {item['modifiedTime']}")
            print()
        
        return items
    
    except Exception as e:
        print(f"❌ Error listing contents: {e}")
        return []

def main():
    """Main function"""
    # Get folder name from command line or use default
    if len(sys.argv) > 1:
        folder_name = ' '.join(sys.argv[1:])
    else:
        folder_name = "Joju Intake Design Sprint"
    
    print(f"\n{'='*80}")
    print(f"🔍 Searching Google Drive for: '{folder_name}'")
    print(f"{'='*80}\n")
    
    # Get credentials
    creds = get_credentials()
    if not creds:
        return
    
    # Build Drive service
    service = build('drive', 'v3', credentials=creds)
    
    # Search for folders
    print("Searching...")
    folders = search_folders(service, folder_name)
    
    if not folders:
        print(f"\n❌ No folders found matching '{folder_name}'")
        print("\nTips:")
        print("  • Check the folder name spelling")
        print("  • Make sure the folder is shared with you")
        print("  • Try searching for part of the name")
        return
    
    print(f"\n✅ Found {len(folders)} folder(s):\n")
    
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder['name']}")
        print(f"   ID: {folder['id']}")
        print(f"   Link: {folder['webViewLink']}")
        
        # Check if shared
        if folder.get('shared'):
            print(f"   Status: 📤 Shared with you")
        
        # Show owners
        if 'owners' in folder:
            owners = [o.get('displayName', o.get('emailAddress', 'Unknown')) for o in folder['owners']]
            print(f"   Owner(s): {', '.join(owners)}")
        
        print()
    
    # If only one folder, offer to list contents
    if len(folders) == 1:
        folder = folders[0]
        print(f"{'─'*80}")
        print(f"📂 Contents of '{folder['name']}':")
        print(f"{'─'*80}\n")
        
        items = list_folder_contents(service, folder['id'])
        
        if items:
            print(f"\n✅ Found {len(items)} item(s) in folder")
        else:
            print("\n📭 Folder is empty")
    
    elif len(folders) > 1:
        print("💡 Multiple folders found. To see contents of a specific folder:")
        print(f"   python3 {Path(__file__).name} --id <folder_id>")
    
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
