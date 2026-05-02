"""Shell execution tools for the productivity agent."""

import subprocess
from typing import Dict, Any


def run_command(command: str, cwd: str = None) -> Dict[str, Any]:
    """
    Execute a shell command and return results.
    
    Args:
        command: Command to execute
        cwd: Working directory for command
    
    Returns:
        Dict with returncode, stdout, and stderr
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': 'Command timed out',
            'success': False
        }
    except Exception as e:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': str(e),
            'success': False
        }


def run_linter(project_path: str, linter_command: str = "ruff check") -> Dict[str, Any]:
    """
    Run a linter on a project.
    
    Args:
        project_path: Path to project directory
        linter_command: Linter command to run
    
    Returns:
        Dict with lint results
    """
    result = run_command(f"{linter_command} {project_path}", cwd=project_path)
    return {
        'passed': result['returncode'] == 0,
        'output': result['stdout'],
        'errors': result['stderr'],
        **result
    }


def run_tests(project_path: str, test_command: str = "pytest") -> Dict[str, Any]:
    """
    Run tests on a project.
    
    Args:
        project_path: Path to project directory
        test_command: Test command to run
    
    Returns:
        Dict with test results
    """
    result = run_command(test_command, cwd=project_path)
    return {
        'passed': result['returncode'] == 0,
        'output': result['stdout'],
        'errors': result['stderr'],
        **result
    }
