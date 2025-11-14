#!/usr/bin/env python3
"""
Restart Component Healing Strategy
Restarts unhealthy or stale components
"""

from typing import Dict, Any

class RestartComponentStrategy:
    """Strategy to restart unhealthy components"""
    
    def heal(self, issue: Dict[str, Any], brain_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Heal by restarting component
        
        Args:
            issue: Issue details
            brain_state: Current brain state
        
        Returns:
            Healing result
        """
        from coordination_engine import CoordinationEngine
        from prediction_engine import PredictionEngine
        
        component = issue.get('component', 'unknown')
        
        # Create restart workflow
        predictor = PredictionEngine(brain_state)
        parsed = {
            "type": "restart",
            "target": component,
            "original": f"restart {component}"
        }
        
        workflow = predictor.create_safe_workflow(parsed)
        
        # Execute via coordination engine
        coordinator = CoordinationEngine(brain_state)
        result = coordinator.execute_workflow(workflow)
        
        if result['status'] == 'success':
            return {
                "success": True,
                "message": f"Restarted {component}",
                "workflow_result": result
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Unknown error'),
                "workflow_result": result
            }
