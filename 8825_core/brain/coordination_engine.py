#!/usr/bin/env python3
"""
8825 Coordination Engine
Orchestrates multi-step workflows with failure handling
"""

import json
import subprocess
import time
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

class CoordinationEngine:
    """Orchestrates multi-step workflows safely"""
    
    def __init__(self, brain_state: Dict[str, Any]):
        self.state = brain_state
        self.config_dir = Path.home() / ".8825"
    
    def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a multi-step workflow
        
        Args:
            workflow: Workflow definition with steps
        
        Returns:
            Execution result with status and details
        """
        
        workflow_id = workflow.get('id', 'unknown')
        steps = workflow.get('steps', [])
        
        print(f"🔄 Executing workflow: {workflow_id}")
        print(f"📋 Steps: {len(steps)}")
        
        # Analyze workflow safety
        safety = self.analyze_workflow_safety(workflow)
        if not safety['safe']:
            return {
                "status": "blocked",
                "reason": safety['reason'],
                "workflow_id": workflow_id
            }
        
        # Add to active workflows
        self.state['active_workflows'].append({
            "id": workflow_id,
            "started": datetime.now().isoformat(),
            "steps_total": len(steps),
            "steps_completed": 0
        })
        
        # Execute steps
        results = []
        for i, step in enumerate(steps, 1):
            print(f"\n[{i}/{len(steps)}] {step.get('action', 'unknown')}...")
            
            result = self.execute_step(step)
            results.append(result)
            
            if result['success']:
                print(f"  ✅ {result.get('message', 'Success')}")
            else:
                print(f"  ❌ {result.get('error', 'Failed')}")
                
                # Handle failure
                recovery = self.handle_failure(step, result, results)
                
                if recovery['success']:
                    print(f"  ✅ Recovered")
                    results.append(recovery)
                else:
                    print(f"  ❌ Recovery failed - Rolling back")
                    self.rollback(results)
                    
                    # Remove from active workflows
                    self.remove_active_workflow(workflow_id)
                    
                    return {
                        "status": "failed",
                        "workflow_id": workflow_id,
                        "failed_step": i,
                        "error": result.get('error'),
                        "results": results
                    }
            
            # Update progress
            self.update_workflow_progress(workflow_id, i)
        
        # Remove from active workflows
        self.remove_active_workflow(workflow_id)
        
        # Record success
        self.record_workflow_outcome(workflow, results, success=True)
        
        print(f"\n✅ Workflow complete: {workflow_id}")
        
        return {
            "status": "success",
            "workflow_id": workflow_id,
            "steps_completed": len(steps),
            "results": results
        }
    
    def analyze_workflow_safety(self, workflow: Dict[str, Any]) -> Dict[str, bool]:
        """Check if entire workflow is safe to execute"""
        from prediction_engine import PredictionEngine
        
        predictor = PredictionEngine(self.state)
        
        for step in workflow.get('steps', []):
            # Skip wait steps
            if step.get('action') in ['wait', 'wait_for_workflow', 'wait_for_cleanup']:
                continue
            
            # Predict step
            action_str = f"{step.get('action')} {step.get('target', '')}"
            prediction = predictor.predict_action(action_str)
            
            if prediction['risk_level'] == 'critical':
                return {
                    "safe": False,
                    "reason": prediction['recommendation']
                }
        
        return {"safe": True}
    
    def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        action = step.get('action')
        target = step.get('target', '')
        
        try:
            if action == 'wait':
                duration = step.get('duration', 5)
                time.sleep(duration)
                return {
                    "step": step,
                    "success": True,
                    "message": f"Waited {duration} seconds"
                }
            
            elif action == 'wait_for_workflow':
                return self.wait_for_workflow(target)
            
            elif action == 'wait_for_cleanup':
                return self.wait_for_cleanup()
            
            elif action == 'stop':
                return self.stop_component(target)
            
            elif action == 'start':
                return self.start_component(target)
            
            elif action == 'verify_health':
                return self.verify_health(target)
            
            elif action == 'cleanup':
                return self.run_cleanup(target)
            
            else:
                return {
                    "step": step,
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
        
        except Exception as e:
            return {
                "step": step,
                "success": False,
                "error": str(e)
            }
    
    def wait_for_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Wait for another workflow to complete"""
        max_wait = 300  # 5 minutes
        waited = 0
        
        while waited < max_wait:
            active = [w for w in self.state['active_workflows'] if w['id'] == workflow_id]
            if not active:
                return {
                    "success": True,
                    "message": f"Workflow {workflow_id} completed"
                }
            
            time.sleep(5)
            waited += 5
        
        return {
            "success": False,
            "error": f"Timeout waiting for workflow {workflow_id}"
        }
    
    def wait_for_cleanup(self) -> Dict[str, Any]:
        """Wait for cleanup scripts to finish"""
        max_wait = 300  # 5 minutes
        waited = 0
        
        while waited < max_wait:
            if not self.is_cleanup_running():
                return {
                    "success": True,
                    "message": "Cleanup completed"
                }
            
            time.sleep(5)
            waited += 5
        
        return {
            "success": False,
            "error": "Timeout waiting for cleanup"
        }
    
    def is_cleanup_running(self) -> bool:
        """Check if cleanup is running"""
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            return "cleanup" in result.stdout.lower()
        except:
            return False
    
    def stop_component(self, target: str) -> Dict[str, Any]:
        """Stop a component (daemon or script)"""
        try:
            # Try pkill first
            result = subprocess.run(
                ["pkill", "-f", target],
                capture_output=True,
                text=True
            )
            
            # Wait a moment
            time.sleep(2)
            
            # Verify stopped
            check = subprocess.run(
                ["pgrep", "-f", target],
                capture_output=True,
                text=True
            )
            
            if check.returncode != 0:
                return {
                    "success": True,
                    "message": f"Stopped {target}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to stop {target}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def start_component(self, target: str) -> Dict[str, Any]:
        """Start a component"""
        try:
            # Look for start script
            start_script = self.find_start_script(target)
            
            if not start_script:
                return {
                    "success": False,
                    "error": f"No start script found for {target}"
                }
            
            # Execute start script
            result = subprocess.run(
                ["bash", str(start_script)],
                capture_output=True,
                text=True,
                cwd=start_script.parent
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Started {target}",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_start_script(self, target: str) -> Path:
        """Find start script for a component"""
        # Common patterns
        patterns = [
            f"start_{target}.sh",
            f"start_all_*.sh",
            "start.sh"
        ]
        
        # Search in common locations
        search_dirs = [
            Path("8825_core/sync"),
            Path("8825_core/inbox"),
            Path("8825_core/brain"),
            Path(".")
        ]
        
        for dir in search_dirs:
            if not dir.exists():
                continue
            
            for pattern in patterns:
                matches = list(dir.glob(pattern))
                if matches:
                    return matches[0]
        
        return None
    
    def verify_health(self, target: str) -> Dict[str, Any]:
        """Verify component is healthy"""
        try:
            # Check if running
            result = subprocess.run(
                ["pgrep", "-f", target],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"{target} is healthy"
                }
            else:
                return {
                    "success": False,
                    "error": f"{target} is not running"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_cleanup(self, target: str) -> Dict[str, Any]:
        """Run cleanup script"""
        try:
            # Find cleanup script
            cleanup_script = self.find_cleanup_script(target)
            
            if not cleanup_script:
                return {
                    "success": False,
                    "error": f"No cleanup script found for {target}"
                }
            
            # Execute
            result = subprocess.run(
                ["bash", str(cleanup_script)],
                capture_output=True,
                text=True,
                cwd=cleanup_script.parent
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Cleanup completed",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_cleanup_script(self, target: str) -> Path:
        """Find cleanup script"""
        patterns = [
            f"cleanup_{target}.sh",
            f"cleanup_*.sh",
            "cleanup.sh"
        ]
        
        search_dirs = [
            Path("8825_core/explorations/features"),
            Path("."),
        ]
        
        for dir in search_dirs:
            if not dir.exists():
                continue
            
            for pattern in patterns:
                matches = list(dir.glob(pattern))
                if matches:
                    return matches[0]
        
        return None
    
    def handle_failure(
        self,
        step: Dict[str, Any],
        result: Dict[str, Any],
        completed_steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Try to recover from failure"""
        error = result.get('error', '')
        
        # File locked - wait and retry
        if "locked" in error.lower() or "busy" in error.lower():
            print("  ⏳ Resource busy, waiting 5 seconds...")
            time.sleep(5)
            return self.execute_step(step)
        
        # Permission denied - can't auto-recover
        if "permission" in error.lower():
            return {
                "success": False,
                "error": "Permission denied - manual intervention required"
            }
        
        # Component not found - can't recover
        if "not found" in error.lower():
            return {
                "success": False,
                "error": "Component not found"
            }
        
        # Unknown error - retry once
        print("  ⏳ Retrying...")
        time.sleep(2)
        return self.execute_step(step)
    
    def rollback(self, completed_steps: List[Dict[str, Any]]):
        """Rollback completed steps"""
        print("\n🔄 Rolling back...")
        
        for result in reversed(completed_steps):
            if not result.get('success'):
                continue
            
            step = result.get('step', {})
            inverse = self.get_inverse_action(step)
            
            if inverse:
                print(f"  ↩️  {inverse.get('action')} {inverse.get('target', '')}")
                self.execute_step(inverse)
    
    def get_inverse_action(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Get inverse of an action for rollback"""
        action = step.get('action')
        target = step.get('target')
        
        inverses = {
            'start': {'action': 'stop', 'target': target},
            'stop': {'action': 'start', 'target': target},
        }
        
        return inverses.get(action)
    
    def update_workflow_progress(self, workflow_id: str, steps_completed: int):
        """Update workflow progress"""
        for workflow in self.state['active_workflows']:
            if workflow['id'] == workflow_id:
                workflow['steps_completed'] = steps_completed
                break
    
    def remove_active_workflow(self, workflow_id: str):
        """Remove workflow from active list"""
        self.state['active_workflows'] = [
            w for w in self.state['active_workflows']
            if w['id'] != workflow_id
        ]
    
    def record_workflow_outcome(
        self,
        workflow: Dict[str, Any],
        results: List[Dict[str, Any]],
        success: bool
    ):
        """Record workflow outcome for learning"""
        outcome = {
            "workflow_id": workflow.get('id'),
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "steps_total": len(workflow.get('steps', [])),
            "steps_completed": len([r for r in results if r.get('success')]),
            "results": results
        }
        
        self.state['history'].append(outcome)
        
        # Save to file
        history_file = self.config_dir / "workflow_history.json"
        try:
            existing = []
            if history_file.exists():
                with open(history_file) as f:
                    existing = json.load(f)
            
            existing.append(outcome)
            
            with open(history_file, 'w') as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save history: {e}")

def main():
    """Test the coordination engine"""
    # Mock brain state
    state = {
        "registry": {"components": []},
        "health": {},
        "history": [],
        "active_workflows": []
    }
    
    engine = CoordinationEngine(state)
    
    # Test workflow
    workflow = {
        "id": "test_workflow",
        "steps": [
            {"action": "wait", "duration": 2},
            {"action": "verify_health", "target": "test"}
        ]
    }
    
    result = engine.execute_workflow(workflow)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
