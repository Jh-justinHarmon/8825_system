#!/usr/bin/env python3
"""
Track Protocol - CLI tool for recording protocol usage

Quick command-line interface for tracking when you consult a protocol.

Usage:
    # Record successful use
    ./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --success --context "Debugging sync"
    
    # Record failure
    ./track_protocol.py WORKFLOW_ORCHESTRATION --fail --context "Too complex" --notes "Need simpler version"
    
    # List all protocols
    ./track_protocol.py --list
    
    # Show usage report
    ./track_protocol.py --report
    
    # Show specific protocol stats
    ./track_protocol.py DEEP_DIVE_RESEARCH_PROTOCOL --stats
"""

import sys
import argparse
from pathlib import Path
from protocol_tracker import ProtocolTracker

def main():
    parser = argparse.ArgumentParser(
        description="Track protocol usage (Proof Protocol)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record successful use
  %(prog)s DEEP_DIVE_RESEARCH_PROTOCOL --success --context "Debugging"
  
  # Record failure
  %(prog)s WORKFLOW_ORCHESTRATION --fail --notes "Too complex"
  
  # List protocols
  %(prog)s --list
  
  # Show report
  %(prog)s --report
  
  # Show stats for specific protocol
  %(prog)s DEEP_DIVE_RESEARCH_PROTOCOL --stats
        """
    )
    
    # Protocol to track
    parser.add_argument('protocol', nargs='?', help='Protocol ID (filename without extension)')
    
    # Success/failure
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--success', '-s', action='store_true', help='Protocol worked')
    group.add_argument('--fail', '-f', action='store_true', help='Protocol failed')
    
    # Context
    parser.add_argument('--context', '-c', default='', help='What task/project was this for?')
    parser.add_argument('--notes', '-n', default='', help='Additional notes')
    
    # Actions
    parser.add_argument('--list', '-l', action='store_true', help='List all protocols')
    parser.add_argument('--report', '-r', action='store_true', help='Generate usage report')
    parser.add_argument('--stats', action='store_true', help='Show stats for specific protocol')
    parser.add_argument('--status', choices=['promoted', 'active', 'decaying', 'deprecated', 'unused'],
                       help='Filter by status')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = ProtocolTracker()
    
    # Handle actions
    if args.list:
        print("📋 Available Protocols\n")
        protocols = tracker.list_protocols(status=args.status)
        
        for p in protocols:
            status_icon = {
                'promoted': '✨',
                'active': '✅',
                'decaying': '⏳',
                'deprecated': '❌',
                'unused': '🆕'
            }.get(p['status'], '•')
            
            print(f"{status_icon} {p['name']}")
            print(f"   ID: {p['id']}")
            print(f"   Uses: {p['use_count']}, Success: {p['success_rate']:.0%}, Status: {p['status']}")
            print()
        
        print(f"Total: {len(protocols)} protocols")
        if args.status:
            print(f"Filtered by: {args.status}")
        
        return
    
    if args.report:
        print(tracker.generate_usage_report())
        return
    
    if args.stats:
        if not args.protocol:
            print("❌ Error: Must specify protocol ID with --stats")
            return
        
        stats = tracker.get_usage_stats(args.protocol)
        if not stats:
            print(f"❌ Protocol not found: {args.protocol}")
            return
        
        protocol = tracker.protocols[args.protocol]
        print(f"\n📊 Stats for: {protocol['name']}\n")
        print(f"ID: {args.protocol}")
        print(f"File: {protocol['file']}")
        print(f"Type: {protocol['type']}")
        print()
        print(f"Use Count: {stats['use_count']}")
        print(f"Successes: {stats['successes']}")
        print(f"Failures: {stats['failures']}")
        print(f"Success Rate: {stats['success_rate']:.0%}")
        print(f"Status: {stats['status']}")
        print(f"Confidence: {stats['confidence']:.0%}")
        print()
        if stats['contexts']:
            print(f"Contexts: {', '.join(stats['contexts'])}")
        if stats['last_used']:
            print(f"Last Used: {stats['last_used']}")
        
        return
    
    # Record usage
    if not args.protocol:
        print("❌ Error: Must specify protocol ID")
        print("Use --list to see available protocols")
        return
    
    if not args.success and not args.fail:
        print("❌ Error: Must specify --success or --fail")
        return
    
    success = args.success
    
    # Record
    result = tracker.record_usage(
        args.protocol,
        success=success,
        context=args.context,
        notes=args.notes
    )
    
    if result:
        print(f"\n{'✅' if success else '❌'} Recorded: {args.protocol}")
        
        # Show updated stats
        stats = tracker.get_usage_stats(args.protocol)
        print(f"   Status: {stats['status']}")
        print(f"   Total uses: {stats['use_count']}")
        print(f"   Success rate: {stats['success_rate']:.0%}")


if __name__ == '__main__':
    main()
