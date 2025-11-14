#!/usr/bin/env python3
"""
8825 Inbox MCP Server
Receives content from external LLMs (ChatGPT, Claude, etc.) and writes to inbox.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
from pathlib import Path
import uuid

app = Flask(__name__)

# Configuration
INBOX_PATH = Path.home() / "Downloads" / "8825_inbox" / "pending"
API_KEY = os.environ.get('INBOX_API_KEY', 'default-dev-key-change-me')

# Valid enums
VALID_CONTENT_TYPES = ['mining_report', 'achievement', 'pattern', 'note', 'feature', 'decision']
VALID_FOCUSES = ['joju', 'hcss', 'team76', 'jh']

@app.route('/write_to_inbox', methods=['POST'])
def write_to_inbox():
    """Write content to 8825 inbox"""
    
    # Authenticate
    auth_key = request.headers.get('X-API-Key')
    if auth_key != API_KEY:
        return jsonify({
            "error": "Unauthorized",
            "message": "Invalid API key"
        }), 401
    
    # Get JSON payload
    try:
        data = request.json
    except Exception as e:
        return jsonify({
            "error": "Invalid JSON",
            "message": str(e)
        }), 400
    
    # Validate required fields
    required = ['content_type', 'target_focus', 'content', 'metadata']
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing
        }), 400
    
    # Validate content_type
    if data['content_type'] not in VALID_CONTENT_TYPES:
        return jsonify({
            "error": "Invalid content_type",
            "valid_types": VALID_CONTENT_TYPES,
            "received": data['content_type']
        }), 400
    
    # Validate target_focus
    if data['target_focus'] not in VALID_FOCUSES:
        return jsonify({
            "error": "Invalid target_focus",
            "valid_focuses": VALID_FOCUSES,
            "received": data['target_focus']
        }), 400
    
    # Validate metadata
    if 'source' not in data['metadata']:
        data['metadata']['source'] = 'external_llm'
    if 'timestamp' not in data['metadata']:
        data['metadata']['timestamp'] = datetime.now().isoformat()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{data['content_type']}_{data['target_focus']}.json"
    filepath = INBOX_PATH / filename
    
    # Ensure inbox directory exists
    INBOX_PATH.mkdir(parents=True, exist_ok=True)
    
    # Write file
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        return jsonify({
            "error": "Failed to write file",
            "message": str(e)
        }), 500
    
    return jsonify({
        "success": True,
        "filename": filename,
        "filepath": str(filepath),
        "message": "✅ Written to inbox. Tell Windsurf: 'fetch inbox'"
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "inbox_path": str(INBOX_PATH),
        "inbox_exists": INBOX_PATH.exists(),
        "valid_content_types": VALID_CONTENT_TYPES,
        "valid_focuses": VALID_FOCUSES
    })

@app.route('/test', methods=['POST'])
def test():
    """Test endpoint (no auth required)"""
    return jsonify({
        "status": "ok",
        "received": request.json,
        "message": "Test successful - use /write_to_inbox for real writes"
    })

if __name__ == '__main__':
    print("=" * 60)
    print("8825 Inbox MCP Server")
    print("=" * 60)
    print(f"Inbox Path: {INBOX_PATH}")
    print(f"API Key: {API_KEY[:10]}..." if len(API_KEY) > 10 else f"API Key: {API_KEY}")
    print(f"Server: http://127.0.0.1:8828")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /write_to_inbox - Write content (requires API key)")
    print("  GET  /health         - Health check")
    print("  POST /test           - Test endpoint (no auth)")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=8828, debug=False)
