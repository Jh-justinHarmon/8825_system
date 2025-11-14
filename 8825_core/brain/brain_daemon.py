#!/usr/bin/env python3
"""
8825 Brain Daemon
Central nervous system for 8825 - maintains system awareness and coordinates actions
"""

import json
import time
import socket
import os
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class BrainDaemon:
    def __init__(self):
        self.home = Path.home()
        self.config_dir = self.home / ".8825"
        self.brain_dir = self.home / "Downloads" / "8825_brain"
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.brain_dir.mkdir(exist_ok=True)
        
        # State
        self.state = {
            "registry": {},
            "health": {},
            "history": [],
            "predictions": {},
            "active_workflows": [],
            "last_sync": None,
            "last_checkpoint_processed": None
        }
        
        # API socket
        self.socket_path = "/tmp/8825_brain.sock"
        self.server_socket = None
        
        # Control
        self.running = False
        
        # Learning capture
        try:
            from learning_extractor import LearningExtractor
            from auto_memory_creator import AutoMemoryCreator
            from checkpoint_reader import CheckpointReader
            self.learning_extractor = LearningExtractor()
            self.memory_creator = AutoMemoryCreator()
            self.checkpoint_reader = CheckpointReader()
        except ImportError as e:
            print(f"⚠️  Learning capture modules not available: {e}")
            self.learning_extractor = None
            self.memory_creator = None
            self.checkpoint_reader = None
        
        # Evolution components
        try:
            from usage_tracker import UsageTracker
            from decay_engine import DecayEngine
            from tool_evolution_detector import ToolEvolutionDetector
            from competition_resolver import CompetitionResolver
            
            self.usage_tracker = UsageTracker(self.memory_creator) if self.memory_creator else None
            self.decay_engine = DecayEngine()
            self.tool_detector = ToolEvolutionDetector()
            self.competition_resolver = CompetitionResolver()
            print("✅ Evolution components loaded")
        except ImportError as e:
            print(f"⚠️  Evolution components not available: {e}")
            self.usage_tracker = None
            self.decay_engine = None
            self.tool_detector = None
            self.competition_resolver = None
        
    def start(self):
        """Start the brain daemon"""
        print("🧠 Starting 8825 Brain Daemon...")
        
        # Initial sync
        print("📊 Initial sync...")
        self.sync_all()
        
        # Start API server in thread
        print("🔌 Starting API server...")
        api_thread = threading.Thread(target=self.start_api_server, daemon=True)
        api_thread.start()
        
        # Start main loop
        print("✅ Brain daemon running")
        self.running = True
        self.main_loop()
    
    def main_loop(self):
        """Main daemon loop"""
        while self.running:
            try:
                # Sync with Phase 1 & 2 data
                self.sync_all()
                
                # Update predictions
                self.update_predictions()
                
                # Check for issues
                self.check_for_issues()
                
                # Auto-capture learnings from checkpoints
                self.auto_capture_learnings()
                
                # Evolution cycle (every 30 seconds)
                self.apply_decay()
                self.resolve_competitions()
                
                # Sleep 30 seconds
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🛑 Shutting down brain daemon...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(30)
    
    def sync_all(self):
        """Sync with all data sources"""
        self.sync_registry()
        self.sync_health()
        self.sync_history()
        self.state['last_sync'] = datetime.now().isoformat()
    
    def sync_registry(self):
        """Read registry from Phase 2"""
        registry_path = self.config_dir / "registry.json"
        if registry_path.exists():
            try:
                with open(registry_path) as f:
                    self.state['registry'] = json.load(f)
            except Exception as e:
                print(f"⚠️  Failed to sync registry: {e}")
        else:
            # Registry doesn't exist yet (Phase 2 not complete)
            self.state['registry'] = {
                "components": [],
                "summary": {
                    "total_count": 0,
                    "by_type": {}
                }
            }
    
    def sync_health(self):
        """Read health from Phase 1"""
        health_path = self.config_dir / "health_status.json"
        if health_path.exists():
            try:
                with open(health_path) as f:
                    self.state['health'] = json.load(f)
            except Exception as e:
                print(f"⚠️  Failed to sync health: {e}")
        else:
            # Health monitoring doesn't exist yet (Phase 1 not complete)
            self.state['health'] = {
                "overall": "unknown",
                "components": []
            }
    
    def sync_history(self):
        """Read change history"""
        history_path = self.config_dir / "change_history.json"
        if history_path.exists():
            try:
                with open(history_path) as f:
                    self.state['history'] = json.load(f)
            except Exception as e:
                print(f"⚠️  Failed to sync history: {e}")
        else:
            self.state['history'] = []
    
    def update_predictions(self):
        """Generate predictions based on current state"""
        # TODO: Implement prediction logic (Phase 3 Session 2)
        pass
    
    def check_for_issues(self):
        """Scan for problems"""
        # TODO: Implement issue detection (Phase 3 Session 4)
        pass
    
    def auto_capture_learnings(self):
        """
        Auto-capture learnings from checkpoint summaries
        Runs every 30 seconds as part of main loop
        """
        if not self.learning_extractor or not self.memory_creator:
            return  # Learning capture not available
        
        try:
            # Get latest checkpoint (placeholder - would read from actual checkpoint system)
            checkpoint_text = self._get_latest_checkpoint()
            
            if not checkpoint_text:
                return  # No new checkpoint
            
            # Check if already processed
            checkpoint_id = self._get_checkpoint_id(checkpoint_text)
            if checkpoint_id == self.state.get('last_checkpoint_processed'):
                return  # Already processed
            
            # Extract learnings
            learnings = self.learning_extractor.extract_learnings(
                checkpoint_text,
                source=checkpoint_id
            )
            
            if not learnings:
                return  # No learnings found
            
            # Save learnings
            results = self.memory_creator.save_learnings(
                learnings,
                min_confidence=0.7
            )
            
            # Log results
            created = sum(1 for r in results if r['action'] == 'created')
            updated = sum(1 for r in results if r['action'] == 'updated')
            
            if created > 0 or updated > 0:
                print(f"🧠 Auto-captured learnings: {created} new, {updated} updated")
            
            # Mark as processed
            self.state['last_checkpoint_processed'] = checkpoint_id
            
        except Exception as e:
            print(f"⚠️  Error in auto_capture_learnings: {e}")
    
    def _get_latest_checkpoint(self) -> str:
        """
        Get latest checkpoint summary from Cascade
        """
        if not self.checkpoint_reader:
            return None
        
        checkpoint = self.checkpoint_reader.get_latest_checkpoint()
        return checkpoint['text'] if checkpoint else None
    
    def _get_checkpoint_id(self, checkpoint_text: str) -> str:
        """Generate ID for checkpoint"""
        import hashlib
        return hashlib.md5(checkpoint_text.encode()).hexdigest()[:12]
    
    def apply_decay(self):
        """Apply time-based decay to all learnings"""
        if not self.decay_engine or not self.memory_creator:
            return
        
        try:
            memories = self.memory_creator.get_all_memories()
            updated = self.decay_engine.apply_decay(memories)
            
            # Save updated memories
            self.memory_creator.memories = updated
            self.memory_creator._save_memories()
        except Exception as e:
            print(f"⚠️  Error applying decay: {e}")
    
    def resolve_competitions(self):
        """Check and resolve tool competitions"""
        if not self.competition_resolver or not self.memory_creator or not self.usage_tracker:
            return
        
        try:
            memories = self.memory_creator.get_all_memories()
            resolutions = self.competition_resolver.check_competitions(
                memories,
                self.usage_tracker
            )
            
            if resolutions:
                # Save updated memories
                self.memory_creator._save_memories()
                
                # Log resolutions
                for resolution in resolutions:
                    print(f"🏆 Competition resolved: {resolution['winner']} wins - {resolution['reason']}")
        except Exception as e:
            print(f"⚠️  Error resolving competitions: {e}")
    
    def start_api_server(self):
        """Start Unix socket API server"""
        # Remove old socket if exists
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        
        # Create socket
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_socket.bind(self.socket_path)
        self.server_socket.listen(5)
        
        print(f"🔌 API server listening on {self.socket_path}")
        
        while self.running:
            try:
                client, _ = self.server_socket.accept()
                # Handle in thread
                threading.Thread(
                    target=self.handle_client,
                    args=(client,),
                    daemon=True
                ).start()
            except Exception as e:
                if self.running:
                    print(f"❌ API server error: {e}")
    
    def handle_client(self, client):
        """Handle API client request"""
        try:
            # Receive request
            data = client.recv(4096).decode()
            request = json.loads(data)
            
            # Route command
            command = request.get('command')
            if command == 'get_status':
                response = self.get_status()
            elif command == 'predict':
                response = self.predict_action(request.get('data'))
            elif command == 'execute':
                response = self.execute_workflow(request.get('data'))
            elif command == 'heal':
                response = self.check_and_heal()
            else:
                response = {"error": f"Unknown command: {command}"}
            
            # Send response
            client.send(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {"error": str(e)}
            client.send(json.dumps(error_response).encode())
        finally:
            client.close()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        registry = self.state['registry']
        health = self.state['health']
        
        # Count components
        total_components = len(registry.get('components', []))
        
        # Get active workflows
        active_workflows = len(self.state['active_workflows'])
        
        # Calculate time since last sync
        last_sync = self.state.get('last_sync')
        if last_sync:
            sync_time = datetime.fromisoformat(last_sync)
            seconds_ago = (datetime.now() - sync_time).total_seconds()
        else:
            seconds_ago = None
        
        return {
            "system_awareness": {
                "components": total_components,
                "health": health.get('overall', 'unknown'),
                "active_workflows": active_workflows,
                "last_sync": f"{int(seconds_ago)}s ago" if seconds_ago else "never"
            },
            "registry": registry.get('summary', {}),
            "health": health,
            "active_workflows": self.state['active_workflows'],
            "recommendations": self.generate_recommendations()
        }
    
    def predict_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict impact of action"""
        from prediction_engine import PredictionEngine
        
        engine = PredictionEngine(self.state)
        action = action_data.get('action', '')
        return engine.predict_action(action)
    
    def execute_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute coordinated workflow"""
        from coordination_engine import CoordinationEngine
        
        engine = CoordinationEngine(self.state)
        return engine.execute_workflow(workflow_data)
    
    def check_and_heal(self) -> Dict[str, Any]:
        """Check for issues and heal if possible"""
        from self_healing_engine import SelfHealingEngine
        
        engine = SelfHealingEngine(self.state)
        return engine.check_and_heal()
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on current state"""
        recommendations = []
        
        # Check if Phase 1 & 2 are complete
        if not self.state['registry'].get('components'):
            recommendations.append("⚠️  Phase 2 not complete - registry empty")
        
        if self.state['health'].get('overall') == 'unknown':
            recommendations.append("⚠️  Phase 1 not complete - health monitoring unavailable")
        
        if not recommendations:
            recommendations.append("✅ System healthy, no action needed")
        
        return recommendations
    
    def save_state(self):
        """Save brain state to disk"""
        state_path = self.brain_dir / "brain_state.json"
        with open(state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def shutdown(self):
        """Graceful shutdown"""
        print("🛑 Shutting down...")
        self.running = False
        
        # Save state
        self.save_state()
        
        # Close socket
        if self.server_socket:
            self.server_socket.close()
        
        # Remove socket file
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        
        print("✅ Brain daemon stopped")

def main():
    """Main entry point"""
    brain = BrainDaemon()
    try:
        brain.start()
    except KeyboardInterrupt:
        brain.shutdown()

if __name__ == "__main__":
    main()
