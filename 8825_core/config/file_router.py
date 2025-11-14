#!/usr/bin/env python3
"""
File Router - Central document destination library
All tools use this to get consistent file paths
"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "file_router.json"

def load_config():
    """Load file router config"""
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_root():
    """Get root path for all files"""
    config = load_config()
    return Path(config["root"])

def get_destination(project):
    """Get destination path for a project"""
    config = load_config()
    root = Path(config["root"])
    dest = config["destinations"].get(project)
    if not dest:
        # Unknown project goes to MISC_INBOX
        dest = config["folders"]["unknown"]
    return root / dest

def get_intake():
    """Get intake folder path"""
    config = load_config()
    return Path(config["root"]) / config["folders"]["intake"]

def get_unknown():
    """Get unknown/misc inbox path"""
    config = load_config()
    return Path(config["root"]) / config["folders"]["unknown"]

def get_case_convention(file_type):
    """Get case convention for file type"""
    config = load_config()
    return config["file_conventions"].get(file_type, "lower")

def get_shareable_root():
    """Get shareable mirror root"""
    config = load_config()
    if config.get("shareable", {}).get("enabled"):
        return Path(config["shareable"]["mirror_root"])
    return None

def list_projects():
    """List all configured projects"""
    config = load_config()
    return list(config["destinations"].keys())

if __name__ == "__main__":
    # Test
    print(f"Root: {get_root()}")
    print(f"8825 destination: {get_destination('8825')}")
    print(f"Intake: {get_intake()}")
    print(f"Unknown: {get_unknown()}")
    print(f"Projects: {list_projects()}")
