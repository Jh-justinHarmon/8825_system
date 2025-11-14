#!/usr/bin/env python3
"""
Meeting Time Tracker
Analyzes meeting duration data from processed transcripts
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class MeetingTimeTracker:
    """Track and analyze meeting time by client/project"""
    
    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base = Path(knowledge_base_path)
        self.json_dir = self.knowledge_base / "json"
    
    def get_meetings_in_range(self, start_date: str, end_date: str, 
                               client_filter: List[str] = None) -> List[Dict]:
        """
        Get all meetings within date range
        
        Args:
            start_date: YYYY-MM-DD
            end_date: YYYY-MM-DD
            client_filter: List of client names (e.g., ['HCSS', 'TGIF', 'RAL'])
            
        Returns:
            List of meeting data with duration
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        meetings = []
        
        if not self.json_dir.exists():
            return meetings
        
        for json_file in self.json_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Parse meeting date
                meeting_date = datetime.strptime(data['date'], '%Y-%m-%d')
                
                # Check if in range
                if start <= meeting_date <= end:
                    # Extract client from title
                    title = data['title']
                    
                    # Filter by client if specified
                    if client_filter:
                        if not any(client.upper() in title.upper() for client in client_filter):
                            continue
                    
                    # Parse duration
                    duration_minutes = self._parse_duration(data['metadata'].get('duration', '0'))
                    
                    meetings.append({
                        'date': data['date'],
                        'title': title,
                        'duration_minutes': duration_minutes,
                        'duration_hours': duration_minutes / 60,
                        'client': self._extract_client(title),
                        'source': data['source'],
                        'file': json_file.name
                    })
            
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
                continue
        
        return sorted(meetings, key=lambda x: x['date'])
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse duration string to minutes"""
        if not duration_str or duration_str == 'N/A':
            return 0
        
        duration_str = duration_str.lower().strip()
        
        # Handle "30 min", "1 hour", "1h 30m", etc.
        minutes = 0
        
        if 'hour' in duration_str or 'h' in duration_str:
            # Extract hours
            parts = duration_str.replace('hours', 'h').replace('hour', 'h').split('h')
            if parts[0].strip().isdigit():
                minutes += int(parts[0].strip()) * 60
            
            # Check for remaining minutes
            if len(parts) > 1:
                remaining = parts[1].strip()
                if 'min' in remaining or 'm' in remaining:
                    mins = remaining.replace('minutes', '').replace('minute', '').replace('min', '').replace('m', '').strip()
                    if mins.isdigit():
                        minutes += int(mins)
        
        elif 'min' in duration_str or 'm' in duration_str:
            # Just minutes
            mins = duration_str.replace('minutes', '').replace('minute', '').replace('min', '').replace('m', '').strip()
            if mins.isdigit():
                minutes = int(mins)
        
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
        else:
            return 'Other'
    
    def generate_weekly_breakdown(self, start_date: str, weeks: int = 2, 
                                  clients: List[str] = None) -> Dict:
        """
        Generate weekly breakdown of meeting hours
        
        Args:
            start_date: YYYY-MM-DD (Monday of first week)
            weeks: Number of weeks to analyze
            clients: List of client names to filter
            
        Returns:
            Dict with weekly breakdown by client and day
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        
        # Calculate end date
        end = start + timedelta(weeks=weeks)
        
        # Get all meetings
        meetings = self.get_meetings_in_range(
            start.strftime('%Y-%m-%d'),
            end.strftime('%Y-%m-%d'),
            clients
        )
        
        # Organize by week and day
        breakdown = {}
        
        for week_num in range(weeks):
            week_start = start + timedelta(weeks=week_num)
            week_end = week_start + timedelta(days=6)
            
            week_key = f"Week {week_num + 1} ({week_start.strftime('%b %d')} - {week_end.strftime('%b %d')})"
            breakdown[week_key] = {
                'by_client': defaultdict(float),
                'by_day': defaultdict(lambda: defaultdict(float)),
                'total_hours': 0
            }
            
            # Filter meetings for this week
            for meeting in meetings:
                meeting_date = datetime.strptime(meeting['date'], '%Y-%m-%d')
                
                if week_start <= meeting_date <= week_end:
                    client = meeting['client']
                    day = meeting_date.strftime('%A')
                    hours = meeting['duration_hours']
                    
                    # Add to totals
                    breakdown[week_key]['by_client'][client] += hours
                    breakdown[week_key]['by_day'][day][client] += hours
                    breakdown[week_key]['total_hours'] += hours
        
        return breakdown
    
    def print_breakdown(self, breakdown: Dict):
        """Print formatted breakdown"""
        print("\n" + "=" * 80)
        print("MEETING TIME BREAKDOWN")
        print("=" * 80)
        
        for week, data in breakdown.items():
            print(f"\n{week}")
            print("-" * 80)
            
            # Client totals
            print("\n📊 Hours by Client:")
            for client, hours in sorted(data['by_client'].items()):
                print(f"  {client:15} {hours:6.1f} hours")
            
            print(f"\n  {'TOTAL':15} {data['total_hours']:6.1f} hours")
            
            # Daily breakdown
            print("\n📅 Daily Breakdown:")
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            for day in days:
                if day in data['by_day']:
                    day_total = sum(data['by_day'][day].values())
                    print(f"\n  {day}:")
                    for client, hours in sorted(data['by_day'][day].items()):
                        print(f"    {client:12} {hours:6.1f} hours")
                    print(f"    {'Total':12} {day_total:6.1f} hours")
        
        print("\n" + "=" * 80)
    
    def export_to_csv(self, breakdown: Dict, output_path: Path):
        """Export breakdown to CSV"""
        import csv
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Week', 'Day', 'Client', 'Hours'])
            
            for week, data in breakdown.items():
                for day, clients in data['by_day'].items():
                    for client, hours in clients.items():
                        writer.writerow([week, day, client, hours])
        
        print(f"\n✅ Exported to: {output_path}")

def main():
    """Demo with sample data"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 time_tracker.py <knowledge_base_path> [start_date] [clients...]")
        print("\nExample:")
        print("  python3 time_tracker.py users/justin_harmon/hcss/knowledge/meetings 2025-10-28 HCSS TGIF RAL")
        sys.exit(1)
    
    knowledge_base = Path(sys.argv[1])
    start_date = sys.argv[2] if len(sys.argv) > 2 else "2025-10-28"
    clients = sys.argv[3:] if len(sys.argv) > 3 else None
    
    tracker = MeetingTimeTracker(knowledge_base)
    
    # Generate breakdown
    breakdown = tracker.generate_weekly_breakdown(
        start_date=start_date,
        weeks=2,
        clients=clients
    )
    
    # Print results
    tracker.print_breakdown(breakdown)
    
    # Export to CSV
    csv_path = Path("meeting_time_breakdown.csv")
    tracker.export_to_csv(breakdown, csv_path)

if __name__ == '__main__':
    main()
