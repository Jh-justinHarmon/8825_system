#!/usr/bin/env python3
"""
8825 Prediction Engine
Predicts impact of actions using Phase 2 impact analysis + historical data
"""

import json
import subprocess
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

class PredictionEngine:
    """Predicts impact of actions and generates recommendations"""
    
    def __init__(self, brain_state: Dict[str, Any]):
        self.state = brain_state
        self.config_dir = Path.home() / ".8825"
    
    def predict_action(self, action: str) -> Dict[str, Any]:
        """
        Predict impact of an action
        
        Args:
            action: Action description (e.g., "restart inbox_daemon")
        
        Returns:
            Prediction with impact, conflicts, risk, and recommendation
        """
        
        # Parse action
        parsed = self.parse_action(action)
        
        # Get Phase 2 impact analysis
        impact = self.get_impact_analysis(parsed)
        
        # Check historical outcomes
        history = self.get_historical_outcomes(parsed)
        
        # Check current conflicts
        conflicts = self.check_current_conflicts(parsed)
        
        # Assess risk
        risk_level = self.assess_risk(impact, history, conflicts)
        
        # Generate recommendation
        recommendation = self.generate_recommendation(
            parsed, impact, history, conflicts, risk_level
        )
        
        return {
            "action": action,
            "parsed": parsed,
            "impact": impact,
            "history": history,
            "conflicts": conflicts,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "safe_to_proceed": risk_level in ["low", "medium"]
        }
    
    def parse_action(self, action: str) -> Dict[str, Any]:
        """Parse action string into structured format"""
        action_lower = action.lower()
        
        # Detect action type
        if "restart" in action_lower:
            action_type = "restart"
        elif "start" in action_lower:
            action_type = "start"
        elif "stop" in action_lower:
            action_type = "stop"
        elif "update" in action_lower or "change" in action_lower:
            action_type = "update"
        elif "cleanup" in action_lower or "clean" in action_lower:
            action_type = "cleanup"
        else:
            action_type = "unknown"
        
        # Extract target
        target = self.extract_target(action)
        
        return {
            "type": action_type,
            "target": target,
            "original": action
        }
    
    def extract_target(self, action: str) -> str:
        """Extract target component from action string"""
        # Common patterns
        words = action.split()
        
        # Look for daemon names
        for word in words:
            if "daemon" in word.lower() or "_sync" in word.lower():
                return word
        
        # Look for script names
        for word in words:
            if ".sh" in word or ".py" in word:
                return word
        
        # Default to last word
        return words[-1] if words else "unknown"
    
    def get_impact_analysis(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Get impact analysis from Phase 2"""
        # Check if Phase 2 impact tool exists
        impact_tool = self.config_dir / "impact_analysis.py"
        
        if not impact_tool.exists():
            # Phase 2 not complete, return basic analysis
            return {
                "source": "basic",
                "affected_components": [],
                "note": "Phase 2 impact analysis not available"
            }
        
        # Call Phase 2 impact analysis
        try:
            result = subprocess.run(
                ["python3", str(impact_tool), parsed['target']],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {
                    "source": "error",
                    "error": result.stderr,
                    "affected_components": []
                }
        except Exception as e:
            return {
                "source": "error",
                "error": str(e),
                "affected_components": []
            }
    
    def get_historical_outcomes(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Look up past outcomes for similar actions"""
        history = self.state.get('history', [])
        
        # Find similar actions
        similar = [
            h for h in history
            if h.get('action_type') == parsed['type']
            and h.get('target') == parsed['target']
        ]
        
        if not similar:
            return {
                "total_attempts": 0,
                "success_rate": None,
                "last_attempt": None,
                "note": "No historical data"
            }
        
        # Calculate success rate
        successes = sum(1 for h in similar if h.get('success', False))
        success_rate = successes / len(similar)
        
        # Get last attempt
        last = similar[-1] if similar else None
        
        return {
            "total_attempts": len(similar),
            "success_rate": success_rate,
            "successes": successes,
            "failures": len(similar) - successes,
            "last_attempt": last,
            "pattern": "successful" if success_rate > 0.7 else "risky" if success_rate < 0.5 else "mixed"
        }
    
    def check_current_conflicts(self, parsed: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if action conflicts with current state"""
        conflicts = []
        
        # Check active workflows
        for workflow in self.state.get('active_workflows', []):
            if self.conflicts_with_workflow(parsed, workflow):
                conflicts.append({
                    "type": "active_workflow",
                    "workflow_id": workflow.get('id'),
                    "reason": f"Workflow {workflow.get('id')} is currently running",
                    "resolution": "wait_for_completion",
                    "severity": "medium"
                })
        
        # Check running components
        registry = self.state.get('registry', {})
        for component in registry.get('components', []):
            if component.get('status') == 'running':
                if parsed['target'] in component.get('id', ''):
                    conflicts.append({
                        "type": "component_active",
                        "component": component['id'],
                        "reason": f"Component {component['id']} is currently running",
                        "resolution": "stop_before_action",
                        "severity": "high"
                    })
        
        # Check for cleanup scripts running
        if parsed['type'] in ['restart', 'start', 'update']:
            # Check if any cleanup is running
            cleanup_running = self.is_cleanup_running()
            if cleanup_running:
                conflicts.append({
                    "type": "cleanup_running",
                    "component": "cleanup_script",
                    "reason": "Cleanup script is currently running",
                    "resolution": "wait_for_cleanup",
                    "severity": "medium"
                })
        
        return conflicts
    
    def conflicts_with_workflow(self, parsed: Dict[str, Any], workflow: Dict[str, Any]) -> bool:
        """Check if action conflicts with a workflow"""
        # Check if workflow involves the same target
        workflow_components = workflow.get('components_involved', [])
        return parsed['target'] in workflow_components
    
    def is_cleanup_running(self) -> bool:
        """Check if any cleanup script is running"""
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            return "cleanup" in result.stdout.lower()
        except:
            return False
    
    def assess_risk(
        self,
        impact: Dict[str, Any],
        history: Dict[str, Any],
        conflicts: List[Dict[str, Any]]
    ) -> str:
        """
        Assess risk level
        
        Returns: "low", "medium", "high", or "critical"
        """
        
        # Critical: High severity conflicts
        if any(c.get('severity') == 'high' for c in conflicts):
            return "critical"
        
        # High: Multiple conflicts or poor history
        if len(conflicts) > 2:
            return "high"
        
        if history.get('success_rate') is not None and history['success_rate'] < 0.5:
            return "high"
        
        # Medium: Some conflicts or unknown history
        if len(conflicts) > 0:
            return "medium"
        
        if history.get('total_attempts') == 0:
            return "medium"
        
        # Low: No conflicts, good history
        return "low"
    
    def generate_recommendation(
        self,
        parsed: Dict[str, Any],
        impact: Dict[str, Any],
        history: Dict[str, Any],
        conflicts: List[Dict[str, Any]],
        risk_level: str
    ) -> str:
        """Generate actionable recommendation"""
        
        # Critical risk
        if risk_level == "critical":
            if conflicts:
                return f"❌ DO NOT PROCEED - {conflicts[0]['reason']}"
            return "❌ DO NOT PROCEED - Critical risk detected"
        
        # High risk
        if risk_level == "high":
            if conflicts:
                return f"⚠️  High risk - {conflicts[0]['resolution']}"
            if history.get('success_rate') is not None:
                return f"⚠️  High risk - Only {history['success_rate']*100:.0f}% success rate historically"
            return "⚠️  High risk - Review carefully before proceeding"
        
        # Medium risk
        if risk_level == "medium":
            if conflicts:
                conflict = conflicts[0]
                if conflict['resolution'] == 'wait_for_completion':
                    return f"⚠️  Wait for {conflict.get('workflow_id', 'workflow')} to complete (~2 minutes)"
                elif conflict['resolution'] == 'wait_for_cleanup':
                    return "⚠️  Wait for cleanup to complete (~2 minutes)"
                else:
                    return f"⚠️  {conflict['resolution']}"
            return "⚠️  Proceed with caution - Monitor for issues"
        
        # Low risk
        if history.get('success_rate') is not None and history['success_rate'] > 0.8:
            return f"✅ Safe to proceed - {history['success_rate']*100:.0f}% success rate"
        
        return "✅ Safe to proceed"
    
    def create_safe_workflow(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Create a safe workflow for the action"""
        steps = []
        
        # Add wait steps for conflicts
        conflicts = self.check_current_conflicts(parsed)
        for conflict in conflicts:
            if conflict['resolution'] == 'wait_for_completion':
                steps.append({
                    "action": "wait_for_workflow",
                    "target": conflict.get('workflow_id')
                })
            elif conflict['resolution'] == 'wait_for_cleanup':
                steps.append({
                    "action": "wait_for_cleanup"
                })
        
        # Add main action steps
        if parsed['type'] == 'restart':
            steps.extend([
                {"action": "stop", "target": parsed['target']},
                {"action": "wait", "duration": 5},
                {"action": "start", "target": parsed['target']},
                {"action": "verify_health", "target": parsed['target']}
            ])
        elif parsed['type'] == 'start':
            steps.extend([
                {"action": "start", "target": parsed['target']},
                {"action": "verify_health", "target": parsed['target']}
            ])
        elif parsed['type'] == 'stop':
            steps.append({"action": "stop", "target": parsed['target']})
        
        return {
            "id": f"safe_{parsed['type']}_{parsed['target']}",
            "steps": steps,
            "created": datetime.now().isoformat()
        }

def main():
    """Test the prediction engine"""
    # Mock brain state
    state = {
        "registry": {"components": []},
        "health": {},
        "history": [],
        "active_workflows": []
    }
    
    engine = PredictionEngine(state)
    
    # Test prediction
    prediction = engine.predict_action("restart inbox_daemon")
    print(json.dumps(prediction, indent=2))

if __name__ == "__main__":
    main()
