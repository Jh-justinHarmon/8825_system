#!/usr/bin/env python3
"""
Try to force access a folder by ID with different API methods
"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive',  # Full access, not just readonly
    'https://www.googleapis.com/auth/calendar'
]

def get_credentials():
    token_path = Path(__file__).parent / 'token.json'
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    return creds

def main():
    folder_id = '1vc7S0jYpxWoCB8hn-I2elA6O1-teihxf'
    
    print(f"\n{'='*80}")
    print(f"🔧 Attempting different access methods for folder")
    print(f"{'='*80}\n")
    
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    # Method 1: Direct file get with supportsAllDrives
    print("Method 1: Direct access with supportsAllDrives...")
    try:
        folder = service.files().get(
            fileId=folder_id,
            fields='id,name,owners,webViewLink,capabilities',
            supportsAllDrives=True
        ).execute()
        print(f"✅ SUCCESS!")
        print(f"   Name: {folder['name']}")
        print(f"   ID: {folder['id']}")
        print(f"   Link: {folder['webViewLink']}")
        
        # Try to list contents
        print(f"\n   Listing contents...")
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields='files(id,name,mimeType)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        items = results.get('files', [])
        print(f"   ✅ Found {len(items)} items")
        for item in items[:5]:
            print(f"      • {item['name']}")
        
        return True
        
    except HttpError as e:
        print(f"   ❌ Failed: {e}")
    
    # Method 2: Check if it's a shared drive
    print("\nMethod 2: Check if it's in a shared drive...")
    try:
        drives = service.drives().list().execute()
        print(f"   Found {len(drives.get('drives', []))} shared drives")
        for drive in drives.get('drives', []):
            print(f"      • {drive['name']}")
    except HttpError as e:
        print(f"   ❌ Failed: {e}")
    
    # Method 3: Try to get permissions
    print("\nMethod 3: Check permissions...")
    try:
        permissions = service.permissions().list(
            fileId=folder_id,
            fields='permissions(id,type,role,emailAddress)',
            supportsAllDrives=True
        ).execute()
        print(f"   ✅ Permissions found:")
        for perm in permissions.get('permissions', []):
            print(f"      • {perm.get('type')}: {perm.get('role')} - {perm.get('emailAddress', 'N/A')}")
    except HttpError as e:
        print(f"   ❌ Failed: {e}")
    
    print(f"\n{'='*80}\n")
    return False

if __name__ == "__main__":
    main()
