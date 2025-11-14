#!/usr/bin/env python3
"""
Timesheet Generator
Generates timesheet data in Justin's format from meeting data
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class TimesheetGenerator:
    """Generate timesheet data from meeting transcripts"""
    
    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base = Path(knowledge_base_path)
        self.json_dir = self.knowledge_base / "json"
    
    def generate_timesheet(self, week_ending: str, clients: List[str] = None) -> Dict:
        """
        Generate timesheet for a specific week
        
        Args:
            week_ending: Sunday date in MM/DD/YY format (e.g., "10/19/25")
            clients: List of client names to include
            
        Returns:
            Dict with timesheet data by client and day
        """
        # Parse week ending date
        week_end = datetime.strptime(week_ending, '%m/%d/%y')
        
        # Calculate week start (Monday)
        week_start = week_end - timedelta(days=6)
        
        # Get all meetings for this week
        meetings = self._get_meetings_in_range(
            week_start.strftime('%Y-%m-%d'),
            week_end.strftime('%Y-%m-%d'),
            clients
        )
        
        # Organize by client and day
        timesheet = defaultdict(lambda: {
            'Mon': 0.0, 'Tue': 0.0, 'Wed': 0.0, 
            'Thu': 0.0, 'Fri': 0.0, 'Sat': 0.0, 'Sun': 0.0,
            'Total': 0.0
        })
        
        # Day name mapping (strftime gives full names, we need 3-letter abbrev)
        day_map = {
            0: 'Mon',  # Monday
            1: 'Tue',  # Tuesday
            2: 'Wed',  # Wednesday
            3: 'Thu',  # Thursday
            4: 'Fri',  # Friday
            5: 'Sat',  # Saturday
            6: 'Sun'   # Sunday
        }
        
        for meeting in meetings:
            meeting_date = datetime.strptime(meeting['date'], '%Y-%m-%d')
            day_name = day_map[meeting_date.weekday()]  # Get correct day abbreviation
            client = meeting['client']
            hours = meeting['duration_hours']
            
            timesheet[client][day_name] += hours
            timesheet[client]['Total'] += hours
        
        return {
            'week_ending': week_ending,
            'week_start': week_start.strftime('%m/%d/%y'),
            'data': dict(timesheet)
        }
    
    def _get_meetings_in_range(self, start_date: str, end_date: str, 
                                client_filter: List[str] = None) -> List[Dict]:
        """Get meetings in date range"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        meetings = []
        
        if not self.json_dir.exists():
            return meetings
        
        for json_file in self.json_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                meeting_date = datetime.strptime(data['date'], '%Y-%m-%d')
                
                if start <= meeting_date <= end:
                    title = data['title']
                    
                    # Filter by client
                    if client_filter:
                        if not any(client.upper() in title.upper() for client in client_filter):
                            continue
                    
                    duration_minutes = self._parse_duration(data['metadata'].get('duration', '0'))
                    
                    meetings.append({
                        'date': data['date'],
                        'title': title,
                        'duration_minutes': duration_minutes,
                        'duration_hours': round(duration_minutes / 60, 2),
                        'client': self._extract_client(title)
                    })
            
            except Exception as e:
                continue
        
        return meetings
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse duration string to minutes"""
        if not duration_str or duration_str == 'N/A':
            return 0
        
        duration_str = duration_str.lower().strip()
        minutes = 0
        
        if 'hour' in duration_str or 'h' in duration_str:
            parts = duration_str.replace('hours', 'h').replace('hour', 'h').split('h')
            if parts[0].strip().replace('.', '').isdigit():
                minutes += int(float(parts[0].strip()) * 60)
            
            if len(parts) > 1:
                remaining = parts[1].strip()
                if 'min' in remaining or 'm' in remaining:
                    mins = remaining.replace('minutes', '').replace('minute', '').replace('min', '').replace('m', '').strip()
                    if mins.replace('.', '').isdigit():
                        minutes += int(float(mins))
        
        elif 'min' in duration_str or 'm' in duration_str:
            mins = duration_str.replace('minutes', '').replace('minute', '').replace('min', '').replace('m', '').strip()
            if mins.replace('.', '').isdigit():
                minutes = int(float(mins))
        
        return minutes
    
    def _extract_client(self, title: str) -> str:
        """Extract client name from meeting title"""
        title_upper = title.upper()
        
        if 'TGIF' in title_upper:
            return 'TGIF'
        elif 'HCSS' in title_upper:
            return 'HCSS'
        elif 'RAL' in title_upper:
            return 'RAL'
        elif 'CBM' in title_upper:
            return 'CBM'
        else:
            return 'Other'
    
    def print_timesheet(self, timesheet: Dict, name: str = "Justin H"):
        """Print timesheet in spreadsheet-ready format"""
        
        print("\n" + "=" * 100)
        print(f"TIMESHEET - Week Ending: {timesheet['week_ending']}")
        print("=" * 100)
        print("\nCopy the data below into your spreadsheet:\n")
        
        # Header
        print(f"Name:\t{name}")
        print(f"Week Ending (Sunday):\t{timesheet['week_ending']}")
        print()
        
        # Column headers with dates
        week_end = datetime.strptime(timesheet['week_ending'], '%m/%d/%y')
        dates = []
        for i in range(6, -1, -1):  # Monday to Sunday
            date = week_end - timedelta(days=i)
            dates.append(date.strftime('%m/%d/%y'))
        
        print("Client-Project\t" + "\t".join(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']) + "\tTotal\tComments")
        print("\t" + "\t".join(dates))
        
        # Data rows
        data = timesheet['data']
        
        # Sort clients
        client_order = ['RAL', 'CBM', 'TGIF meetings', 'TGIF', 'HCSS']
        sorted_clients = []
        for client in client_order:
            if client in data:
                sorted_clients.append(client)
        
        # Add any other clients not in the order
        for client in sorted(data.keys()):
            if client not in sorted_clients:
                sorted_clients.append(client)
        
        total_row = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0, 'Total': 0}
        
        for client in sorted_clients:
            row = data[client]
            
            # Determine comment based on client
            if 'meeting' in client.lower():
                comment = 'meeting'
            else:
                comment = 'project assistance'
            
            values = [
                f"{row['Mon']:.2f}" if row['Mon'] > 0 else "",
                f"{row['Tue']:.2f}" if row['Tue'] > 0 else "",
                f"{row['Wed']:.2f}" if row['Wed'] > 0 else "",
                f"{row['Thu']:.2f}" if row['Thu'] > 0 else "",
                f"{row['Fri']:.2f}" if row['Fri'] > 0 else "",
                f"{row['Sat']:.2f}" if row['Sat'] > 0 else "",
                f"{row['Sun']:.2f}" if row['Sun'] > 0 else "",
                f"{row['Total']:.2f}"
            ]
            
            print(f"{client}\t" + "\t".join(values) + f"\t{comment}")
            
            # Add to totals
            for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Total']:
                total_row[day] += row[day]
        
        # Print total row
        print()
        total_values = [
            f"{total_row['Mon']:.2f}",
            f"{total_row['Tue']:.2f}",
            f"{total_row['Wed']:.2f}",
            f"{total_row['Thu']:.2f}",
            f"{total_row['Fri']:.2f}",
            f"{total_row['Sat']:.2f}",
            f"{total_row['Sun']:.2f}",
            f"{total_row['Total']:.2f}"
        ]
        print("TOTAL\t" + "\t".join(total_values))
        
        print("\n" + "=" * 100)
    
    def export_to_csv(self, timesheet: Dict, output_path: Path, name: str = "Justin H"):
        """Export timesheet to CSV for easy import"""
        import csv
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header rows
            writer.writerow(['Name:', name])
            writer.writerow(['Week Ending (Sunday):', timesheet['week_ending']])
            writer.writerow([])
            
            # Column headers
            week_end = datetime.strptime(timesheet['week_ending'], '%m/%d/%y')
            dates = []
            for i in range(6, -1, -1):
                date = week_end - timedelta(days=i)
                dates.append(date.strftime('%m/%d/%y'))
            
            writer.writerow(['Client-Project', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Total', 'Comments'])
            writer.writerow([''] + dates)
            
            # Data rows
            data = timesheet['data']
            client_order = ['RAL', 'CBM', 'TGIF meetings', 'TGIF', 'HCSS']
            sorted_clients = [c for c in client_order if c in data]
            sorted_clients += [c for c in sorted(data.keys()) if c not in sorted_clients]
            
            total_row = [0, 0, 0, 0, 0, 0, 0, 0]
            
            for client in sorted_clients:
                row = data[client]
                comment = 'meeting' if 'meeting' in client.lower() else 'project assistance'
                
                values = [
                    row['Mon'], row['Tue'], row['Wed'], row['Thu'],
                    row['Fri'], row['Sat'], row['Sun'], row['Total']
                ]
                
                writer.writerow([client] + values + [comment])
                
                for i, val in enumerate(values):
                    total_row[i] += val
            
            writer.writerow([])
            writer.writerow(['TOTAL'] + total_row)
        
        print(f"\n✅ Exported to: {output_path}")

def main():
    """Generate timesheet"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 timesheet_generator.py <knowledge_base_path> <week_ending> [clients...]")
        print("\nExample:")
        print("  python3 timesheet_generator.py users/justin_harmon/hcss/knowledge/meetings 10/19/25 HCSS TGIF RAL")
        print("\nWeek ending should be Sunday in MM/DD/YY format")
        sys.exit(1)
    
    knowledge_base = Path(sys.argv[1])
    week_ending = sys.argv[2]
    clients = sys.argv[3:] if len(sys.argv) > 3 else None
    
    generator = TimesheetGenerator(knowledge_base)
    
    # Generate timesheet
    timesheet = generator.generate_timesheet(week_ending, clients)
    
    # Print to console
    generator.print_timesheet(timesheet)
    
    # Export to CSV
    csv_filename = f"timesheet_{week_ending.replace('/', '_')}.csv"
    generator.export_to_csv(timesheet, Path(csv_filename))

if __name__ == '__main__':
    main()
