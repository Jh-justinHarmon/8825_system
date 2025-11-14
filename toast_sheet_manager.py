#!/usr/bin/env python3
"""
Toast Installation Schedule Manager - Google Sheets Integration
Allows dynamic updates to the installation tracking spreadsheet
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path

class ToastScheduleManager:
    def __init__(self, credentials_path: str = None):
        """Initialize Google Sheets connection"""
        if credentials_path is None:
            credentials_path = Path.home() / '.config' / 'gspread' / 'service_account.json'
        
        self.credentials_path = Path(credentials_path)
        self.sheet = None
        self.worksheet = None
        
    def connect(self, sheet_name: str = "Toast Installation Schedule"):
        """Connect to Google Sheets"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Credentials not found at {self.credentials_path}\n"
                "Please set up Google Sheets API credentials first."
            )
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(self.credentials_path), scope
        )
        client = gspread.authorize(creds)
        
        # Open or create the sheet
        try:
            self.sheet = client.open(sheet_name)
            self.worksheet = self.sheet.sheet1
            print(f"✓ Connected to existing sheet: {sheet_name}")
        except gspread.SpreadsheetNotFound:
            self.sheet = client.create(sheet_name)
            self.worksheet = self.sheet.sheet1
            self._initialize_sheet()
            print(f"✓ Created new sheet: {sheet_name}")
        
        return self.worksheet
    
    def _initialize_sheet(self):
        """Set up initial headers and formatting"""
        headers = [
            "Date", "Day", "Store ID", "Location", 
            "Toast Equipment Status", "Network Equipment Needed",
            "Network Equipment Status", "On-Site Resources Status", "Notes"
        ]
        self.worksheet.update('A1:I1', [headers])
        
        # Initial data
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
        
        self.worksheet.update('A2:I6', data)
        
        # Format headers
        self.worksheet.format('A1:I1', {
            "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        })
    
    def update_store_status(self, store_id: str, **kwargs):
        """Update status for a specific store
        
        Args:
            store_id: Store ID to update
            **kwargs: Fields to update (toast_status, network_equipment, 
                     network_status, onsite_status, notes)
        """
        # Find the row for this store
        cell = self.worksheet.find(store_id)
        if not cell:
            print(f"✗ Store {store_id} not found")
            return False
        
        row = cell.row
        
        # Column mapping
        col_map = {
            'toast_status': 5,  # E
            'network_equipment': 6,  # F
            'network_status': 7,  # G
            'onsite_status': 8,  # H
            'notes': 9  # I
        }
        
        # Update each field
        for field, value in kwargs.items():
            if field in col_map:
                col = col_map[field]
                self.worksheet.update_cell(row, col, value)
                print(f"✓ Updated {store_id} - {field}: {value}")
        
        return True
    
    def add_store(self, date: str, day: str, store_id: str, location: str, **kwargs):
        """Add a new store to the schedule"""
        row_data = [
            date, day, store_id, location,
            kwargs.get('toast_status', 'Unknown'),
            kwargs.get('network_equipment', 'Unknown'),
            kwargs.get('network_status', 'Unknown'),
            kwargs.get('onsite_status', 'Unknown'),
            kwargs.get('notes', '')
        ]
        
        self.worksheet.append_row(row_data)
        print(f"✓ Added store {store_id} - {location}")
    
    def get_all_stores(self):
        """Get all store data"""
        return self.worksheet.get_all_records()
    
    def get_stores_needing_attention(self):
        """Get stores that need status checks or have issues"""
        all_stores = self.get_all_stores()
        needs_attention = []
        
        for store in all_stores:
            if any([
                'UNKNOWN' in str(store.get('Toast Equipment Status', '')),
                'UNKNOWN' in str(store.get('On-Site Resources Status', '')),
                'NEEDS' in str(store.get('Network Equipment Status', ''))
            ]):
                needs_attention.append(store)
        
        return needs_attention
    
    def mark_complete(self, store_id: str):
        """Mark a store installation as complete"""
        self.update_store_status(
            store_id,
            toast_status="✓ Installed",
            network_status="✓ Installed",
            onsite_status="✓ Complete",
            notes=f"Completed on {datetime.now().strftime('%m/%d/%Y %H:%M')}"
        )


def main():
    """Example usage"""
    manager = ToastScheduleManager()
    
    # Connect to sheet
    manager.connect("Toast Installation Schedule")
    
    # Example updates
    print("\n" + "="*60)
    print("EXAMPLE UPDATES")
    print("="*60)
    
    # Update a store status
    manager.update_store_status(
        "1548",
        toast_status="Shipped - Arriving 11/17",
        onsite_status="Scheduled for 11/18 9am"
    )
    
    # Get stores needing attention
    print("\n" + "="*60)
    print("STORES NEEDING ATTENTION")
    print("="*60)
    needs_attention = manager.get_stores_needing_attention()
    for store in needs_attention:
        print(f"\n{store['Store ID']} - {store['Location']}")
        print(f"  Toast: {store['Toast Equipment Status']}")
        print(f"  On-site: {store['On-Site Resources Status']}")


if __name__ == "__main__":
    main()
