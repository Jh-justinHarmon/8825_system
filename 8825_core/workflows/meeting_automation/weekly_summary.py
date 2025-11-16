#!/usr/bin/env python3
"""
Weekly Meeting Summary Generator
Automatically generates and optionally emails weekly TGIF meeting summaries
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from meeting_recall import MeetingRecall

class WeeklySummaryGenerator:
    """Generate weekly meeting summaries"""
    
    def __init__(self, output_dir=None):
        """
        Initialize generator
        
        Args:
            output_dir: Directory to save summaries (default: summaries/)
        """
        self.recall = MeetingRecall()
        
        if output_dir is None:
            output_dir = Path(__file__).parent / "summaries"
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_last_week(self, save=True, email=False):
        """
        Generate summary for last week (Monday-Sunday)
        
        Args:
            save: Save to file
            email: Send via email
            
        Returns:
            Summary markdown string
        """
        # Calculate last week's date range
        today = datetime.now()
        
        # Find last Monday
        days_since_monday = (today.weekday() - 0) % 7
        if days_since_monday == 0:
            days_since_monday = 7  # If today is Monday, go back to last Monday
        
        last_monday = today - timedelta(days=days_since_monday + 7)
        last_sunday = last_monday + timedelta(days=6)
        
        start_date = last_monday.strftime("%Y-%m-%d")
        end_date = last_sunday.strftime("%Y-%m-%d")
        
        return self.generate_summary(start_date, end_date, save=save, email=email)
    
    def generate_this_week(self, save=True, email=False):
        """
        Generate summary for this week so far (Monday-today)
        
        Args:
            save: Save to file
            email: Send via email
            
        Returns:
            Summary markdown string
        """
        today = datetime.now()
        
        # Find this Monday
        days_since_monday = today.weekday()
        this_monday = today - timedelta(days=days_since_monday)
        
        start_date = this_monday.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        
        return self.generate_summary(start_date, end_date, save=save, email=email)
    
    def generate_summary(self, start_date, end_date, save=True, email=False):
        """
        Generate summary for date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            save: Save to file
            email: Send via email
            
        Returns:
            Summary markdown string
        """
        print(f"\n📊 Generating weekly summary: {start_date} to {end_date}")
        
        # Find meetings
        meetings = self.recall.find_meetings(start_date, end_date)
        
        if not meetings:
            print(f"   ⚠️  No meetings found in date range")
            return None
        
        print(f"   ✅ Found {len(meetings)} meeting(s)")
        
        # Generate markdown
        summary = self.recall.generate_summary(meetings, format='markdown')
        
        # Add header with metadata
        header = self._generate_header(start_date, end_date, len(meetings))
        full_summary = header + "\n\n" + summary
        
        # Save to file
        if save:
            filename = f"weekly_summary_{start_date}_to_{end_date}.md"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w') as f:
                f.write(full_summary)
            
            print(f"   💾 Saved to: {filepath}")
        
        # Email if requested
        if email:
            self._send_email(full_summary, start_date, end_date)
        
        return full_summary
    
    def _generate_header(self, start_date, end_date, meeting_count):
        """Generate summary header with metadata"""
        header = f"# TGIF Weekly Meeting Summary\n\n"
        header += f"**Week:** {start_date} to {end_date}  \n"
        header += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n"
        header += f"**Meetings:** {meeting_count}  \n"
        header += f"**System:** 8825 Meeting Automation  \n"
        
        return header
    
    def _send_email(self, summary, start_date, end_date):
        """
        Send summary via email
        
        Args:
            summary: Markdown summary
            start_date: Start date
            end_date: End date
        """
        print(f"\n📧 Sending email...")
        
        # Import email sender (to be implemented)
        try:
            from email_sender import send_meeting_summary
            
            send_meeting_summary(
                summary=summary,
                subject=f"TGIF Weekly Summary: {start_date} to {end_date}",
                recipients=["justin@example.com"]  # TODO: Configure
            )
            
            print(f"   ✅ Email sent")
        
        except ImportError:
            print(f"   ⚠️  Email sender not configured yet")
            print(f"   💡 Run: python3 setup_email.py to configure")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate weekly meeting summaries")
    parser.add_argument("--last-week", action="store_true", help="Generate for last week (Mon-Sun)")
    parser.add_argument("--this-week", action="store_true", help="Generate for this week so far")
    parser.add_argument("--from", dest="start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="end_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--email", action="store_true", help="Send via email")
    parser.add_argument("--no-save", action="store_true", help="Don't save to file")
    parser.add_argument("--output-dir", help="Output directory for summaries")
    
    args = parser.parse_args()
    
    # Create generator
    generator = WeeklySummaryGenerator(output_dir=args.output_dir)
    
    # Generate summary
    if args.last_week:
        summary = generator.generate_last_week(
            save=not args.no_save,
            email=args.email
        )
    elif args.this_week:
        summary = generator.generate_this_week(
            save=not args.no_save,
            email=args.email
        )
    elif args.start_date and args.end_date:
        summary = generator.generate_summary(
            args.start_date,
            args.end_date,
            save=not args.no_save,
            email=args.email
        )
    else:
        # Default: last week
        print("No date range specified, using --last-week")
        summary = generator.generate_last_week(
            save=not args.no_save,
            email=args.email
        )
    
    if summary:
        print(f"\n✅ Summary generated successfully")
        
        if not args.no_save:
            print(f"\n📁 View summary in: {generator.output_dir}")
    else:
        print(f"\n❌ No summary generated")
        sys.exit(1)


if __name__ == "__main__":
    main()
