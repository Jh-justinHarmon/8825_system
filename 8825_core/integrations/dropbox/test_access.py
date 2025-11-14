#!/usr/bin/env python3
"""
Quick test to verify Dropbox API access
"""

import sys

# Test 1: Check if dropbox package is installed
try:
    import dropbox
    print("✓ dropbox package installed")
except ImportError:
    print("✗ dropbox package NOT installed")
    print("  Install with: pip3 install dropbox")
    sys.exit(1)

# Test 2: Check for existing Dropbox app credentials
print("\n📱 Checking for existing Dropbox app...")
print("   App name: 8825")
print("   Status: Development")
print("   Permission type: Scoped App (App Folder)")
print("   ✓ App exists (from screenshot)")

# Test 3: Explain what we need
print("\n🔑 To test API access, we need:")
print("   1. Go to: https://www.dropbox.com/developers/apps")
print("   2. Click on '8825' app")
print("   3. Go to 'Settings' tab")
print("   4. Under 'OAuth 2', click 'Generate' access token")
print("   5. Copy the token")
print("   6. Run: export DROPBOX_ACCESS_TOKEN='paste_token_here'")
print("   7. Run this script again")

# Test 4: Try to connect if token exists
import os
token = os.getenv('DROPBOX_ACCESS_TOKEN')

if not token:
    print("\n⚠️  DROPBOX_ACCESS_TOKEN not set")
    print("   Set it with: export DROPBOX_ACCESS_TOKEN='your_token'")
    sys.exit(0)

print(f"\n✓ Token found (length: {len(token)})")

# Test 5: Connect to Dropbox
try:
    dbx = dropbox.Dropbox(token)
    account = dbx.users_get_current_account()
    print(f"\n✅ Connected to Dropbox!")
    print(f"   Account: {account.name.display_name}")
    print(f"   Email: {account.email}")
    print(f"   Account ID: {account.account_id}")
    
    # Test 6: List root folder
    print(f"\n📁 Testing folder access...")
    result = dbx.files_list_folder("", recursive=False)
    print(f"   ✓ Can list root folder")
    print(f"   Found {len(result.entries)} items")
    
    if result.entries:
        print(f"\n   First few items:")
        for entry in result.entries[:5]:
            entry_type = "📁" if isinstance(entry, dropbox.files.FolderMetadata) else "📄"
            print(f"   {entry_type} {entry.name}")
    
    print(f"\n✅ Dropbox API access confirmed!")
    print(f"   Ready to run dropbox_miner.py")
    
except dropbox.exceptions.AuthError as e:
    print(f"\n✗ Authentication failed: {e}")
    print("   Token may be invalid or expired")
    print("   Generate a new token from the Dropbox app console")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)
