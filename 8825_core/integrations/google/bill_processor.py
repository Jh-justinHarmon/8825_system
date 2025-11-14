#!/usr/bin/env python3
"""
8825 Bill Processor
Processes images from Downloads → OCR → Categorize → Google Calendar + Drive
"""

import os
import sys
import json
import re
import csv
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple, List

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'utils'))
from paths import get_user_dir, get_downloads_dir

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OCR imports
try:
    from PIL import Image
    import pytesseract
    from pillow_heif import register_heif_opener
    register_heif_opener()  # Enable HEIC support
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("Warning: OCR dependencies not installed")

# Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/drive.file'
]

# Paths
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'
TOKEN_FILE = SCRIPT_DIR / 'token.json'
DOWNLOADS_DIR = get_downloads_dir()
PROCESSED_DIR = DOWNLOADS_DIR / '8825_processed' / 'bills'

# CSV Export (Phil's Ledger integration)
CSV_EXPORT_DIR = get_user_dir('justin_harmon') / 'jh_assistant' / 'data' / 'phils_ledger_imports'
CSV_EXPORT_ENABLED = True

class BillProcessor:
    def __init__(self):
        self.calendar_service = None
        self.drive_service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google APIs"""
        creds = None
        
        # Load existing token
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        
        # Refresh or get new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        # Build services
        self.calendar_service = build('calendar', 'v3', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)
        
        print("✓ Authenticated with Google")
    
    def ocr_image(self, image_path: Path) -> Optional[str]:
        """Extract text from image"""
        if not HAS_OCR:
            return None
        
        try:
            # Try to open image
            try:
                image = Image.open(image_path)
            except Exception as e:
                # If HEIC fails, try converting with sips (macOS built-in)
                if image_path.suffix.lower() in ['.heic', '.heif']:
                    print(f"  → Converting HEIC to PNG...")
                    temp_png = Path('/tmp') / f"{image_path.stem}.png"
                    subprocess.run(['sips', '-s', 'format', 'png', str(image_path), '--out', str(temp_png)], 
                                 capture_output=True, check=True)
                    image = Image.open(temp_png)
                    temp_png.unlink()  # Clean up temp file
                else:
                    raise e
            
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"OCR error for {image_path.name}: {e}")
            return None
    
    def categorize_document(self, text: str) -> Tuple[str, float]:
        """
        Categorize document and return confidence
        Returns: (category, confidence)
        """
        text_lower = text.lower()
        
        # Bill indicators
        bill_keywords = [
            'amount due', 'payment due', 'total due', 'balance due',
            'invoice', 'bill', 'account number', 'pay by', 'due date',
            'please pay', 'payment', 'statement'
        ]
        bill_score = sum(1 for kw in bill_keywords if kw in text_lower)
        
        # Confidence calculation
        confidence = min(bill_score / 5.0, 1.0)
        
        if confidence >= 0.4:
            return 'bill', confidence
        else:
            return 'reference', confidence
    
    def extract_bill_info(self, text: str) -> Dict:
        """Extract key information from bill"""
        info = {
            'vendor': None,
            'amount': None,
            'due_date': None,
            'account_number': None
        }
        
        # Extract amount (e.g., $125.00, $1,234.56)
        amount_pattern = r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
        amounts = re.findall(amount_pattern, text)
        if amounts:
            # Usually the largest amount is the total due
            info['amount'] = max(amounts, key=lambda x: float(x.replace('$', '').replace(',', '')))
        
        # Extract dates (MM/DD/YYYY, MM-DD-YYYY, Month DD, YYYY)
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, text, re.IGNORECASE)
            if dates:
                info['due_date'] = dates[0]
                break
        
        # Extract account number (various patterns)
        account_patterns = [
            r'Account(?:\s+#|:)?\s*(\d+)',
            r'Acct(?:\s+#|:)?\s*(\d+)'
        ]
        
        for pattern in account_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['account_number'] = match.group(1)
                break
        
        # Try to identify vendor (first line often has company name)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Look for company-like names in first few lines
            for line in lines[:5]:
                if len(line) > 3 and len(line) < 50 and not line.startswith('$'):
                    info['vendor'] = line
                    break
        
        return info
    
    def parse_due_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        if not date_str:
            return None
        
        formats = [
            '%m/%d/%Y',
            '%m-%d-%Y',
            '%m/%d/%y',
            '%B %d, %Y',
            '%b %d, %Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def upload_to_drive(self, file_path: Path, folder_name: str = '8825_Bills') -> Optional[str]:
        """Upload file to Google Drive and return file ID"""
        try:
            # Check if folder exists, create if not
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.drive_service.files().list(q=query, fields='files(id, name)').execute()
            folders = results.get('files', [])
            
            if folders:
                folder_id = folders[0]['id']
            else:
                # Create folder
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = folder['id']
            
            # Upload file
            file_metadata = {
                'name': file_path.name,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(str(file_path), resumable=True)
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            print(f"✓ Uploaded to Drive: {file.get('webViewLink')}")
            return file.get('id')
        
        except Exception as e:
            print(f"Drive upload error: {e}")
            return None
    
    def export_to_csv(self, bill_info: Dict, drive_link: str = None, calendar_link: str = None, image_filename: str = None):
        """Export bill to CSV for Phil's Ledger import"""
        if not CSV_EXPORT_ENABLED:
            return
        
        try:
            # Create export directory
            CSV_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
            
            # CSV file path (one file per month)
            now = datetime.now()
            csv_filename = f"bills_{now.strftime('%Y-%m')}.csv"
            csv_path = CSV_EXPORT_DIR / csv_filename
            
            # Check if file exists to determine if we need headers
            file_exists = csv_path.exists()
            
            # Prepare row data
            vendor = bill_info.get('vendor', 'Unknown')
            amount = bill_info.get('amount', '')
            due_date_str = bill_info.get('due_date', '')
            account = bill_info.get('account_number', '')
            
            # Parse due date for consistent format
            due_date = self.parse_due_date(due_date_str)
            if due_date:
                due_date_formatted = due_date.strftime('%Y-%m-%d')
            else:
                due_date_formatted = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            row = {
                'Date': due_date_formatted,
                'Vendor': vendor,
                'Amount': amount,
                'Category': '',  # To be filled by user
                'Note': f"Account: {account}" if account else '',
                'DriveURL': drive_link or '',
                'CalendarURL': calendar_link or '',
                'Paid': 'false',
                'DueDate': due_date_formatted,
                'PaidDate': '',
                'Account': account,
                'Tags': '',
                'Source': f"bill_processor:{image_filename or 'unknown'}',
                'BankTxnId': ''
            }
            
            # Write to CSV
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                fieldnames = ['Date', 'Vendor', 'Amount', 'Category', 'Note', 'DriveURL', 
                             'CalendarURL', 'Paid', 'DueDate', 'PaidDate', 'Account', 'Tags', 
                             'Source', 'BankTxnId']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Write header if new file
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(row)
            
            print(f"✓ Exported to CSV: {csv_path}")
            
        except Exception as e:
            print(f"CSV export error: {e}")
    
    def create_calendar_event(self, bill_info: Dict, drive_link: str = None) -> Optional[str]:
        """Create Google Calendar event for bill"""
        try:
            vendor = bill_info.get('vendor', 'Unknown')
            amount = bill_info.get('amount', '')
            due_date_str = bill_info.get('due_date')
            
            # Parse due date
            due_date = self.parse_due_date(due_date_str)
            if not due_date:
                # Default to 30 days from now
                due_date = datetime.now() + timedelta(days=30)
            
            # Create event
            event = {
                'summary': f"Bill Due: {vendor} {amount}",
                'description': f"Account: {bill_info.get('account_number', 'N/A')}",
                'start': {
                    'date': due_date.strftime('%Y-%m-%d'),
                    'timeZone': 'America/Chicago',
                },
                'end': {
                    'date': due_date.strftime('%Y-%m-%d'),
                    'timeZone': 'America/Chicago',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 24 * 60},
                    ],
                },
            }
            
            if drive_link:
                event['description'] += f"\n\nDocument: {drive_link}"
            
            event = self.calendar_service.events().insert(calendarId='primary', body=event).execute()
            calendar_link = event.get('htmlLink')
            print(f"✓ Calendar event created: {calendar_link}")
            return calendar_link
            
        except Exception as e:
            print(f"Calendar event error: {e}")
            return None
    
    def process_image(self, image_path: Path) -> Dict:
        """Process a single image"""
        result = {
            'file': image_path.name,
            'category': 'unknown',
            'confidence': 0.0,
            'bill_info': {},
            'processed': False
        }
        
        print(f"\nProcessing: {image_path.name}")
        
        # OCR
        text = self.ocr_image(image_path)
        if not text:
            print("  ✗ OCR failed")
            return result
        
        print(f"  ✓ OCR extracted {len(text)} characters")
        
        # Categorize
        category, confidence = self.categorize_document(text)
        result['category'] = category
        result['confidence'] = confidence
        
        print(f"  → Category: {category} (confidence: {confidence:.2f})")
        
        # If it's a bill, process it
        if category == 'bill' and confidence >= 0.4:
            bill_info = self.extract_bill_info(text)
            result['bill_info'] = bill_info
            
            print(f"  → Vendor: {bill_info.get('vendor', 'Unknown')}")
            print(f"  → Amount: {bill_info.get('amount', 'Unknown')}")
            print(f"  → Due: {bill_info.get('due_date', 'Unknown')}")
            
            # Upload to Drive
            drive_link = self.upload_to_drive(image_path)
            
            # Create calendar event
            calendar_link = self.create_calendar_event(bill_info, drive_link)
            
            # Export to CSV for Phil's Ledger
            self.export_to_csv(bill_info, drive_link, calendar_link, image_path.name)
            
            result['processed'] = True
            result['drive_link'] = drive_link
            result['calendar_link'] = calendar_link
        
        return result
    
    def process_downloads(self):
        """Process all images in Downloads folder"""
        # Supported image formats
        image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.heif']
        
        # Find all images
        images = []
        for ext in image_extensions:
            images.extend(DOWNLOADS_DIR.glob(f'*{ext}'))
            images.extend(DOWNLOADS_DIR.glob(f'*{ext.upper()}'))
        
        if not images:
            print("No images found in Downloads")
            return
        
        print(f"Found {len(images)} images to process")
        
        results = []
        for image_path in images:
            result = self.process_image(image_path)
            results.append(result)
            
            # Move processed files
            if result['processed']:
                PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
                dest = PROCESSED_DIR / image_path.name
                image_path.rename(dest)
                print(f"  ✓ Moved to: {dest}")
        
        # Summary
        print(f"\n{'='*50}")
        print(f"Processed: {len(results)} images")
        print(f"Bills found: {sum(1 for r in results if r['category'] == 'bill')}")
        print(f"Calendar events created: {sum(1 for r in results if r['processed'])}")
        if CSV_EXPORT_ENABLED:
            print(f"CSV exports: {sum(1 for r in results if r['processed'])}")
            print(f"Export location: {CSV_EXPORT_DIR}")

def main():
    processor = BillProcessor()
    processor.process_downloads()

if __name__ == '__main__':
    main()
