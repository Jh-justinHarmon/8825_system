#!/usr/bin/env python3
"""
8825 Path Utilities
Centralized path management using environment variables for portability
"""

from pathlib import Path
import os
from typing import Optional


def get_system_root() -> Path:
    """
    Get 8825 system root directory
    
    Returns:
        Path to 8825-system directory
        
    Environment:
        SYSTEM_ROOT: Override default path
        
    Default:
        ~/8825-system
    """
    default = Path.home() / '8825-system'
    return Path(os.getenv('SYSTEM_ROOT', default))


def get_dropbox_root() -> Path:
    """
    Get Dropbox root directory
    
    Returns:
        Path to Dropbox root
        
    Environment:
        DROPBOX_ROOT: Override default path
        
    Default:
        ~/Dropbox
    """
    default = Path.home() / 'Dropbox'
    return Path(os.getenv('DROPBOX_ROOT', default))


def get_user_dir(username: Optional[str] = None) -> Path:
    """
    Get user directory within 8825 system
    
    Args:
        username: Username (defaults to current user or USER_NAME env var)
        
    Returns:
        Path to users/{username} directory
        
    Environment:
        USER_NAME: Override default username
    """
    if username is None:
        username = os.getenv('USER_NAME', os.getenv('USER', 'default_user'))
    return get_system_root() / 'users' / username


def get_downloads_dir() -> Path:
    """
    Get downloads directory
    
    Returns:
        Path to Downloads directory
        
    Environment:
        DOWNLOADS_DIR: Override default path
        
    Default:
        ~/Downloads
    """
    default = Path.home() / 'Downloads'
    return Path(os.getenv('DOWNLOADS_DIR', default))


def get_config_dir() -> Path:
    """
    Get 8825 config directory
    
    Returns:
        Path to ~/.8825 directory
        
    Environment:
        CONFIG_DIR: Override default path
        
    Default:
        ~/.8825
    """
    default = Path.home() / '.8825'
    return Path(os.getenv('CONFIG_DIR', default))


def get_brain_state_dir() -> Path:
    """
    Get brain state directory
    
    Returns:
        Path to brain state directory
        
    Default:
        ~/.8825/brain_state
    """
    return get_config_dir() / 'brain_state'


def get_focus_dir(focus_name: str, username: Optional[str] = None) -> Path:
    """
    Get focus directory for a user
    
    Args:
        focus_name: Focus name (e.g., 'joju', 'hcss', 'jh_assistant')
        username: Username (defaults to current user)
        
    Returns:
        Path to users/{username}/{focus_name} directory
    """
    return get_user_dir(username) / focus_name


def get_core_dir() -> Path:
    """
    Get 8825_core directory
    
    Returns:
        Path to 8825_core directory
    """
    return get_system_root() / '8825_core'


# Convenience functions for common paths
def get_protocols_dir() -> Path:
    """Get protocols directory"""
    return get_core_dir() / 'protocols'


def get_agents_dir() -> Path:
    """Get agents directory"""
    return get_core_dir() / 'agents'


def get_workflows_dir() -> Path:
    """Get workflows directory"""
    return get_core_dir() / 'workflows'


def get_integrations_dir() -> Path:
    """Get integrations directory"""
    return get_core_dir() / 'integrations'


# Debug function
def print_paths():
    """Print all configured paths (for debugging)"""
    print("8825 Path Configuration:")
    print(f"  SYSTEM_ROOT: {get_system_root()}")
    print(f"  DROPBOX_ROOT: {get_dropbox_root()}")
    print(f"  USER_DIR: {get_user_dir()}")
    print(f"  DOWNLOADS_DIR: {get_downloads_dir()}")
    print(f"  CONFIG_DIR: {get_config_dir()}")
    print(f"  BRAIN_STATE_DIR: {get_brain_state_dir()}")
    print(f"  CORE_DIR: {get_core_dir()}")


if __name__ == '__main__':
    print_paths()
