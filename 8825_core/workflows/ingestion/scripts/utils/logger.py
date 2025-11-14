#!/usr/bin/env python3
"""
Logger utility for 8825 Ingestion Engine
"""

import sys
from datetime import datetime
from pathlib import Path

# Global log file handle
_log_file = None

def setup_logging(log_path):
    """Setup logging to file"""
    global _log_file
    _log_file = open(log_path, 'a')

def log(message, level="INFO"):
    """
    Log message to console and file
    
    Args:
        message: Message to log
        level: Log level (INFO, WARN, ERROR, DEBUG)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    
    # Print to console
    print(log_message)
    
    # Write to file if setup
    if _log_file:
        _log_file.write(log_message + "\n")
        _log_file.flush()

def close_logging():
    """Close log file"""
    global _log_file
    if _log_file:
        _log_file.close()
        _log_file = None
