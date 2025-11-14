#!/usr/bin/env python3
"""
Quick script to populate an existing Google Sheet
Run this AFTER you've created the sheet manually and shared it
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

def setup_sheet(sheet_url_or_name: str):
    """Connect to existing sheet and populate it"""
    
    # Setup credentials
    credentials_path = Path.home() / '.config' / 'gspread' / 'service_account.json'
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        str(credentials_path), scope
    )
    client = gspread.authorize(creds)
    
    # Open the sheet
    try:
        if sheet_url_or_name.startswith('http'):
            sheet = client.open_by_url(sheet_url_or_name)
        else:
            sheet = client.open(sheet_url_or_name)
        worksheet = sheet.sheet1
        print(f"✓ Connected to: {sheet.title}")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nMake sure you:")
        print("1. Created the sheet in Google Sheets")
        print("2. Shared it with: tgif-schedules@mythic-evening-477708-a3.iam.gserviceaccount.com")
        print("3. Gave it Editor access")
        return None
    
    # Clear existing content
    worksheet.clear()
    
    # Add headers
    headers = [
        "Date", "Day", "Store ID", "Location", 
        "Toast Equipment Status", "Network Equipment Needed",
        "Network Equipment Status", "On-Site Resources Status", "Notes"
    ]
    worksheet.update('A1:I1', [headers])
    
    # Add data
    data = [
        ["11/18/2025", "Tuesday", "1191", "Midlothian, VA", 
         "Arrived - On-site ready to install", "PRNSC24P 24 port switch + 5 APs",
         "NEEDS TO SHIP BEFORE 11-18", "Unknown", 
         "Equipment must arrive before installation date"],
        
        ["11/18/2025", "Tuesday", "1887", "Dover, DE",
         "Arrived - On-site ready to install", "Unknown", "Unknown", "Unknown", ""],
        
        ["11/18/2025", "Tuesday", "1548", "Erie, PA",
         "UNKNOWN - NEEDS STATUS CHECK", "Unknown", "Unknown",
         "UNKNOWN - NEEDS STATUS CHECK", "Both equipment and resource status needed"],
        
        ["11/19/2025", "Wednesday", "1412", "Brooklyn, OH",
         "UNKNOWN - NEEDS STATUS CHECK", "Unknown", "Unknown",
         "UNKNOWN - NEEDS STATUS CHECK", "Both equipment and resource status needed"],
        
        ["11/19/2025", "Wednesday", "4156", "Hollywood, CA",
         "UNKNOWN - NEEDS STATUS CHECK", "Unknown", "Unknown",
         "UNKNOWN - NEEDS STATUS CHECK", "Both equipment and resource status needed"]
    ]
    
    worksheet.update('A2:I6', data)
    
    # Format headers
    worksheet.format('A1:I1', {
        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
    })
    
    # Auto-resize columns
    worksheet.columns_auto_resize(0, 8)
    
    print(f"✓ Sheet populated with {len(data)} stores")
    print(f"✓ Sheet URL: {sheet.url}")
    
    return sheet


if __name__ == "__main__":
    print("="*60)
    print("TOAST INSTALLATION SCHEDULE - SHEET SETUP")
    print("="*60)
    print("\nService Account Email:")
    print("tgif-schedules@mythic-evening-477708-a3.iam.gserviceaccount.com")
    print("\nSteps:")
    print("1. Go to sheets.google.com")
    print("2. Create a new sheet (any name)")
    print("3. Share it with the email above (Editor access)")
    print("4. Copy the sheet URL or name")
    print("="*60)
    
    sheet_input = input("\nEnter sheet URL or name: ").strip()
    
    if sheet_input:
        setup_sheet(sheet_input)
    else:
        print("No input provided. Exiting.")
