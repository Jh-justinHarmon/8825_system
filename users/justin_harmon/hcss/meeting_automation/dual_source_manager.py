#!/usr/bin/env python3
"""
Dual-Source Manager
Manages Otter API (primary) + Gmail API (fallback) with health monitoring
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from otter_client import OtterClient
from gmail_client import GmailClient

class DualSourceManager:
    """Manage dual-source meeting transcript retrieval"""
    
    def __init__(self, config_path: Path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.log_file = Path(config_path).parent / "logs/dual_source_manager.log"
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Initialize sources
        self.otter = None
        self.gmail = None
        
        if self.config['otter_api']['enabled']:
            email = self.config['otter_api']['email']
            password = self._get_otter_password()
            self.otter = OtterClient(email, password)
        
        if self.config['gmail']['enabled']:
            creds_path = self.config['gmail']['credentials_path']
            token_path = self.config['gmail']['token_path']
            self.gmail = GmailClient(creds_path, token_path)
        
        # Health tracking
        self.health = {
            'otter_api': {'status': 'unknown', 'failures': 0, 'last_success': None},
            'gmail': {'status': 'unknown', 'failures': 0, 'last_success': None}
        }
        
        self.current_source = self.config['strategy']['primary']
        
        self.log("🔄 Dual-Source Manager initialized", "INFO")
    
    def _get_otter_password(self) -> str:
        """Get Otter password from macOS Keychain"""
        try:
            key = self.config['otter_api']['password_keychain_key']
            result = subprocess.run(
                ['security', 'find-generic-password', '-s', key, '-w'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception as e:
            raise Exception(f"Failed to get Otter password from keychain: {e}")
    
    def get_transcripts(self) -> List[Dict]:
        """
        Get transcripts using dual-source strategy
        
        Returns:
            List of transcript objects
        """
        primary_result = None
        fallback_result = None
        
        # Try primary source
        if self.current_source == 'otter_api' and self.otter:
            try:
                self.log("Fetching from Otter API (primary)...", "INFO")
                primary_result = self._get_from_otter()
                self._mark_success('otter_api')
                self.log(f"✅ Otter API: {len(primary_result)} transcripts", "INFO")
                
            except Exception as e:
                self.log(f"⚠️  Otter API failed: {e}", "WARN")
                self._mark_failure('otter_api')
                
                if self._should_failover('otter_api'):
                    self._failover_to('gmail')
        
        # Try fallback (if cross_validate or primary failed)
        if self.config['validation']['cross_check'] or not primary_result:
            if self.gmail:
                try:
                    self.log("Fetching from Gmail (fallback)...", "INFO")
                    fallback_result = self._get_from_gmail()
                    self._mark_success('gmail')
                    self.log(f"✅ Gmail: {len(fallback_result)} transcripts", "INFO")
                    
                except Exception as e:
                    self.log(f"❌ Gmail failed: {e}", "ERROR")
                    self._mark_failure('gmail')
        
        # Select best result
        return self._select_best_result(primary_result, fallback_result)
    
    def _get_from_otter(self) -> List[Dict]:
        """Get transcripts from Otter API"""
        speeches = self.otter.get_speeches(limit=10)
        
        # Filter for TGIF meetings
        tgif_speeches = [s for s in speeches if 'TGIF' in s['title'].upper()]
        
        transcripts = []
        for speech in tgif_speeches:
            # Check if already processed
            if self._is_processed(speech['id'], 'otter_api'):
                continue
            
            # Download transcript
            content = self.otter.download_speech(speech['id'], format='txt')
            
            transcripts.append({
                'source': 'otter_api',
                'id': speech['id'],
                'title': speech['title'],
                'date': speech['date'],
                'transcript': content,
                'metadata': {
                    'duration': speech.get('duration'),
                    'participants': speech.get('participants', [])
                }
            })
        
        return transcripts
    
    def _get_from_gmail(self) -> List[Dict]:
        """Get transcripts from Gmail"""
        query = self.config['gmail']['search_query']
        messages = self.gmail.search(query, max_results=10)
        
        transcripts = []
        for message in messages:
            # Check if already processed
            if self._is_processed(message['id'], 'gmail'):
                continue
            
            # Extract transcript from email body
            transcript = message['body']
            
            transcripts.append({
                'source': 'gmail',
                'id': message['id'],
                'title': message['subject'],
                'date': message['date'],
                'transcript': transcript,
                'metadata': {
                    'email_id': message['id'],
                    'from': message['from']
                }
            })
        
        return transcripts
    
    def _select_best_result(self, primary: List[Dict], fallback: List[Dict]) -> List[Dict]:
        """Select best result from primary and fallback"""
        
        # Only primary has results
        if primary and not fallback:
            return primary
        
        # Only fallback has results
        if fallback and not primary:
            self.log("Using fallback source (primary failed)", "WARN")
            return fallback
        
        # Both have results - use preferred
        if primary and fallback:
            if self.config['validation']['cross_check']:
                self.log(f"Cross-validation: {len(primary)} vs {len(fallback)}", "INFO")
            
            preferred = self.config['validation']['prefer_source']
            if preferred == 'otter_api':
                return primary
            else:
                return fallback
        
        # Neither has results
        return []
    
    def _is_processed(self, item_id: str, source: str) -> bool:
        """Check if item already processed"""
        # TODO: Track processed items
        return False
    
    def _mark_failure(self, source: str):
        """Mark source as failed"""
        self.health[source]['failures'] += 1
        self.health[source]['status'] = 'degraded'
        self.log(f"⚠️  {source} failure count: {self.health[source]['failures']}", "WARN")
    
    def _mark_success(self, source: str):
        """Mark source as successful"""
        self.health[source]['failures'] = 0
        self.health[source]['status'] = 'healthy'
        self.health[source]['last_success'] = datetime.now().isoformat()
    
    def _should_failover(self, source: str) -> bool:
        """Check if should failover"""
        if not self.config['health_monitoring']['auto_failover']:
            return False
        
        threshold = self.config['health_monitoring']['failure_threshold']
        failures = self.health[source]['failures']
        
        return failures >= threshold
    
    def _failover_to(self, source: str):
        """Failover to different source"""
        old_source = self.current_source
        self.current_source = source
        
        self.log(f"🔄 FAILOVER: {old_source} → {source}", "WARN")
    
    def get_health_status(self) -> Dict:
        """Get health status"""
        return {
            'current_source': self.current_source,
            'otter_api': self.health['otter_api'],
            'gmail': self.health['gmail'],
            'auto_failover_enabled': self.config['health_monitoring']['auto_failover']
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a') as f:
            f.write(log_message)

def main():
    """Test dual-source manager"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 dual_source_manager.py <config_path>")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    manager = DualSourceManager(config_path)
    
    print("\n=== Health Status ===")
    status = manager.get_health_status()
    print(json.dumps(status, indent=2))
    
    print("\n=== Fetching Transcripts ===")
    transcripts = manager.get_transcripts()
    print(f"Found {len(transcripts)} transcripts")
    
    for t in transcripts:
        print(f"\n- {t['title']}")
        print(f"  Source: {t['source']}")
        print(f"  Date: {t['date']}")

if __name__ == '__main__':
    main()
