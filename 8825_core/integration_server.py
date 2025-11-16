#!/usr/bin/env python3
"""
Integration Server for 8825 System
Handles API key configuration via HTTP endpoints
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for local HTML files

# Paths
CORE_DIR = Path(__file__).resolve().parent
ENV_FILE = CORE_DIR / ".env"
BACKUP_DIR = CORE_DIR / "backups" / "env_backups"


def validate_api_key(api_key: str, prefix: str) -> tuple[bool, str]:
    """Validate API key format."""
    if not api_key:
        return False, "API key is required"
    
    if not api_key.startswith(prefix):
        return False, f"Invalid API key format. Must start with '{prefix}'"
    
    if len(api_key) < 30:
        return False, "API key appears too short"
    
    return True, ""


def backup_env_file() -> Path:
    """Create backup of existing .env file."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if ENV_FILE.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f".env.backup_{timestamp}"
        
        with open(ENV_FILE, 'r') as src:
            with open(backup_path, 'w') as dst:
                dst.write(src.read())
        
        return backup_path
    
    return None


def update_env_file(key_name: str, key_value: str) -> bool:
    """Update or create .env file with API key."""
    try:
        existing_lines = []
        key_exists = False
        
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    if line.strip().startswith(f'{key_name}='):
                        existing_lines.append(f'{key_name}={key_value}\n')
                        key_exists = True
                    else:
                        existing_lines.append(line)
        
        if not key_exists:
            existing_lines.append(f'\n# {key_name} Configuration\n')
            existing_lines.append(f'# Added: {datetime.now().isoformat()}\n')
            existing_lines.append(f'{key_name}={key_value}\n')
        
        with open(ENV_FILE, 'w') as f:
            f.writelines(existing_lines)
        
        # Update environment
        os.environ[key_name] = key_value
        
        return True
        
    except Exception as e:
        print(f"Error updating .env: {e}", file=sys.stderr)
        return False


@app.route('/api/configure-gemini', methods=['POST', 'OPTIONS'])
def configure_gemini():
    """Configure Gemini API key."""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        api_key = data.get('apiKey', '').strip()
        
        # Validate
        is_valid, error_msg = validate_api_key(api_key, 'AIzaSy')
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Backup
        backup_path = backup_env_file()
        
        # Save
        if not update_env_file('GOOGLE_GEMINI_API_KEY', api_key):
            return jsonify({'success': False, 'error': 'Failed to save API key'}), 500
        
        # Success
        key_preview = f"{api_key[:10]}...{api_key[-4:]}"
        return jsonify({
            'success': True,
            'message': 'Gemini API key configured successfully',
            'details': {
                'env_file': str(ENV_FILE),
                'backup': str(backup_path) if backup_path else None,
                'key_preview': key_preview,
                'activated': True
            }
        }), 200
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/configure-openai', methods=['POST', 'OPTIONS'])
def configure_openai():
    """Configure OpenAI API key."""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        api_key = data.get('apiKey', '').strip()
        
        # Validate
        is_valid, error_msg = validate_api_key(api_key, 'sk-')
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Backup
        backup_path = backup_env_file()
        
        # Save
        if not update_env_file('OPENAI_API_KEY', api_key):
            return jsonify({'success': False, 'error': 'Failed to save API key'}), 500
        
        # Success
        key_preview = f"{api_key[:10]}...{api_key[-4:]}"
        return jsonify({
            'success': True,
            'message': 'OpenAI API key configured successfully',
            'details': {
                'env_file': str(ENV_FILE),
                'backup': str(backup_path) if backup_path else None,
                'key_preview': key_preview,
                'activated': True
            }
        }), 200
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'server': '8825 Integration Server',
        'env_file': str(ENV_FILE),
        'env_exists': ENV_FILE.exists()
    })


@app.route('/setup')
def setup_page():
    """Serve Gemini integration setup page."""
    html_path = CORE_DIR / 'workflows' / 'meeting_automation' / 'gemini_integration_setup.html'
    return send_file(html_path)


@app.route('/openai-setup')
def openai_setup_page():
    """Serve OpenAI integration setup page."""
    html_path = CORE_DIR / 'workflows' / 'meeting_automation' / 'openai_integration_setup.html'
    return send_file(html_path)


if __name__ == '__main__':
    PORT = 5001  # Changed from 5000 (AirTunes conflict)
    print("🚀 Starting 8825 Integration Server...")
    print(f"📁 ENV file location: {ENV_FILE}")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"✅ CORS enabled for local HTML files")
    print(f"\nEndpoints:")
    print(f"  GET  http://localhost:{PORT}/setup (Gemini)")
    print(f"  GET  http://localhost:{PORT}/openai-setup (OpenAI)")
    print(f"  POST http://localhost:{PORT}/api/configure-gemini")
    print(f"  POST http://localhost:{PORT}/api/configure-openai")
    print(f"  GET  http://localhost:{PORT}/api/health")
    print(f"\nPress Ctrl+C to stop\n")
    
    app.run(host='localhost', port=PORT, debug=True)
