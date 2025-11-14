#!/usr/bin/env python3
"""
Flight Pickup Timing Calculator
Quick tool to calculate when to leave for airport pickup
"""

import sys
from datetime import datetime, timedelta
import requests

class FlightPickupCalculator:
    def __init__(self):
        self.home_address = "7247 Whispering Pines Dr, Dallas, TX 75248"
        self.default_airport = "DFW"
        self.default_drive_time = 35  # minutes to DFW
        self.default_buffer = 5  # minutes
    
    def get_flight_status(self, flight_number, date=None):
        """Get flight arrival time from FlightStats"""
        if date is None:
            date = datetime.now()
        
        # For now, return scheduled times
        # TODO: Integrate real-time flight API
        print(f"Checking {flight_number} for {date.strftime('%Y-%m-%d')}...")
        print("Note: Using scheduled times. Check FlightStats for real-time status.")
        return None
    
    def calculate_departure_time(self, arrival_time_str, drive_minutes=None, buffer_minutes=None):
        """Calculate when to leave home
        
        Args:
            arrival_time_str: Flight arrival in format "2:22 PM" or "14:22"
            drive_minutes: Drive time (default: 35 for DFW)
            buffer_minutes: Buffer time (default: 5)
        """
        drive_minutes = drive_minutes or self.default_drive_time
        buffer_minutes = buffer_minutes or self.default_buffer
        
        # Parse arrival time
        try:
            if 'PM' in arrival_time_str.upper() or 'AM' in arrival_time_str.upper():
                arrival_time = datetime.strptime(arrival_time_str, "%I:%M %p")
            else:
                arrival_time = datetime.strptime(arrival_time_str, "%H:%M")
            
            # Set to today
            now = datetime.now()
            arrival_time = arrival_time.replace(year=now.year, month=now.month, day=now.day)
        except ValueError:
            print(f"Error: Could not parse time '{arrival_time_str}'")
            print("Use format: '2:22 PM' or '14:22'")
            return None
        
        # Calculate departure
        total_time = drive_minutes + buffer_minutes
        departure_time = arrival_time - timedelta(minutes=total_time)
        airport_arrival = departure_time + timedelta(minutes=drive_minutes)
        
        # Display result
        print(f"\n🚗 Leave home by: {departure_time.strftime('%I:%M %p')}")
        
        # Show time until
        now = datetime.now()
        if departure_time > now:
            time_until = departure_time - now
            minutes_until = int(time_until.total_seconds() / 60)
            print(f"   ({minutes_until} minutes from now)")
        
        return departure_time
    
    def quick_lookup(self, flight_number):
        """Quick lookup for common flights"""
        # DL417 schedule
        if flight_number.upper() == "DL417":
            print("\nDL417 operates twice daily:")
            print("  1. LGA→DFW: Arrives 2:22 PM CST")
            print("  2. DFW→LGA: Departs 3:12 PM CST")
            print("\nWhich arrival are you picking up? (Enter time like '2:22 PM')")
            return
        
        print(f"Flight {flight_number} not in quick lookup database.")
        print("Enter arrival time manually.")


def main():
    calc = FlightPickupCalculator()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 flight_pickup_calculator.py <arrival_time>")
        print("  python3 flight_pickup_calculator.py <flight_number>")
        print("\nExamples:")
        print("  python3 flight_pickup_calculator.py '2:22 PM'")
        print("  python3 flight_pickup_calculator.py DL417")
        print("  python3 flight_pickup_calculator.py '14:22' 40 10  # custom drive/buffer")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    # Check if it's a flight number or time
    if arg.upper().startswith('DL') or arg.upper().startswith('AA') or arg.upper().startswith('UA'):
        calc.quick_lookup(arg)
    else:
        # It's a time
        drive_time = int(sys.argv[2]) if len(sys.argv) > 2 else None
        buffer_time = int(sys.argv[3]) if len(sys.argv) > 3 else None
        calc.calculate_departure_time(arg, drive_time, buffer_time)


if __name__ == "__main__":
    main()
