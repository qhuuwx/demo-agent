"""File operations tools for the productivity agent."""

import pathlib
import os
from typing import List, Dict, Any


def read_file(file_path: str) -> str:
    """Read the contents of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"


def write_file(file_path: str, content: str) -> bool:
    """Write content to a file. Creates directories if needed."""
    try:
        path = pathlib.Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {str(e)}")
        return False


def append_file(file_path: str, content: str) -> bool:
    """Append content to a file."""
    try:
        path = pathlib.Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error appending to file {file_path}: {str(e)}")
        return False


def list_files(directory: str, patterns: List[str] = None, exclude_patterns: List[str] = None) -> List[Dict[str, Any]]:
    """
    List files in a directory matching patterns.
    
    Args:
        directory: Path to directory
        patterns: File patterns to include (e.g., ["*.py"])
        exclude_patterns: Patterns to exclude (e.g., ["__pycache__"])
    
    Returns:
        List of dicts with file info
    """
    if patterns is None:
        patterns = ["*"]
    if exclude_patterns is None:
        exclude_patterns = []
    
    files = []
    try:
        dir_path = pathlib.Path(directory)
        
        for pattern in patterns:
            for file_path in dir_path.rglob(pattern):
                if file_path.is_file():
                    # Check if file matches any exclude pattern
                    should_exclude = False
                    for exclude in exclude_patterns:
                        if exclude in str(file_path):
                            should_exclude = True
                            break
                    
                    if not should_exclude:
                        files.append({
                            'path': str(file_path),
                            'name': file_path.name,
                            'size': file_path.stat().st_size,
                            'relative_path': str(file_path.relative_to(directory))
                        })
    except Exception as e:
        print(f"Error listing files in {directory}: {str(e)}")
    
    return files


def file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return pathlib.Path(file_path).exists()


def create_directory(directory: str) -> bool:
    """Create a directory and any parent directories."""
    try:
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {str(e)}")
        return False
