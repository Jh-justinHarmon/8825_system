#!/usr/bin/env python3
"""
Create master Toast schedule sheet matching the format from the image
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import os

def create_master_schedule():
    """Create new master schedule sheet"""
    
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
    
    # Create new sheet
    sheet = client.create("Toast Master Schedule")
    worksheet = sheet.sheet1
    
    print(f"✓ Created sheet: {sheet.title}")
    print(f"✓ URL: {sheet.url}")
    
    # Set up headers (matching image format)
    headers = [
        "#",
        "Franchisee", 
        "GT Contract Signed?",
        "Toast Contract Signed?",
        "Restaurant",
        "Go-Live",
        "Actual Go-Live",
        "Day of Week",
        "Equipment Arrival",
        "Support",
        ""  # Empty column L
    ]
    
    worksheet.update('A13:L13', [headers])
    
    # Format header row
    worksheet.format('A13:L13', {
        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER"
    })
    
    # Add data rows (starting from row 14)
    data = [
        # Row 1 (14)
        [1, "Sugarloaf Hospitality", "Y", "Y", "64169-VALLEY STREAM, NY", "N/A", "N/A", "N/A", "", ""],
        # Row 2 (15)
        [2, "Sugarloaf Hospitality", "Y", "Y", "64170-CENTRAL ISLIP, NY", "N/A", "N/A", "N/A", "", ""],
        # Row 3 (16)
        [3, "Sugarloaf Hospitality", "Y", "Y", "64164-STOUGHTON, MA", "11/4/25", "11/4/25", "Tue", "", ""],
        # Row 4 (17)
        [4, "Sugarloaf Hospitality", "Y", "Y", "64157-METHUEN, MA", "11/5/25", "11/5/25", "Wed", "", ""],
        # Row 5 (18)
        [5, "Sugarloaf Hospitality", "Y", "Y", "64160-EVERETT, MA", "11/11/25", "11/11/25", "Tue", "", ""],
        # Row 6 (19)
        [6, "Sugarloaf Hospitality", "Y", "Y", "64158-BOSTON/HAM CIRCLE, MA", "11/11/25", "11/11/25", "Tue", "", ""],
        # Row 7 (20)
        [7, "Sugarloaf Hospitality", "Y", "Y", "64163-MILLBURY, MA", "11/11/25", "11/11/25", "Tue", "", ""],
        # Row 8 (21)
        [8, "Sugarloaf Hospitality", "Y", "Y", "61521-NEWARK, DE", "11/12/25", "11/12/25", "Wed", "", ""],
        # Row 9 (22) - Dover, DE with updated info
        [9, "Sugarloaf Hospitality", "Y", "Y", "61887-DOVER, DE", "11/12/25", "11/18/25", "Tue", "Delivered 11/12", "Rescheduled - Toast avail 11/25"],
        # Row 10 (23)
        [10, "Ohana's, LLC", "Y", "Y", "61191-RICHMOND/SWIFT CREEK, VA", "11/12/25", "11/18/25", "Tue", "", ""],
        # Row 11 (24)
        [11, "Sugarloaf Hospitality", "Y", "Y", "61548-ERIE, PA", "11/18/25", "11/18/25", "Tue", "Delivered 11/12", ""],
        # Row 12 (25)
        [12, "Sugarloaf Hospitality", "Y", "Y", "61412-BROOKLYN, OH", "11/19/25", "11/19/25", "Wed", "Delivered 11/11", ""],
        # Row 13 (26)
        [13, "Sugarloaf Hospitality", "Y", "Y", "64156-HOLLYWOOD HGT, CA", "11/19/25", "11/19/25", "Wed", "Delivered 11/12", "Onsite not confirmed"],
    ]
    
    worksheet.update('A14:K26', data)
    
    # Format data rows
    worksheet.format('A14:K26', {
        "horizontalAlignment": "LEFT",
        "wrapStrategy": "WRAP"
    })
    
    # Center align specific columns
    worksheet.format('A14:A26', {"horizontalAlignment": "CENTER"})  # #
    worksheet.format('C14:D26', {"horizontalAlignment": "CENTER"})  # Y columns
    worksheet.format('F14:H26', {"horizontalAlignment": "CENTER"})  # Date columns
    
    # Auto-resize columns
    worksheet.columns_auto_resize(0, 11)
    
    print(f"\n✓ Sheet populated with {len(data)} stores")
    print(f"\nShare with: tgif-schedules@mythic-evening-477708-a3.iam.gserviceaccount.com")
    
    return sheet


if __name__ == "__main__":
    print("="*60)
    print("CREATING TOAST MASTER SCHEDULE")
    print("="*60)
    print()
    
    sheet = create_master_schedule()
    
    print("\n" + "="*60)
    print("COMPLETE")
    print("="*60)
    print(f"\nSheet URL: {sheet.url}")
    print("\nDon't forget to share with the service account!")
