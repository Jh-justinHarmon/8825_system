#!/usr/bin/env python3
"""
Gmail API Client
Official Google Gmail API wrapper
"""

import os
import base64
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class GmailClient:
    """Gmail API client for reading emails"""
    
    def __init__(self, credentials_path: str, token_path: str):
        """
        Initialize Gmail client
        
        Args:
            credentials_path: Path to credentials.json from Google Cloud
            token_path: Path to store OAuth token
        """
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self._service = None
    
    def _get_service(self):
        """Get or create Gmail service"""
        if self._service is None:
            try:
                from google.auth.transport.requests import Request
                from google.oauth2.credentials import Credentials
                from google_auth_oauthlib.flow import InstalledAppFlow
                from googleapiclient.discovery import build
                
                SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
                          'https://www.googleapis.com/auth/gmail.modify']
                
                creds = None
                
                # Load existing token
                if self.token_path.exists():
                    creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
                
                # Refresh or get new token
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            str(self.credentials_path), SCOPES)
                        creds = flow.run_local_server(port=0)
                    
                    # Save token
                    with open(self.token_path, 'w') as token:
                        token.write(creds.to_json())
                
                self._service = build('gmail', 'v1', credentials=creds)
                
            except ImportError:
                raise ImportError(
                    "Gmail API not installed. Install with:\n"
                    "pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client"
                )
        
        return self._service
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search Gmail messages
        
        Args:
            query: Gmail search query (e.g., "from:no-reply@otter.ai")
            max_results: Maximum results to return
            
        Returns:
            List of message objects
        """
        try:
            service = self._get_service()
            
            # Search messages
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get full message details
            full_messages = []
            for msg in messages:
                full_msg = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()
                
                full_messages.append({
                    'id': full_msg['id'],
                    'thread_id': full_msg['threadId'],
                    'subject': self._get_header(full_msg, 'Subject'),
                    'from': self._get_header(full_msg, 'From'),
                    'date': self._get_header(full_msg, 'Date'),
                    'body': self._get_body(full_msg),
                    'raw': full_msg
                })
            
            return full_messages
            
        except Exception as e:
            raise Exception(f"Failed to search Gmail: {e}")
    
    def mark_as_read(self, message_id: str):
        """Mark message as read"""
        try:
            service = self._get_service()
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            raise Exception(f"Failed to mark as read: {e}")
    
    def _get_header(self, message: Dict, name: str) -> str:
        """Extract header value from message"""
        headers = message.get('payload', {}).get('headers', [])
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''
    
    def _get_body(self, message: Dict) -> str:
        """Extract body from message"""
        try:
            payload = message.get('payload', {})
            
            # Check for plain text part
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            
            # Single part message
            if 'body' in payload and 'data' in payload['body']:
                data = payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            
            return ''
            
        except Exception:
            return ''
    
    def test_connection(self) -> bool:
        """Test if connection works"""
        try:
            service = self._get_service()
            service.users().getProfile(userId='me').execute()
            return True
        except Exception:
            return False

def main():
    """Test Gmail client"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 gmail_client.py <credentials_path> <token_path>")
        sys.exit(1)
    
    creds_path = sys.argv[1]
    token_path = sys.argv[2]
    
    print("Testing Gmail connection...")
    client = GmailClient(creds_path, token_path)
    
    if client.test_connection():
        print("✅ Connection successful!")
        
        # Test search
        print("\nSearching for Otter.ai emails...")
        messages = client.search("from:no-reply@otter.ai", max_results=5)
        print(f"Found {len(messages)} messages")
        
        for msg in messages:
            print(f"\n- {msg['subject']}")
            print(f"  Date: {msg['date']}")
    else:
        print("❌ Connection failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
