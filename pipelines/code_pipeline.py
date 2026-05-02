import subprocess
import pathlib
import anthropic
import json
from tools.file_tools import list_files, read_file, write_file
from tools.shell_tools import run_linter

client = anthropic.Anthropic()
MAX_RETRIES = 3


def scan_directory(project_path: str) -> list:
    """
    Scan a directory and extract Python files with their content.
    
    Args:
        project_path: Path to scan
    
    Returns:
        List of dicts with file info and content
    """
    files = list_files(
        project_path,
        patterns=["*.py"],
        exclude_patterns=["__pycache__", ".venv", ".git", "node_modules"]
    )
    
    result = []
    for file_info in files:
        try:
            content = read_file(file_info['path'])
            result.append({
                'path': file_info['relative_path'],
                'name': file_info['name'],
                'size': file_info['size'],
                'content': content[:2000]  # Limit content size
            })
        except Exception as e:
            print(f"Error reading {file_info['path']}: {e}")
    
    return result


def run_code_pipeline(project_path: str):
    """
    Main code pipeline: scan → generate docs → lint → fix loop.
    """
    files = scan_directory(project_path)
    docs = generate_docs(files)
    
    for attempt in range(MAX_RETRIES):
        write_docs(project_path, docs)
        lint_result = run_linter(project_path)
        
        if lint_result['passed']:
            return {"status": "passed", "attempts": attempt + 1, "output": docs}
        
        # Feed lint errors back into Claude → fix → retry
        docs = fix_docs(docs, lint_result['output'])
    
    return {"status": "max_retries_reached"}


def generate_docs(files: list) -> str:
    """
    Use Claude to generate docstrings and documentation for files.
    """
    file_summary = "\n".join([
        f"- {f['path']}: {f['size']} bytes\n  {f['content'][:500]}..."
        for f in files[:5]  # Limit to first 5 files for context
    ])
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""Generate comprehensive docstrings and a README for this Python project.
Include:
1. Module-level docstrings for each file
2. Function docstrings with Args and Returns
3. Class docstrings
4. A comprehensive README.md

Files to document:
{file_summary}

Return the output as a JSON object with keys: "README.md", "docstrings" (list of file updates)"""
        }]
    )
    return response.content[0].text


def write_docs(project_path: str, docs_json: str):
    """
    Write generated documentation to project files.
    """
    try:
        docs = json.loads(docs_json)
        
        # Write README
        if "README.md" in docs:
            write_file(f"{project_path}/README.md", docs["README.md"])
        
        # Write docstrings to files
        if "docstrings" in docs:
            for file_update in docs["docstrings"]:
                if "path" in file_update and "content" in file_update:
                    write_file(f"{project_path}/{file_update['path']}", file_update["content"])
    except json.JSONDecodeError:
        # If not valid JSON, write as raw content
        write_file(f"{project_path}/GENERATED_DOCS.md", docs_json)


def fix_docs(docs: str, lint_errors: str) -> str:
    """
    Use Claude to fix documentation based on lint errors.
    """
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""The documentation/code generated had the following lint errors:

{lint_errors}

Original documentation:
{docs}

Please fix the documentation to resolve these lint errors while maintaining quality.
Return the fixed output in the same JSON format."""
        }]
    )
    return response.content[0].text