#!/usr/bin/env python3
"""
Time Calibration System - Recalibrate estimates based on actual performance
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta


@dataclass
class TaskEstimate:
    """Task with estimate and actual time"""
    task: str
    estimated_minutes: int
    actual_minutes: int
    complexity: str  # simple, medium, complex, system-wide
    
    @property
    def accuracy_ratio(self) -> float:
        """How accurate was the estimate? (actual/estimated)"""
        return self.actual_minutes / self.estimated_minutes if self.estimated_minutes > 0 else 1.0


class TimeCalibrator:
    """Calibrate time estimates based on historical performance"""
    
    # Session data from 2025-11-08 (Inbox Ingestion System build)
    SESSION_DATA = [
        # Phase 0: Foundation
        TaskEstimate("Build validator", 10, 5, "medium"),
        TaskEstimate("Build classifier", 15, 8, "complex"),
        TaskEstimate("Build weighting system", 10, 5, "medium"),
        TaskEstimate("Build router", 5, 3, "simple"),
        
        # Phase 1: Lane A
        TaskEstimate("Build deduplicator", 15, 10, "medium"),
        TaskEstimate("Build Lane A processor", 20, 12, "complex"),
        TaskEstimate("Create index system", 10, 5, "medium"),
        TaskEstimate("Test Lane A flow", 10, 8, "medium"),
        
        # Phase 2: Lane B
        TaskEstimate("Build AI sweep engine", 25, 15, "complex"),
        TaskEstimate("Build pattern searcher", 15, 0, "complex"),  # Integrated into sweep
        TaskEstimate("Build teaching ticket generator", 20, 12, "complex"),
        TaskEstimate("Build Lane B processor", 10, 5, "simple"),
        TaskEstimate("Test Lane B flow", 10, 5, "medium"),
        
        # Option B: Docs + CLI
        TaskEstimate("Create README", 15, 10, "medium"),
        TaskEstimate("Build ticket review CLI", 15, 8, "medium"),
        
        # Option C: Production improvements
        TaskEstimate("Add search exclusions", 10, 5, "medium"),
        TaskEstimate("Improve summary extraction", 10, 5, "medium"),
        TaskEstimate("Add relevance filtering", 15, 8, "complex"),
        TaskEstimate("Test improvements", 10, 5, "medium"),
        TaskEstimate("Final documentation", 15, 8, "medium"),
        
        # Meeting Prep System
        TaskEstimate("Create meeting prep structure", 20, 12, "complex"),
        TaskEstimate("Build prep generator", 25, 15, "complex"),
        TaskEstimate("Build calendar analyzer", 15, 0, "medium"),  # Not needed
        TaskEstimate("Create CLI interface", 20, 10, "complex"),
        TaskEstimate("Test with example", 10, 5, "simple"),
    ]
    
    def __init__(self):
        self.session_data = self.SESSION_DATA
    
    def calculate_calibration_factors(self) -> Dict[str, float]:
        """Calculate calibration factors by complexity"""
        by_complexity = {
            'simple': [],
            'medium': [],
            'complex': [],
            'system-wide': []
        }
        
        # Group by complexity
        for task in self.session_data:
            if task.actual_minutes > 0:  # Only count completed tasks
                by_complexity[task.complexity].append(task.accuracy_ratio)
        
        # Calculate average ratio for each complexity
        factors = {}
        for complexity, ratios in by_complexity.items():
            if ratios:
                avg_ratio = sum(ratios) / len(ratios)
                factors[complexity] = avg_ratio
            else:
                factors[complexity] = 1.0
        
        return factors
    
    def get_session_stats(self) -> Dict:
        """Get overall session statistics"""
        completed_tasks = [t for t in self.session_data if t.actual_minutes > 0]
        
        total_estimated = sum(t.estimated_minutes for t in completed_tasks)
        total_actual = sum(t.actual_minutes for t in completed_tasks)
        
        return {
            'total_tasks': len(completed_tasks),
            'total_estimated_minutes': total_estimated,
            'total_actual_minutes': total_actual,
            'overall_ratio': total_actual / total_estimated if total_estimated > 0 else 1.0,
            'efficiency': (total_estimated / total_actual) if total_actual > 0 else 1.0,
            'time_saved_minutes': total_estimated - total_actual,
            'accuracy_percentage': (total_actual / total_estimated * 100) if total_estimated > 0 else 100
        }
    
    def calibrate_estimate(self, task_description: str, initial_estimate_minutes: int, 
                          complexity: str = 'medium') -> Dict:
        """
        Calibrate a new estimate based on historical performance
        
        Args:
            task_description: What the task is
            initial_estimate_minutes: Your initial gut estimate
            complexity: simple, medium, complex, system-wide
        
        Returns:
            Dict with calibrated estimate and confidence
        """
        factors = self.calculate_calibration_factors()
        calibration_factor = factors.get(complexity, 1.0)
        
        # Apply calibration
        calibrated_minutes = int(initial_estimate_minutes * calibration_factor)
        
        # Calculate confidence based on sample size
        complexity_tasks = [t for t in self.session_data 
                          if t.complexity == complexity and t.actual_minutes > 0]
        confidence = min(len(complexity_tasks) / 5.0, 1.0)  # Max confidence at 5+ samples
        
        return {
            'task': task_description,
            'initial_estimate_minutes': initial_estimate_minutes,
            'calibration_factor': calibration_factor,
            'calibrated_estimate_minutes': calibrated_minutes,
            'complexity': complexity,
            'confidence': confidence,
            'sample_size': len(complexity_tasks),
            'recommendation': self._get_recommendation(calibration_factor)
        }
    
    def _get_recommendation(self, factor: float) -> str:
        """Get recommendation based on calibration factor"""
        if factor < 0.5:
            return "You're 2x faster than estimated - trust your speed"
        elif factor < 0.7:
            return "You're significantly faster - reduce estimates by ~30%"
        elif factor < 0.9:
            return "You're slightly faster - reduce estimates by ~10%"
        elif factor < 1.1:
            return "Your estimates are accurate - keep current approach"
        elif factor < 1.3:
            return "You're slightly slower - add 10-20% buffer"
        else:
            return "You're significantly slower - add 30%+ buffer or break down tasks"
    
    def generate_report(self) -> str:
        """Generate calibration report"""
        stats = self.get_session_stats()
        factors = self.calculate_calibration_factors()
        
        report = f"""
