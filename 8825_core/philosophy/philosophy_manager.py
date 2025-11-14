#!/usr/bin/env python3
"""
Philosophy Manager - Orchestrate philosophy evolution

Coordinates:
- Learning extraction from sessions
- Principle usage tracking
- Decay monitoring
- Report generation

Main entry point for philosophy automation.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json

from learning_extractor import LearningExtractor
from principle_tracker import PrincipleTracker
from decay_monitor import DecayMonitor
from philosophy_validator import validate_philosophy

class PhilosophyManager:
    """Orchestrate philosophy evolution and maintenance"""
    
    def __init__(self, philosophy_path: Path = None):
        if philosophy_path is None:
            philosophy_path = Path(__file__).parent.parent.parent / "PHILOSOPHY.md"
        
        self.philosophy_path = philosophy_path
        self.extractor = LearningExtractor(philosophy_path)
        self.tracker = PrincipleTracker(philosophy_path)
        self.monitor = DecayMonitor(philosophy_path)
    
    def process_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a session end-to-end
        
        Args:
            session_data: Session transcript and metadata
        
        Returns:
            {
                'learnings': {...},
                'proposals': [...],
                'validations': [...],
                'report_path': '...'
            }
        """
        print("\n" + "="*80)
        print("PROCESSING SESSION")
        print("="*80 + "\n")
        
        # Validate philosophy format first
        print("🔍 Validating PHILOSOPHY.md format...")
        is_valid, errors, warnings = validate_philosophy(self.philosophy_path)
        
        if not is_valid:
            print(f"❌ PHILOSOPHY.md has {len(errors)} error(s):")
            for error in errors[:5]:  # Show first 5
                print(f"  • {error}")
            print("\n⚠️  Please fix errors before processing session")
            return {
                'error': 'Invalid PHILOSOPHY.md format',
                'errors': errors,
                'warnings': warnings
            }
        
        if warnings:
            print(f"⚠️  {len(warnings)} warning(s) in PHILOSOPHY.md")
        
        # Extract learnings
        print("\n📚 Extracting learnings...")
        learnings = self.extractor.extract_from_session(session_data)
        
        # Update use counts for validated principles
        print("\n✅ Updating validated principles...")
        for validation in learnings['validations']:
            self.tracker.record_usage(
                validation['principle'],
                f"Validated by session: {session_data.get('objective')}",
                impact_type="validation"
            )
        
        # Generate learning report
        report_dir = Path(__file__).parent / "reports"
        report_dir.mkdir(exist_ok=True)
        
        date_str = session_data.get('date', datetime.now().strftime("%Y-%m-%d"))
        report_path = report_dir / f"learning_report_{date_str}.md"
        
        self.extractor.generate_report(learnings, report_path)
        
        return {
            'learnings': learnings,
            'proposals': learnings['proposed_principles'],
            'validations': learnings['validations'],
            'report_path': str(report_path)
        }
    
    def record_principle_usage(self, principle_title: str, context: str, 
                              impact_type: Optional[str] = None) -> bool:
        """Record that a principle was used during decision-making"""
        return self.tracker.record_usage(principle_title, context, impact_type)
    
    def run_weekly_maintenance(self, auto_deprecate: bool = False) -> Dict[str, Any]:
        """Run weekly philosophy maintenance
        
        Args:
            auto_deprecate: If True, auto-deprecate stale principles
        
        Returns:
            {
                'usage_stats': {...},
                'decay_status': {...},
                'deprecated': [...],
                'reports': {...}
            }
        """
        print("\n" + "="*80)
        print("WEEKLY PHILOSOPHY MAINTENANCE")
        print("="*80 + "\n")
        
        # Get usage stats
        print("📊 Generating usage stats...")
        usage_stats = self.tracker.get_usage_stats()
        
        # Check decay
        print("\n⏰ Checking for decay...")
        decay_status = self.monitor.check_decay()
        
        # Auto-deprecate if enabled
        deprecated = []
        if auto_deprecate:
            print("\n🗑️  Auto-deprecating stale principles...")
            deprecated = self.monitor.auto_deprecate_stale(dry_run=False)
        else:
            print("\n[DRY RUN] Would deprecate:")
            self.monitor.auto_deprecate_stale(dry_run=True)
        
        # Generate reports
        report_dir = Path(__file__).parent / "reports"
        report_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        usage_report_path = report_dir / f"usage_report_{date_str}.md"
        usage_report = self.tracker.generate_usage_report()
        usage_report_path.write_text(usage_report)
        
        decay_report_path = report_dir / f"decay_report_{date_str}.md"
        decay_report = self.monitor.generate_decay_report()
        decay_report_path.write_text(decay_report)
        
        print(f"\n✅ Reports generated:")
        print(f"   - {usage_report_path}")
        print(f"   - {decay_report_path}")
        
        return {
            'usage_stats': usage_stats,
            'decay_status': decay_status,
            'deprecated': deprecated,
            'reports': {
                'usage': str(usage_report_path),
                'decay': str(decay_report_path)
            }
        }
    
    def get_dashboard(self) -> str:
        """Get philosophy health dashboard"""
        usage_stats = self.tracker.get_usage_stats()
        decay_status = self.monitor.check_decay()
        
        dashboard = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PHILOSOPHY HEALTH DASHBOARD                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 USAGE STATISTICS
   Total Principles: {usage_stats['total_principles']}
   Total Uses: {usage_stats['total_uses']}
   Average Uses: {usage_stats['total_uses'] / max(usage_stats['total_principles'], 1):.1f}

🏆 MOST USED
   {usage_stats['most_used']['title']} ({usage_stats['most_used']['count']} uses)

⚠️  DECAY STATUS
   Healthy: {len(decay_status['healthy'])}
   Decaying: {len(decay_status['decaying'])} (30-89 days)
   Deprecated: {len(decay_status['deprecated'])} (90+ days)

❌ NEVER USED
   {len(usage_stats['never_used'])} principles

✨ PROMOTION CANDIDATES
"""
        
        # Check for promotion candidates
        promotion_count = 0
        for title in usage_stats['recently_used']:
            recommendation = self.tracker.check_for_promotion(title)
            if recommendation:
                dashboard += f"   - {title}\n"
                promotion_count += 1
        
        if promotion_count == 0:
            dashboard += "   None\n"
        
        dashboard += "\n" + "="*80 + "\n"
        
        return dashboard

def main():
    """Example usage"""
    manager = PhilosophyManager()
    
    # Show dashboard
    print(manager.get_dashboard())
    
    # Example: Process a session
    session_data = {
        'date': '2025-11-11',
        'objective': 'Build philosophy automation',
        'transcript': 'We learned that automation should be fully automated...',
        'outcomes': ['Philosophy manager created']
    }
    
    # Uncomment to test:
    # result = manager.process_session(session_data)
    # print(f"\nSession processed: {result['report_path']}")
    
    # Run weekly maintenance (dry run)
    # result = manager.run_weekly_maintenance(auto_deprecate=False)

if __name__ == '__main__':
    main()
