"""
8825 v3.0 Environment Variable Loader
Loads .env files and expands variables in config files
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any


def load_env_file(env_path: str = None) -> Dict[str, str]:
    """
    Load environment variables from .env file
    
    Args:
        env_path: Path to .env file. If None, searches for .env in user directory
    
    Returns:
        Dictionary of environment variables
    """
    if env_path is None:
        # Look for .env in users/{user_id}/ directory
        v3_root = Path(__file__).parent.parent.parent
        user_dirs = list((v3_root / "users").glob("*"))
        
        if not user_dirs:
            raise FileNotFoundError("No user directories found in users/")
        
        # Use first user directory (or could detect from env)
        env_path = user_dirs[0] / ".env"
    
    env_vars = {}
    
    if not os.path.exists(env_path):
        print(f"Warning: .env file not found at {env_path}")
        print("Using .env.template as reference")
        return env_vars
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                env_vars[key] = value
    
    return env_vars


def expand_env_vars(text: str, env_vars: Dict[str, str] = None) -> str:
    """
    Expand environment variables in text
    
    Supports:
    - ${VAR_NAME}
    - $VAR_NAME
    
    Args:
        text: Text containing variables
        env_vars: Dictionary of environment variables. If None, uses os.environ
    
    Returns:
        Text with variables expanded
    """
    if env_vars is None:
        env_vars = dict(os.environ)
    
    # Expand ${VAR_NAME}
    def replace_braced(match):
        var_name = match.group(1)
        return env_vars.get(var_name, match.group(0))
    
    text = re.sub(r'\$\{([A-Z_][A-Z0-9_]*)\}', replace_braced, text)
    
    # Expand $VAR_NAME (word boundary)
    def replace_unbraced(match):
        var_name = match.group(1)
        return env_vars.get(var_name, match.group(0))
    
    text = re.sub(r'\$([A-Z_][A-Z0-9_]*)\b', replace_unbraced, text)
    
    return text


def load_config_with_env(config_path: str, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Load JSON config file and expand environment variables
    
    Args:
        config_path: Path to JSON config file
        env_vars: Dictionary of environment variables. If None, loads from .env
    
    Returns:
        Config dictionary with expanded variables
    """
    if env_vars is None:
        env_vars = load_env_file()
    
    with open(config_path, 'r') as f:
        config_text = f.read()
    
    # Expand environment variables
    expanded_text = expand_env_vars(config_text, env_vars)
    
    # Parse JSON
    config = json.loads(expanded_text)
    
    return config


def get_user_id() -> str:
    """
    Get current user ID from environment or user directory
    
    Returns:
        User ID string
    """
    # Try environment variable first
    user_id = os.environ.get('USER_ID')
    
    if user_id:
        return user_id
    
    # Fall back to detecting from users/ directory
    v3_root = Path(__file__).parent.parent.parent
    user_dirs = list((v3_root / "users").glob("*"))
    
    if user_dirs:
        return user_dirs[0].name
    
    raise ValueError("No USER_ID found in environment or users/ directory")


# Example usage
if __name__ == "__main__":
    print("8825 v3.0 Environment Loader")
    print("-" * 50)
    
    # Load environment variables
    try:
        env_vars = load_env_file()
        print(f"✅ Loaded {len(env_vars)} environment variables")
        
        # Show non-sensitive variables
        safe_vars = {k: v for k, v in env_vars.items() 
                     if not any(x in k.lower() for x in ['token', 'password', 'key', 'secret'])}
        
        for key, value in safe_vars.items():
            print(f"  {key} = {value}")
        
        # Test config loading
        print("\n" + "-" * 50)
        print("Testing config loading...")
        
        config_path = Path(__file__).parent.parent / "workflows/ingestion/config/ingestion_config.json"
        
        if config_path.exists():
            config = load_config_with_env(str(config_path), env_vars)
            print(f"✅ Loaded config: {config_path.name}")
            print(f"  Sources path: {config['sources']['downloads']['path']}")
            print(f"  Destinations: {len(config['destinations'])} configured")
        
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        print("  Create .env from .env.template in users/{user_id}/")
    except Exception as e:
        print(f"❌ Error: {e}")