# Time Calibration Report
**Session Date**: 2025-11-08 (Inbox Ingestion + Meeting Prep)

## Overall Performance

- **Tasks Completed**: {stats['total_tasks']}
- **Total Estimated**: {stats['total_estimated_minutes']} minutes ({stats['total_estimated_minutes']/60:.1f} hours)
- **Total Actual**: {stats['total_actual_minutes']} minutes ({stats['total_actual_minutes']/60:.1f} hours)
- **Overall Ratio**: {stats['overall_ratio']:.2f}x (actual/estimated)
- **Efficiency**: {stats['efficiency']:.2f}x (estimated/actual)
- **Time Saved**: {stats['time_saved_minutes']} minutes ({stats['time_saved_minutes']/60:.1f} hours)
- **Accuracy**: {stats['accuracy_percentage']:.0f}%

## Calibration Factors by Complexity

"""
        for complexity, factor in factors.items():
            tasks_count = len([t for t in self.session_data 
                             if t.complexity == complexity and t.actual_minutes > 0])
            report += f"- **{complexity.title()}**: {factor:.2f}x ({tasks_count} tasks)\n"
            report += f"  - {self._get_recommendation(factor)}\n"
        
        report += f"""
## Key Insights

### What This Means

**You are {stats['efficiency']:.1f}x faster than your initial estimates.**

- Original estimate: {stats['total_estimated_minutes']/60:.1f} hours
- Actual time: {stats['total_actual_minutes']/60:.1f} hours
- **Saved: {stats['time_saved_minutes']/60:.1f} hours**

### Pattern Recognition

1. **Simple tasks**: {factors['simple']:.2f}x - {self._get_recommendation(factors['simple'])}
2. **Medium tasks**: {factors['medium']:.2f}x - {self._get_recommendation(factors['medium'])}
3. **Complex tasks**: {factors['complex']:.2f}x - {self._get_recommendation(factors['complex'])}

### Recommendation for Future Estimates

When estimating new tasks:
1. Make your gut estimate
2. Identify complexity level
3. Multiply by calibration factor:
   - Simple: ×{factors['simple']:.2f}
   - Medium: ×{factors['medium']:.2f}
   - Complex: ×{factors['complex']:.2f}

**Example:**
- Gut estimate: 30 minutes (complex task)
- Calibrated: 30 × {factors['complex']:.2f} = {int(30 * factors['complex'])} minutes
- **Use the calibrated estimate in brainstorms**

## Session Breakdown

"""
        for task in self.session_data:
            if task.actual_minutes > 0:
                variance = ((task.actual_minutes - task.estimated_minutes) / task.estimated_minutes * 100)
                report += f"- **{task.task}** ({task.complexity})\n"
                report += f"  - Estimated: {task.estimated_minutes}m | Actual: {task.actual_minutes}m | "
                report += f"Variance: {variance:+.0f}%\n"
        
        return report


def main():
    """Generate and print calibration report"""
    calibrator = TimeCalibrator()
    
    print(calibrator.generate_report())
    
    print("\n" + "="*60)
    print("Example: Calibrating a New Estimate")
    print("="*60 + "\n")
    
    # Example calibration
    result = calibrator.calibrate_estimate(
        task_description="Build new feature X",
        initial_estimate_minutes=45,
        complexity='complex'
    )
    
    print(f"Task: {result['task']}")
    print(f"Your gut estimate: {result['initial_estimate_minutes']} minutes")
    print(f"Complexity: {result['complexity']}")
    print(f"Calibration factor: {result['calibration_factor']:.2f}x")
    print(f"Calibrated estimate: {result['calibrated_estimate_minutes']} minutes")
    print(f"Confidence: {result['confidence']:.0%} (based on {result['sample_size']} similar tasks)")
    print(f"Recommendation: {result['recommendation']}")


if __name__ == '__main__':
    main()
