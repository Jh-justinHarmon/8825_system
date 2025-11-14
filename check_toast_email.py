#!/usr/bin/env python3
"""
Quick script to check latest Gmail for Toast updates and update sheet
"""

import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from toast_sheet_manager import ToastScheduleManager

def get_latest_toast_email():
    """Get the most recent email about Toast"""
    creds_path = os.path.expanduser('~/Hammer Consulting Dropbox/Justin Harmon/Public/8825/8825-system/8825_core/integrations/google/token.json')
    
    creds = Credentials.from_authorized_user_file(creds_path)
    service = build('gmail', 'v1', credentials=creds)
    
    # Search for recent emails with "1887" or "Dover"
    results = service.users().messages().list(
        userId='me',
        q='(1887 OR Dover) newer_than:1h',
        maxResults=1
    ).execute()
    
    messages = results.get('messages', [])
    if not messages:
        print("No recent emails found about 1887/Dover")
        return None
    
    # Get the full message
    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    
    # Extract subject and body
    headers = msg['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    
    # Get body (handle multipart emails)
    def get_body(payload):
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(part['body'].get('data', '')).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    html = base64.urlsafe_b64decode(part['body'].get('data', '')).decode('utf-8')
                    # Strip HTML tags for simple parsing
                    import re
                    return re.sub(r'<[^>]+>', ' ', html)
                elif 'parts' in part:
                    result = get_body(part)
                    if result:
                        return result
        else:
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
        return ''
    
    body = get_body(msg['payload'])
    
    print(f"\n{'='*60}")
    print(f"SUBJECT: {subject}")
    print(f"{'='*60}")
    print(body[:500])
    print(f"{'='*60}\n")
    
    return {'subject': subject, 'body': body}

def parse_and_update(email_data):
    """Parse email and update sheet"""
    if not email_data:
        return
    
    body = email_data['body'].lower()
    
    # Extract info (simple keyword matching for now)
    updates = {}
    
    if 'shipped' in body or 'tracking' in body:
        updates['toast_status'] = 'Shipped'
        # Try to extract tracking number
        import re
        tracking = re.search(r'tracking[:\s]+([A-Z0-9]+)', body, re.I)
        if tracking:
            updates['toast_status'] = f"Shipped - Tracking #{tracking.group(1)}"
    
    if 'arrived' in body or 'delivered' in body:
        updates['toast_status'] = 'Arrived - Ready to install'
    
    if 'scheduled' in body or 'appointment' in body:
        updates['onsite_status'] = 'Scheduled'
        # Try to extract date
        import re
        date_match = re.search(r'(\d{1,2}[/-]\d{1,2})', body)
        if date_match:
            updates['onsite_status'] = f"Scheduled for {date_match.group(1)}"
    
    if updates:
        print("Extracted updates:")
        for key, val in updates.items():
            print(f"  {key}: {val}")
        
        # Update sheet
        manager = ToastScheduleManager()
        manager.connect("Toast Equipment Schedule")
        manager.update_store_status("1887", **updates)
        print("\n✓ Sheet updated!")
    else:
        print("No status updates detected in email")
        print("\nEmail body preview:")
        print(email_data['body'][:300])

if __name__ == "__main__":
    email = get_latest_toast_email()
    parse_and_update(email)
