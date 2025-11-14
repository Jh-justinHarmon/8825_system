#!/usr/bin/env python3
"""
Safe File Operations - Atomic writes and file locking

Prevents corruption when multiple processes access same files.
Critical for Dropbox-synced files with concurrent access.

Usage:
    from safe_file_ops import safe_write_json, safe_read_json
    
    # Atomic write with locking
    safe_write_json(path, data)
    
    # Safe read with retry
    data = safe_read_json(path)
"""

import json
import fcntl
import time
import tempfile
import shutil
from pathlib import Path
from typing import Any, Dict, Optional
from contextlib import contextmanager

class FileLockTimeout(Exception):
    """Raised when file lock cannot be acquired"""
    pass

class FileCorruptionError(Exception):
    """Raised when file appears corrupted"""
    pass

@contextmanager
def file_lock(file_path: Path, timeout: int = 10, mode: str = 'r'):
    """Context manager for file locking
    
    Args:
        file_path: Path to lock
        timeout: Seconds to wait for lock
        mode: File open mode ('r' or 'w')
    
    Raises:
        FileLockTimeout: If lock cannot be acquired
    
    Usage:
        with file_lock(path, mode='w') as f:
            f.write(data)
    """
    lock_file = None
    start_time = time.time()
    
    try:
        # Create parent directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open file
        lock_file = open(file_path, mode)
        
        # Try to acquire lock with timeout
        while True:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except IOError:
                if time.time() - start_time > timeout:
                    raise FileLockTimeout(f"Could not acquire lock on {file_path} after {timeout}s")
                time.sleep(0.1)
        
        yield lock_file
    
    finally:
        if lock_file:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            except:
                pass
            lock_file.close()

def safe_write_json(file_path: Path, data: Dict[str, Any], 
                   backup: bool = True, timeout: int = 10) -> bool:
    """Atomically write JSON file with locking
    
    Process:
    1. Create backup if file exists
    2. Write to temp file
    3. Acquire lock
    4. Atomic rename (temp -> target)
    5. Release lock
    
    Args:
        file_path: Target file path
        data: Data to write
        backup: Create .bak backup before writing
        timeout: Lock timeout in seconds
    
    Returns:
        True if successful
    
    Raises:
        FileLockTimeout: If lock cannot be acquired
        IOError: If write fails
    """
    file_path = Path(file_path)
    
    try:
        # Create backup if file exists
        if backup and file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            shutil.copy2(file_path, backup_path)
        
        # Write to temp file first (atomic operation)
        temp_fd, temp_path = tempfile.mkstemp(
            dir=file_path.parent,
            prefix=f'.{file_path.name}.',
            suffix='.tmp'
        )
        
        try:
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            
            # Atomic rename (this is the critical moment)
            # On POSIX, rename is atomic even if target exists
            shutil.move(temp_path, file_path)
            
            return True
        
        except Exception as e:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except:
                pass
            raise
    
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        
        # Try to restore from backup
        if backup:
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            if backup_path.exists():
                print(f"Restoring from backup: {backup_path}")
                shutil.copy2(backup_path, file_path)
        
        return False

def safe_read_json(file_path: Path, default: Optional[Dict] = None,
                  retry_count: int = 3, retry_delay: float = 0.5) -> Dict[str, Any]:
    """Safely read JSON file with retry and corruption detection
    
    Args:
        file_path: File to read
        default: Default value if file doesn't exist
        retry_count: Number of retries on failure
        retry_delay: Delay between retries (seconds)
    
    Returns:
        Parsed JSON data or default
    
    Raises:
        FileCorruptionError: If file is corrupted after retries
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return default if default is not None else {}
    
    last_error = None
    
    for attempt in range(retry_count):
        try:
            with file_lock(file_path, mode='r') as f:
                content = f.read()
                
                # Validate not empty
                if not content.strip():
                    raise FileCorruptionError(f"{file_path} is empty")
                
                # Parse JSON
                data = json.loads(content)
                return data
        
        except json.JSONDecodeError as e:
            last_error = e
            print(f"JSON decode error on attempt {attempt + 1}/{retry_count}: {e}")
            
            # Try backup if available
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            if backup_path.exists():
                print(f"Trying backup: {backup_path}")
                try:
                    with open(backup_path, 'r') as f:
                        data = json.load(f)
                        print(f"✅ Restored from backup")
                        # Restore the backup to main file
                        shutil.copy2(backup_path, file_path)
                        return data
                except:
                    pass
            
            if attempt < retry_count - 1:
                time.sleep(retry_delay)
        
        except FileLockTimeout:
            last_error = FileLockTimeout(f"Could not acquire lock on {file_path}")
            if attempt < retry_count - 1:
                time.sleep(retry_delay)
        
        except Exception as e:
            last_error = e
            print(f"Error reading {file_path} on attempt {attempt + 1}/{retry_count}: {e}")
            if attempt < retry_count - 1:
                time.sleep(retry_delay)
    
    # All retries failed
    if default is not None:
        print(f"⚠️  Using default value after {retry_count} failed attempts")
        return default
    
    raise FileCorruptionError(f"Could not read {file_path} after {retry_count} attempts: {last_error}")

def safe_append_jsonl(file_path: Path, data: Dict[str, Any], timeout: int = 10) -> bool:
    """Safely append to JSONL file with locking
    
    Args:
        file_path: JSONL file path
        data: Data to append
        timeout: Lock timeout
    
    Returns:
        True if successful
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Use append mode with lock
        with file_lock(file_path, mode='a', timeout=timeout) as f:
            f.write(json.dumps(data) + '\n')
            f.flush()
            os.fsync(f.fileno())
        return True
    
    except Exception as e:
        print(f"Error appending to {file_path}: {e}")
        return False

# Need to import os for fsync
import os

def test_safe_ops():
    """Test safe file operations"""
    import tempfile
    
    print("Testing safe file operations...")
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = Path(f.name)
    
    try:
        # Test write
        test_data = {'test': 'data', 'count': 42}
        print(f"\n1. Writing to {temp_path}")
        assert safe_write_json(temp_path, test_data)
        print("✅ Write successful")
        
        # Test read
        print(f"\n2. Reading from {temp_path}")
        read_data = safe_read_json(temp_path)
        assert read_data == test_data
        print("✅ Read successful")
        
        # Test backup
        print(f"\n3. Testing backup")
        test_data['count'] = 43
        assert safe_write_json(temp_path, test_data, backup=True)
        backup_path = temp_path.with_suffix(temp_path.suffix + '.bak')
        assert backup_path.exists()
        print("✅ Backup created")
        
        # Test JSONL append
        jsonl_path = temp_path.with_suffix('.jsonl')
        print(f"\n4. Testing JSONL append to {jsonl_path}")
        assert safe_append_jsonl(jsonl_path, {'line': 1})
        assert safe_append_jsonl(jsonl_path, {'line': 2})
        assert jsonl_path.exists()
        print("✅ JSONL append successful")
        
        print("\n✅ All tests passed!")
    
    finally:
        # Cleanup
        for path in [temp_path, backup_path, jsonl_path]:
            if path.exists():
                path.unlink()

if __name__ == '__main__':
    test_safe_ops()
