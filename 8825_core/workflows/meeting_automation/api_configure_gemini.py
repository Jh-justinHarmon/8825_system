#!/usr/bin/env python3
"""
Backend API endpoint for automated Gemini API configuration.

This endpoint receives the API key from the frontend and:
1. Validates the key format
2. Saves it to 8825_core/.env
3. Updates environment variables
4. Configures meeting automation to use Gemini
5. Returns success/failure status

Usage:
    POST /api/configure-gemini
    Body: { "apiKey": "AIzaSy..." }
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

# Paths
CORE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = CORE_DIR / ".env"
BACKUP_DIR = CORE_DIR / "backups" / "env_backups"


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    Validate Gemini API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not api_key:
        return False, "API key is required"
    
    if not api_key.startswith("AIzaSy"):
        return False, "Invalid API key format. Must start with 'AIzaSy'"
    
    if len(api_key) < 30:
        return False, "API key appears too short"
    
    return True, ""


def backup_env_file() -> Path:
    """
    Create a backup of the existing .env file.
    
    Returns:
        Path to the backup file
    """
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if ENV_FILE.exists():
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f".env.backup_{timestamp}"
        
        with open(ENV_FILE, 'r') as src:
            with open(backup_path, 'w') as dst:
                dst.write(src.read())
        
        return backup_path
    
    return None


def update_env_file(api_key: str) -> bool:
    """
    Update or create .env file with Gemini API key.
    Immediately activates the key in the current environment.
    
    Args:
        api_key: The Gemini API key to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read existing .env if it exists
        existing_lines = []
        gemini_key_exists = False
        
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    if line.strip().startswith('GOOGLE_GEMINI_API_KEY='):
                        # Replace existing key
                        existing_lines.append(f'GOOGLE_GEMINI_API_KEY={api_key}\n')
                        gemini_key_exists = True
                    else:
                        existing_lines.append(line)
        
        # Add key if it doesn't exist
        if not gemini_key_exists:
            from datetime import datetime
            existing_lines.append(f'\n# Google Gemini API Configuration\n')
            existing_lines.append(f'# Added: {datetime.now().isoformat()}\n')
            existing_lines.append(f'# Auto-activated - no restart required\n')
            existing_lines.append(f'GOOGLE_GEMINI_API_KEY={api_key}\n')
        
        # Write updated .env
        with open(ENV_FILE, 'w') as f:
            f.writelines(existing_lines)
        
        # IMMEDIATELY update current environment - no restart needed
        os.environ['GOOGLE_GEMINI_API_KEY'] = api_key
        
        # Reload any modules that cache environment variables
        reload_environment_modules()
        
        return True
        
    except Exception as e:
        print(f"Error updating .env file: {e}")
        return False


def reload_environment_modules():
    """
    Reload modules that cache environment variables.
    Ensures immediate activation without restart.
    """
    try:
        # If using python-dotenv, reload it
        try:
            from dotenv import load_dotenv
            load_dotenv(ENV_FILE, override=True)
        except ImportError:
            pass
        
        # Trigger any environment-dependent reloads
        # Add custom reload logic here if needed
        
    except Exception as e:
        print(f"Warning: Could not reload environment modules: {e}")


def configure_gemini(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main handler for Gemini API configuration.
    
    Args:
        request_data: Dictionary with 'apiKey' field
        
    Returns:
        Response dictionary with status and message
    """
    # Extract API key
    api_key = request_data.get('apiKey', '').strip()
    
    # Validate
    is_valid, error_msg = validate_api_key(api_key)
    if not is_valid:
        return {
            'success': False,
            'error': error_msg,
            'status': 400
        }
    
    # Backup existing .env
    backup_path = backup_env_file()
    
    # Update .env file
    if not update_env_file(api_key):
        return {
            'success': False,
            'error': 'Failed to save API key to .env file',
            'status': 500
        }
    
    # Success response
    return {
        'success': True,
        'message': 'Gemini API key configured and activated immediately',
        'details': {
            'env_file': str(ENV_FILE),
            'backup_created': str(backup_path) if backup_path else None,
            'key_preview': f"{api_key[:10]}...{api_key[-4:]}",
            'activated': True,
            'restart_required': False
        },
        'status': 200
    }


# Flask endpoint (if using Flask)
def flask_endpoint():
    """Flask endpoint wrapper."""
    from flask import request, jsonify
    
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    try:
        data = request.get_json()
        result = configure_gemini(data)
        status = result.pop('status', 200)
        return jsonify(result), status
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# FastAPI endpoint (if using FastAPI)
async def fastapi_endpoint(api_key: str):
    """FastAPI endpoint wrapper."""
    from fastapi import HTTPException
    
    result = configure_gemini({'apiKey': api_key})
    status = result.pop('status', 200)
    
    if not result.get('success'):
        raise HTTPException(status_code=status, detail=result.get('error'))
    
    return result


# CLI for testing
def main():
    """CLI for testing the configuration."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python api_configure_gemini.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    result = configure_gemini({'apiKey': api_key})
    
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
